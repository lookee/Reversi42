"""
UI Widgets Package - Component-Based Architecture

Reusable UI components for building game interfaces.
Implements Composite Pattern for hierarchical widget composition.

Design Patterns:
- Composite: Widget hierarchy
- Strategy: Pluggable renderers
- Observer: Event propagation
"""

from .base import Widget, Container, VBox, HBox, Grid, Interactive
from .primitives import Button, Label, Panel, InputBox, Dialog
from .game import BoardWidget, ScorePanel, OpeningTooltip, MoveIndicator

__all__ = [
    # Base
    'Widget', 'Container', 'VBox', 'HBox', 'Grid', 'Interactive',
    # Primitives
    'Button', 'Label', 'Panel', 'InputBox', 'Dialog',
    # Game-specific
    'BoardWidget', 'ScorePanel', 'OpeningTooltip', 'MoveIndicator',
]

