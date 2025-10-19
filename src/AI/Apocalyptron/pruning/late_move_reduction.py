"""
Late Move Reduction (LMR).

Search later moves (after first 3) at reduced depth.
If they look good, re-search at full depth.

Extracted from GrandmasterEngine (lines 419-443).
"""

from AI.Apocalyptron.pruning.interfaces import PruningStrategy, PruningResult


class LateMoveReduction(PruningStrategy):
    """
    Late Move Reduction strategy.
    
    Moves ordered later are less likely to be good.
    Search them at reduced depth first:
    - Moves 4-8: Reduce depth by 1
    - Moves 9+: Reduce depth by 2
    
    If reduced search raises alpha, re-search at full depth.
    
    Requires:
    - Move index >= 3 (first 3 moves at full depth)
    - Depth >= 3
    - Not in desperate position
    
    Provides 1.4-2x speedup.
    """
    
    MIN_DEPTH = 3
    FIRST_FULL_MOVES = 3
    
    def __init__(self):
        """Initialize LMR"""
        self.reductions = 0
        self.re_searches = 0
    
    def should_reduce(self, move_index: int, depth: int, best_value: int) -> int:
        """
        Determine depth reduction for this move.
        
        Args:
            move_index: Index of move in ordered list (0-based)
            depth: Current search depth
            best_value: Best value found so far
            
        Returns:
            int: Depth reduction (0 = no reduction, 1-2 = reduce)
        """
        INFINITY = 999999
        
        # First few moves at full depth
        if move_index < self.FIRST_FULL_MOVES:
            return 0
        
        # Only for deep searches
        if depth < self.MIN_DEPTH:
            return 0
        
        # Not in desperate position
        if best_value <= -INFINITY + 100:
            return 0
        
        # Calculate reduction
        if move_index >= 8:
            reduction = 2  # Moves 9+ are very likely bad
        else:
            reduction = 1  # Moves 4-8 reduce moderately
        
        self.reductions += 1
        return reduction
    
    def record_re_search(self):
        """Record that a re-search was needed"""
        self.re_searches += 1
    
    def get_statistics(self) -> dict:
        """Get LMR statistics"""
        re_search_rate = (self.re_searches / self.reductions * 100) if self.reductions > 0 else 0
        return {
            'reductions': self.reductions,
            're_searches': self.re_searches,
            're_search_rate': re_search_rate,
        }
    
    def reset_statistics(self):
        """Reset statistics"""
        self.reductions = 0
        self.re_searches = 0
    
    def should_prune(self, context) -> PruningResult:
        """Not a pruning strategy, returns False"""
        return PruningResult(False, reason="lmr_is_reduction_not_pruning")

