"""
Quiet Observer - No output.

Silent observer for testing, tournaments, or batch processing.
"""

from typing import Any, Dict, Optional

from AI.Apocalyptron.observers.interfaces import SearchObserver


class QuietObserver(SearchObserver):
    """
    Quiet observer that produces no output.

    Useful for:
    - Testing (no stdout capture needed)
    - Tournaments (no output overhead)
    - Batch processing
    - Background analysis
    """

    def on_search_start(
        self, depth: int, player_name: Optional[str], game: Any, mode: str = "sequential"
    ):
        """Silent"""
        pass

    def on_iteration_start(
        self,
        current_depth: int,
        target_depth: int,
        use_aspiration: bool = False,
        alpha: int = 0,
        beta: int = 0,
    ):
        """Silent"""
        pass

    def on_move_evaluated(
        self, move: Any, value: int, is_best: bool, nodes: int, pruning: int, elapsed_time: float
    ):
        """Silent"""
        pass

    def on_iteration_complete(
        self,
        depth: int,
        best_move: Any,
        value: int,
        iteration_time: float,
        aspiration_success: bool = True,
    ):
        """Silent"""
        pass

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
        """Silent"""
        pass

    def on_parallel_phase_start(self, depth: int, num_workers: int):
        """Silent"""
        pass

    def on_parallel_result(self, move: Any, value: int, is_best: bool, nodes: int, pruning: int):
        """Silent"""
        pass

    def on_phase1_complete(
        self,
        stats: Dict,
        time_elapsed: float,
        final_depth: int,
        target_depth: int,
        best_move: Any = None,
        best_value: int = 0,
    ):
        """Silent"""
        pass
