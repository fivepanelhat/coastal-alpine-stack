# Coastal Alpine Tech Limited - Local CI/CD Test Runner
# This script runs the security audit scans and full unit/stress test suites across all portals and packages.

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Starting Coastal Alpine Stack Unified Local CI  " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$venvPython = ".venv/Scripts/python.exe"
$venvPytest = ".venv/Scripts/pytest.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "Virtual environment not found! Please ensure '.venv' exists with dependencies installed."
    exit 1
}

$allPassed = $true

# 1. Run SecOps Security Audit (Prompt Guard)
Write-Host "Running SecOps Security Audit Scan..." -ForegroundColor Yellow
& $venvPython -m coastal_alpine_core.prompt_guard
if ($LASTEXITCODE -eq 0) {
    Write-Host "[PASS] SecOps Security Scan Passed!" -ForegroundColor Green
} else {
    Write-Host "[FAIL] SecOps Security Scan Failed!" -ForegroundColor Red
    $allPassed = $false
}

# 2. Run Pytest Test Suite (70+ unit & stress tests across all repos)
Write-Host "Running Unified Test Suite..." -ForegroundColor Yellow
& $venvPytest
if ($LASTEXITCODE -eq 0) {
    Write-Host "[PASS] All Pytest Suites Passed!" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Test Suite Failures Detected!" -ForegroundColor Red
    $allPassed = $false
}

Write-Host "==================================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "   CI STATUS: SUCCESS (All scans and tests passed)   " -ForegroundColor Green
} else {
    Write-Host "   CI STATUS: FAILURE (Some scans or tests failed)   " -ForegroundColor Red
    exit 1
}
Write-Host "==================================================" -ForegroundColor Cyan
