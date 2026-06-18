# Environment & Prerequisites Setup Guide

This guide details the system prerequisites required before installing the Coastal Alpine Stack on Windows or Linux.

## Linux Setup

### Prerequisites
1. **Python 3.10+**: Make sure Python and its virtual environment modules are installed.
2. **System Dependencies**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-dev python3-venv python3-pip git build-essential
   sudo apt-get install -y portaudio19-dev libasound2-dev libgl1 libglib2.0-0
   ```

---

## Windows Setup

### Prerequisites
1. **Python 3.10+**: Ensure Python is installed from python.org and "Add Python to PATH" is checked during installation.
2. **Git for Windows**: Download and install from [git-scm.com](https://git-scm.com/).
3. **C++ Build Tools** (Optional/Recommended for compiling some binary dependencies): Install the Visual Studio Build Tools with the "Desktop development with C++" workload.
