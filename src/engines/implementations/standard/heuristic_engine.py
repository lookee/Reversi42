"""
Heuristic Engine

Position-based heuristic evaluation.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engines.base.engine import Engine
from engines.base.engine_metadata import EngineMetadata
from engines.factory.engine_registry import EngineRegistry


@EngineRegistry.register('heuristic', EngineMetadata(
    name='heuristic',
    display_name='Heuristic Hero',
    description='Position-based evaluation - favors corners and edges',
    complexity='low',
    speed='fast',
    strength='medium',
    features=['positional_weights']
))
class HeuristicEngine(Engine):
    """
    Heuristic evaluation engine.
    
    Uses position weights:
    - Corners are valuable
    - Edges are good
    - Center is neutral
    - Near corners are dangerous
    
    Wrapper around AI/HeuristicEngine.py.
    """
    
    def __init__(self, config=None):
        """Initialize heuristic engine."""
        super().__init__("Heuristic", config)
        
        # Use legacy heuristic engine
        from AI.HeuristicEngine import HeuristicEngine as LegacyHeuristicEngine
        self._legacy_engine = LegacyHeuristicEngine()
    
    def get_best_move(self, game, depth: int, **kwargs):
        """Find best move using heuristic evaluation."""
        move = self._legacy_engine.get_best_move(game, depth, **kwargs)
        
        # Update statistics
        if hasattr(self._legacy_engine, 'nodes'):
            self.update_statistics(nodes_evaluated=self._legacy_engine.nodes)
        
        return move
    
    def evaluate_position(self, game) -> float:
        """Evaluate position using positional heuristics."""
        if hasattr(self._legacy_engine, 'evaluator'):
            return self._legacy_engine.evaluator.evaluate(game)
        return 0.0

