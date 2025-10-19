"""
Apocalyptron configuration.

Centralized configuration for all engine parameters.
"""

from dataclasses import dataclass, field
from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights


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
    num_workers: int = None  # None = auto-detect
    parallel_threshold_depth: int = 7
    parallel_threshold_moves: int = 4
    
    # Evaluation
    weights: EvaluationWeights = field(default_factory=EvaluationWeights)
    
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
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.depth < 1:
            raise ValueError("Depth must be >= 1")
        
        if self.depth > 20:
            raise ValueError("Depth > 20 is impractical")
        
        if self.num_workers is not None and self.num_workers < 1:
            raise ValueError("num_workers must be >= 1 or None")
    
    def to_dict(self) -> dict:
        """Export configuration as dictionary"""
        return {
            'depth': self.depth,
            'use_iterative_deepening': self.use_iterative_deepening,
            'use_aspiration_windows': self.use_aspiration_windows,
            'use_parallel': self.use_parallel,
            'num_workers': self.num_workers,
            'enable_null_move_pruning': self.enable_null_move_pruning,
            'enable_futility_pruning': self.enable_futility_pruning,
            'enable_late_move_reduction': self.enable_late_move_reduction,
            'enable_multi_cut_pruning': self.enable_multi_cut_pruning,
            'weights': self.weights.to_dict(),
        }

