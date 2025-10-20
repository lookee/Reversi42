"""PieceRenderer - Specialized piece rendering"""

import pygame

from ui.common import ColorPalette, Theme


class PieceRenderer:
    def __init__(self, theme: ColorPalette = Theme.PROFESSIONAL):
        self.theme = theme

    def render_piece(self, surface, center_x, center_y, color, radius):
        """Render a single piece with shadow and shine"""
        piece_color = self.theme.black_piece if color == "B" else self.theme.white_piece

        # Shadow
        pygame.draw.circle(surface, self.theme.board_shadow, (center_x + 2, center_y + 2), radius)

        # Piece
        pygame.draw.circle(surface, piece_color, (center_x, center_y), radius)

        # Shine
        pygame.draw.circle(
            surface,
            (255, 255, 255, 100),
            (center_x - radius // 3, center_y - radius // 3),
            radius // 4,
        )
