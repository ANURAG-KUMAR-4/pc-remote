import os
import sys
from flask import Flask, render_template_string, request, jsonify
import pyautogui

# Disable PyAutoGUI fail-safe to prevent remote pointer disconnects
pyautogui.FAILSAFE = False

app = Flask(__name__)

# Basic layout interface delivered to your mobile browser
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Custom PC Remote</title>
    <style>
        body {
            font-family: sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .status-card {
            background: #1e293b;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        h1 { color: #3b82f6; margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="status-card">
        <h1>💻 PC Remote Live</h1>
        <p>Your local network development platform is active.</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Binds to 0.0.0.0 so devices on your home network can connect
    app.run(host='0.0.0.0', port=5000, debug=False)
