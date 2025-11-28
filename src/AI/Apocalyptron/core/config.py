"""
Apocalyptron configuration.

Centralized configuration for all engine parameters.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights


@dataclass
class EvaluatorConfig:
    """
    Configuration for a single evaluator.

    Allows customization of which evaluators to use and their weights.
    """

    evaluator_type: str  # 'mobility', 'positional', 'stability', 'parity'
    weight: float = 1.0
    custom_weights: Any = None  # Optional custom EvaluationWeights for this evaluator


def _default_evaluators() -> List[EvaluatorConfig]:
    """
    Get default evaluator configuration.

    Returns standard 4-evaluator setup (same as before refactoring).
    """
    return [
        EvaluatorConfig("mobility", weight=1.0),
        EvaluatorConfig("positional", weight=1.0),
        EvaluatorConfig("stability", weight=1.0),
        EvaluatorConfig("parity", weight=1.0),
    ]


def calculate_default_temperature(depth: int) -> float:
    """
    Calculate default temperature based on depth level.

    Lower depth players (weaker AI) get higher temperature for more variety.
    Higher depth players (stronger AI) get lower temperature for consistency.

    Args:
        depth: Search depth (1-20)

    Returns:
        Temperature value between 0.0 and 1.0

    Examples:
        depth 1-3:  0.4-0.5 (high variety for beginners)
        depth 4-6:  0.2-0.3 (moderate variety)
        depth 7-9:  0.05-0.15 (low variety, more consistent)
        depth 10+:  0.0-0.05 (minimal variety, highly consistent)
    """
    if depth <= 3:
        # Beginner level: high variety
        return 0.4 + (depth - 1) * 0.05  # 0.4-0.5
    if depth <= 6:
        # Intermediate level: moderate variety
        return 0.2 + (depth - 4) * 0.033  # 0.2-0.3
    if depth <= 9:
        # Advanced level: low variety
        return 0.05 + (depth - 7) * 0.033  # 0.05-0.15
    # Expert level: minimal variety
    return max(0.0, 0.05 - (depth - 10) * 0.01)  # 0.05-0.0


@dataclass
class ApocalyptronConfig:
    """
    Configuration for Apocalyptron engine.

    All parameters in one place for easy configuration and validation.
    """

    # Search parameters
    depth: int = 9
    use_iterative_deepening: bool = True
    use_aspiration_windows: bool = True
    aspiration_window_size: int = 50

    # Parallelization
    use_parallel: bool = True
    num_workers: Optional[int] = None  # None = auto-detect
    parallel_threshold_depth: int = 7
    parallel_threshold_moves: int = 4

    # Evaluation
    weights: EvaluationWeights = field(default_factory=EvaluationWeights)

    # Evaluator configuration (NEW - for custom evaluator combinations)
    evaluators: List[EvaluatorConfig] = field(default_factory=_default_evaluators)

    # Search strategy configuration (NEW)
    search_strategy: str = "iterative_deepening"  # 'fixed_depth', 'iterative_deepening', 'adaptive'

    # Adaptive depth configuration (NEW - only used if search_strategy='adaptive')
    adaptive_depths: Dict[str, int] = field(
        default_factory=lambda: {"opening": 7, "midgame": 9, "endgame": 11}
    )

    # Pruning techniques (enable/disable)
    enable_null_move_pruning: bool = True
    enable_futility_pruning: bool = True
    enable_late_move_reduction: bool = True
    enable_multi_cut_pruning: bool = True

    # Move ordering
    enable_killer_moves: bool = True
    enable_history_heuristic: bool = True
    enable_pv_ordering: bool = True

    # Caching
    use_transposition_table: bool = True

    # Output
    show_search_output: bool = True
    show_statistics: bool = True
    verbose: bool = False

    # Randomization / Temperature for move variety
    temperature: float = 0.0  # 0.0 = deterministic, 1.0 = maximum variety

    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.depth < 1:
            raise ValueError("Depth must be >= 1")

        if self.depth > 20:
            raise ValueError("Depth > 20 is impractical")

        if self.num_workers is not None and self.num_workers < 1:
            raise ValueError("num_workers must be >= 1 or None")

        if self.temperature < 0.0 or self.temperature > 1.0:
            raise ValueError("temperature must be between 0.0 and 1.0")

    def to_dict(self) -> dict:
        """Export configuration as dictionary"""
        return {
            "depth": self.depth,
            "use_iterative_deepening": self.use_iterative_deepening,
            "use_aspiration_windows": self.use_aspiration_windows,
            "use_parallel": self.use_parallel,
            "num_workers": self.num_workers,
            "enable_null_move_pruning": self.enable_null_move_pruning,
            "enable_futility_pruning": self.enable_futility_pruning,
            "enable_late_move_reduction": self.enable_late_move_reduction,
            "enable_multi_cut_pruning": self.enable_multi_cut_pruning,
            "weights": self.weights.to_dict(),
            # NEW fields
            "search_strategy": self.search_strategy,
            "adaptive_depths": self.adaptive_depths,
            "evaluators": [{"type": e.evaluator_type, "weight": e.weight} for e in self.evaluators],
            "temperature": self.temperature,
        }
