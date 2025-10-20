"""
Label Widget - Text display component

Simple text label with customizable font, size, and color.

Design Pattern: Component
"""

from typing import Optional, Tuple

import pygame

from ui.widgets.base import Widget


def Title(text: str, font_size: int = 48, color: Tuple[int, int, int] = (230, 240, 235)):
    """
    Create a centered title label.
    
    Convenience function that creates a Label with center_in_parent=True
    and title-appropriate styling.
    
    Args:
        text: Title text
        font_size: Font size (default: 48)
        color: Text color (default: light color)
    
    Returns:
        Label configured as a centered title
    
    Example:
        layout = Stack()
        layout.add(Title("Game Menu"))  # Auto-centered!
        layout.add(Button("Start"))
    """
    label = Label(text, font_size=font_size, color=color)
    label.center_in_parent = True
    return label


class Label(Widget):
    """
    Text label widget.

    Features:
    - Customizable font and size
    - Text alignment
    - Color support
    - Auto-sizing

    Usage:
        label = Label("Score: 34")
        label.render(surface)
    """

    def __init__(
        self,
        text: str,
        x: int = 0,
        y: int = 0,
        font_size: int = 24,
        color: Tuple[int, int, int] = (240, 240, 245),
    ):
        """
        Initialize label.

        Args:
            text: Label text
            x, y: Position
            font_size: Font size in pixels
            color: Text color (RGB)
        """
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.bold = False
        self.italic = False

        # Calculate size from text
        text_surface = self.font.render(text, True, color)
        width, height = text_surface.get_size()

        super().__init__(x, y, width, height)

    def render(self, surface: pygame.Surface):
        """Render label."""
        if not self.visible:
            return

        # Get absolute rect for rendering
        abs_rect = self.get_absolute_rect()

        # Render text
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, (abs_rect.x, abs_rect.y))

    def set_text(self, text: str):
        """
        Update label text and resize.

        Args:
            text: New text
        """
        self.text = text
        text_surface = self.font.render(text, True, self.color)
        self.rect.width, self.rect.height = text_surface.get_size()

    def set_color(self, color: Tuple[int, int, int]):
        """
        Set text color.

        Args:
            color: RGB color tuple
        """
        self.color = color

    def set_font_size(self, size: int):
        """
        Set font size.

        Args:
            size: Font size in pixels
        """
        self.font_size = size
        self.font = pygame.font.Font(None, size)
        # Recalculate size
        self.set_text(self.text)
