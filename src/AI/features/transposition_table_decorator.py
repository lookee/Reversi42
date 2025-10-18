"""
Transposition Table Decorator

Decorator Pattern: Adds position caching (memoization).

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from AI.base.engine import Engine
from typing import Optional, Dict, Tuple


class TranspositionTableDecorator(Engine):
    """
    Decorator Pattern: Wraps any engine with transposition table.
    
    Caches evaluated positions to avoid redundant computation.
    Massive performance boost for deep searches.
    
    Example:
        base_engine = MinimaxEngine()
        engine = TranspositionTableDecorator(base_engine, size_mb=128)
    """
    
    def __init__(self, wrapped_engine: Engine, size_mb: int = 64):
        """
        Wrap engine with transposition table.
        
        Args:
            wrapped_engine: Base engine to wrap
            size_mb: Cache size in megabytes
        """
        super().__init__(name=f"{wrapped_engine.name}+TTable")
        self.engine = wrapped_engine
        self.size_mb = size_mb
        
        # Transposition table: position_hash -> (depth, score, best_move)
        self.table: Dict[str, Tuple[int, float, Any]] = {}
        self.max_entries = (size_mb * 1024 * 1024) // 128  # Estimate
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Get best move: Check cache first.
        
        Args:
            game: Game state
            depth: Search depth
            **kwargs: Additional parameters
        
        Returns:
            Move: Best move
        """
        # Generate position hash
        position_hash = self._hash_position(game)
        
        # Check transposition table
        if position_hash in self.table:
            cached_depth, cached_score, cached_move = self.table[position_hash]
            
            # Use cached result if depth is sufficient
            if cached_depth >= depth:
                self.update_statistics(cache_hits=1)
                return cached_move
        
        self.update_statistics(cache_misses=1)
        
        # Cache miss - compute move
        best_move = self.engine.get_best_move(game, depth, **kwargs)
        best_score = self.engine.evaluate_position(game)
        
        # Store in cache
        self._store(position_hash, depth, best_score, best_move)
        
        return best_move
    
    def evaluate_position(self, game) -> float:
        """Evaluate position (may use cache)."""
        position_hash = self._hash_position(game)
        
        if position_hash in self.table:
            _, cached_score, _ = self.table[position_hash]
            return cached_score
        
        return self.engine.evaluate_position(game)
    
    def _hash_position(self, game) -> str:
        """
        Generate hash for game position.
        
        Args:
            game: Game state
        
        Returns:
            str: Position hash
        """
        try:
            # Try Zobrist hash if available (BitboardGame)
            if hasattr(game, 'get_zobrist_hash'):
                return str(game.get_zobrist_hash())
            
            # Fallback to string export
            return game.export_str() + game.get_turn()
        except:
            # Last resort: string representation
            return str(game)
    
    def _store(self, position_hash: str, depth: int, score: float, move):
        """Store position in transposition table."""
        # Evict old entries if table is full
        if len(self.table) >= self.max_entries:
            # Simple FIFO eviction (could use LRU for better performance)
            oldest_key = next(iter(self.table))
            del self.table[oldest_key]
        
        self.table[position_hash] = (depth, score, move)
    
    def clear_cache(self):
        """Clear transposition table."""
        self.table.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        stats = self.get_statistics()
        return {
            'entries': len(self.table),
            'max_entries': self.max_entries,
            'hits': stats.get('cache_hits', 0),
            'misses': stats.get('cache_misses', 0),
            'hit_rate': stats.get('cache_hits', 0) / max(1, stats.get('cache_hits', 0) + stats.get('cache_misses', 0))
        }

