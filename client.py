import requests
import time
import psutil

def load_config():
    config = {}
    with open("Config.txt") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=")
                config[key] = value
    return config

config = load_config()

SERVER = f"http://{config['SERVER_IP']}:{config['SERVER_PORT']}/device"
DEVICE_ID = config["DEVICE_ID"]
INTERVAL = int(config["POLL_INTERVAL"])

while True:
    processes = [p.name() for p in psutil.process_iter()]

    data = {
        "device_id": DEVICE_ID,
        "process_count": len(processes),
        "processes": processes
    }

    try:
        res = requests.post(SERVER, json=data)
        cmd = res.json().get("command")

        if cmd and cmd["command"] == "end_task":
            target = cmd["target"]

            for p in psutil.process_iter():
                if p.name() == target:
                    p.terminate()

    except Exception as e:
        print("Error:", e)

    time.sleep(INTERVAL)
