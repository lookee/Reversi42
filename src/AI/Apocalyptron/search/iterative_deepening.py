"""
Iterative Deepening Search with Observer Pattern.

Complete refactored version with all print statements replaced by observer notifications.
"""

from typing import Optional, List
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete, INFINITY
from AI.Apocalyptron.ordering.pv_move import PVMoveOrderer
from AI.Apocalyptron.ordering.killer_moves import KillerMoveOrderer
from AI.Apocalyptron.observers.interfaces import SearchObserver
from AI.Apocalyptron.observers.console import ConsoleObserver
import time


class IterativeDeepeningSearch:
    """
    Iterative deepening with Observer Pattern.
    
    Complete separation of search logic from output.
    Notifies observers of all search events.
    """
    
    def __init__(self, alphabeta: AlphaBetaSearchComplete, 
                 use_aspiration: bool = True,
                 observers: Optional[List[SearchObserver]] = None):
        """
        Initialize with observers.
        
        Args:
            alphabeta: AlphaBetaSearchComplete instance
            use_aspiration: Whether to use aspiration windows
            observers: List of SearchObserver instances (None = console, [] = quiet)
        """
        self.alphabeta = alphabeta
        self.use_aspiration = use_aspiration
        
        # Setup observers
        if observers is None:
            self.observers = [ConsoleObserver()]
        elif observers == []:
            from AI.Apocalyptron.observers.quiet import QuietObserver
            self.observers = [QuietObserver()]
        else:
            self.observers = observers
        
        # Extract orderers for updates
        self.pv_orderer = None
        self.killer_orderer = None
        
        for orderer in alphabeta.orderer.orderers:
            if isinstance(orderer, PVMoveOrderer):
                self.pv_orderer = orderer
            elif isinstance(orderer, KillerMoveOrderer):
                self.killer_orderer = orderer
    
    def get_best_move(self, game, target_depth: int, player_name: str = None,
                     opening_book=None, game_history: str = None):
        """
        Get best move using iterative deepening with observer notifications.
        
        Args:
            game: BitboardGame instance
            target_depth: Target search depth
            player_name: Player name (for observers)
            opening_book: Opening book (for observers)
            game_history: Game history (for observers)
            
        Returns:
            Best move found
        """
        time_start = time.perf_counter()
        
        # Notify: Search start
        self._notify_search_start(target_depth, player_name, game)
        
        move_list = game.get_move_list()
        if not move_list:
            return None
        
        final_best_move = None
        final_best_value = -INFINITY
        prev_iteration_value = 0
        
        # Aspiration statistics (stored as instance attributes for access by ParallelSearch)
        self.aspiration_hits = 0
        self.aspiration_fails = 0
        aspiration_hits = 0
        aspiration_fails = 0
        
        # Iterative deepening loop
        for current_depth in range(1, target_depth + 1):
            iter_start = time.perf_counter()
            self.alphabeta.nodes = 0
            self.alphabeta.pruning = 0
            
            # Set killer depth
            if self.killer_orderer:
                self.killer_orderer.set_depth(current_depth)
            
            # Aspiration window
            use_asp = self.use_aspiration and current_depth >= 3
            alpha_asp = prev_iteration_value - max(25, 100 - current_depth * 10) if use_asp else -INFINITY
            beta_asp = prev_iteration_value + max(25, 100 - current_depth * 10) if use_asp else INFINITY
            
            # Notify: Iteration start
            self._notify_iteration_start(current_depth, target_depth, use_asp, alpha_asp, beta_asp)
            
            # Order moves
            ordered_moves = self.alphabeta.orderer.order_moves(game, move_list)
            
            best_value = -INFINITY
            best_move = None
            re_search_needed = False
            
            # Search moves
            for move in ordered_moves:
                move_start = time.perf_counter()
                game.move(move)
                
                # Try aspiration or full window
                if use_asp and not re_search_needed:
                    value = -self.alphabeta.alphabeta(game, current_depth - 1, -beta_asp, -max(alpha_asp, best_value))
                    if value <= alpha_asp or value >= beta_asp:
                        value = -self.alphabeta.alphabeta(game, current_depth - 1, -INFINITY, -best_value)
                        re_search_needed = True
                        aspiration_fails += 1
                        self.aspiration_fails += 1
                    else:
                        aspiration_hits += 1
                        self.aspiration_hits += 1
                else:
                    value = -self.alphabeta.alphabeta(game, current_depth - 1, -INFINITY, -best_value)
                
                game.undo_move()
                
                move_time = time.perf_counter() - move_start
                is_new_best = (value > best_value or best_move is None)
                
                # Notify: Move evaluated
                self._notify_move_evaluated(move, value, is_new_best, 
                                           self.alphabeta.nodes, self.alphabeta.pruning, move_time)
                
                if value > best_value or best_move is None:
                    best_value = value
                    best_move = move
            
            # Update PV
            if self.pv_orderer:
                self.pv_orderer.set_pv_move(best_move)
            
            final_best_move = best_move
            final_best_value = best_value
            prev_iteration_value = best_value
            
            iter_time = time.perf_counter() - iter_start
            
            # Notify: Iteration complete
            self._notify_iteration_complete(current_depth, best_move, best_value, 
                                           iter_time, not re_search_needed)
        
        # Prepare final statistics
        time_total = time.perf_counter() - time_start
        stats = self.alphabeta.get_statistics()
        stats['depth'] = target_depth
        stats['aspiration_hits'] = aspiration_hits
        stats['aspiration_fails'] = aspiration_fails
        
        # Notify: Search complete
        self._notify_search_complete(final_best_move, final_best_value, stats, time_total,
                                     opening_book, game_history, game)
        
        return final_best_move
    
    # Observer notification methods
    
    def _notify_search_start(self, depth, player_name, game):
        """Notify all observers of search start"""
        for observer in self.observers:
            observer.on_search_start(depth, player_name, game, mode="sequential")
    
    def _notify_iteration_start(self, current_depth, target_depth, use_asp, alpha, beta):
        """Notify all observers of iteration start"""
        for observer in self.observers:
            observer.on_iteration_start(current_depth, target_depth, use_asp, alpha, beta)
    
    def _notify_move_evaluated(self, move, value, is_best, nodes, pruning, elapsed_time):
        """Notify all observers of move evaluation"""
        for observer in self.observers:
            observer.on_move_evaluated(move, value, is_best, nodes, pruning, elapsed_time)
    
    def _notify_iteration_complete(self, depth, best_move, value, iteration_time, asp_success):
        """Notify all observers of iteration completion"""
        for observer in self.observers:
            observer.on_iteration_complete(depth, best_move, value, iteration_time, asp_success)
    
    def _notify_search_complete(self, best_move, value, stats, total_time, 
                                opening_book, game_history, game):
        """Notify all observers of search completion"""
        for observer in self.observers:
            observer.on_search_complete(best_move, value, stats, total_time,
                                       opening_book, game_history, game)
    
    def reset(self):
        """Reset search state"""
        self.alphabeta.reset()

