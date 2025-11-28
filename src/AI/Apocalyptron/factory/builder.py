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

    def with_depth(self, depth: int) -> "ApocalyptronConfigBuilder":
        """Set search depth"""
        self._config.depth = depth
        return self

    def with_weights(self, weights: EvaluationWeights) -> "ApocalyptronConfigBuilder":
        """Set evaluation weights"""
        self._config.weights = weights
        return self

    def with_preset_weights(self, preset_name: str) -> "ApocalyptronConfigBuilder":
        """Set weights from preset name"""
        self._config.weights = get_preset_weights(preset_name)
        return self

    def with_num_workers(self, num_workers: int) -> "ApocalyptronConfigBuilder":
        """Set number of worker processes"""
        self._config.num_workers = num_workers
        return self

    def with_temperature(self, temperature: float) -> "ApocalyptronConfigBuilder":
        """
        Set temperature for move variety.

        Args:
            temperature: Temperature value (0.0 = deterministic, 1.0 = maximum variety)
        """
        if temperature < 0.0 or temperature > 1.0:
            raise ValueError("temperature must be between 0.0 and 1.0")
        self._config.temperature = temperature
        return self

    def enable_iterative_deepening(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable iterative deepening"""
        self._config.use_iterative_deepening = enabled
        return self

    def enable_aspiration_windows(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable aspiration windows"""
        self._config.use_aspiration_windows = enabled
        return self

    def enable_parallel(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable parallel search"""
        self._config.use_parallel = enabled
        return self

    def enable_null_move_pruning(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable null move pruning"""
        self._config.enable_null_move_pruning = enabled
        return self

    def enable_futility_pruning(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable futility pruning"""
        self._config.enable_futility_pruning = enabled
        return self

    def enable_late_move_reduction(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable late move reduction"""
        self._config.enable_late_move_reduction = enabled
        return self

    def enable_multi_cut_pruning(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable multi-cut pruning"""
        self._config.enable_multi_cut_pruning = enabled
        return self

    def enable_all_optimizations(self) -> "ApocalyptronConfigBuilder":
        """Enable all optimization techniques"""
        self._config.enable_null_move_pruning = True
        self._config.enable_futility_pruning = True
        self._config.enable_late_move_reduction = True
        self._config.enable_multi_cut_pruning = True
        self._config.use_iterative_deepening = True
        self._config.use_aspiration_windows = True
        self._config.use_parallel = True
        return self

    def enable_output(self, enabled: bool = True) -> "ApocalyptronConfigBuilder":
        """Enable/disable search output"""
        self._config.show_search_output = enabled
        self._config.show_statistics = enabled
        return self

    def quiet_mode(self) -> "ApocalyptronConfigBuilder":
        """Disable all output (quiet mode)"""
        self._config.show_search_output = False
        self._config.show_statistics = False
        self._config.verbose = False
        return self

    def verbose_mode(self) -> "ApocalyptronConfigBuilder":
        """Enable verbose output"""
        self._config.verbose = True
        self._config.show_search_output = True
        self._config.show_statistics = True
        return self

    # NEW: Search strategy configuration methods

    def with_search_strategy(self, strategy: str) -> "ApocalyptronConfigBuilder":
        """
        Set search strategy.

        Args:
            strategy: 'fixed_depth', 'iterative_deepening', or 'adaptive'
        """
        valid_strategies = ["fixed_depth", "iterative_deepening", "adaptive"]
        if strategy not in valid_strategies:
            raise ValueError(f"Invalid strategy '{strategy}'. Must be one of: {valid_strategies}")
        self._config.search_strategy = strategy
        return self

    def with_fixed_depth_search(self) -> "ApocalyptronConfigBuilder":
        """Use fixed depth search (no iterative deepening)"""
        self._config.search_strategy = "fixed_depth"
        self._config.use_iterative_deepening = False  # For backward compatibility
        return self

    def with_adaptive_depth(
        self, opening: int = 7, midgame: int = 9, endgame: int = 11
    ) -> "ApocalyptronConfigBuilder":
        """
        Use adaptive depth based on game phase.

        Args:
            opening: Depth for opening phase (default: 7)
            midgame: Depth for midgame phase (default: 9)
            endgame: Depth for endgame phase (default: 11)
        """
        self._config.search_strategy = "adaptive"
        self._config.adaptive_depths = {"opening": opening, "midgame": midgame, "endgame": endgame}
        return self

    # NEW: Evaluator configuration methods

    def with_evaluators(self, evaluator_configs: list) -> "ApocalyptronConfigBuilder":
        """
        Set evaluators explicitly.

        Args:
            evaluator_configs: List of EvaluatorConfig objects
        """
        self._config.evaluators = evaluator_configs
        return self

    def with_only_mobility(self, weight: float = 1.0) -> "ApocalyptronConfigBuilder":
        """Use ONLY mobility evaluator"""
        from AI.Apocalyptron.core.config import EvaluatorConfig

        self._config.evaluators = [EvaluatorConfig("mobility", weight=weight)]
        return self

    def with_only_positional(self, weight: float = 1.0) -> "ApocalyptronConfigBuilder":
        """Use ONLY positional evaluator"""
        from AI.Apocalyptron.core.config import EvaluatorConfig

        self._config.evaluators = [EvaluatorConfig("positional", weight=weight)]
        return self

    def with_only_stability(self, weight: float = 1.0) -> "ApocalyptronConfigBuilder":
        """Use ONLY stability evaluator"""
        from AI.Apocalyptron.core.config import EvaluatorConfig

        self._config.evaluators = [EvaluatorConfig("stability", weight=weight)]
        return self

    def with_only_parity(self, weight: float = 1.0) -> "ApocalyptronConfigBuilder":
        """Use ONLY parity evaluator"""
        from AI.Apocalyptron.core.config import EvaluatorConfig

        self._config.evaluators = [EvaluatorConfig("parity", weight=weight)]
        return self

    def add_evaluator(
        self, eval_type: str, weight: float = 1.0, custom_weights=None
    ) -> "ApocalyptronConfigBuilder":
        """
        Add single evaluator to configuration.

        Args:
            eval_type: 'mobility', 'positional', 'stability', or 'parity'
            weight: Evaluator weight (default: 1.0)
            custom_weights: Custom EvaluationWeights (optional)
        """
        from AI.Apocalyptron.core.config import EvaluatorConfig

        # If evaluators is still default, clear it first (avoid duplicates)
        default_factory = self._config.__class__.__dataclass_fields__["evaluators"].default_factory
        if default_factory is not None and callable(default_factory):
            default_evaluators = default_factory()
            if self._config.evaluators == default_evaluators:
                self._config.evaluators = []

        self._config.evaluators.append(EvaluatorConfig(eval_type, weight, custom_weights))
        return self

    def disable_all_pruning(self) -> "ApocalyptronConfigBuilder":
        """Disable ALL pruning techniques (pure alpha-beta)"""
        self._config.enable_null_move_pruning = False
        self._config.enable_futility_pruning = False
        self._config.enable_late_move_reduction = False
        self._config.enable_multi_cut_pruning = False
        return self

    def build(self) -> ApocalyptronConfig:
        """
        Build and return the configuration.

        CRITICAL: Returns a deep copy to ensure isolation between instances.
        This prevents configuration sharing between different player instances.
        """
        import copy

        return copy.deepcopy(self._config)
