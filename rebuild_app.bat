@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set PYCMD=py
) else (
    set PYCMD=python
)

echo Rebuilding PyTendance.exe...
%PYCMD% -m PyInstaller PyTendance.spec --noconfirm
if errorlevel 1 (
    echo.
    echo Build failed. See the errors above.
    pause >nul
    exit /b 1
)

echo.
echo Build finished. PyTendance.exe has been updated on your Desktop.
pause >nul
