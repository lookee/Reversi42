
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
    
    PLAYER_METADATA = {
        'display_name': 'Human',
        'description': 'Interactive player using mouse/keyboard',
        'enabled': True,
        'parameters': []  # No configurable parameters
    }

    def __init__(self, name='Human'):
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
            
            # Handle opening book info display with fixed position
            current_opening_info = None
            
            if control.show_opening and control.opening_book:
                # Determine which move is being hovered (mouse or cursor)
                if control.cursor_mode:
                    cursor_x, cursor_y = control.view.cursorX, control.view.cursorY
                    if cursor_x is not None and cursor_y is not None:
                        cursor_move = Move(cursor_x + 1, cursor_y + 1)
                        if cursor_move in moves:
                            current_opening_info = control.opening_book.get_openings_for_move(game.history, cursor_move)
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    bx, by = control.view.point2Box(mouse_pos[0], mouse_pos[1])
                    if bx is not None and by is not None and bx in range(control.sizex) and by in range(control.sizey):
                        hover_move = Move(bx + 1, by + 1)
                        if hover_move in moves:
                            current_opening_info = control.opening_book.get_openings_for_move(game.history, hover_move)
            
            # Initialize last_opening_info if not exists
            if not hasattr(control, 'last_opening_info'):
                control.last_opening_info = None
            
            # Check if opening info changed (including None -> something or something -> None)
            info_changed = (current_opening_info != control.last_opening_info)
            
            if info_changed:
                # Tooltip changed - clear old tooltip area first
                control.view.clear_tooltip_area()
                
                # Redraw entire board to ensure clean state
                control.renderModel()
                
                # Now draw tooltip in fixed position if we have opening info
                if current_opening_info:
                    control.view.set_opening_info(current_opening_info)
                    control.view.draw_opening_info_fixed()
                else:
                    # Just clear, no new tooltip
                    control.view.set_opening_info(None)
                
                # Update entire display
                pygame.display.flip()
                control.last_opening_info = current_opening_info
            else:
                # Nothing changed - just normal update
                control.view.update(control.cursor_mode)
            
            clock.tick(60)  # Limit to 60 FPS
        
        return None
