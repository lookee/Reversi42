"""
Widget - Base class for all UI components

Implements Composite Pattern foundation.
All UI elements inherit from Widget and can be composed hierarchically.

Design Pattern: Composite + Template Method
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

import pygame


class Widget(ABC):
    """
    Base widget class for all UI components.

    This is the Component in the Composite pattern.
    Provides common functionality for all widgets:
    - Position and size (rect)
    - Visibility and enabled state
    - Event handling
    - Rendering interface

    Subclasses must implement render() method.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        center_in_parent: bool = False,
    ):
        """
        Initialize widget.

        Args:
            x: X position (relative to parent)
            y: Y position (relative to parent)
            width: Widget width
            height: Widget height
            center_in_parent: If True, widget will be centered in its parent container
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
        self.parent: Optional["Widget"] = None
        self.center_in_parent = center_in_parent

        # Styling
        self.background_color: Optional[Tuple[int, int, int]] = None
        self.border_color: Optional[Tuple[int, int, int]] = None
        self.border_width: int = 0

        # State
        self.focused = False
        self.hovered = False

    @abstractmethod
    def render(self, surface: pygame.Surface):
        """
        Render this widget to the surface.

        Args:
            surface: Pygame surface to render on
        """
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event

        Returns:
            True if event was handled, False otherwise
        """
        if not self.enabled or not self.visible:
            return False

        # Check for mouse hover
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.contains_point(event.pos[0], event.pos[1])

        return False

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if point is inside this widget.

        Args:
            x: Screen X coordinate
            y: Screen Y coordinate

        Returns:
            True if point is inside widget bounds
        """
        # Use absolute rect for collision detection
        abs_rect = self.get_absolute_rect()
        return abs_rect.collidepoint(x, y)

    def get_absolute_rect(self) -> pygame.Rect:
        """
        Get absolute screen rectangle (including parent offsets).

        Returns:
            Absolute screen rect
        """
        if self.parent:
            parent_rect = self.parent.get_absolute_rect()
            return pygame.Rect(
                parent_rect.x + self.rect.x,
                parent_rect.y + self.rect.y,
                self.rect.width,
                self.rect.height,
            )
        return self.rect.copy()

    def set_position(self, x: int, y: int):
        """Set widget position."""
        self.rect.x = x
        self.rect.y = y

    def set_size(self, width: int, height: int):
        """Set widget size."""
        self.rect.width = width
        self.rect.height = height

    def show(self):
        """Make widget visible."""
        self.visible = True

    def hide(self):
        """Make widget invisible."""
        self.visible = False

    def enable(self):
        """Enable widget interaction."""
        self.enabled = True

    def disable(self):
        """Disable widget interaction."""
        self.enabled = False

    def _render_background(self, surface: pygame.Surface):
        """
        Render widget background if set.

        Helper method for subclasses.
        """
        if self.background_color:
            pygame.draw.rect(surface, self.background_color, self.rect)

        if self.border_color and self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
