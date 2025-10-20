"""
Interactive Widget Mixins - Event Handling Enhancements

Provides mixins for common interactive behaviors:
- Clickable: Mouse click handling
- Hoverable: Mouse hover effects
- Focusable: Keyboard focus

Design Pattern: Mixin
"""

from typing import Callable, Optional

import pygame


class Interactive:
    """
    Base mixin for interactive widgets.

    Provides common interactive state and event handling.
    """

    def __init__(self):
        """Initialize interactive state."""
        self.hovered = False
        self.pressed = False
        self.focused = False


class Clickable:
    """
    Mixin for clickable widgets.

    Provides click event handling with callbacks.

    Usage:
        class MyButton(Widget, Clickable):
            def __init__(self):
                Widget.__init__(self)
                Clickable.__init__(self, on_click=my_callback)
    """

    def __init__(self, on_click: Optional[Callable] = None):
        """
        Initialize clickable behavior.

        Args:
            on_click: Callback function when clicked
        """
        self.on_click = on_click
        self.click_sound: Optional[pygame.mixer.Sound] = None

    def handle_click_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse click events.

        Call this from your handle_event() method.

        Args:
            event: Pygame event

        Returns:
            True if click was handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self, "contains_point") and self.contains_point(event.pos[0], event.pos[1]):
                self.pressed = True
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if hasattr(self, "contains_point") and self.contains_point(event.pos[0], event.pos[1]):
                if self.pressed:
                    # Click completed
                    self.pressed = False
                    self._trigger_click()
                    return True
            self.pressed = False

        return False

    def _trigger_click(self):
        """Trigger click callback and effects."""
        # Play click sound if set
        if self.click_sound:
            self.click_sound.play()

        # Call callback
        if self.on_click:
            self.on_click()

    def set_click_callback(self, callback: Callable):
        """
        Set click callback.

        Args:
            callback: Function to call when clicked
        """
        self.on_click = callback


class Hoverable:
    """
    Mixin for hoverable widgets.

    Provides hover state and visual feedback.

    Usage:
        class MyWidget(Widget, Hoverable):
            def render(self, surface):
                if self.hovered:
                    # Draw hover effect
                    pass
    """

    def __init__(self, on_hover: Optional[Callable] = None, on_unhover: Optional[Callable] = None):
        """
        Initialize hoverable behavior.

        Args:
            on_hover: Callback when mouse enters widget
            on_unhover: Callback when mouse leaves widget
        """
        self.hovered = False
        self.on_hover = on_hover
        self.on_unhover = on_unhover
        self._was_hovered = False

    def handle_hover_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse hover events.

        Call this from your handle_event() method.

        Args:
            event: Pygame event

        Returns:
            True if hover state changed
        """
        if event.type == pygame.MOUSEMOTION:
            if hasattr(self, "contains_point"):
                now_hovered = self.contains_point(event.pos[0], event.pos[1])

                # Check for hover state change
                if now_hovered and not self._was_hovered:
                    # Entered
                    self.hovered = True
                    if self.on_hover:
                        self.on_hover()
                    self._was_hovered = True
                    return True

                elif not now_hovered and self._was_hovered:
                    # Exited
                    self.hovered = False
                    if self.on_unhover:
                        self.on_unhover()
                    self._was_hovered = False
                    return True

        return False


class Focusable:
    """
    Mixin for focusable widgets (keyboard input).

    Provides keyboard focus management.
    """

    def __init__(self, on_focus: Optional[Callable] = None, on_blur: Optional[Callable] = None):
        """
        Initialize focusable behavior.

        Args:
            on_focus: Callback when widget gains focus
            on_blur: Callback when widget loses focus
        """
        self.focused = False
        self.on_focus = on_focus
        self.on_blur = on_blur

    def focus(self):
        """Give focus to this widget."""
        if not self.focused:
            self.focused = True
            if self.on_focus:
                self.on_focus()

    def blur(self):
        """Remove focus from this widget."""
        if self.focused:
            self.focused = False
            if self.on_blur:
                self.on_blur()

    def handle_key_event(self, event: pygame.event.Event) -> bool:
        """
        Handle keyboard events (override in subclasses).

        Args:
            event: Pygame event

        Returns:
            True if event was handled
        """
        if not self.focused:
            return False

        # Subclasses should override this
        return False
