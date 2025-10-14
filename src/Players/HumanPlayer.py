
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
from Players.Player import Player

import random

class HumanPlayer(Player):

    def __init__(self,name='Human'):
        self.name = name

    def get_move(self, game, moves, control):

        while 1:

            control.cursorHand()
            control.action()
            
            x = control.bx + 1
            y = control.by + 1

            move = Move(x,y)
            print("move: %s" %move)

            if game.valid_move(move):
                break
            else:
                print("This move is not valid!")

        return move
