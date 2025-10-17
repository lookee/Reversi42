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

class StandardEvaluator(Evaluator):
    """
    Standard evaluation function for Reversi.
    
    In opening/midgame: focuses on mobility and corner control.
    In endgame: maximizes piece count.
    """
    
    def __init__(self):
        super().__init__("StandardEvaluator")
    
    def evaluate(self, game):
        """
        Evaluate position using standard Reversi heuristics.
        
        Opening/Midgame strategy:
        - Maximize mobility (number of available moves)
        - Evaluate corner control and adjacency penalties
        
        Endgame strategy:
        - Maximize piece count
        """
        
        # Determine game phase
        occupied_cells = game.white_cnt + game.black_cnt
        total_cells = game.cells_cnt
        endgame_threshold = total_cells * 0.7
        
        if occupied_cells < endgame_threshold:
            # Opening and midgame: maximize mobility, eval corners
            return self._evaluate_midgame(game)
        else:
            # Endgame: maximize the number of pieces
            return self._evaluate_endgame(game)
    
    def _evaluate_midgame(self, game):
        """Evaluate position in opening/midgame"""
        
        # Start with mobility score
        out = len(game.get_move_list())
        
        # Evaluate corners and adjacent positions
        for x in game.corner:
            for y in game.corner:
                xx, dx = x
                yy, dy = y
                
                # Check if the corner is free
                if game.matrix[yy][xx] == '.':
                    # Penalty for occupying positions adjacent to free corners
                    # (they give opponent a chance to take the corner)
                    
                    # Check position adjacent to corner on x-axis
                    if game.matrix[yy][dx] != '.':
                        if game.matrix[yy][dx] == game.turn:
                            out -= 3  # penalty for our piece
                        else:
                            out += 3  # bonus if opponent has the risky piece
                    
                    # Check position adjacent to corner on y-axis
                    if game.matrix[dy][xx] != '.':
                        if game.matrix[dy][xx] == game.turn:
                            out -= 3  # penalty for our piece
                        else:
                            out += 3  # bonus if opponent has the risky piece
                    
                    # Check diagonal position (most dangerous)
                    if game.matrix[dy][dx] != '.':
                        if game.matrix[dy][dx] == game.turn:
                            out -= 7  # higher penalty for diagonal
                        else:
                            out += 7  # higher bonus if opponent is there
                
                # Check if we own the corner (very valuable)
                elif game.matrix[yy][xx] == game.turn:
                    out += 10  # large bonus for owning a corner
                else:
                    out -= 10  # large penalty if opponent owns corner
        
        return out
    
    def _evaluate_endgame(self, game):
        """Evaluate position in endgame by piece count"""
        
        if game.turn == 'W':
            return game.white_cnt - game.black_cnt
        else:
            return game.black_cnt - game.white_cnt

