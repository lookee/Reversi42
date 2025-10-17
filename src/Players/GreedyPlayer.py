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
from Reversi.Game import Move

class GreedyPlayer(Player):
    """
    Greedy player that always chooses the move that captures 
    the maximum number of pieces immediately.
    
    This is a simple, short-sighted strategy that doesn't consider
    long-term positional advantages or mobility. It's useful for
    testing and as a baseline opponent.
    """
    
    def __init__(self, name='Greedy'):
        self.name = name
    
    def get_move(self, game, moves, control):
        """
        Select the move that flips the most opponent pieces.
        
        Args:
            game: Current game state
            moves: List of available moves
            control: Board control (for GUI updates, can be None)
            
        Returns:
            Move: The move that captures the most pieces
        """
        if not moves:
            return None
        
        best_move = None
        max_flips = -1
        
        current_turn = game.get_turn()
        
        # Evaluate each move
        for move in moves:
            # Make the move
            game.move(move)
            
            # Count how many pieces we have after this move
            if current_turn == 'B':
                piece_count = game.black_cnt
            else:
                piece_count = game.white_cnt
            
            # Undo the move
            game.undo_move()
            
            # Check if this move gives us more pieces
            if piece_count > max_flips:
                max_flips = piece_count
                best_move = move
        
        return best_move
    
    def get_name(self):
        return self.name

