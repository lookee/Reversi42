"""
Interfaces for move ordering.

Move ordering is critical for alpha-beta efficiency.
Better move ordering = more cutoffs = faster search.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class MoveOrderer(ABC):
    """
    Abstract base class for move ordering strategies.

    Good move ordering can provide 2-3x speedup in alpha-beta search
    by causing more cutoffs earlier.
    """

    @abstractmethod
    def score_moves(self, game, moves: List) -> List[Tuple[float, Any]]:
        """
        Score moves for ordering.

        Args:
            game: BitboardGame instance
            moves: List of Move objects to score

        Returns:
            List of (score, move) tuples, higher score = better move
        """
        pass

    def order_moves(self, game, moves: List) -> List:
        """
        Order moves by score (best first).

        Args:
            game: BitboardGame instance
            moves: List of Move objects

        Returns:
            List of Move objects sorted by score (descending)
        """
        if not moves:
            return []

        scored = self.score_moves(game, moves)
        scored.sort(reverse=True, key=lambda x: x[0])
        return [move for _, move in scored]

    def get_name(self) -> str:
        """Get orderer name for debugging"""
        return self.__class__.__name__
