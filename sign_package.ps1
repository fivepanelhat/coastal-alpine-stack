# Coastal Alpine Tech Limited - Automated Package Signer
param (
    [string]$TargetPackagePath # The zip or tar.gz update payload
)

if (-not $TargetPackagePath) {
    Write-Host "Error: You must provide a path to the target update file." -ForegroundColor Red
    Exit
}

$packageName = Split-Path $TargetPackagePath -Leaf
Write-Host "Signing deployment payload: $packageName..." -ForegroundColor Cyan

# Use absolute path to Git's openssl.exe if global openssl isn't registered
$opensslPath = "C:\Program Files\Git\usr\bin\openssl.exe"
if (-not (Test-Path $opensslPath)) {
    $opensslPath = "openssl" # Fallback to path
}

# Generate a SHA-256 cryptographic hash signed by your master private key
& $opensslPath dgst -sha256 -sign "Sovereign-Keys\ota_private.pem" -out "Staged-Updates\$packageName.sig" $TargetPackagePath

# Package the signed bundle alongside the public key signature manifest
Compress-Archive -Path $TargetPackagePath, "Staged-Updates\$packageName.sig" -DestinationPath "Staged-Updates\$packageName-OTA-SIGNED.zip" -Force

Write-Host "[SUCCESS] Sealed cryptographically signed package at: Staged-Updates\$packageName-OTA-SIGNED.zip" -ForegroundColor Green
