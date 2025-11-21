"""
Principal Variation move ordering.

The best move from the previous iteration (in iterative deepening)
is tried first in the next iteration.
"""

from typing import Any, List, Tuple

from AI.Apocalyptron.ordering.interfaces import MoveOrderer


class PVMoveOrderer(MoveOrderer):
    """
    Orders the PV (Principal Variation) move first.

    In iterative deepening, the best move from depth N-1
    is very likely to be the best move at depth N as well.

    By trying it first, we get a good alpha-beta window early,
    leading to more cutoffs.

    Extracted from GrandmasterEngine (pv_move usage).
    """

    PV_MOVE_SCORE = 10000  # Highest priority

    def __init__(self):
        """Initialize PV move storage"""
        self.pv_move = None

    def set_pv_move(self, move):
        """
        Set the principal variation move.

        Args:
            move: Best move from previous iteration
        """
        self.pv_move = move

    def score_moves(self, game, moves: List) -> List[Tuple[float, Any]]:
        """
        Score moves - PV move gets highest score.

        Args:
            game: BitboardGame instance
            moves: List of Move objects

        Returns:
            List of (score, move) tuples
        """
        scored_moves: List[Tuple[float, Any]] = []

        for move in moves:
            score: float = 0.0

            # PV move gets maximum priority
            if self.pv_move and move == self.pv_move:
                score = float(self.PV_MOVE_SCORE)

            scored_moves.append((score, move))

        return scored_moves

    def clear(self):
        """Clear PV move (for new search)"""
        self.pv_move = None
