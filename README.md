# Remote Access Tool (RAT) – Process Monitoring & Management

## Overview
This project is a Remote Access Tool (RAT) focused on process monitoring and management. It enables a client to retrieve real-time information about active programs on a host device, terminate processes, and collect usage metrics such as application frequency, runtime, and overall system activity.

## Features
- **Real-Time Process Monitoring**
  - View all currently running programs on the host system
- **Task Management**
  - Terminate active processes remotely
- **Usage Analytics**
  - Track most-used applications
  - Monitor runtime and activity patterns
- **Data Reporting**
  - Collect and display statistics on program usage

## Use Cases
- System supervision across multiple devices  
- Monitoring application usage  
- Remote task management for administrative purposes  

## How It Works
1. The **host device** runs the RAT service, which collects process data.
2. The **client** connects to the host.
3. The client can:
   - Request a list of active programs
   - End specific tasks
   - Retrieve usage statistics

## Installation
```bash
# Clone the repository
git clone https://github.com/TheHardwareKnight/Task-manager-RAT

# Navigate into the project directory
cd Task-manager-RAT
