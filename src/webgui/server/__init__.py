"""
Reversi42 WebGUI Server

WebSocket backend server for real-time Reversi42 gameplay
Provides bridge between web frontend and game engine

Components:
  - reversi42_server.py: Main WebSocket server
  - websocket_observer.py: AI search observer for live insights
"""

# Import version from centralized location
try:
    from __version__ import __version__
except ImportError:
    __version__ = "6.2.0"  # Fallback (must match pyproject.toml)
