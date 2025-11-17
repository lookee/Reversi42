# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Reversi42
Creates standalone executables for Windows, Linux, and macOS
"""

import os
from pathlib import Path

# Get project root
project_root = Path(SPECPATH)
src_dir = project_root / 'src'
icons_dir = project_root / 'icons'

# Icon paths (optional - will use default if not found)
icon_paths = {
    'windows': icons_dir / 'reversi42.ico',
    'macos': icons_dir / 'reversi42.icns',
    'linux': icons_dir / 'reversi42.png',
}

# Determine icon based on platform
import sys
if sys.platform == 'win32':
    icon_file = icon_paths['windows'] if icon_paths['windows'].exists() else None
elif sys.platform == 'darwin':
    icon_file = icon_paths['macos'] if icon_paths['macos'].exists() else None
else:
    icon_file = icon_paths['linux'] if icon_paths['linux'].exists() else None

icon_str = str(icon_file) if icon_file and icon_file.exists() else None

# Collect all data files needed at runtime
datas = []

# WebGUI templates
datas += [
    (str(src_dir / 'webgui' / 'templates'), 'webgui/templates'),
    (str(src_dir / 'webgui' / 'css'), 'webgui/css'),
    (str(src_dir / 'webgui' / 'js'), 'webgui/js'),
    (str(src_dir / 'webgui' / 'game_websocket.html'), 'webgui'),
]

# Configuration files
datas += [
    ('config/game.yaml', 'config'),
    ('config/players', 'config/players'),
]

# Domain knowledge data
datas += [
    (str(src_dir / 'domain' / 'knowledge' / 'data'), 'domain/knowledge/data'),
]

# Images
if (src_dir / 'Images').exists():
    datas += [
        (str(src_dir / 'Images'), 'Images'),
    ]

# Hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    'uvicorn',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.logging',
    'fastapi',
    'fastapi.staticfiles',
    'fastapi.templating',
    'websockets',
    'websockets.server',
    'websockets.client',
    'yaml',
    'multipart',
    'multipart.multipart',
    'pydantic',
    'pydantic.fields',
    'pydantic.types',
    'starlette',
    'starlette.applications',
    'starlette.routing',
    'starlette.responses',
    'starlette.staticfiles',
    'starlette.templating',
    'jinja2',
    'jinja2.ext',
    'Reversi',
    'Reversi.BitboardGame',
    'Reversi.Game',
    'Board',
    'Board.BoardModel',
    'Board.BoardControl',
    'Board.AbstractBoardView',
    'Players',
    'Players.Player',
    'Players.PlayerFactory',
    'Players.PlayerApocalyptron',
    'Players.config',
    'Players.config.PlayerRegistry',
    'AI',
    'AI.Apocalyptron',
    'webgui',
    'webgui.server',
    'webgui.server.reversi42_server',
    'webgui.server.websocket_observer',
    'core',
    'core.config',
    'core.game_config',
    'domain',
    'domain.knowledge',
]

a = Analysis(
    ['src/webgui/cli.py'],
    pathex=[str(src_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'pytest_cov',
        'pylint',
        'black',
        'mypy',
        'ipdb',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='reversi42',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for server output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_str,  # Icon path (auto-detected from icons/ directory)
)

