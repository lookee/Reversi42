"""
MockInputProvider - Mock implementation for testing

Provides predefined moves for automated testing.
No UI dependencies!

Design Pattern: Mock Object
"""

from typing import Optional, List, Iterator
from Reversi.Game import Move
from Players.abstractions import InputProvider


class MockInputProvider(InputProvider):
    """
    Mock InputProvider for testing.
    
    Returns predefined moves from an iterable.
    Perfect for unit testing PlayerHuman without any UI.
    
    Example:
        moves = [Move(3, 3), Move(4, 4)]
        provider = MockInputProvider(moves)
        player = PlayerHuman(provider)
        # Will return moves in order
    """
    
    def __init__(self, moves: List[Move], auto_exit: bool = True):
        """
        Initialize mock input provider.
        
        Args:
            moves: List of moves to return
            auto_exit: If True, exit after all moves are consumed
        """
        self.moves_iter: Iterator[Move] = iter(moves)
        self.auto_exit = auto_exit
        self._exit_requested = False
        self._pause_requested = False
        self._moves_exhausted = False
    
    def get_move_input(self, game, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get next predefined move.
        
        Args:
            game: Current game state (ignored)
            legal_moves: List of legal moves (for validation)
            
        Returns:
            Next move from list, or None if exhausted
        """
        try:
            move = next(self.moves_iter)
            
            # Validate move is legal
            if move not in legal_moves:
                raise ValueError(f"Predefined move {move} is not legal!")
            
            return move
        except StopIteration:
            self._moves_exhausted = True
            if self.auto_exit:
                self._exit_requested = True
            return None
    
    def should_exit(self) -> bool:
        """Check if exit should happen."""
        return self._exit_requested
    
    def should_pause(self) -> bool:
        """Check if pause requested."""
        return self._pause_requested
    
    def reset(self):
        """Reset to start of moves list."""
        self._exit_requested = False
        self._pause_requested = False
        self._moves_exhausted = False

