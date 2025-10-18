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

# View implementations
from .PygameBoardView import PygameBoardView
from .TerminalBoardView import TerminalBoardView
from .HeadlessBoardView import HeadlessBoardView

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
    'TerminalBoardView',
    'HeadlessBoardView',
    
    # Factory
    'ViewFactory',
]

