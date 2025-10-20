"""
Pygame UI Components

Menu, dialogs, and UI elements specific to Pygame implementation.

Version: 3.1.0
"""

from .menu import Menu
from .game_over import GameOver
from .pause_menu import PauseMenu

# Note: dialog_box.py has been replaced by ui.widgets.primitives.Dialog system!
# Use InputDialog, ListDialog, Dialog from ui.widgets.primitives instead.

__all__ = [
    'Menu',
    'GameOver',
    'PauseMenu',
]

