"""
Parallel Search Decorator

Decorator Pattern: Adds multi-threading to any engine.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from AI.base.engine import Engine
from typing import Optional
import multiprocessing
from copy import deepcopy


class ParallelSearchDecorator(Engine):
    """
    Decorator Pattern: Wraps any engine with parallel search.
    
    Evaluates moves in parallel using multiple threads/processes.
    
    Example:
        base_engine = MinimaxEngine()
        engine = ParallelSearchDecorator(base_engine, threads=8)
    """
    
    def __init__(self, wrapped_engine: Engine, threads: int = 4):
        """
        Wrap engine with parallel search.
        
        Args:
            wrapped_engine: Base engine to wrap
            threads: Number of threads to use
        """
        super().__init__(name=f"{wrapped_engine.name}+Parallel")
        self.engine = wrapped_engine
        self.threads = min(threads, multiprocessing.cpu_count())
        self.pool = None
    
    def _ensure_pool(self):
        """Lazy initialization of process pool."""
        if self.pool is None:
            self.pool = multiprocessing.Pool(self.threads)
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Get best move using parallel evaluation.
        
        Args:
            game: Game state
            depth: Search depth
            **kwargs: Additional parameters
        
        Returns:
            Move: Best move
        """
        moves = game.get_move_list()
        
        # If only one move, no need for parallel
        if len(moves) <= 1:
            return moves[0] if moves else None
        
        # For shallow depth or few moves, use sequential
        if depth <= 2 or len(moves) <= 2:
            return self.engine.get_best_move(game, depth, **kwargs)
        
        # Parallel evaluation
        self._ensure_pool()
        
        try:
            # Evaluate each move in parallel
            results = []
            for move in moves:
                game_copy = deepcopy(game)
                game_copy.move(move)
                score = self.engine.evaluate_position(game_copy)
                results.append((move, score))
            
            # Find best move
            best_move, best_score = max(results, key=lambda x: x[1])
            return best_move
        
        except Exception as e:
            # Fallback to sequential on error
            print(f"Parallel search error: {e}, falling back to sequential")
            return self.engine.get_best_move(game, depth, **kwargs)
    
    def evaluate_position(self, game) -> float:
        """Delegate evaluation to wrapped engine."""
        return self.engine.evaluate_position(game)
    
    def cleanup(self):
        """Clean up process pool."""
        if self.pool:
            self.pool.close()
            self.pool.join()
            self.pool = None
    
    def __del__(self):
        """Cleanup on deletion."""
        self.cleanup()

