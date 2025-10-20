"""UIRenderer - UI elements rendering"""

import pygame

from ui.common import ColorPalette, Theme


class UIRenderer:
    def __init__(self, theme: ColorPalette = Theme.PROFESSIONAL):
        self.theme = theme
        self.font = pygame.font.Font(None, 24)

    def render_text(self, surface, text, x, y, color=None):
        """Render text at position"""
        color = color or self.theme.ui_text
        text_surf = self.font.render(text, True, color)
        surface.blit(text_surf, (x, y))
        return text_surf.get_rect(topleft=(x, y))

    def render_panel(self, surface, rect, bg_color=None, border_color=None):
        """Render UI panel"""
        bg = bg_color or self.theme.ui_background
        border = border_color or self.theme.ui_accent
        pygame.draw.rect(surface, bg, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, 2, border_radius=8)
