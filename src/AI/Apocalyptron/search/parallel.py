"""
Parallel Search Decorator with Observer Pattern.

Wraps sequential search to add root-level parallelization.
Distributes root moves across worker processes for speedup.
Uses observers for output separation.

Extracted from GrandmasterEngine._get_best_move_parallel_ordered and
ParallelBitboardMinimaxEngine (lines 776-920 and parallel engine).
"""

import copy
import sys
import time
from multiprocessing import Pool, cpu_count
from typing import TYPE_CHECKING, List, Optional, Union

if TYPE_CHECKING:
    from multiprocessing.pool import Pool as PoolType
else:
    PoolType = Pool

from AI.Apocalyptron.observers.interfaces import SearchObserver

# Set multiprocessing start method for Windows and macOS compatibility
# macOS Python 3.9+ can have issues with "fork" when used with pytest-xdist
# Using "spawn" is more reliable across platforms
if sys.platform in ("win32", "darwin"):
    try:
        from multiprocessing import set_start_method

        set_start_method("spawn", force=True)
    except RuntimeError:
        # Already set, ignore
        pass


def _evaluate_move_worker(args):
    """
    Worker function for parallel move evaluation.

    Must be at module level for pickling.

    Args:
        args: Tuple of (game_state, move, depth, evaluator_data, orderer_data)

    Returns:
        Tuple of (move, value, nodes, pruning)
    """
    game_state, move, depth = args

    # Create search instance for this worker
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
    from AI.Apocalyptron.weights import EvaluationWeights

    # Recreate components in worker
    weights = EvaluationWeights()

    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights))
    evaluator.add_evaluator(PositionalEvaluator(weights))
    evaluator.add_evaluator(StabilityEvaluator(weights))
    evaluator.add_evaluator(ParityEvaluator(weights))

    orderer = CompositeOrderer()
    orderer.add_orderer(PVMoveOrderer())
    orderer.add_orderer(KillerMoveOrderer())
    orderer.add_orderer(HistoryHeuristicOrderer())
    orderer.add_orderer(PositionalOrderer(weights))

    search = AlphaBetaSearchComplete(evaluator, orderer)

    # Copy game
    game = copy.deepcopy(game_state)

    # Make move
    game.move(move)

    # Evaluate
    from AI.Apocalyptron.search.alphabeta_complete import INFINITY

    value = -search.alphabeta(game, depth - 1, -INFINITY, INFINITY)

    return (move, value, search.nodes, search.pruning)


class ParallelSearch:
    """
    Parallel search using multiprocessing.

    Parallelizes root-level move evaluation across worker processes.
    Provides 2-5x speedup on multi-core systems.
    """

    def __init__(
        self,
        base_search,
        num_workers: Optional[int] = None,
        parallel_threshold_depth: int = 7,
        parallel_threshold_moves: int = 4,
        observers: Optional[List[SearchObserver]] = None,
    ):
        """
        Initialize parallel search.

        Args:
            base_search: IterativeDeepeningSearch instance
            num_workers: Number of worker processes (None = auto)
            parallel_threshold_depth: Min depth for parallel (default: 7)
            parallel_threshold_moves: Min moves for parallel (default: 4)
            observers: List of observers (inherits from base_search if None)
        """
        self.base_search = base_search
        self.num_workers = num_workers or max(1, cpu_count() - 1)
        self.parallel_threshold_depth = parallel_threshold_depth
        self.parallel_threshold_moves = parallel_threshold_moves

        # Use base_search observers if not provided
        self.observers = observers if observers is not None else base_search.observers

        # Worker pool (lazy init)
        self._pool: Optional[PoolType] = None

    def _get_pool(self):
        """Get or create worker pool"""
        if self._pool is None:
            try:
                self._pool = Pool(processes=self.num_workers)
            except Exception as e:
                # Fallback: disable parallel processing on error (e.g., Windows issues)
                import warnings

                warnings.warn(
                    f"Failed to create multiprocessing pool: {e}. "
                    "Falling back to sequential processing."
                )
                # Return None to indicate sequential fallback
                return None
        return self._pool

    def close_pool(self):
        """Close worker pool"""
        if self._pool is not None:
            self._pool.close()
            self._pool.join()
            self._pool = None

    def get_best_move(
        self,
        game,
        target_depth: int,
        player_name: Optional[str] = None,
        opening_book=None,
        game_history: Optional[str] = None,
    ):
        """
        Get best move with optional parallelization.

        Decides whether to use parallel or sequential based on:
        - Depth (>= parallel_threshold_depth)
        - Number of moves (>= parallel_threshold_moves)
        - Available cores

        Args:
            game: BitboardGame instance
            target_depth: Search depth
            player_name: Player name for display
            opening_book: Opening book instance
            game_history: Game history string

        Returns:
            Best move found
        """
        move_list = game.get_move_list()
        if not move_list:
            return None

        # Decide parallel vs sequential
        use_parallel = (
            target_depth >= self.parallel_threshold_depth
            and len(move_list) >= self.parallel_threshold_moves
            and self.num_workers >= 2
        )

        # CRITICAL: Check if sequential search has already completed to target depth
        # If so, avoid parallel search to prevent re-searching from scratch
        if use_parallel:
            # Check if base_search has already reached target depth
            # This prevents parallel search from re-searching if sequential is already complete
            if hasattr(self.base_search, "max_depth_reached"):
                if self.base_search.max_depth_reached >= target_depth:
                    # Sequential search already complete, use it directly
                    return self.base_search.get_best_move(
                        game, target_depth, player_name, opening_book, game_history
                    )

            return self._get_best_move_parallel(
                game, target_depth, player_name, move_list, opening_book, game_history
            )
        else:
            # Use sequential iterative deepening
            return self.base_search.get_best_move(
                game, target_depth, player_name, opening_book, game_history
            )

    def _get_best_move_parallel(
        self, game, depth, player_name, move_list, opening_book, game_history
    ):
        """
        Parallel search at root level.

        Strategy: Iterative deepening sequentially up to depth-1,
        then parallel search at final depth.
        """
        time_start = time.perf_counter()

        # Notify: Search start (hybrid mode)
        for observer in self.observers:
            observer.on_search_start(depth, player_name, game, mode="hybrid")

        # Phase 1: Iterative deepening sequentially up to depth-1
        # (Phase 1 notifications handled by base_search observers)
        phase1_best_move = None
        phase1_best_value = 0
        phase1_time = 0.0
        phase1_stats = {}  # Initialize outside if block for later access
        move_progression = []  # Track best move at each depth

        # Use base search for depths 1 to depth-1 (builds TT, PV, history)
        if depth > 1:
            phase1_start = time.perf_counter()

            # Use quiet observers for intermediate depths
            from AI.Apocalyptron.observers.quiet import QuietObserver

            original_observers = self.base_search.observers
            # CRITICAL: Replace observers with QuietObserver to prevent output during Phase 1
            self.base_search.observers = [QuietObserver()]

            # Track best moves at each depth for stability analysis
            # IMPORTANT: Only run Phase 1 if we haven't already searched up to depth-1
            # Check if alphabeta has already searched to depth-1 by checking statistics
            existing_depth = 0
            if hasattr(self.base_search, "alphabeta") and hasattr(
                self.base_search.alphabeta, "get_statistics"
            ):
                existing_stats = self.base_search.alphabeta.get_statistics()
                existing_depth = existing_stats.get("depth_reached", existing_stats.get("depth", 0))

            # Only run Phase 1 if we haven't already reached depth-1
            if existing_depth < depth - 1:
                for current_depth in range(max(1, existing_depth + 1), depth):
                    phase1_best_move = self.base_search.get_best_move(
                        game, current_depth, player_name=None
                    )
                    move_progression.append((current_depth, phase1_best_move))
            else:
                # Already searched to depth-1, skip Phase 1
                # Get the best move from the last search
                if hasattr(self.base_search, "alphabeta") and hasattr(
                    self.base_search.alphabeta, "orderer"
                ):
                    # Try to get PV move from orderer
                    for orderer in self.base_search.alphabeta.orderer.orderers:
                        if hasattr(orderer, "pv_move") and orderer.pv_move:
                            phase1_best_move = orderer.pv_move
                            break

            # Restore original observers AFTER Phase 1 completes
            self.base_search.observers = original_observers

            phase1_time = time.perf_counter() - phase1_start

            # Get Phase 1 statistics
            phase1_stats = self.base_search.alphabeta.get_statistics()

            # Get best value from alphabeta if available
            if hasattr(self.base_search, "last_best_value"):
                phase1_best_value = self.base_search.last_best_value

            # Add aspiration windows stats from iterative deepening
            if hasattr(self.base_search, "aspiration_hits"):
                phase1_stats["aspiration_hits"] = self.base_search.aspiration_hits
                phase1_stats["aspiration_fails"] = self.base_search.aspiration_fails

            # Add move progression for stability analysis
            phase1_stats["move_progression"] = move_progression

            # Notify: Phase 1 complete
            for observer in self.observers:
                observer.on_phase1_complete(
                    stats=phase1_stats,
                    time_elapsed=phase1_time,
                    final_depth=depth - 1,
                    target_depth=depth,
                    best_move=phase1_best_move,
                    best_value=phase1_best_value,
                )

        # Phase 2: Parallel search at final depth
        # Notify: Parallel phase start
        for observer in self.observers:
            observer.on_parallel_phase_start(depth, self.num_workers)

        parallel_start = time.perf_counter()

        # Order moves using current orderer state
        ordered_moves = self.base_search.alphabeta.orderer.order_moves(game, move_list)

        # Prepare work items
        work_items = [(game, move, depth) for move in ordered_moves]

        # Evaluate in parallel - use imap_unordered for streaming results
        pool = self._get_pool()

        # Fallback to sequential if pool creation failed (e.g., Windows issues)
        if pool is None:
            # Use base search sequentially instead
            return self.base_search.get_best_move(
                game, depth, player_name, opening_book, game_history
            )

        # Process results as they arrive (streaming like tail -f)
        best_move = None
        best_value = -999999
        total_nodes = 0
        total_pruning = 0
        moves_with_values = []  # Collect all moves with values for temperature selection

        move_count = 0
        for move, value, nodes, pruning in pool.imap_unordered(_evaluate_move_worker, work_items):
            total_nodes += nodes
            total_pruning += pruning
            move_count += 1

            moves_with_values.append((move, value))

            is_best = value > best_value or best_move is None

            # Notify: Parallel result IMMEDIATELY as it arrives
            for observer in self.observers:
                observer.on_parallel_result(move, value, is_best, total_nodes, total_pruning)

            if value > best_value or best_move is None:
                best_value = value
                best_move = move

        # Apply temperature-based selection if enabled
        # Get temperature from base_search if available
        temperature = 0.0
        if hasattr(self.base_search, "alphabeta") and hasattr(
            self.base_search.alphabeta, "temperature"
        ):
            temperature = self.base_search.alphabeta.temperature

        if temperature > 0.0:
            from AI.Apocalyptron.randomization import apply_temperature_selection

            # Sort moves by value descending
            moves_with_values.sort(key=lambda x: x[1], reverse=True)
            best_move = apply_temperature_selection(moves_with_values, temperature)

        parallel_time = time.perf_counter() - parallel_start
        time_total = time.perf_counter() - time_start

        # Notify: Search complete (with parallel-specific statistics)
        stats = (
            self.base_search.alphabeta.get_statistics()
            if hasattr(self.base_search, "alphabeta")
            else {}
        )

        # Get Phase 1 nodes if available (from phase1_stats)
        phase1_nodes = phase1_stats.get("nodes", 0) if depth > 1 else 0
        phase1_pruning = phase1_stats.get("pruning", 0) if depth > 1 else 0

        # IMPORTANT: Combine Phase 1 + Parallel phase nodes for accurate totals
        total_nodes_combined = phase1_nodes + total_nodes
        total_pruning_combined = phase1_pruning + total_pruning

        # Use standard keys for compatibility with observers
        stats["depth_reached"] = depth
        stats["nodes_searched"] = total_nodes_combined  # Phase 1 + Parallel
        stats["nodes_pruned"] = total_pruning_combined  # Phase 1 + Parallel
        stats["parallel_time"] = parallel_time * 1000  # Convert to ms
        stats["total_time"] = time_total * 1000  # Convert to ms
        stats["parallel_workers"] = self.num_workers
        stats["parallel_mode"] = "active"
        stats["parallel_moves_evaluated"] = len(work_items)
        stats["num_workers"] = self.num_workers
        stats["phase1_nodes"] = phase1_nodes  # For debugging
        stats["parallel_nodes"] = total_nodes  # For debugging

        for observer in self.observers:
            observer.on_search_complete(
                best_move,
                best_value,
                stats,
                time_total * 1000,
                opening_book,
                game_history,
                game,  # Convert to ms
            )

        return best_move

    def __del__(self):
        """Cleanup on destruction"""
        self.close_pool()
