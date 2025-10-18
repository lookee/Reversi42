"""
Endgame Solver Decorator

Decorator Pattern: Adds perfect endgame solving.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from engines.base.engine import Engine


class EndgameSolverDecorator(Engine):
    """
    Decorator Pattern: Wraps engine with perfect endgame solver.
    
    When few empty squares remain, solves game perfectly.
    
    Example:
        base_engine = MinimaxEngine()
        engine = EndgameSolverDecorator(base_engine, trigger=12)
    """
    
    def __init__(self, wrapped_engine: Engine, trigger: int = 12):
        """
        Wrap engine with endgame solver.
        
        Args:
            wrapped_engine: Base engine
            trigger: Empty squares threshold for perfect solve
        """
        super().__init__(name=f"{wrapped_engine.name}+Endgame")
        self.engine = wrapped_engine
        self.trigger = trigger
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Get best move: Perfect solve if near endgame.
        
        Args:
            game: Game state
            depth: Search depth
            **kwargs: Additional parameters
        
        Returns:
            Move: Best move
        """
        # Count empty squares
        empty_count = self._count_empty(game)
        
        # If endgame threshold reached, solve perfectly
        if empty_count <= self.trigger:
            return self._solve_endgame(game)
        
        # Otherwise use wrapped engine
        return self.engine.get_best_move(game, depth, **kwargs)
    
    def evaluate_position(self, game) -> float:
        """Delegate to wrapped engine."""
        return self.engine.evaluate_position(game)
    
    def _count_empty(self, game) -> int:
        """Count empty squares on board."""
        try:
            board_str = game.export_str()
            return board_str.count('.')
        except:
            return 64  # Fallback
    
    def _solve_endgame(self, game):
        """
        Perfect endgame solver (simple exhaustive search).
        
        For production, this should use optimized algorithms like:
        - NegaScout with deep endgame optimizations
        - Bitboard operations
        - Move ordering heuristics
        """
        # For now, delegate to engine with maximum depth
        return self.engine.get_best_move(game, depth=20)

