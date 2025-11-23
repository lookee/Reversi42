"""
Iterative Deepening Search Strategy.

Wrapper around IterativeDeepeningSearch to implement SearchStrategy interface.
Provides backward compatibility while enabling strategy pattern.
"""

from typing import List, Optional

from AI.Apocalyptron.observers.interfaces import SearchObserver
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
from AI.Apocalyptron.search.strategy_interface import SearchStrategy


class IterativeDeepeningStrategy(SearchStrategy):
    """
    Iterative deepening strategy - progressive depth 1→N.

    Wraps existing IterativeDeepeningSearch to provide SearchStrategy interface.
    Maintains backward compatibility with existing code.

    Advantages:
    - Time management (can stop at any depth)
    - Better move ordering from shallow searches
    - Aspiration window optimization
    - Progressive refinement

    This is the DEFAULT strategy (same behavior as before refactoring).
    """

    def __init__(
        self,
        alphabeta: AlphaBetaSearchComplete,
        use_aspiration: bool = True,
        observers: Optional[List[SearchObserver]] = None,
    ):
        """
        Initialize iterative deepening strategy.

        Args:
            alphabeta: AlphaBetaSearchComplete instance
            use_aspiration: Whether to use aspiration windows
            observers: List of SearchObserver instances
        """
        # Delegate to existing IterativeDeepeningSearch implementation
        self.search = IterativeDeepeningSearch(
            alphabeta=alphabeta, use_aspiration=use_aspiration, observers=observers
        )
        self.alphabeta = alphabeta

    def get_best_move(
        self,
        game,
        depth: int,
        player_name: Optional[str] = None,
        opening_book=None,
        game_history: Optional[str] = None,
    ):
        """
        Get best move using iterative deepening (1→depth).

        Delegates to existing IterativeDeepeningSearch implementation.

        Args:
            game: BitboardGame instance
            depth: Target search depth (searches 1→depth progressively)
            player_name: Player name for display
            opening_book: Opening book instance
            game_history: Game history string

        Returns:
            Best move found
        """
        # Direct delegation to existing implementation
        return self.search.get_best_move(game, depth, player_name, opening_book, game_history)

    def reset(self):
        """Reset search state"""
        self.search.reset()

    @property
    def aspiration_hits(self):
        """Get aspiration window hits (for statistics)"""
        return self.search.aspiration_hits

    @property
    def aspiration_fails(self):
        """Get aspiration window failures (for statistics)"""
        return self.search.aspiration_fails

    @property
    def observers(self):
        """Get observers list (for ParallelSearch compatibility)"""
        return self.search.observers

    @observers.setter
    def observers(self, value: List[SearchObserver]):
        """Set observers list (for ParallelSearch compatibility)"""
        self.search.observers = value

    def add_observer(self, observer: SearchObserver):
        """Add an observer dynamically"""
        if observer and observer not in self.search.observers:
            self.search.observers.append(observer)

    def remove_observer(self, observer: SearchObserver):
        """Remove an observer"""
        if observer and observer in self.search.observers:
            self.search.observers.remove(observer)
