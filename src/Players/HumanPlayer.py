
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
import pygame
from pygame.locals import *

class HumanPlayer(Player):

    def __init__(self,name='Human'):
        self.name = name

    def get_move(self, game, moves, control):
        control.cursorHand()
        control.waitInput = True
        control.resetSelection()  # Reset any previous selection
        
        clock = pygame.time.Clock()
        
        while control.waitInput and not control.should_exit and not control.should_pause:
            # Process events
            control.action()
            
            # Check if user wants to pause or exit
            if control.should_pause or control.should_exit:
                return None
            
            # Check if we have a move
            if control.bx is not None and control.by is not None:
                x = control.bx + 1
                y = control.by + 1
                move = Move(x, y)
                print("move: %s" % move)
                
                if game.valid_move(move):
                    control.waitInput = False
                    return move
                else:
                    print("This move is not valid!")
                    control.bx = control.by = None  # Reset for next attempt
            
            # Update display
            control.view.update(control.cursor_mode)
            clock.tick(60)  # Limit to 60 FPS
        
        return None
