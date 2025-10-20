"""MoveIndicator - Simple move indicator"""

import pygame

from ui.widgets.base import Widget


class MoveIndicator(Widget):
    def __init__(self, x, y, radius=10, color=(180, 220, 190)):
        super().__init__(x, y, radius * 2, radius * 2)
        self.radius = radius
        self.color = color

    def render(self, surface):
        if self.visible:
            pygame.draw.circle(surface, self.color, self.rect.center, self.radius, 2)
