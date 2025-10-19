"""
Configuration builder for Apocalyptron.

Provides fluent API for building engine configurations.
"""

from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights
from AI.Apocalyptron.weights.weight_presets import get_preset_weights


class ApocalyptronConfigBuilder:
    """
    Fluent builder for ApocalyptronConfig.
    
    Example:
        config = (ApocalyptronConfigBuilder()
            .with_depth(9)
            .with_weights(get_preset_weights('aggressive'))
            .enable_all_optimizations()
            .build())
    """
    
    def __init__(self):
        """Initialize with default config"""
        self._config = ApocalyptronConfig()
    
    def with_depth(self, depth: int) -> 'ApocalyptronConfigBuilder':
        """Set search depth"""
        self._config.depth = depth
        return self
    
    def with_weights(self, weights: EvaluationWeights) -> 'ApocalyptronConfigBuilder':
        """Set evaluation weights"""
        self._config.weights = weights
        return self
    
    def with_preset_weights(self, preset_name: str) -> 'ApocalyptronConfigBuilder':
        """Set weights from preset name"""
        self._config.weights = get_preset_weights(preset_name)
        return self
    
    def with_num_workers(self, num_workers: int) -> 'ApocalyptronConfigBuilder':
        """Set number of worker processes"""
        self._config.num_workers = num_workers
        return self
    
    def enable_iterative_deepening(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable iterative deepening"""
        self._config.use_iterative_deepening = enabled
        return self
    
    def enable_aspiration_windows(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable aspiration windows"""
        self._config.use_aspiration_windows = enabled
        return self
    
    def enable_parallel(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable parallel search"""
        self._config.use_parallel = enabled
        return self
    
    def enable_null_move_pruning(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable null move pruning"""
        self._config.enable_null_move_pruning = enabled
        return self
    
    def enable_futility_pruning(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable futility pruning"""
        self._config.enable_futility_pruning = enabled
        return self
    
    def enable_late_move_reduction(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable late move reduction"""
        self._config.enable_late_move_reduction = enabled
        return self
    
    def enable_multi_cut_pruning(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable multi-cut pruning"""
        self._config.enable_multi_cut_pruning = enabled
        return self
    
    def enable_all_optimizations(self) -> 'ApocalyptronConfigBuilder':
        """Enable all optimization techniques"""
        self._config.enable_null_move_pruning = True
        self._config.enable_futility_pruning = True
        self._config.enable_late_move_reduction = True
        self._config.enable_multi_cut_pruning = True
        self._config.use_iterative_deepening = True
        self._config.use_aspiration_windows = True
        self._config.use_parallel = True
        return self
    
    def enable_output(self, enabled: bool = True) -> 'ApocalyptronConfigBuilder':
        """Enable/disable search output"""
        self._config.show_search_output = enabled
        self._config.show_statistics = enabled
        return self
    
    def quiet_mode(self) -> 'ApocalyptronConfigBuilder':
        """Disable all output (quiet mode)"""
        self._config.show_search_output = False
        self._config.show_statistics = False
        self._config.verbose = False
        return self
    
    def verbose_mode(self) -> 'ApocalyptronConfigBuilder':
        """Enable verbose output"""
        self._config.verbose = True
        self._config.show_search_output = True
        self._config.show_statistics = True
        return self
    
    def build(self) -> ApocalyptronConfig:
        """Build and return the configuration"""
        return self._config

