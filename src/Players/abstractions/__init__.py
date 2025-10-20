"""
Player Abstractions - Clean Architecture

This package contains abstract interfaces for the Player domain layer.
Players depend on these abstractions, NOT on concrete UI implementations.

This implements Dependency Inversion Principle (SOLID).
"""

from .input_provider import InputProvider
from .player_interface import PlayerInterface

__all__ = [
    "InputProvider",
    "PlayerInterface",
]
