"""
Futility pruning.

If a position is so bad that even the best possible move can't improve it,
prune the search early.

Extracted from GrandmasterEngine (lines 326-352).
"""

from typing import List, Optional, Tuple

from AI.Apocalyptron.pruning.interfaces import PruningResult, PruningStrategy


class FutilityPruning(PruningStrategy):
    """
    Futility pruning at frontier nodes.

    At shallow depths (1-3), if static evaluation + margin still can't beat alpha,
    the position is futile and can be pruned.

    Margins per depth (conservative for Reversi):
    - Depth 1: 200 points (one move can improve ~200)
    - Depth 2: 350 points (cumulative)
    - Depth 3: 500 points (cumulative)

    Provides 1.15-1.25x speedup at frontier nodes.
    """

    FUTILITY_MARGINS = {
        1: 200,
        2: 350,
        3: 500,
    }

    def __init__(self, evaluator=None):
        """
        Initialize futility pruning.

        Args:
            evaluator: PositionEvaluator for static evaluation
        """
        self.evaluator = evaluator
        self.pruning_count = 0

    def should_prune(self, context) -> PruningResult:
        """
        Check if position is futile.

        Note: This is a simplified check. Actual implementation needs
        static evaluation which requires the evaluator.

        Args:
            context: SearchContext

        Returns:
            PruningResult
        """
        # Futility pruning only at shallow depths
        if context.depth > 3 or context.depth <= 0:
            return PruningResult(False, reason="depth_out_of_range")

        # Need evaluator to check
        if self.evaluator is None:
            return PruningResult(False, reason="no_evaluator")

        # This check requires game state and alpha value
        # Actual implementation in search algorithm
        return PruningResult(False, reason="requires_evaluation")

    def can_prune_futile(
        self, game, depth: int, alpha: int, beta: int, move_list: List
    ) -> Tuple[bool, Optional[int]]:
        """
        Check if position is futile (actual implementation).

        Args:
            game: Current game state
            depth: Remaining depth
            alpha, beta: Alpha-beta window
            move_list: Available moves

        Returns:
            tuple: (should_prune, cutoff_value)
        """
        INFINITY = 999999

        # Check conditions
        if depth > 3 or depth <= 0:
            return (False, None)

        if len(move_list) == 0:  # Forced pass
            return (False, None)

        if alpha >= INFINITY - 1000 or beta <= -INFINITY + 1000:
            return (False, None)

        if self.evaluator is None:
            return (False, None)

        # Get static evaluation
        static_eval = self.evaluator.evaluate(game)

        # Get margin for this depth
        margin = self.FUTILITY_MARGINS.get(depth, 0)

        # If even best case can't beat alpha, prune
        if static_eval + margin <= alpha:
            self.pruning_count += 1
            return (True, alpha)

        return (False, None)

    def get_statistics(self) -> dict:
        """Get futility pruning statistics"""
        return {
            "pruning_count": self.pruning_count,
        }

    def reset_statistics(self):
        """Reset statistics"""
        self.pruning_count = 0
