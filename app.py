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
    <link rel="manifest" href="data:application/manifest+json,{"name":"PC Remote","short_name":"PCRemote","start_url":"/remote?key=alpha_secure_99","display":"standalone","background_color":"#090d16","theme_color":"#090d16"}">

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
        .section {
            width: 100%; max-width: 440px; background: var(--card-color);
            border-radius: 12px; padding: 14px; margin-bottom: 12px; box-sizing: border-box;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4);
        }
        .section-title {
            font-size: 11px; text-transform: uppercase; letter-spacing: 0.07em; color: #64748b; margin-bottom: 10px; font-weight: 700;
        }
        .tab-bar { display: flex; gap: 8px; margin-bottom: 10px; width: 100%; }
        .tab-btn { flex: 1; padding: 10px; background: #1e293b; border-radius: 6px; font-size: 13px; font-weight: bold; text-align: center; color: white; cursor: pointer; border: none; }
        .tab-btn.active { background: var(--accent-color); }
        .stream-wrapper { position: relative; width: 100%; overflow: hidden; border-radius: 8px; border: 1px solid #1e293b; background: #000; }
        #stream-view { width: 100%; display: block; object-fit: contain; transform-origin: top left; transition: transform 0.1s ease; }
        .slider-container { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 8px; font-size: 12px; color: #94a3b8; }
        .zoom-slider { flex: 1; accent-color: var(--accent-color); }
        #trackpad {
            height: 160px; background: #020617; border: 2px dashed #1e293b; border-radius: 8px;
            display: flex; align-items: center; justify-content: center; color: #475569; font-size: 13px; touch-action: none;
        }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        button {
            background: #1e293b; color: var(--text-color); border: none; padding: 12px; font-size: 14px; border-radius: 6px;
            font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center;
        }
        button:active { background: var(--accent-color); }
        .file-item { display: flex; justify-content: space-between; padding: 8px; background: #020617; margin-bottom: 4px; border-radius: 4px; font-size: 13px; }
    </style>
</head>
<body>
    <!-- Monitor Tabs -->
    <div class="section">
        <div class="section-title">Select Active View Window</div>
        <div class="tab-bar">
            <button class="tab-btn active" onclick="switchMonitor(0)">🖥️ Monitor 1</button>
            <button class="tab-btn" onclick="switchMonitor(1)">🖥️ Monitor 2</button>
        </div>
        <div class="stream-wrapper">
            <img id="stream-view" src="/api/stream?monitor=0&key={{ auth_key }}" alt="Desktop Display Stream">
        </div>
        <div class="slider-container">
            <span>🔎 Zoom View:</span>
            <input type="range" class="zoom-slider" min="1" max="3" step="0.1" value="1" oninput="adjustZoom(this.value)">
        </div>
    </div>

    <!-- Precision Trackpad -->
    <div class="section">
        <div class="section-title">Precision Trackpad Surface</div>
        <div id="trackpad">Slide finger to drive active cursor</div>
        <div class="grid-2" style="margin-top: 10px;">
            <button id="btn-left-click">Left Click</button>
            <button id="btn-right-click">Right Click</button>
        </div>
    </div>

    <!-- Macros -->
    <div class="section">
        <div class="section-title">Application Control Macros</div>
        <div class="grid-3">
            <button onclick="sendAction('macro', {app: 'chrome'})">🌐 Chrome</button>
            <button onclick="sendAction('macro', {app: 'youtube'})">📺 YouTube</button>
            <button onclick="sendAction('macro', {app: 'netflix'})">🎬 Netflix</button>
        </div>
        <div class="grid-3" style="margin-top: 8px;">
            <button onclick="sendAction('macro', {app: 'yt_skip'})">⏩ Skip Ad</button>
            <button onclick="sendAction('macro', {app: 'fullscreen'})">全 Fullscr</button>
            <button onclick="sendAction('macro', {app: 'close_tab'})">❌ Close Tab</button>
        </div>
    </div>

    <!-- Media Controls -->
    <div class="section">
        <div class="section-title">System Media Control Panel</div>
        <div class="grid-3">
            <button onclick="sendAction('media', {action: 'prev'})">⏮️ Prev</button>
            <button onclick="sendAction('media', {action: 'playpause'})">⏯️ Play/Pause</button>
            <button onclick="sendAction('media', {action: 'next'})">⏭️ Next</button>
        </div>
        <div class="grid-2" style="margin-top: 8px;">
            <button onclick="sendAction('media', {action: 'voldown'})">🔉 Vol -</button>
            <button onclick="sendAction('media', {action: 'volup'})">🔊 Vol +</button>
        </div>
    </div>
    <!-- Text Inputs -->
    <div class="section">
        <div class="section-title">Text Input & Hotkey Matrix</div>
        <div style="display: flex; gap: 8px; margin-bottom: 8px;">
            <input type="text" id="keyboardInput" placeholder="Type letters/numbers here...">
            <button id="btn-send-text">Send</button>
        </div>
        <div class="grid-3">
            <button onclick="sendAction('key', {key: 'enter'})">Enter ↵</button>
            <button onclick="sendAction('key', {key: 'backspace'})">⌫ Back</button>
            <button onclick="sendAction('key', {key: 'space'})">Space</button>
        </div>
        <div class="grid-3" style="margin-top: 8px;">
            <button onclick="sendAction('hotkey', {keys: ['ctrl', 'c']})">Copy</button>
            <button onclick="sendAction('hotkey', {keys: ['ctrl', 'v']})">Paste</button>
            <button onclick="sendAction('hotkey', {keys: ['alt', 'f4']})">Alt+F4</button>
        </div>
    </div>

    <div class="section">
        <div class="section-title">C:\\ Remote File Workspace</div>
        <div id="file-list">Accessing local partitions...</div>
    </div>

    <script>
        const authKey = "{{ auth_key }}";
        let currentMonitor = 0;
        let lastX = 0, lastY = 0;

        function sendAction(endpoint, data = {}) {
            return fetch('/api/' + endpoint + '?key=' + authKey, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        function switchMonitor(index) {
            currentMonitor = index;
            document.querySelectorAll('.tab-btn').forEach((btn, i) => {
                btn.classList.toggle('active', i === index);
            });
            document.getElementById('stream-view').src = "/api/stream?monitor=" + index + "&key=" + authKey;
        }

        // Upgraded HD Zoom Core: Uses smooth CSS scaling to preserve text clarity
        function adjustZoom(val) {
            const view = document.getElementById('stream-view');
            view.style.transform = "scale(" + val + ")";
            
            // Adjusts the visual center pivot so zooming doesn't clip screen boundaries
            if(val > 1) {
                view.style.transformOrigin = "center center";
            } else {
                view.style.transformOrigin = "top left";
            }
        }

        const streamImg = document.getElementById('stream-view');
        streamImg.addEventListener('click', (e) => {
            const rect = streamImg.getBoundingClientRect();
            const clickX = (e.clientX - rect.left) / rect.width;
            const clickY = (e.clientY - rect.top) / rect.height;
            sendAction('directclick', { x: clickX, y: clickY, monitor: currentMonitor });
        });

        const trackpad = document.getElementById('trackpad');
        trackpad.addEventListener('touchstart', (e) => {
            if(e.touches.length === 1) {
                lastX = e.touches[0].clientX;
                lastY = e.touches[0].clientY;
            }
        }, {passive: true});

        trackpad.addEventListener('touchmove', (e) => {
            if(e.touches.length === 1) {
                const currentX = e.touches[0].clientX;
                const currentY = e.touches[0].clientY;
                const deltaX = (currentX - lastX) * 4.5;
                const deltaY = (currentY - lastY) * 4.5;

                if (Math.abs(deltaX) > 0.1 || Math.abs(deltaY) > 0.1) {
                    sendAction('mousemove', { dx: deltaX, dy: deltaY });
                }
                lastX = currentX; lastY = currentY;
            }
        }, {passive: false});

        document.getElementById('btn-left-click').addEventListener('click', () => sendAction('click', {btn: 'left'}));
        document.getElementById('btn-right-click').addEventListener('click', () => sendAction('click', {btn: 'right'}));

        document.getElementById('btn-send-text').addEventListener('click', () => {
            const input = document.getElementById('keyboardInput');
            if(input.value) {
                sendAction('type', { text: input.value });
                input.value = '';
            }
        });

        async function loadFiles() {
            try {
                const res = await fetch('/api/files?key=' + authKey);
                const data = await res.json();
                const container = document.getElementById('file-list');
                container.innerHTML = '';
                data.files.forEach(f => {
                    container.innerHTML += `<div class="file-item"><span>${f.name}</span><button onclick="alert('File workspace initialized')">Open</button></div>`;
                });
            } catch(e) {}
        }
        loadFiles();
    </script>
</body>
</html>
'''
def verify_security():
    return request.args.get('key') == SECURITY_TOKEN

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
        monitor_idx = int(request.json.get('monitor', 0))
        if monitor_idx >= len(monitors): monitor_idx = 0
        m = monitors[monitor_idx]
        target_x = m.x + int(request.json['x'] * m.width)
        target_y = m.y + int(request.json['y'] * m.height)
        pyautogui.click(target_x, target_y)
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

@app.route('/api/hotkey', methods=['POST'])
def hotkey_trigger():
    if not verify_security(): return "Unauthorized", 403
    pyautogui.hotkey(*request.json.get('keys', []))
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
    app_target = request.json.get('app')
    if app_target == 'chrome': os.system("start chrome")
    elif app_target == 'youtube': os.system("start chrome youtube.com")
    elif app_target == 'netflix': os.system("start chrome netflix.com")
    elif app_target == 'yt_skip':
        pyautogui.press('tab'); pyautogui.press('enter')
    elif app_target == 'fullscreen': pyautogui.press('f')
    elif app_target == 'close_tab': pyautogui.hotkey('ctrl', 'w')
    return jsonify(status="success")

@app.route('/api/files')
def list_files():
    if not verify_security(): return "Unauthorized", 403
    target_dir = "C:\\"
    try:
        items = [{"name": i, "is_dir": os.path.isdir(os.path.join(target_dir, i))} for i in os.listdir(target_dir)[:6]]
        return jsonify(files=items)
    except:
        return jsonify(files=[{"name": "System Root Secured", "is_dir": False}])

def generate_monitor_frame(monitor_id):
    import PIL.ImageGrab as ImageGrab
    import mss
    with mss.mss() as sct:
        while True:
            try:
                monitors = sct.monitors
                target = monitors[monitor_id + 1] if (monitor_id + 1) < len(monitors) else monitors
                sct_img = sct.grab(target)
                img = io.BytesIO(mss.tools.to_png(sct_img.rgb, sct_img.size))
                
                from PIL import Image
                pil_img = Image.open(img)
                
                # Dynamic HD Scaling Engine: Delivers maximum raw quality pixels
                # Width is boosted to 1280px HD with a 90% JPEG density quality matrix
                pil_img = pil_img.resize((1280, 720))
                frame_buffer = io.BytesIO()
                pil_img.save(frame_buffer, format='JPEG', quality=90)
                
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_buffer.getvalue() + b'\r\n')
            except:
                pass
            time.sleep(0.06)


@app.route('/api/stream')
def video_feed_stream():
    if not verify_security(): return "Unauthorized", 403
    monitor_id = int(request.args.get('monitor', 0))
    return Response(generate_monitor_frame(monitor_id), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CUSTOM_PORT, debug=False, threaded=True)