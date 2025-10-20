"""
Primitive Widgets - Basic Reusable UI Components

Standard UI widgets that can be composed to build complex interfaces.
"""

from .button import Button
from .dialog import Dialog
from .input_box import InputBox
from .label import Label
from .panel import Panel

__all__ = ["Button", "Label", "Panel", "InputBox", "Dialog"]
