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

import abc

class Evaluator(abc.ABC):
    """Abstract base class for position evaluation strategies"""
    
    def __init__(self, name="Evaluator"):
        self.name = name
    
    def get_name(self):
        return self.name
    
    @abc.abstractmethod
    def evaluate(self, game):
        """
        Evaluate a game position from the perspective of the current player.
        
        Args:
            game: Game instance to evaluate
            
        Returns:
            int: Evaluation score (positive is better for current player)
        """
        pass

