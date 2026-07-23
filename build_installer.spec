# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Stickity Stacks
Builds a Windows executable with embedded icon and proper metadata
"""

a = Analysis(
    ['stickity_stacks.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['gi', 'gi.repository.Gtk', 'gi.repository.Gdk', 'gi.repository.Pango'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StickityStacks',
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
    icon='stickity_stacks.ico',
)
