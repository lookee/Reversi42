"""
Composite move orderer.

Combines multiple ordering strategies by summing their scores.
Implements Composite Pattern for flexible move ordering.
"""

from typing import Any, List, Tuple

from AI.Apocalyptron.ordering.interfaces import MoveOrderer


class CompositeOrderer(MoveOrderer):
    """
    Composite orderer that combines multiple ordering strategies.

    Each orderer contributes a score, and the final score is the sum.

    Typical combination:
    1. PVMoveOrderer (score: 10000) - PV move first
    2. KillerMoveOrderer (score: 5000) - Killer moves next
    3. HistoryHeuristicOrderer (score: 0-1000) - Historical success
    4. PositionalOrderer (score: 0-1000) - Strategic value

    This creates a natural priority:
    PV > Killers > Good history/position > Others

    Example:
        orderer = CompositeOrderer()
        orderer.add_orderer(PVMoveOrderer())
        orderer.add_orderer(KillerMoveOrderer())
        orderer.add_orderer(HistoryHeuristicOrderer())
        orderer.add_orderer(PositionalOrderer(weights))

        ordered_moves = orderer.order_moves(game, move_list)
    """

    def __init__(self):
        """Initialize empty composite orderer"""
        self.orderers: List[MoveOrderer] = []

    def add_orderer(self, orderer: MoveOrderer):
        """
        Add an orderer to the composite.

        Args:
            orderer: MoveOrderer instance to add
        """
        self.orderers.append(orderer)

    def score_moves(self, game, moves: List) -> List[Tuple[float, Any]]:
        """
        Score moves using all registered orderers.

        Args:
            game: BitboardGame instance
            moves: List of Move objects

        Returns:
            List of (total_score, move) tuples
        """
        if not moves:
            return []

        # Initialize scores to zero
        move_scores = {id(move): 0.0 for move in moves}

        # Sum scores from all orderers
        for orderer in self.orderers:
            scored = orderer.score_moves(game, moves)
            for score, move in scored:
                move_scores[id(move)] += score

        # Return as list of tuples
        return [(move_scores[id(move)], move) for move in moves]

    def get_orderer_count(self) -> int:
        """Get number of registered orderers"""
        return len(self.orderers)
