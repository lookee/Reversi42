#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Reversi42 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Reversi42.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

"""
Player Factory - Backward Compatibility Wrapper

This file maintains backward compatibility by delegating to the new
modular architecture (PlayerFactoryV2).

ALL AI PLAYERS now use the new architecture:
- Players/ai/ai_player.py (ONE class with Dependency Injection)
- AI/factory/engine_builder.py (Builder Pattern)
- AI/features/ (Decorator Pattern)

Legacy player files (AIPlayer.py, AIPlayerBook.py, etc.) have been REMOVED
as they are now obsolete.

Version: 3.2.0
Architecture: Wrapper around PlayerFactoryV2
"""

# New architecture
from Players.factory.player_factory_v2 import PlayerFactoryV2

# Legacy players (still used)
from Players.Monkey import Monkey
from Players.HumanPlayer import HumanPlayer
from Players.NetworkPlayer import NetworkPlayer
from Players.Player import Player


class PlayerFactory:
    """
    Factory class for creating different types of players.
    
    This is now a WRAPPER around the new PlayerFactoryV2 architecture.
    All functionality is delegated to the modular system.
    
    Maintains backward compatibility with existing code while using
    the new enterprise architecture internally.
    
    Version: 3.2.0 - Refactored to use modular architecture
    """
    
    @staticmethod
    def create_player(player_type, **kwargs):
        """
        Create a player by type name.
        Delegates to PlayerFactoryV2.
        
        Args:
            player_type: Display name of player type
            **kwargs: Additional parameters (deep, show_book_options, etc.)
        
        Returns:
            Player instance
        """
        return PlayerFactoryV2.create_player(player_type, **kwargs)
    
    @staticmethod
    def create_ai_player(engine_type='Minimax', difficulty=6):
        """
        Create an AI player with specified engine and difficulty.
        Delegates to PlayerFactoryV2.
        
        Args:
            engine_type: Type of engine ('Minimax', 'Bitboard', 'Grandmaster')
            difficulty: Difficulty level (depth)
        
        Returns:
            AI player instance
        """
        return PlayerFactoryV2.create_ai_player(engine_type, difficulty)
    
    @staticmethod
    def get_player_metadata(player_type):
        """
        Get metadata for a player type.
        Delegates to PlayerFactoryV2.
        
        Args:
            player_type: Player type name
        
        Returns:
            dict: Player metadata
        """
        return PlayerFactoryV2.get_player_metadata(player_type)
    
    @staticmethod
    def list_available_players():
        """
        List all available player types.
        Delegates to PlayerFactoryV2.
        
        Returns:
            dict: Available players with metadata
        """
        return PlayerFactoryV2.list_available_players()


# Populate AVAILABLE_PLAYERS as class attribute for backward compatibility
# This is accessed by existing code as PlayerFactory.AVAILABLE_PLAYERS
PlayerFactory.AVAILABLE_PLAYERS = PlayerFactory.list_available_players()
