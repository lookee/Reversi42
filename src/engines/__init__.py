"""
Engines Module

Modular engine architecture with DI and design patterns.

Version: 3.2.0
"""

from .base.engine import Engine
from .base.engine_metadata import EngineMetadata
from .factory.engine_registry import EngineRegistry
from .factory.engine_builder import EngineBuilder

# Auto-import all engines to trigger registration
try:
    from .implementations.standard.minimax_engine import MinimaxEngine
    from .implementations.bitboard.bitboard_engine import BitboardEngine
    from .implementations.grandmaster.grandmaster_engine import GrandmasterEngine
    from .implementations.random.random_engine import RandomEngine
    from .implementations.standard.greedy_engine import GreedyEngine
    from .implementations.standard.heuristic_engine import HeuristicEngine
except ImportError as e:
    # Some engines may not be available yet
    pass

__all__ = [
    'Engine',
    'EngineMetadata',
    'EngineRegistry',
    'EngineBuilder'
]

