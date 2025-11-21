"""
Transposition table for position caching.

Stores previously evaluated positions to avoid redundant searches.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TTEntry:
    """
    Transposition table entry.

    Stores evaluation result for a position.
    """

    depth: int  # Depth at which position was evaluated
    value: int  # Evaluation score
    flag: str  # 'exact', 'lower' (beta cutoff), 'upper' (alpha cutoff)
    best_move: Optional[Any] = None  # Best move found (optional)

    def is_usable(self, search_depth: int) -> bool:
        """Check if this entry can be used for current search depth"""
        return self.depth >= search_depth


class TranspositionTable:
    """
    Transposition table using dictionary storage.

    Caches position evaluations to speed up search by avoiding
    re-evaluation of previously seen positions.

    Usage:
        tt = TranspositionTable()

        # Store entry
        tt.store(zobrist_hash, depth=5, value=120, flag='exact')

        # Lookup entry
        entry = tt.lookup(zobrist_hash)
        if entry and entry.is_usable(current_depth):
            # Use cached value
    """

    def __init__(self, max_size: int = 1000000):
        """
        Initialize transposition table.

        Args:
            max_size: Maximum number of entries (default: 1M)
        """
        self.table: dict[int, TTEntry] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self.stores = 0

    def store(self, zobrist_hash: int, depth: int, value: int, flag: str, best_move: Optional[Any] = None):
        """
        Store position evaluation.

        Args:
            zobrist_hash: Position hash
            depth: Search depth
            value: Evaluation score
            flag: 'exact', 'lower', or 'upper'
            best_move: Best move found (optional)
        """
        # Replace if we have deeper evaluation or table is not full
        if zobrist_hash in self.table:
            existing = self.table[zobrist_hash]
            if depth < existing.depth:
                return  # Don't replace with shallower search

        # Simple replacement scheme: always store if not full
        if len(self.table) < self.max_size or zobrist_hash in self.table:
            self.table[zobrist_hash] = TTEntry(depth, value, flag, best_move)
            self.stores += 1
        # If full, could implement replacement scheme (age, depth, etc.)
        # For now, just skip if full and not already present

    def lookup(self, zobrist_hash: int) -> Optional[TTEntry]:
        """
        Lookup position in table.

        Args:
            zobrist_hash: Position hash

        Returns:
            TTEntry if found, None otherwise
        """
        entry = self.table.get(zobrist_hash)

        if entry:
            self.hits += 1
            return entry
        else:
            self.misses += 1
            return None

    def clear(self):
        """Clear all entries"""
        self.table.clear()
        self.hits = 0
        self.misses = 0
        self.stores = 0

    def size(self) -> int:
        """Get current number of entries"""
        return len(self.table)

    def get_statistics(self) -> dict:
        """Get table statistics"""
        total_queries = self.hits + self.misses
        hit_rate = (self.hits / total_queries * 100) if total_queries > 0 else 0

        return {
            "size": len(self.table),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "stores": self.stores,
        }
