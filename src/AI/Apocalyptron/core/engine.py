"""
Apocalyptron Engine - Standalone Implementation.

Complete standalone engine using ONLY modular components.
NO dependency on GrandmasterEngine.

This is the full refactored version that uses:
- AlphaBetaSearchComplete (all optimizations)
- IterativeDeepeningSearch (progressive search)
- ParallelSearch (multi-core)
- All modular evaluation/ordering/pruning components
"""

import time
from typing import Optional

from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.Apocalyptron.evaluation import (
    CompositeEvaluator,
    MobilityEvaluator,
    ParityEvaluator,
    PositionalEvaluator,
    StabilityEvaluator,
)
from AI.Apocalyptron.ordering import (
    CompositeOrderer,
    HistoryHeuristicOrderer,
    KillerMoveOrderer,
    PositionalOrderer,
    PVMoveOrderer,
)
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
from AI.Apocalyptron.search.parallel import ParallelSearch
from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights


class ApocalyptronEngine:
    """
    Apocalyptron engine using ONLY modular components.

    Complete standalone implementation with ZERO dependency on GrandmasterEngine.
    Uses clean modular architecture with all optimizations.

    Architecture:
    - Evaluation: CompositeEvaluator (Mobility + Positional + Stability + Parity)
    - Ordering: CompositeOrderer (PV + Killer + History + Positional)
    - Search: AlphaBetaSearchComplete (all optimizations)
    - Iterative: IterativeDeepeningSearch (progressive + aspiration)
    - Parallel: ParallelSearch (multi-core at final depth)
    """

    def __init__(
        self,
        config: Optional[ApocalyptronConfig] = None,
        weights: Optional[EvaluationWeights] = None,
    ):
        """
        Initialize standalone Apocalyptron engine.

        Args:
            config: ApocalyptronConfig instance (None = default)
            weights: EvaluationWeights instance (None = default from config)
        """
        self.config = config if config is not None else ApocalyptronConfig()
        self.weights = weights if weights is not None else self.config.weights

        # Build evaluator
        self.evaluator = self._build_evaluator()

        # Build orderer
        self.orderer = self._build_orderer()

        # Build search
        self.alphabeta = AlphaBetaSearchComplete(
            self.evaluator,
            self.orderer,
            enable_null_move=self.config.enable_null_move_pruning,
            enable_futility=self.config.enable_futility_pruning,
            enable_lmr=self.config.enable_late_move_reduction,
            enable_multi_cut=self.config.enable_multi_cut_pruning,
        )

        # Setup observers based on config
        self.observers = self._build_observers()

        # Build search strategy (NEW - uses SearchStrategy pattern)
        self.search_strategy = self._build_search_strategy()

        # Wrap with parallel search
        if self.config.use_parallel:
            self.parallel_search = ParallelSearch(
                self.search_strategy,  # Wrap the strategy (not alphabeta directly)
                num_workers=self.config.num_workers,
                parallel_threshold_depth=self.config.parallel_threshold_depth,
                parallel_threshold_moves=self.config.parallel_threshold_moves,
                observers=self.observers,
            )
        else:
            self.parallel_search = self.search_strategy

        # Statistics
        self.searches_performed = 0
        self.total_time = 0.0

    def _build_evaluator(self) -> CompositeEvaluator:
        """
        Build composite evaluator from configuration.

        UPDATED: Now supports dynamic evaluator configuration.
        Can build different combinations based on config.evaluators.
        """
        evaluator = CompositeEvaluator()

        # Build evaluators from configuration (dynamic!)
        for eval_config in self.config.evaluators:
            # Use custom weights if provided, otherwise use engine default weights
            eval_weights = eval_config.custom_weights or self.weights

            if eval_config.evaluator_type == "mobility":
                evaluator.add_evaluator(MobilityEvaluator(eval_weights), weight=eval_config.weight)
            elif eval_config.evaluator_type == "positional":
                evaluator.add_evaluator(
                    PositionalEvaluator(eval_weights), weight=eval_config.weight
                )
            elif eval_config.evaluator_type == "stability":
                evaluator.add_evaluator(StabilityEvaluator(eval_weights), weight=eval_config.weight)
            elif eval_config.evaluator_type == "parity":
                evaluator.add_evaluator(ParityEvaluator(eval_weights), weight=eval_config.weight)

        return evaluator

    def _build_orderer(self) -> CompositeOrderer:
        """Build composite orderer with all components"""
        orderer = CompositeOrderer()

        if self.config.enable_pv_ordering:
            orderer.add_orderer(PVMoveOrderer())

        if self.config.enable_killer_moves:
            orderer.add_orderer(KillerMoveOrderer())

        if self.config.enable_history_heuristic:
            orderer.add_orderer(HistoryHeuristicOrderer())

        orderer.add_orderer(PositionalOrderer(self.weights))

        return orderer

    def _build_observers(self):
        """Build observers based on configuration"""
        from AI.Apocalyptron.observers import ConsoleObserver, QuietObserver

        if self.config.show_search_output:
            return [ConsoleObserver()]
        else:
            return [QuietObserver()]

    def _build_search_strategy(self):
        """
        Build search strategy from configuration.

        NEW METHOD: Creates appropriate SearchStrategy based on config.search_strategy.
        Supports: 'fixed_depth', 'iterative_deepening', 'adaptive'
        """
        from AI.Apocalyptron.search import (
            AdaptiveDepthStrategy,
            FixedDepthStrategy,
            IterativeDeepeningStrategy,
        )

        if self.config.search_strategy == "fixed_depth":
            return FixedDepthStrategy(self.alphabeta, observers=self.observers)

        elif self.config.search_strategy == "iterative_deepening":
            return IterativeDeepeningStrategy(
                self.alphabeta,
                use_aspiration=self.config.use_aspiration_windows,
                observers=self.observers,
            )

        elif self.config.search_strategy == "adaptive":
            # CRITICAL: Create a copy of adaptive_depths to avoid sharing
            # This ensures each engine instance has its own independent depth config
            import copy

            adaptive_depths_copy = copy.deepcopy(self.config.adaptive_depths)
            return AdaptiveDepthStrategy(
                self.alphabeta, depth_config=adaptive_depths_copy, observers=self.observers
            )

        else:
            raise ValueError(
                f"Unknown search strategy: {self.config.search_strategy}. "
                f"Valid options: 'fixed_depth', 'iterative_deepening', 'adaptive'"
            )

    def get_best_move(
        self,
        game,
        depth: int,
        player_name: Optional[str] = None,
        opening_book=None,
        game_history: Optional[str] = None,
        observer=None,
    ):
        """
        Get best move for position.

        Args:
            game: BitboardGame instance
            depth: Search depth
            player_name: Player name for display
            opening_book: Opening book instance
            game_history: Game history string
            observer: Optional SearchObserver for real-time updates

        Returns:
            Best move found
        """
        start_time = time.perf_counter()

        # Add dynamic observer if provided
        if observer:
            self.search_strategy.add_observer(observer)

        # Use parallel search (which internally decides parallel vs sequential)
        move = self.parallel_search.get_best_move(
            game, depth, player_name, opening_book, game_history
        )

        # Remove dynamic observer
        if observer:
            self.search_strategy.remove_observer(observer)

        elapsed = time.perf_counter() - start_time

        # Update statistics
        self.searches_performed += 1
        self.total_time += elapsed

        return move

    def evaluate(self, game) -> int:
        """Evaluate position"""
        return self.evaluator.evaluate(game)

    def get_statistics(self) -> dict:
        """Get engine statistics"""
        return {
            "engine": "Apocalyptron (Modular Architecture)",
            "searches_performed": self.searches_performed,
            "total_time": self.total_time,
            "avg_time": (
                self.total_time / self.searches_performed if self.searches_performed > 0 else 0
            ),
            "search_stats": self.alphabeta.get_statistics(),
            "config": self.config.to_dict(),
        }

    def reset(self):
        """Reset engine state"""
        self.alphabeta.reset()
        self.searches_performed = 0
        self.total_time = 0.0

    @property
    def num_workers(self):
        """Get number of worker processes"""
        if self.config.use_parallel:
            return self.parallel_search.num_workers
        return 1

    def __del__(self):
        """Cleanup on destruction"""
        if hasattr(self, "parallel_search") and isinstance(self.parallel_search, ParallelSearch):
            self.parallel_search.close_pool()
