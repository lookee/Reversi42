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

# View factory
from .ViewFactory import ViewFactory

# Backward compatibility: BoardView alias (was a wrapper for PygameBoardView)
# Created via lazy import to avoid circular dependency
def _get_boardview():
    from ui.implementations.pygame.view import PygameBoardView
    return PygameBoardView

__all__ = [
    # Core
    'BoardModel',
    'BoardControl',
    
    # Views
    'AbstractBoardView',
    'BoardView',  # Backward compatible (alias to PygameBoardView)
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
    elif name == 'BoardView':
        # Backward compatibility: BoardView is an alias for PygameBoardView
        from ui.implementations.pygame.view import PygameBoardView
        return PygameBoardView
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

