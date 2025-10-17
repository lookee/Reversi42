#!/usr/bin/env python3

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

from AI.Evaluator import Evaluator

class AdvancedEvaluator(Evaluator):
    """
    Advanced evaluation function with weighted position values.
    Uses a position weight matrix similar to the one used for move ordering.
    """
    
    def __init__(self):
        super().__init__("AdvancedEvaluator")
        
        # Position weight matrix (corners are most valuable)
        self.position_weights = [ 
            [ 0,  0,  0,  0,  0,  0,  0,  0,  0 ],
            [ 0, 20, -3,  3,  2,  2,  3, -3, 20 ], 
            [ 0, -3, -5, -1, -1, -1, -1, -5, -3 ], 
            [ 0,  3, -1,  1,  0,  0,  1, -1,  3 ], 
            [ 0,  2, -1,  0,  0,  0,  0, -1,  2 ], 
            [ 0,  2, -1,  0,  0,  0,  0, -1,  2 ], 
            [ 0,  3, -1,  1,  0,  0,  1, -1,  3 ], 
            [ 0, -3, -5, -1, -1, -1, -1, -5, -3 ], 
            [ 0, 20, -3,  3,  2,  2,  3, -3, 20 ], 
        ]
    
    def evaluate(self, game):
        """
        Evaluate position using multiple factors:
        - Position weights (corners, edges, etc.)
        - Mobility (number of available moves)
        - Piece count in endgame
        """
        
        # Determine game phase
        occupied_cells = game.white_cnt + game.black_cnt
        total_cells = game.cells_cnt
        
        # Calculate weights based on game phase
        if occupied_cells < total_cells * 0.5:
            # Early game: focus heavily on position and mobility
            position_weight = 2.0
            mobility_weight = 1.5
            piece_weight = 0.0
        elif occupied_cells < total_cells * 0.75:
            # Mid game: balance position, mobility, and pieces
            position_weight = 1.5
            mobility_weight = 1.0
            piece_weight = 0.5
        else:
            # End game: focus on piece count
            position_weight = 0.5
            mobility_weight = 0.5
            piece_weight = 2.0
        
        score = 0.0
        
        # Evaluate position weights
        position_score = self._evaluate_positions(game)
        score += position_score * position_weight
        
        # Evaluate mobility
        mobility_score = len(game.get_move_list())
        score += mobility_score * mobility_weight
        
        # Evaluate piece count
        if game.turn == 'W':
            piece_score = game.white_cnt - game.black_cnt
        else:
            piece_score = game.black_cnt - game.white_cnt
        score += piece_score * piece_weight
        
        return int(score)
    
    def _evaluate_positions(self, game):
        """Evaluate board positions using weight matrix"""
        
        score = 0
        
        for y in range(1, game.size + 1):
            for x in range(1, game.size + 1):
                cell = game.matrix[y][x]
                if cell != '.':
                    weight = self.position_weights[y][x]
                    if cell == game.turn:
                        score += weight
                    else:
                        score -= weight
        
        return score

