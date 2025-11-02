"""
UI Abstractions - Abstract Interfaces

Clean interfaces following Interface Segregation Principle.
No implementation details, only contracts.
"""

from .input_interface import AbstractInputHandler, InputEvent
from .view_interface import AbstractView

__all__ = [
    "AbstractView",
    "AbstractInputHandler",
    "InputEvent",
]
