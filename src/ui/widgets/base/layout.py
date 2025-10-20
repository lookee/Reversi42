"""
Advanced Layout Primitives - Bootstrap-like Layout System

Provides powerful layout primitives for building responsive UIs:
- Center: Automatically centers content
- Spacer: Flexible spacing component
- Stack: Enhanced VBox with alignment options
- Divider: Visual separator

Design Pattern: Composite + Strategy (for alignment)
"""

from typing import Optional, List, Literal

import pygame

from .container import Container, VBox, HBox
from .widget import Widget


class Center(Container):
    """
    Center container - automatically centers its child.
    
    Like Bootstrap's d-flex justify-content-center align-items-center.
    
    Features:
    - Automatic centering (horizontal, vertical, or both)
    - Minimal boilerplate
    - Responsive to parent size
    
    Usage:
        center = Center(width=800, height=600)
        center.add(my_widget)  # Automatically centered!
    """
    
    def __init__(
        self, 
        width: int = 0, 
        height: int = 0,
        horizontal: bool = True,
        vertical: bool = True,
        **kwargs
    ):
        """
        Initialize center container.
        
        Args:
            width: Container width
            height: Container height
            horizontal: Center horizontally
            vertical: Center vertically
            **kwargs: Additional container arguments
        """
        super().__init__(0, 0, width, height)
        self.center_horizontal = horizontal
        self.center_vertical = vertical
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def add(self, widget: Widget):
        """Add widget and center it."""
        super().add(widget)
        self._center_child()
    
    def _center_child(self):
        """Center the child widget."""
        if not self.children:
            return
        
        # Center only the first child (single child container)
        child = self.children[0]
        
        x = child.rect.x
        y = child.rect.y
        
        if self.center_horizontal:
            x = (self.rect.width - child.rect.width) // 2
        
        if self.center_vertical:
            y = (self.rect.height - child.rect.height) // 2
        
        child.set_position(x, y)
    
    def set_size(self, width: int, height: int):
        """Update size and re-center child."""
        super().set_size(width, height)
        self._center_child()


class Spacer(Widget):
    """
    Spacer - flexible spacing component.
    
    Like Bootstrap's flex-grow spacer.
    
    Features:
    - Fixed or flexible sizing
    - Can be used in HBox/VBox for spacing
    - Invisible (no rendering)
    
    Usage:
        row = HBox()
        row.add(Button("Left"))
        row.add(Spacer(width=50))  # Fixed 50px space
        row.add(Button("Right"))
    """
    
    def __init__(self, width: int = 0, height: int = 0):
        """
        Initialize spacer.
        
        Args:
            width: Spacer width
            height: Spacer height
        """
        super().__init__(0, 0, width, height)
        self.visible = False  # Invisible
    
    def render(self, surface: pygame.Surface):
        """Spacers don't render anything."""
        pass
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Spacers don't handle events."""
        return False


class Stack(VBox):
    """
    Stack - Enhanced VBox with Bootstrap-like options.
    
    Like Bootstrap's d-flex flex-column.
    
    Features:
    - Multiple alignment options
    - Justify content (start, center, end, space-between, space-around)
    - Align items (start, center, end, stretch)
    - Gap instead of spacing (cleaner API)
    
    Usage:
        stack = Stack(gap=20, align="center", justify="center")
        stack.add(Button("First"))
        stack.add(Button("Second"))
    """
    
    def __init__(
        self,
        children: Optional[List[Widget]] = None,
        gap: int = 0,
        align: Literal["start", "center", "end", "stretch"] = "start",
        justify: Literal["start", "center", "end", "space-between", "space-around"] = "start",
        **kwargs
    ):
        """
        Initialize stack.
        
        Args:
            children: List of child widgets
            gap: Space between children (replaces spacing)
            align: Horizontal alignment of children
            justify: Vertical distribution of children
            **kwargs: Additional arguments
        """
        # Set attributes BEFORE calling super().__init__() 
        # because _layout() will be called during parent init
        self.justify = justify
        self.gap = gap
        self.align_mode = align
        
        # Convert align to VBox's align parameter
        vbox_align = {
            "start": "left",
            "center": "center",
            "end": "right",
            "stretch": "left"  # TODO: implement stretch
        }.get(align, "left")
        
        super().__init__(children=children, spacing=gap, align=vbox_align, **kwargs)
    
    def _layout(self):
        """Enhanced layout with justify support."""
        if self.justify == "start":
            # Standard VBox layout
            super()._layout()
        elif self.justify == "center":
            # Center all items vertically
            super()._layout()
            # Calculate total height
            total_height = sum(child.rect.height for child in self.children)
            total_height += self.gap * (len(self.children) - 1) if self.children else 0
            
            # Center vertically
            start_y = (self.rect.height - total_height) // 2
            current_y = start_y
            
            for child in self.children:
                child.rect.y = current_y
                current_y += child.rect.height + self.gap
        elif self.justify == "end":
            # Align to bottom
            super()._layout()
            total_height = sum(child.rect.height for child in self.children)
            total_height += self.gap * (len(self.children) - 1) if self.children else 0
            
            start_y = self.rect.height - total_height - self.padding
            current_y = start_y
            
            for child in self.children:
                child.rect.y = current_y
                current_y += child.rect.height + self.gap
        elif self.justify == "space-between":
            # Distribute evenly with space between
            if len(self.children) <= 1:
                super()._layout()
                return
            
            super()._layout()
            total_child_height = sum(child.rect.height for child in self.children)
            available_space = self.rect.height - 2 * self.padding - total_child_height
            spacing = available_space // (len(self.children) - 1)
            
            current_y = self.padding
            for child in self.children:
                child.rect.y = current_y
                current_y += child.rect.height + spacing
        elif self.justify == "space-around":
            # Distribute evenly with space around
            if not self.children:
                return
            
            super()._layout()
            total_child_height = sum(child.rect.height for child in self.children)
            available_space = self.rect.height - 2 * self.padding - total_child_height
            spacing = available_space // (len(self.children) + 1)
            
            current_y = self.padding + spacing
            for child in self.children:
                child.rect.y = current_y
                current_y += child.rect.height + spacing


class Divider(Widget):
    """
    Divider - visual separator line.
    
    Like Bootstrap's <hr> or border utilities.
    
    Features:
    - Horizontal or vertical lines
    - Customizable color and thickness
    - Margins
    
    Usage:
        divider = Divider(orientation="horizontal", width=200, color=(100, 100, 100))
    """
    
    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        width: int = 100,
        height: int = 1,
        color: tuple = (100, 100, 110),
        thickness: int = 1,
    ):
        """
        Initialize divider.
        
        Args:
            orientation: Line orientation
            width: Divider width
            height: Divider height
            color: Line color
            thickness: Line thickness
        """
        super().__init__(0, 0, width, height)
        self.orientation = orientation
        self.color = color
        self.thickness = thickness
        
        # Auto-size based on orientation
        if orientation == "horizontal":
            self.rect.height = thickness
        else:
            self.rect.width = thickness
    
    def render(self, surface: pygame.Surface):
        """Render divider line."""
        if not self.visible:
            return
        
        abs_rect = self.get_absolute_rect()
        
        if self.orientation == "horizontal":
            start_pos = (abs_rect.x, abs_rect.y + abs_rect.height // 2)
            end_pos = (abs_rect.x + abs_rect.width, abs_rect.y + abs_rect.height // 2)
        else:
            start_pos = (abs_rect.x + abs_rect.width // 2, abs_rect.y)
            end_pos = (abs_rect.x + abs_rect.width // 2, abs_rect.y + abs_rect.height)
        
        pygame.draw.line(surface, self.color, start_pos, end_pos, self.thickness)


class Row(HBox):
    """
    Row - Bootstrap-like row container.
    
    Like Bootstrap's <div class="row">.
    
    Features:
    - Contains Col widgets
    - 12-column grid system
    - Responsive gaps
    - Auto-distribution
    
    Usage:
        row = Row(gap=10)
        row.add(Col(span=6, child=Button("Left")))
        row.add(Col(span=6, child=Button("Right")))
    """
    
    def __init__(
        self,
        children: Optional[List[Widget]] = None,
        gap: int = 10,
        align: str = "top",
        **kwargs
    ):
        """
        Initialize row.
        
        Args:
            children: List of Col widgets
            gap: Space between columns
            align: Vertical alignment
            **kwargs: Additional arguments
        """
        super().__init__(children=children, spacing=gap, align=align, **kwargs)
        self.gap = gap


class Col(Container):
    """
    Col - Bootstrap-like column.
    
    Like Bootstrap's <div class="col-{span}">.
    
    Features:
    - 12-column span system (1-12)
    - Auto-sizing
    - Single child container
    
    Usage:
        col = Col(span=6, child=Button("Content"))
        col = Col(span=12, child=Label("Full width"))
    """
    
    def __init__(
        self,
        span: int = 12,
        child: Optional[Widget] = None,
        **kwargs
    ):
        """
        Initialize column.
        
        Args:
            span: Column span (1-12)
            child: Child widget to contain
            **kwargs: Additional arguments
        """
        super().__init__()
        self.span = max(1, min(12, span))  # Clamp to 1-12
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        if child:
            self.add(child)
            # Auto-size to child
            self.set_size(child.rect.width, child.rect.height)
    
    def add(self, widget: Widget):
        """Add child (only one allowed)."""
        if self.children:
            # Replace existing child
            self.clear()
        super().add(widget)
        # Center child within column
        self._center_child()
    
    def _center_child(self):
        """Center child widget."""
        if not self.children:
            return
        
        child = self.children[0]
        x = (self.rect.width - child.rect.width) // 2 if self.rect.width > child.rect.width else 0
        y = (self.rect.height - child.rect.height) // 2 if self.rect.height > child.rect.height else 0
        child.set_position(x, y)

