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

# Core MVC components
from .core.model import BoardModel
from .core.state import GameState
from .core.controller import BoardController

# Abstract interfaces
from .abstractions.view_interface import AbstractView
from .abstractions.input_interface import AbstractInputHandler, InputEvent

# Input handlers (concrete implementations)
from .implementations.pygame.input_handler import PygameInputHandler
from .implementations.terminal.input_handler import TerminalInputHandler
from .implementations.headless.input_handler import HeadlessInputHandler

# Views will be imported later when implemented
# from .implementations.pygame.view import PygameView
# from .implementations.terminal.view import TerminalView
# from .implementations.headless.view import HeadlessView

# Factories
from .factories.view_factory import ViewFactory
from .factories.ui_factory import UIFactory

__all__ = [
    # Core
    'BoardModel',
    'GameState',
    'BoardController',
    
    # Abstractions
    'AbstractView',
    'AbstractInputHandler',
    'InputEvent',
    
    # Input Handlers
    'PygameInputHandler',
    'TerminalInputHandler',
    'HeadlessInputHandler',
    
    # Views - TODO: Add when implemented
    # 'PygameView',
    # 'TerminalView',
    # 'HeadlessView',
    
    # Factories
    'ViewFactory',
    'UIFactory',
]

__version__ = '3.1.0'

