#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Reversi42 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Reversi42.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

import random
from AI.GameEngine import GameEngine
from Reversi.Game import Game
from Reversi.Game import Move

class RandomEngine(GameEngine):
    """
    A simple random move engine for demonstration purposes.
    """
    
    def __init__(self, evaluator=None):
        super().__init__("RandomEngine", evaluator)
    
    def get_best_move(self, game, depth):
        """
        Get a random move from available moves.
        
        Args:
            game: The current game state
            depth: Search depth (ignored for random engine)
            
        Returns:
            Move: A random move from available moves
        """
        moves = game.get_move_list()
        if not moves:
            return None
        
        # Simple heuristic: prefer corners and edges
        corner_moves = []
        edge_moves = []
        other_moves = []
        
        for move in moves:
            if self._is_corner(move):
                corner_moves.append(move)
            elif self._is_edge(move):
                edge_moves.append(move)
            else:
                other_moves.append(move)
        
        # Prefer corners, then edges, then other moves
        if corner_moves:
            return random.choice(corner_moves)
        elif edge_moves:
            return random.choice(edge_moves)
        else:
            return random.choice(other_moves)
    
    def _is_corner(self, move):
        """Check if move is in a corner."""
        corners = [(1,1), (1,8), (8,1), (8,8)]
        return (move.x, move.y) in corners
    
    def _is_edge(self, move):
        """Check if move is on an edge."""
        return (move.x == 1 or move.x == 8 or move.y == 1 or move.y == 8)
