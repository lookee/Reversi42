"""
View Factory

Creates view instances based on type string.
Provides convenient methods for view creation.
"""

import os
import sys
from typing import Optional

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from ui.implementations.headless.view import HeadlessBoardView  # New Headless


class ViewFactory:
    """
    Factory for creating view instances.

    Uses views from ui.implementations.*
    """

    @staticmethod
    def create_view(
        view_type: str, width: int, height: int, window_width: int = 800, window_height: int = 600
    ):
        """
        Create view instance based on type.

        Args:
            view_type: 'headless'
            width: Board width in cells
            height: Board height in cells
            window_width: Display width
            window_height: Display height

        Returns:
            View instance
        """
        view_type = view_type.lower()

        if view_type in ["headless", "none", "null"]:
            return HeadlessBoardView(width, height, window_width, window_height)
        else:
            raise ValueError(f"Unknown view type: {view_type}. Available: headless, none, null")

    @staticmethod
    def create_headless_view(width: int, height: int):
        """Create Headless view"""
        return HeadlessBoardView(width, height, 0, 0)
