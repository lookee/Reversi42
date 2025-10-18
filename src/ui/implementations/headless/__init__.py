"""
Headless View Implementation

No rendering, no input - for automated tournaments and testing.

Version: 3.1.0
"""

# from .view import HeadlessView  # TODO: Implement
from .input_handler import HeadlessInputHandler

__all__ = [
    # 'HeadlessView',  # TODO
    'HeadlessInputHandler'
]

