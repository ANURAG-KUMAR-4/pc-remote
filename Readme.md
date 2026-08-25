# PC Remote Pro: Advanced Multi-Monitor Control System

A high-performance, low-latency remote administration tool built with Python and the Windows Native API. This system transforms any mobile device into a professional peripheral suite, capable of controlling a PC even during secure session transitions (Windows Lock Screen).

## 🚀 Key Engineering Features

- **Kernel-Level Input Injection:** Bypasses standard software limitations by using `win32api` to inject mouse and keyboard events directly into the hardware input buffer.
- **Session-Aware Desktop Switching:** Implements a specialized hook using `win32service.OpenInputDesktop` to maintain control when the PC switches to the "Winlogon" (password) desktop.
- **Native MJPEG Streaming:** Optimized multi-threaded display engine providing smooth, high-frame-rate visual feedback from multiple monitors simultaneously.
- **Immersive Viewport UX:** A borderless fullscreen mode with a transparent floating action menu (Hot Ball) for seamless navigation.
- **Complete Peripheral Matrix:**
  - **Precision Trackpad:** Responsive cursor tracking with variable sensitivity.
  - **Media Deck:** Full control over System Volume and Playback (Prev, Play/Pause, Next).
  - **Hardware Modifiers:** Dedicated toggles for `Ctrl`, `Alt`, `Fn`, and `Caps Lock`.
  - **Storage Workspace:** Direct remote browsing of the local file system.

## 🛠️ Technology Stack

- **Backend:** Python 3.13 / Flask (Asynchronous)
- **OS Integration:** Microsoft Win32 API (`pywin32`)
- **Graphics:** `mss` (Kernel-level screen capture) & `Pillow` (Image Matrix Processing)
- **Frontend:** HTML5 Canvas / CSS3 Grid / Vanilla JavaScript (ES6)

## 📦 Installation & Setup

1. **Clone the project:**
   ```bash
   git clone https://github.com
   cd pc-remote
   ```

2. **Initialize Environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install flask pyautogui pillow mss pywin32
   ```

3. **Deploy with Privileges:**
   To enable Lock-Screen control and hardware injection, launch the server as **Administrator**:
   ```powershell
   python app.py
   ```

## 🌐 Network Configuration & Masking

This project utilizes **mDNS (Multicast DNS)** to obfuscate the host's raw IP address. Instead of numbers, connect using your machine's hostname:

```text
URL: http://[YOUR-HOSTNAME].local:38491
```

## 🔒 Security Policy Requirements

To allow the application to interact with the Windows Secure Desktop (Login Screen), the following Local Group Policy must be configured:
1. Run `gpedit.msc`.
2. Navigate to: `Computer Configuration -> Administrative Templates -> Windows Components -> Windows Logon Options`.
3. Set **"Disable or enable software Secure Attention Sequence"** to **Enabled**.
4. Select **"Services and Ease of Access applications"** in the options pane.

---
**Developed by [Anurag Kumar]**