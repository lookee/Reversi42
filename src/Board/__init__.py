"""
Board Module - Modular MVC Architecture

Provides multiple view implementations for board visualization.

Version: 3.2.0 - Cleaned up, removed pygame and terminal views
"""

# Abstract interface
from .AbstractBoardView import AbstractBoardView
from .BoardControl import BoardControl

# Core MVC components
from .BoardModel import BoardModel

# View factory
from .ViewFactory import ViewFactory

# View implementations - all use lazy import for consistency
# HeadlessBoardView: lazy import


__all__ = [
    # Core
    "BoardModel",
    "BoardControl",
    # Views
    "AbstractBoardView",
    # Factory
    "ViewFactory",
]


def __getattr__(name):
    """Lazy imports for view implementations to avoid circular dependencies"""
    if name == "HeadlessBoardView":
        from ui.implementations.headless import HeadlessBoardView

        return HeadlessBoardView
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
