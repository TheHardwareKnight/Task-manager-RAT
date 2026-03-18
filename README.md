# Remote Access Tool – Process Monitoring & Management

## Overview
This project provides a system for monitoring and managing processes across multiple devices using a central server. A Raspberry Pi (Pi 4 or Pi 5) acts as the management server, while devices send data and receive commands.

## Features
- Real-time process monitoring
- Remote task termination
- Multi-device support
- LAN-based or self-hosted deployment
- Config-driven setup

---

## Architecture
Device → Pi Server → Dashboard

- Devices send process data to the Pi
- Pi stores and serves device data
- Dashboard displays devices and sends commands

---

## Supported Hardware

### Raspberry Pi 4
- Recommended OS: Raspberry Pi OS (64-bit)
- RAM: 2GB+ recommended
- Works well for small to medium setups

### Raspberry Pi 5
- Faster CPU and networking
- Better for multiple devices and real-time updates
- Recommended for long-term use

---

## Pi Server Setup

### 1. Install dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install flask
