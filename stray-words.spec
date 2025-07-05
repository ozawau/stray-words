# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['./src'],
    binaries=[],
    datas=[('src', 'src'), ('wordlists', 'wordlists')],
    hiddenimports=['pystray', 'PIL', 'PIL._tkinter_finder', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont', 'pyperclip', 'yaml', 'sqlite3', 'service', 'service.config_loader', 'service.words_loader', 'service.wordbook_service', 'service.view_menu_service', 'service.dao', 'service.dao.wordbook_dao', 'service.dao.wordlist_dao', 'model', 'model.config', 'model.constants', 'model.sqlite', 'model.sqlite.base_model', 'model.sqlite.wordbook', 'model.sqlite.wordlist', 'app_platform', 'app_platform.windows', 'app_platform.macos'],
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
    name='stray-words',
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
)
