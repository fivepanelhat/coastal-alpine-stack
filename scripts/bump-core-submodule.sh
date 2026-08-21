#!/usr/bin/env bash
# Bump stack gitlinks for Core + Weaver after Sprint A–C.
# Git submodule pointers cannot be updated via GitHub file API — run locally.
#
# Usage (from coastal-alpine-stack clone):
#   ./scripts/bump-core-submodule.sh
#   git add coastal_alpine_core weaver
#   git commit -m "chore(submodules): Core v0.5.9 + Weaver main"
#   git push
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CORE_REF="${STACK_CORE_REF:-v0.5.9}"
WEAVER_REF="${STACK_WEAVER_REF:-main}"

echo "[stack] Updating coastal_alpine_core → $CORE_REF"
git submodule update --init coastal_alpine_core
git -C coastal_alpine_core fetch --tags origin
git -C coastal_alpine_core checkout "$CORE_REF"

echo "[stack] Updating weaver → $WEAVER_REF"
git submodule update --init weaver
git -C weaver fetch origin
git -C weaver checkout "$WEAVER_REF"
git -C weaver pull --ff-only origin "$WEAVER_REF" || true

echo
echo "[stack] Staged pointers (review then commit):"
git status --short coastal_alpine_core weaver || true
echo
echo "Core release: https://github.com/fivepanelhat/Coastal-Alpine-Core/releases/tag/$CORE_REF"
