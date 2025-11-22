"""
Common UI Utilities - Shared across all UI implementations

Provides theme management, layout calculations, event systems, etc.
These are framework-agnostic utilities (can be used with any UI).
"""

from .event_bus import EventBus
from .theme import ColorPalette, Theme

__all__ = [
    "Theme",
    "ColorPalette",
    "EventBus",
]
