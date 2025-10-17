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

from abc import ABC, abstractmethod
from Reversi.Game import Game
from Reversi.Game import Move

class GameEngine(ABC):
    """
    Abstract base class for all game engines.
    This provides a common interface for different AI strategies.
    """
    
    def __init__(self, name="GameEngine"):
        self.name = name
        self.nodes = 0
        self.pruning = 0
    
    @abstractmethod
    def get_best_move(self, game, depth):
        """
        Get the best move for the current position.
        
        Args:
            game: The current game state
            depth: Search depth
            
        Returns:
            Move: The best move found
        """
        pass
    
    def get_statistics(self):
        """
        Get engine statistics.
        
        Returns:
            dict: Statistics about the engine's performance
        """
        return {
            'name': self.name,
            'nodes': self.nodes,
            'pruning': self.pruning
        }
    
    def reset_statistics(self):
        """Reset engine statistics."""
        self.nodes = 0
        self.pruning = 0
