# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['BMU_CANTOOL_V1.01.py','BMU_BalanceCtrl.py','BMU_CANCOMDEAL.py','BMU_CANPARASET.py','BMU_CANTOOL.py','DataTurn.py','PythonMemory.py'],
    pathex=['D:\\WorkSpace\\BMU_CANTool32\\UISource'],
    binaries=[],
    datas=[('..\Source\DLL\ControlCAN.dll','.'),('Cell_Power.xlsx','.')],
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
    [],
    exclude_binaries=True,
    name='BMU_CANTOOL_V1.01',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BMU_CANTOOL_V1.01',
)
