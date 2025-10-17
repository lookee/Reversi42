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
from Players.AIPlayerBook import AIPlayerBook
from Players.AIPlayerBitboard import AIPlayerBitboard
from Players.AIPlayerBitboardBook import AIPlayerBitboardBook
from Players.Monkey import Monkey
from Players.GreedyPlayer import GreedyPlayer
from Players.HeuristicPlayer import HeuristicPlayer
from Players.NetworkPlayer import NetworkPlayer
from AI.MinimaxEngine import MinimaxEngine
from AI.RandomEngine import RandomEngine
from AI.HeuristicEngine import HeuristicEngine
from AI.StandardEvaluator import StandardEvaluator
from AI.SimpleEvaluator import SimpleEvaluator
from AI.AdvancedEvaluator import AdvancedEvaluator
from AI.GreedyEvaluator import GreedyEvaluator

class PlayerFactory:
    """
    Factory class for creating different types of players.
    This makes it easy to add new player types and engines.
    
    Player types are automatically discovered from their metadata.
    """
    
    # Registry of all player classes (including disabled ones)
    ALL_PLAYER_CLASSES = [
        HumanPlayer,
        AIPlayer,
        AIPlayerBook,
        AIPlayerBitboard,
        AIPlayerBitboardBook,
        HeuristicPlayer,
        GreedyPlayer,
        Monkey,
        NetworkPlayer,  # Disabled by default
    ]
    
    # Build registry from metadata
    PLAYER_TYPES = {
        cls.PLAYER_METADATA['display_name']: cls
        for cls in ALL_PLAYER_CLASSES
    }
    
    # Registry of available AI engines
    AI_ENGINES = {
        'Minimax': MinimaxEngine,
        'Random': RandomEngine,
        'Heuristic': HeuristicEngine,
    }
    
    # Registry of available evaluators
    EVALUATORS = {
        'Standard': StandardEvaluator,
        'Simple': SimpleEvaluator,
        'Advanced': AdvancedEvaluator,
        'Greedy': GreedyEvaluator,
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
    def create_ai_player(cls, engine_type='Minimax', difficulty=6, evaluator_type='Standard', **kwargs):
        """
        Create an AI player with the specified engine and evaluator.
        
        Args:
            engine_type (str): Type of AI engine to use
            difficulty (int): Difficulty level (depth for minimax)
            evaluator_type (str): Type of evaluator to use
            **kwargs: Additional arguments for player creation
            
        Returns:
            AIPlayer: The created AI player instance
            
        Raises:
            ValueError: If engine type or evaluator type is not supported
        """
        if engine_type not in cls.AI_ENGINES:
            raise ValueError(f"Unsupported engine type: {engine_type}")
        
        if evaluator_type not in cls.EVALUATORS:
            raise ValueError(f"Unsupported evaluator type: {evaluator_type}")
        
        # Create evaluator instance
        evaluator_class = cls.EVALUATORS[evaluator_type]
        evaluator = evaluator_class()
        
        # Create AI player with custom engine
        player = AIPlayer(difficulty)
        
        # Replace the default engine with the specified one
        engine_class = cls.AI_ENGINES[engine_type]
        player.engine = engine_class(evaluator=evaluator)
        player.name = f"{engine_type}AI{difficulty}"
        
        return player
    
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
    
    @classmethod
    def get_available_evaluators(cls):
        """
        Get list of available evaluators.
        
        Returns:
            list: List of available evaluator type names
        """
        return list(cls.EVALUATORS.keys())
    
    @classmethod
    def register_evaluator(cls, name, evaluator_class):
        """
        Register a new evaluator.
        
        Args:
            name (str): Name of the evaluator
            evaluator_class: Class that implements the evaluator
        """
        cls.EVALUATORS[name] = evaluator_class
