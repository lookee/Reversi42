"""
PlayerInterface - Abstract base class for all players

Defines the contract that all player implementations must follow.
This ensures consistency and allows polymorphic usage.

Design Pattern: Template Method + Strategy
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from Reversi.Game import Move


class PlayerInterface(ABC):
    """
    Abstract base class for all players.
    
    All player types (Human, AI, Network) must implement this interface.
    This ensures consistent API and enables polymorphic usage.
    """
    
    # Class-level metadata for menu generation
    PLAYER_METADATA = {
        'display_name': 'Player',
        'description': 'Base player class',
        'enabled': False,
        'parameters': []
    }
    
    @abstractmethod
    def __init__(self):
        """Initialize player with a name"""
        self.name = 'Player'
    
    def get_name(self) -> str:
        """
        Get player name.
        
        Returns:
            Player's name
        """
        return self.name
    
    @abstractmethod
    def get_move(self, game, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get the next move from this player.
        
        This is the main method that must be implemented by all players.
        
        Args:
            game: Current game state
            legal_moves: List of legal moves available
            
        Returns:
            Selected move, or None if player wants to exit/pause
        """
        pass
    
    @classmethod
    def get_metadata(cls):
        """
        Get player metadata for menu generation.
        
        Returns:
            Dictionary with player metadata
        """
        return cls.PLAYER_METADATA

