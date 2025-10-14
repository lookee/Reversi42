
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
        self.view = BoardView(sizex,sizey,600,480)
        self.model = BoardModel(sizex,sizey)

        self.keyPressed = False
        #self.action()

    def action(self):

        self.waitInput = True
        self.bx = self.by = None

        while self.waitInput:
            for event in pygame.event.get():
                self.handleEvent(event)

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
            self.triggerEnd()

    def triggerEnd(self):
        exit()

    def handleMouseButtonEvents(self, event):

        (x,y) = event.pos
        (bx,by) = self.view.point2Box(x,y)

        #print "(x: %d, y: %d) -> (bx: %d, by: %d)" %(x,y,bx,by)

        if bx in range(self.sizex) and by in range(self.sizey):

            if event.button == 1:
                self.waitInput = False;
                self.bx = bx
                self.by = by

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

        self.view.update()

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

    def cursorHand(self):
        self.view.cursorHand()

    def cursorWait(self):
        self.view.cursorWait()
