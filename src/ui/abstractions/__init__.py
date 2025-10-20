"""
UI Abstractions - Abstract Interfaces

Clean interfaces following Interface Segregation Principle.
No implementation details, only contracts.

Version: 3.1.0
"""

from .input_interface import AbstractInputHandler, InputEvent
from .view_interface import AbstractView

__all__ = [
    "AbstractView",
    "AbstractInputHandler",
    "InputEvent",
]
