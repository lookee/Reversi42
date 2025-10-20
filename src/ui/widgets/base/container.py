"""
Container Widgets - Composite Pattern Implementation

Container widgets can hold child widgets and manage their layout.
Implements Composite Pattern for hierarchical UI composition.

Design Pattern: Composite
"""

from typing import List, Optional, Tuple

import pygame

from .widget import Widget


class Container(Widget):
    """
    Container widget - can contain child widgets.

    This is the Composite in the Composite pattern.
    Manages child widgets and propagates rendering/events to them.
    """

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        """
        Initialize container.

        Args:
            x, y: Position
            width, height: Size
        """
        super().__init__(x, y, width, height)
        self.children: List[Widget] = []
        self.padding = 10
        self.spacing = 5

    def add(self, widget: Widget):
        """
        Add child widget.

        Args:
            widget: Widget to add
        """
        widget.parent = self
        self.children.append(widget)

    def remove(self, widget: Widget):
        """
        Remove child widget.

        Args:
            widget: Widget to remove
        """
        if widget in self.children:
            widget.parent = None
            self.children.remove(widget)

    def clear(self):
        """Remove all children."""
        for child in self.children:
            child.parent = None
        self.children.clear()

    def render(self, surface: pygame.Surface):
        """
        Render container and all children.

        Composite pattern: delegates to children.
        """
        if not self.visible:
            return

        # Render background if set
        self._render_background(surface)

        # Render all children
        for child in self.children:
            if child.visible:
                child.render(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle event and propagate to children.

        Args:
            event: Pygame event

        Returns:
            True if event was handled by any child
        """
        if not self.enabled or not self.visible:
            return False

        # Propagate to children (reverse order for z-index)
        for child in reversed(self.children):
            if child.handle_event(event):
                return True

        return super().handle_event(event)


class VBox(Container):
    """
    Vertical box layout container.

    Arranges children vertically with configurable spacing.
    """

    def __init__(self, children: Optional[List[Widget]] = None, spacing: int = 5, **kwargs):
        """
        Initialize VBox.

        Args:
            children: List of child widgets
            spacing: Space between children
            **kwargs: Additional arguments (x, y, width, height) - set as attributes
        """
        super().__init__()
        self.spacing = spacing
        
        # Support legacy x, y, width, height parameters
        for key, value in kwargs.items():
            setattr(self, key, value)

        if children:
            for child in children:
                self.add(child)

        self._layout()

    def add(self, widget: Widget):
        """Add widget and recalculate layout."""
        super().add(widget)
        self._layout()

    def _layout(self):
        """Calculate vertical layout."""
        current_y = self.padding
        max_width = 0

        for child in self.children:
            child.set_position(self.padding, current_y)
            current_y += child.rect.height + self.spacing
            max_width = max(max_width, child.rect.width)

        # Update container size
        if self.children:
            self.set_size(max_width + 2 * self.padding, current_y - self.spacing + self.padding)


class HBox(Container):
    """
    Horizontal box layout container.

    Arranges children horizontally with configurable spacing.
    """

    def __init__(self, children: Optional[List[Widget]] = None, spacing: int = 5, **kwargs):
        """
        Initialize HBox.

        Args:
            children: List of child widgets
            spacing: Space between children
            **kwargs: Additional arguments (x, y, width, height) - set as attributes
        """
        super().__init__()
        self.spacing = spacing
        
        # Support legacy x, y, width, height parameters
        for key, value in kwargs.items():
            setattr(self, key, value)

        if children:
            for child in children:
                self.add(child)

        self._layout()

    def add(self, widget: Widget):
        """Add widget and recalculate layout."""
        super().add(widget)
        self._layout()

    def _layout(self):
        """Calculate horizontal layout."""
        current_x = self.padding
        max_height = 0

        for child in self.children:
            child.set_position(current_x, self.padding)
            current_x += child.rect.width + self.spacing
            max_height = max(max_height, child.rect.height)

        # Update container size
        if self.children:
            self.set_size(current_x - self.spacing + self.padding, max_height + 2 * self.padding)


class Grid(Container):
    """
    Grid layout container.

    Arranges children in a grid with rows and columns.
    """

    def __init__(self, rows: int, cols: int, cell_width: int, cell_height: int):
        """
        Initialize grid.

        Args:
            rows: Number of rows
            cols: Number of columns
            cell_width: Width of each cell
            cell_height: Height of each cell
        """
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.cell_width = cell_width
        self.cell_height = cell_height

        # Calculate container size
        self.set_size(cols * cell_width + 2 * self.padding, rows * cell_height + 2 * self.padding)

    def add_at(self, widget: Widget, row: int, col: int):
        """
        Add widget at specific grid position.

        Args:
            widget: Widget to add
            row: Row index
            col: Column index
        """
        if row >= self.rows or col >= self.cols:
            raise ValueError(f"Position ({row}, {col}) outside grid ({self.rows}, {self.cols})")

        # Calculate position
        x = self.padding + col * self.cell_width
        y = self.padding + row * self.cell_height

        widget.set_position(x, y)
        self.add(widget)

    def get_cell_at(self, screen_x: int, screen_y: int) -> Optional[Tuple[int, int]]:
        """
        Get grid cell at screen position.

        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate

        Returns:
            (row, col) tuple or None if outside grid
        """
        if not self.contains_point(screen_x, screen_y):
            return None

        # Convert to grid coordinates
        rel_x = screen_x - self.rect.x - self.padding
        rel_y = screen_y - self.rect.y - self.padding

        col = rel_x // self.cell_width
        row = rel_y // self.cell_height

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return (row, col)

        return None
