# Coastal Alpine Tech Limited — Cross-Platform Install Script (Windows PowerShell)
# Sets up the monorepo virtual environment and installs all dependencies.

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "=== Coastal Alpine Stack — Windows Installer ===" -ForegroundColor Cyan
Write-Host ""

# 1. Create virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "[1/4] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "[1/4] Virtual environment (.venv) already exists." -ForegroundColor Gray
}

# 2. Activate
Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# 3. Install shared core in editable mode
Write-Host "[3/4] Installing coastal_alpine_core (editable)..." -ForegroundColor Yellow
pip install -e ./coastal_alpine_core

# 4. Install dev dependencies
Write-Host "[4/4] Installing development dependencies..." -ForegroundColor Yellow
pip install -r requirements-dev.txt

Write-Host ""
Write-Host "=== Installation complete ===" -ForegroundColor Green
Write-Host "To activate the environment later, run:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "To set up individual portals, cd into the portal directory and run:" -ForegroundColor Cyan
Write-Host "  pip install -r requirements.txt"
