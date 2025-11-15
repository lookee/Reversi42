"""
Factory for creating Apocalyptron engines.

Provides convenient methods for creating pre-configured engines.
"""

from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.Apocalyptron.core.engine import ApocalyptronEngine
from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder
from AI.Apocalyptron.weights.weight_presets import get_preset_weights


class ApocalyptronFactory:
    """
    Factory for creating Apocalyptron engines.

    Provides convenient methods for common configurations.
    """

    @staticmethod
    def create_engine(config: ApocalyptronConfig = None) -> ApocalyptronEngine:
        """
        Create engine from configuration.

        Args:
            config: ApocalyptronConfig instance (None = default)

        Returns:
            ApocalyptronEngine instance
        """
        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_default(depth: int = 9) -> ApocalyptronEngine:
        """
        Create engine with default settings.

        Args:
            depth: Search depth (default: 9)

        Returns:
            ApocalyptronEngine with default configuration
        """
        config = ApocalyptronConfigBuilder().with_depth(depth).enable_all_optimizations().build()

        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_aggressive(depth: int = 9) -> ApocalyptronEngine:
        """
        Create aggressive mobility-focused engine.

        Args:
            depth: Search depth (default: 9)

        Returns:
            ApocalyptronEngine with aggressive weights
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_preset_weights("aggressive")
            .enable_all_optimizations()
            .build()
        )

        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_defensive(depth: int = 9) -> ApocalyptronEngine:
        """
        Create defensive stability-focused engine.

        Args:
            depth: Search depth (default: 9)

        Returns:
            ApocalyptronEngine with defensive weights
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_preset_weights("defensive")
            .enable_all_optimizations()
            .build()
        )

        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_tournament(depth: int = 10) -> ApocalyptronEngine:
        """
        Create tournament-optimized engine.

        Args:
            depth: Search depth (default: 10)

        Returns:
            ApocalyptronEngine optimized for tournament play
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .enable_all_optimizations()
            .quiet_mode()  # No output in tournament
            .build()
        )

        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_analysis(depth: int = 12) -> ApocalyptronEngine:
        """
        Create analysis engine (deep search, verbose).

        Args:
            depth: Search depth (default: 12)

        Returns:
            ApocalyptronEngine for deep position analysis
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .enable_all_optimizations()
            .verbose_mode()
            .build()
        )

        return ApocalyptronEngine(config=config)

    # NEW PRESETS - Diverse Player Configurations

    @staticmethod
    def create_speed_demon(depth: int = 6) -> ApocalyptronEngine:
        """
        Speed Demon: Maximum speed, minimal intelligence.

        - Fixed depth (no iterative deepening)
        - No pruning techniques
        - Only positional evaluator
        - No parallel (overhead too high for shallow)

        Args:
            depth: Search depth (default: 6)

        Returns:
            ApocalyptronEngine optimized for speed
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_fixed_depth_search()
            .with_only_positional()
            .disable_all_pruning()
            .enable_parallel(False)
            .quiet_mode()
            .build()
        )
        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_mobility_obsessed(depth: int = 9) -> ApocalyptronEngine:
        """
        Mobility Obsessed: Only cares about move count.

        - Only mobility evaluator
        - All other optimizations enabled

        Args:
            depth: Search depth (default: 9)

        Returns:
            ApocalyptronEngine focused on mobility
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_only_mobility(weight=1.0)
            .enable_all_optimizations()
            .build()
        )
        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_corner_hunter(depth: int = 9) -> ApocalyptronEngine:
        """
        Corner Hunter: Obsessed with corners.

        - Only positional evaluator
        - Corner hunter weight preset
        - All optimizations enabled

        Args:
            depth: Search depth (default: 9)

        Returns:
            ApocalyptronEngine focused on positional play
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_only_positional()
            .with_preset_weights("corner_hunter")
            .enable_all_optimizations()
            .build()
        )
        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_pure_alphabeta(depth: int = 7) -> ApocalyptronEngine:
        """
        Pure Alpha-Beta: No fancy optimizations.

        - Fixed depth
        - No pruning
        - No iterative deepening
        - Basic evaluator mix

        Args:
            depth: Search depth (default: 7)

        Returns:
            ApocalyptronEngine with pure alpha-beta
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_fixed_depth_search()
            .disable_all_pruning()
            .enable_parallel(False)
            .build()
        )
        return ApocalyptronEngine(config=config)

    @staticmethod
    def create_adaptive_player(
        opening_depth: int = 7, mid_depth: int = 9, end_depth: int = 11
    ) -> ApocalyptronEngine:
        """
        Adaptive Player: Changes depth based on game phase.

        - Adaptive depth strategy
        - All optimizations enabled
        - Shallow in opening, deep in endgame

        Args:
            opening_depth: Depth for opening phase (default: 7)
            mid_depth: Depth for midgame phase (default: 9)
            end_depth: Depth for endgame phase (default: 11)

        Returns:
            ApocalyptronEngine with adaptive depth
        """
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(mid_depth)  # Base depth
            .with_adaptive_depth(opening_depth, mid_depth, end_depth)
            .enable_all_optimizations()
            .build()
        )
        return ApocalyptronEngine(config=config)
