import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None
icon_file = 'imagenes/icono.ico' if sys.platform.startswith('win') else None

a = Analysis(
    ['principal.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('imagenes/error.png', 'imagenes'),
        ('imagenes/icono.ico', 'imagenes'),
        ('imagenes/LedLogin.gif', 'imagenes'),
        ('imagenes/logo.png', 'imagenes'),
        ('imagenes/informacion.png', 'imagenes'),
        ('.env', '.'),
    ],
    hiddenimports=collect_submodules('PIL'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LedsUp',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    icon=icon_file,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='LedsUp_dist'
)
