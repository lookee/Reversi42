
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
        self.bgColor            = (  0,     108,     85)  # Darker green background
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
        self.cursorColor        = (255,     255,      0)   # Yellow for cursor highlight

        # Minimum window size
        self.min_width = 400
        self.min_height = 300
        
        # Initialize header settings first (before calculateDimensions)
        pygame.font.init()
        self.header_font = pygame.font.Font(None, 32)
        self.header_height = 50  # Height reserved for header
        
        # Player information
        self.black_player_name = "Black"
        self.white_player_name = "White"
        self.black_count = 2
        self.white_count = 2
        
        # Calculate dynamic dimensions
        self.calculateDimensions()
        
        # Track last move position for red dot indicator
        self.lastMoveX = None
        self.lastMoveY = None
        
        # Track cursor position for navigation
        self.cursorX = 0
        self.cursorY = 0
       
        self.__init_screen()
        self.__init_grid()
        self.update(False)
    
    def calculateDimensions(self):
        """Calculate dynamic dimensions based on current window size"""
        # Reserve space for header
        board_height = self.heigth - self.header_height
        
        # Calculate cell size to fit the board
        self.stepx = self.width // self.sizex
        self.stepy = board_height // self.sizey
        
        # Calculate margins to center the board
        self.marginx = (self.width % self.sizex) // 2
        self.marginy = self.header_height + (board_height % self.sizey) // 2
    
    def resize(self, new_width, new_height):
        """Handle window resize"""
        # Ensure minimum size
        self.width = max(new_width, self.min_width)
        self.heigth = max(new_height, self.min_height)
        
        # Recalculate dimensions
        self.calculateDimensions()
        
        # Resize the screen
        self.screen = pygame.display.set_mode((self.width, self.heigth), pygame.RESIZABLE)
        
        # Redraw everything
        self.__init_grid()
        self.update(False)

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

        self.screen = pygame.display.set_mode((self.width,self.heigth), pygame.RESIZABLE, 32)
        pygame.display.set_caption(self.caption)

        self.screen.fill(self.bgColor)

    def __init_grid(self):
        
        screen = self.screen

        for n in range(0,self.sizex + 1):

            # grid: vertical lines
            start = (self.stepx * n + self.marginx, 0 + self.marginy)
            end   = (self.stepx * n + self.marginx, self.sizey * self.stepy + self.marginy)
            pygame.draw.lines(screen, self.lineColor, False, [start, end], 2)

        for n in range(0,self.sizey + 1):

            # grid: horizontal lines
            start = (0 + self.marginx, self.stepy * n + self.marginy)
            end   = (self.sizex * self.stepx + self.marginx, self.stepy * n + self.marginy)
            pygame.draw.lines(screen, self.lineColor, False, [start, end], 2)
            
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

    def update(self, cursor_mode=False):
        # Draw header with player info
        self.drawHeader()
        # Draw last move indicator before updating display
        self.drawLastMoveIndicator()
        # Draw cursor only if in cursor mode
        self.drawCursor(cursor_mode)
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
                pygame.gfxdraw.aacircle(self.screen, int(posx+2), int(posy+2), radius, self.shadowColor)
                pygame.gfxdraw.filled_circle(self.screen, int(posx+2), int(posy+2), radius, self.shadowColor)

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
        # Make smaller circles for possible moves
        radius = int((self.stepy-10) // 4)  # Smaller radius
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)
        
        self.unfillBox(bx, by)
        # Draw smaller hollow circle for possible moves
        pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, self.canMoveColor)
        pygame.draw.circle(self.screen, self.canMoveColor, (posx, posy), radius, 2)

    def setCanMoveBlack(self, bx, by):
        # Make smaller circles for possible moves
        radius = int((self.stepy-10) // 4)  # Smaller radius
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)
        
        self.unfillBox(bx, by)
        # Draw smaller hollow circle for possible moves
        pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, self.blackMoveColor)
        pygame.draw.circle(self.screen, self.blackMoveColor, (posx, posy), radius, 2)

    def setCanMoveWhite(self, bx, by):
        # Make smaller circles for possible moves
        radius = int((self.stepy-10) // 4)  # Smaller radius
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)
        
        self.unfillBox(bx, by)
        # Draw smaller hollow circle for possible moves
        pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, self.whiteMoveColor)
        pygame.draw.circle(self.screen, self.whiteMoveColor, (posx, posy), radius, 2)

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
    
    def setCursor(self, bx, by):
        """Set cursor position"""
        self.cursorX = bx
        self.cursorY = by
    
    def drawCursor(self, cursor_mode=False):
        """Draw yellow rectangle around cursor position"""
        if cursor_mode and 0 <= self.cursorX < self.sizex and 0 <= self.cursorY < self.sizey:
            # Draw yellow rectangle around the cursor position
            rect_x = self.marginx + self.cursorX * self.stepx + 2
            rect_y = self.marginy + self.cursorY * self.stepy + 2
            rect_width = self.stepx - 4
            rect_height = self.stepy - 4
            
            pygame.draw.rect(self.screen, self.cursorColor, 
                           (rect_x, rect_y, rect_width, rect_height), 3)
    
    def moveCursor(self, dx, dy):
        """Move cursor by dx, dy"""
        old_x = self.cursorX
        old_y = self.cursorY
        
        new_x = self.cursorX + dx
        new_y = self.cursorY + dy
        
        # Keep cursor within bounds
        if 0 <= new_x < self.sizex:
            self.cursorX = new_x
        if 0 <= new_y < self.sizey:
            self.cursorY = new_y
        
        # If cursor moved, we need to redraw the board to clear the old cursor
        if old_x != self.cursorX or old_y != self.cursorY:
            # Clear the old cursor position by redrawing the cell
            self.unfillBox(old_x, old_y)
            # Redraw any piece or move indicator that was there
            # This will be handled by the calling code
    
    def getCursorPosition(self):
        """Get current cursor position"""
        return (self.cursorX, self.cursorY)
    
    def setPlayerNames(self, black_name, white_name):
        """Set the names of the players"""
        self.black_player_name = black_name
        self.white_player_name = white_name
    
    def setPlayerCounts(self, black_count, white_count):
        """Set the piece counts for both players"""
        self.black_count = black_count
        self.white_count = white_count
    
    def drawHeader(self):
        """Draw the header with player names and piece counts"""
        # Clear header area
        header_rect = pygame.Rect(0, 0, self.width, self.header_height)
        self.screen.fill(self.bgColor, header_rect)
        
        # Calculate positions
        left_x = 20
        right_x = self.width - 20
        center_y = self.header_height // 2
        piece_radius = 12
        piece_spacing = 25  # Increased spacing between piece and text
        
        # Draw black player info (left side)
        # First draw the black piece
        piece_x = left_x
        piece_y = center_y
        pygame.gfxdraw.filled_circle(self.screen, piece_x, piece_y, piece_radius, self.blackPieceColor)
        pygame.gfxdraw.aacircle(self.screen, piece_x, piece_y, piece_radius, self.blackPieceColor)
        
        # Then draw the text after the piece
        black_text = f"{self.black_player_name}: {self.black_count}"
        black_surface = self.header_font.render(black_text, True, self.whitePieceColor)
        black_rect = black_surface.get_rect()
        black_rect.midleft = (left_x + piece_radius + piece_spacing, center_y)
        self.screen.blit(black_surface, black_rect)
        
        # Draw white player info (right side)
        # First draw the text
        white_text = f"{self.white_player_name}: {self.white_count}"
        white_surface = self.header_font.render(white_text, True, self.whitePieceColor)
        white_rect = white_surface.get_rect()
        white_rect.midright = (right_x - piece_radius - piece_spacing, center_y)
        self.screen.blit(white_surface, white_rect)
        
        # Then draw the white piece after the text
        piece_x = right_x
        piece_y = center_y
        pygame.gfxdraw.filled_circle(self.screen, piece_x, piece_y, piece_radius, self.whitePieceColor)
        pygame.gfxdraw.aacircle(self.screen, piece_x, piece_y, piece_radius, self.blackPieceColor)
        
        # Draw a separator line
        pygame.draw.line(self.screen, self.lineColor, 
                        (0, self.header_height - 2), 
                        (self.width, self.header_height - 2), 2)

