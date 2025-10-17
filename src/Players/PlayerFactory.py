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
from Players.HumanPlayer import HumanPlayer
from Players.AIPlayer import AIPlayer
from Players.Monkey import Monkey
from AI.MinimaxEngine import MinimaxEngine
from AI.RandomEngine import RandomEngine
from AI.HeuristicEngine import HeuristicEngine

class PlayerFactory:
    """
    Factory class for creating different types of players.
    This makes it easy to add new player types and engines.
    """
    
    # Registry of available player types
    PLAYER_TYPES = {
        'Human': HumanPlayer,
        'AI': AIPlayer,
        'Monkey': Monkey,
    }
    
    # Registry of available AI engines
    AI_ENGINES = {
        'Minimax': MinimaxEngine,
        'Random': RandomEngine,
        'Heuristic': HeuristicEngine,
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
    def create_ai_player(cls, engine_type='Minimax', difficulty=6, **kwargs):
        """
        Create an AI player with the specified engine.
        
        Args:
            engine_type (str): Type of AI engine to use
            difficulty (int): Difficulty level (depth for minimax)
            **kwargs: Additional arguments for player creation
            
        Returns:
            AIPlayer: The created AI player instance
            
        Raises:
            ValueError: If engine type is not supported
        """
        if engine_type not in cls.AI_ENGINES:
            raise ValueError(f"Unsupported engine type: {engine_type}")
        
        # Create AI player with custom engine
        player = AIPlayer(difficulty)
        
        # Replace the default engine with the specified one
        engine_class = cls.AI_ENGINES[engine_type]
        player.engine = engine_class()
        player.name = f"{engine_type}AI{difficulty}"
        
        return player
    
    @classmethod
    def get_available_player_types(cls):
        """
        Get list of available player types.
        
        Returns:
            list: List of available player type names
        """
        return list(cls.PLAYER_TYPES.keys())
    
    @classmethod
    def get_available_engines(cls):
        """
        Get list of available AI engines.
        
        Returns:
            list: List of available engine type names
        """
        return list(cls.AI_ENGINES.keys())
    
    @classmethod
    def register_player_type(cls, name, player_class):
        """
        Register a new player type.
        
        Args:
            name (str): Name of the player type
            player_class: Class that implements the player
        """
        cls.PLAYER_TYPES[name] = player_class
    
    @classmethod
    def register_engine(cls, name, engine_class):
        """
        Register a new AI engine.
        
        Args:
            name (str): Name of the engine
            engine_class: Class that implements the engine
        """
        cls.AI_ENGINES[name] = engine_class
