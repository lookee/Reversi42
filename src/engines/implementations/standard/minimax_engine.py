"""
Minimax Engine

Classic minimax with alpha-beta pruning.
Migrated from AI/MinimaxEngine.py with new architecture.

Version: 3.2.0
Architecture: Strategy Pattern + Registry
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engines.base.engine import Engine
from engines.base.engine_metadata import EngineMetadata
from engines.factory.engine_registry import EngineRegistry
from Reversi.Game import Game, Move


@EngineRegistry.register('minimax', EngineMetadata(
    name='minimax',
    display_name='Classic Minimax',
    description='Traditional alpha-beta pruning search - solid and reliable',
    complexity='medium',
    speed='medium',
    strength='medium',
    features=['alpha_beta', 'move_ordering']
))
class MinimaxEngine(Engine):
    """
    Classic Minimax with Alpha-Beta pruning.
    
    Algorithm:
    - Minimax tree search
    - Alpha-Beta pruning for efficiency
    - Move ordering for better pruning
    
    Wrapper around existing AI/MinimaxEngine.py for compatibility.
    """
    
    def __init__(self, config=None):
        """
        Initialize minimax engine.
        
        Args:
            config: Optional configuration dict
                - evaluator: Custom evaluator instance
        """
        super().__init__("Minimax", config)
        
        # Get or create evaluator
        if config and 'evaluator' in config:
            self.evaluator = config['evaluator']
        else:
            # Use default evaluator
            from AI.StandardEvaluator import StandardEvaluator
            self.evaluator = StandardEvaluator()
        
        # Use legacy MinimaxEngine for actual computation
        from AI.MinimaxEngine import MinimaxEngine as LegacyMinimaxEngine
        self._legacy_engine = LegacyMinimaxEngine()
        self._legacy_engine.evaluator = self.evaluator
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Find best move using minimax with alpha-beta.
        
        Args:
            game: Game state
            depth: Search depth
            **kwargs: Additional parameters (player_name, etc.)
        
        Returns:
            Move: Best move
        """
        # Delegate to legacy engine for now
        move = self._legacy_engine.get_best_move(game, depth, **kwargs)
        
        # Update statistics
        self.update_statistics(
            nodes_evaluated=self._legacy_engine.nodes,
            pruning_count=self._legacy_engine.pruning
        )
        
        return move
    
    def evaluate_position(self, game) -> float:
        """
        Evaluate position using configured evaluator.
        
        Args:
            game: Game state
        
        Returns:
            float: Position score
        """
        return self.evaluator.evaluate(game)

