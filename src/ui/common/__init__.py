"""
Common UI Utilities - Shared across all UI implementations

Provides theme management, layout calculations, event systems, etc.
These are framework-agnostic utilities (can be used with any UI).
"""

from .theme import Theme, ColorPalette
from .layout import LayoutManager
from .event_bus import EventBus

__all__ = [
    'Theme', 'ColorPalette',
    'LayoutManager',
    'EventBus',
]

