"""
Search Strategy Interface - Base for all search strategies.

Provides abstraction layer for different search approaches:
- Fixed Depth: Direct search at target depth
- Iterative Deepening: Progressive depth 1→N
- Adaptive Depth: Depth varies by game phase
"""

from abc import ABC, abstractmethod
from typing import Optional


class SearchStrategy(ABC):
    """
    Abstract base class for search strategies.

    Defines the interface that all search strategies must implement.
    Allows engine to use different search approaches interchangeably.
    """

    @abstractmethod
    def get_best_move(
        self, game, depth: int, player_name: Optional[str] = None, opening_book=None, game_history: Optional[str] = None
    ):
        """
        Execute search and return best move.

        Args:
            game: BitboardGame instance
            depth: Target search depth (interpretation varies by strategy)
            player_name: Player name for observers (optional)
            opening_book: Opening book instance (optional)
            game_history: Game history string (optional)

        Returns:
            Best move found (position 0-63)
        """
        pass

    @abstractmethod
    def reset(self):
        """Reset strategy state (transposition table, statistics, etc.)"""
        pass
