# Remote Access Tool (RAT) – Process Monitoring & Management

## Overview
This project is a Remote Access Tool (RAT) focused on process monitoring and management. It enables a client to retrieve real-time information about active programs on a host device, terminate processes, and collect usage statistics.

## Features
- **Real-Time Process Monitoring** – View all currently running programs on the host system
- **Task Management** – Terminate active processes remotely
- **Usage Analytics** – Track most-used applications and runtime
- **Data Reporting** – Collect and display statistics on program usage
- **Flexible Deployment** – Run on LAN or over the internet (self-hosted)
- **Configurable** – Device and server settings stored in professional config files

## Use Cases
- System supervision across multiple devices
- Monitoring application usage
- Remote task management for authorized administrative purposes

## How It Works
1. The host device runs the RAT service, which collects process data.
2. The client connects to the host.
3. The client can:
   - Request a list of active programs
   - End specific tasks
   - Retrieve usage statistics

## Project Structure
my-rat-project/
├── backend/
├── device/
├── frontend/
├── config/
├── README.md
└── LICENSE

## Installation
```bash
# Clone the repository
git clone https://github.com/TheHardwareKnight/Task-manager-RAT

# Navigate into the project directory
cd Task-manager-RAT
