"""
TerminalBoardView - ASCII Art Terminal View

Beautiful ASCII art rendering for terminal/console play.
Perfect for:
- SSH/remote play
- Terminal purists
- Lightweight systems
- Screen reader accessibility

Version: 3.1.0
Architecture: Isolated in ui/implementations/terminal/
"""

import sys
import os

# Add path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from Board.AbstractBoardView import AbstractBoardView  # Use legacy for now
from typing import List, Tuple, Optional


class TerminalBoardView(AbstractBoardView):
    """
    Terminal-based ASCII art view.
    
    Features:
    - Beautiful Unicode box drawing
    - Color support (ANSI codes)
    - Keyboard-only input
    - Lightweight (<1KB memory)
    - Works over SSH
    """
    
    # Pure ASCII mode - no ANSI colors (works on any background)
    # Set USE_COLORS = False for pure ASCII, True for colored version
    USE_COLORS = False
    
    # ANSI color codes (only used if USE_COLORS = True)
    RESET = '\033[0m' if USE_COLORS else ''
    BOLD = '\033[1m' if USE_COLORS else ''
    
    # Pieces - Using ● and ○ symbols
    if USE_COLORS:
        BLACK_PIECE = '\033[1;37m●\033[0m'  # Bold white circle
        WHITE_PIECE = '\033[1;90m○\033[0m'  # Bold gray open circle
        EMPTY = '\033[2;37m·\033[0m'  # Dim dot
    else:
        # Pure symbols - works on any background
        BLACK_PIECE = '●'  # Black filled circle
        WHITE_PIECE = '○'  # White open circle
        EMPTY = '·'  # Dot for empty
    
    # Backgrounds (only if colors enabled)
    BG_GREEN = '\033[42m' if USE_COLORS else ''
    BG_YELLOW = '\033[43m' if USE_COLORS else ''
    BG_CYAN = '\033[46m' if USE_COLORS else ''
    
    # Text colors (only if colors enabled)
    GREEN = '\033[32m' if USE_COLORS else ''
    YELLOW = '\033[33m' if USE_COLORS else ''
    CYAN = '\033[36m' if USE_COLORS else ''
    RED = '\033[31m' if USE_COLORS else ''
    
    # Box drawing characters
    BOX_H = '─'
    BOX_V = '│'
    BOX_TL = '┌'
    BOX_TR = '┐'
    BOX_BL = '└'
    BOX_BR = '┘'
    BOX_CROSS = '┼'
    BOX_T_DOWN = '┬'
    BOX_T_UP = '┴'
    BOX_T_RIGHT = '├'
    BOX_T_LEFT = '┤'
    
    def __init__(self, sizex=8, sizey=8, width=80, height=24):
        """
        Initialize terminal view.
        
        Args:
            sizex: Board width (default 8)
            sizey: Board height (default 8)
            width: Terminal width in columns
            height: Terminal height in rows
        """
        super().__init__(sizex, sizey, width, height)
        
        # State
        self.board_state = [[' ' for _ in range(sizex)] for _ in range(sizey)]
        self.valid_moves_list = []
        self.use_color = True  # Can be disabled for non-color terminals
        self.last_output_lines = 0
        self.move_count = 0  # Track move number
        
        # Game info
        self.black_count = 2
        self.white_count = 2
        self.current_turn = 'B'
        
        # Player names
        self.black_player_name = "Black"
        self.white_player_name = "White"
        
        # Cursor and last move
        self.cursorX = 0
        self.cursorY = 0
        self.last_move_x = -1
        self.last_move_y = -1
    
    def initialize(self):
        """Initialize terminal (clear screen, setup)"""
        self.clear_screen()
        print(f"{self.BOLD}{self.GREEN}╔═══════════════════════════════════════════════════════════════╗{self.RESET}")
        print(f"{self.BOLD}{self.GREEN}║           REVERSI42 - TERMINAL MODE                           ║{self.RESET}")
        print(f"{self.BOLD}{self.GREEN}╚═══════════════════════════════════════════════════════════════╝{self.RESET}")
        print()
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def render_board(self, model):
        """Render complete board in ASCII art"""
        # Update internal state
        for y in range(self.sizey):
            for x in range(self.sizex):
                piece = model.getPoint(x, y)
                self.board_state[y][x] = piece if piece else ' '
        
        # Draw board
        self._draw_board()
    
    def _draw_board(self):
        """Internal: Draw the board in beautiful ASCII"""
        # Don't clear previous output - let terminal scroll naturally
        # This keeps the board visible between moves for human players
        
        lines = []
        
        # Compact header with player info on one line
        # Use ● for Black turn, ○ for White turn
        turn_symbol = '●' if self.current_turn == 'B' else '○'
        
        # Header with horizontal lines and pipe separators
        lines.append("")  # Empty line for spacing
        lines.append("─" * 40)
        lines.append(f"  Turn: {self.YELLOW if self.current_turn == 'B' else self.CYAN}{turn_symbol}{self.RESET}  |   " +
                    f"●:{self.black_count:>2}  ○:{self.white_count:>2}  |  " +
                    f"Move:{self.move_count}")
        lines.append("─" * 40)
        lines.append("")  # Empty line for spacing
        
        # Column headers (top only, perfectly aligned with board cells)
        # Each cell is 3 chars wide + 1 separator = 4 chars total
        col_header = "    " + "   ".join("ABCDEFGH"[:self.sizex])
        lines.append(col_header)
        
        # Top border
        top_line = "  " + self.BOX_TL
        for x in range(self.sizex):
            top_line += self.BOX_H * 3
            if x < self.sizex - 1:
                top_line += self.BOX_T_DOWN
        top_line += self.BOX_TR
        lines.append(top_line)
        
        # Board rows
        for y in range(self.sizey):
            # Row number
            row_str = f"{y + 1} {self.BOX_V}"
            
            for x in range(self.sizex):
                piece = self.board_state[y][x]
                
                # Check if this is a valid move
                is_valid_move = (x, y) in [(m[0] - 1 if hasattr(m, 'x') else m[0], 
                                           m[1] - 1 if hasattr(m, 'y') else m[1]) 
                                          for m in self.valid_moves_list]
                
                # Check if this is the last move
                is_last_move = (self.last_move_x == x + 1 and self.last_move_y == y + 1) or \
                              (self.last_move_x == x and self.last_move_y == y)
                
                # Check if cursor is here
                is_cursor = (self.cursorX == x and self.cursorY == y)
                
                # Determine what to display
                if piece == 'B':
                    cell = f" {self.BLACK_PIECE} "
                elif piece == 'W':
                    cell = f" {self.WHITE_PIECE} "
                elif piece in ['b', 'w'] or is_valid_move:  # b/w are valid move markers
                    # Valid move marker (use * for ASCII mode, ⊡ for color mode)
                    marker = '*' if not self.USE_COLORS else '⊡'
                    cell = f" {self.GREEN}{marker}{self.RESET} "
                else:
                    cell = f" {self.EMPTY} "
                
                # Highlight cursor
                if is_cursor:
                    cell = f"{self.BG_CYAN}{cell}{self.RESET}"
                # Highlight last move
                elif is_last_move:
                    cell = f"{self.BG_YELLOW}{cell}{self.RESET}"
                
                row_str += cell + self.BOX_V
            
            lines.append(row_str)
            
            # Middle separator or bottom border
            if y < self.sizey - 1:
                sep_line = "  " + self.BOX_T_RIGHT
                for x in range(self.sizex):
                    sep_line += self.BOX_H * 3
                    if x < self.sizex - 1:
                        sep_line += self.BOX_CROSS
                sep_line += self.BOX_T_LEFT
                lines.append(sep_line)
        
        # Bottom border
        bottom_line = "  " + self.BOX_BL
        for x in range(self.sizex):
            bottom_line += self.BOX_H * 3
            if x < self.sizex - 1:
                bottom_line += self.BOX_T_UP
        bottom_line += self.BOX_BR
        lines.append(bottom_line)
        
        # Print all lines with extra spacing for readability
        output = '\n'.join(lines)
        print(output)
        print()  # Extra blank line for separation between turns
    
    def render_piece(self, x: int, y: int, color: str):
        """Render single piece"""
        if 0 <= y < len(self.board_state) and 0 <= x < len(self.board_state[0]):
            self.board_state[y][x] = color
    
    def highlight_valid_moves(self, moves: List):
        """Highlight valid moves"""
        self.valid_moves_list = moves
    
    def highlight_last_move(self, x: int, y: int):
        """Highlight last move"""
        self.last_move_x = x
        self.last_move_y = y
    
    def update_display(self, cursor_mode: bool = False):
        """Update display (redraw board)"""
        self._draw_board()
    
    def clear_display(self):
        """Clear display"""
        self.clear_screen()
    
    def show_message(self, message: str, duration: float = 2.0):
        """Show message"""
        print(f"\n{self.BOLD}{self.YELLOW}>>> {message} <<<{self.RESET}\n")
        if duration > 0:
            import time
            time.sleep(duration)
    
    def resize(self, width: int, height: int):
        """Resize (adjust terminal view if needed)"""
        self.width = width
        self.height = height
    
    # Additional methods required by BoardControl
    
    def unsetBox(self, x: int, y: int):
        """Unset/clear a box (make it empty)"""
        if 0 <= y < len(self.board_state) and 0 <= x < len(self.board_state[0]):
            self.board_state[y][x] = ' '
    
    def setCanMoveWhite(self, x: int, y: int):
        """Mark position as valid move for white"""
        if 0 <= y < len(self.board_state) and 0 <= x < len(self.board_state[0]):
            self.board_state[y][x] = 'w'  # lowercase = valid move
    
    def setCanMoveBlack(self, x: int, y: int):
        """Mark position as valid move for black"""
        if 0 <= y < len(self.board_state) and 0 <= x < len(self.board_state[0]):
            self.board_state[y][x] = 'b'  # lowercase = valid move
    
    def setPlayerCounts(self, black_count: int, white_count: int):
        """Update player piece counts"""
        self.black_count = black_count
        self.white_count = white_count
        # Update move count (total pieces - 4 starting pieces)
        self.move_count = black_count + white_count - 4
    
    def setCanMoveBook(self, x: int, y: int, count: int):
        """Mark position as opening book move (terminal just marks as valid)"""
        # In terminal, just mark as valid move (no special book highlighting)
        if 0 <= y < len(self.board_state) and 0 <= x < len(self.board_state[0]):
            # Keep existing marker if it's a valid move
            pass
    
    def unfillBox(self, x: int, y: int):
        """Clear a box (alias for unsetBox)"""
        self.unsetBox(x, y)
    
    def setBox(self, x: int, y: int):
        """Set box (used by some legacy code)"""
        # For terminal view, this is handled by render_piece
        pass
    
    def setBoxWhite(self, x: int, y: int):
        """Set box to white piece"""
        if 0 <= y < len(self.board_state) and 0 <= x < len(self.board_state[0]):
            self.board_state[y][x] = 'W'
    
    def setBoxBlack(self, x: int, y: int):
        """Set box to black piece"""
        if 0 <= y < len(self.board_state) and 0 <= x < len(self.board_state[0]):
            self.board_state[y][x] = 'B'
    
    def setLastMove(self, x: int, y: int):
        """Set last move position (for highlighting)"""
        self.last_move_x = x
        self.last_move_y = y
    
    def cleanup(self):
        """Cleanup terminal"""
        self.clear_screen()
    
    # Compatibility methods for existing code
    
    def cursorHand(self):
        """No-op in terminal"""
        pass
    
    def cursorWait(self):
        """No-op in terminal"""
        pass
    
    def refresh(self):
        """Refresh display"""
        self._draw_board()
    
    def update(self, cursor_mode=False):
        """Update display"""
        self._draw_board()
    
    # AbstractBoardView required methods
    
    def set_cursor(self, x: int, y: int):
        """Implements AbstractBoardView.set_cursor"""
        self.cursorX = x
        self.cursorY = y
    
    def get_cursor_position(self) -> Tuple[Optional[int], Optional[int]]:
        """Implements AbstractBoardView.get_cursor_position"""
        return (self.cursorX, self.cursorY)
    
    def point_to_board_position(self, screen_x: int, screen_y: int) -> Tuple[Optional[int], Optional[int]]:
        """Implements AbstractBoardView.point_to_board_position"""
        return (None, None)  # Not applicable in terminal
    
    def set_player_info(self, black_name: str, white_name: str, 
                       black_count: int, white_count: int, current_turn: str):
        """Implements AbstractBoardView.set_player_info"""
        self.black_player_name = black_name
        self.white_player_name = white_name
        self.black_count = black_count
        self.white_count = white_count
        self.current_turn = current_turn
    
    # Compatibility methods for existing code
    
    def point2Box(self, x, y):
        """Point to box (not applicable in terminal)"""
        return (None, None)
    
    def setCursor(self, bx, by):
        """Set cursor position (compatibility)"""
        self.set_cursor(bx, by)
    
    def moveCursor(self, dx, dy):
        """Move cursor"""
        if self.cursorX is None:
            self.cursorX = 0
        if self.cursorY is None:
            self.cursorY = 0
        
        self.cursorX = max(0, min(self.sizex - 1, self.cursorX + dx))
        self.cursorY = max(0, min(self.sizey - 1, self.cursorY + dy))
    
    def getCursorPosition(self):
        """Get cursor position (compatibility)"""
        return self.get_cursor_position()
    
    def setPlayerNames(self, black_name, white_name):
        """Set player names (compatibility)"""
        self.black_player_name = black_name
        self.white_player_name = white_name
    
    def setPlayerCounts(self, black_count, white_count):
        """Set piece counts (compatibility)"""
        self.black_count = black_count
        self.white_count = white_count
        # Update move count (total pieces - 4 starting pieces)
        self.move_count = black_count + white_count - 4
    
    def setCurrentTurn(self, turn):
        """Set current turn (compatibility)"""
        self.current_turn = turn
    
    def drawHeader(self):
        """Draw header (included in board rendering)"""
        pass
    
    def set_opening_info(self, opening_names):
        """Set opening info (could display below board)"""
        if opening_names:
            print(f"{self.CYAN}Opening: {', '.join(opening_names[:3])}{self.RESET}")
    
    def clear_tooltip_area(self):
        """Clear tooltip (no-op)"""
        pass
    
    def draw_opening_info_fixed(self):
        """Draw opening info (no-op, info shown inline)"""
        pass

