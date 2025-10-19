"""
Parallel Search Decorator.

Wraps sequential search to add root-level parallelization.
Distributes root moves across worker processes for speedup.

Extracted from GrandmasterEngine._get_best_move_parallel_ordered and
ParallelBitboardMinimaxEngine (lines 776-920 and parallel engine).
"""

from multiprocessing import Pool, cpu_count
from typing import Optional
import time
import copy


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
    from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
    from AI.Apocalyptron.evaluation import (
        CompositeEvaluator, MobilityEvaluator, PositionalEvaluator,
        StabilityEvaluator, ParityEvaluator
    )
    from AI.Apocalyptron.ordering import (
        CompositeOrderer, PositionalOrderer, KillerMoveOrderer,
        HistoryHeuristicOrderer, PVMoveOrderer
    )
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
    
    def __init__(self, base_search, num_workers: Optional[int] = None,
                 parallel_threshold_depth: int = 7,
                 parallel_threshold_moves: int = 4,
                 verbose: bool = True):
        """
        Initialize parallel search.
        
        Args:
            base_search: IterativeDeepeningSearch instance
            num_workers: Number of worker processes (None = auto)
            parallel_threshold_depth: Min depth for parallel (default: 7)
            parallel_threshold_moves: Min moves for parallel (default: 4)
            verbose: Print search progress
        """
        self.base_search = base_search
        self.num_workers = num_workers or max(1, cpu_count() - 1)
        self.parallel_threshold_depth = parallel_threshold_depth
        self.parallel_threshold_moves = parallel_threshold_moves
        self.verbose = verbose
        
        # Worker pool (lazy init)
        self._pool = None
    
    def _get_pool(self):
        """Get or create worker pool"""
        if self._pool is None:
            self._pool = Pool(processes=self.num_workers)
        return self._pool
    
    def close_pool(self):
        """Close worker pool"""
        if self._pool is not None:
            self._pool.close()
            self._pool.join()
            self._pool = None
    
    def get_best_move(self, game, target_depth: int, player_name: str = None,
                     opening_book=None, game_history: str = None):
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
            target_depth >= self.parallel_threshold_depth and
            len(move_list) >= self.parallel_threshold_moves and
            self.num_workers >= 2
        )
        
        if use_parallel:
            return self._get_best_move_parallel(game, target_depth, player_name, 
                                              move_list, opening_book, game_history)
        else:
            # Use sequential iterative deepening
            return self.base_search.get_best_move(game, target_depth, player_name,
                                                 opening_book, game_history)
    
    def _get_best_move_parallel(self, game, depth, player_name, move_list,
                                opening_book, game_history):
        """
        Parallel search at root level.
        
        Strategy: Iterative deepening sequentially up to depth-1,
        then parallel search at final depth.
        """
        time_start = time.perf_counter()
        
        if self.verbose:
            print("\n" + "="*80)
            engine_name = "APOCALYPTRON AI"
            if player_name:
                print(f"🧠 {engine_name} (HYBRID) - {player_name} ({self.num_workers} cores)")
            else:
                print(f"🧠 {engine_name} (HYBRID) - {self.num_workers} cores")
            
            current_move = game.turn_cnt + 1
            max_moves = game.cells_cnt
            progress_pct = (current_move / max_moves) * 100
            print(f"Move: {current_move}/{max_moves} ({progress_pct:.1f}% complete)")
            print(f"Target depth: {depth} (Sequential 1-{depth-1}, Parallel {depth})")
            print("="*80)
        
        # Phase 1: Iterative deepening sequentially up to depth-1
        if depth > 1 and self.verbose:
            print(f"\n📈 Phase 1: Iterative deepening (depths 1-{depth-1})...")
        
        # Use base search for depths 1 to depth-1 (builds TT, PV, history)
        if depth > 1:
            # Temporarily disable verbose for intermediate depths
            original_verbose = self.base_search.verbose
            self.base_search.verbose = False
            
            for current_depth in range(1, depth):
                self.base_search.get_best_move(game, current_depth, player_name=None)
                
                if self.verbose:
                    best_move = self.base_search.pv_orderer.pv_move if self.base_search.pv_orderer else None
                    nodes = self.base_search.alphabeta.nodes
                    print(f"  Depth {current_depth}: {best_move} ({nodes:,} nodes)")
            
            self.base_search.verbose = original_verbose
        
        # Phase 2: Parallel search at final depth
        if self.verbose:
            print(f"\n⚡ Phase 2: Parallel search at depth {depth}...")
        
        parallel_start = time.perf_counter()
        
        # Order moves using current orderer state
        ordered_moves = self.base_search.alphabeta.orderer.order_moves(game, move_list)
        
        # Prepare work items
        work_items = [(game, move, depth) for move in ordered_moves]
        
        # Evaluate in parallel
        pool = self._get_pool()
        results = pool.map(_evaluate_move_worker, work_items)
        
        # Process results
        if self.verbose:
            print(f"\n{'Move':<8} {'Value':<10} {'Nodes':<12} {'Pruning':<10}")
            print("-"*50)
        
        best_move = None
        best_value = -999999
        total_nodes = 0
        total_pruning = 0
        
        for move, value, nodes, pruning in results:
            total_nodes += nodes
            total_pruning += pruning
            
            is_best = value > best_value or best_move is None
            
            if self.verbose:
                move_str = f"⭐{move}" if is_best else f"  {move}"
                print(f"{move_str:<8} {value:>8d}   {nodes:>10,}   {pruning:>8,}")
            
            if value > best_value or best_move is None:
                best_value = value
                best_move = move
        
        parallel_time = time.perf_counter() - parallel_start
        time_total = time.perf_counter() - time_start
        
        # Final summary
        if self.verbose:
            self._print_parallel_summary(depth, best_move, best_value, total_nodes,
                                        total_pruning, parallel_time, time_total,
                                        opening_book, game_history, game)
        
        return best_move
    
    def _print_parallel_summary(self, depth, best_move, best_value, total_nodes,
                               total_pruning, parallel_time, time_total,
                               opening_book, game_history, game):
        """Print parallel search summary"""
        print("\n" + "="*80)
        print(f"🤖 HYBRID ITERATIVE DEEPENING + PARALLEL SUMMARY:")
        
        # Opening book info
        if opening_book and game_history:
            current_opening = opening_book.get_current_opening_name(game_history)
            all_openings = opening_book.get_remaining_openings(game_history)
            
            if current_opening:
                advantage = opening_book.get_opening_advantage(game_history)
                if advantage and advantage != '=':
                    eval_score = opening_book.evaluate_advantage_for_player(advantage, game.turn)
                    desc, _ = opening_book.interpret_advantage(advantage)
                    sign = '+' if eval_score >= 0 else ''
                    print(f"   • Opening: {current_opening} [{advantage}] - {desc} ({sign}{eval_score:.2f})")
                else:
                    print(f"   • Opening: {current_opening}")
            elif len(all_openings) > 0:
                openings_preview = ', '.join(sorted(all_openings)[:3])
                if len(all_openings) > 3:
                    print(f"   • Following: {openings_preview} ...")
                else:
                    print(f"   • Following: {openings_preview}")
            
            if len(all_openings) > 0:
                print(f"   • Openings in book: {len(all_openings)} available")
        
        print(f"   • Final depth: {depth}")
        print(f"   • Workers (final depth): {self.num_workers} cores")
        print(f"   • Parallel nodes: {total_nodes:,}")
        print(f"   • Parallel pruning: {total_pruning:,} ({100*total_pruning/max(total_nodes,1):.1f}%)")
        
        stats = self.base_search.alphabeta.get_statistics()
        if 'history_entries' in stats:
            print(f"   • History table entries: {stats['history_entries']}")
        
        print(f"   • Parallel time: {parallel_time:.3f}s")
        print(f"   • Total time: {time_total:.3f}s")
        if time_total > 0:
            print(f"   • Overall rate: {total_nodes/time_total:,.0f} nodes/sec")
        print(f"   • Selected move: {best_move} (value: {best_value})")
        print(f"   🚀 HYBRID: Iterative deepening + history + parallel power!")
        print("="*80 + "\n")
    
    def __del__(self):
        """Cleanup on destruction"""
        self.close_pool()

