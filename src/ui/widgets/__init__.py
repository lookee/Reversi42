"""
UI Widgets Package - Component-Based Architecture

Reusable UI components for building game interfaces.
Implements Composite Pattern for hierarchical widget composition.

Design Patterns:
- Composite: Widget hierarchy
- Strategy: Pluggable renderers
- Observer: Event propagation
"""

from .base import Container, Grid, HBox, Interactive, VBox, Widget
from .game import BoardWidget, MoveIndicator, OpeningTooltip, ScorePanel
from .primitives import Button, Dialog, InputBox, Label, Panel

__all__ = [
    # Base
    "Widget",
    "Container",
    "VBox",
    "HBox",
    "Grid",
    "Interactive",
    # Primitives
    "Button",
    "Label",
    "Panel",
    "InputBox",
    "Dialog",
    # Game-specific
    "BoardWidget",
    "ScorePanel",
    "OpeningTooltip",
    "MoveIndicator",
]
