"""
Positional move ordering.

Orders moves based on strategic square values:
1. Corners (best)
2. Edges (good)
3. Center (medium)
4. Others (low)

Extracted from GrandmasterEngine.order_moves (lines 117-129).
"""

from typing import Any, List, Tuple

from AI.Apocalyptron.ordering.interfaces import MoveOrderer


class PositionalOrderer(MoveOrderer):
    """
    Orders moves based on positional value.

    Priority:
    1. Corners - always strongest (cannot be flipped)
    2. Stable edges - next best
    3. Center - medium value
    4. Others - lower priority
    """

    # Bit masks for strategic squares
    CORNER_MASK = 0x8100000000000081  # a1, h1, a8, h8
    STABLE_EDGE_MASK = 0x7E0000000000007E  # Edges without X-squares
    CENTER_MASK = 0x0000001818000000  # d4, e4, d5, e5

    def __init__(self, weights=None):
        """
        Initialize positional orderer.

        Args:
            weights: EvaluationWeights instance
        """
        from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights

        self.weights = weights if weights is not None else EvaluationWeights()

    def score_moves(self, game, moves: List) -> List[Tuple[float, Any]]:
        """
        Score moves based on positional value.

        Args:
            game: BitboardGame instance
            moves: List of Move objects

        Returns:
            List of (score, move) tuples
        """
        scored_moves = []

        for move in moves:
            score = 0

            # Get bit position
            if isinstance(move, str):
                # String format like "F5"
                col = ord(move[0].upper()) - ord("A")
                row = int(move[1]) - 1
                bit = row * 8 + col
            else:
                # Move object
                bit = (move.y - 1) * 8 + (move.x - 1)

            bit_mask = 1 << bit

            # 1. Corner: Maximum priority
            if bit_mask & self.CORNER_MASK:
                score += self.weights.move_order_corner
            # 2. Stable edge: High priority
            elif bit_mask & self.STABLE_EDGE_MASK:
                score += self.weights.move_order_edge
            # 3. Center control: Medium priority
            elif bit_mask & self.CENTER_MASK:
                score += self.weights.move_order_center

            scored_moves.append((score, move))

        return scored_moves
