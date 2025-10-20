"""
Interfaces for pruning strategies.

Pruning strategies decide when to cut off search early.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class PruningResult:
    """
    Result of a pruning decision.

    Attributes:
        should_prune: Whether to prune this branch
        cutoff_value: Value to return if pruning (None if not pruning)
        reason: Description of why pruning occurred (for debugging)
    """

    should_prune: bool
    cutoff_value: Optional[int] = None
    reason: str = ""


class PruningStrategy(ABC):
    """
    Abstract base class for pruning strategies.

    Pruning strategies decide when to stop searching a branch early,
    saving time without losing accuracy (or with acceptable accuracy loss).

    Different strategies:
    - Null move pruning: If giving opponent free move still wins, prune
    - Futility pruning: If position is hopeless, don't search further
    - Late move reduction: Search bad moves at reduced depth
    - Multi-cut pruning: If many moves cause cutoff, position is winning
    """

    @abstractmethod
    def should_prune(self, context) -> PruningResult:
        """
        Decide whether to prune this search node.

        Args:
            context: SearchContext with all search state

        Returns:
            PruningResult with decision and optional cutoff value
        """
        pass

    @abstractmethod
    def get_statistics(self) -> dict:
        """
        Get statistics about this pruning strategy.

        Returns:
            dict: Statistics (attempts, successes, etc.)
        """
        pass

    def reset_statistics(self):
        """Reset statistics counters"""
        pass

    def get_name(self) -> str:
        """Get strategy name for debugging"""
        return self.__class__.__name__
