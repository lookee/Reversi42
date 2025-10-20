"""
Base Widget Classes - Foundation for Component System

Implements Composite Pattern for hierarchical UI composition.
"""

from .widget import Widget
from .container import Container, VBox, HBox, Grid
from .interactive import Interactive, Clickable, Hoverable

__all__ = [
    'Widget',
    'Container', 'VBox', 'HBox', 'Grid',
    'Interactive', 'Clickable', 'Hoverable',
]

