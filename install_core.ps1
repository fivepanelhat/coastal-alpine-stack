# Coastal Alpine Tech Limited - Core Infrastructure Installation Linker
# This PowerShell script links the local 'coastal_alpine_core' shared package into all portals.

Write-Host "Linking coastal_alpine_core dependency locally across portals..." -ForegroundColor Cyan

$portals = @("Blue-Moon-Portal", "AquaGuard-Portal", "SoilGuard-Portal", "Sting-Operation-AI", "Weaver")

foreach ($portal in $portals) {
    if (Test-Path $portal) {
        Write-Host "Installing core in $portal..." -ForegroundColor Yellow
        Push-Location $portal

        # Create venv if not present
        if (-not (Test-Path "venv")) {
            Write-Host "  Creating virtual environment..." -ForegroundColor Gray
            python -m venv venv
        }

        # Activate venv and install core
        & .\venv\Scripts\Activate.ps1
        pip install -e ../coastal_alpine_core
        deactivate

        Pop-Location
        Write-Host "  Done: $portal" -ForegroundColor Green
    } else {
        Write-Warning "Directory $portal not found. Skipping."
    }
}

Write-Host "Local core package link installation complete." -ForegroundColor Green
