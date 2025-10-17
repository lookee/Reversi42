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

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI.Evaluator import Evaluator

class GreedyEvaluator(Evaluator):
    """
    Greedy evaluation function that only considers piece count.
    
    This evaluator always favors having more pieces on the board,
    regardless of position quality or strategic considerations.
    It's a short-sighted strategy that can be effective against
    beginners but weak against more sophisticated players.
    """
    
    def __init__(self):
        super().__init__("GreedyEvaluator")
    
    def evaluate(self, game):
        """
        Evaluate position by piece count difference only.
        
        This is the simplest possible evaluation: just count pieces
        and maximize our count. No positional considerations at all.
        
        Args:
            game: Game instance to evaluate
            
        Returns:
            int: Difference in piece count (positive favors current player)
        """
        
        if game.turn == 'W':
            return game.white_cnt - game.black_cnt
        else:
            return game.black_cnt - game.white_cnt

