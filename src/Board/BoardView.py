
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

        # colors - updated to match the reference image
        self.bgColor            = (  0,      80,      40)  # Darker green background
        self.lineColor          = (  0,       0,      0)   # Black grid lines
        self.boxColor           = (  0,       0,      0)
        self.shadowColor        = ( 40,      60,     40)
        self.whitePieceColor    = (255,     255,    255)
        self.blackPieceColor    = (  0,       0,      0)
        self.lastMoveColor      = (255,       0,      0)   # Red dot for last move
        self.hoshiColor         = (  0,       0,      0)   # Black dots for hoshi points
        self.canMoveColor       = (200,     200,    200)   # Light gray for possible moves
        self.whiteMoveColor     = (220,     220,    220)   # Light gray for white possible moves
        self.blackMoveColor     = (180,     180,    180)   # Darker gray for black possible moves

        self.stepx = self.width // self.sizex
        self.stepy = self.heigth // self.sizey

        self.marginx = (self.width % self.sizex) // 2
        self.marginy = (self.heigth % self.sizey) // 2
        
        # Track last move position for red dot indicator
        self.lastMoveX = None
        self.lastMoveY = None
       
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
            
        # Add hoshi points (reference dots) - 4 corners for 8x8 board
        # Hoshi points should be at the intersections of the 3rd and 6th lines (both horizontal and vertical)
        if self.sizex == 8 and self.sizey == 8:
            # Positions for 8x8 board: intersections of 3rd and 6th lines (0-indexed)
            hoshi_positions = [(2, 2), (5, 2), (2, 5), (5, 5)]  # (3,3), (6,3), (3,6), (6,6) in 1-indexed
            for hoshi_x, hoshi_y in hoshi_positions:
                # Position at the intersection of grid lines, not at the center of squares
                intersection_x = self.marginx + hoshi_x * self.stepx
                intersection_y = self.marginy + hoshi_y * self.stepy
                # Draw a small black circle at the intersection
                pygame.draw.circle(screen, self.hoshiColor, (intersection_x, intersection_y), 4)

    def update(self):
        # Draw last move indicator before updating display
        self.drawLastMoveIndicator()
        pygame.display.update()

    def unfillBox(self, bx, by):

        rect = Rect(self.stepx * bx + 2 + self.marginx, self.stepy * by + 2 + self.marginy, self.stepx - 3, self.stepy - 3)
        self.screen.fill(self.bgColor,rect)     

    def fillBox(self, bx, by, color, shadow=True, hollow=False):

        radius = int((self.stepy-10) // 2)
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)

        self.unfillBox(bx, by)

        if hollow:
            # Draw hollow circle for possible moves
            pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, color)
            pygame.draw.circle(self.screen, color, (posx, posy), radius, 2)
        else:
            # antialiased filled circle shadow
            if shadow:
                pygame.gfxdraw.aacircle(self.screen, int(posx+2), int(posy+1), radius, self.shadowColor)
                pygame.gfxdraw.filled_circle(self.screen, int(posx+2), int(posy+1), radius, self.shadowColor)

            # antialiased filled circle
            pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, color)
            pygame.gfxdraw.filled_circle(self.screen, posx, posy, radius, color)

    def setBox(self, bx, by, color, shadow=False):
        self.fillBox(bx, by, color, shadow)

    def setBoxWhite(self, bx, by):
        self.setBox(bx, by, self.whitePieceColor, True)

    def setBoxBlack(self, bx, by):
        self.setBox(bx, by, self.blackPieceColor, True)

    def setLastMove(self, bx, by):
        """Set the position of the last move and draw a red dot"""
        self.lastMoveX = bx
        self.lastMoveY = by

    def drawLastMoveIndicator(self):
        """Draw red dot on the last move position"""
        if self.lastMoveX is not None and self.lastMoveY is not None:
            posx = int(self.marginx + self.stepx * self.lastMoveX + self.stepx // 2)
            posy = int(self.marginy + self.stepy * self.lastMoveY + self.stepy // 2)
            pygame.draw.circle(self.screen, self.lastMoveColor, (posx, posy), 4)

    def setCanMove(self, bx, by):
        self.fillBox(bx, by, self.canMoveColor, False, True)

    def setCanMoveBlack(self, bx, by):
        self.fillBox(bx, by, self.blackMoveColor, False, True)

    def setCanMoveWhite(self, bx, by):
        self.fillBox(bx, by, self.whiteMoveColor, False, True)

    def unsetBox(self, bx, by):
        self.unfillBox(bx, by)

    def setPoint(self, x, y, color):
        (bx, by) = self.point2Box(x, y)
        self.setBox(bx,by)

    def setPointBlack(self, x, y, color):
        self.setPoint(x, y, self.blackPieceColor)

    def setPointWhite(self, x, y, color):
        self.setPoint(x, y, self.whitePieceColor)

    def unsetPoint(self, x, y):
        (bx, by) = self.point2Box(x, y)
        self.unsetBox(bx,by)
    
    def point2Box(self, x, y):
        bx = int((x - self.marginx) // self.stepx)
        by = int((y - self.marginy) // self.stepy)
        return (bx, by)

