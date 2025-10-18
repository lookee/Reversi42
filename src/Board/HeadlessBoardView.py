"""
HeadlessBoardView - No-Rendering View for Tournaments

This view implementation performs no rendering at all. It's perfect for:
- Automated tournaments
- Performance benchmarking  
- Batch game execution
- CI/CD testing

Maximum speed - zero overhead from graphics!

Version: 3.1.0
"""

from .AbstractBoardView import AbstractBoardView
from typing import List, Tuple, Optional


class HeadlessBoardView(AbstractBoardView):
    """
    Headless view with no rendering.
    
    All methods are no-ops or minimal implementations.
    Perfect for maximum speed in tournaments where visualization isn't needed.
    
    Performance: 0ms rendering overhead (vs 10-50ms for Pygame)
    """
    
    def __init__(self, sizex=8, sizey=8, width=0, height=0):
        """
        Initialize headless view.
        
        Args:
            sizex: Board width (default 8)
            sizey: Board height (default 8)
            width: Ignored (no display)
            height: Ignored (no display)
        """
        super().__init__(sizex, sizey, width, height)
        
        # Minimal state tracking
        self.initialized = False
    
    def initialize(self):
        """Initialize (no-op for headless)"""
        self.initialized = True
    
    def render_board(self, model):
        """Render board (no-op for headless)"""
        pass
    
    def render_piece(self, x: int, y: int, color: str):
        """Render piece (no-op for headless)"""
        pass
    
    def highlight_valid_moves(self, moves: List[Tuple[int, int]]):
        """Highlight valid moves (no-op for headless)"""
        pass
    
    def highlight_last_move(self, x: int, y: int):
        """Highlight last move (no-op for headless)"""
        self.last_move_x = x
        self.last_move_y = y
    
    def update_display(self, cursor_mode: bool = False):
        """Update display (no-op for headless)"""
        pass
    
    def clear_display(self):
        """Clear display (no-op for headless)"""
        pass
    
    def set_cursor(self, x: int, y: int):
        """Set cursor (minimal tracking)"""
        self.cursorX = x
        self.cursorY = y
    
    def get_cursor_position(self) -> Tuple[Optional[int], Optional[int]]:
        """Get cursor position"""
        return (self.cursorX, self.cursorY)
    
    def point_to_board_position(self, screen_x: int, screen_y: int) -> Tuple[Optional[int], Optional[int]]:
        """Convert screen to board position (returns None for headless)"""
        return (None, None)
    
    def set_player_info(self, black_name: str, white_name: str, 
                       black_count: int, white_count: int, current_turn: str):
        """Set player info (minimal tracking)"""
        self.black_player_name = black_name
        self.white_player_name = white_name
        self.black_count = black_count
        self.white_count = white_count
        self.current_turn = current_turn
    
    def show_message(self, message: str, duration: float = 2.0):
        """Show message (print to console for headless)"""
        print(f"[MESSAGE] {message}")
    
    def resize(self, width: int, height: int):
        """Resize (no-op for headless)"""
        self.width = width
        self.height = height
    
    def cleanup(self):
        """Cleanup (minimal for headless)"""
        self.initialized = False
    
    # Pygame-specific methods that some code might call
    # Provide no-op implementations for compatibility
    
    def cursorHand(self):
        """No-op cursor change"""
        pass
    
    def cursorWait(self):
        """No-op cursor change"""
        pass
    
    def refresh(self):
        """No-op refresh"""
        pass
    
    def update(self, cursor_mode=False):
        """No-op update"""
        pass
    
    def fillBox(self, bx, by, color, shadow=True, hollow=False):
        """No-op fill box"""
        pass
    
    def unfillBox(self, bx, by):
        """No-op unfill box"""
        pass
    
    def setBox(self, bx, by, color, shadow=False):
        """No-op set box"""
        pass
    
    def setLastMove(self, bx, by):
        """Track last move (minimal)"""
        self.last_move_x = bx
        self.last_move_y = by
    
    def drawLastMoveIndicator(self):
        """No-op draw last move"""
        pass
    
    def setCanMove(self, bx, by):
        """No-op set can move"""
        pass
    
    def drawHeader(self):
        """No-op draw header"""
        pass
    
    def drawCoordinates(self):
        """No-op draw coordinates"""
        pass
    
    def point2Box(self, x, y):
        """Convert point to box (returns None for headless)"""
        return (None, None)
    
    def setCursor(self, bx, by):
        """Set cursor position (minimal tracking)"""
        self.cursorX = bx
        self.cursorY = by
    
    def drawCursor(self, cursor_mode=False):
        """No-op draw cursor"""
        pass
    
    def moveCursor(self, dx, dy):
        """Move cursor (minimal tracking)"""
        if self.cursorX is not None and self.cursorY is not None:
            self.cursorX = max(0, min(self.sizex - 1, self.cursorX + dx))
            self.cursorY = max(0, min(self.sizey - 1, self.cursorY + dy))
    
    def setPlayerNames(self, black_name, white_name):
        """Set player names"""
        self.black_player_name = black_name
        self.white_player_name = white_name
    
    def setPlayerCounts(self, black_count, white_count):
        """Set piece counts"""
        self.black_count = black_count
        self.white_count = white_count
    
    def setCurrentTurn(self, turn):
        """Set current turn"""
        self.current_turn = turn
    
    def set_opening_info(self, opening_names):
        """No-op set opening info"""
        pass
    
    def clear_tooltip_area(self):
        """No-op clear tooltip"""
        pass
    
    def draw_opening_info_fixed(self):
        """No-op draw opening info"""
        pass

