#!/usr/bin/env bash
# coastal-alpine-stack — dual-platform monorepo installer (Linux / macOS)
#
# One-line:
#   curl -fsSL https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.sh | bash
#
# From a clone:
#   ./install.sh
#
# Sets up Core (editable) + monorepo dev deps for hybrid Windows/Linux development
# and RPi edge deployment. Optional: Docker compose for local services.
set -euo pipefail

REPO_URL="${STACK_REPO_URL:-https://github.com/fivepanelhat/coastal-alpine-stack.git}"
INSTALL_DIR="${STACK_HOME:-$HOME/.coastal-alpine-stack-app}"

info() { printf '\033[36m[stack]\033[0m %s\n' "$1"; }
warn() { printf '\033[33m[stack]\033[0m %s\n' "$1"; }
err()  { printf '\033[31m[stack]\033[0m %s\n' "$1" >&2; }

PYTHON_BIN="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON_BIN" ]]; then
  err "Python 3.10+ (prefer 3.11+) is required. On Debian/Ubuntu/RPi OS:"
  err "  sudo apt-get install -y python3 python3-venv python3-pip git build-essential"
  exit 1
fi
PY_VER="$("$PYTHON_BIN" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"

# Python version gate
PY_MAJOR="$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[0])')"
PY_MINOR="$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[1])')"
if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
  err "Python 3.10+ is required (found ${PY_MAJOR}.${PY_MINOR})."
  exit 1
fi
info "Using Python $PY_VER ($PYTHON_BIN)"

if [[ -f "pyproject.toml" ]] && { [[ -d "coastal_alpine_core" ]] || [[ -f "docker-compose.yml" ]]; }; then
  SRC_DIR="$(pwd)"
  info "Installing from current checkout: $SRC_DIR"
else
  if ! command -v git >/dev/null 2>&1; then
    err "git is required to fetch the stack monorepo."
    exit 1
  fi
  mkdir -p "$INSTALL_DIR"
  SRC_DIR="$INSTALL_DIR/src"
  if [[ -d "$SRC_DIR/.git" ]]; then
    info "Updating existing checkout in $SRC_DIR"
    git -C "$SRC_DIR" pull --ff-only || warn "Could not fast-forward; using existing checkout."
    git -C "$SRC_DIR" submodule update --init --recursive 2>/dev/null || true
  else
    info "Cloning $REPO_URL (with submodules)"
    git clone --depth 1 --recurse-submodules "$REPO_URL" "$SRC_DIR" \
      || git clone --depth 1 "$REPO_URL" "$SRC_DIR"
  fi
fi

cd "$SRC_DIR"
VENV_DIR="$SRC_DIR/.venv"

info "Creating virtualenv at $VENV_DIR"
"$PYTHON_BIN" -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip >/dev/null

if [[ -d "coastal_alpine_core" ]]; then
  info "Installing Coastal-Alpine-Core (editable hybrid SDK)"
  pip install -e "./coastal_alpine_core[dev]" || pip install -e "./coastal_alpine_core"
else
  warn "Local coastal_alpine_core not found; installing from GitHub"
  pip install "git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git@v0.5.4"
fi

if [[ -f "requirements-dev.txt" ]]; then
  info "Installing requirements-dev.txt"
  pip install -r requirements-dev.txt || warn "Some dev deps failed; continuing."
elif [[ -f "requirements.txt" ]]; then
  info "Installing requirements.txt"
  pip install -r requirements.txt || warn "Some deps failed; continuing."
fi

if command -v docker >/dev/null 2>&1; then
  info "Docker detected. Optional:  docker compose up -d"
else
  warn "Docker not found (optional for local Mosquitto/Ollama compose)."
fi

echo
info "Done. Activate with:"
echo "    source $VENV_DIR/bin/activate"
echo
info "Hybrid components:"
echo "    Core:    coastal_alpine_core / https://github.com/fivepanelhat/Coastal-Alpine-Core"
echo "    Weaver:  weaver/ or https://github.com/fivepanelhat/Weaver"
echo "    Aether:  curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh | bash"
echo
info "Docs: ARCHITECTURE.md · PRODUCTION_HARDENING.md · DATA_FLYWHEEL_GUIDE.md"
