
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

import pygame
from pygame.locals import *

from Board.BoardView import BoardView
from Board.BoardModel import BoardModel

class BoardControl(object):

    def __init__(self, sizex, sizey):

        self.sizex = sizex
        self.sizey = sizey
        self.view = BoardView(sizex,sizey,800,600)
        self.model = BoardModel(sizex,sizey)

        self.keyPressed = False
        self.cursor_mode = False  # Whether we're in cursor navigation mode
        self.should_exit = False  # Flag to signal exit
        
        # Initialize cursor to center of board
        self.view.setCursor(sizex // 2, sizey // 2)

    def action(self):
        """Non-blocking action method that processes events once"""
        self.waitInput = True
        # Don't reset bx, by here - they might have been set by ENTER/SPACE
        
        # Process all pending events
        for event in pygame.event.get():
            self.handleEvent(event)
    
    def check_events(self):
        """Check for events without setting waitInput - used during AI turns"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.should_exit = True
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.should_exit = True

    def handleEvent(self, event):

        if event.type == QUIT:
            self.triggerEnd()

        if event.type == MOUSEBUTTONDOWN:
            self.handleMouseButtonEvents(event)

        if event.type == KEYUP:
            self.keyPressed = False

        if event.type == KEYDOWN and not self.keyPressed:
            self.keyPressed = True
            self.handleKeyEvents(event)

    def handleKeyEvents(self, event):

        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            self.should_exit = True
            self.waitInput = False
        elif event.key == pygame.K_c:
            # Toggle cursor mode
            self.cursor_mode = not self.cursor_mode
            if self.cursor_mode:
                # Set cursor to center of board
                self.view.setCursor(self.sizex // 2, self.sizey // 2)
            # Redraw board to show/hide cursor
            self.redrawBoard()
        elif self.cursor_mode:
            # Handle cursor navigation
            if event.key == pygame.K_UP:
                self.view.moveCursor(0, -1)
                self.redrawBoard()  # Redraw to clear old cursor
            elif event.key == pygame.K_DOWN:
                self.view.moveCursor(0, 1)
                self.redrawBoard()  # Redraw to clear old cursor
            elif event.key == pygame.K_LEFT:
                self.view.moveCursor(-1, 0)
                self.redrawBoard()  # Redraw to clear old cursor
            elif event.key == pygame.K_RIGHT:
                self.view.moveCursor(1, 0)
                self.redrawBoard()  # Redraw to clear old cursor
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Select current cursor position
                self.bx, self.by = self.view.getCursorPosition()
                # Don't set waitInput = False here, let HumanPlayer handle validation

    def triggerEnd(self):
        self.should_exit = True
        self.waitInput = False

    def handleMouseButtonEvents(self, event):

        (x,y) = event.pos
        (bx,by) = self.view.point2Box(x,y)

        #print "(x: %d, y: %d) -> (bx: %d, by: %d)" %(x,y,bx,by)

        if bx in range(self.sizex) and by in range(self.sizey):

            if event.button == 1:
                self.waitInput = False;
                self.bx = bx
                self.by = by
                # Update cursor position when clicking
                self.view.setCursor(bx, by)

    def renderModel(self):

        for x in range(self.sizex):
            for y in range(self.sizey):
                cell = self.model.getPoint(x,y)
                if cell == 'W':
                    self.view.setBoxWhite(x,y)
                elif cell == 'B':
                    self.view.setBoxBlack(x,y)
                elif cell == 'w':
                    self.view.setCanMoveWhite(x,y)
                elif cell == 'b':
                    self.view.setCanMoveBlack(x,y)
                else:
                    self.view.unsetBox(x,y)

        self.view.update(self.cursor_mode)

    def importModel(self,model):
        for y in range(self.sizey):
            for x in range(self.sizex):
                value = model[y*self.sizey+x] 
                if value == 'W' or value == 'B':
                    self.model.setPoint(x,y,value)
                else:
                    self.model.unsetPoint(x,y)
                    self.model.setPoint(x,y,value)

    def setCanMove(self, bx, by, turn):
        self.model.setPoint(bx-1,by-1, turn.lower())

    def setLastMove(self, bx, by):
        """Set the last move position for red dot indicator"""
        self.view.setLastMove(bx-1, by-1)  # Convert from 1-indexed to 0-indexed

    def cursorHand(self):
        self.view.cursorHand()

    def cursorWait(self):
        self.view.cursorWait()
    
    def redrawBoard(self):
        """Redraw the board to clear old cursor and redraw current state"""
        # Redraw the model (pieces and possible moves)
        self.renderModel()
    
    def resetSelection(self):
        """Reset the current move selection"""
        self.bx = self.by = None
