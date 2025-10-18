"""
Abstract Player Base Class

Strategy Pattern: Defines interface for all players.

Version: 3.2.0
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Player(ABC):
    """
    Abstract base class for all players.
    
    Strategy Pattern: Different player implementations.
    
    All players must implement:
    - get_move(): Return a move given game state
    
    Example:
        class MyPlayer(Player):
            def get_move(self, game, moves, control):
                return moves[0]
    """
    
    # Class-level metadata for menu generation
    PLAYER_METADATA = {
        'display_name': 'Player',
        'description': 'Base player class',
        'enabled': False,  # Not selectable by default
        'parameters': []
    }
    
    def __init__(self, name: str = 'Player'):
        """
        Initialize player.
        
        Args:
            name: Player display name
        """
        self.name = name
    
    @abstractmethod
    def get_move(self, game, move_list, control):
        """
        Get player's move for current position.
        
        Args:
            game: Game state object
            move_list: List of valid moves
            control: Board control object
        
        Returns:
            Move: Selected move or None to quit
        """
        pass
    
    def get_name(self) -> str:
        """Get player display name."""
        return self.name
    
    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """Get player metadata for menu generation."""
        return cls.PLAYER_METADATA.copy()
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"

