"""
Bitboard Engine

Ultra-fast bitboard-based minimax.
Migrated from AI/BitboardMinimaxEngine.py.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engines.base.engine import Engine
from engines.base.engine_metadata import EngineMetadata
from engines.factory.engine_registry import EngineRegistry


@EngineRegistry.register('bitboard', EngineMetadata(
    name='bitboard',
    display_name='Bitboard Blitz',
    description='Ultra-fast bitboard implementation - 10x faster than standard',
    complexity='high',
    speed='fast',
    strength='strong',
    features=['bitboard', 'alpha_beta', 'move_ordering']
))
class BitboardEngine(Engine):
    """
    High-performance bitboard engine.
    
    Features:
    - Bitboard representation (64-bit integers)
    - Optimized move generation
    - Fast position evaluation
    - 5-10x faster than standard minimax
    
    Wrapper around AI/BitboardMinimaxEngine.py.
    """
    
    def __init__(self, config=None):
        """
        Initialize bitboard engine.
        
        Args:
            config: Optional configuration
        """
        super().__init__("Bitboard", config)
        
        # Get evaluator
        if config and 'evaluator' in config:
            self.evaluator = config['evaluator']
        else:
            from AI.StandardEvaluator import StandardEvaluator
            self.evaluator = StandardEvaluator()
        
        # Use legacy bitboard engine
        from AI.BitboardMinimaxEngine import BitboardMinimaxEngine
        self._legacy_engine = BitboardMinimaxEngine()
        self._legacy_engine.evaluator = self.evaluator
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Find best move using bitboard search.
        
        Args:
            game: Game state
            depth: Search depth
            **kwargs: Additional parameters
        
        Returns:
            Move: Best move
        """
        move = self._legacy_engine.get_best_move(game, depth, **kwargs)
        
        # Update statistics
        self.update_statistics(
            nodes_evaluated=self._legacy_engine.nodes,
            pruning_count=self._legacy_engine.pruning
        )
        
        return move
    
    def evaluate_position(self, game) -> float:
        """Evaluate position."""
        return self.evaluator.evaluate(game)

