"""
Game State - Shared State Container

Immutable game state shared between MVC components.
Uses dataclass for clean, type-safe state management.

Architecture: State object in MVC
Version: 3.1.0
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class GameState:
    """
    Game state container.
    
    Holds all game state information that needs to be shared
    between Model, View, and Controller.
    
    Design: Immutable (use frozen=True for strict immutability)
    """
    
    # Board state
    size_x: int = 8
    size_y: int = 8
    
    # Score
    black_score: int = 2
    white_score: int = 2
    
    # Turn management
    current_turn: str = 'B'  # 'B' for Black, 'W' for White
    
    # Player info
    black_player_name: str = "Black"
    white_player_name: str = "White"
    
    # Moves
    valid_moves: List[Tuple[int, int]] = field(default_factory=list)
    last_move: Optional[Tuple[int, int]] = None
    move_history: str = ""
    
    # Cursor/selection
    cursor_position: Tuple[int, int] = (3, 3)
    cursor_mode: bool = False
    
    # Game state flags
    game_over: bool = False
    winner: Optional[str] = None
    should_exit: bool = False
    should_pause: bool = False
    wait_input: bool = False
    
    # Opening book
    show_opening: bool = False
    book_moves: List[Tuple[int, int, int]] = field(default_factory=list)  # (x, y, count)
    
    # Input state
    selected_position: Optional[Tuple[int, int]] = None
    
    def reset(self):
        """Reset state to initial values"""
        self.black_score = 2
        self.white_score = 2
        self.current_turn = 'B'
        self.valid_moves = []
        self.last_move = None
        self.move_history = ""
        self.game_over = False
        self.winner = None
        self.should_exit = False
        self.should_pause = False
    
    def to_dict(self) -> dict:
        """Convert state to dictionary"""
        return {
            'black_score': self.black_score,
            'white_score': self.white_score,
            'current_turn': self.current_turn,
            'black_player_name': self.black_player_name,
            'white_player_name': self.white_player_name,
            'valid_moves': self.valid_moves,
            'last_move': self.last_move,
            'game_over': self.game_over,
            'winner': self.winner,
        }

