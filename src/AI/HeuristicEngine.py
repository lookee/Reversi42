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

from AI.GameEngine import GameEngine
from Reversi.Game import Game
from Reversi.Game import Move

class HeuristicEngine(GameEngine):
    """
    A heuristic-based engine that uses simple evaluation functions.
    """
    
    def __init__(self, evaluator=None):
        super().__init__("HeuristicEngine", evaluator)
        
        # Corner positions (highest priority)
        self.corners = [(1,1), (1,8), (8,1), (8,8)]
        
        # Edge positions (medium priority)
        self.edges = [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
                      (2,1), (3,1), (4,1), (5,1), (6,1), (7,1),
                      (2,8), (3,8), (4,8), (5,8), (6,8), (7,8),
                      (8,2), (8,3), (8,4), (8,5), (8,6), (8,7)]
        
        # Priority matrix for move evaluation
        self.priority = [ 
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 1, 8, 7, 6, 6, 7, 8, 1 ], 
            [ 0, 8, 9, 7, 4, 4, 7, 9, 8 ], 
            [ 0, 7, 5, 3, 2, 2, 3, 5, 7 ], 
            [ 0, 6, 4, 2, 0, 0, 2, 4, 6 ], 
            [ 0, 6, 4, 2, 0, 0, 2, 4, 6 ], 
            [ 0, 7, 5, 3, 2, 2, 3, 5, 7 ], 
            [ 0, 8, 9, 7, 4, 4, 7, 9, 8 ], 
            [ 0, 1, 8, 7, 6, 6, 7, 8, 1 ], 
        ]
    
    def get_best_move(self, game, depth, player_name=None):
        """
        Get the best move using heuristic evaluation.
        
        Args:
            game: The current game state
            depth: Search depth (ignored for heuristic engine)
            player_name: Optional name of the player for display
            
        Returns:
            Move: The best move found using heuristics
        """
        moves = game.get_move_list()
        if not moves:
            return None
        
        best_move = None
        best_score = -float('inf')
        
        for move in moves:
            score = self._evaluate_move(move, game)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _evaluate_move(self, move, game):
        """
        Evaluate a move using various heuristics.
        
        Args:
            move: The move to evaluate
            game: The current game state
            
        Returns:
            float: The score for this move
        """
        score = 0
        
        # Corner moves are extremely valuable
        if (move.x, move.y) in self.corners:
            score += 1000
        
        # Edge moves are valuable but less than corners
        elif (move.x, move.y) in self.edges:
            score += 100
        
        # Priority matrix score
        score += self.priority[move.y][move.x]
        
        # Mobility: more moves after this move is better
        game.move(move)
        mobility = len(game.get_move_list())
        game.undo_move()
        score += mobility * 10
        
        # Piece count: more pieces is generally better
        if game.get_turn() == 'B':
            score += game.black_cnt * 2
        else:
            score += game.white_cnt * 2
        
        return score
