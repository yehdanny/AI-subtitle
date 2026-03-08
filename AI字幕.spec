# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

whisper_datas = collect_data_files("whisper")
tiktoken_datas = collect_data_files("tiktoken")

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("templates", "templates"),
    ] + whisper_datas + tiktoken_datas,
    hiddenimports=[
        "whisper",
        "whisper.audio",
        "whisper.model",
        "whisper.tokenizer",
        "whisper.transcribe",
        "whisper.utils",
        "tiktoken",
        "tiktoken_ext",
        "tiktoken_ext.openai_public",
        "imageio_ffmpeg",
        "flask",
        "werkzeug",
        "werkzeug.serving",
        "werkzeug.routing",
        "jinja2",
        "numpy",
        "numba",
        "tqdm",
    ] + collect_submodules("torch"),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "IPython", "pandas", "scipy", "sklearn"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AI字幕",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="AI字幕",
)
