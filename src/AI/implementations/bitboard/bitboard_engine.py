"""
Bitboard Engine

Ultra-fast bitboard-based minimax.
Migrated from AI/BitboardMinimaxEngine.py.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from AI.base.engine import Engine
from AI.base.engine_metadata import EngineMetadata
from AI.factory.engine_registry import EngineRegistry


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
        # Convert to BitboardGame if necessary
        from Reversi.BitboardGame import BitboardGame
        
        if not isinstance(game, BitboardGame):
            # Convert traditional Game to BitboardGame
            bitboard_game = BitboardGame()
            bitboard_game.import_game_state(game)
            game_to_use = bitboard_game
        else:
            game_to_use = game
        
        move = self._legacy_engine.get_best_move(game_to_use, depth, **kwargs)
        
        # Update statistics
        self.update_statistics(
            nodes_evaluated=self._legacy_engine.nodes,
            pruning_count=self._legacy_engine.pruning
        )
        
        return move
    
    def evaluate_position(self, game) -> float:
        """Evaluate position."""
        return self.evaluator.evaluate(game)

