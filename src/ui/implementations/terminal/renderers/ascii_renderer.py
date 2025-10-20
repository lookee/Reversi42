"""
ASCIIRenderer - Terminal rendering engine

Handles all ASCII/Unicode rendering for terminal UI.
Extracted from TerminalBoardView for separation of concerns.

Design Pattern: Strategy (rendering strategy for terminal)
"""

from typing import Dict, List, Optional, Tuple

from .ascii_theme import ANSIColors, ASCIIColorScheme, ASCIITheme


class ASCIIRenderer:
    """
    ASCII/Unicode renderer for terminal.

    Handles:
    - Board grid rendering
    - Piece rendering
    - UI elements (header, scores, etc.)
    - Highlights (valid moves, last move, book moves)

    Similar to pygame BoardRenderer but for terminal.
    """

    # Unicode box drawing characters
    BOX_H = "─"
    BOX_V = "│"
    BOX_TL = "┌"
    BOX_TR = "┐"
    BOX_BL = "└"
    BOX_BR = "┘"
    BOX_CROSS = "┼"
    BOX_T_DOWN = "┬"
    BOX_T_UP = "┴"
    BOX_T_RIGHT = "├"
    BOX_T_LEFT = "┤"

    def __init__(self, theme: ASCIIColorScheme = ASCIITheme.CLASSIC):
        """
        Initialize renderer.

        Args:
            theme: Color scheme to use
        """
        self.theme = theme
        self.reset = ANSIColors.RESET if theme.use_colors else ""

    def render_header(
        self,
        turn: str,
        black_count: int,
        white_count: int,
        move_count: int,
        black_name: str = "Black",
        white_name: str = "White",
    ) -> str:
        """
        Render game header with scores and turn info.

        Args:
            turn: Current turn ('X' or 'O')
            black_count: Black piece count
            white_count: White piece count
            move_count: Current move number
            black_name: Black player name
            white_name: White player name

        Returns:
            Formatted header string
        """
        if self.theme.use_colors:
            header = f"{self.theme.header_bg}{self.theme.header_text}"
            header += f" Reversi42 - Move {move_count} {self.reset}\n"
            header += f"{self.theme.score_text}"
            header += f"{black_name}: {black_count} {self.theme.black_piece}  "
            header += f"{white_name}: {white_count} {self.theme.white_piece}  "
            header += f"{self.theme.turn_indicator}Turn: {turn}{self.reset}\n"
        else:
            header = f"Reversi42 - Move {move_count}\n"
            header += f"{black_name}: {black_count} {self.theme.black_piece}  "
            header += f"{white_name}: {white_count} {self.theme.white_piece}  "
            header += f"Turn: {turn}\n"

        return header

    def render_board(
        self,
        board_state: List[List[str]],
        valid_moves: Optional[List[Tuple[int, int]]] = None,
        last_move: Optional[Tuple[int, int]] = None,
        book_moves: Optional[Dict[Tuple[int, int], int]] = None,
    ) -> str:
        """
        Render the board with pieces and highlights.

        Args:
            board_state: 2D array of board state ('X', 'O', ' ')
            valid_moves: List of valid move coordinates
            last_move: Last move coordinates (x, y)
            book_moves: Dict of book moves with counts

        Returns:
            Formatted board string
        """
        size = len(board_state)
        lines = []

        # Column coordinates
        col_line = self._render_column_coords(size)
        lines.append(col_line)

        # Top border
        border = self._render_top_border(size)
        lines.append(border)

        # Board rows
        for y in range(size):
            row = self._render_row(y, board_state, valid_moves, last_move, book_moves)
            lines.append(row)

            # Middle border (except last row)
            if y < size - 1:
                middle = self._render_middle_border(size)
                lines.append(middle)

        # Bottom border
        bottom = self._render_bottom_border(size)
        lines.append(bottom)

        return "\n".join(lines)

    def _render_column_coords(self, size: int) -> str:
        """Render column coordinate letters (A-H for chess notation)"""
        # Align with border and cells
        # Row number takes 2 chars ("1 "), then border starts
        # Each cell is " content " = 3 chars between │ symbols
        # So each column section is │ + 3 chars = 4 chars total
        line = self.theme.coordinates + "   "  # 3 spaces for better alignment
        for x in range(size):
            # Use letters A-H (chess notation)
            letter = chr(ord("A") + x)
            # Better centered: 1 left + letter + 2 right
            line += f" {letter}  "  # 1 space + letter + 2 spaces = 4 chars (più spazio a destra)
        line += self.reset
        return line

    def _render_top_border(self, size: int) -> str:
        """Render top border of board"""
        line = self.theme.board_border
        line += f"  {self.BOX_TL}"
        for x in range(size):
            line += self.BOX_H * 3
            if x < size - 1:
                line += self.BOX_T_DOWN
        line += self.BOX_TR
        line += self.reset
        return line

    def _render_middle_border(self, size: int) -> str:
        """Render middle border between rows"""
        line = self.theme.board_grid
        line += f"  {self.BOX_T_RIGHT}"
        for x in range(size):
            line += self.BOX_H * 3
            if x < size - 1:
                line += self.BOX_CROSS
        line += self.BOX_T_LEFT
        line += self.reset
        return line

    def _render_bottom_border(self, size: int) -> str:
        """Render bottom border of board"""
        line = self.theme.board_border
        line += f"  {self.BOX_BL}"
        for x in range(size):
            line += self.BOX_H * 3
            if x < size - 1:
                line += self.BOX_T_UP
        line += self.BOX_BR
        line += self.reset
        return line

    def _render_row(
        self,
        y: int,
        board_state: List[List[str]],
        valid_moves: Optional[List[Tuple[int, int]]] = None,
        last_move: Optional[Tuple[int, int]] = None,
        book_moves: Optional[Dict[Tuple[int, int], int]] = None,
    ) -> str:
        """Render a single row"""
        size = len(board_state)

        # Row coordinate
        line = self.theme.coordinates + f"{y + 1} " + self.reset
        line += self.theme.board_grid + self.BOX_V + self.reset

        for x in range(size):
            cell_content = self._render_cell(x, y, board_state, valid_moves, last_move, book_moves)
            line += cell_content
            line += self.theme.board_grid + self.BOX_V + self.reset

        return line

    def _render_cell(
        self,
        x: int,
        y: int,
        board_state: List[List[str]],
        valid_moves: Optional[List[Tuple[int, int]]] = None,
        last_move: Optional[Tuple[int, int]] = None,
        book_moves: Optional[Dict[Tuple[int, int], int]] = None,
    ) -> str:
        """Render a single cell"""
        piece = board_state[y][x]
        is_valid_move = valid_moves and (x, y) in valid_moves
        is_last_move = last_move and last_move == (x, y)
        is_book_move = book_moves and (x, y) in book_moves

        # Determine cell content
        if piece == "X":  # Black piece
            content = self.theme.black_piece
        elif piece == "O":  # White piece
            content = self.theme.white_piece
        elif is_book_move:
            # COMPATTO: Mostra solo simbolo speciale invece di numero
            # Rank by popularity: ★ for top 3, ✦ for others
            count = book_moves[(x, y)]

            # Get ranking (top 3 get star, others get dot)
            sorted_moves = sorted(book_moves.items(), key=lambda x: x[1], reverse=True)
            rank = next(
                (i for i, ((mx, my), _) in enumerate(sorted_moves) if (mx, my) == (x, y)), 999
            )

            if rank < 3:
                # Top 3: Show star (most popular)
                content = f"{self.theme.book_move}★{self.reset}"
            else:
                # Others: Show count only if <= 9, otherwise •
                if count <= 9:
                    content = f"{self.theme.book_move}{count}{self.reset}"
                else:
                    content = f"{self.theme.book_move}•{self.reset}"
        elif is_valid_move:
            content = f"{self.theme.valid_move}·{self.reset}"
        else:
            content = self.theme.empty_cell

        # Apply last move highlight
        if is_last_move and self.theme.use_colors:
            content = f"{self.theme.last_move}{content}{self.reset}"

        # Center content in cell (3 chars wide)
        return f" {content} "

    def render_opening_info(self, opening_name: str, variation: str = "") -> str:
        """
        Render opening book information (compact version).

        Args:
            opening_name: Name of the opening
            variation: Variation name (optional)

        Returns:
            Formatted opening info string (compact, single line)
        """
        if self.theme.use_colors:
            # Compact single line with icon
            info = f"{self.theme.book_move}📖 {opening_name}"
            if variation:
                info += f" • {variation}"
            info += self.reset
        else:
            # Pure ASCII, compact
            info = f"Book: {opening_name}"
            if variation:
                info += f" | {variation}"

        return info

    def render_book_moves_summary(self, book_moves: Dict[Tuple[int, int], int]) -> str:
        """
        Render compact summary of available book moves.

        Args:
            book_moves: Dict mapping (x, y) to occurrence count

        Returns:
            Compact single-line summary of book moves
        """
        if not book_moves:
            return ""

        # Sort by count (most popular first)
        sorted_moves = sorted(book_moves.items(), key=lambda x: x[1], reverse=True)

        # Format: "C3(15) E6(8) F5(3)" - position and count
        move_strs = []
        for (x, y), count in sorted_moves[:5]:  # Show top 5
            # Convert to chess notation (A1, B2, etc.)
            col = chr(ord("A") + x)
            row = y + 1
            move_strs.append(f"{col}{row}({count})")

        if self.theme.use_colors:
            summary = f"{self.theme.book_move}📚 Book moves: {' '.join(move_strs)}"
            if len(sorted_moves) > 5:
                summary += f" +{len(sorted_moves) - 5} more"
            summary += self.reset
        else:
            summary = f"Book: {' '.join(move_strs)}"
            if len(sorted_moves) > 5:
                summary += f" +{len(sorted_moves) - 5}"

        return summary

    def render_message(self, message: str, msg_type: str = "info") -> str:
        """
        Render a status message.

        Args:
            message: Message text
            msg_type: Type of message ("info", "warning", "error")

        Returns:
            Formatted message string
        """
        if not self.theme.use_colors:
            return message

        if msg_type == "warning":
            return f"{self.theme.warning_text}⚠️  {message}{self.reset}"
        elif msg_type == "error":
            return f"{self.theme.error_text}❌ {message}{self.reset}"
        else:
            return f"{self.theme.info_text}ℹ️  {message}{self.reset}"

    def clear_screen(self) -> str:
        """Return ANSI clear screen sequence"""
        return "\033[2J\033[H" if self.theme.use_colors else "\n" * 50
