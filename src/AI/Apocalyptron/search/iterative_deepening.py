"""
Iterative Deepening Search.

Progressively searches from depth 1 to target depth, using results
from previous iterations to improve move ordering and aspiration windows.

Extracted from GrandmasterEngine._get_best_move_sequential_ordered (lines 538-774).
"""

from typing import Optional
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete, INFINITY
from AI.Apocalyptron.ordering.pv_move import PVMoveOrderer
from AI.Apocalyptron.ordering.killer_moves import KillerMoveOrderer
import time


class IterativeDeepeningSearch:
    """
    Iterative deepening with aspiration windows.
    
    Searches progressively from depth 1 to target depth.
    Uses results from previous iterations for:
    - Better move ordering (PV move)
    - Narrower search windows (aspiration)
    - Transposition table population
    """
    
    def __init__(self, alphabeta: AlphaBetaSearchComplete, 
                 use_aspiration: bool = True,
                 verbose: bool = True):
        """
        Initialize iterative deepening search.
        
        Args:
            alphabeta: AlphaBetaSearchComplete instance
            use_aspiration: Whether to use aspiration windows
            verbose: Whether to print search progress
        """
        self.alphabeta = alphabeta
        self.use_aspiration = use_aspiration
        self.verbose = verbose
        
        # Extract PV orderer from alphabeta for updates
        self.pv_orderer = None
        for orderer_component in alphabeta.orderer.orderers:
            if isinstance(orderer_component, PVMoveOrderer):
                self.pv_orderer = orderer_component
                break
        
        # Extract killer orderer for depth setting
        self.killer_orderer = None
        for orderer_component in alphabeta.orderer.orderers:
            if isinstance(orderer_component, KillerMoveOrderer):
                self.killer_orderer = orderer_component
                break
    
    def get_best_move(self, game, target_depth: int, player_name: str = None,
                     opening_book=None, game_history: str = None):
        """
        Get best move using iterative deepening.
        
        Args:
            game: BitboardGame instance
            target_depth: Target search depth
            player_name: Player name for display
            opening_book: Opening book (for display)
            game_history: Game history (for display)
            
        Returns:
            Best move found at target depth
        """
        time_start = time.perf_counter()
        
        # Print header
        if self.verbose:
            self._print_header(game, target_depth, player_name)
        
        move_list = game.get_move_list()
        if not move_list:
            return None
        
        final_best_move = None
        final_best_value = -INFINITY
        prev_iteration_value = 0
        
        # Aspiration statistics
        aspiration_hits = 0
        aspiration_fails = 0
        
        # ITERATIVE DEEPENING: depth 1, 2, 3, ..., target_depth
        for current_depth in range(1, target_depth + 1):
            iter_start = time.perf_counter()
            self.alphabeta.nodes = 0
            self.alphabeta.pruning = 0
            
            # Set depth for killer moves
            if self.killer_orderer:
                self.killer_orderer.set_depth(current_depth)
            
            # Determine aspiration window
            use_asp = self.use_aspiration and current_depth >= 3
            
            if use_asp:
                window_size = max(25, 100 - current_depth * 10)
                alpha_asp = prev_iteration_value - window_size
                beta_asp = prev_iteration_value + window_size
                
                if self.verbose:
                    print(f"\n🔍 Depth {current_depth}/{target_depth} [Aspiration: {alpha_asp} to {beta_asp}, window ±{window_size}]:")
            else:
                if self.verbose:
                    print(f"\n🔍 Depth {current_depth}/{target_depth}:")
            
            if self.verbose:
                print(f"{'Move':<8} {'Value':<10} {'Best':<10} {'Nodes':<10} {'Pruning':<10} {'Time(s)':<10}")
                print("-"*80)
            
            # Order moves (PV first if available)
            ordered_moves = self.alphabeta.orderer.order_moves(game, move_list)
            
            best_value = -INFINITY
            best_move = None
            re_search_needed = False
            
            # Search moves
            for move in ordered_moves:
                game.move(move)
                
                if use_asp and not re_search_needed:
                    # Try aspiration window
                    value = -self.alphabeta.alphabeta(game, current_depth - 1, -beta_asp, -max(alpha_asp, best_value))
                    
                    # Check if need full window
                    if value <= alpha_asp or value >= beta_asp:
                        value = -self.alphabeta.alphabeta(game, current_depth - 1, -INFINITY, -best_value)
                        re_search_needed = True
                        aspiration_fails += 1
                    else:
                        aspiration_hits += 1
                else:
                    # Full window search
                    value = -self.alphabeta.alphabeta(game, current_depth - 1, -INFINITY, -best_value)
                
                game.undo_move()
                
                if self.verbose:
                    time_diff = time.perf_counter() - iter_start
                    is_new_best = (value > best_value or best_move is None)
                    move_str = f"⭐{move}" if is_new_best else f"  {move}"
                    print(f"{move_str:<8} {value:>8d}   {best_value:>8d}   {self.alphabeta.nodes:>8d}   "
                          f"{self.alphabeta.pruning:>8d}   {time_diff:>8.3f}")
                
                if value > best_value or best_move is None:
                    best_value = value
                    best_move = move
            
            # Update PV for next iteration
            if self.pv_orderer:
                self.pv_orderer.set_pv_move(best_move)
            
            final_best_move = best_move
            final_best_value = best_value
            prev_iteration_value = best_value
            
            if self.verbose:
                iter_time = time.perf_counter() - iter_start
                print("-"*80)
                asp_info = f" [Asp: {'✓' if not re_search_needed and use_asp else '✗ re-search' if re_search_needed else 'N/A'}]" if use_asp else ""
                print(f"  ✓ Depth {current_depth} complete: {best_move} (value: {best_value}) in {iter_time:.3f}s{asp_info}")
        
        # Final summary
        if self.verbose:
            self._print_summary(target_depth, final_best_move, final_best_value, 
                              aspiration_hits, aspiration_fails, time_start,
                              opening_book, game_history, game)
        
        return final_best_move
    
    def _print_header(self, game, depth, player_name):
        """Print search header"""
        print("\n" + "="*80)
        
        engine_name = "APOCALYPTRON AI"
        if player_name:
            print(f"🧠 {engine_name} - {player_name} (Iterative Deepening)")
        else:
            print(f"🧠 {engine_name} (Iterative Deepening)")
        
        current_move = game.turn_cnt + 1
        max_moves = game.cells_cnt
        progress_pct = (current_move / max_moves) * 100
        print(f"Move: {current_move}/{max_moves} ({progress_pct:.1f}% complete)")
        print(f"Target depth: {depth}")
        print("="*80)
    
    def _print_summary(self, depth, best_move, best_value, asp_hits, asp_fails,
                      time_start, opening_book, game_history, game):
        """Print final summary"""
        time_total = time.perf_counter() - time_start
        stats = self.alphabeta.get_statistics()
        
        print("\n" + "="*80)
        print(f"🤖 ITERATIVE DEEPENING SUMMARY:")
        
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
        print(f"   • Total nodes: {stats['nodes']:,}")
        print(f"   • Alpha-beta pruning: {stats['pruning']:,} ({100*stats['pruning']/max(stats['nodes'],1):.1f}%)")
        
        if 'lmr' in stats and stats['lmr']['reductions'] > 0:
            lmr_rate = stats['lmr']['re_search_rate']
            print(f"   • Late move reduction: {stats['lmr']['reductions']:,} reductions, "
                  f"{stats['lmr']['re_searches']:,} re-searches ({lmr_rate:.1f}%)")
        
        if 'futility' in stats and stats['futility']['pruning_count'] > 0:
            print(f"   • Futility pruning: {stats['futility']['pruning_count']:,} hopeless positions cut")
        
        if 'multi_cut' in stats and stats['multi_cut']['pruning_count'] > 0:
            print(f"   • Multi-cut pruning: {stats['multi_cut']['pruning_count']:,} cutoffs")
        
        if 'null_move' in stats and stats['null_move']['attempts'] > 0:
            nmp_rate = stats['null_move']['success_rate']
            print(f"   • Null move pruning: {stats['null_move']['cutoffs']:,}/"
                  f"{stats['null_move']['attempts']:,} cutoffs ({nmp_rate:.1f}% success)")
        
        if 'history_entries' in stats:
            print(f"   • History table entries: {stats['history_entries']}")
        
        if asp_hits + asp_fails > 0:
            asp_rate = 100 * asp_hits / (asp_hits + asp_fails)
            print(f"   • Aspiration windows: {asp_hits} hits, {asp_fails} fails ({asp_rate:.1f}% success)")
        
        print(f"   • Total time: {time_total:.3f}s")
        if time_total > 0:
            print(f"   • Average rate: {stats['nodes']/time_total:,.0f} nodes/sec")
        
        print(f"   • Selected move: {best_move} (value: {best_value})")
        print(f"   🚀 FUTILITY + LMR + MULTI-CUT + NULL + ASP + ID + HISTORY: Ultimate!")
        print("="*80 + "\n")
    
    def reset(self):
        """Reset search state"""
        self.alphabeta.reset()

