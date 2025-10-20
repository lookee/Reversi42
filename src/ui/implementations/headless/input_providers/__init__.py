"""
Headless Input Providers

Mock implementations of InputProvider for testing and automation.
"""

from .mock_input_provider import MockInputProvider
from .replay_input_provider import ReplayInputProvider

__all__ = ["MockInputProvider", "ReplayInputProvider"]
