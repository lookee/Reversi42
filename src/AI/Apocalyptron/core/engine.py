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

from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights
from AI.Apocalyptron.evaluation import (
    CompositeEvaluator, MobilityEvaluator, PositionalEvaluator,
    StabilityEvaluator, ParityEvaluator
)
from AI.Apocalyptron.ordering import (
    CompositeOrderer, PositionalOrderer, KillerMoveOrderer,
    HistoryHeuristicOrderer, PVMoveOrderer
)
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
from AI.Apocalyptron.search.parallel import ParallelSearch
import time


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
    
    def __init__(self, config: ApocalyptronConfig = None, weights: EvaluationWeights = None):
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
            enable_multi_cut=self.config.enable_multi_cut_pruning
        )
        
        # Setup observers based on config
        self.observers = self._build_observers()
        
        # Wrap with iterative deepening
        if self.config.use_iterative_deepening:
            self.search = IterativeDeepeningSearch(
                self.alphabeta,
                use_aspiration=self.config.use_aspiration_windows,
                observers=self.observers
            )
        else:
            self.search = self.alphabeta
        
        # Wrap with parallel search
        if self.config.use_parallel:
            self.parallel_search = ParallelSearch(
                self.search,
                num_workers=self.config.num_workers,
                parallel_threshold_depth=self.config.parallel_threshold_depth,
                parallel_threshold_moves=self.config.parallel_threshold_moves,
                observers=self.observers
            )
        else:
            self.parallel_search = self.search
        
        # Statistics
        self.searches_performed = 0
        self.total_time = 0.0
        
        print(f"[ApocalyptronEngine] Initialized with modular components (NO GrandmasterEngine)!")
        print(f"  • Evaluators: {self.evaluator.get_evaluator_count()}")
        print(f"  • Orderers: {self.orderer.get_orderer_count()}")
        print(f"  • Null move: {self.config.enable_null_move_pruning}")
        print(f"  • Futility: {self.config.enable_futility_pruning}")
        print(f"  • LMR: {self.config.enable_late_move_reduction}")
        print(f"  • Multi-cut: {self.config.enable_multi_cut_pruning}")
        print(f"  • Iterative deepening: {self.config.use_iterative_deepening}")
        print(f"  • Parallel: {self.config.use_parallel}")
    
    def _build_evaluator(self) -> CompositeEvaluator:
        """Build composite evaluator with all components"""
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(self.weights), weight=1.0)
        evaluator.add_evaluator(PositionalEvaluator(self.weights), weight=1.0)
        evaluator.add_evaluator(StabilityEvaluator(self.weights), weight=1.0)
        evaluator.add_evaluator(ParityEvaluator(self.weights), weight=1.0)
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
    
    def get_best_move(self, game, depth: int, player_name: str = None,
                     opening_book=None, game_history: str = None):
        """
        Get best move for position.
        
        Args:
            game: BitboardGame instance
            depth: Search depth
            player_name: Player name for display
            opening_book: Opening book instance
            game_history: Game history string
            
        Returns:
            Best move found
        """
        start_time = time.perf_counter()
        
        # Use parallel search (which internally decides parallel vs sequential)
        move = self.parallel_search.get_best_move(
            game, depth, player_name, opening_book, game_history
        )
        
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
            'engine': 'Apocalyptron (Modular Architecture)',
            'searches_performed': self.searches_performed,
            'total_time': self.total_time,
            'avg_time': self.total_time / self.searches_performed if self.searches_performed > 0 else 0,
            'search_stats': self.alphabeta.get_statistics(),
            'config': self.config.to_dict(),
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
        if hasattr(self, 'parallel_search') and isinstance(self.parallel_search, ParallelSearch):
            self.parallel_search.close_pool()

