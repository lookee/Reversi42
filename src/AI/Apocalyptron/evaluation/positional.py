"""
Positional evaluation.

Evaluates strategic square values: corners, edges, x-squares.
Corners are always valuable, x-squares are dangerous, edges provide stability.
"""

from AI.Apocalyptron.evaluation.interfaces import PositionEvaluator


class PositionalEvaluator(PositionEvaluator):
    """
    Evaluates position based on strategic square control.

    Evaluates:
    - Corner control (always critical - cannot be flipped)
    - X-squares penalty (adjacent to empty corners - very dangerous)
    - Edge control (builds towards corners, harder to flip)
    - Frontier discs (pieces with empty neighbors - vulnerable in midgame)

    Extracted from GrandmasterEngine.evaluate_advanced (lines 194-280).
    """

    # Bit masks for strategic squares
    CORNER_MASK = 0x8100000000000081  # a1, h1, a8, h8
    EDGE_MASK = 0xFF818181818181FF  # All edge squares
    CENTER_MASK = 0x0000001818000000  # d4, e4, d5, e5

    # X-square mappings: (corner_bit, x_square_bit)
    X_SQUARE_PENALTIES = [
        (0, 9),  # a1 corner -> b2 x-square
        (7, 14),  # h1 corner -> g2 x-square
        (56, 49),  # a8 corner -> b7 x-square
        (63, 54),  # h8 corner -> g7 x-square
    ]

    def __init__(self, weights=None):
        """
        Initialize positional evaluator.

        Args:
            weights: EvaluationWeights instance
        """
        from AI.Apocalyptron.evaluation.phase_detector import GamePhaseDetector
        from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights

        self.weights = weights if weights is not None else EvaluationWeights()
        self.phase_detector = GamePhaseDetector()

    def evaluate(self, game) -> int:
        """
        Evaluate positional factors.

        Args:
            game: BitboardGame instance

        Returns:
            int: Positional score
        """
        player, opponent = game._get_player_boards()
        score = 0

        # 1. CORNER CONTROL (always critical)
        score += self._evaluate_corners(player, opponent)

        # 2. X-SQUARES PENALTY (adjacent to empty corners)
        score += self._evaluate_x_squares(player, opponent)

        # 3. EDGE CONTROL
        score += self._evaluate_edges(player, opponent)

        # 4. FRONTIER DISCS (only in midgame)
        phase = self.phase_detector.detect_phase(game)
        from AI.Apocalyptron.evaluation.interfaces import GamePhase

        if phase == GamePhase.MIDGAME:
            score += self._evaluate_frontier(player, opponent, game)

        return score

    def _evaluate_corners(self, player: int, opponent: int) -> int:
        """Evaluate corner control"""
        player_corners = self._count_bits(player & self.CORNER_MASK)
        opponent_corners = self._count_bits(opponent & self.CORNER_MASK)
        return (player_corners - opponent_corners) * self.weights.corner_weight

    def _evaluate_x_squares(self, player: int, opponent: int) -> int:
        """
        Evaluate X-square penalty.

        X-squares are diagonal to corners and are dangerous if corner is empty.
        """
        score = 0

        for corner_bit, x_bit in self.X_SQUARE_PENALTIES:
            corner_mask_single = 1 << corner_bit
            x_mask_single = 1 << x_bit

            # Check if corner is empty
            corner_occupied = (player | opponent) & corner_mask_single

            if not corner_occupied:
                # Corner empty - X-square is BAD
                if player & x_mask_single:
                    score -= self.weights.x_square_penalty  # Heavy penalty
                if opponent & x_mask_single:
                    score += self.weights.x_square_penalty  # Good for us

        return score

    def _evaluate_edges(self, player: int, opponent: int) -> int:
        """Evaluate edge control"""
        player_edges = self._count_bits(player & self.EDGE_MASK)
        opponent_edges = self._count_bits(opponent & self.EDGE_MASK)
        return (player_edges - opponent_edges) * self.weights.edge_weight

    def _evaluate_frontier(self, player: int, opponent: int, game) -> int:
        """
        Evaluate frontier discs (pieces with empty neighbors).

        Fewer frontier discs = more stable position in midgame.
        """
        empty = ~(player | opponent) & 0xFFFFFFFFFFFFFFFF

        # Frontier: pieces adjacent to empty squares
        player_frontier = 0
        opponent_frontier = 0

        # Check all 8 directions for empty neighbors
        for shift in [1, 7, 8, 9]:  # Right, up-left, up, up-right
            player_frontier |= ((player << shift) | (player >> shift)) & empty
            opponent_frontier |= ((opponent << shift) | (opponent >> shift)) & empty

        player_frontier_count = self._count_bits(player_frontier & player)
        opponent_frontier_count = self._count_bits(opponent_frontier & opponent)

        # Fewer frontier discs is better (more stable)
        return (opponent_frontier_count - player_frontier_count) * self.weights.frontier_weight

    def _count_bits(self, bitboard: int) -> int:
        """Count number of set bits in bitboard"""
        count = 0
        while bitboard:
            count += 1
            bitboard &= bitboard - 1
        return count
