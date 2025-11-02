"""
AI Player Configuration System

This package provides a centralized, elegant system for managing AI players
through YAML configuration files.

Architecture:
- Auto-discovery: Recursively scans config/players/enabled/
- Validation: Ensures configuration integrity
- Registry: Centralized player management
- Factory: Creates player instances from configs
- Logging: Comprehensive startup and runtime logging

Usage:
    from Players.config import PlayerRegistry
    
    # Initialize registry (auto-discovers all players)
    registry = PlayerRegistry()
    
    # Get available players
    players = registry.list_players()
    
    # Create player instance
    player = registry.create_player("DIVZERO.EXE")
"""

from .registry import PlayerRegistry
from .loader import ConfigLoader
from .factory import PlayerFactory
from .discovery import PlayerDiscovery
from .validator import ConfigValidator
from .exceptions import (
    PlayerConfigError,
    PlayerNotFoundError,
    InvalidConfigError,
    PlayerCreationError
)

__all__ = [
    'PlayerRegistry',
    'ConfigLoader',
    'PlayerFactory',
    'PlayerDiscovery',
    'ConfigValidator',
    'PlayerConfigError',
    'PlayerNotFoundError',
    'InvalidConfigError',
    'PlayerCreationError',
]

__version__ = '1.0.0'

