"""
TextArea Widget - Multi-line text input component

Multi-line text editor with scrolling and rich text support.

Design Pattern: State (manages multi-line input state)
"""

from typing import Callable, List, Optional

import pygame

from ui.widgets.base import Clickable, Widget


class TextArea(Widget, Clickable):
    """
    Multi-line text input widget.

    Features:
    - Multi-line text editing
    - Vertical scrolling
    - Line numbers (optional)
    - Syntax highlighting (optional)
    - Auto-resize support

    Usage:
        textarea = TextArea(width=400, height=300)
        text = textarea.get_text()
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 300,
        height: int = 200,
        placeholder: str = "",
        max_lines: int = 100,
        show_line_numbers: bool = False,
        on_change: Optional[Callable] = None,
        default_text: str = "",
        center_in_parent: bool = False,
    ):
        """
        Initialize textarea.

        Args:
            x, y: Position
            width, height: Size
            placeholder: Placeholder text
            max_lines: Maximum number of lines
            show_line_numbers: Show line numbers
            on_change: Callback when text changes
            default_text: Initial text value
            center_in_parent: Auto-center in parent
        """
        Widget.__init__(self, x, y, width, height, center_in_parent)
        Clickable.__init__(self)

        self.placeholder = placeholder
        self.max_lines = max_lines
        self.show_line_numbers = show_line_numbers
        self.on_change = on_change

        # Parse initial text into lines
        self.lines: List[str] = default_text.split("\n") if default_text else [""]
        self.current_line = 0
        self.cursor_col = 0
        self.scroll_offset = 0

        self.font = pygame.font.Font(None, 22)
        self.line_height = self.font.get_height() + 4
        self.cursor_visible = True
        self.cursor_blink_time = 0

        # Colors
        self.color_background = (40, 40, 45)
        self.color_border = (80, 80, 90)
        self.color_border_focus = (0, 150, 200)
        self.color_text = (240, 240, 245)
        self.color_placeholder = (120, 120, 130)
        self.color_cursor = (240, 240, 245)
        self.color_line_numbers = (100, 100, 110)
        self.color_selection = (100, 150, 200, 100)

    def render(self, surface: pygame.Surface):
        """Render textarea."""
        if not self.visible:
            return

        abs_rect = self.get_absolute_rect()

        # Draw background
        pygame.draw.rect(surface, self.color_background, abs_rect, border_radius=4)

        # Draw border
        border_color = self.color_border_focus if self.focused else self.color_border
        pygame.draw.rect(surface, border_color, abs_rect, 2, border_radius=4)

        # Calculate visible lines
        visible_lines = (abs_rect.height - 10) // self.line_height
        line_number_width = 40 if self.show_line_numbers else 0
        text_x = abs_rect.x + 10 + line_number_width
        text_y = abs_rect.y + 5

        # Render visible lines
        if not self.lines or (len(self.lines) == 1 and not self.lines[0]):
            # Show placeholder
            if not self.focused:
                placeholder_surface = self.font.render(
                    self.placeholder, True, self.color_placeholder
                )
                surface.blit(placeholder_surface, (text_x, text_y))
        else:
            # Render lines
            for i in range(
                self.scroll_offset,
                min(self.scroll_offset + visible_lines, len(self.lines)),
            ):
                line_y = text_y + (i - self.scroll_offset) * self.line_height

                # Line numbers
                if self.show_line_numbers:
                    num_surface = self.font.render(f"{i+1:3}", True, self.color_line_numbers)
                    surface.blit(num_surface, (abs_rect.x + 5, line_y))

                # Line text
                line_surface = self.font.render(self.lines[i], True, self.color_text)
                surface.blit(line_surface, (text_x, line_y))

                # Draw cursor on current line
                if self.focused and i == self.current_line and self.cursor_visible:
                    cursor_text = self.lines[i][: self.cursor_col]
                    cursor_width = self.font.size(cursor_text)[0]
                    cursor_x = text_x + cursor_width
                    pygame.draw.line(
                        surface,
                        self.color_cursor,
                        (cursor_x, line_y),
                        (cursor_x, line_y + self.line_height - 4),
                        2,
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
                # New line
                if len(self.lines) < self.max_lines:
                    current_line_text = self.lines[self.current_line]
                    before = current_line_text[: self.cursor_col]
                    after = current_line_text[self.cursor_col :]
                    self.lines[self.current_line] = before
                    self.lines.insert(self.current_line + 1, after)
                    self.current_line += 1
                    self.cursor_col = 0
                    self._trigger_change()
                return True

            elif event.key == pygame.K_BACKSPACE:
                # Delete character or merge lines
                if self.cursor_col > 0:
                    # Delete character
                    line = self.lines[self.current_line]
                    self.lines[self.current_line] = (
                        line[: self.cursor_col - 1] + line[self.cursor_col :]
                    )
                    self.cursor_col -= 1
                    self._trigger_change()
                elif self.current_line > 0:
                    # Merge with previous line
                    prev_line = self.lines[self.current_line - 1]
                    current_line = self.lines[self.current_line]
                    self.lines[self.current_line - 1] = prev_line + current_line
                    self.lines.pop(self.current_line)
                    self.current_line -= 1
                    self.cursor_col = len(prev_line)
                    self._trigger_change()
                return True

            elif event.key == pygame.K_DELETE:
                # Delete character after cursor
                line = self.lines[self.current_line]
                if self.cursor_col < len(line):
                    self.lines[self.current_line] = (
                        line[: self.cursor_col] + line[self.cursor_col + 1 :]
                    )
                    self._trigger_change()
                return True

            elif event.key == pygame.K_LEFT:
                if self.cursor_col > 0:
                    self.cursor_col -= 1
                elif self.current_line > 0:
                    self.current_line -= 1
                    self.cursor_col = len(self.lines[self.current_line])
                return True

            elif event.key == pygame.K_RIGHT:
                if self.cursor_col < len(self.lines[self.current_line]):
                    self.cursor_col += 1
                elif self.current_line < len(self.lines) - 1:
                    self.current_line += 1
                    self.cursor_col = 0
                return True

            elif event.key == pygame.K_UP:
                if self.current_line > 0:
                    self.current_line -= 1
                    self.cursor_col = min(self.cursor_col, len(self.lines[self.current_line]))
                return True

            elif event.key == pygame.K_DOWN:
                if self.current_line < len(self.lines) - 1:
                    self.current_line += 1
                    self.cursor_col = min(self.cursor_col, len(self.lines[self.current_line]))
                return True

            elif event.key == pygame.K_HOME:
                self.cursor_col = 0
                return True

            elif event.key == pygame.K_END:
                self.cursor_col = len(self.lines[self.current_line])
                return True

            elif event.key == pygame.K_ESCAPE:
                self.focused = False
                return True

            elif event.unicode.isprintable():
                # Insert character
                line = self.lines[self.current_line]
                self.lines[self.current_line] = (
                    line[: self.cursor_col] + event.unicode + line[self.cursor_col :]
                )
                self.cursor_col += 1
                self._trigger_change()
                return True

        return False

    def _trigger_change(self):
        """Trigger change callback."""
        if self.on_change:
            self.on_change(self.get_text())

    def get_text(self) -> str:
        """Get current text."""
        return "\n".join(self.lines)

    def set_text(self, text: str):
        """Set text."""
        self.lines = text.split("\n")[: self.max_lines]
        self.current_line = 0
        self.cursor_col = 0
        self._trigger_change()

    def clear(self):
        """Clear text."""
        self.lines = [""]
        self.current_line = 0
        self.cursor_col = 0
        self._trigger_change()
