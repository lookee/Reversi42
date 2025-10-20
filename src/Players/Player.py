"""
Player - Base class for all players

Clean Architecture: Players are in the domain layer and should NOT
depend on UI frameworks (pygame, etc.)

Design Pattern: Template Method
"""

from typing import List, Optional
from Reversi.Game import Move


class Player(object):
    """
    Base class for all players.
    
    This is the domain layer - NO UI dependencies allowed here!
    Players depend on abstractions (InputProvider), not concrete implementations.
    
    Subclasses can define class-level metadata for automatic menu generation.
    """
    
    # Class-level metadata for menu generation
    PLAYER_METADATA = {
        'display_name': 'Player',
        'description': 'Base player class',
        'enabled': False,  # Not selectable by default
        'parameters': []  # List of configurable parameters
    }

    def __init__(self):
        self.name = 'Player'

    def get_name(self) -> str:
        """Get player name."""
        return self.name

    def get_move(self, game, move_list: List[Move], control=None) -> Optional[Move]:
        """
        Get next move from this player.
        
        Args:
            game: Current game state
            move_list: List of legal moves
            control: (DEPRECATED) BoardControl instance - use InputProvider instead
            
        Returns:
            Selected move, or None if exit/pause
        """
        # Default implementation: return first move
        return move_list[0] if move_list else None
    
    @classmethod
    def get_metadata(cls):
        """Get player metadata for menu generation"""
        return cls.PLAYER_METADATA
