#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required" >&2
  exit 1
fi

if ! command -v pipx >/dev/null 2>&1; then
  echo "Installing pipx..."
  python3 -m pip install --user pipx >/dev/null
  python3 -m pipx ensurepath >/dev/null 2>&1 || true
  export PATH="$HOME/.local/bin:$PATH"
fi

pipx install --force bastyn-cli

echo
echo "✓ bastyn CLI installed"
echo "  Run: bastyn init"
