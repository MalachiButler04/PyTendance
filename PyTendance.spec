# -*- mode: python ; coding: utf-8 -*-

import os
import sys

from PyInstaller.config import CONF
from PyInstaller.utils.hooks import collect_data_files

# Always build straight to the Desktop instead of the local dist/ folder.
# Prefer the OneDrive-redirected Desktop when present, since that's the real one on this machine.
_onedrive = os.environ.get('OneDrive')
if _onedrive and os.path.isdir(os.path.join(_onedrive, 'Desktop')):
    _desktop = os.path.join(_onedrive, 'Desktop')
else:
    _desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
CONF['distpath'] = _desktop

ttkbootstrap_datas = collect_data_files('ttkbootstrap')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('config/book_config.json', 'config'), ('config/students_config.json', 'config'), ('config/config_docs.md', 'config')] + ttkbootstrap_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=False,
    name='PyTendance',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/app_icon.ico'] if sys.platform == 'win32' else None,
)
