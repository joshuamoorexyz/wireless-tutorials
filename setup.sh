#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  Wireless Tutorials — Manim Setup"
echo "========================================"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.10+ from https://python.org"
    exit 1
fi

PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "[✓] Python $PY_VER"

# ── System deps via Homebrew (macOS) ──────────────────────────────
if [[ "$(uname)" == "Darwin" ]]; then
    echo ""
    echo "--- System dependencies (Homebrew) ---"
    if ! command -v brew &>/dev/null; then
        echo "ERROR: Homebrew is required. Install from https://brew.sh"
        exit 1
    fi
    brew_deps=()
    command -v ffmpeg &>/dev/null || brew_deps+=(ffmpeg)
    command -v pkg-config &>/dev/null || brew_deps+=(pkg-config)
    if ! pkg-config --exists cairo 2>/dev/null; then brew_deps+=(cairo); fi
    if ! pkg-config --exists pango 2>/dev/null; then brew_deps+=(pango); fi
    if [[ ${#brew_deps[@]} -gt 0 ]]; then
        brew install "${brew_deps[@]}"
    fi
    echo "[✓] System deps satisfied"
fi

# ── Python virtual environment ────────────────────────────────────
echo ""
echo "--- Python virtual environment ---"
VENV_DIR="$PROJECT_DIR/.venv"
if [[ -d "$VENV_DIR" ]]; then
    echo "  Reusing existing virtual env"
else
    python3 -m venv "$VENV_DIR"
    echo "[✓] Created virtual env"
fi

source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "$PROJECT_DIR/requirements.txt"
echo "[✓] Python packages installed"

echo ""
echo "========================================"
echo "  Setup complete!"
echo "========================================"
echo ""
echo "  Activate:  source .venv/bin/activate"
echo "  Run:       manim -pql tutorials/5g-initial-setup/5g_initial_setup.py FiveGInitialSetup"
echo ""
