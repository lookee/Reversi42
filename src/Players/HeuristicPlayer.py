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

from Players.Player import Player
from AI.HeuristicEngine import HeuristicEngine

class HeuristicPlayer(Player):
    """
    Heuristic player that uses simple heuristics without full minimax search.
    
    This player uses the HeuristicEngine which evaluates moves based on:
    - Corner and edge priorities
    - Priority matrix scores
    - Mobility (number of moves after placement)
    - Piece count
    
    Faster than full Minimax but less sophisticated.
    Good for medium difficulty opponents.
    """
    
    PLAYER_METADATA = {
        'display_name': 'Heuristic',
        'description': 'Fast AI using simple heuristics (no deep search)',
        'enabled': True,
        'parameters': []  # No configurable parameters
    }
    
    def __init__(self, name='Heuristic'):
        self.name = name
        self.engine = HeuristicEngine()
    
    def get_move(self, game, moves, control):
        """
        Get move using heuristic evaluation.
        
        Args:
            game: Current game state
            moves: List of available moves
            control: Board control (for GUI updates, can be None)
            
        Returns:
            Move: The best move found using heuristics
        """
        # Depth parameter is ignored by HeuristicEngine
        move = self.engine.get_best_move(game, depth=1)
        return move
    
    def get_name(self):
        return self.name

