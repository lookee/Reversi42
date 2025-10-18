"""
UI Core - Core MVC Components

Model, Controller, and shared State.
Completely framework-independent.

Version: 3.1.0
"""

from .model import BoardModel
from .state import GameState
from .controller import BoardController

__all__ = ['BoardModel', 'GameState', 'BoardController']

