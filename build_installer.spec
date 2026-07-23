# -*- mode: python ; coding: utf-8 -*-

"""
Build the Windows tkinter version of Stickity Stacks.
"""

a = Analysis(
    ["stickity_stacks_win.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["gi"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="StickityStacks",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon="stickity_stacks.ico",
)
