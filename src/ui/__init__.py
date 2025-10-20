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

# Core MVC components removed - using MVP pattern now
# Old: from .core.model import BoardModel
# Old: from .core.state import GameState
# New: Use ui/widgets/ and ui/implementations/*/presenters/

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
    # Abstractions (safe exports)
    'AbstractView',
    'AbstractInputHandler',
    'InputEvent',
    
    # Note: Import components directly:
    #   from ui.widgets import Button, Label, Panel
    #   from ui.common import Theme, LayoutManager, EventBus
    #   from ui.implementations.pygame.presenters import BoardPresenter
    #   from ui.implementations.pygame.renderers import BoardRenderer
]

__version__ = '3.1.0'

