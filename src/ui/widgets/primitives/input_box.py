"""
InputBox Widget - Text input component

Text input field with cursor, selection, and keyboard handling.

Design Pattern: State (manages input state)
"""

from typing import Callable, Optional

import pygame

from ui.widgets.base import Clickable, Widget


class InputBox(Widget, Clickable):
    """
    Text input widget.

    Features:
    - Cursor blinking
    - Text selection
    - Keyboard input
    - Max length
    - Placeholder text

    Usage:
        input_box = InputBox(placeholder="Enter name...")
        text = input_box.get_text()
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 200,
        height: int = 30,
        placeholder: str = "",
        max_length: int = 50,
        on_submit: Optional[Callable] = None,
        default_text: str = "",
    ):
        """
        Initialize input box.

        Args:
            x, y: Position
            width, height: Size
            placeholder: Placeholder text
            max_length: Maximum text length
            on_submit: Callback when Enter is pressed
            default_text: Initial text value
        """
        Widget.__init__(self, x, y, width, height)
        Clickable.__init__(self)

        self.text = default_text
        self.placeholder = placeholder
        self.max_length = max_length
        self.on_submit = on_submit

        self.font = pygame.font.Font(None, 24)
        self.cursor_visible = True
        self.cursor_blink_time = 0
        self.cursor_position = 0

        # Colors
        self.color_background = (50, 50, 60)
        self.color_border = (100, 100, 110)
        self.color_border_focus = (0, 150, 200)
        self.color_text = (240, 240, 245)
        self.color_placeholder = (120, 120, 130)
        self.color_cursor = (240, 240, 245)

    def render(self, surface: pygame.Surface):
        """Render input box."""
        if not self.visible:
            return

        # Draw background
        pygame.draw.rect(surface, self.color_background, self.rect, border_radius=4)

        # Draw border (different color when focused)
        border_color = self.color_border_focus if self.focused else self.color_border
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=4)

        # Render text or placeholder
        if self.text:
            text_surface = self.font.render(self.text, True, self.color_text)
        else:
            text_surface = self.font.render(self.placeholder, True, self.color_placeholder)

        # Position text with padding
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surface, text_rect)

        # Draw cursor if focused
        if self.focused and self.cursor_visible:
            cursor_x = text_rect.x + text_rect.width + 2
            cursor_y1 = self.rect.y + 5
            cursor_y2 = self.rect.y + self.rect.height - 5
            pygame.draw.line(
                surface, self.color_cursor, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2
            )

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events."""
        if not self.enabled or not self.visible:
            return False

        # Handle click to focus
        if self.handle_click_event(event):
            self.focused = True
            return True

        # Handle keyboard input when focused
        if self.focused and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Submit
                if self.on_submit:
                    self.on_submit(self.text)
                return True
            elif event.key == pygame.K_BACKSPACE:
                # Delete character
                self.text = self.text[:-1]
                return True
            elif event.key == pygame.K_ESCAPE:
                # Unfocus
                self.focused = False
                return True
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                # Add character
                self.text += event.unicode
                return True

        return False

    def get_text(self) -> str:
        """Get current text."""
        return self.text

    def set_text(self, text: str):
        """Set text."""
        self.text = text[: self.max_length]

    def clear(self):
        """Clear text."""
        self.text = ""
