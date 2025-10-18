"""
Engine Registry

Registry Pattern: Auto-registration and discovery of engines.

Version: 3.2.0
"""

from typing import Dict, Type, Optional, Callable
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from AI.base.engine import Engine
from AI.base.engine_metadata import EngineMetadata


class EngineRegistry:
    """
    Registry Pattern: Centralized engine registration and discovery.
    
    Engines can self-register using the @EngineRegistry.register decorator.
    
    Example:
        @EngineRegistry.register('minimax', EngineMetadata(
            name='minimax',
            display_name='Classic Minimax',
            description='Traditional alpha-beta search'
        ))
        class MinimaxEngine(Engine):
            pass
    
    Usage:
        # Get engine by name
        engine = EngineRegistry.get_engine('minimax')
        
        # List all engines
        engines = EngineRegistry.list_engines()
    """
    
    _engines: Dict[str, Type[Engine]] = {}
    _metadata: Dict[str, EngineMetadata] = {}
    
    @classmethod
    def register(cls, name: str, metadata: Optional[EngineMetadata] = None):
        """
        Decorator to register an engine.
        
        Args:
            name: Unique engine identifier
            metadata: Engine metadata (optional)
        
        Returns:
            Decorator function
        
        Example:
            @EngineRegistry.register('minimax')
            class MinimaxEngine(Engine):
                pass
        """
        def decorator(engine_class: Type[Engine]):
            # Validate it's an Engine subclass
            if not issubclass(engine_class, Engine):
                raise TypeError(f"{engine_class.__name__} must inherit from Engine")
            
            # Register engine
            cls._engines[name] = engine_class
            
            # Register metadata
            if metadata:
                cls._metadata[name] = metadata
            else:
                # Create default metadata
                cls._metadata[name] = EngineMetadata(
                    name=name,
                    display_name=engine_class.__name__,
                    description=f"{engine_class.__name__} engine"
                )
            
            return engine_class
        
        return decorator
    
    @classmethod
    def get_engine(cls, name: str, **kwargs) -> Engine:
        """
        Create an engine instance by name.
        
        Args:
            name: Engine identifier
            **kwargs: Arguments to pass to engine constructor
        
        Returns:
            Engine instance
        
        Raises:
            ValueError: If engine not found
        """
        if name not in cls._engines:
            available = ', '.join(cls._engines.keys())
            raise ValueError(
                f"Engine '{name}' not registered. "
                f"Available engines: {available}"
            )
        
        return cls._engines[name](**kwargs)
    
    @classmethod
    def list_engines(cls) -> Dict[str, EngineMetadata]:
        """
        List all registered engines with metadata.
        
        Returns:
            dict: Mapping of engine names to metadata
        """
        return cls._metadata.copy()
    
    @classmethod
    def get_metadata(cls, name: str) -> Optional[EngineMetadata]:
        """
        Get metadata for specific engine.
        
        Args:
            name: Engine identifier
        
        Returns:
            EngineMetadata or None if not found
        """
        return cls._metadata.get(name)
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Check if engine is registered.
        
        Args:
            name: Engine identifier
        
        Returns:
            bool: True if registered
        """
        return name in cls._engines
    
    @classmethod
    def unregister(cls, name: str):
        """
        Unregister an engine (mainly for testing).
        
        Args:
            name: Engine identifier
        """
        cls._engines.pop(name, None)
        cls._metadata.pop(name, None)
    
    @classmethod
    def clear(cls):
        """Clear all registrations (mainly for testing)."""
        cls._engines.clear()
        cls._metadata.clear()

