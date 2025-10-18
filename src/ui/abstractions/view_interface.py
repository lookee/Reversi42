"""
Abstract View Interface

Defines the contract for all view implementations.
Pure rendering responsibilities - NO input handling.

Architecture: Following Single Responsibility Principle
Version: 3.1.0
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any


class AbstractView(ABC):
    """
    Pure view interface - ONLY rendering responsibilities.
    
    Responsibilities:
    - Render game state visually
    - Display information
    - Update display
    - Clear display
    
    NOT responsible for:
    - Input handling (that's InputHandler's job)
    - Game logic (that's Model's job)
    - Event coordination (that's Controller's job)
    
    Design Philosophy:
    - View is a pure function: State → Visual Output
    - No state modification
    - No event handling
    - No framework leakage in interface
    """
    
    def __init__(self, width: int, height: int, window_width: int, window_height: int):
        """
        Initialize view.
        
        Args:
            width: Board width in cells
            height: Board height in cells
            window_width: Display width (pixels or characters)
            window_height: Display height (pixels or characters)
        """
        self.width = width
        self.height = height
        self.window_width = window_width
        self.window_height = window_height
    
    # Core Rendering Methods
    
    @abstractmethod
    def render_board(self, board_state: List[List[str]]):
        """
        Render complete board with current state.
        
        Args:
            board_state: 2D array of board state
                - 'B' or 'X' = Black piece
                - 'W' or 'O' = White piece
                - ' ' or '.' = Empty
                - 'b' = Valid move for black
                - 'w' = Valid move for white
        """
        pass
    
    @abstractmethod
    def render_piece(self, x: int, y: int, piece_type: str):
        """
        Render single piece at position.
        
        Args:
            x: Column (0-indexed)
            y: Row (0-indexed)
            piece_type: 'B', 'W', or ' '
        """
        pass
    
    @abstractmethod
    def highlight_cells(self, positions: List[Tuple[int, int]], 
                       highlight_type: str):
        """
        Highlight specific cells.
        
        Args:
            positions: List of (x, y) tuples
            highlight_type: Type of highlight
                - 'valid_move'
                - 'last_move'
                - 'cursor'
                - 'book_move'
        """
        pass
    
    @abstractmethod
    def update_display(self):
        """
        Update/refresh the display.
        
        Flush all pending rendering operations to screen.
        """
        pass
    
    @abstractmethod
    def clear_display(self):
        """Clear entire display"""
        pass
    
    # Information Display
    
    @abstractmethod
    def show_game_info(self, info: Dict[str, Any]):
        """
        Display game information.
        
        Args:
            info: Dictionary with game info:
                {
                    'black_score': int,
                    'white_score': int,
                    'current_turn': str,  # 'B' or 'W'
                    'black_player_name': str,
                    'white_player_name': str,
                }
        """
        pass
    
    @abstractmethod
    def show_message(self, message: str, duration: float = 0):
        """
        Show temporary message.
        
        Args:
            message: Message text
            duration: Display duration in seconds (0 = until next update)
        """
        pass
    
    def show_opening_info(self, opening_info: Optional[Dict]):
        """
        Show opening book information (optional).
        
        Args:
            opening_info: Opening book data or None
        """
        pass  # Optional - views can override
    
    # Lifecycle Methods
    
    def initialize(self):
        """
        Initialize view resources.
        
        Called once before first render.
        """
        pass  # Optional - views can override
    
    def cleanup(self):
        """
        Cleanup view resources.
        
        Called when view is destroyed.
        """
        pass  # Optional - views can override
    
    def resize(self, width: int, height: int):
        """
        Handle resize event.
        
        Args:
            width: New width
            height: New height
        """
        pass  # Optional - views can override
    
    # Utility Methods
    
    def get_capabilities(self) -> Dict[str, bool]:
        """
        Get view capabilities.
        
        Returns:
            Dict with capabilities:
            {
                'supports_mouse': bool,
                'supports_resize': bool,
                'supports_animation': bool,
                'supports_color': bool,
            }
        """
        return {
            'supports_mouse': False,
            'supports_resize': False,
            'supports_animation': False,
            'supports_color': False,
        }

