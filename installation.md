# Installation Guide

Follow the instructions below to install the Coastal Alpine Stack on your operating system.

## Linux Installation

### Option 1: Automated Setup (Recommended)
Run the bootstrap script, which creates the virtual environment, configures environment files, upgrades pip, and installs all dependencies:
```bash
python3 bootstrap.py
```

### Option 2: Manual Setup
If you prefer to perform the setup steps manually:
1. Clone the repository with its submodules:
   ```bash
   git clone --recursive https://github.com/fivepanelhat/coastal-alpine-stack.git
   cd coastal-alpine-stack
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Upgrade pip and install development dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements-dev.txt
   ```
4. Install the core package in editable mode:
   ```bash
   pip install -e coastal_alpine_core
   ```

---

## Windows Installation

### Option 1: Automated Setup (Recommended)
Run the bootstrap script in PowerShell or Command Prompt:
```powershell
python bootstrap.py
```

### Option 2: Manual Setup
If you prefer to perform the setup steps manually:
1. Clone the repository with its submodules:
   ```powershell
   git clone --recursive https://github.com/fivepanelhat/coastal-alpine-stack.git
   cd coastal-alpine-stack
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Upgrade pip and install development dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt
   ```
4. Install the core package in editable mode:
   ```powershell
   pip install -e coastal_alpine_core
   ```
