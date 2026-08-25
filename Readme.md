# Custom High-Performance PC Remote Control System

A high-speed, localized remote control platform built with Python (Flask) and low-level Windows API integration. This project allows a mobile device to function as a full-system peripheral, controlling mouse movements, keyboard inputs, and live dual-monitor streaming.

## 🚀 Key Features

- **Low-Latency Screen Mirroring:** High-resolution JPEG streaming from multiple monitors.
- **Precision Virtual Trackpad:** Native Windows `mouse_event` integration for fluid cursor tracking.
- **Hardware-Level Input:** Uses Windows Scancodes to bypass software restrictions, allowing control over administrative windows and login screens.
- **Matrix Keyboard:** Support for character strings and system hotkeys (Ctrl, Alt, Shift, etc.).
- **Dual-Monitor Support:** Dynamic monitor index switching.
- **Security-First Architecture:** Optional URI masking and port remapping to secure local network traffic.

## 🛠️ Tech Stack

- **Backend:** Python 3.x
- **Framework:** Flask (Asynchronous threading enabled)
- **Input Drivers:** Win32 API (`pywin32`)
- **Display Engine:** `mss` (Multi-screen shot) & `Pillow` for real-time image processing

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd pc-remote
   ```

2. **Setup Virtual Environment:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server:**
   ```bash
   python app.py
   ```

## 📱 Mobile Connection

Once the server is running, find your laptop's local IP using `ipconfig` and navigate to:
`http://<YOUR_IP>:38491`

*Note: For the best experience, use "Add to Home Screen" on your mobile browser to run the application in borderless standalone mode.*

## 🔒 Security & Policy Configuration

To enable control over the Windows Secure Desktop (Login Screen), the following local policy was implemented:
- **Policy:** `Disable or enable software Secure Attention Sequence`
- **Configuration:** Set to `Enabled` with `Services and Ease of Access applications`.

---
Developed by [Anurag Kumar]