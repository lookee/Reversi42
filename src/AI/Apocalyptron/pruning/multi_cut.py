"""
Multi-Cut pruning.

If multiple moves cause beta cutoffs in the first few moves,
the position is very strong and can be cut off early.

Extracted from GrandmasterEngine (lines 476-482).
"""

from AI.Apocalyptron.pruning.interfaces import PruningResult, PruningStrategy


class MultiCutPruning(PruningStrategy):
    """
    Multi-Cut pruning strategy.

    If C consecutive moves (default: 3) cause beta cutoffs within
    the first M moves (default: 10), the position is clearly winning
    and we can return beta immediately.

    Parameters:
    - C = 3 (cutoffs needed)
    - M = 10 (check only first M moves)
    - depth >= 3

    Provides 1.15-1.3x speedup.
    """

    C = 3  # Cutoffs needed
    M = 10  # Check only first M moves
    MIN_DEPTH = 3

    def __init__(self):
        """Initialize multi-cut pruning"""
        self.pruning_count = 0

    def should_multi_cut(self, cutoff_count: int, move_index: int, depth: int) -> bool:
        """
        Check if multi-cut applies.

        Args:
            cutoff_count: Number of cutoffs seen so far
            move_index: Current move index (0-based)
            depth: Current search depth

        Returns:
            bool: True if should multi-cut
        """
        if depth < self.MIN_DEPTH:
            return False

        if cutoff_count >= self.C and move_index < self.M:
            self.pruning_count += 1
            return True

        return False

    def get_statistics(self) -> dict:
        """Get multi-cut statistics"""
        return {
            "pruning_count": self.pruning_count,
        }

    def reset_statistics(self):
        """Reset statistics"""
        self.pruning_count = 0

    def should_prune(self, context) -> PruningResult:
        """Multi-cut requires tracking during search"""
        return PruningResult(False, reason="multi_cut_requires_cutoff_tracking")
