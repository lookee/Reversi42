"""
UI Package - Modular MVC Architecture

Professional MVC implementation with complete separation of concerns:
- Model: Domain logic (core/model.py)
- View: Pure rendering (abstractions/view_interface.py)
- Controller: Orchestration (core/controller.py)
- Input: Event handling (abstractions/input_interface.py)

Version: 3.1.0
Architecture: Clean MVC with Dependency Inversion
"""

# Core MVC components (safe to import - no dependencies)
from .core.model import BoardModel
from .core.state import GameState

# Abstract interfaces (safe to import - no dependencies)
from .abstractions.view_interface import AbstractView
from .abstractions.input_interface import AbstractInputHandler, InputEvent

# Lazy imports to avoid circular dependencies
# Import implementations and factories only when needed
# Users should import directly from submodules:
#   from ui.implementations.pygame import PygameInputHandler
#   from ui.implementations.terminal import TerminalBoardView
#   from ui.factories.ui_factory import UIFactory

# Note: Controller imported separately to avoid circular deps
# from .core.controller import BoardController

__all__ = [
    # Core (safe exports)
    'BoardModel',
    'GameState',
    
    # Abstractions (safe exports)
    'AbstractView',
    'AbstractInputHandler',
    'InputEvent',
    
    # Note: Import implementations and factories directly:
    #   from ui.implementations.pygame import PygameInputHandler
    #   from ui.implementations.terminal import TerminalBoardView
    #   from ui.implementations.headless import HeadlessInputHandler
    #   from ui.factories.ui_factory import UIFactory
    #   from ui.core.controller import BoardController
]

__version__ = '3.1.0'

