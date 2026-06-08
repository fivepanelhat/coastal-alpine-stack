# Coastal Alpine Tech Limited - Core Infrastructure Installation Linker
# This PowerShell script links the local 'coastal_alpine_core' shared package into all portals.

Write-Host "Linking coastal_alpine_core dependency locally across portals..." -ForegroundColor Cyan

$portals = @("Blue-Moon-Portal", "AquaGuard-Portal", "SoilGuard-Portal")

foreach ($portal in $portals) {
    if (Test-Path $portal) {
        Write-Host "Installing in $portal..." -ForegroundColor Yellow
        Push-Location $portal
        npm install ../coastal_alpine_core
        Pop-Location
    } else {
        Write-Warning "Directory $portal not found. Skipping."
    }
}

Write-Host "Local core package link installation complete." -ForegroundColor Green
