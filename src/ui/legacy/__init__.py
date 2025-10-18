"""
Legacy Compatibility Layer

Provides backward compatibility wrappers that allow existing code
to continue working while using the new architecture underneath.

This layer will be deprecated in v4.0.0

Version: 3.1.0
"""

# Import from original Board module for now
# These are just aliases to maintain compatibility

import sys
import os

# Add Board to path
board_path = os.path.join(os.path.dirname(__file__), '../..')
if board_path not in sys.path:
    sys.path.insert(0, board_path)

# Import from existing Board module and new ui module
from Board.BoardModel import BoardModel
from Board.BoardControl import BoardControl
from Board.BoardView import BoardView
from Board.PygameBoardView import PygameBoardView
from ui.implementations.terminal import TerminalBoardView  # New location
from ui.implementations.headless import HeadlessBoardView  # New location
from Board.ViewFactory import ViewFactory
from Board.AbstractBoardView import AbstractBoardView

# Import TerminalHumanPlayer from new location
from ui.implementations.terminal import TerminalHumanPlayer

__all__ = [
    'BoardModel',
    'BoardControl',
    'BoardView',
    'PygameBoardView',
    'TerminalBoardView',
    'TerminalHumanPlayer',
    'HeadlessBoardView',
    'ViewFactory',
    'AbstractBoardView',
]

