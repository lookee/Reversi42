"""
Game-Specific Widgets - Reversi UI Components

Widgets specific to Reversi42 game interface.
"""

from .board import BoardWidget
from .move_indicator import MoveIndicator
from .opening_tooltip import OpeningTooltip
from .score_panel import ScorePanel

__all__ = ["BoardWidget", "ScorePanel", "OpeningTooltip", "MoveIndicator"]
