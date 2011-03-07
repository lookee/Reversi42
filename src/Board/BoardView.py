
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
from pygame.gfxdraw import *
from sys import exit

class BoardView(object):

    def __init__(self, sizex=64, sizey=48, width=480, heigth=400):

        self.sizex = sizex
        self.sizey = sizey
        self.width = width 
        self.heigth = heigth
        self.caption = "Reversi42"

        # colors
        self.bgColor            = (  0,     102,     51)
        self.lineColor          = (255,     255,    255)
        self.boxColor           = (  0,       0,      0)
        self.shadowColor        = ( 51,      68,     51)
        self.whitePieceColor    = (255,     255,    255)
        self.blackPieceColor    = (  0,       0,      0)
        self.canMoveColor       = ( 10,     112,     61)
        self.whiteMoveColor     = ( 14,     175,     94)
        self.blackMoveColor     = (  6,      66,     36)

        self.stepx = self.width / self.sizex
        self.stepy = self.heigth / self.sizey

        self.marginx = (self.width % self.sizex)  / 2
        self.marginy = (self.heigth % self.sizey) / 2
       
        self.__init_screen()
        self.__init_grid()
        self.update()

    def cursorHand(self):
        
        #Hand Cursor (TextWidget)
        __hand_cursor_string = (
        "     XX         ",
        "    X..X        ",
        "    X..X        ",
        "    X..X        ",
        "    X..XXXXX    ",
        "    X..X..X.XX  ",
        " XX X..X..X.X.X ",
        "X..XX.........X ",
        "X...X.........X ",
        " X.....X.X.X..X ",
        "  X....X.X.X..X ",
        "  X....X.X.X.X  ",
        "   X...X.X.X.X  ",
        "    X.......X   ",
        "     X....X.X   ",
        "     XXXXX XX   ")
        __hcurs, __hmask = pygame.cursors.compile(__hand_cursor_string
        , ".", "X")
        self.__hand = ((16, 16), (5, 1), __hcurs, __hmask)
        pygame.mouse.set_cursor(*self.__hand)

    def cursorWait(self):
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        #pygame.mouse.set_cursor(*pygame.cursors.diamond)
        #pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def __init_screen(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width,self.heigth), 0, 32)
        pygame.display.set_caption(self.caption)

        self.screen.fill(self.bgColor)

    def __init_grid(self):
        
        screen = self.screen

        for n in range(0,self.sizex + 1):

            # grid: vertical lines
	        start = (self.stepx * n + self.marginx, 0 + self.marginy)
	        end   = (self.stepx * n + self.marginx, self.sizey * self.stepy + self.marginy)
	        pygame.draw.lines(screen, self.lineColor, False, [start, end], 1)

        for n in range(0,self.sizey + 1):

            # grid: horizontal lines
	        start = (0 + self.marginx, self.stepy * n + self.marginy)
	        end   = (self.sizex * self.stepx + self.marginx, self.stepy * n + self.marginy)
	        pygame.draw.lines(screen, self.lineColor, False, [start, end], 1)

    def update(self):
        pygame.display.update()

    def unfillBox(self, bx, by):

        rect = Rect(self.stepx * bx + 2 + self.marginx, self.stepy * by + 2 + self.marginy, self.stepx - 3, self.stepy - 3)
        self.screen.fill(self.bgColor,rect)     

    def fillBox(self, bx, by, color, shadow=True):

        radius = (self.stepy-10) / 2
        posx = self.marginx + self.stepx * bx + self.stepx /2 
        posy = self.marginy + self.stepy * by + self.stepy /2

        self.unfillBox(bx, by)

        # antialiased filled circle shadow
        if shadow:
            pygame.gfxdraw.aacircle(self.screen, posx+2 ,posy+1, radius, self.shadowColor)
            pygame.gfxdraw.filled_circle(self.screen, posx+2 ,posy+1, radius, self.shadowColor)

        # antialiased filled circle
        pygame.gfxdraw.aacircle(self.screen, posx ,posy, radius, color)
        pygame.gfxdraw.filled_circle(self.screen, posx ,posy, radius, color)

    def setBox(self, bx, by, color, shadow=False):
        self.fillBox(bx, by, color, shadow)

    def setBoxWhite(self, bx, by):
        self.setBox(bx, by, self.whitePieceColor, True)

    def setBoxBlack(self, bx, by):
        self.setBox(bx, by, self.blackPieceColor, True)

    def setCanMove(self, bx, by):
        self.setBox(bx, by, self.canMoveColor, False)

    def setCanMoveBlack(self, bx, by):
        self.setBox(bx, by, self.blackMoveColor, False)

    def setCanMoveWhite(self, bx, by):
        self.setBox(bx, by, self.whiteMoveColor, False)

    def unsetBox(self, bx, by):
        self.unfillBox(bx, by)

    def setPoint(self, x, y, color):
        (bx, by) = self.point2Box(x, y)
        self.setBox(bx,by)

    def setPointBlack(self, x, y, color):
        self.setPoint(self, x, y, self.blackPieceColor)

    def setPointWhite(x, y, color):
        self.setPoint(self. x, y, self.whitePieceColor)

    def unsetPoint(x, y):
        (bx, by) = self.point2Box(x, y)
        self.unsetBox(bx,by)
    
    def point2Box(self, x, y):
        bx = (x - self.marginx) / self.stepx
        by = (y - self.marginy) / self.stepy
        return (bx, by)

