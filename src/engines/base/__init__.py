"""
Base Engine Classes

Abstract interfaces for game engines.

Version: 3.2.0
Architecture: Strategy Pattern + Dependency Injection
"""

from .engine import Engine
from .engine_metadata import EngineMetadata

__all__ = ['Engine', 'EngineMetadata']

