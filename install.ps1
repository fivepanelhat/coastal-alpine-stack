# coastal-alpine-stack - dual-platform monorepo installer (Windows / PowerShell)
#
# One-line:
# irm https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.ps1 | iex
#
# From a clone:
# powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# Sets up Core (editable) + monorepo dev deps on Windows. Edge production remains
# RPi 5 / Linux; Windows is a first-class development host.

$ErrorActionPreference = "Stop"

$RepoUrl = if ($env:STACK_REPO_URL) { $env:STACK_REPO_URL } else { "https://github.com/fivepanelhat/coastal-alpine-stack.git" }
$InstallDir = if ($env:STACK_HOME) { $env:STACK_HOME } else { Join-Path $env:USERPROFILE ".coastal-alpine-stack-app" }
$CorePin = if ($env:STACK_CORE_REF) { $env:STACK_CORE_REF } else { "v0.5.9" }

function Info($m) { Write-Host "[stack] $m" -ForegroundColor Cyan }
function Warn($m) { Write-Host "[stack] $m" -ForegroundColor Yellow }
function Fail($m) { Write-Host "[stack] $m" -ForegroundColor Red; exit 1 }
function Require-Ok([string]$Step) {
 if ($null -ne $LASTEXITCODE -and $LASTEXITCODE -ne 0) {
 Fail "$Step failed (exit code $LASTEXITCODE)"
 }
}

$PythonBin = $null
foreach ($cand in @("python", "python3", "py")) {
 if (Get-Command $cand -ErrorAction SilentlyContinue) { $PythonBin = $cand; break }
}
if (-not $PythonBin) {
 Fail "Python 3.10+ (prefer 3.11+) is required. Install from https://www.python.org (Add to PATH)."
}
$PyVer = & $PythonBin -c "import sys; print('%d.%d' % sys.version_info[:2])"
& $PythonBin -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) { Fail "Python 3.10+ is required (found $PyVer)" }
Info "Using Python $PyVer ($PythonBin)"

if ((Test-Path "pyproject.toml") -and ((Test-Path "coastal_alpine_core") -or (Test-Path "docker-compose.yml"))) {
 $SrcDir = (Get-Location).Path
 Info "Installing from current checkout: $SrcDir"
} else {
 if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
 Fail "git is required. Install Git for Windows from https://git-scm.com"
 }
 New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
 $SrcDir = Join-Path $InstallDir "src"
 if (Test-Path (Join-Path $SrcDir ".git")) {
 Info "Updating existing checkout in $SrcDir"
 git -C $SrcDir pull --ff-only 2>$null
 git -C $SrcDir submodule update --init --recursive 2>$null
 } else {
 Info "Cloning $RepoUrl (with submodules)"
 git clone --depth 1 --recurse-submodules $RepoUrl $SrcDir 2>$null
 if (-not (Test-Path $SrcDir)) {
 git clone --depth 1 $RepoUrl $SrcDir
 Require-Ok "git clone"
 }
 }
}

Set-Location $SrcDir
$VenvDir = Join-Path $SrcDir ".venv"

Info "Creating virtualenv at $VenvDir"
& $PythonBin -m venv $VenvDir
Require-Ok "venv create"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPython)) { Fail "venv python not found at $VenvPython" }
& $VenvPython -m pip install --upgrade pip
Require-Ok "pip upgrade"

if (Test-Path "coastal_alpine_core") {
 Info "Installing Coastal-Alpine-Core (editable hybrid SDK)"
 & $VenvPython -m pip install -e "./coastal_alpine_core[dev]"
 if ($LASTEXITCODE -ne 0) {
 Warn "core[dev] failed; retrying without extras"
 & $VenvPython -m pip install -e "./coastal_alpine_core"
 Require-Ok "pip install core"
 }
} else {
 Warn "Local coastal_alpine_core not found; installing from GitHub @$CorePin"
 & $VenvPython -m pip install "git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git@$CorePin"
 Require-Ok "pip install core from GitHub"
}

if (Test-Path "requirements-dev.txt") {
 Info "Installing requirements-dev.txt"
 & $VenvPython -m pip install -r requirements-dev.txt
 if ($LASTEXITCODE -ne 0) { Warn "Some dev deps failed; continuing." }
} elseif (Test-Path "requirements.txt") {
 Info "Installing requirements.txt"
 & $VenvPython -m pip install -r requirements.txt
 if ($LASTEXITCODE -ne 0) { Warn "Some deps failed; continuing." }
}

Info "Verifying Core import"
& $VenvPython -c "import coastal_alpine_core; print('ok')"
Require-Ok "import coastal_alpine_core"

if (Get-Command docker -ErrorAction SilentlyContinue) {
 Info "Docker detected. Optional: docker compose up -d"
} else {
 Warn "Docker not found (optional - install Docker Desktop for local compose)."
}

Write-Host ""
Info "Done. Activate with:"
Write-Host " $VenvDir\Scripts\Activate.ps1"
Write-Host ""
Info "Hybrid components:"
Write-Host " Core: coastal_alpine_core / https://github.com/fivepanelhat/Coastal-Alpine-Core/releases/tag/$CorePin"
Write-Host " Weaver: weaver/ or https://github.com/fivepanelhat/Weaver"
Write-Host " Aether: irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 | iex"
Write-Host ""
Info "Docs: ARCHITECTURE.md | PRODUCTION_HARDENING.md | DATA_FLYWHEEL_GUIDE.md"
