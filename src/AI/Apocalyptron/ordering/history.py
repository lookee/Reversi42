"""
History heuristic ordering.

Tracks globally successful moves across all depths and positions.
Moves that caused many cutoffs get higher scores.
"""

from AI.Apocalyptron.ordering.interfaces import MoveOrderer


class HistoryHeuristicOrderer(MoveOrderer):
    """
    Orders moves based on history heuristic.
    
    The history table tracks how often each move has caused
    a beta cutoff throughout the entire search tree.
    
    Moves that caused more cutoffs (especially at deeper levels)
    get higher priority.
    
    Score is increased by depth² when a move causes a cutoff,
    so deeper cutoffs count more.
    
    Extracted from GrandmasterEngine (history_table usage).
    """
    
    def __init__(self):
        """Initialize history table"""
        self.history_table = {}  # {(x, y): score}
    
    def score_moves(self, game, moves: list) -> list[tuple[float, any]]:
        """
        Score moves based on historical success.
        
        Args:
            game: BitboardGame instance
            moves: List of Move objects
            
        Returns:
            List of (score, move) tuples
        """
        scored_moves = []
        
        for move in moves:
            # Get move coordinates
            if isinstance(move, str):
                col = ord(move[0].upper()) - ord('A')
                row = int(move[1]) - 1
                move_key = (col, row)
            else:
                move_key = (move.x - 1, move.y - 1)
            
            # Get historical score
            score = self.history_table.get(move_key, 0)
            
            scored_moves.append((score, move))
        
        return scored_moves
    
    def update_history(self, move, depth: int):
        """
        Update history score for a move that caused cutoff.
        
        Args:
            move: Move that caused cutoff
            depth: Depth at which cutoff occurred (deeper = more valuable)
        """
        # Get move coordinates
        if isinstance(move, str):
            col = ord(move[0].upper()) - ord('A')
            row = int(move[1]) - 1
            move_key = (col, row)
        else:
            move_key = (move.x - 1, move.y - 1)
        
        # Initialize if not present
        if move_key not in self.history_table:
            self.history_table[move_key] = 0
        
        # Increase score by depth squared (deeper cutoffs = more valuable)
        self.history_table[move_key] += depth * depth
    
    def clear(self):
        """Clear history table (for new search)"""
        self.history_table.clear()

