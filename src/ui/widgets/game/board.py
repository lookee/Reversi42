"""
BoardWidget - Reversi board visualization component

Encapsulates all board rendering logic in a reusable component.

Design Pattern: Composite
"""

from typing import List, Optional, Tuple

import pygame

from ui.common import ColorPalette, Theme
from ui.widgets.base import Grid


class BoardWidget(Grid):
    """
    Reversi board widget.

    Features:
    - Grid-based layout (8x8)
    - Piece rendering
    - Legal move indicators
    - Last move highlighting
    - Opening book move highlighting
    - Cursor support
    - Theme support

    This widget handles ONLY board visualization.
    Game logic is handled by the Presenter.
    """

    def __init__(
        self, size: int = 8, cell_size: int = 50, theme: ColorPalette = Theme.PROFESSIONAL
    ):
        """
        Initialize board widget.

        Args:
            size: Board size (8x8)
            cell_size: Size of each cell in pixels
            theme: Color theme
        """
        super().__init__(rows=size, cols=size, cell_width=cell_size, cell_height=cell_size)

        self.size = size
        self.cell_size = cell_size
        self.theme = theme

        # Board state (set by Presenter)
        self.board_state: List[List[str]] = [["." for _ in range(size)] for _ in range(size)]
        self.legal_moves: List[Tuple[int, int]] = []
        self.last_move: Optional[Tuple[int, int]] = None
        self.book_moves: List[Tuple[int, int]] = []
        self.cursor_pos: Optional[Tuple[int, int]] = None

    def set_board_state(self, state: List[List[str]]):
        """
        Set board state (called by Presenter).

        Args:
            state: 2D array of '.' (empty), 'B' (black), 'W' (white)
        """
        self.board_state = state

    def set_legal_moves(self, moves: List[Tuple[int, int]]):
        """Set legal moves to highlight."""
        self.legal_moves = moves

    def set_last_move(self, pos: Optional[Tuple[int, int]]):
        """Set last move position."""
        self.last_move = pos

    def set_book_moves(self, moves: List[Tuple[int, int]]):
        """Set opening book moves to highlight."""
        self.book_moves = moves

    def set_cursor(self, pos: Optional[Tuple[int, int]]):
        """Set cursor position."""
        self.cursor_pos = pos

    def render(self, surface: pygame.Surface):
        """Render complete board."""
        if not self.visible:
            return

        # Draw grid
        self._draw_grid(surface)

        # Draw hoshi points (guide dots)
        self._draw_hoshi(surface)

        # Draw legal move indicators
        self._draw_legal_moves(surface)

        # Draw book move indicators
        self._draw_book_moves(surface)

        # Draw pieces
        self._draw_pieces(surface)

        # Draw last move indicator
        self._draw_last_move(surface)

        # Draw cursor
        self._draw_cursor(surface)

    def _draw_grid(self, surface: pygame.Surface):
        """Draw board grid."""
        # Background
        pygame.draw.rect(surface, self.theme.board_background, self.rect)

        # Grid lines
        for i in range(self.size + 1):
            # Horizontal lines
            y = self.rect.y + i * self.cell_size
            pygame.draw.line(
                surface,
                self.theme.board_lines,
                (self.rect.x, y),
                (self.rect.x + self.rect.width, y),
                2,
            )

            # Vertical lines
            x = self.rect.x + i * self.cell_size
            pygame.draw.line(
                surface,
                self.theme.board_lines,
                (x, self.rect.y),
                (x, self.rect.y + self.rect.height),
                2,
            )

    def _draw_hoshi(self, surface: pygame.Surface):
        """Draw hoshi points (guide dots)."""
        hoshi_positions = [(2, 2), (2, 5), (5, 2), (5, 5)]
        for hx, hy in hoshi_positions:
            center_x = self.rect.x + hx * self.cell_size + self.cell_size // 2
            center_y = self.rect.y + hy * self.cell_size + self.cell_size // 2
            pygame.draw.circle(surface, self.theme.board_hoshi, (center_x, center_y), 4)

    def _draw_legal_moves(self, surface: pygame.Surface):
        """Draw legal move indicators."""
        for bx, by in self.legal_moves:
            center_x = self.rect.x + bx * self.cell_size + self.cell_size // 2
            center_y = self.rect.y + by * self.cell_size + self.cell_size // 2
            pygame.draw.circle(
                surface, self.theme.legal_move, (center_x, center_y), self.cell_size // 6, 2
            )

    def _draw_book_moves(self, surface: pygame.Surface):
        """Draw opening book move indicators."""
        for bx, by in self.book_moves:
            x = self.rect.x + bx * self.cell_size
            y = self.rect.y + by * self.cell_size
            pygame.draw.rect(
                surface,
                self.theme.book_move,
                (x + 2, y + 2, self.cell_size - 4, self.cell_size - 4),
                3,
            )

    def _draw_pieces(self, surface: pygame.Surface):
        """Draw all pieces on the board."""
        for by in range(self.size):
            for bx in range(self.size):
                piece = self.board_state[by][bx]
                if piece != ".":
                    center_x = self.rect.x + bx * self.cell_size + self.cell_size // 2
                    center_y = self.rect.y + by * self.cell_size + self.cell_size // 2
                    radius = int(self.cell_size * 0.4)

                    color = self.theme.black_piece if piece == "B" else self.theme.white_piece

                    # Draw shadow
                    shadow_offset = 2
                    pygame.draw.circle(
                        surface,
                        self.theme.board_shadow,
                        (center_x + shadow_offset, center_y + shadow_offset),
                        radius,
                    )

                    # Draw piece
                    pygame.draw.circle(surface, color, (center_x, center_y), radius)

                    # Draw highlight/shine
                    shine_offset = radius // 3
                    pygame.draw.circle(
                        surface,
                        (255, 255, 255, 100),
                        (center_x - shine_offset, center_y - shine_offset),
                        radius // 4,
                    )

    def _draw_last_move(self, surface: pygame.Surface):
        """Draw last move indicator."""
        if self.last_move:
            bx, by = self.last_move
            center_x = self.rect.x + bx * self.cell_size + self.cell_size // 2
            center_y = self.rect.y + by * self.cell_size + self.cell_size // 2
            pygame.draw.circle(
                surface, self.theme.last_move, (center_x, center_y), int(self.cell_size * 0.48), 3
            )

    def _draw_cursor(self, surface: pygame.Surface):
        """Draw cursor if active."""
        if self.cursor_pos:
            bx, by = self.cursor_pos
            x = self.rect.x + bx * self.cell_size
            y = self.rect.y + by * self.cell_size
            pygame.draw.rect(
                surface,
                self.theme.cursor,
                (x + 4, y + 4, self.cell_size - 8, self.cell_size - 8),
                3,
            )
