"""
EnhancedOpeningBook - Advanced opening book with sophisticated move evaluation

Backward compatible with OpeningBook but with advanced features:
- Parametric filters for evaluation thresholds
- Multi-criteria scoring system
- Configurable selection modes
- Statistical analysis of variants

Not used by existing players - available for future implementations.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from domain.knowledge.opening_book import OpeningBook


class SelectionMode(Enum):
    """Move selection mode from opening book"""

    BEST_SCORE = "best"  # Best absolute score
    WEIGHTED_RANDOM = "weighted"  # Weighted random by score
    VARIETY_FIRST = "variety"  # Prefers variety (more continuations)
    SAFE_FIRST = "safe"  # Prefers balanced moves (=)
    AGGRESSIVE = "aggressive"  # Prefers strong advantages (w++, b++)


@dataclass
class MoveEvaluation:
    """Detailed evaluation of a move from the opening book"""

    move: str
    score: float  # Final score (weighted)
    advantage_score: float  # Score from advantage
    variety_score: float  # Score from variety
    count_continuations: int  # Number of available continuations
    has_evaluation: bool  # Se ha dati di advantage
    advantage_symbol: Optional[str]  # Simbolo advantage (=, w, w+, etc.)
    is_above_threshold: bool  # Se supera la soglia configurata


class EnhancedOpeningBook(OpeningBook):
    """
    Advanced version of the opening book with sophisticated scoring system.

    BACKWARD COMPATIBLE with OpeningBook - can be used as drop-in replacement.

    New features:
    - Configurable threshold to filter moves (score_threshold)
    - Filter based on average instead of absolute value only
    - Multi-criteria system (advantage + variety + safety)
    - Different selection modes
    - Advanced statistical analysis

    Not used by existing players - ready for future extensions.
    """

    def __init__(
        self,
        book_path=None,
        advantage_weight=0.2,
        variety_weight=0.1,
        only_evaluated_openings=True,
        score_threshold=0.0,  # NEW: Minimum score threshold (default: 0.0)
        use_average_threshold=True,  # NEW: Use average instead of absolute value
        selection_mode=SelectionMode.BEST_SCORE,  # NEW: Selection mode
        safety_weight=0.05,  # NEW: Weight for safe moves (=)
    ):
        """
        Initialize enhanced opening book.

        Args:
            book_path: Path to opening book file
            advantage_weight: Weight for advantage evaluation (default: 0.2)
            variety_weight: Weight for variety (default: 0.1)
            only_evaluated_openings: Only openings with advantage data
            score_threshold: Minimum threshold to accept moves (default: 0.0)
            use_average_threshold: If True, use average of valid moves as threshold
            selection_mode: Selection mode (BEST_SCORE, WEIGHTED_RANDOM, etc.)
            safety_weight: Bonus weight for balanced moves '=' (default: 0.05)
        """
        # Initialize base class (backward compatibility)
        super().__init__(
            book_path=book_path,
            advantage_weight=advantage_weight,
            variety_weight=variety_weight,
            only_evaluated_openings=only_evaluated_openings,
        )

        # Parametri avanzati (NEW!)
        self.score_threshold = score_threshold
        self.use_average_threshold = use_average_threshold
        self.selection_mode = selection_mode
        self.safety_weight = safety_weight

    def evaluate_move_detailed(
        self, move_str: str, game_history: str, available_moves: List
    ) -> MoveEvaluation:
        """
        Detailed evaluation of a move from the opening book.

        Args:
            move_str: Move to evaluate (e.g., "C4")
            game_history: Current game history
            available_moves: All valid moves

        Returns:
            MoveEvaluation with detailed scoring
        """
        # Test if this move is in the book
        test_sequence = game_history + move_str
        book_moves_after = self.get_book_moves(test_sequence)

        # Count available continuations
        count_continuations = len(book_moves_after) if book_moves_after else 0

        # Get advantage for this sequence
        advantage = None
        for seq, adv in self.opening_advantages.items():
            if seq.upper().startswith(test_sequence.upper()):
                # Find the first matching advantage
                advantage = adv
                break

        # Calculate scores
        advantage_score = 0.0
        variety_score = 0.0
        safety_bonus = 0.0
        has_evaluation = advantage is not None

        if advantage:
            # Interpret advantage
            _, numeric_value = self.interpret_advantage(advantage)
            advantage_score = numeric_value * self.advantage_weight

            # Bonus for safe moves (=)
            if advantage == "=":
                safety_bonus = self.safety_weight

        # Variety score (more continuations = better)
        if count_continuations > 0:
            # Normalize: log scale to avoid high numbers dominating
            import math

            variety_score = math.log(1 + count_continuations) * self.variety_weight

        # Score finale
        total_score = advantage_score + variety_score + safety_bonus

        # Determina se supera soglia
        is_above_threshold = total_score >= self.score_threshold

        return MoveEvaluation(
            move=move_str,
            score=total_score,
            advantage_score=advantage_score,
            variety_score=variety_score,
            count_continuations=count_continuations,
            has_evaluation=has_evaluation,
            advantage_symbol=advantage,
            is_above_threshold=is_above_threshold,
        )

    def get_ranked_moves(self, game_history: str, available_moves: List) -> List[MoveEvaluation]:
        """
        Get all ranked moves with detailed evaluations.

        Args:
            game_history: Current game history
            available_moves: Valid moves

        Returns:
            List of MoveEvaluation sorted by score (descending)
        """
        evaluations = []

        for move in available_moves:
            move_str = str(move).upper()
            eval_result = self.evaluate_move_detailed(move_str, game_history, available_moves)
            evaluations.append(eval_result)

        # Sort by score (descending - best first)
        evaluations.sort(key=lambda e: e.score, reverse=True)

        return evaluations

    def get_filtered_moves(
        self, game_history: str, available_moves: List, apply_threshold=True
    ) -> List[MoveEvaluation]:
        """
        Get filtered moves based on configured criteria.

        Args:
            game_history: Game history
            available_moves: Valid moves
            apply_threshold: If True, apply score_threshold

        Returns:
            List of filtered and sorted MoveEvaluation
        """
        # Get all evaluations
        all_evals = self.get_ranked_moves(game_history, available_moves)

        if not apply_threshold:
            return all_evals

        # Determine effective threshold
        effective_threshold = self.score_threshold

        if self.use_average_threshold and all_evals:
            # Use average as threshold if configured
            scores = [e.score for e in all_evals if e.has_evaluation]
            if scores:
                average_score = sum(scores) / len(scores)
                # Use the maximum between score_threshold and average
                effective_threshold = max(self.score_threshold, average_score)

        # Filter moves above threshold
        filtered = [e for e in all_evals if e.score >= effective_threshold]

        # If filter removes everything, return at least the best one
        if not filtered and all_evals:
            filtered = [all_evals[0]]

        return filtered

    def select_best_move(
        self, game_history: str, available_moves: List, mode: Optional[SelectionMode] = None
    ) -> Optional[str]:
        """
        Select the best move according to the configured mode.

        Args:
            game_history: Game history
            available_moves: Valid moves
            mode: Selection mode (None = use self.selection_mode)

        Returns:
            Selected move string or None
        """
        if mode is None:
            mode = self.selection_mode

        # Get filtered moves
        filtered_moves = self.get_filtered_moves(game_history, available_moves)

        if not filtered_moves:
            return None

        # Selection based on mode
        if mode == SelectionMode.BEST_SCORE:
            # Best absolute score
            return filtered_moves[0].move

        elif mode == SelectionMode.WEIGHTED_RANDOM:
            # Weighted random by score
            import random

            weights = [max(0.1, e.score + 1.0) for e in filtered_moves]  # +1 to avoid negatives
            total_weight = sum(weights)
            # Security: Using random.random() is appropriate here - not for cryptographic purposes
            # This is for game move selection, not security-sensitive operations
            r = random.random() * total_weight

            cumulative = 0
            for eval_result, weight in zip(filtered_moves, weights):
                cumulative += weight
                if r <= cumulative:
                    return eval_result.move

            return filtered_moves[0].move  # Fallback

        elif mode == SelectionMode.VARIETY_FIRST:
            # Prefers moves with more continuations
            sorted_by_variety = sorted(
                filtered_moves, key=lambda e: e.count_continuations, reverse=True
            )
            return sorted_by_variety[0].move

        elif mode == SelectionMode.SAFE_FIRST:
            # Prefers balanced moves (=)
            safe_moves = [e for e in filtered_moves if e.advantage_symbol == "="]
            if safe_moves:
                return safe_moves[0].move
            return filtered_moves[0].move  # Fallback to best

        elif mode == SelectionMode.AGGRESSIVE:
            # Prefers strong advantages (w++, w+)
            aggressive_moves = [
                e for e in filtered_moves if e.advantage_symbol in ["w++", "w+", "b++", "b+"]
            ]
            if aggressive_moves:
                # Sort by advantage score
                aggressive_moves.sort(key=lambda e: abs(e.advantage_score), reverse=True)
                return aggressive_moves[0].move
            return filtered_moves[0].move  # Fallback

        else:
            # Default: best score
            return filtered_moves[0].move

    def get_move_statistics(self, game_history: str, available_moves: List) -> Dict:
        """
        Get detailed statistics on available moves.

        Returns:
            Dict with complete statistics for debug/analysis
        """
        all_evals = self.get_ranked_moves(game_history, available_moves)
        filtered_evals = self.get_filtered_moves(game_history, available_moves)

        stats = {
            "total_moves": len(all_evals),
            "filtered_moves": len(filtered_evals),
            "has_book_moves": any(e.has_evaluation for e in all_evals),
            "best_move": filtered_evals[0].move if filtered_evals else None,
            "best_score": filtered_evals[0].score if filtered_evals else 0.0,
            "average_score": sum(e.score for e in all_evals) / len(all_evals) if all_evals else 0.0,
            "threshold_used": self.score_threshold,
            "selection_mode": self.selection_mode.value,
            "evaluations": filtered_evals,
        }

        return stats


def get_enhanced_opening_book(
    score_threshold=0.0, use_average_threshold=True, selection_mode=SelectionMode.BEST_SCORE
):
    """
    Factory to create EnhancedOpeningBook with default configuration.

    Args:
        score_threshold: Minimum score threshold (default: 0.0 - accepts only positive)
        use_average_threshold: Use average as dynamic threshold
        selection_mode: Selection mode

    Returns:
        Configured EnhancedOpeningBook ready to use
    """
    import os

    # Determine path to opening book files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")

    # Search for opening book files
    book_files = []
    if os.path.exists(data_dir):
        for filename in sorted(os.listdir(data_dir)):
            if filename.endswith(".txt") and "opening" in filename.lower():
                book_files.append(os.path.join(data_dir, filename))

    # Create enhanced book (use first file or None)
    book_path = book_files[0] if book_files else None

    enhanced_book = EnhancedOpeningBook(
        book_path=book_path,
        advantage_weight=0.2,
        variety_weight=0.1,
        only_evaluated_openings=True,
        score_threshold=score_threshold,
        use_average_threshold=use_average_threshold,
        selection_mode=selection_mode,
        safety_weight=0.05,
    )

    # Load any additional files
    for additional_file in book_files[1:]:
        enhanced_book.load_additional_book(additional_file)

    return enhanced_book
