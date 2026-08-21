import os
import sys
import io
import time
from flask import Flask, render_template_string, request, jsonify, Response
import pyautogui

# Ultimate Performance Configurations
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

app = Flask(__name__)

SECRET_URL_PATH = "remote"
SECURITY_TOKEN = "alpha_secure_99"
CUSTOM_PORT = 38491

IIS_MASK_TEMPLATE = '''<!DOCTYPE html><html><head><title>IIS Windows Server</title><style>body { font-family: 'Segoe UI', sans-serif; background-color: #244976; color: #fff; padding: 40px; } .container { max-width: 600px; margin: 0 auto; } h1 { font-size: 42px; font-weight: 300; } p { font-size: 16px; color: #a9c7ed; }</style></head><body><div class="container"><h1>Internet Information Services</h1><p>Static distribution block active.</p></div></body></html>'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Enterprise System Controller</title>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <style>
        :root {
            --bg-color: #090d16;
            --card-color: #131c2e;
            --accent-color: #2563eb;
            --text-color: #f1f5f9;
            --danger-color: #dc2626;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color); color: var(--text-color);
            margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center;
            user-select: none; -webkit-user-select: none; overflow-x: hidden;
        }
        .section { width: 100%; max-width: 440px; background: var(--card-color); border-radius: 12px; padding: 14px; margin-bottom: 12px; box-sizing: border-box; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4); }
        .section-title { font-size: 11px; text-transform: uppercase; letter-spacing: 0.07em; color: #64748b; margin-bottom: 10px; font-weight: 700; }
        .tab-bar { display: flex; gap: 8px; margin-bottom: 10px; width: 100%; }
        .tab-btn { flex: 1; padding: 10px; background: #1e293b; border-radius: 6px; font-size: 13px; font-weight: bold; text-align: center; color: white; cursor: pointer; border: none; }
        .tab-btn.active { background: var(--accent-color); }
        .stream-wrapper { position: relative; width: 100%; overflow: hidden; border-radius: 8px; border: 1px solid #1e293b; background: #000; }
        #stream-view { width: 100%; display: block; object-fit: contain; transform-origin: top left; transition: transform 0.1s ease; }
        .slider-container { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 8px; font-size: 12px; color: #94a3b8; }
        .zoom-slider { flex: 1; accent-color: var(--accent-color); }
        #trackpad { height: 160px; background: #020617; border: 2px dashed #1e293b; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #475569; font-size: 13px; touch-action: none; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        button { background: #1e293b; color: var(--text-color); border: none; padding: 12px; font-size: 14px; border-radius: 6px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        button:active { background: var(--accent-color); }
        .file-item { display: flex; justify-content: space-between; padding: 8px; background: #020617; margin-bottom: 4px; border-radius: 4px; font-size: 13px; }
        #camera-preview { width: 100%; height: 140px; background: #020617; border-radius: 6px; display: none; object-fit: cover; margin-top: 8px; }
        
        /* --- IMMERSIVE FULLSCREEN LAYER --- */
        #immersive-viewport { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #000; z-index: 99999; overflow: hidden; touch-action: none; }
        #fullscreen-canvas { width: 100%; height: 100%; object-fit: contain; }
        #action-orb { position: absolute; top: 20px; left: 20px; width: 50px; height: 50px; background: rgba(37, 99, 235, 0.6); border: 2px solid rgba(255,255,255,0.4); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.5); z-index: 100001; touch-action: none; }
        #orb-menu { display: none; position: absolute; top: 80px; left: 20px; background: rgba(19, 28, 46, 0.95); border: 1px solid #1e293b; border-radius: 8px; padding: 10px; width: 160px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 100002; }
        .orb-menu-btn { width: 100%; margin-bottom: 6px; padding: 8px; font-size: 12px; }
        #floating-keyboard-wrapper { display: none; position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); background: rgba(9, 13, 22, 0.95); border: 1px solid #1e293b; border-radius: 10px; padding: 10px; width: 90%; max-width: 500px; z-index: 100003; }
    </style>
</head>
<body>
    <!-- Monitor Active View Windows -->
    <div class="section">
        <div class="section-title">Select Active View Window</div>
        <div class="tab-bar">
            <button class="tab-btn active" onclick="switchMonitor(0)">Monitor 1</button>
            <button class="tab-btn" onclick="switchMonitor(1)">Monitor 2</button>
        </div>
        <div class="stream-wrapper">
            <img id="stream-view" src="/api/stream?monitor=0&key={{ auth_key }}" alt="Desktop Display Stream">
        </div>
        <div class="slider-container">
            <span>Zoom View:</span>
            <input type="range" class="zoom-slider" min="1" max="3" step="0.1" value="1" oninput="adjustZoom(this.value)">
        </div>
        <!-- Live Widescreen Toggle Button Included Safely -->
        <button onclick="launchImmersiveMode()" style="width: 100%; margin-top: 10px; padding: 14px; background: var(--accent-color);">Launch Fullscreen Immersive Mode</button>
    </div>

    <!-- RESTORED: Dedicated Precision Trackpad Workspace Box -->
    <div class="section">
        <div class="section-title">Precision Trackpad Surface</div>
        <div id="trackpad">Slide finger to drive active cursor</div>
        <div class="grid-2" style="margin-top: 10px;">
            <button id="btn-left-click">Left Click</button>
            <button id="btn-right-click">Right Click</button>
        </div>
    </div>

    <!-- Active Hardware Streams (Preserved) -->
    <div class="section">
        <div class="section-title">Hardware Streams to Host PC</div>
        <button id="btn-toggle-hardware" style="width: 100%;">Launch Phone Camera and Mic Stream</button>
        <video id="camera-preview" autoplay playsinline muted></video>
    </div>
    <!-- Application Control Matrix Macros (Preserved) -->
    <div class="section">
        <div class="section-title">Application Control Macros</div>
        <div class="grid-3">
            <button onclick="sendAction('macro', {app: 'chrome'})">Chrome</button>
            <button onclick="sendAction('macro', {app: 'youtube'})">YouTube</button>
            <button onclick="sendAction('macro', {app: 'netflix'})">Netflix</button>
        </div>
    </div>

    <!-- System Media Control Layout Row (Preserved) -->
    <div class="section">
        <div class="section-title">System Media Control Panel</div>
        <div class="grid-3">
            <button onclick="sendAction('media', {action: 'prev'})">Prev</button>
            <button onclick="sendAction('media', {action: 'playpause'})">Play</button>
            <button onclick="sendAction('media', {action: 'next'})">Next</button>
        </div>
        <div class="grid-2" style="margin-top: 8px;">
            <button onclick="sendAction('media', {action: 'voldown'})">Vol -</button>
            <button onclick="sendAction('media', {action: 'volup'})">Vol +</button>
        </div>
    </div>

    <!-- Character Text Buffers Layout Frame (Preserved) -->
    <div class="section">
        <div class="section-title">Text Input and Hotkey Matrix</div>
        <div style="display: flex; gap: 8px; margin-bottom: 8px;">
            <input type="text" id="keyboardInput" placeholder="Type letters/numbers here...">
            <button id="btn-send-text">Send</button>
        </div>
        <div class="grid-3">
            <button onclick="sendAction('key', {key: 'enter'})">Enter</button>
            <button onclick="sendAction('key', {key: 'backspace'})">Back</button>
            <button onclick="sendAction('key', {key: 'space'})">Space</button>
        </div>
    </div>

    <!-- File Workspace Managers Panel (Preserved) -->
    <div class="section">
        <div class="section-title">C:\\ Remote File Workspace</div>
        <div id="file-list">Accessing storage partition blocks...</div>
    </div>

    <!-- IMMERSIVE WIDESCREEN VIEWPORT ENGINE PANEL -->
    <div id="immersive-viewport">
        <div id="action-orb">MENU</div>
        <div id="orb-menu">
            <button class="orb-menu-btn" onclick="cycleMonitor()">Switch Monitor</button>
            <button class="orb-menu-btn" onclick="toggleFloatingKeyboard()">Keyboard Input</button>
            <button class="orb-menu-btn" onclick="adjustOrbOpacity()">Fade Ball</button>
            <button class="orb-menu-btn" style="background:var(--danger-color);" onclick="exitImmersiveMode()">Exit Fullscreen</button>
        </div>
        <div id="floating-keyboard-wrapper">
            <div style="display:flex; gap:6px; margin-bottom:6px;">
                <input type="text" id="floatingInput" style="flex:1; padding:8px; border-radius:4px; border:1px solid #334155; background:#020617; color:white;" placeholder="Type data parameters...">
                <button onclick="sendFloatingText()">Send</button>
            </div>
        </div>
        <img id="fullscreen-canvas" src="" alt="Live Desktop Environment Grid">
    </div>
    <script>
        const authKey = "{{ auth_key }}";
        let currentMonitor = 0;
        let orbOpacityState = 0.6;
        let lastTouchX = 0, lastTouchY = 0;
        let lastTrackX = 0, lastTrackY = 0;
        let isDraggingMouse = false;

        function sendAction(endpoint, data = {}) {
            return fetch('/api/' + endpoint + '?key=' + authKey, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        function switchMonitor(index) {
            currentMonitor = index;
            document.querySelectorAll('.tab-btn').forEach((btn, i) => { btn.classList.toggle('active', i === index); });
            document.getElementById('stream-view').src = "/api/stream?monitor=" + index + "&key=" + authKey;
        }

        function adjustZoom(val) {
            const view = document.getElementById('stream-view');
            view.style.transform = "scale(" + val + ")";
            view.style.transformOrigin = val > 1 ? "center center" : "top left";
        }

        // --- TRACKPAD MOUSEPAD LOGIC RETURNED AND BOUND PROPERLY ---
        const trackpad = document.getElementById('trackpad');
        trackpad.addEventListener('touchstart', (e) => {
            if(e.touches.length === 1) {
                lastTrackX = e.touches[0].clientX;
                lastTrackY = e.touches[0].clientY;
            }
        }, {passive: true});

        trackpad.addEventListener('touchmove', (e) => {
            if(e.touches.length === 1) {
                const cx = e.touches[0].clientX; const cy = e.touches[0].clientY;
                sendAction('mousemove', { dx: (cx - lastTrackX) * 4.5, dy: (cy - lastTrackY) * 4.5 });
                lastTrackX = cx; lastTrackY = cy;
            }
        }, {passive: false});

        document.getElementById('btn-left-click').addEventListener('click', () => sendAction('click', {btn: 'left'}));
        document.getElementById('btn-right-click').addEventListener('click', () => sendAction('click', {btn: 'right'}));
        document.getElementById('btn-send-text').addEventListener('click', () => {
            const input = document.getElementById('keyboardInput');
            if(input.value) { sendAction('type', { text: input.value }); input.value = ''; }
        });

        // --- IMMERSIVE MODE METHODS ---
        function launchImmersiveMode() {
            document.getElementById('immersive-viewport').style.display = 'block';
            document.getElementById('fullscreen-canvas').src = "/api/stream?monitor=" + currentMonitor + "&key=" + authKey;
            if (screen.orientation && screen.orientation.lock) { screen.orientation.lock('landscape').catch(() => {}); }
            if (document.documentElement.requestFullscreen) { document.documentElement.requestFullscreen(); }
        }

        function exitImmersiveMode() {
            document.getElementById('immersive-viewport').style.display = 'none';
            document.getElementById('fullscreen-canvas').src = "";
            if (document.exitFullscreen) { document.exitFullscreen().catch(() => {}); }
            if (screen.orientation && screen.orientation.unlock) { screen.orientation.unlock(); }
        }

        const canvas = document.getElementById('fullscreen-canvas');
        canvas.addEventListener('touchstart', (e) => { if(e.touches.length===1){ lastTouchX=e.touches.clientX; lastTouchY=e.touches.clientY; isDraggingMouse=false; } });
        canvas.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1) {
                isDraggingMouse = true;
                const cx = e.touches.clientX; const cy = e.touches.clientY;
                sendAction('mousemove', { dx: (cx - lastTouchX) * 3.5, dy: (cy - lastTouchY) * 3.5 });
                lastTouchX = cx; lastTouchY = cy;
            }
        });
        canvas.addEventListener('touchend', (e) => {
            if (!isDraggingMouse) {
                const rect = canvas.getBoundingClientRect();
                sendAction('directclick', { x: (lastTouchX - rect.left) / rect.width, y: (lastTouchY - rect.top) / rect.height, monitor: currentMonitor });
            }
        });

        const orb = document.getElementById('action-orb'); const menu = document.getElementById('orb-menu');
        orb.addEventListener('click', (e) => { e.stopPropagation(); menu.style.display = menu.style.display === 'block' ? 'none' : 'block'; });
        orb.addEventListener('touchmove', (e) => { if(e.touches.length===1){ orb.style.left=e.touches.clientX-25+'px'; orb.style.top=e.touches.clientY-25+'px'; menu.style.left=orb.style.left; menu.style.top=parseInt(orb.style.top)+60+'px'; } });

        function cycleMonitor() { currentMonitor = currentMonitor === 0 ? 1 : 0; document.getElementById('fullscreen-canvas').src = "/api/stream?monitor=" + currentMonitor + "&key=" + authKey; menu.style.display = 'none'; }
        function toggleFloatingKeyboard() { const kb = document.getElementById('floating-keyboard-wrapper'); kb.style.display = kb.style.display==='block'?'none':'block'; menu.style.display = 'none'; }
        function adjustOrbOpacity() { orbOpacityState = orbOpacityState <= 0.2 ? 0.8 : orbOpacityState - 0.2; orb.style.background = `rgba(37, 99, 235, ${orbOpacityState})`; }
        function sendFloatingText() { const el = document.getElementById('floatingInput'); if(el.value){ sendAction('type', { text: el.value }); el.value = ''; } }

        document.getElementById('btn-toggle-hardware').addEventListener('click', async () => {
            try { const s = await navigator.mediaDevices.getUserMedia({ video: true, audio: true }); const v = document.getElementById('camera-preview'); v.srcObject = s; v.style.display = "block"; } catch (e) {}
        });

        async function loadFiles() {
            try {
                const res = await fetch('/api/files?key=' + authKey); const data = await res.json();
                const container = document.getElementById('file-list'); container.innerHTML = '';
                data.files.forEach(f => { container.innerHTML += `<div class="file-item"><span>${f.name}</span><button>Open</button></div>`; });
            } catch(e) {}
        }
        loadFiles();
    </script>
</body>
</html>
'''
def verify_security(): return request.args.get('key') == SECURITY_TOKEN
@app.route('/')
def handle_root_mask(): return render_template_string(IIS_MASK_TEMPLATE)
@app.route(f'/{SECRET_URL_PATH}')
def handle_authenticated_console():
    if not verify_security(): return render_template_string(IIS_MASK_TEMPLATE), 403
    return render_template_string(DASHBOARD_TEMPLATE, auth_key=SECURITY_TOKEN)

@app.route('/api/mousemove', methods=['POST'])
def mouse_move():
    if not verify_security(): return "Unauthorized", 403
    pyautogui.moveRel(int(request.json['dx']), int(request.json['dy']))
    return jsonify(status="success")

@app.route('/api/click', methods=['POST'])
def mouse_click():
    if not verify_security(): return "Unauthorized", 403
    pyautogui.click(button=request.json.get('btn', 'left'))
    return jsonify(status="success")

@app.route('/api/directclick', methods=['POST'])
def direct_screen_click():
    if not verify_security(): return "Unauthorized", 403
    import screeninfo
    try:
        monitors = screeninfo.get_monitors()
        m_idx = int(request.json.get('monitor', 0))
        m = monitors[m_idx] if m_idx < len(monitors) else monitors
        tx = m.x + int(request.json['x'] * m.width)
        ty = m.y + int(request.json['y'] * m.height)
        pyautogui.click(tx, ty)
    except:
        w, h = pyautogui.size()
        pyautogui.click(int(request.json['x'] * w), int(request.json['y'] * h))
    return jsonify(status="success")

@app.route('/api/type', methods=['POST'])
def text_type():
    if not verify_security(): return "Unauthorized", 403
    pyautogui.write(request.json.get('text', ''))
    return jsonify(status="success")

@app.route('/api/key', methods=['POST'])
def key_press():
    if not verify_security(): return "Unauthorized", 403
    pyautogui.press(request.json.get('key'))
    return jsonify(status="success")
@app.route('/api/media', methods=['POST'])
def media_control():
    if not verify_security(): return "Unauthorized", 403
    mapping = {'playpause':'playpause', 'next':'nexttrack', 'prev':'prevtrack', 'volup':'volumeup', 'voldown':'volumedown'}
    action = request.json.get('action')
    if action in mapping: pyautogui.press(mapping[action])
    return jsonify(status="success")

@app.route('/api/macro', methods=['POST'])
def application_macros():
    if not verify_security(): return "Unauthorized", 403
    t = request.json.get('app')
    if t == 'chrome': os.system("start chrome")
    elif t == 'youtube': os.system("start chrome youtube.com")
    elif t == 'netflix': os.system("start chrome netflix.com")
    return jsonify(status="success")

@app.route('/api/files')
def list_files():
    if not verify_security(): return "Unauthorized", 403
    try:
        items = [{"name": i} for i in os.listdir("C:\\\\")[:5]]
        return jsonify(files=items)
    except: return jsonify(files=[{"name": "System Root Secured"}])

def generate_monitor_frame(monitor_id):
    import mss
    from PIL import Image
    with mss.mss() as sct:
        while True:
            try:
                monitors = sct.monitors
                target_idx = (monitor_id + 1) if (monitor_id + 1) < len(monitors) else 1
                target = monitors[target_idx]
                
                sct_img = sct.grab(target)
                img = io.BytesIO(mss.tools.to_png(sct_img.rgb, sct_img.size))
                
                pil_img = Image.open(img).resize((1920, 1080))
                frame_buffer = io.BytesIO()
                pil_img.save(frame_buffer, format='JPEG', quality=85)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_buffer.getvalue() + b'\r\n')
            except: pass
            time.sleep(0.04)

@app.route('/api/stream')
def video_feed_stream():
    if not verify_security(): return "Unauthorized", 403
    return Response(generate_monitor_frame(int(request.args.get('monitor', 0))), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CUSTOM_PORT, debug=False, threaded=True)