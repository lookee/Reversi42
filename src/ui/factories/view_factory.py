"""
View Factory

Creates view instances based on type string.
Provides convenient methods for view creation.

Version: 3.1.0
"""

from typing import Optional
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Import views from their proper isolated locations
from ui.implementations.pygame.view import PygameBoardView  # New Pygame
from ui.implementations.terminal.view import TerminalBoardView  # New Terminal
from ui.implementations.headless.view import HeadlessBoardView  # New Headless


class ViewFactory:
    """
    Factory for creating view instances.
    
    Eventually will use views from ui.implementations.*
    For now, uses legacy Board views for compatibility.
    """
    
    @staticmethod
    def create_view(view_type: str, width: int, height: int,
                   window_width: int = 800, window_height: int = 600):
        """
        Create view instance based on type.
        
        Args:
            view_type: 'pygame', 'terminal', or 'headless'
            width: Board width in cells
            height: Board height in cells
            window_width: Display width
            window_height: Display height
            
        Returns:
            View instance
        """
        view_type = view_type.lower()
        
        if view_type in ['pygame', 'gui']:
            return PygameBoardView(width, height, window_width, window_height)
        elif view_type in ['terminal', 'console', 'ascii']:
            return TerminalBoardView(width, height, window_width, window_height)
        elif view_type in ['headless', 'none', 'null']:
            return HeadlessBoardView(width, height, window_width, window_height)
        else:
            raise ValueError(f"Unknown view type: {view_type}")
    
    @staticmethod
    def create_pygame_view(width: int, height: int, 
                          window_width: int = 800, window_height: int = 600):
        """Create Pygame view"""
        return PygameBoardView(width, height, window_width, window_height)
    
    @staticmethod
    def create_terminal_view(width: int, height: int,
                            window_width: int = 80, window_height: int = 24):
        """Create Terminal view"""
        return TerminalBoardView(width, height, window_width, window_height)
    
    @staticmethod
    def create_headless_view(width: int, height: int):
        """Create Headless view"""
        return HeadlessBoardView(width, height, 0, 0)

