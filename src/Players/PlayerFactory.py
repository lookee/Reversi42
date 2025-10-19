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

from Players.Player import Player
from Players.PlayerHuman import PlayerHuman
from Players.PlayerApocalyptron import PlayerApocalyptron

class PlayerFactory:
    """
    Factory class for creating players.
    Now featuring Apocalyptron - the ultimate Reversi AI.
    
    Player types are automatically discovered from their metadata.
    """
    
    # Registry of all player classes
    # Apocalyptron is the ultimate AI
    ALL_PLAYER_CLASSES = [
        PlayerHuman,                     # Human player (disabled in menu, but available for API)
        PlayerApocalyptron,              # ⚡ Apocalyptron - The ultimate AI (enabled in menu)
    ]
    
    # Build registry from metadata
    PLAYER_TYPES = {
        cls.PLAYER_METADATA['display_name']: cls
        for cls in ALL_PLAYER_CLASSES
    }
    
    @classmethod
    def create_player(cls, player_type, **kwargs):
        """
        Create a player of the specified type.
        
        Args:
            player_type (str): Type of player to create
            **kwargs: Additional arguments for player creation
            
        Returns:
            Player: The created player instance
            
        Raises:
            ValueError: If player type is not supported
        """
        if player_type not in cls.PLAYER_TYPES:
            raise ValueError(f"Unsupported player type: {player_type}")
        
        player_class = cls.PLAYER_TYPES[player_type]
        return player_class(**kwargs)
    
    @classmethod
    def create_apocalyptron(cls, depth=9, weights=None, **kwargs):
        """
        Create an Apocalyptron AI player (recommended).
        
        Args:
            depth (int): Search depth (7-12 recommended, default 9)
            weights: GrandmasterWeights instance for custom evaluation (None = default)
            **kwargs: Additional arguments for player creation
            
        Returns:
            PlayerApocalyptron: The created Apocalyptron AI instance
        """
        return PlayerApocalyptron(depth=depth, weights=weights, **kwargs)
    
    @classmethod
    def create_grandmaster(cls, difficulty=9, weights=None, **kwargs):
        """
        Create a Grandmaster AI player (legacy alias for create_apocalyptron).
        
        Note: This method is kept for backwards compatibility.
        Grandmaster AI has been replaced by Apocalyptron.
        
        Args:
            difficulty (int): Search depth (7-12 recommended, default 9)
            weights: GrandmasterWeights instance for custom evaluation (None = default)
            **kwargs: Additional arguments for player creation
            
        Returns:
            PlayerApocalyptron: The created Apocalyptron AI instance
        """
        return PlayerApocalyptron(depth=difficulty, weights=weights, **kwargs)
    
    @classmethod
    def get_available_player_types(cls):
        """
        Get list of available (enabled) player types.
        
        Returns:
            list: List of available player type names
        """
        return [
            player_class.PLAYER_METADATA['display_name']
            for player_class in cls.ALL_PLAYER_CLASSES
            if player_class.PLAYER_METADATA['enabled']
        ]
    
    @classmethod
    def get_all_player_types(cls):
        """
        Get list of all player types (including disabled).
        
        Returns:
            list: List of all player type names
        """
        return list(cls.PLAYER_TYPES.keys())
    
    @classmethod
    def get_player_metadata(cls, player_type):
        """
        Get metadata for a specific player type.
        
        Args:
            player_type: Name of the player type
            
        Returns:
            dict: Player metadata
        """
        if player_type in cls.PLAYER_TYPES:
            return cls.PLAYER_TYPES[player_type].PLAYER_METADATA
        return None
    
    @classmethod
    def get_all_player_metadata(cls):
        """
        Get metadata for all player types.
        
        Returns:
            dict: Dictionary mapping player type names to their metadata
        """
        return {
            player_class.PLAYER_METADATA['display_name']: player_class.PLAYER_METADATA
            for player_class in cls.ALL_PLAYER_CLASSES
        }
    
    @classmethod
    def register_player_type(cls, name, player_class):
        """
        Register a new player type.
        
        Args:
            name (str): Name of the player type
            player_class: Class that implements the player
        """
        cls.PLAYER_TYPES[name] = player_class
