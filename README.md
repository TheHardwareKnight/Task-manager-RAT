# 🖥️ Task Manager RAT — Remote Process Monitor

A self-hosted remote process monitoring and management system. A Raspberry Pi acts as the central server and displays a fullscreen dark dashboard showing all connected devices and their running processes in real time. Windows client devices phone home automatically and can have processes terminated remotely from the dashboard.

---

## How It Works

```
Windows Device          Raspberry Pi
─────────────           ─────────────────────────────────
client.exe     ──────►  server.py  (Flask API)
  sends process list              │
  receives commands               ▼
                         dashboard.py  (Fullscreen UI)
                           shows all devices + processes
                           End Task button sends commands back
```

1. Each Windows device runs `client.exe` silently in the background
2. Every few seconds it sends a list of its running processes to the Pi
3. The Pi's Flask server stores the data and serves it to the dashboard
4. The dashboard displays all connected devices in a dark fullscreen window
5. Clicking **End Task** on a process sends a termination command back to that device

---

## Requirements

| Component | Requirements |
|---|---|
| Raspberry Pi | Pi 4 or 5, Raspberry Pi OS 64-bit, Python 3.8+, desktop environment |
| Windows clients | Windows 10/11, Python 3.8+, internet access to Pi on LAN |

---

## Installation

### Step 1 — Set up the Raspberry Pi (server + dashboard)

Clone the repo on your Pi:

```bash
git clone https://github.com/TheHardwareKnight/Network-Devices.git
cd Network-Devices
```

Run the Pi setup script:

```bash
python3 setup_pi.py
```

The script will:
- Ask for your Pi's IP address, port, and poll interval
- Install all dependencies (`flask`, `tkinter`, etc.)
- Generate `server.py` and `dashboard.py` with your config baked in
- Install and enable two systemd services so both start automatically on boot

At the end it will print the IP and port to give to your client devices.

---

### Step 2 — Set up each Windows client device

Clone the repo (or just copy `setup_client.py`) onto each Windows machine:

```
git clone https://github.com/TheHardwareKnight/Network-Devices.git
cd Network-Devices
```

Run the client setup script **as Administrator**:

```
python setup_client.py
```

The script will:
- Ask for the Pi's IP address, port, a name for this device, and poll interval
- Install Python dependencies (`requests`, `psutil`, `pyinstaller`)
- Generate `client.py` with your config baked in
- Compile it into `client.exe` using PyInstaller (no console window)
- Register `client.exe` as a Windows startup task via Task Scheduler (runs at login)
- Start the client immediately in the background

> **Note:** Run as Administrator to allow Task Scheduler registration. If you skip this, the client will still work but won't auto-start on login.

---

## File Overview

| File | Where it runs | What it does |
|---|---|---|
| `setup_pi.py` | Raspberry Pi | One-time setup — generates server + dashboard, installs services |
| `setup_client.py` | Windows | One-time setup — generates + compiles client, registers startup task |
| `server.py` | Pi (generated) | Flask API — receives device data, queues commands |
| `dashboard.py` | Pi (generated) | Fullscreen dark tkinter dashboard |
| `client.py` | Windows (generated) | Sends process list, receives + executes commands |
| `client.exe` | Windows (compiled) | Compiled silent executable, auto-starts at login |

---

## Dashboard

The dashboard runs fullscreen on the Pi's display automatically on boot.

- **Left panel** — device cards showing each connected device, its IP, online status, and process count
- **Right panel** — process list for the selected device with live search
- **End Task button** — terminates the selected process on the remote device
- **ESC** — exit fullscreen
- **F11** — re-enter fullscreen

---

## Auto-Start Behaviour

### Raspberry Pi
Both services are managed by `systemd` and start automatically on boot:

```bash
# Check status
sudo systemctl status taskmanager-server
sudo systemctl status taskmanager-dashboard

# View logs
sudo journalctl -u taskmanager-server -f
sudo journalctl -u taskmanager-dashboard -f

# Restart manually
sudo systemctl restart taskmanager-server
sudo systemctl restart taskmanager-dashboard

# Disable auto-start
sudo systemctl disable taskmanager-server
sudo systemctl disable taskmanager-dashboard
```

### Windows Clients
`client.exe` is registered as a Task Scheduler task that runs at login with no console window.

```powershell
# List the task
schtasks /query /tn "TaskManagerClient_<DeviceName>"

# Run it now manually
schtasks /run /tn "TaskManagerClient_<DeviceName>"

# Remove the startup task
schtasks /delete /tn "TaskManagerClient_<DeviceName>" /f
```

To stop the client immediately: open Task Manager → find `client.exe` → End Task.

---

## Troubleshooting

**Dashboard shows "Server unreachable"**
- Check the Flask server is running: `sudo systemctl status taskmanager-server`
- Confirm the port is correct and not blocked by a firewall

**Client devices not appearing**
- Confirm `client.exe` is running on the device (check Task Manager)
- Make sure the Pi's IP and port match what was entered during client setup
- Check both devices are on the same network

**Task Scheduler registration failed**
- Re-run `setup_client.py` as Administrator (right-click → Run as administrator)

**Dashboard won't open on boot**
- The dashboard service requires a desktop session. Make sure your Pi is set to auto-login to the desktop (Raspberry Pi Configuration → System → Boot → Desktop Autologin)

---

## License

MIT — do whatever you like with it.
