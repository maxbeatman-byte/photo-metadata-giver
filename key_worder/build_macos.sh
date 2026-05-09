#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(pwd)"
VENV="${ROOT}/../.venv/bin/pyinstaller"
if [[ ! -x "$VENV" ]]; then
  echo "Run from key_worder/; expected ../.venv/bin/pyinstaller" >&2
  exit 1
fi
"$VENV" --noconfirm main.spec
cp -f prompt.txt dist/prompt.txt
echo "OK: dist/key_worder and dist/prompt.txt"
