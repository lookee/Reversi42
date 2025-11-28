"""
Complete Alpha-Beta search with ALL optimizations.

This is the full implementation with all techniques from GrandmasterEngine:
- Null Move Pruning
- Futility Pruning
- Late Move Reduction
- Multi-Cut Pruning
- Killer Move tracking
- History Heuristic
- Transposition Table

Extracted and refactored from GrandmasterEngine.alphabeta (lines 299-495).
"""

import time
from typing import Any, Dict, List, Optional, Tuple

from AI.Apocalyptron.cache.transposition_table import TranspositionTable
from AI.Apocalyptron.cache.zobrist_hash import ZobristHasher
from AI.Apocalyptron.core.search_context import SearchContext
from AI.Apocalyptron.core.search_result import SearchResult
from AI.Apocalyptron.evaluation.composite import CompositeEvaluator
from AI.Apocalyptron.ordering.composite import CompositeOrderer
from AI.Apocalyptron.ordering.history import HistoryHeuristicOrderer
from AI.Apocalyptron.ordering.killer_moves import KillerMoveOrderer
from AI.Apocalyptron.pruning.futility import FutilityPruning
from AI.Apocalyptron.pruning.late_move_reduction import LateMoveReduction
from AI.Apocalyptron.pruning.multi_cut import MultiCutPruning
from AI.Apocalyptron.pruning.null_move import NullMovePruning
from AI.Apocalyptron.search.interfaces import SearchAlgorithm

INFINITY = 999999


class AlphaBetaSearchComplete(SearchAlgorithm):
    """
    Complete alpha-beta implementation with all optimizations.

    This is the full-featured search that replicates all GrandmasterEngine
    functionality using modular components.
    """

    def __init__(
        self,
        evaluator: CompositeEvaluator,
        orderer: CompositeOrderer,
        enable_null_move: bool = True,
        enable_futility: bool = True,
        enable_lmr: bool = True,
        enable_multi_cut: bool = True,
        temperature: float = 0.0,
    ):
        """
        Initialize complete alpha-beta search.

        Args:
            evaluator: CompositeEvaluator for position evaluation
            orderer: CompositeOrderer for move ordering (should include killer, history, PV)
            enable_null_move: Enable null move pruning
            enable_futility: Enable futility pruning
            enable_lmr: Enable late move reduction
            enable_multi_cut: Enable multi-cut pruning
            temperature: Temperature for move variety (0.0 = deterministic, 1.0 = max variety)
        """
        self.evaluator = evaluator
        self.orderer = orderer
        self.temperature = temperature

        # Optimization strategies
        self.null_move = NullMovePruning() if enable_null_move else None
        self.futility = FutilityPruning(evaluator) if enable_futility else None
        self.lmr = LateMoveReduction() if enable_lmr else None
        self.multi_cut = MultiCutPruning() if enable_multi_cut else None

        # Extract killer and history from orderer for updates
        self.killer_orderer = None
        self.history_orderer = None
        for orderer_component in orderer.orderers:
            if isinstance(orderer_component, KillerMoveOrderer):
                self.killer_orderer = orderer_component
            elif isinstance(orderer_component, HistoryHeuristicOrderer):
                self.history_orderer = orderer_component

        # Transposition table
        self.tt = TranspositionTable()
        self.zobrist = ZobristHasher()

        # Statistics
        self.nodes = 0
        self.pruning = 0

    def search(self, context: SearchContext) -> SearchResult:
        """Search from context (not used - use get_best_move)"""
        best_move = self.get_best_move(context.game, context.depth)
        return SearchResult(
            best_move=best_move,
            value=0,  # Value not tracked in get_best_move
            nodes_searched=self.nodes,
            time_elapsed=0.0,  # Time not tracked in get_best_move
        )

    def get_best_move(self, game, depth: int, **kwargs):
        """
        Get best move with full alpha-beta search.

        Args:
            game: BitboardGame instance
            depth: Search depth
            **kwargs: Additional parameters (ignored)

        Returns:
            Best move found
        """
        self.nodes = 0
        self.pruning = 0

        move_list = game.get_move_list()
        if not move_list:
            return None

        # Order moves
        ordered_moves = self.orderer.order_moves(game, move_list)

        # Search each move and collect values
        moves_with_values = []
        best_move = None
        best_value = -INFINITY
        alpha = -INFINITY
        beta = INFINITY

        for move in ordered_moves:
            game.move(move)
            value = -self.alphabeta(game, depth - 1, -beta, -alpha, allow_null_move=True)
            game.undo_move()

            moves_with_values.append((move, value))

            if value > best_value or best_move is None:
                best_value = value
                best_move = move

            if value > alpha:
                alpha = value

        # Apply temperature-based selection if enabled
        if self.temperature > 0.0:
            from AI.Apocalyptron.randomization import apply_temperature_selection

            # Sort moves by value descending
            moves_with_values.sort(key=lambda x: x[1], reverse=True)
            # Convert values to float for type compatibility
            moves_with_float_values = [(move, float(value)) for move, value in moves_with_values]
            best_move = apply_temperature_selection(moves_with_float_values, self.temperature)

        return best_move

    def alphabeta(
        self, game, depth: int, alpha: int, beta: int, allow_null_move: bool = True
    ) -> int:
        """
        Alpha-beta search with all optimizations.

        This is the complete implementation extracted from GrandmasterEngine.

        Args:
            game: Current game state
            depth: Remaining depth
            alpha: Alpha bound
            beta: Beta bound
            allow_null_move: Whether null move is allowed

        Returns:
            int: Position evaluation
        """
        self.nodes += 1

        # Transposition table lookup
        pos_hash = self.zobrist.hash_position(game)
        entry = self.tt.lookup(pos_hash)

        if entry and entry.is_usable(depth):
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

        # FUTILITY PRUNING (at frontier nodes - depth 1-3)
        if self.futility and depth <= 3 and depth > 0 and len(move_list) > 0:
            can_prune, cutoff_value = self.futility.can_prune_futile(
                game, depth, alpha, beta, move_list
            )
            if can_prune and cutoff_value is not None:
                return cutoff_value

        # NULL MOVE PRUNING
        if self.null_move and len(move_list) > 0:
            can_attempt = self.null_move.can_attempt_null_move(
                game, depth, alpha, beta, allow_null_move, move_list
            )

            if can_attempt:
                self.null_move.record_attempt()

                # Make null move
                game.pass_turn()

                # Reduced depth search
                R = 2
                null_score = -self.alphabeta(
                    game, depth - R - 1, -beta, -beta + 1, allow_null_move=False
                )

                # Undo null move
                game.undo_move()

                # Check for cutoff
                if null_score >= beta:
                    self.null_move.record_cutoff()
                    return beta

        # Handle pass
        if len(move_list) == 0:
            game.pass_turn()
            value = -self.alphabeta(game, depth - 1, -beta, -alpha, allow_null_move=False)
            game.undo_move()
            return value

        # ORDER MOVES
        ordered_moves = self.orderer.order_moves(game, move_list)

        # Search moves
        best_value = -INFINITY
        original_alpha = alpha
        cutoff_count = 0

        for move_index, move in enumerate(ordered_moves):
            game.move(move)

            # LATE MOVE REDUCTION
            reduction = 0
            do_full_search = True

            if self.lmr:
                reduction = self.lmr.should_reduce(move_index, depth, best_value)

                if reduction > 0:
                    # Try reduced depth first
                    value = -self.alphabeta(
                        game, depth - 1 - reduction, -beta, -alpha, allow_null_move=True
                    )

                    # If move looks good, re-search at full depth
                    if value > alpha:
                        self.lmr.record_re_search()
                        do_full_search = True
                    else:
                        do_full_search = False

            # Full depth search
            if do_full_search:
                value = -self.alphabeta(game, depth - 1, -beta, -alpha, allow_null_move=True)

            game.undo_move()

            if value > best_value:
                best_value = value

            if value > alpha:
                alpha = value

            if alpha >= beta:
                # Beta cutoff!
                self.pruning += 1
                cutoff_count += 1

                # Update killer moves
                if self.killer_orderer:
                    self.killer_orderer.add_killer(move, depth)

                # Update history heuristic
                if self.history_orderer:
                    self.history_orderer.update_history(move, depth)

                # MULTI-CUT PRUNING
                if self.multi_cut and self.multi_cut.should_multi_cut(
                    cutoff_count, move_index, depth
                ):
                    self.tt.store(pos_hash, depth, beta, "lower", move)
                    return beta

                self.tt.store(pos_hash, depth, beta, "lower", move)
                return beta

        # Store in transposition table
        if best_value <= original_alpha:
            self.tt.store(pos_hash, depth, best_value, "upper")
        elif best_value >= beta:
            self.tt.store(pos_hash, depth, best_value, "lower")
        else:
            self.tt.store(pos_hash, depth, best_value, "exact")

        return best_value

    def get_statistics(self) -> Dict[str, Any]:
        """Get search statistics"""
        stats: Dict[str, Any] = {
            "nodes": self.nodes,
            "pruning": self.pruning,
            "tt_hits": self.tt.hits,
            "tt_size": self.tt.size(),
        }

        if self.null_move:
            stats["null_move"] = self.null_move.get_statistics()
        if self.futility:
            stats["futility"] = self.futility.get_statistics()
        if self.lmr:
            stats["lmr"] = self.lmr.get_statistics()
        if self.multi_cut:
            stats["multi_cut"] = self.multi_cut.get_statistics()

        if self.history_orderer:
            stats["history_entries"] = len(self.history_orderer.history_table)

        if self.killer_orderer:
            # Count total killer moves stored
            killer_count = sum(
                1
                for depth_killers in self.killer_orderer.killer_moves.values()
                for k in depth_killers
                if k is not None
            )
            stats["killer_moves"] = killer_count

        return stats

    def reset(self):
        """Reset search state"""
        self.nodes = 0
        self.pruning = 0
        self.tt.clear()

        if self.killer_orderer:
            self.killer_orderer.clear()
        if self.history_orderer:
            self.history_orderer.clear()

        if self.null_move:
            self.null_move.reset_statistics()
        if self.futility:
            self.futility.reset_statistics()
        if self.lmr:
            self.lmr.reset_statistics()
        if self.multi_cut:
            self.multi_cut.reset_statistics()
