"""
Engine Builder

Builder Pattern: Fluent API for configuring complex engines.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from typing import Optional, Any, Dict
from AI.base.engine import Engine


class EngineBuilder:
    """
    Fluent Builder Pattern for engine configuration.
    
    Allows composing engines with features using a readable API.
    
    Example:
        engine = (EngineBuilder()
            .use_bitboard()
            .with_advanced_evaluator()
            .with_opening_book("master.book")
            .with_parallel_search(threads=8)
            .build())
    
    Features are applied using Decorator Pattern.
    """
    
    def __init__(self):
        """Initialize builder."""
        self._engine_type = None
        self._engine_class = None
        self._evaluator = None
        self._features = []  # List of (feature_name, config) tuples
        self._config = {}
        self._name = None
    
    # ========== Engine Selection ==========
    
    def use_minimax(self):
        """Use classic minimax engine with alpha-beta pruning."""
        self._engine_type = 'minimax'
        return self
    
    def use_bitboard(self):
        """Use optimized bitboard engine."""
        self._engine_type = 'bitboard'
        return self
    
    def use_grandmaster(self):
        """Use grandmaster-level engine."""
        self._engine_type = 'grandmaster'
        return self
    
    def use_random(self):
        """Use random move engine."""
        self._engine_type = 'random'
        return self
    
    def use_greedy(self):
        """Use greedy (immediate gain) engine."""
        self._engine_type = 'greedy'
        return self
    
    def use_heuristic(self):
        """Use heuristic-based engine."""
        self._engine_type = 'heuristic'
        return self
    
    def use_engine(self, engine_class):
        """Use a custom engine class directly."""
        self._engine_class = engine_class
        return self
    
    # ========== Evaluator Selection ==========
    
    def with_evaluator(self, evaluator):
        """Set a custom evaluator instance."""
        self._evaluator = evaluator
        return self
    
    def with_standard_evaluator(self):
        """Use standard evaluator (mobility + stability)."""
        self._config['evaluator_type'] = 'standard'
        return self
    
    def with_advanced_evaluator(self):
        """Use advanced evaluator (corners, edges, patterns)."""
        self._config['evaluator_type'] = 'advanced'
        return self
    
    def with_greedy_evaluator(self):
        """Use greedy evaluator (piece count only)."""
        self._config['evaluator_type'] = 'greedy'
        return self
    
    def with_positional_evaluator(self):
        """Use positional evaluator (board positions)."""
        self._config['evaluator_type'] = 'positional'
        return self
    
    # ========== Features (Decorators) ==========
    
    def with_opening_book(self, book_path: Optional[str] = None):
        """
        Add opening book feature.
        
        Args:
            book_path: Path to opening book file (optional)
        """
        self._features.append(('opening_book', {'path': book_path}))
        return self
    
    def with_parallel_search(self, threads: int = 4):
        """
        Add parallel search feature.
        
        Args:
            threads: Number of threads to use
        """
        self._features.append(('parallel', {'threads': threads}))
        return self
    
    def with_transposition_table(self, size_mb: int = 64):
        """
        Add transposition table (memoization).
        
        Args:
            size_mb: Cache size in megabytes
        """
        self._features.append(('ttable', {'size_mb': size_mb}))
        return self
    
    def with_endgame_solver(self, depth_trigger: int = 12):
        """
        Add perfect endgame solver.
        
        Args:
            depth_trigger: Depth at which to trigger perfect solver
        """
        self._features.append(('endgame', {'trigger': depth_trigger}))
        return self
    
    def with_iterative_deepening(self):
        """Add iterative deepening search."""
        self._features.append(('iterative_deepening', {}))
        return self
    
    # ========== Configuration ==========
    
    def with_name(self, name: str):
        """Set custom engine name."""
        self._name = name
        return self
    
    def with_config(self, **kwargs):
        """Set additional configuration parameters."""
        self._config.update(kwargs)
        return self
    
    # ========== Build ==========
    
    def build(self) -> Engine:
        """
        Build the configured engine.
        
        Returns:
            Engine: Configured engine instance
        
        Raises:
            ValueError: If no engine type selected
        """
        # Validate engine selection
        if not self._engine_type and not self._engine_class:
            raise ValueError(
                "No engine selected. Call use_minimax(), use_bitboard(), "
                "or use_engine() first."
            )
        
        # Get or create engine
        if self._engine_class:
            # Custom engine class provided
            engine = self._engine_class(config=self._config)
        else:
            # Create from type using registry
            engine = self._create_engine_by_type()
        
        # Set custom name if provided
        if self._name:
            engine.name = self._name
        
        # Apply features using Decorator Pattern
        for feature_name, feature_config in self._features:
            engine = self._apply_feature(engine, feature_name, feature_config)
        
        return engine
    
    def _create_engine_by_type(self) -> Engine:
        """Create base engine from type selection."""
        # Import and create engine based on type
        if self._engine_type == 'minimax':
            from AI.implementations.standard.minimax_engine import MinimaxEngine
            return MinimaxEngine(config=self._config)
        
        elif self._engine_type == 'bitboard':
            from AI.implementations.bitboard.bitboard_engine import BitboardEngine
            return BitboardEngine(config=self._config)
        
        elif self._engine_type == 'grandmaster':
            from AI.implementations.grandmaster.grandmaster_engine import GrandmasterEngine
            return GrandmasterEngine(config=self._config)
        
        elif self._engine_type == 'random':
            from AI.implementations.random.random_engine import RandomEngine
            return RandomEngine(config=self._config)
        
        elif self._engine_type == 'greedy':
            from AI.implementations.standard.greedy_engine import GreedyEngine
            return GreedyEngine(config=self._config)
        
        elif self._engine_type == 'heuristic':
            from AI.implementations.standard.heuristic_engine import HeuristicEngine
            return HeuristicEngine(config=self._config)
        
        else:
            raise ValueError(f"Unknown engine type: {self._engine_type}")
    
    def _apply_feature(self, engine: Engine, feature_name: str, config: Dict[str, Any]) -> Engine:
        """
        Apply a feature decorator to the engine.
        
        Decorator Pattern: Wraps engine with additional functionality.
        
        Args:
            engine: Base engine to wrap
            feature_name: Feature to apply
            config: Feature configuration
        
        Returns:
            Engine: Wrapped engine with feature
        """
        if feature_name == 'opening_book':
            from AI.features.opening_book_decorator import OpeningBookDecorator
            return OpeningBookDecorator(engine, book_path=config.get('path'))
        
        elif feature_name == 'parallel':
            from AI.features.parallel_search_decorator import ParallelSearchDecorator
            return ParallelSearchDecorator(engine, threads=config.get('threads', 4))
        
        elif feature_name == 'ttable':
            from AI.features.transposition_table_decorator import TranspositionTableDecorator
            return TranspositionTableDecorator(engine, size_mb=config.get('size_mb', 64))
        
        elif feature_name == 'endgame':
            from AI.features.endgame_solver_decorator import EndgameSolverDecorator
            return EndgameSolverDecorator(engine, trigger=config.get('trigger', 12))
        
        elif feature_name == 'iterative_deepening':
            from AI.features.iterative_deepening_decorator import IterativeDeepeningDecorator
            return IterativeDeepeningDecorator(engine)
        
        else:
            # Unknown feature - skip with warning
            print(f"Warning: Unknown feature '{feature_name}' - skipping")
            return engine

