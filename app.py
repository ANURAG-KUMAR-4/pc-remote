import os, sys, io, time
from flask import Flask, render_template_string, request, jsonify, Response
import win32api, win32con, win32service

app = Flask(__name__)
CUSTOM_PORT = 38491

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>PC Remote Pro Master</title>
    <style>
        :root { --bg: #090d16; --card: #131c2e; --accent: #2563eb; --text: #f1f5f9; --danger: #dc2626; }
        body { font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center; user-select: none; }
        .section { width: 100%; max-width: 440px; background: var(--card); border-radius: 12px; padding: 14px; margin-bottom: 12px; box-sizing: border-box; }
        .section-title { font-size: 11px; text-transform: uppercase; color: #64748b; margin-bottom: 10px; font-weight: 700; }
        .tab-bar { display: flex; gap: 8px; margin-bottom: 10px; }
        .tab-btn { flex: 1; padding: 10px; background: #1e293b; border-radius: 6px; color: white; border: none; font-weight: bold; }
        .tab-btn.active { background: var(--accent); }
        #view { width: 100%; border-radius: 8px; display: block; background: #000; border: 1px solid #333; }
        #pad { height: 180px; background: #020617; border: 2px dashed #1e293b; border-radius: 12px; margin-top: 10px; display: flex; align-items: center; justify-content: center; color: #475569; touch-action: none; }
        .grid { display: grid; gap: 8px; margin-top: 10px; }
        button { background: #1e293b; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: 600; cursor: pointer; }
        button:active { background: var(--accent); }
        input { width: 60%; padding: 12px; background: #000; color: #fff; border: 1px solid #444; border-radius: 6px; }
        #camera-preview { width: 100%; height: 140px; background: #000; border-radius: 6px; display: none; object-fit: cover; margin-top: 8px; }
        .file-item { display: flex; justify-content: space-between; padding: 8px; background: #020617; margin-bottom: 4px; border-radius: 4px; font-size: 13px; }
        #immersive-viewport { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #000; z-index: 99999; }
        #fs-canvas { width: 100%; height: 100%; object-fit: contain; }
        #orb { position: absolute; top: 20px; left: 20px; width: 50px; height: 50px; background: rgba(37,99,235,0.6); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 100001; color: white; }
    </style>
</head>
'''
DASHBOARD_TEMPLATE += '''
<body>
    <div class="section">
        <div class="section-title">Live Desktop</div>
        <div class="tab-bar">
            <button class="tab-btn active" onclick="sm(0)">Screen 1</button>
            <button class="tab-btn" onclick="sm(1)">Screen 2</button>
        </div>
        <img id="view" src="">
        <button onclick="launchFS()" style="width:100%; margin-top:10px; background:var(--accent);">Launch Fullscreen Mode</button>
    </div>

    <div class="section">
        <div id="pad">TRACKPAD</div>
        <div class="grid" style="grid-template-columns: 1fr 1fr;">
            <button onclick="act('click',{b:'l'})">LEFT CLICK</button>
            <button onclick="act('click',{b:'r'})">RIGHT CLICK</button>
        </div>
    </div>

    <div class="section">
        <div class="section-title">App Macros & Hardware</div>
        <div class="grid" style="grid-template-columns: repeat(3, 1fr);">
            <button onclick="act('macro',{a:'chrome'})">Chrome</button>
            <button onclick="act('macro',{a:'yt'})">YouTube</button>
            <button onclick="act('macro',{a:'nf'})">Netflix</button>
        </div>
        <button id="cam-btn" onclick="startCam()" style="width:100%; margin-top:10px;">Start Camera/Mic</button>
        <video id="camera-preview" autoplay playsinline muted></video>
    </div>
'''
DASHBOARD_TEMPLATE += '''
    <div class="section">
        <div class="section-title">Keyboard & Modifiers</div>
        <div style="display:flex; gap:5px;"><input type="text" id="k"><button onclick="sendT()" style="flex:1;">SEND</button></div>
        <div class="grid" style="grid-template-columns: repeat(4, 1fr);">
            <button onclick="act('key',{k:'ctrl'})">Ctrl</button>
            <button onclick="act('key',{k:'alt'})">Alt</button>
            <button onclick="act('key',{k:'fn'})">Fn</button>
            <button onclick="act('key',{k:'caps'})">Caps</button>
        </div>
        <div class="grid" style="grid-template-columns: repeat(3, 1fr);">
            <button onclick="act('key',{k:'enter'})">Enter</button>
            <button onclick="act('key',{k:'backspace'})">Del</button>
            <button onclick="act('key',{k:'space'})">Space</button>
        </div>
    </div>

    <div class="section">
        <div class="section-title">Media & Files</div>
        <div class="grid" style="grid-template-columns: repeat(3, 1fr);">
            <button onclick="act('media',{a:'prev'})">⏮ Prev</button>
            <button onclick="act('media',{a:'pp'})">⏯ Play</button>
            <button onclick="act('media',{a:'next'})">⏭ Next</button>
        </div>
        <div class="grid" style="grid-template-columns: 1fr 1fr; margin-top: 8px;">
            <button onclick="act('media',{a:'voldown'})">Vol -</button>
            <button onclick="act('media',{a:'volup'})">Vol +</button>
        </div>
        <div id="file-list" style="margin-top:10px;">Loading files...</div>
    </div>

    <div id="immersive-viewport">
        <div id="orb" onclick="exitFS()">Exit</div>
        <img id="fs-canvas" src="">
    </div>
'''
DASHBOARD_TEMPLATE += '''
    <script>
        let currentMonitor = 0; let lastX, lastY;
        function act(e, d={}) { fetch('/api/'+e, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(d)}); }
        function sm(i) { currentMonitor = i; document.getElementById('view').src = "/stream?m="+i; }
        
        const pad = document.getElementById('pad');
        pad.addEventListener('touchstart', e => { lastX = e.touches[0].clientX; lastY = e.touches[0].clientY; });
        pad.addEventListener('touchmove', e => {
            e.preventDefault();
            let dx = (e.touches[0].clientX - lastX) * 3;
            let dy = (e.touches[0].clientY - lastY) * 3;
            act('move', {dx, dy});
            lastX = e.touches[0].clientX; lastY = e.touches[0].clientY;
        }, {passive:false});

        function sendT() { const i = document.getElementById('k'); act('type', {t: i.value}); i.value=''; }
        function launchFS() { document.getElementById('immersive-viewport').style.display='block'; document.getElementById('fs-canvas').src="/stream?m="+currentMonitor; }
        function exitFS() { document.getElementById('immersive-viewport').style.display='none'; }
        
        async function startCam() {
            const s = await navigator.mediaDevices.getUserMedia({video:true, audio:true});
            const v = document.getElementById('camera-preview'); v.srcObject = s; v.style.display="block";
        }

        async function loadFiles() {
            const r = await fetch('/api/files'); const d = await r.json();
            const c = document.getElementById('file-list'); c.innerHTML = '';
            d.files.forEach(f => { c.innerHTML += `<div class="file-item"><span>${f.name}</span><button>Get</button></div>`; });
        }
        window.onload = () => { sm(0); loadFiles(); };
    </script>
</body></html>
'''
VK = {'enter':0x0D, 'backspace':0x08, 'ctrl':0x11, 'alt':0x12, 'space':0x20, 'caps':0x14}

@app.route('/')
def index(): return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/move', methods=['POST'])
def move():
    d = request.json
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(d['dx']), int(d['dy']), 0, 0)
    return "ok"

@app.route('/api/click', methods=['POST'])
def click():
    b = request.json['b']; down = win32con.MOUSEEVENTF_LEFTDOWN if b=='l' else win32con.MOUSEEVENTF_RIGHTDOWN
    up = win32con.MOUSEEVENTF_LEFTUP if b=='l' else win32con.MOUSEEVENTF_RIGHTUP
    win32api.mouse_event(down,0,0,0,0); win32api.mouse_event(up,0,0,0,0); return "ok"

@app.route('/api/type', methods=['POST'])
def type_t():
    for c in request.json['t']:
        vk = win32api.VkKeyScan(c)
        if vk != -1: win32api.keybd_event(vk & 0xFF,0,0,0); win32api.keybd_event(vk & 0xFF,0,win32con.KEYEVENTF_KEYUP,0)
    return "ok"

@app.route('/api/key', methods=['POST'])
def key_p():
    v = VK.get(request.json['k'])
    if v: win32api.keybd_event(v,0,0,0); win32api.keybd_event(v,0,win32con.KEYEVENTF_KEYUP,0)
    return "ok"

@app.route('/api/macro', methods=['POST'])
def macro():
    a = request.json['a']
    if a == 'chrome': os.system("start chrome")
    elif a == 'yt': os.system("start chrome youtube.com")
    elif a == 'nf': os.system("start chrome netflix.com")
    return "ok"

@app.route('/api/media', methods=['POST'])
def media():
    m = {'volup':0xAF, 'voldown':0xAE, 'pp':0xB3}
    win32api.keybd_event(m[request.json['a']],0,0,0)
    return "ok"

@app.route('/api/files')
def list_f():
    items = [{"name": i} for i in os.listdir("C:\\\\")[:5]]
    return jsonify(files=items)

def gen(m_id):
    import mss
    from PIL import Image
    with mss.mss() as sct:
        while True:
            try:
                img = sct.grab(sct.monitors[m_id+1])
                p_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX").resize((1024, 576))
                buf = io.BytesIO(); p_img.save(buf, format='JPEG', quality=60)
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.getvalue() + b'\r\n')
            except: pass
            time.sleep(0.04)

@app.route('/stream')
def stream():
    return Response(gen(int(request.args.get('m', 0))), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=38491, threaded=True)