"""
Search result - return value from search.

Contains the best move found and detailed search statistics.
"""

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class SearchResult:
    """
    Result of a search operation.
    
    Contains:
    - Best move found
    - Evaluation score
    - Search statistics
    - Performance metrics
    """
    
    # Primary results
    best_move: Optional[Any] = None  # Move object or None
    value: int = 0
    
    # Search statistics
    nodes_searched: int = 0
    nodes_pruned: int = 0
    time_elapsed: float = 0.0
    
    # Depth information
    depth_reached: int = 0
    selective_depth: int = 0  # Maximum depth reached with extensions
    
    # Optimization statistics
    null_move_cutoffs: int = 0
    null_move_attempts: int = 0
    futility_pruning: int = 0
    lmr_reductions: int = 0
    lmr_re_searches: int = 0
    multi_cut_pruning: int = 0
    
    # Table statistics
    tt_hits: int = 0
    tt_size: int = 0
    history_entries: int = 0
    
    # Aspiration window statistics
    aspiration_hits: int = 0
    aspiration_fails: int = 0
    
    # Additional data
    metadata: dict = field(default_factory=dict)
    
    def get_pruning_rate(self) -> float:
        """Calculate pruning efficiency percentage"""
        total = self.nodes_searched + self.nodes_pruned
        if total == 0:
            return 0.0
        return (self.nodes_pruned / total) * 100
    
    def get_nodes_per_second(self) -> float:
        """Calculate search speed (nodes/second)"""
        if self.time_elapsed == 0:
            return 0.0
        return self.nodes_searched / self.time_elapsed
    
    def get_null_move_success_rate(self) -> float:
        """Calculate null move pruning success rate"""
        if self.null_move_attempts == 0:
            return 0.0
        return (self.null_move_cutoffs / self.null_move_attempts) * 100
    
    def get_aspiration_success_rate(self) -> float:
        """Calculate aspiration window success rate"""
        total = self.aspiration_hits + self.aspiration_fails
        if total == 0:
            return 0.0
        return (self.aspiration_hits / total) * 100
    
    def to_dict(self) -> dict:
        """Export result as dictionary"""
        return {
            'best_move': str(self.best_move) if self.best_move else None,
            'value': self.value,
            'nodes_searched': self.nodes_searched,
            'nodes_pruned': self.nodes_pruned,
            'pruning_rate': self.get_pruning_rate(),
            'time_elapsed': self.time_elapsed,
            'nodes_per_second': self.get_nodes_per_second(),
            'depth_reached': self.depth_reached,
            'statistics': {
                'null_move': {
                    'attempts': self.null_move_attempts,
                    'cutoffs': self.null_move_cutoffs,
                    'success_rate': self.get_null_move_success_rate(),
                },
                'futility_pruning': self.futility_pruning,
                'lmr': {
                    'reductions': self.lmr_reductions,
                    're_searches': self.lmr_re_searches,
                },
                'multi_cut': self.multi_cut_pruning,
                'aspiration': {
                    'hits': self.aspiration_hits,
                    'fails': self.aspiration_fails,
                    'success_rate': self.get_aspiration_success_rate(),
                },
                'transposition_table': {
                    'hits': self.tt_hits,
                    'size': self.tt_size,
                },
                'history_entries': self.history_entries,
            },
            'metadata': self.metadata,
        }

