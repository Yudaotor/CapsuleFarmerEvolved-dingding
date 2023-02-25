# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py',
    'AssertCondition.py',
    'Browser.py',
    'Config.py',
    'DataProviderThread.py',
    'FarmThread.py',
    'GuiThread.py',
    'IMAP.py',
    'Logger.py',
    'Match.py',
    'Restarter.py',
    'SharedData.py',
    'Stats.py',
    'VersionManager.py',
    'Exceptions\\CapsuleFarmerEvolvedException.py',
    'Exceptions\\Fail2FAException.py',
    'Exceptions\\FailFind2FAException.py',
    'Exceptions\\InvalidCredentialsException.py',
    'Exceptions\\InvalidIMAPCredentialsException.py',
    'Exceptions\\NoAccessTokenException.py',
    'Exceptions\\RateLimitException.py',
    'Exceptions\\StatusCodeAssertException.py'
    ],
    pathex=['C:\\Users\\Khalil\\Desktop\\src\\CapsuleFarmerEvolved-dingding\\src'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CapsuleFarmerEvolvedV1.43-dingding',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\Users\\Khalil\\Desktop\\src\\CapsuleFarmerEvolved-dingding\\poro.ico'
)
