"""
Button Widget - Clickable button component

Standard button with hover effects, click handling, and customizable appearance.

Design Pattern: Command (via callback)
"""

from typing import Callable, Optional, Tuple

import pygame

from ui.widgets.base import Clickable, Hoverable, Widget


class Button(Widget, Clickable, Hoverable):
    """
    Clickable button widget.

    Features:
    - Hover effects
    - Click feedback
    - Customizable colors
    - Text rendering
    - Sound support

    Usage:
        button = Button("Start Game", on_click=start_game)
        button.render(surface)
    """

    def __init__(
        self,
        text: str,
        x: int = 0,
        y: int = 0,
        width: int = 150,
        height: int = 40,
        on_click: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize button.

        Args:
            text: Button text
            x, y: Position
            width, height: Size
            on_click: Click callback
            **kwargs: Additional arguments (color, text_color, hover_color) - ignored for backward compatibility
        """
        Widget.__init__(self, x, y, width, height)
        Clickable.__init__(self, on_click)
        Hoverable.__init__(self)

        self.text = text
        self.font = pygame.font.Font(None, 28)

        # Colors (defaults)
        self.color_normal = kwargs.get('color', (60, 60, 70))
        self.color_hover = kwargs.get('hover_color', (80, 80, 90))
        self.color_pressed = (40, 40, 50)
        self.color_text = kwargs.get('text_color', (240, 240, 245))
        self.color_border = (100, 100, 110)

    def render(self, surface: pygame.Surface):
        """Render button with current state."""
        if not self.visible:
            return

        # Get absolute rect for rendering
        abs_rect = self.get_absolute_rect()

        # Determine color based on state
        if self.pressed:
            color = self.color_pressed
        elif self.hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        # Draw button background
        pygame.draw.rect(surface, color, abs_rect, border_radius=5)
        pygame.draw.rect(surface, self.color_border, abs_rect, 2, border_radius=5)

        # Render text centered
        text_surface = self.font.render(self.text, True, self.color_text)
        text_rect = text_surface.get_rect(center=abs_rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events."""
        if not self.enabled or not self.visible:
            return False

        # Handle hover
        self.handle_hover_event(event)

        # Handle click
        return self.handle_click_event(event)

    def set_text(self, text: str):
        """Update button text."""
        self.text = text
