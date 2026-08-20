#!/usr/bin/env bash
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
    PYCMD=python3
else
    PYCMD=python
fi

echo "Rebuilding PyTendance.exe..."
"$PYCMD" -m PyInstaller PyTendance.spec --noconfirm
status=$?
echo

if [ $status -ne 0 ]; then
    read -n 1 -s -r -p "Build failed. See the errors above. Press any key to close."
    echo
    exit 1
fi

read -n 1 -s -r -p "Build finished. PyTendance.exe has been updated on your Desktop. Press any key to close."
echo