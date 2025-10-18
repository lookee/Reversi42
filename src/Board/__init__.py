"""
Board Module - Modular MVC Architecture

Provides multiple view implementations for board visualization.

Version: 3.1.0
"""

# Core MVC components
from .BoardModel import BoardModel
from .BoardControl import BoardControl

# Abstract interface
from .AbstractBoardView import AbstractBoardView

# View implementations - all use lazy import for consistency
# PygameBoardView: lazy import
# TerminalBoardView: lazy import
# HeadlessBoardView: lazy import

# Backward compatibility
from .BoardView import BoardView

# View factory
from .ViewFactory import ViewFactory

__all__ = [
    # Core
    'BoardModel',
    'BoardControl',
    
    # Views
    'AbstractBoardView',
    'BoardView',  # Backward compatible
    'PygameBoardView',
    # 'TerminalBoardView',  # Import directly from ui.implementations.terminal
    # 'HeadlessBoardView',  # Import directly from ui.implementations.headless
    
    # Factory
    'ViewFactory',
]

def __getattr__(name):
    """Lazy imports for ALL view implementations to avoid circular dependencies"""
    if name == 'PygameBoardView':
        from ui.implementations.pygame.view import PygameBoardView
        return PygameBoardView
    elif name == 'TerminalBoardView':
        from ui.implementations.terminal import TerminalBoardView
        return TerminalBoardView
    elif name == 'HeadlessBoardView':
        from ui.implementations.headless import HeadlessBoardView
        return HeadlessBoardView
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

