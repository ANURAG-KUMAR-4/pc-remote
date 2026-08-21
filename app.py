import os
import sys
import io
import time
from flask import Flask, render_template_string, request, jsonify, Response
import pyautogui

# Performance Tuning: Remove standard internal latency delays
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

app = Flask(__name__)

# Security Access Values
SECRET_URL_PATH = "remote"
SECURITY_TOKEN = "alpha_secure_99"
CUSTOM_PORT = 38491

# Visual Mask: Returns a generic Microsoft IIS screen if someone guesses the IP
IIS_MASK_TEMPLATE = '''
<!DOCTYPE html>
<html><head><title>IIS Windows Server</title><style>
body { font-family: 'Segoe UI', Tahoma, Arial; background-color: #244976; color: #fff; margin: 0; padding: 40px; }
.container { max-width: 600px; margin: 0 auto; }
h1 { font-size: 42px; font-weight: 300; margin: 0 0 10px 0; }
p { font-size: 16px; color: #a9c7ed; line-height: 1.5; }
</style></head><body><div class="container"><h1>Internet Information Services</h1><p>The web server configuration is currently hosting an inactive static distribution block.</p></div></body></html>
'''

# The Dashboard UI Engine with Trackpad, Media, App Macros, and Screen Streaming Canvas
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Production System Console</title>
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
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0; padding: 12px;
            display: flex; flex-direction: column; align-items: center;
            user-select: none; -webkit-user-select: none;
        }
        .section {
            width: 100%; max-width: 420px;
            background: var(--card-color); border-radius: 12px;
            padding: 14px; margin-bottom: 12px; box-sizing: border-box;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4);
        }
        .section-title {
            font-size: 11px; text-transform: uppercase; letter-spacing: 0.07em;
            color: #64748b; margin-bottom: 10px; font-weight: 700;
        }
        #stream-view {
            width: 100%; height: 180px; background: #000;
            border-radius: 8px; border: 1px solid #1e293b; object-fit: contain;
        }
        #trackpad {
            height: 180px; background: #020617; border: 2px dashed #1e293b;
            border-radius: 8px; display: flex; align-items: center;
            justify-content: center; color: #475569; font-size: 13px; touch-action: none;
        }
        .mouse-buttons { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        button {
            background: #1e293b; color: var(--text-color); border: none;
            padding: 12px; font-size: 14px; border-radius: 6px;
            font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center;
        }
        button:active { background: var(--accent-color); }
        button.danger:active { background: var(--danger-color); }
        .kbd-container { display: flex; gap: 6px; }
        input[type="text"] {
            flex: 1; padding: 10px; border-radius: 6px;
            border: 1px solid #334155; background: #020617; color: white; font-size: 14px;
        }
    </style>
</head>
<body>

    <!-- Screen Mirroring Frame Window -->
    <div class="section">
        <div class="section-title">Live PC Monitor View</div>
        <img id="stream-view" src="/api/stream?key={{ auth_key }}" alt="Desktop Monitor Feed">
    </div>

    <!-- Responsive Trackpad Engine -->
    <div class="section">
        <div class="section-title">Ultra-Responsive Trackpad</div>
        <div id="trackpad">Drag surface area to drive cursor</div>
        <div class="mouse-buttons">
            <button onclick="sendAction('click', {btn: 'left'})">Left Click</button>
            <button onclick="sendAction('click', {btn: 'right'})">Right Click</button>
        </div>
    </div>

    <!-- Application Shortcuts & Macros -->
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

    <!-- Media Controls Arrays -->
    <div class="section">
        <div class="section-title">Media Arrays</div>
        <div class="grid-3">
            <button onclick="sendAction('media', {action: 'prev'})">⏮️</button>
            <button onclick="sendAction('media', {action: 'playpause'})">⏯️</button>
            <button onclick="sendAction('media', {action: 'next'})">⏭️</button>
        </div>
        <div class="grid-2" style="margin-top: 8px;">
            <button onclick="sendAction('media', {action: 'voldown'})">Vol -</button>
            <button onclick="sendAction('media', {action: 'volup'})">Vol +</button>
        </div>
    </div>

    <!-- Keyboard Input buffer -->
    <div class="section">
        <div class="section-title">Keyboard String Entry</div>
        <div class="kbd-container">
            <input type="text" id="keyboardInput" placeholder="Type data parameters...">
            <button onclick="sendText()">Send</button>
        </div>
    </div>

    <script>
        let lastX = 0, lastY = 0;
        const authKey = "{{ auth_key }}";
        const trackpad = document.getElementById('trackpad');

        trackpad.addEventListener('touchstart', (e) => {
            lastX = e.touches.clientX;
            lastY = e.touches.clientY;
        });

        trackpad.addEventListener('touchmove', (e) => {
            e.preventDefault();
            const currentX = e.touches.clientX;
            const currentY = e.touches.clientY;
            
            const deltaX = currentX - lastX;
            const deltaY = currentY - lastY;
            
            // Highly accelerated speed value multiplier configuration
            const sensitivity = 4.5; 

            if (Math.abs(deltaX) > 0.05 || Math.abs(deltaY) > 0.05) {
                sendAction('mousemove', { dx: deltaX * sensitivity, dy: deltaY * sensitivity });
            }
            lastX = currentX; lastY = currentY;
        });

        function sendAction(endpoint, data = {}) {
            fetch('/api/' + endpoint + '?key=' + authKey, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        function sendText() {
            const input = document.getElementById('keyboardInput');
            if(input.value) {
                sendAction('type', { text: input.value });
                input.value = '';
            }
        }
    </script>
</body>
</html>
'''

def verify_security():
    client_key = request.args.get('key')
    return client_key == SECURITY_TOKEN

@app.route('/')
def handle_root_mask():
    # Return fake IIS web block to mask existence of the interface
    return render_template_string(IIS_MASK_TEMPLATE)

@app.route(f'/{SECRET_URL_PATH}')
def handle_authenticated_console():
    client_key = request.args.get('key')
    if client_key != SECURITY_TOKEN:
        return render_template_string(IIS_MASK_TEMPLATE), 403
    return render_template_string(DASHBOARD_TEMPLATE, auth_key=SECURITY_TOKEN)

@app.route('/api/mousemove', methods=['POST'])
def mouse_move():
    if not verify_security(): return jsonify(error="Unauthorized"), 403
    data = request.json
    pyautogui.moveRel(int(data['dx']), int(data['dy']))
    return jsonify(status="success")

@app.route('/api/click', methods=['POST'])
def mouse_click():
    if not verify_security(): return jsonify(error="Unauthorized"), 403
    pyautogui.click(button=request.json.get('btn', 'left'))
    return jsonify(status="success")

@app.route('/api/media', methods=['POST'])
def media_control():
    if not verify_security(): return jsonify(error="Unauthorized"), 403
    mapping = {'playpause':'playpause', 'next':'nexttrack', 'prev':'prevtrack', 'volup':'volumeup', 'voldown':'volumedown'}
    action = request.json.get('action')
    if action in mapping: pyautogui.press(mapping[action])
    return jsonify(status="success")

@app.route('/api/type', methods=['POST'])
def text_type():
    if not verify_security(): return jsonify(error="Unauthorized"), 403
    pyautogui.write(request.json.get('text', ''), interval=0.0)
    return jsonify(status="success")

@app.route('/api/macro', methods=['POST'])
def application_macros():
    if not verify_security(): return jsonify(error="Unauthorized"), 403
    app_target = request.json.get('app')
    if app_target == 'chrome':
        os.system("start chrome")
    elif app_target == 'youtube':
        os.system("start chrome youtube.com")
    elif app_target == 'netflix':
        os.system("start chrome netflix.com")
    elif app_target == 'yt_skip':
        pyautogui.press('tab')
        pyautogui.press('enter')
    elif app_target == 'fullscreen':
        pyautogui.press('f')
    elif app_target == 'close_tab':
        pyautogui.hotkey('ctrl', 'w')
    return jsonify(status="success")

def generate_screen_frames():
    import PIL.ImageGrab as ImageGrab
    while True:
        # Snap active layout view, downscale dimension metrics to respect network overhead
        img = ImageGrab.grab()
        img = img.resize((500, 300))
        frame_buffer = io.BytesIO()
        img.save(frame_buffer, format='JPEG', quality=40)
        frame_bytes = frame_buffer.getvalue()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.05)  # Keeps loop pacing optimized

@app.route('/api/stream')
def video_feed_stream():
    if not verify_security():
        return "Unauthorized", 403
    return Response(generate_screen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == 'main':
    # Run server on high, random port
    app.run(host='0.0.0.0', port=CUSTOM_PORT, debug=False, threaded=True)