"""
TerminalPresenter - MVP Presenter for Terminal UI

Handles presentation logic for terminal board view.
Separates business logic from rendering.

Design Pattern: MVP (Model-View-Presenter)
"""

from typing import List, Tuple, Optional, Dict, Any


class TerminalPresenter:
    """
    Presenter for terminal board view.
    
    Responsibilities:
    - Manage board state
    - Handle valid moves
    - Track last move
    - Manage opening book info
    - Prepare data for view rendering
    
    The View only renders what the Presenter tells it.
    """
    
    def __init__(self, board_size: int = 8):
        """
        Initialize presenter.
        
        Args:
            board_size: Size of the board (default 8x8)
        """
        self.board_size = board_size
        
        # Model data
        self.board_state = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.valid_moves = []
        self.last_move = None
        self.book_moves = {}
        
        # Game info
        self.black_count = 2
        self.white_count = 2
        self.current_turn = 'X'
        self.move_count = 0
        
        # Player info
        self.black_player_name = "Black"
        self.white_player_name = "White"
        
        # Opening info
        self.opening_name = None
        self.opening_variation = None
    
    def update_from_model(self, model: Any):
        """
        Update presenter state from board model.
        
        Args:
            model: BoardModel instance
        """
        # Update board state
        for y in range(self.board_size):
            for x in range(self.board_size):
                self.board_state[y][x] = model.matrix[y + 1][x + 1]
        
        # Update counts
        self.black_count = model.black_cnt
        self.white_count = model.white_cnt
        self.current_turn = model.turn
        self.move_count = model.turn_cnt
    
    def set_piece(self, x: int, y: int, color: str):
        """
        Set a piece on the board.
        
        Args:
            x, y: Board coordinates (0-based)
            color: Piece color ('X' or 'O')
        """
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            self.board_state[y][x] = color
    
    def clear_piece(self, x: int, y: int):
        """Clear a piece from the board."""
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            self.board_state[y][x] = ' '
    
    def set_valid_moves(self, moves: List[Tuple[int, int]]):
        """
        Set list of valid moves.
        
        Args:
            moves: List of (x, y) tuples (0-based coordinates)
        """
        self.valid_moves = moves
    
    def set_last_move(self, x: int, y: int):
        """
        Set the last move position.
        
        Args:
            x, y: Board coordinates (0-based)
        """
        self.last_move = (x, y)
    
    def set_book_moves(self, moves: Dict[Tuple[int, int], int]):
        """
        Set opening book moves with counts.
        
        Args:
            moves: Dict mapping (x, y) to occurrence count
        """
        self.book_moves = moves
    
    def clear_book_moves(self):
        """Clear opening book moves."""
        self.book_moves = {}
    
    def set_player_counts(self, black_count: int, white_count: int):
        """Update player piece counts."""
        self.black_count = black_count
        self.white_count = white_count
    
    def set_player_names(self, black_name: str, white_name: str):
        """Update player names."""
        self.black_player_name = black_name
        self.white_player_name = white_name
    
    def set_current_turn(self, turn: str):
        """Update current turn."""
        self.current_turn = turn
    
    def set_opening_info(self, opening_name: str, variation: str = ""):
        """Set opening book information."""
        self.opening_name = opening_name
        self.opening_variation = variation
    
    def clear_opening_info(self):
        """Clear opening book information."""
        self.opening_name = None
        self.opening_variation = None
    
    def get_render_data(self) -> Dict[str, Any]:
        """
        Get all data needed for rendering.
        
        Returns:
            Dict with all presentation data
        """
        return {
            'board_state': self.board_state,
            'valid_moves': self.valid_moves,
            'last_move': self.last_move,
            'book_moves': self.book_moves,
            'black_count': self.black_count,
            'white_count': self.white_count,
            'current_turn': self.current_turn,
            'move_count': self.move_count,
            'black_player_name': self.black_player_name,
            'white_player_name': self.white_player_name,
            'opening_name': self.opening_name,
            'opening_variation': self.opening_variation
        }

