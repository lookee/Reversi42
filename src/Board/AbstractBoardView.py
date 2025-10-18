"""
AbstractBoardView - Interface for Board Visualization

This abstract class defines the interface that all board view implementations
must follow. It enables multiple UI implementations (Pygame, Terminal, Web, etc.)
without changing the core game logic.

Version: 3.1.0
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any


class AbstractBoardView(ABC):
    """
    Abstract interface for board visualization.
    
    Any view implementation must implement these methods to be compatible
    with the Reversi42 game system.
    
    This allows for multiple UI implementations:
    - PygameBoardView: Graphical UI with Pygame
    - TerminalBoardView: ASCII art in terminal
    - HeadlessBoardView: No rendering (for tournaments)
    - WebBoardView: HTML/WebSocket for web apps
    """
    
    def __init__(self, sizex: int, sizey: int, width: int, height: int):
        """
        Initialize the view.
        
        Args:
            sizex: Board width in cells
            sizey: Board height in cells
            width: Display width in pixels (or columns for terminal)
            height: Display height in pixels (or rows for terminal)
        """
        self.sizex = sizex
        self.sizey = sizey
        self.width = width
        self.height = height
        
        # Common state
        self.cursorX = None
        self.cursorY = None
        self.last_move_x = None
        self.last_move_y = None
        
        # Player information
        self.black_player_name = "Black"
        self.white_player_name = "White"
        self.black_count = 2
        self.white_count = 2
        self.current_turn = 'B'
    
    @abstractmethod
    def initialize(self):
        """
        Initialize the view (create window, setup display, etc.).
        
        This is called once at view creation.
        """
        pass
    
    @abstractmethod
    def render_board(self, model):
        """
        Render the complete board with all pieces.
        
        Args:
            model: BoardModel instance with current board state
        """
        pass
    
    @abstractmethod
    def render_piece(self, x: int, y: int, color: str):
        """
        Render a single piece at the specified position.
        
        Args:
            x: X coordinate (0-based)
            y: Y coordinate (0-based)
            color: 'B' for black, 'W' for white
        """
        pass
    
    @abstractmethod
    def highlight_valid_moves(self, moves: List[Tuple[int, int]]):
        """
        Highlight squares where moves are valid.
        
        Args:
            moves: List of (x, y) tuples representing valid moves
        """
        pass
    
    @abstractmethod
    def highlight_last_move(self, x: int, y: int):
        """
        Highlight the last move played.
        
        Args:
            x: X coordinate (1-based, from Move object)
            y: Y coordinate (1-based, from Move object)
        """
        pass
    
    @abstractmethod
    def update_display(self, cursor_mode: bool = False):
        """
        Update/refresh the display.
        
        Args:
            cursor_mode: Whether cursor navigation is active
        """
        pass
    
    @abstractmethod
    def clear_display(self):
        """Clear the entire display."""
        pass
    
    @abstractmethod
    def set_cursor(self, x: int, y: int):
        """
        Set cursor position.
        
        Args:
            x: X coordinate (0-based)
            y: Y coordinate (0-based)
        """
        pass
    
    @abstractmethod
    def get_cursor_position(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Get current cursor position.
        
        Returns:
            Tuple of (x, y) coordinates (0-based), or (None, None)
        """
        pass
    
    @abstractmethod
    def point_to_board_position(self, screen_x: int, screen_y: int) -> Tuple[Optional[int], Optional[int]]:
        """
        Convert screen coordinates to board position.
        
        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate
            
        Returns:
            Tuple of (board_x, board_y) coordinates (0-based), or (None, None)
        """
        pass
    
    @abstractmethod
    def set_player_info(self, black_name: str, white_name: str, 
                       black_count: int, white_count: int, current_turn: str):
        """
        Update player information display.
        
        Args:
            black_name: Black player name
            white_name: White player name
            black_count: Number of black pieces
            white_count: Number of white pieces
            current_turn: 'B' or 'W'
        """
        pass
    
    @abstractmethod
    def show_message(self, message: str, duration: float = 2.0):
        """
        Display a temporary message.
        
        Args:
            message: Message to display
            duration: How long to show (seconds)
        """
        pass
    
    @abstractmethod
    def resize(self, width: int, height: int):
        """
        Handle window/display resize.
        
        Args:
            width: New width
            height: New height
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """
        Cleanup resources (close window, free memory, etc.).
        """
        pass
    
    # Optional methods with default implementations
    
    def set_opening_info(self, info: Optional[List[str]]):
        """
        Set opening book information to display (optional).
        
        Args:
            info: List of opening names, or None
        """
        # Default: do nothing
        pass
    
    def draw_opening_info_fixed(self):
        """
        Draw opening book info in fixed position (optional).
        """
        # Default: do nothing
        pass
    
    def clear_tooltip_area(self):
        """
        Clear tooltip/info area (optional).
        """
        # Default: do nothing
        pass
    
    def set_book_moves(self, book_moves: List[Tuple[int, int, int]]):
        """
        Set list of opening book moves with counts (optional).
        
        Args:
            book_moves: List of (x, y, count) tuples
        """
        # Default: do nothing
        pass
    
    def get_window_size(self) -> Tuple[int, int]:
        """
        Get current window/display size.
        
        Returns:
            Tuple of (width, height)
        """
        return (self.width, self.height)

