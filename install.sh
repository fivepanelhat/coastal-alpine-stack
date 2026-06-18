#!/usr/bin/env bash
# Coastal Alpine Tech Limited — Cross-Platform Install Script (Linux / macOS)
# Sets up the monorepo virtual environment and installs all dependencies.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Coastal Alpine Stack — Linux/macOS Installer ==="
echo ""

# 1. Create virtual environment
if [ ! -d ".venv" ]; then
    echo "[1/4] Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "[1/4] Virtual environment (.venv) already exists."
fi

# 2. Activate
echo "[2/4] Activating virtual environment..."
source .venv/bin/activate

# 3. Install shared core in editable mode
echo "[3/4] Installing coastal_alpine_core (editable)..."
pip install -e ./coastal_alpine_core

# 4. Install dev dependencies
echo "[4/4] Installing development dependencies..."
pip install -r requirements-dev.txt

echo ""
echo "=== Installation complete ==="
echo "To activate the environment later, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To set up individual portals, cd into the portal directory and run:"
echo "  pip install -r requirements.txt"
