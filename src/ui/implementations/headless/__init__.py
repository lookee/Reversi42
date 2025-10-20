"""
Headless View Implementation

No rendering, no input - for automated tournaments and testing.
All headless-specific code is isolated here.

Version: 3.1.0
"""

from .input_handler import HeadlessInputHandler
from .view import HeadlessBoardView

__all__ = [
    "HeadlessBoardView",
    "HeadlessInputHandler",
]
