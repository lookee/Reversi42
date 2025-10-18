"""
Headless View Implementation

No rendering, no input - for automated tournaments and testing.
All headless-specific code is isolated here.

Version: 3.1.0
"""

from .view import HeadlessBoardView
from .input_handler import HeadlessInputHandler

__all__ = [
    'HeadlessBoardView',
    'HeadlessInputHandler',
]

