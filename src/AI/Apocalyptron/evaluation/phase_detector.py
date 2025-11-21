"""
Game phase detection.

Classifies game into opening/midgame/endgame based on piece count.
"""

from AI.Apocalyptron.evaluation.interfaces import GamePhase


class GamePhaseDetector:
    """
    Detects the current game phase based on piece count.

    Thresholds:
    - Opening: 0-19 pieces (moves 1-15)
    - Midgame: 20-49 pieces (moves 16-45)
    - Endgame: 50-64 pieces (moves 46-60)
    """

    def __init__(self, opening_threshold: int = 20, endgame_threshold: int = 50):
        """
        Initialize phase detector.

        Args:
            opening_threshold: Pieces count threshold for opening (default: 20)
            endgame_threshold: Pieces count threshold for endgame (default: 50)
        """
        self.opening_threshold = opening_threshold
        self.endgame_threshold = endgame_threshold

    def detect_phase(self, game) -> GamePhase:
        """
        Detect current game phase.

        Args:
            game: BitboardGame instance

        Returns:
            GamePhase enum value
        """
        piece_count = game.black_cnt + game.white_cnt

        if piece_count < self.opening_threshold:
            return GamePhase.OPENING
        elif piece_count < self.endgame_threshold:
            return GamePhase.MIDGAME
        else:
            return GamePhase.ENDGAME

    def get_piece_count(self, game) -> int:
        """Get total piece count on board"""
        black = getattr(game, "black_cnt", 0)
        white = getattr(game, "white_cnt", 0)
        return int(black) + int(white)
