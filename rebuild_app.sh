#!/usr/bin/env bash
cd "$(dirname "$0")"
python3 -m PyInstaller PyTendance.spec
echo
read -n 1 -s -r -p "Build finished. Press any key to close."
echo
