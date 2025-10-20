"""
Stability evaluation.

Evaluates pieces that cannot be flipped (stable pieces).
Corners are always stable, edges become stable when adjacent to owned corners.
"""

from AI.Apocalyptron.evaluation.interfaces import PositionEvaluator


class StabilityEvaluator(PositionEvaluator):
    """
    Evaluates stability (pieces that cannot be flipped).

    Stable pieces provide a permanent advantage.
    - Corners are always stable
    - Edges adjacent to owned corners become stable
    - More stable pieces = better position

    Extracted from GrandmasterEngine.evaluate_advanced (lines 222-254).
    """

    CORNER_MASK = 0x8100000000000081  # a1, h1, a8, h8

    def __init__(self, weights=None):
        """
        Initialize stability evaluator.

        Args:
            weights: EvaluationWeights instance
        """
        from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights

        self.weights = weights if weights is not None else EvaluationWeights()

    def evaluate(self, game) -> int:
        """
        Evaluate stability differential.

        Args:
            game: BitboardGame instance

        Returns:
            int: Stability score
        """
        player, opponent = game._get_player_boards()

        # Calculate stable pieces for both players
        player_stable = self._calculate_stable_pieces(player, opponent)
        opponent_stable = self._calculate_stable_pieces(opponent, player)

        player_stable_count = self._count_bits(player_stable)
        opponent_stable_count = self._count_bits(opponent_stable)

        return (player_stable_count - opponent_stable_count) * self.weights.stability_weight

    def _calculate_stable_pieces(self, player: int, opponent: int) -> int:
        """
        Calculate stable pieces for a player.

        Returns bitboard of stable pieces.
        """
        stable_pieces = player & self.CORNER_MASK  # Corners always stable

        # Add edges adjacent to owned corners
        for corner_bit in [0, 7, 56, 63]:
            if player & (1 << corner_bit):
                # Player owns corner - adjacent edges are stable
                if corner_bit == 0:  # a1
                    stable_pieces |= player & 0x01010101010101FF  # a-file + rank 1
                elif corner_bit == 7:  # h1
                    stable_pieces |= player & 0x80808080808080FF  # h-file + rank 1
                elif corner_bit == 56:  # a8
                    stable_pieces |= player & 0xFF01010101010101  # a-file + rank 8
                elif corner_bit == 63:  # h8
                    stable_pieces |= player & 0xFF80808080808080  # h-file + rank 8

        return stable_pieces

    def _count_bits(self, bitboard: int) -> int:
        """Count number of set bits"""
        count = 0
        while bitboard:
            count += 1
            bitboard &= bitboard - 1
        return count
