"""
Mobility evaluation.

Evaluates position based on move availability for current player vs opponent.
Critical factor in midgame, less important in opening/endgame.
"""

from AI.Apocalyptron.evaluation.interfaces import GamePhase, PositionEvaluator
from AI.Apocalyptron.evaluation.phase_detector import GamePhaseDetector


class MobilityEvaluator(PositionEvaluator):
    """
    Evaluates position based on mobility (number of available moves).

    Mobility is weighted differently based on game phase:
    - Opening: Low weight (piece count matters more)
    - Midgame: High weight (control and options are critical)
    - Endgame: Low weight (piece count dominates)

    Extracted from GrandmasterEngine.evaluate_advanced (lines 179-192).
    """

    def __init__(self, weights=None):
        """
        Initialize mobility evaluator.

        Args:
            weights: EvaluationWeights instance (uses mobility_opening/midgame/endgame)
        """
        from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights

        self.weights = weights if weights is not None else EvaluationWeights()
        self.phase_detector = GamePhaseDetector()

    def evaluate(self, game) -> int:
        """
        Evaluate mobility differential.

        Args:
            game: BitboardGame instance

        Returns:
            int: Mobility score (positive = more moves than opponent)
        """
        # Detect game phase
        phase = self.phase_detector.detect_phase(game)

        # Calculate my mobility (current player)
        my_mobility = game._count_bits(game.get_valid_moves())

        # Calculate opponent mobility (temporarily pass turn)
        game.pass_turn()
        opponent_mobility = game._count_bits(game.get_valid_moves())
        game.undo_move()  # Restore turn

        # Mobility differential
        mobility_diff = my_mobility - opponent_mobility

        # Apply phase-specific weight
        if phase == GamePhase.OPENING:
            return int(mobility_diff * self.weights.mobility_opening)
        elif phase == GamePhase.MIDGAME:
            return int(mobility_diff * self.weights.mobility_midgame)
        else:  # ENDGAME
            return int(mobility_diff * self.weights.mobility_endgame)
