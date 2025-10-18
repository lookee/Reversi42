
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

from Reversi.Game import Game
from Reversi.Game import Move
from AI.MinimaxEngine import MinimaxEngine
from Players.Player import Player

class AIPlayer(Player):
    
    PLAYER_METADATA = {
        'display_name': 'Alpha-Beta AI',
        'description': 'Classic minimax with alpha-beta pruning - solid and reliable',
        'enabled': True,
        'parameters': [
            {
                'name': 'difficulty',
                'display_name': 'Difficulty Level',
                'type': 'int',
                'min': 1,
                'max': 10,
                'default': 6,
                'description': 'Search depth (higher = stronger but slower)'
            }
        ]
    }

    def __init__(self, deep=6):
        self.depth = deep
        self.deep = deep  # Keep for backwards compatibility
        self.name = f'AlphaBeta{deep}'
        self.engine = MinimaxEngine()

    def get_move(self, game, moves, control):

        move = self.engine.get_best_move(game, self.deep, player_name=self.name)

        return move
