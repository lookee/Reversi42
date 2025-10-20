"""
Panel Widget - Container with background and border

Decorated container for grouping related widgets visually.

Design Pattern: Decorator (adds visual styling to Container)
"""

from typing import Optional, Tuple

import pygame

from ui.widgets.base import Container


class Panel(Container):
    """
    Panel widget - container with styled background.

    Features:
    - Colored background
    - Border
    - Padding
    - Shadow (optional)

    Usage:
        panel = Panel(width=300, height=200)
        panel.add(Label("Title"))
        panel.add(Button("OK"))
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 200,
        height: int = 100,
        background_color: Optional[Tuple[int, int, int]] = None,
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 2,
    ):
        """
        Initialize panel.

        Args:
            x, y: Position
            width, height: Size
            background_color: Background color (None = transparent)
            border_color: Border color (None = no border)
            border_width: Border width in pixels
        """
        super().__init__(x, y, width, height)

        self.background_color = background_color or (40, 40, 45)
        self.border_color = border_color or (80, 80, 90)
        self.border_width = border_width
        self.border_radius = 8
        self.shadow = True
        self.shadow_offset = 3
        self.shadow_color = (0, 0, 0, 128)  # Semi-transparent

    def render(self, surface: pygame.Surface):
        """Render panel with background, border, and children."""
        if not self.visible:
            return

        # Draw shadow if enabled
        if self.shadow:
            shadow_rect = self.rect.move(self.shadow_offset, self.shadow_offset)
            shadow_surface = pygame.Surface(
                (shadow_rect.width, shadow_rect.height), pygame.SRCALPHA
            )
            pygame.draw.rect(
                shadow_surface,
                self.shadow_color,
                shadow_surface.get_rect(),
                border_radius=self.border_radius,
            )
            surface.blit(shadow_surface, shadow_rect)

        # Draw background
        pygame.draw.rect(
            surface, self.background_color, self.rect, border_radius=self.border_radius
        )

        # Draw border
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(
                surface,
                self.border_color,
                self.rect,
                self.border_width,
                border_radius=self.border_radius,
            )

        # Render children
        for child in self.children:
            if child.visible:
                child.render(surface)
