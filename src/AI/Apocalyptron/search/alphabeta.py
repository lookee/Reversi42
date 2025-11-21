"""
Alpha-Beta search implementation using modular components.

Clean implementation that uses:
- CompositeEvaluator for position evaluation
- CompositeOrderer for move ordering
- PruningStrategies for optimization
- TranspositionTable for caching
"""

import time
from typing import List, Optional

from AI.Apocalyptron.cache.transposition_table import TranspositionTable
from AI.Apocalyptron.cache.zobrist_hash import ZobristHasher
from AI.Apocalyptron.core.search_context import SearchContext
from AI.Apocalyptron.core.search_result import SearchResult
from AI.Apocalyptron.evaluation.composite import CompositeEvaluator
from AI.Apocalyptron.ordering.composite import CompositeOrderer
from AI.Apocalyptron.search.interfaces import SearchAlgorithm

INFINITY = 999999


class AlphaBetaSearch(SearchAlgorithm):
    """
    Alpha-beta search using modular components.

    This is a clean implementation that uses composition instead of
    inheritance, making it easy to test and extend.

    Components:
    - Evaluator: Position evaluation (CompositeEvaluator)
    - Orderer: Move ordering (CompositeOrderer)
    - Pruning: Optimization strategies (list of PruningStrategy)
    - Cache: Transposition table for position caching
    """

    def __init__(
        self,
        evaluator: CompositeEvaluator,
        orderer: CompositeOrderer,
        pruning_strategies: Optional[List] = None,
        use_transposition_table: bool = True,
    ):
        """
        Initialize AlphaBeta search.

        Args:
            evaluator: CompositeEvaluator instance
            orderer: CompositeOrderer instance
            pruning_strategies: List of PruningStrategy instances (optional)
            use_transposition_table: Whether to use TT (default: True)
        """
        self.evaluator = evaluator
        self.orderer = orderer
        self.pruning_strategies = pruning_strategies or []

        # Transposition table
        self.use_tt = use_transposition_table
        self.tt = TranspositionTable() if use_transposition_table else None
        self.zobrist = ZobristHasher() if use_transposition_table else None

        # Statistics
        self.nodes = 0
        self.pruning = 0
        self.tt_hits = 0
        self.start_time = 0

    def search(self, context: SearchContext) -> SearchResult:
        """
        Perform alpha-beta search.

        Args:
            context: SearchContext with position and parameters

        Returns:
            SearchResult with best move and statistics
        """
        self.nodes = 0
        self.pruning = 0
        self.tt_hits = 0
        self.start_time = time.perf_counter()

        # Get moves
        move_list = context.game.get_move_list()

        if not move_list:
            return SearchResult(best_move=None, value=0, nodes_searched=0, time_elapsed=0)

        # Order moves
        ordered_moves = self.orderer.order_moves(context.game, move_list)

        # Search each move
        best_move = None
        best_value = -INFINITY
        alpha = context.alpha
        beta = context.beta

        for move in ordered_moves:
            # Make move
            context.game.move(move)

            # Search
            value = -self._alphabeta(
                context.game,
                context.depth - 1,
                -beta,
                -alpha,
                not context.allow_null_move,  # Toggle null move
            )

            # Undo move
            context.game.undo_move()

            # Update best
            if value > best_value or best_move is None:
                best_value = value
                best_move = move

            # Update alpha
            if value > alpha:
                alpha = value

            # Beta cutoff
            if alpha >= beta:
                self.pruning += 1
                break

        # Create result
        elapsed = time.perf_counter() - self.start_time

        return SearchResult(
            best_move=best_move,
            value=best_value,
            nodes_searched=self.nodes,
            nodes_pruned=self.pruning,
            time_elapsed=elapsed,
            depth_reached=context.depth,
            tt_hits=self.tt_hits,
            tt_size=self.tt.size() if self.tt else 0,
        )

    def _alphabeta(self, game, depth: int, alpha: int, beta: int, allow_null_move: bool) -> int:
        """
        Recursive alpha-beta search.

        Args:
            game: Game instance
            depth: Remaining depth
            alpha: Alpha bound
            beta: Beta bound
            allow_null_move: Whether null move is allowed

        Returns:
            int: Position evaluation
        """
        self.nodes += 1

        # Transposition table lookup
        if self.use_tt:
            pos_hash = self.zobrist.hash_position(game)
            entry = self.tt.lookup(pos_hash)

            if entry and entry.is_usable(depth):
                self.tt_hits += 1
                if entry.flag == "exact":
                    return entry.value
                elif entry.flag == "lower" and entry.value >= beta:
                    return entry.value
                elif entry.flag == "upper" and entry.value <= alpha:
                    return entry.value

        # Terminal conditions
        if game.check_lost():
            return -INFINITY
        if game.check_win():
            return INFINITY
        if depth == 0:
            return self.evaluator.evaluate(game)

        # Get moves
        move_list = game.get_move_list()

        # No moves = pass
        if not move_list:
            game.pass_turn()
            value = -self._alphabeta(game, depth - 1, -beta, -alpha, False)
            game.undo_move()
            return value

        # Order moves
        ordered_moves = self.orderer.order_moves(game, move_list)

        # Search moves
        best_value = -INFINITY
        original_alpha = alpha

        for move in ordered_moves:
            game.move(move)
            value = -self._alphabeta(game, depth - 1, -beta, -alpha, True)
            game.undo_move()

            if value > best_value:
                best_value = value

            if value > alpha:
                alpha = value

            if alpha >= beta:
                self.pruning += 1
                # Store in TT
                if self.use_tt:
                    self.tt.store(pos_hash, depth, beta, "lower", move)
                return beta

        # Store in TT
        if self.use_tt:
            if best_value <= original_alpha:
                self.tt.store(pos_hash, depth, best_value, "upper")
            else:
                self.tt.store(pos_hash, depth, best_value, "exact")

        return best_value

    def get_best_move(self, game, depth: int, **kwargs):
        """
        Get best move (high-level interface).

        Args:
            game: Game instance
            depth: Search depth
            **kwargs: Additional parameters

        Returns:
            Best move found
        """
        context = SearchContext(
            game=game,
            depth=depth,
            alpha=-INFINITY,
            beta=INFINITY,
            allow_null_move=True,
        )

        result = self.search(context)
        return result.best_move

    def get_statistics(self) -> dict:
        """Get search statistics"""
        return {
            "nodes": self.nodes,
            "pruning": self.pruning,
            "tt_hits": self.tt_hits,
            "tt_size": self.tt.size() if self.tt else 0,
        }

    def reset(self):
        """Reset search state"""
        self.nodes = 0
        self.pruning = 0
        self.tt_hits = 0
        if self.tt:
            self.tt.clear()
