"""
Base Widget Classes - Foundation for Component System

Implements Composite Pattern for hierarchical UI composition.
"""

from .container import Container, Grid, HBox, VBox
from .interactive import Clickable, Hoverable, Interactive
from .widget import Widget

__all__ = [
    "Widget",
    "Container",
    "VBox",
    "HBox",
    "Grid",
    "Interactive",
    "Clickable",
    "Hoverable",
]
