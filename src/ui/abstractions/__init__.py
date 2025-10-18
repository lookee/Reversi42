"""
UI Abstractions - Abstract Interfaces

Clean interfaces following Interface Segregation Principle.
No implementation details, only contracts.

Version: 3.1.0
"""

from .view_interface import AbstractView
from .input_interface import AbstractInputHandler, InputEvent

__all__ = [
    'AbstractView',
    'AbstractInputHandler',
    'InputEvent',
]

