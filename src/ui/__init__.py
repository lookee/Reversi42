"""
UI Package - Modular MVC Architecture

Professional MVC implementation with complete separation of concerns:
- Model: Domain logic (core/model.py)
- View: Pure rendering (abstractions/view_interface.py)
- Controller: Orchestration (core/controller.py)
- Input: Event handling (abstractions/input_interface.py)

Architecture: Clean MVC with Dependency Inversion
Note: Pygame and terminal views removed in favor of web-based interface
"""

# Core MVC components removed - using MVP pattern now
# Old: from .core.model import BoardModel
# Old: from .core.state import GameState

from .abstractions.input_interface import AbstractInputHandler, InputEvent

# Abstract interfaces (safe to import - no dependencies)
from .abstractions.view_interface import AbstractView

# Lazy imports to avoid circular dependencies
# Import implementations and factories only when needed
# Users should import directly from submodules:
#   from ui.implementations.headless import HeadlessBoardView
#   from ui.factories.ui_factory import UIFactory

# Note: Controller imported separately to avoid circular deps
# from .core.controller import BoardController

__all__ = [
    # Abstractions (safe exports)
    "AbstractView",
    "AbstractInputHandler",
    "InputEvent",
]

# Import version from centralized location
try:
    from __version__ import __version__
except ImportError:
    __version__ = "6.1.2"  # Fallback (must match pyproject.toml)
