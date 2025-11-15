"""
Fixed Depth Search Strategy.

Searches directly at target depth without iterative deepening.
Faster for situations where:
- Time is not a constraint
- You want consistent depth throughout game
- Avoiding iterative deepening overhead
"""

import time
from typing import List, Optional

from AI.Apocalyptron.observers.interfaces import SearchObserver
from AI.Apocalyptron.search.alphabeta_complete import INFINITY, AlphaBetaSearchComplete
from AI.Apocalyptron.search.strategy_interface import SearchStrategy


class FixedDepthStrategy(SearchStrategy):
    """
    Fixed depth search strategy - no iterative deepening.

    Searches directly at target depth, skipping progressive 1→N search.

    Advantages:
    - Simpler (no aspiration window complexity)
    - Slightly faster for exact depth (no 1→depth-1 overhead)
    - Predictable behavior

    Disadvantages:
    - No time management capability
    - Doesn't benefit from move ordering improvements from shallow searches
    - No progressive results (all or nothing)
    """

    def __init__(
        self, alphabeta: AlphaBetaSearchComplete, observers: Optional[List[SearchObserver]] = None
    ):
        """
        Initialize fixed depth strategy.

        Args:
            alphabeta: AlphaBetaSearchComplete instance
            observers: List of SearchObserver instances (optional)
        """
        self.alphabeta = alphabeta
        self.observers = observers or []

    def get_best_move(
        self, game, depth: int, player_name: str = None, opening_book=None, game_history: str = None
    ):
        """
        Get best move using fixed depth search.

        Searches directly at target depth (no iterative deepening).

        Args:
            game: BitboardGame instance
            depth: Search depth (used directly, no progression)
            player_name: Player name for display
            opening_book: Opening book instance (for observers)
            game_history: Game history string (for observers)

        Returns:
            Best move found
        """
        time_start = time.perf_counter()

        # Notify: Search start
        self._notify_search_start(depth, player_name, game)

        move_list = game.get_move_list()
        if not move_list:
            return None

        # Reset search statistics
        self.alphabeta.nodes = 0
        self.alphabeta.pruning = 0

        # Order moves
        ordered_moves = self.alphabeta.orderer.order_moves(game, move_list)

        # Search directly at target depth (NO iterative deepening)
        best_value = -INFINITY
        best_move = None

        for move in ordered_moves:
            game.move(move)

            # Search at full depth
            value = -self.alphabeta.alphabeta(game, depth - 1, -INFINITY, -best_value)

            game.undo_move()

            if value > best_value or best_move is None:
                best_value = value
                best_move = move

        # Update PV if available
        if hasattr(self.alphabeta, "orderer"):
            for orderer in self.alphabeta.orderer.orderers:
                if hasattr(orderer, "set_pv_move"):
                    orderer.set_pv_move(best_move)
                    break

        time_total = time.perf_counter() - time_start

        # Prepare statistics
        stats = self.alphabeta.get_statistics()
        stats["depth"] = depth
        stats["search_type"] = "fixed_depth"

        # Notify: Search complete (convert time to milliseconds)
        self._notify_search_complete(
            best_move, best_value, stats, time_total * 1000, opening_book, game_history, game
        )

        return best_move

    def reset(self):
        """Reset search state"""
        self.alphabeta.reset()

    def add_observer(self, observer: SearchObserver):
        """Add an observer dynamically"""
        if observer and observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: SearchObserver):
        """Remove an observer"""
        if observer and observer in self.observers:
            self.observers.remove(observer)

    # Observer notification methods

    def _notify_search_start(self, depth, player_name, game):
        """Notify all observers of search start"""
        for observer in self.observers:
            observer.on_search_start(depth, player_name, game, mode="fixed_depth")

    def _notify_search_complete(
        self, best_move, value, stats, total_time, opening_book, game_history, game
    ):
        """Notify all observers of search completion"""
        for observer in self.observers:
            observer.on_search_complete(
                best_move, value, stats, total_time, opening_book, game_history, game
            )
