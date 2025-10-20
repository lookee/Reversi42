"""
Parity evaluation.

Evaluates who will make the last move (important in endgame).
Even parity (we make last move) is favorable.
"""

from AI.Apocalyptron.evaluation.interfaces import GamePhase, PositionEvaluator
from AI.Apocalyptron.evaluation.phase_detector import GamePhaseDetector


class ParityEvaluator(PositionEvaluator):
    """
    Evaluates parity (who makes the last move).

    In endgame, making the last move is advantageous because
    you get the final opportunity to flip pieces.

    Even parity (even number of empty squares) = we make last move (good)
    Odd parity (odd number of empty squares) = opponent makes last move (bad)

    Only applied in endgame phase.

    Extracted from GrandmasterEngine.evaluate_advanced (lines 281-288).
    """

    def __init__(self, weights=None):
        """
        Initialize parity evaluator.

        Args:
            weights: EvaluationWeights instance
        """
        from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights

        self.weights = weights if weights is not None else EvaluationWeights()
        self.phase_detector = GamePhaseDetector()

    def evaluate(self, game) -> int:
        """
        Evaluate parity advantage.

        Args:
            game: BitboardGame instance

        Returns:
            int: Parity score (only non-zero in endgame)
        """
        # Only apply in endgame
        phase = self.phase_detector.detect_phase(game)
        if phase != GamePhase.ENDGAME:
            return 0

        # Calculate empty squares
        piece_count = game.black_cnt + game.white_cnt
        empty_count = 64 - piece_count

        # Even parity = we make last move (favorable)
        if empty_count % 2 == 0:
            return self.weights.parity_favorable
        else:
            return self.weights.parity_unfavorable
