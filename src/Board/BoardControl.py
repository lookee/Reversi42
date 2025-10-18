
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

"""
BoardControl - Controller for Board MVC Architecture

Manages interaction between Model and View with support for multiple view types.
Now 100% framework-agnostic using InputHandler abstraction.

Version: 3.1.0
Architecture: Framework-independent controller
"""

from Board.BoardView import BoardView
from Board.BoardModel import BoardModel
from ui.abstractions.input_interface import InputEvent

# Lazy import for pygame only when needed
try:
    import pygame
    from pygame.locals import *
    _PYGAME_AVAILABLE = True
except ImportError:
    _PYGAME_AVAILABLE = False

class BoardControl(object):
    """
    Board controller with pluggable view support.
    
    Supports dependency injection of view implementation:
    - PygameBoardView (default) - Graphical Pygame UI
    - TerminalBoardView - ASCII art terminal
    - HeadlessBoardView - No rendering (tournaments)
    - Custom views implementing AbstractBoardView
    """

    def __init__(self, sizex, sizey, view_class=None, view_args=None, input_handler=None):
        """
        Initialize board control.
        
        Args:
            sizex: Board width
            sizey: Board height
            view_class: View class to use (default: BoardView/PygameBoardView)
            view_args: Additional arguments for view constructor (dict)
            input_handler: Optional input handler (auto-created if None)
        """
        self.sizex = sizex
        self.sizey = sizey
        
        # Create view with dependency injection
        if view_class is None:
            view_class = BoardView  # Default to Pygame view
        
        if view_args is None:
            view_args = {}
        
        # Create view instance
        self.view = view_class(sizex, sizey, 800, 600, **view_args)
        self.model = BoardModel(sizex, sizey)

        self.keyPressed = False
        self.cursor_mode = False  # Whether we're in cursor navigation mode
        self.should_exit = False  # Flag to signal exit
        self.should_pause = False  # Flag to signal pause request
        self.should_return_to_menu = False  # Flag to signal return to menu
        
        # Opening book support
        self.opening_book = None
        self.show_opening = False
        self.book_moves = []  # List of (x, y, count) tuples for book moves with opening count
        
        # Initialize cursor to center of board
        self.view.setCursor(sizex // 2, sizey // 2)
        
        # Create or use provided input handler
        if input_handler is None:
            # Auto-create appropriate input handler based on view type
            self.input_handler = self._create_input_handler_for_view()
        else:
            self.input_handler = input_handler
    
    def _create_input_handler_for_view(self):
        """Auto-create appropriate input handler based on view type"""
        view_type = type(self.view).__name__
        
        if 'Pygame' in view_type:
            from ui.implementations.pygame.input_handler import PygameInputHandler
            return PygameInputHandler()
        elif 'Terminal' in view_type:
            from ui.implementations.terminal.input_handler import TerminalInputHandler
            return TerminalInputHandler()
        elif 'Headless' in view_type:
            from ui.implementations.headless.input_handler import HeadlessInputHandler
            return HeadlessInputHandler()
        else:
            # Default to pygame if unknown
            if _PYGAME_AVAILABLE:
                from ui.implementations.pygame.input_handler import PygameInputHandler
                return PygameInputHandler()
            else:
                from ui.implementations.headless.input_handler import HeadlessInputHandler
                return HeadlessInputHandler()

    def action(self):
        """Non-blocking action method that processes events once"""
        self.waitInput = True
        # Don't reset bx, by here - they might have been set by ENTER/SPACE
        
        # Process all pending events using InputHandler
        events = self.input_handler.poll_events()
        for event in events:
            self.handleInputEvent(event)
    
    def check_events(self):
        """Check for events without setting waitInput - used during AI turns"""
        events = self.input_handler.poll_events()
        for event in events:
            event_type = event.get('type')
            
            if event_type == InputEvent.QUIT:
                self.should_exit = True
            elif event_type == InputEvent.QUIT_DIRECT:
                self.should_exit = True
            elif event_type == InputEvent.RESIZE:
                # Handle window resize
                data = event.get('data', {})
                self.view.resize(data.get('width', 800), data.get('height', 600))
                # Redraw the board content after resize
                self.renderModel()
            elif event_type == InputEvent.PAUSE:
                self.should_pause = True

    def handleInputEvent(self, event):
        """Handle framework-agnostic InputEvent"""
        event_type = event.get('type')
        
        if event_type == InputEvent.QUIT:
            self.triggerEnd()
        elif event_type == InputEvent.QUIT_DIRECT:
            self.should_exit = True
            self.waitInput = False
        elif event_type == InputEvent.RESIZE:
            # Handle window resize
            data = event.get('data', {})
            self.view.resize(data.get('width', 800), data.get('height', 600))
            self.renderModel()
        elif event_type == InputEvent.CLICK:
            self.handleMouseClick(event)
        elif event_type == InputEvent.PAUSE:
            self.should_pause = True
            self.waitInput = False
        elif event_type == InputEvent.TOGGLE_CURSOR:
            self.handleToggleCursor()
        elif event_type in (InputEvent.MOVE_UP, InputEvent.MOVE_DOWN, 
                           InputEvent.MOVE_LEFT, InputEvent.MOVE_RIGHT):
            self.handleCursorMove(event_type)
        elif event_type == InputEvent.SELECT:
            self.handleCursorSelect()
    
    def handleEvent(self, event):
        """Legacy method for backward compatibility"""
        # For backward compatibility with old code that might call this directly
        if _PYGAME_AVAILABLE and hasattr(event, 'type'):
            # This is a raw pygame event - handle with legacy methods
            from pygame.locals import QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, VIDEORESIZE
            
            if event.type == QUIT:
                self.triggerEnd()
            elif event.type == VIDEORESIZE:
                self.view.resize(event.w, event.h)
                self.renderModel()
            elif event.type == MOUSEBUTTONDOWN:
                self.handleMouseButtonEvents(event)
            elif event.type == KEYUP:
                self.keyPressed = False
            elif event.type == KEYDOWN and not self.keyPressed:
                self.keyPressed = True
                self.handleKeyEventsLegacy(event)
        else:
            # Already an InputEvent dict
            self.handleInputEvent(event)

    def handleToggleCursor(self):
        """Toggle cursor navigation mode"""
        self.cursor_mode = not self.cursor_mode
        if self.cursor_mode:
            # Set cursor to center of board
            self.view.setCursor(self.sizex // 2, self.sizey // 2)
        # Redraw board to show/hide cursor
        self.redrawBoard()
    
    def handleCursorMove(self, direction):
        """Handle cursor movement"""
        if not self.cursor_mode:
            return
        
        if direction == InputEvent.MOVE_UP:
            self.view.moveCursor(0, -1)
        elif direction == InputEvent.MOVE_DOWN:
            self.view.moveCursor(0, 1)
        elif direction == InputEvent.MOVE_LEFT:
            self.view.moveCursor(-1, 0)
        elif direction == InputEvent.MOVE_RIGHT:
            self.view.moveCursor(1, 0)
        
        self.redrawBoard()  # Redraw to show new cursor position
    
    def handleCursorSelect(self):
        """Handle cursor selection (ENTER/SPACE)"""
        if self.cursor_mode:
            # Select current cursor position
            self.bx, self.by = self.view.getCursorPosition()
            # Don't set waitInput = False here, let HumanPlayer handle validation
    
    def handleKeyEvents(self, event):
        """Legacy method for backward compatibility"""
        # This is now handled by handleInputEvent
        pass

    def triggerEnd(self):
        self.should_exit = True
        self.waitInput = False

    def handleMouseClick(self, event):
        """Handle mouse click event (framework-agnostic)"""
        data = event.get('data', {})
        position = data.get('position')
        
        if position is None:
            return
        
        (x, y) = position
        (bx, by) = self.view.point2Box(x, y)
        
        if bx in range(self.sizex) and by in range(self.sizey):
            print(f"Mouse click at ({bx}, {by})")
            self.bx = bx
            self.by = by
            # Update cursor position when clicking
            self.view.setCursor(bx, by)
            # Don't set waitInput = False here, let HumanPlayer handle validation
    
    def handleMouseButtonEvents(self, event):
        """Legacy method - handles pygame mouse events"""
        if hasattr(event, 'pos'):
            (x, y) = event.pos
            (bx, by) = self.view.point2Box(x, y)
            
            if bx in range(self.sizex) and by in range(self.sizey):
                if event.button == 1:  # Left click
                    print(f"Mouse click at ({bx}, {by})")
                    self.bx = bx
                    self.by = by
                    self.view.setCursor(bx, by)

    def renderModel(self):
        # Count pieces while rendering
        black_count = 0
        white_count = 0
        
        for x in range(self.sizex):
            for y in range(self.sizey):
                cell = self.model.getPoint(x,y)
                if cell == 'W':
                    self.view.setBoxWhite(x,y)
                    white_count += 1
                elif cell == 'B':
                    self.view.setBoxBlack(x,y)
                    black_count += 1
                elif cell == 'w':
                    self.view.setCanMoveWhite(x,y)
                elif cell == 'b':
                    self.view.setCanMoveBlack(x,y)
                else:
                    self.view.unsetBox(x,y)
        
        # Update piece counts in the view
        self.view.setPlayerCounts(black_count, white_count)
        self.view.update(self.cursor_mode)
        
        # Redraw opening book moves AFTER update (so they appear on top and don't get erased)
        # Works for both Pygame and Terminal views
        if self.show_opening and len(self.book_moves) > 0:
            for bx, by, count in self.book_moves:
                self.view.setCanMoveBook(bx, by, count)
            # Force display update to show the golden/X moves
            if hasattr(self.view, 'screen') and self.view.screen is not None:
                # Pygame view - force display update
                import pygame
                pygame.display.update()
            elif hasattr(self.view, '_draw_board'):
                # Terminal view - redraw board to show book moves
                self.view._draw_board()

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
    
    def setPlayerNames(self, black_name, white_name):
        """Set the player names for display in the header"""
        self.view.setPlayerNames(black_name, white_name)
    
    def display_available_moves(self, game, moves, turn):
        """
        Display all available moves with optional opening book highlighting.
        
        Consolidates logic previously duplicated in multiple places.
        Handles both normal moves and opening book golden highlighting.
        
        Args:
            game: Current game state (for history)
            moves: List of available moves
            turn: Current player turn ('B' or 'W')
        """
        self.book_moves = []  # Reset book moves list
        
        if self.show_opening and self.opening_book:
            # Check each move to see if it leads to an opening
            for move in moves:
                # Get all openings that include this move
                openings = self.opening_book.get_openings_for_move(game.history, move)
                
                if openings:
                    # This move leads to opening(s) - save for highlighting with count
                    self.book_moves.append((move.get_x() - 1, move.get_y() - 1, len(openings)))
                    self.setCanMove(move.get_x(), move.get_y(), turn)
                else:
                    self.setCanMove(move.get_x(), move.get_y(), turn)
        else:
            # No opening book - show all moves normally
            for move in moves:
                self.setCanMove(move.get_x(), move.get_y(), turn)
    
    def setCurrentTurn(self, turn):
        """Set whose turn it is for the turn indicator"""
        self.view.setCurrentTurn(turn)
