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

class SimpleEvaluator(Evaluator):
    """
    Simple evaluation function that only considers piece count.
    Good for beginners or testing purposes.
    """
    
    def __init__(self):
        super().__init__("SimpleEvaluator")
    
    def evaluate(self, game):
        """
        Evaluate position by simple piece count difference.
        
        This is a very basic evaluation that just counts pieces.
        It doesn't consider positional advantages, mobility, or corners.
        """
        
        if game.turn == 'W':
            return game.white_cnt - game.black_cnt
        else:
            return game.black_cnt - game.white_cnt

