"""
Grandmaster Engine

Ultimate AI - combines best techniques.
Migrated from AI/GrandmasterEngine.py.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from AI.base.engine import Engine
from AI.base.engine_metadata import EngineMetadata
from AI.factory.engine_registry import EngineRegistry


@EngineRegistry.register('grandmaster', EngineMetadata(
    name='grandmaster',
    display_name='Grandmaster',
    description='Ultimate AI challenge - combines all best techniques',
    complexity='very_high',
    speed='slow',
    strength='master',
    features=['bitboard', 'advanced_eval', 'endgame', 'move_ordering', 'killer_moves']
))
class GrandmasterEngine(Engine):
    """
    Grandmaster-level engine.
    
    Combines:
    - Bitboard representation
    - Advanced evaluation
    - Deep search
    - Sophisticated move ordering
    - Endgame optimization
    
    Wrapper around AI/GrandmasterEngine.py.
    """
    
    def __init__(self, config=None):
        """Initialize grandmaster engine."""
        super().__init__("Grandmaster", config)
        
        # Get evaluator
        if config and 'evaluator' in config:
            self.evaluator = config['evaluator']
        else:
            from AI.AdvancedEvaluator import AdvancedEvaluator
            self.evaluator = AdvancedEvaluator()
        
        # Use legacy grandmaster engine
        from AI.GrandmasterEngine import GrandmasterEngine as LegacyGrandmasterEngine
        self._legacy_engine = LegacyGrandmasterEngine()
        self._legacy_engine.evaluator = self.evaluator
    
    def get_best_move(self, game, depth: int, **kwargs):
        """Find best move using grandmaster techniques."""
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
        if hasattr(self._legacy_engine, 'nodes'):
            self.update_statistics(
                nodes_evaluated=self._legacy_engine.nodes,
                pruning_count=getattr(self._legacy_engine, 'pruning', 0)
            )
        
        return move
    
    def evaluate_position(self, game) -> float:
        """Evaluate position using advanced evaluator."""
        return self.evaluator.evaluate(game)

