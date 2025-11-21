"""
Search context - immutable search state.

Contains all information needed for a single search node.
Immutability ensures thread safety and makes debugging easier.
"""

from dataclasses import dataclass, field, replace
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class SearchContext:
    """
    Immutable search context for a single node.

    Contains all state needed to perform search at this node:
    - Game position
    - Remaining depth
    - Alpha-beta window
    - Search parameters
    - Heuristic tables (immutable snapshots)

    Being immutable (frozen=True) means:
    - Thread-safe for parallel search
    - Easy to debug (no hidden state changes)
    - Can use with_* methods to create modified copies
    """

    # Game state
    game: Any  # BitboardGame instance

    # Search parameters
    depth: int
    alpha: int
    beta: int

    # Search control
    allow_null_move: bool = True
    ply_from_root: int = 0

    # Heuristic data (immutable snapshots)
    killer_moves: Tuple[Any, ...] = field(default_factory=tuple)
    history_table: Dict[Any, Any] = field(default_factory=dict)

    # Move list cache (to avoid recomputing)
    move_list: Optional[Tuple[Any, ...]] = field(default=None)

    def with_reduced_depth(self, reduction: int) -> "SearchContext":
        """
        Create new context with reduced depth.

        Args:
            reduction: Amount to reduce depth by

        Returns:
            New SearchContext with reduced depth
        """
        return replace(self, depth=self.depth - reduction)

    def with_alpha_beta(self, alpha: int, beta: int) -> "SearchContext":
        """
        Create new context with different alpha-beta window.

        Args:
            alpha: New alpha value
            beta: New beta value

        Returns:
            New SearchContext with updated window
        """
        return replace(self, alpha=alpha, beta=beta)

    def with_next_ply(self) -> "SearchContext":
        """
        Create new context for next ply (depth - 1, ply + 1).

        Returns:
            New SearchContext for child node
        """
        return replace(self, depth=self.depth - 1, ply_from_root=self.ply_from_root + 1)

    def with_no_null_move(self) -> "SearchContext":
        """
        Create new context with null move disabled.

        Returns:
            New SearchContext with allow_null_move=False
        """
        return replace(self, allow_null_move=False)
