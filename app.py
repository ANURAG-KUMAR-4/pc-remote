import os
import sys
from flask import Flask, render_template_string, request, jsonify
import pyautogui

# Disable PyAutoGUI fail-safe to prevent accidental server shutdowns on edge movement
pyautogui.FAILSAFE = False

app = Flask(__name__)

# Complete responsive CSS Grid dashboard interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Custom PC Remote Dashboard</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-color: #1e293b;
            --accent-color: #3b82f6;
            --text-color: #f8fafc;
            --danger-color: #ef4444;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            user-select: none;
            -webkit-user-select: none;
        }
        h2 { margin-bottom: 16px; font-weight: 600; font-size: 22px; letter-spacing: -0.025em; }
        .section {
            width: 100%;
            max-width: 400px;
            background: var(--card-color);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            box-sizing: border-box;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
        }
        .section-title {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            margin-bottom: 12px;
            font-weight: 700;
        }
        #trackpad {
            height: 220px;
            background: #020617;
            border: 2px dashed #334155;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #64748b;
            font-size: 14px;
            touch-action: none;
        }
        .mouse-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 12px;
        }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        button {
            background: #334155;
            color: var(--text-color);
            border: none;
            padding: 14px;
            font-size: 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.1s ease;
        }
        button:active { background: var(--accent-color); }
        button.danger:active { background: var(--danger-color); }
        .kbd-container { display: flex; gap: 8px; }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #475569;
            background: #020617;
            color: white;
            font-size: 16px;
        }
    </style>
</head>
<body>

    <h2>💻 Custom System Remote</h2>

    <!-- Vector Capture Workspace -->
    <div class="section">
        <div class="section-title">Trackpad Area</div>
        <div id="trackpad">Swipe to control cursor</div>
        <div class="mouse-buttons">
            <button onclick="sendCommand('click', {btn: 'left'})">Left Click</button>
            <button onclick="sendCommand('click', {btn: 'right'})">Right Click</button>
        </div>
    </div>

    <!-- Media Controls Mapping Grid -->
    <div class="section">
        <div class="section-title">System Media Array</div>
        <div class="grid-3">
            <button onclick="sendCommand('media', {action: 'prev'})">⏮️</button>
            <button onclick="sendCommand('media', {action: 'playpause'})">⏯️</button>
            <button onclick="sendCommand('media', {action: 'next'})">⏭️</button>
        </div>
        <div class="grid-2" style="margin-top: 10px;">
            <button onclick="sendCommand('media', {action: 'voldown'})">Vol -</button>
            <button onclick="sendCommand('media', {action: 'volup'})">Vol +</button>
        </div>
    </div>

    <!-- Live Entry Buffer -->
    <div class="section">
        <div class="section-title">Keyboard String Entry</div>
        <div class="kbd-container">
            <input type="text" id="keyboardInput" placeholder="Enter string text...">
            <button onclick="sendText()">Send</button>
        </div>
        <div class="grid-2" style="margin-top: 10px;">
            <button onclick="sendCommand('key', {key: 'enter'})">Enter ↵</button>
            <button onclick="sendCommand('key', {key: 'backspace'})">⌫ Back</button>
        </div>
    </div>

    <!-- OS Execution Targets -->
    <div class="section">
        <div class="section-title">Core Power Utilities</div>
        <div class="grid-3">
            <button class="danger" onclick="confirmPower('sleep')">Sleep</button>
            <button class="danger" onclick="confirmPower('restart')">Restart</button>
            <button class="danger" onclick="confirmPower('shutdown')">Off</button>
        </div>
    </div>

    <script>
        let lastX = 0, lastY = 0;
        const trackpad = document.getElementById('trackpad');

        trackpad.addEventListener('touchstart', (e) => {
            lastX = e.touches[0].clientX;
            lastY = e.touches[0].clientY;
        });

        trackpad.addEventListener('touchmove', (e) => {
            e.preventDefault();
            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;
            
            const deltaX = currentX - lastX;
            const deltaY = currentY - lastY;
            const sensitivity = 1.8; // Calibrated speed index multiplier

            if (Math.abs(deltaX) > 0.1 || Math.abs(deltaY) > 0.1) {
                sendCommand('mousemove', { dx: deltaX * sensitivity, dy: deltaY * sensitivity });
            }
            lastX = currentX; lastY = currentY;
        });

        function sendCommand(endpoint, data = {}) {
            fetch('/api/' + endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        function sendText() {
            const input = document.getElementById('keyboardInput');
            if(input.value) {
                sendCommand('type', { text: input.value });
                input.value = '';
            }
        }

        // Prevention layer for dangerous OS actions
        function confirmPower(action) {
            if(confirm("Trigger systemic " + action + "?")) {
                sendCommand('power', { action: action });
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/mousemove', methods=['POST'])
def mouse_move():
    data = request.json
    pyautogui.moveRel(data['dx'], data['dy'])
    return jsonify(status="success")

@app.route('/api/click', methods=['POST'])
def mouse_click():
    btn = request.json.get('btn', 'left')
    pyautogui.click(button=btn)
    return jsonify(status="success")

@app.route('/api/media', methods=['POST'])
def media_control():
    action = request.json.get('action')
    mapping = {'playpause': 'playpause', 'next': 'nexttrack', 'prev': 'prevtrack', 'volup': 'volumeup', 'voldown': 'volumedown'}
    if action in mapping: 
        pyautogui.press(mapping[action])
    return jsonify(status="success")

@app.route('/api/key', methods=['POST'])
def key_press():
    pyautogui.press(request.json.get('key'))
    return jsonify(status="success")

@app.route('/api/type', methods=['POST'])
def text_type():
    pyautogui.write(request.json.get('text', ''), interval=0.01)
    return jsonify(status="success")

@app.route('/api/power', methods=['POST'])
def power_control():
    action = request.json.get('action')
    if sys.platform.startswith('win'):
        if action == 'sleep': os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif action == 'restart': os.system("shutdown /r /t 1")
        elif action == 'shutdown': os.system("shutdown /s /t 1")
    return jsonify(status="success")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
