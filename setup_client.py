#!/usr/bin/env python3
"""
setup_client.py — Windows Client Setup
Run this once on each Windows device you want to monitor.

Usage:
    python setup_client.py

What it does:
    1. Asks for the Pi server IP, port, a device name, and poll interval
    2. Generates client.py with your config baked in
    3. Uses PyInstaller to compile client.exe
    4. Registers client.exe as a Windows startup task via Task Scheduler
       so it runs automatically on login (hidden, no console window)
"""

import os
import sys
import subprocess
import shutil


# ── helpers ───────────────────────────────────────────────────────────────────

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"  {prompt}{suffix}: ").strip()
    return val if val else default

def section(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

def run(cmd, check=True, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, check=check,
                              capture_output=True, text=True)
    subprocess.run(cmd, shell=True, check=check)


# ── check platform ────────────────────────────────────────────────────────────

if sys.platform != "win32":
    print("[!] This setup script is for Windows only.")
    print("    Run setup_pi.py on your Raspberry Pi instead.")
    sys.exit(1)


# ── gather config ─────────────────────────────────────────────────────────────

section("Windows Client Setup")
print("""
  This script will configure this device as a monitored client
  and register it to start automatically on login.
""")

import socket
hostname = socket.gethostname()

print("  Enter your configuration below.")
print("  Press Enter to accept the [default] value.\n")

SERVER_IP     = ask("Raspberry Pi IP address")
SERVER_PORT   = ask("Server port", "5000")
DEVICE_ID     = ask("Name for this device", hostname)
POLL_INTERVAL = ask("How often to send data (seconds)", "5")
INSTALL_DIR   = ask("Where to install client files",
                    os.path.join(os.environ.get("APPDATA", "C:\\Users\\User"), "TaskManagerClient"))

print()
print("  Configuration summary:")
print(f"    Pi IP         : {SERVER_IP}")
print(f"    Port          : {SERVER_PORT}")
print(f"    Device name   : {DEVICE_ID}")
print(f"    Poll interval : {POLL_INTERVAL}s")
print(f"    Install dir   : {INSTALL_DIR}")
print()
confirm = input("  Looks good? (y/n): ").strip().lower()
if confirm != "y":
    print("  Aborted.")
    sys.exit(0)

os.makedirs(INSTALL_DIR, exist_ok=True)


# ── install Python dependencies ───────────────────────────────────────────────

section("Installing Python Dependencies")
run(f"{sys.executable} -m pip install requests psutil pyinstaller --quiet")


# ── generate client.py ────────────────────────────────────────────────────────

section("Generating client.py")

CLIENT_CODE = f'''import requests
import time
import psutil
import sys

SERVER    = "http://{SERVER_IP}:{SERVER_PORT}/device"
DEVICE_ID = "{DEVICE_ID}"
INTERVAL  = {POLL_INTERVAL}

while True:
    try:
        processes = []
        for p in psutil.process_iter(["name"]):
            try:
                name = p.info["name"]
                if name:
                    processes.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        data = {{
            "device_id":     DEVICE_ID,
            "process_count": len(processes),
            "processes":     processes,
        }}

        res = requests.post(SERVER, json=data, timeout=10)
        cmd = res.json().get("command")

        if cmd and cmd.get("command") == "end_task":
            target = cmd.get("target", "")
            for p in psutil.process_iter(["name"]):
                try:
                    if p.info["name"] == target:
                        p.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    except requests.exceptions.ConnectionError:
        pass  # server offline, retry silently
    except Exception:
        pass  # never crash — keep running

    time.sleep(INTERVAL)
'''

client_py = os.path.join(INSTALL_DIR, "client.py")
with open(client_py, "w") as f:
    f.write(CLIENT_CODE)
print(f"  [+] Written: {client_py}")


# ── compile to .exe ───────────────────────────────────────────────────────────

section("Compiling client.exe with PyInstaller")

dist_dir  = os.path.join(INSTALL_DIR, "dist")
build_dir = os.path.join(INSTALL_DIR, "build")

run(
    f'pyinstaller --onefile --noconsole --distpath "{dist_dir}" '
    f'--workpath "{build_dir}" --specpath "{INSTALL_DIR}" "{client_py}"'
)

exe_path = os.path.join(dist_dir, "client.exe")
if not os.path.exists(exe_path):
    print("  [!] PyInstaller did not produce client.exe — check output above.")
    sys.exit(1)

# copy exe to install root for tidiness
final_exe = os.path.join(INSTALL_DIR, "client.exe")
shutil.copy2(exe_path, final_exe)
print(f"  [+] Compiled: {final_exe}")


# ── register startup via Task Scheduler ──────────────────────────────────────

section("Registering Windows Startup Task")

TASK_NAME = f"TaskManagerClient_{DEVICE_ID.replace(' ', '_')}"

# Remove existing task if present (ignore errors)
run(f'schtasks /delete /tn "{TASK_NAME}" /f', check=False)

# Create task: run at logon for current user, hidden
result = run(
    f'schtasks /create /tn "{TASK_NAME}" '
    f'/tr "{final_exe}" '
    f'/sc ONLOGON '
    f'/rl HIGHEST '
    f'/f',
    check=False,
    capture=True,
)

if result.returncode == 0:
    print(f"  [+] Startup task registered: {TASK_NAME}")
    print("      The client will start automatically on next login.")
else:
    print("  [!] Task Scheduler registration failed.")
    print("      You may need to run this script as Administrator.")
    print(f"      To register manually, run:")
    print(f'      schtasks /create /tn "{TASK_NAME}" /tr "{final_exe}" /sc ONLOGON /rl HIGHEST /f')


# ── start client now ─────────────────────────────────────────────────────────

section("Starting Client")
print("  Starting client.exe in the background...")
subprocess.Popen(
    [final_exe],
    creationflags=subprocess.CREATE_NO_WINDOW,
    close_fds=True,
)
print("  [+] Client started.")


# ── done ─────────────────────────────────────────────────────────────────────

section("Setup Complete")
print(f"""
  Files installed to : {INSTALL_DIR}\\
    client.py          — Source (config baked in)
    client.exe         — Compiled executable

  Startup task       : {TASK_NAME}
    Runs automatically at Windows login (no console window)

  To stop the client:
    Open Task Manager -> find client.exe -> End Task

  To uninstall the startup task:
    schtasks /delete /tn "{TASK_NAME}" /f

  Connecting to:
    http://{SERVER_IP}:{SERVER_PORT}
""")
