"""
Random Engine

Pure random move selection.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from AI.base.engine import Engine
from AI.base.engine_metadata import EngineMetadata
from AI.factory.engine_registry import EngineRegistry
import random


@EngineRegistry.register('random', EngineMetadata(
    name='random',
    display_name='Random Chaos',
    description='Pure random move selection - unpredictable',
    complexity='low',
    speed='instant',
    strength='weak',
    features=[]
))
class RandomEngine(Engine):
    """
    Random move selection engine.
    
    Selects moves uniformly at random.
    Useful for:
    - Testing
    - Baseline comparison
    - Fun/chaotic gameplay
    """
    
    def __init__(self, config=None):
        """Initialize random engine."""
        super().__init__("Random", config)
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Select random move from valid moves.
        
        Args:
            game: Game state
            depth: Ignored (random doesn't search)
            **kwargs: Ignored
        
        Returns:
            Move: Random valid move
        """
        moves = game.get_move_list()
        
        if not moves:
            return None
        
        # Pure random selection
        move = random.choice(moves)
        
        self.update_statistics(nodes_evaluated=len(moves))
        
        return move
    
    def evaluate_position(self, game) -> float:
        """
        Random evaluation (not used for move selection).
        
        Returns random score for testing purposes.
        """
        return random.uniform(-1.0, 1.0)

