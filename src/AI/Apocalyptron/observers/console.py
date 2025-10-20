"""
Console Observer - Formatted output to console.

Extracts all print statements from search components.
Provides rich, formatted output for interactive play.
"""

from typing import Any, Dict, Optional

from AI.Apocalyptron.observers.interfaces import SearchObserver


class ConsoleObserver(SearchObserver):
    """
    Console observer with rich formatted output.

    Prints search progress, iteration details, and statistics
    in a user-friendly format.

    All print statements extracted from IterativeDeepeningSearch
    and ParallelSearch are here.
    """

    def __init__(self):
        """Initialize console observer"""
        self.iteration_start_time = 0

    def on_search_start(
        self, depth: int, player_name: Optional[str], game: Any, mode: str = "sequential"
    ):
        """Print search header"""
        print("\n" + "=" * 80)

        engine_name = "APOCALYPTRON AI"

        if mode == "hybrid":
            if player_name:
                print(f"🧠 {engine_name} (HYBRID) - {player_name} (multi-core)")
            else:
                print(f"🧠 {engine_name} (HYBRID) - multi-core")
        else:
            if player_name:
                print(f"🧠 {engine_name} - {player_name} (Iterative Deepening)")
            else:
                print(f"🧠 {engine_name} (Iterative Deepening)")

        # Game progress
        current_move = game.turn_cnt + 1
        max_moves = game.cells_cnt
        progress_pct = (current_move / max_moves) * 100
        print(f"Move: {current_move}/{max_moves} ({progress_pct:.1f}% complete)")
        print(f"Target depth: {depth}")
        print("=" * 80)

    def on_iteration_start(
        self,
        current_depth: int,
        target_depth: int,
        use_aspiration: bool = False,
        alpha: int = 0,
        beta: int = 0,
    ):
        """Print iteration header"""
        import time

        self.iteration_start_time = time.perf_counter()

        if use_aspiration:
            window_size = beta - alpha
            print(
                f"\n🔍 Depth {current_depth}/{target_depth} [Aspiration: {alpha} to {beta}, window ±{window_size//2}]:"
            )
        else:
            print(f"\n🔍 Depth {current_depth}/{target_depth}:")

        print(
            f"{'Move':<8} {'Value':<10} {'Best':<10} {'Nodes':<10} {'Pruning':<10} {'Time(s)':<10}"
        )
        print("-" * 80)

    def on_move_evaluated(
        self, move: Any, value: int, is_best: bool, nodes: int, pruning: int, elapsed_time: float
    ):
        """Print move evaluation result"""
        move_str = f"⭐{move}" if is_best else f"🚫{move}"
        best_value = value if is_best else (value - 1)  # Approximate

        print(
            f"{move_str:<8} {value:>8d}   {best_value:>8d}   {nodes:>8d}   "
            f"{pruning:>8d}   {elapsed_time:>8.3f}"
        )

    def on_iteration_complete(
        self,
        depth: int,
        best_move: Any,
        value: int,
        iteration_time: float,
        aspiration_success: bool = True,
    ):
        """Print iteration completion"""
        print("-" * 80)

        asp_info = ""
        if depth >= 3:  # Aspiration used from depth 3
            asp_info = f" [Asp: {'✓' if aspiration_success else '✗ re-search'}]"

        print(
            f"  ✓ Depth {depth} complete: {best_move} (value: {value}) in {iteration_time:.3f}s{asp_info}"
        )

    def on_search_complete(
        self,
        best_move: Any,
        value: int,
        statistics: Dict,
        total_time: float,
        opening_book: Any = None,
        game_history: str = None,
        game: Any = None,
    ):
        """Print final summary"""
        print("\n" + "=" * 80)
        print(f"🤖 ITERATIVE DEEPENING SUMMARY:")

        # Opening book info
        if opening_book and game_history:
            self._print_opening_info(opening_book, game_history, game)

        # Statistics
        self._print_statistics(statistics, total_time, best_move, value)

        print(f"   🚀 FUTILITY + LMR + MULTI-CUT + NULL + ASP + ID + HISTORY: Ultimate!")
        print("=" * 80 + "\n")

    def on_phase1_complete(
        self,
        stats: Dict,
        time_elapsed: float,
        final_depth: int,
        target_depth: int,
        best_move: Any = None,
        best_value: int = 0,
    ):
        """Print Phase 1 summary"""
        print("\n" + "=" * 80)
        print(f"🔍 PHASE 1: Sequential Iterative Deepening (depths 1→{final_depth})")
        print("=" * 80)

        nodes = stats.get("nodes", 0)
        pruning = stats.get("pruning", 0)
        pruning_pct = (pruning / max(nodes, 1)) * 100

        # Search Statistics
        print(f"\n📊 Search Statistics:")
        print(f"   • Total nodes explored: {nodes:,}")
        print(f"   • Alpha-beta pruning: {pruning:,} cuts ({pruning_pct:.1f}%)")
        print(f"   • Search time: {time_elapsed:.3f}s")
        if time_elapsed > 0 and nodes > 0:
            print(f"   • Average speed: {nodes/time_elapsed:,.0f} nodes/sec")

        # Optimizations Applied
        print(f"\n🎯 Optimizations Applied:")

        # LMR
        if "lmr" in stats and stats["lmr"].get("reductions", 0) > 0:
            lmr = stats["lmr"]
            print(
                f"   • Late move reduction: {lmr['reductions']:,} reductions, "
                f"{lmr['re_searches']:,} re-searches ({lmr['re_search_rate']:.1f}% re-search rate)"
            )
        else:
            print(f"   • Late move reduction: 0 reductions")

        # Null move
        if "null_move" in stats and stats["null_move"].get("attempts", 0) > 0:
            nm = stats["null_move"]
            print(
                f"   • Null move pruning: {nm['cutoffs']:,}/{nm['attempts']:,} cutoffs ({nm['success_rate']:.1f}% success)"
            )
        else:
            print(f"   • Null move pruning: 0 cutoffs")

        # Futility
        if "futility" in stats and stats["futility"].get("pruning_count", 0) > 0:
            print(
                f"   • Futility pruning: {stats['futility']['pruning_count']:,} hopeless positions cut"
            )
        else:
            print(f"   • Futility pruning: 0 hopeless positions cut")

        # Multi-cut
        if "multi_cut" in stats and stats["multi_cut"].get("pruning_count", 0) > 0:
            print(f"   • Multi-cut pruning: {stats['multi_cut']['pruning_count']:,} early cutoffs")
        else:
            print(f"   • Multi-cut pruning: 0 early cutoffs")

        # Aspiration windows
        if "aspiration_hits" in stats and "aspiration_fails" in stats:
            hits = stats["aspiration_hits"]
            fails = stats["aspiration_fails"]
            if hits + fails > 0:
                asp_rate = (hits / (hits + fails)) * 100
                print(
                    f"   • Aspiration windows: {hits} hits, {fails} fails ({asp_rate:.1f}% success)"
                )

        # Knowledge Base Built
        print(f"\n🧠 Knowledge Base Built:")

        if "history_entries" in stats:
            print(f"   • History table entries: {stats['history_entries']}")

        if "killer_moves" in stats:
            print(f"   • Killer moves cached: {stats['killer_moves']}")

        if "tt_size" in stats:
            tt_size = stats["tt_size"]
            tt_hits = stats.get("tt_hits", 0)
            print(f"   • Transposition table: {tt_size:,} entries, {tt_hits:,} hits")

        if best_move:
            print(f"   • PV move from depth {final_depth}: {best_move} (value: {best_value})")

        # Move Stability Analysis
        if "move_progression" in stats and len(stats["move_progression"]) > 0:
            self._print_move_stability(stats["move_progression"])

        print(f"\n⚡ Ready for Phase 2 parallel search at depth {target_depth}")
        print("=" * 80 + "\n")

    def _print_move_stability(self, move_progression):
        """Print move stability analysis from Phase 1"""
        print(f"\n📈 Best Move Progression:")

        # Group consecutive depths with same best move
        if not move_progression:
            return

        groups = []
        current_move = move_progression[0][1]
        start_depth = move_progression[0][0]
        end_depth = start_depth

        for depth, move in move_progression[1:]:
            if move == current_move:
                end_depth = depth
            else:
                groups.append((start_depth, end_depth, current_move))
                current_move = move
                start_depth = depth
                end_depth = depth

        # Add last group
        groups.append((start_depth, end_depth, current_move))

        # Print groups
        for start, end, move in groups:
            if start == end:
                status = ""
            else:
                status = " (stable)" if (end - start + 1) >= 3 else ""

            if start == end:
                print(f"   • Depth {start}: {move}{status}")
            else:
                print(f"   • Depth {start}-{end}: {move}{status}")

        # Final move convergence indicator
        if len(groups) == 1:
            print(f"   ✓ Completely stable (same move all depths)")
        elif groups[-1][1] - groups[-1][0] >= 2:
            print(f"   ✓ Converged to {groups[-1][2]}")

    def on_parallel_phase_start(self, depth: int, num_workers: int):
        """Print parallel phase start"""
        print(f"{'Move':<8} {'Value':<10} {'Nodes':<12} {'Pruning':<10}")
        print("-" * 50)

    def on_parallel_result(self, move: Any, value: int, is_best: bool, nodes: int, pruning: int):
        """Print parallel evaluation result"""
        move_str = f"⭐{move}" if is_best else f"🚫{move}"
        print(f"{move_str:<8} {value:>8d}   {nodes:>10,}   {pruning:>8,}")

    def _print_opening_info(self, opening_book, game_history, game):
        """Print opening book information"""
        current_opening = opening_book.get_current_opening_name(game_history)
        all_openings = opening_book.get_remaining_openings(game_history)

        if current_opening:
            advantage = opening_book.get_opening_advantage(game_history)
            if advantage and advantage != "=":
                eval_score = opening_book.evaluate_advantage_for_player(advantage, game.turn)
                desc, _ = opening_book.interpret_advantage(advantage)
                sign = "+" if eval_score >= 0 else ""
                print(
                    f"   • Opening: {current_opening} [{advantage}] - {desc} ({sign}{eval_score:.2f})"
                )
            else:
                print(f"   • Opening: {current_opening}")
        elif len(all_openings) > 0:
            openings_preview = ", ".join(sorted(all_openings)[:3])
            if len(all_openings) > 3:
                print(f"   • Following: {openings_preview} ...")
            else:
                print(f"   • Following: {openings_preview}")

        if len(all_openings) > 0:
            print(f"   • Openings in book: {len(all_openings)} available")

    def _print_statistics(self, stats: Dict, total_time: float, best_move: Any, value: int):
        """Print detailed statistics"""
        print(f"   • Final depth: {stats.get('depth', '?')}")
        print(f"   • Total nodes: {stats.get('nodes', 0):,}")

        nodes = stats.get("nodes", 1)
        pruning = stats.get("pruning", 0)
        pruning_pct = (pruning / max(nodes, 1)) * 100
        print(f"   • Alpha-beta pruning: {pruning:,} ({pruning_pct:.1f}%)")

        # LMR statistics
        if "lmr" in stats and stats["lmr"].get("reductions", 0) > 0:
            lmr = stats["lmr"]
            print(
                f"   • Late move reduction: {lmr['reductions']:,} reductions, "
                f"{lmr['re_searches']:,} re-searches ({lmr['re_search_rate']:.1f}%)"
            )

        # Futility statistics
        if "futility" in stats and stats["futility"].get("pruning_count", 0) > 0:
            print(
                f"   • Futility pruning: {stats['futility']['pruning_count']:,} hopeless positions cut"
            )

        # Multi-cut statistics
        if "multi_cut" in stats and stats["multi_cut"].get("pruning_count", 0) > 0:
            print(f"   • Multi-cut pruning: {stats['multi_cut']['pruning_count']:,} cutoffs")

        # Null move statistics
        if "null_move" in stats and stats["null_move"].get("attempts", 0) > 0:
            nm = stats["null_move"]
            print(
                f"   • Null move pruning: {nm['cutoffs']:,}/{nm['attempts']:,} cutoffs ({nm['success_rate']:.1f}% success)"
            )

        # History table
        if "history_entries" in stats:
            print(f"   • History table entries: {stats['history_entries']}")

        # Aspiration windows (if provided separately)
        if "aspiration_hits" in stats and "aspiration_fails" in stats:
            hits = stats["aspiration_hits"]
            fails = stats["aspiration_fails"]
            if hits + fails > 0:
                asp_rate = (hits / (hits + fails)) * 100
                print(
                    f"   • Aspiration windows: {hits} hits, {fails} fails ({asp_rate:.1f}% success)"
                )

        # Time and speed
        print(f"   • Total time: {total_time:.3f}s")
        if total_time > 0 and nodes > 0:
            print(f"   • Average rate: {nodes/total_time:,.0f} nodes/sec")

        # Best move
        print(f"   • Selected move: {best_move} (value: {value})")
