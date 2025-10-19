"""
Killer move ordering.

Stores moves that caused beta cutoffs at each depth level.
These moves are likely to cause cutoffs in sibling positions.
"""

from typing import List, Tuple, Any
from AI.Apocalyptron.ordering.interfaces import MoveOrderer


class KillerMoveOrderer(MoveOrderer):
    """
    Orders moves based on killer move heuristic.
    
    Killer moves are moves that caused beta cutoffs at the same
    depth level in other positions. They're tried first because
    they're likely to be good in similar positions.
    
    Stores up to 2 killer moves per depth level.
    
    Extracted from GrandmasterEngine (killer_moves usage).
    """
    
    MAX_KILLERS_PER_DEPTH = 2
    KILLER_MOVE_SCORE = 5000  # High priority (after PV, before others)
    
    def __init__(self):
        """Initialize killer move storage"""
        self.killer_moves = {}  # {depth: [move1, move2]}
        self.current_depth = 0
    
    def set_depth(self, depth: int):
        """Set current search depth for killer move lookup"""
        self.current_depth = depth
    
    def add_killer(self, move, depth: int):
        """
        Add a killer move for this depth.
        
        Args:
            move: Move that caused cutoff
            depth: Depth level where cutoff occurred
        """
        if depth not in self.killer_moves:
            self.killer_moves[depth] = []
        
        # Don't add duplicates
        if move not in self.killer_moves[depth]:
            self.killer_moves[depth].insert(0, move)
            
            # Keep only MAX_KILLERS_PER_DEPTH most recent
            if len(self.killer_moves[depth]) > self.MAX_KILLERS_PER_DEPTH:
                self.killer_moves[depth].pop()
    
    def score_moves(self, game, moves: List) -> List[Tuple[float, Any]]:
        """
        Score moves - high score for killer moves.
        
        Args:
            game: BitboardGame instance
            moves: List of Move objects
            
        Returns:
            List of (score, move) tuples
        """
        scored_moves = []
        
        # Get killers for current depth
        killers = self.killer_moves.get(self.current_depth, [])
        
        for move in moves:
            score = 0
            
            # Check if this is a killer move
            if move in killers:
                score = self.KILLER_MOVE_SCORE
            
            scored_moves.append((score, move))
        
        return scored_moves
    
    def clear(self):
        """Clear all killer moves (for new search)"""
        self.killer_moves.clear()

