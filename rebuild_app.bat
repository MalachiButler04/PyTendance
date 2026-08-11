@echo off
cd /d "%~dp0"
python -m PyInstaller PyTendance.spec
echo.
echo Build finished. Press any key to close.
pause >nul