"""BoardRenderer - Specialized board grid rendering"""
import pygame
from ui.common import ColorPalette, Theme

class BoardRenderer:
    def __init__(self, theme: ColorPalette = Theme.PROFESSIONAL):
        self.theme = theme
    
    def render_grid(self, surface, rect, size=8):
        """Render board grid"""
        cell_size = rect.width // size
        pygame.draw.rect(surface, self.theme.board_background, rect)
        
        for i in range(size + 1):
            y = rect.y + i * cell_size
            pygame.draw.line(surface, self.theme.board_lines, (rect.x, y), (rect.x + rect.width, y), 2)
            x = rect.x + i * cell_size
            pygame.draw.line(surface, self.theme.board_lines, (x, rect.y), (x, rect.y + rect.height), 2)
    
    def render_hoshi(self, surface, rect, size=8):
        """Render hoshi points"""
        cell_size = rect.width // size
        for hx, hy in [(2, 2), (2, 5), (5, 2), (5, 5)]:
            cx = rect.x + hx * cell_size + cell_size // 2
            cy = rect.y + hy * cell_size + cell_size // 2
            pygame.draw.circle(surface, self.theme.board_hoshi, (cx, cy), 4)

