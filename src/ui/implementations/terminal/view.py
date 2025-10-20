"""
TerminalBoardView - Refactored with MVP Pattern

Reduces from 473 LoC → ~150 LoC by applying MVP!

Architecture:
- Model: Board state (in Presenter)
- View: This class (thin rendering layer)
- Presenter: TerminalPresenter (business logic)

Design Patterns:
- MVP (separation of concerns)
- Strategy (ASCIIRenderer, ASCIITheme)
- Dependency Injection (Renderer, Theme, Presenter)
"""

import os
import sys

# Add path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from typing import Any, Dict, List, Optional, Tuple

from Board.AbstractBoardView import AbstractBoardView

from .presenters import TerminalPresenter
from .renderers import ASCIIRenderer, ASCIITheme


class TerminalBoardView(AbstractBoardView):
    """
    Terminal-based ASCII art view (MVP refactored).

    Reduced from 473 LoC to ~150 LoC!

    Features:
    - MVP pattern (testable presenter!)
    - ASCIIRenderer (separation of concerns)
    - Theme support (3 presets)
    - Backward compatible API
    """

    def __init__(self, sizex=8, sizey=8, width=80, height=24, theme: Optional[Any] = None):
        """
        Initialize terminal view.

        Args:
            sizex: Board width
            sizey: Board height
            width: Terminal width (unused in terminal)
            height: Terminal height (unused in terminal)
            theme: ASCIIColorScheme (default: CLASSIC)
        """
        super().__init__(sizex, sizey, width, height)

        # MVP Pattern: Inject dependencies
        self.theme = theme or ASCIITheme.CLASSIC
        self.renderer = ASCIIRenderer(self.theme)
        self.presenter = TerminalPresenter(board_size=sizex)

        # Output tracking
        self.last_output_lines = 0

    def initialize(self):
        """Initialize the view (required by AbstractBoardView)"""
        self.clear_screen()

    def clear_screen(self):
        """Clear terminal screen"""
        print(self.renderer.clear_screen(), end="")

    def render_board(self, model: Any):
        """
        Render board from model.

        Args:
            model: BoardModel instance
        """
        # MVP: Update presenter from model
        self.presenter.update_from_model(model)
        self.update_display()

    def update_display(self, cursor_mode: bool = False):
        """
        Update the terminal display.

        Args:
            cursor_mode: Whether to show cursor (unused in terminal)
        """
        # MVP: Get data from presenter
        data = self.presenter.get_render_data()

        # Clear previous output
        self.clear_screen()

        # Render header
        header = self.renderer.render_header(
            turn=data["current_turn"],
            black_count=data["black_count"],
            white_count=data["white_count"],
            move_count=data["move_count"],
            black_name=data["black_player_name"],
            white_name=data["white_player_name"],
        )
        print(header)

        # Render board
        board = self.renderer.render_board(
            board_state=data["board_state"],
            valid_moves=data["valid_moves"],
            last_move=data["last_move"],
            book_moves=data["book_moves"],
        )
        print(board)

        # Render book info (compact, single line)
        book_info_parts = []

        # Opening name (if available)
        if data["opening_name"]:
            opening_info = self.renderer.render_opening_info(
                data["opening_name"], data["opening_variation"] or ""
            )
            book_info_parts.append(opening_info)

        # Book moves summary (compact)
        if data["book_moves"]:
            book_summary = self.renderer.render_book_moves_summary(data["book_moves"])
            book_info_parts.append(book_summary)

        # Print on single line (compact!)
        if book_info_parts:
            print("  ".join(book_info_parts))

    # ============================================================
    # AbstractBoardView interface (backward compatibility)
    # ============================================================

    def setBoxWhite(self, x: int, y: int):
        """Set white piece (AbstractBoardView API)"""
        self.presenter.set_piece(x, y, "O")

    def setBoxBlack(self, x: int, y: int):
        """Set black piece (AbstractBoardView API)"""
        self.presenter.set_piece(x, y, "X")

    def unfillBox(self, x: int, y: int):
        """Clear piece (AbstractBoardView API)"""
        self.presenter.clear_piece(x, y)

    def unsetBox(self, x: int, y: int):
        """Clear piece - alias for unfillBox (backward compatibility)"""
        self.unfillBox(x, y)

    def setBox(self, x: int, y: int, color: str = "X"):
        """Set piece with color (backward compatibility)"""
        self.presenter.set_piece(x, y, color)

    def setCanMoveWhite(self, x: int, y: int):
        """Mark as valid move for white"""
        if (x, y) not in self.presenter.valid_moves:
            self.presenter.valid_moves.append((x, y))

    def setCanMoveBlack(self, x: int, y: int):
        """Mark as valid move for black"""
        if (x, y) not in self.presenter.valid_moves:
            self.presenter.valid_moves.append((x, y))

    def setLastMove(self, x: int, y: int):
        """Set last move position"""
        self.presenter.set_last_move(x, y)

    def setPlayerCounts(self, black_count: int, white_count: int):
        """Update piece counts"""
        self.presenter.set_player_counts(black_count, white_count)

    def setPlayerNames(self, black_name: str, white_name: str):
        """Update player names"""
        self.presenter.set_player_names(black_name, white_name)

    def setCurrentTurn(self, turn: str):
        """Update current turn"""
        self.presenter.set_current_turn(turn)

    def set_opening_info(self, opening_info):
        """
        Set opening book information (handles multiple formats for compatibility).

        Formats supported:
        - Dict: {'name': '...', 'variation': '...'}
        - List of tuples: [('C4', ['C4: Opening1', 'C4: Opening2']), ...]
        - Simple list: ['name', 'variation'] or ['name']
        - String: 'name'
        - None
        """
        if not opening_info:
            self.presenter.clear_opening_info()
            return

        # Handle list of tuples format (from BoardControl with all variations)
        if isinstance(opening_info, list) and len(opening_info) > 0:
            # Check if it's list of tuples [(move, [openings])]
            if isinstance(opening_info[0], tuple) and len(opening_info[0]) == 2:
                # Extract FIRST opening name only (most common/important)
                move_str, opening_names = opening_info[0]
                if opening_names and len(opening_names) > 0:
                    # Take first opening, extract name (remove "C4: " prefix)
                    first_opening = opening_names[0]
                    if ": " in first_opening:
                        name = first_opening.split(": ", 1)[1]
                    else:
                        name = first_opening

                    # Count total variations
                    total_variations = sum(len(openings) for _, openings in opening_info)
                    variation = (
                        f"{len(opening_info)} moves, {total_variations} variations"
                        if total_variations > 1
                        else ""
                    )
                else:
                    name = "Opening Book"
                    variation = ""
            # Simple list format: [name, variation] or [name]
            elif isinstance(opening_info[0], str):
                name = str(opening_info[0])
                variation = str(opening_info[1]) if len(opening_info) > 1 else ""
            else:
                name = "Opening Book"
                variation = ""
        # Handle dict format
        elif isinstance(opening_info, dict):
            name = opening_info.get("name", "")
            variation = opening_info.get("variation", "")
        # Handle string format
        else:
            name = str(opening_info)
            variation = ""

        self.presenter.set_opening_info(name, variation)

    def setCanMoveBook(self, x: int, y: int, count: int):
        """Set opening book move with count"""
        self.presenter.book_moves[(x, y)] = count

    def clear_book_moves(self):
        """Clear all book moves"""
        self.presenter.clear_book_moves()

    def refresh(self):
        """Refresh display"""
        self.update_display()

    def update(self, cursor_mode=False):
        """Update display (alias for refresh)"""
        self.update_display(cursor_mode)

    # ============================================================
    # Abstract methods implementation (required by AbstractBoardView)
    # ============================================================

    def render_piece(self, x: int, y: int, color: str):
        """Render a piece at position (AbstractBoardView API)"""
        if color == "X":
            self.presenter.set_piece(x, y, "X")
        elif color == "O":
            self.presenter.set_piece(x, y, "O")

    def highlight_valid_moves(self, moves: List):
        """Highlight valid moves (AbstractBoardView API)"""
        move_coords = [(m.x - 1, m.y - 1) for m in moves if hasattr(m, "x")]
        self.presenter.set_valid_moves(move_coords)

    def highlight_last_move(self, x: int, y: int):
        """Highlight last move (AbstractBoardView API)"""
        self.presenter.set_last_move(x, y)

    def clear_display(self):
        """Clear the display"""
        self.clear_screen()

    def show_message(self, message: str, duration: float = 2.0):
        """Show a message (AbstractBoardView API)"""
        msg = self.renderer.render_message(message, "info")
        print(f"\n{msg}")

    def resize(self, width: int, height: int):
        """Resize terminal (no-op for terminal)"""
        pass

    def set_player_info(
        self, black_name: str, white_name: str, black_count: int, white_count: int, turn: str
    ):
        """Set player information (AbstractBoardView API)"""
        self.presenter.set_player_names(black_name, white_name)
        self.presenter.set_player_counts(black_count, white_count)
        self.presenter.set_current_turn(turn)

    def point_to_board_position(
        self, screen_x: int, screen_y: int
    ) -> Tuple[Optional[int], Optional[int]]:
        """Convert screen coords to board coords (not used in terminal)"""
        return None, None

    # Cursor methods (not used in terminal, for compatibility)
    def cursorHand(self):
        """Cursor hand mode (unused in terminal)"""
        pass

    def cursorWait(self):
        """Cursor wait mode (unused in terminal)"""
        pass

    def set_cursor(self, x: int, y: int):
        """Set cursor position (unused in terminal)"""
        pass

    def setCursor(self, x: int, y: int):
        """Set cursor position - camelCase for backward compatibility"""
        pass

    def moveCursor(self, dx: int, dy: int):
        """Move cursor (unused in terminal)"""
        pass

    def getCursorPosition(self) -> Tuple[Optional[int], Optional[int]]:
        """Get cursor position - camelCase for backward compatibility"""
        return None, None

    def get_cursor_position(self) -> Tuple[Optional[int], Optional[int]]:
        """Get cursor position (unused in terminal)"""
        return None, None

    def point2Box(self, x, y):
        """Convert point to box (unused in terminal)"""
        return None, None

    def drawHeader(self):
        """Draw header (handled in update_display)"""
        pass

    def clear_tooltip_area(self):
        """Clear tooltip area (unused in terminal)"""
        pass

    def draw_opening_info_fixed(self):
        """Draw opening info (handled in update_display)"""
        pass

    def cleanup(self):
        """Cleanup resources"""
        pass
