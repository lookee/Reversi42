
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

        # Professional color palette - optimized for clarity and elegance
        self.bgColor            = (  0,      95,     75)  # Rich forest green background
        self.lineColor          = ( 15,      55,     45)  # Dark teal lines (not pure black)
        self.boxColor           = (  0,       0,      0)
        self.shadowColor        = ( 25,      50,     40)  # Subtle shadow
        
        # Piece colors with improved contrast
        self.whitePieceColor    = (248,     248,    250)  # Soft white (less harsh)
        self.blackPieceColor    = ( 15,      15,     20)  # Deep black (not pure black)
        
        # UI accent colors
        self.lastMoveColor      = (255,     180,     50)  # Golden amber for last move
        self.hoshiColor         = ( 20,      70,     55)  # Subtle dark teal for hoshi
        self.canMoveColor       = (180,     220,    190)  # Soft mint for possible moves
        self.whiteMoveColor     = (200,     230,    210)  # Light mint for white moves
        self.blackMoveColor     = (160,     200,    170)  # Darker mint for black moves
        self.cursorColor        = (255,     215,      0)  # Pure gold for cursor

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
        self.current_turn = 'B'  # Track whose turn it is
        
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
        
        # Calculate line width based on cell size (proportional to smallest dimension)
        min_step = min(self.stepx, self.stepy)
        self.line_width = max(1, min(4, min_step // 25))  # Between 1 and 4 pixels
    
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
            pygame.draw.lines(screen, self.lineColor, False, [start, end], self.line_width)

        for n in range(0,self.sizey + 1):

            # grid: horizontal lines
            start = (0 + self.marginx, self.stepy * n + self.marginy)
            end   = (self.sizex * self.stepx + self.marginx, self.stepy * n + self.marginy)
            pygame.draw.lines(screen, self.lineColor, False, [start, end], self.line_width)
            
        # Add hoshi points (star points) with professional appearance
        if self.sizex == 8 and self.sizey == 8:
            hoshi_positions = [(2, 2), (5, 2), (2, 5), (5, 5)]
            for hoshi_x, hoshi_y in hoshi_positions:
                intersection_x = self.marginx + hoshi_x * self.stepx
                intersection_y = self.marginy + hoshi_y * self.stepy
                
                # Calculate proportional radius
                hoshi_radius = max(4, min(7, min(self.stepx, self.stepy) // 14))
                
                # Draw with anti-aliasing for smooth appearance
                pygame.gfxdraw.filled_circle(screen, intersection_x, intersection_y, hoshi_radius, self.hoshiColor)
                pygame.gfxdraw.aacircle(screen, intersection_x, intersection_y, hoshi_radius, self.hoshiColor)

    def update(self, cursor_mode=False):
        # Draw header with player info
        self.drawHeader()
        # Draw last move indicator before updating display
        self.drawLastMoveIndicator()
        # Draw cursor only if in cursor mode
        self.drawCursor(cursor_mode)
        pygame.display.update()

    def unfillBox(self, bx, by):
        """Clear a box and redraw grid lines for clean appearance"""
        # Fill the entire cell area with background color
        rect = Rect(
            self.marginx + bx * self.stepx,
            self.marginy + by * self.stepy,
            self.stepx,
            self.stepy
        )
        self.screen.fill(self.bgColor, rect)
        
        # Redraw the grid lines for this cell
        # Left line
        if bx == 0 or True:  # Always redraw left line
            x = self.marginx + bx * self.stepx
            start = (x, self.marginy + by * self.stepy)
            end = (x, self.marginy + (by + 1) * self.stepy)
            pygame.draw.line(self.screen, self.lineColor, start, end, self.line_width)
        
        # Right line
        x = self.marginx + (bx + 1) * self.stepx
        start = (x, self.marginy + by * self.stepy)
        end = (x, self.marginy + (by + 1) * self.stepy)
        pygame.draw.line(self.screen, self.lineColor, start, end, self.line_width)
        
        # Top line
        if by == 0 or True:  # Always redraw top line
            y = self.marginy + by * self.stepy
            start = (self.marginx + bx * self.stepx, y)
            end = (self.marginx + (bx + 1) * self.stepx, y)
            pygame.draw.line(self.screen, self.lineColor, start, end, self.line_width)
        
        # Bottom line
        y = self.marginy + (by + 1) * self.stepy
        start = (self.marginx + bx * self.stepx, y)
        end = (self.marginx + (bx + 1) * self.stepx, y)
        pygame.draw.line(self.screen, self.lineColor, start, end, self.line_width)
        
        # Redraw hoshi point if this cell contains one
        if self.sizex == 8 and self.sizey == 8:
            hoshi_positions = [(2, 2), (5, 2), (2, 5), (5, 5)]
            if (bx, by) in hoshi_positions:
                intersection_x = self.marginx + bx * self.stepx
                intersection_y = self.marginy + by * self.stepy
                hoshi_radius = max(4, min(7, min(self.stepx, self.stepy) // 14))
                pygame.gfxdraw.filled_circle(self.screen, intersection_x, intersection_y, hoshi_radius, self.hoshiColor)
                pygame.gfxdraw.aacircle(self.screen, intersection_x, intersection_y, hoshi_radius, self.hoshiColor)     

    def fillBox(self, bx, by, color, shadow=True, hollow=False):

        radius = int((self.stepy-10) // 2)
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)

        self.unfillBox(bx, by)

        if hollow:
            # Draw hollow circle for possible moves with anti-aliasing
            pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, color)
            pygame.draw.circle(self.screen, color, (posx, posy), radius, 2)
        else:
            # Draw shadow with soft edge
            if shadow:
                shadow_offset = 3
                shadow_x = int(posx + shadow_offset)
                shadow_y = int(posy + shadow_offset)
                # Multi-layer shadow for smoother appearance
                pygame.gfxdraw.filled_circle(self.screen, shadow_x, shadow_y, radius, self.shadowColor)
                pygame.gfxdraw.aacircle(self.screen, shadow_x, shadow_y, radius, self.shadowColor)

            # Draw main piece with gradient effect
            # Create subtle gradient by drawing concentric circles
            if color == self.whitePieceColor:
                # White piece: bright in center, slightly darker at edge
                for r in range(radius, max(0, radius - 8), -1):
                    brightness = 248 - int((radius - r) * 2)
                    gradient_color = (brightness, brightness, min(250, brightness + 2))
                    pygame.gfxdraw.filled_circle(self.screen, posx, posy, r, gradient_color)
            elif color == self.blackPieceColor:
                # Black piece: subtle highlight in center
                for r in range(radius, max(0, radius - 6), -1):
                    darkness = 15 + int((radius - r) * 4)
                    gradient_color = (darkness, darkness, darkness + 5)
                    pygame.gfxdraw.filled_circle(self.screen, posx, posy, r, gradient_color)
            else:
                # Other colors: draw normally
                pygame.gfxdraw.filled_circle(self.screen, posx, posy, radius, color)
            
            # Anti-aliased edge for crisp appearance
            pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, color)

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
        """Draw golden indicator on the last move position with glow"""
        if self.lastMoveX is not None and self.lastMoveY is not None:
            posx = int(self.marginx + self.stepx * self.lastMoveX + self.stepx // 2)
            posy = int(self.marginy + self.stepy * self.lastMoveY + self.stepy // 2)
            
            # Draw with anti-aliasing and subtle glow
            radius = max(5, min(8, min(self.stepx, self.stepy) // 12))
            
            # Outer glow
            glow_color = (255, 200, 80, 80)
            for i in range(3):
                glow_radius = radius + 2 + i * 2
                pygame.gfxdraw.filled_circle(self.screen, posx, posy, glow_radius, (255, 200, 80, 40 - i * 10))
            
            # Main dot with anti-aliasing
            pygame.gfxdraw.filled_circle(self.screen, posx, posy, radius, self.lastMoveColor)
            pygame.gfxdraw.aacircle(self.screen, posx, posy, radius, self.lastMoveColor)

    def setCanMove(self, bx, by):
        """Draw possible move indicator with perfectly smooth anti-aliased edges"""
        radius = int((self.stepy-10) // 4)
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)
        
        self.unfillBox(bx, by)
        
        # Use larger surface and pygame.draw.circle for better quality
        surf_size = radius * 4  # Much larger to avoid artifacts
        s = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        center = surf_size // 2
        
        # Draw filled circle using pygame.draw (better anti-aliasing than gfxdraw)
        pygame.draw.circle(s, (*self.canMoveColor, 180), (center, center), radius)
        
        # Add manual anti-aliasing by drawing semi-transparent rings
        for i in range(1, 4):
            alpha = 180 - i * 50
            if alpha > 0:
                pygame.draw.circle(s, (*self.canMoveColor, alpha), (center, center), radius + i, 1)
        
        self.screen.blit(s, (posx - center, posy - center))

    def setCanMoveBlack(self, bx, by):
        """Draw possible move for black with perfectly smooth edges"""
        radius = int((self.stepy-10) // 4)
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)
        
        self.unfillBox(bx, by)
        
        surf_size = radius * 4
        s = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        center = surf_size // 2
        
        # Draw with smooth anti-aliasing
        pygame.draw.circle(s, (*self.blackMoveColor, 200), (center, center), radius)
        
        # Manual anti-aliasing rings
        for i in range(1, 4):
            alpha = 200 - i * 50
            if alpha > 0:
                pygame.draw.circle(s, (*self.blackMoveColor, alpha), (center, center), radius + i, 1)
        
        self.screen.blit(s, (posx - center, posy - center))

    def setCanMoveWhite(self, bx, by):
        """Draw possible move for white with perfectly smooth edges"""
        radius = int((self.stepy-10) // 4)
        posx = int(self.marginx + self.stepx * bx + self.stepx // 2)
        posy = int(self.marginy + self.stepy * by + self.stepy // 2)
        
        self.unfillBox(bx, by)
        
        surf_size = radius * 4
        s = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        center = surf_size // 2
        
        # Draw with smooth anti-aliasing
        pygame.draw.circle(s, (*self.whiteMoveColor, 200), (center, center), radius)
        
        # Manual anti-aliasing rings
        for i in range(1, 4):
            alpha = 200 - i * 50
            if alpha > 0:
                pygame.draw.circle(s, (*self.whiteMoveColor, alpha), (center, center), radius + i, 1)
        
        self.screen.blit(s, (posx - center, posy - center))

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
        """Draw elegant golden cursor with rounded corners"""
        if cursor_mode and 0 <= self.cursorX < self.sizex and 0 <= self.cursorY < self.sizey:
            rect_x = self.marginx + self.cursorX * self.stepx + 3
            rect_y = self.marginy + self.cursorY * self.stepy + 3
            rect_width = self.stepx - 6
            rect_height = self.stepy - 6
            
            # Draw outer glow for visibility
            glow_rect = pygame.Rect(rect_x - 2, rect_y - 2, rect_width + 4, rect_height + 4)
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*self.cursorColor, 60), s.get_rect(), width=6, border_radius=6)
            self.screen.blit(s, glow_rect.topleft)
            
            # Main cursor border (thicker, rounded)
            cursor_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(self.screen, self.cursorColor, cursor_rect, width=4, border_radius=4)
    
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
    
    def refresh(self):
        """Completely refresh the screen (useful after overlays like pause menu)"""
        self.screen.fill(self.bgColor)
        self.__init_grid()
    
    def setPlayerNames(self, black_name, white_name):
        """Set the names of the players"""
        self.black_player_name = black_name
        self.white_player_name = white_name
    
    def setPlayerCounts(self, black_count, white_count):
        """Set the piece counts for both players"""
        self.black_count = black_count
        self.white_count = white_count
    
    def setCurrentTurn(self, turn):
        """Set whose turn it is (B or W)"""
        self.current_turn = turn
    
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
        piece_spacing = 25
        indicator_radius = 5  # Small yellow dot for turn indicator
        indicator_spacing = 15  # Distance from text
        
        # Text color is always white (no color change)
        text_color = self.whitePieceColor
        
        # Draw black player info (left side)
        # Draw the black piece
        piece_x = left_x
        piece_y = center_y
        pygame.gfxdraw.filled_circle(self.screen, piece_x, piece_y, piece_radius, self.blackPieceColor)
        pygame.gfxdraw.aacircle(self.screen, piece_x, piece_y, piece_radius, self.blackPieceColor)
        
        # Draw the text after the piece
        black_text = f"{self.black_player_name}: {self.black_count}"
        black_surface = self.header_font.render(black_text, True, text_color)
        black_rect = black_surface.get_rect()
        black_rect.midleft = (left_x + piece_radius + piece_spacing, center_y)
        self.screen.blit(black_surface, black_rect)
        
        # Draw turn indicator for black (small yellow dot to the right of text)
        if self.current_turn == 'B':
            indicator_x = black_rect.right + indicator_spacing
            indicator_y = center_y
            pygame.gfxdraw.filled_circle(self.screen, indicator_x, indicator_y, indicator_radius, self.cursorColor)
            pygame.gfxdraw.aacircle(self.screen, indicator_x, indicator_y, indicator_radius, self.cursorColor)
        
        # Draw white player info (right side)
        # Prepare white text
        white_text = f"{self.white_player_name}: {self.white_count}"
        white_surface = self.header_font.render(white_text, True, text_color)
        white_rect = white_surface.get_rect()
        white_rect.midright = (right_x - piece_radius - piece_spacing, center_y)
        
        # Draw turn indicator for white first (to the left of text, before it)
        if self.current_turn == 'W':
            indicator_x = white_rect.left - indicator_spacing
            indicator_y = center_y
            pygame.gfxdraw.filled_circle(self.screen, indicator_x, indicator_y, indicator_radius, self.cursorColor)
            pygame.gfxdraw.aacircle(self.screen, indicator_x, indicator_y, indicator_radius, self.cursorColor)
        
        # Draw the text
        self.screen.blit(white_surface, white_rect)
        
        # Draw the white piece after the text
        piece_x = right_x
        piece_y = center_y
        pygame.gfxdraw.filled_circle(self.screen, piece_x, piece_y, piece_radius, self.whitePieceColor)
        pygame.gfxdraw.aacircle(self.screen, piece_x, piece_y, piece_radius, self.blackPieceColor)
        
        # Draw a separator line
        pygame.draw.line(self.screen, self.lineColor, 
                        (0, self.header_height - 2), 
                        (self.width, self.header_height - 2), 2)

