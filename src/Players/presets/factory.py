"""
Generic Player Factory

Creates players from pure metadata configurations.
No need for individual create_*() functions!
"""

from AI.factory.engine_registry import EngineRegistry
from AI.factory.engine_builder import EngineBuilder
from Players.ai.ai_player import AIPlayer
from Players.presets.metadata import PLAYER_PRESETS

# Force import all engines to ensure registration
import AI.implementations.standard.minimax_engine
import AI.implementations.standard.greedy_engine
import AI.implementations.standard.heuristic_engine
import AI.implementations.random.random_engine
import AI.implementations.bitboard.bitboard_engine
import AI.implementations.grandmaster.grandmaster_engine


class PresetFactory:
    """
    Generic factory that creates players from metadata.
    
    Pure declarative approach - no create_*() functions needed!
    
    Example:
        # Simple creation
        player = PresetFactory.create('Grandmaster')
        
        # With custom depth
        player = PresetFactory.create('Grandmaster', depth=12)
        
        # With all parameters
        player = PresetFactory.create('Ultimate AI', depth=10, threads=8)
    """
    
    @staticmethod
    def create(preset_name: str, **kwargs) -> AIPlayer:
        """
        Create a player from preset metadata.
        
        Args:
            preset_name: Name of the preset (e.g., 'Grandmaster')
            **kwargs: Override default parameters (e.g., depth=10)
        
        Returns:
            Configured AIPlayer instance
        
        Raises:
            KeyError: If preset not found
        
        Example:
            player = PresetFactory.create('Grandmaster', depth=12)
        """
        # Get preset metadata
        if preset_name not in PLAYER_PRESETS:
            available = ', '.join(PLAYER_PRESETS.keys())
            raise KeyError(f"Preset '{preset_name}' not found. Available: {available}")
        
        preset = PLAYER_PRESETS[preset_name]
        
        # Extract configuration
        engine_type = preset['engine_type']
        depth = kwargs.get('depth', preset.get('default_depth', 5))
        name = kwargs.get('name', preset['name'])
        features = preset.get('features', [])
        engine_config = preset.get('engine_config', {})
        
        # Build engine based on features
        if 'engine_config' in preset and preset['engine_config']:
            # Advanced configuration (e.g., Ultimate AI)
            engine = PresetFactory._build_advanced_engine(engine_type, engine_config, kwargs)
        elif features:
            # Use EngineBuilder for features
            engine = PresetFactory._build_engine_with_features(engine_type, features)
        else:
            # Simple engine from registry
            engine = EngineRegistry.get_engine(engine_type)
        
        # Create and return player
        return AIPlayer(
            engine=engine,
            depth=depth,
            name=name
        )
    
    @staticmethod
    def _build_engine_with_features(engine_type: str, features: list):
        """Build engine with specified features using EngineBuilder."""
        builder = EngineBuilder()
        
        # Set base engine
        if engine_type == 'bitboard' or 'bitboard' in features:
            builder.use_bitboard()
        elif engine_type == 'minimax':
            builder.use_minimax()
        elif engine_type == 'grandmaster':
            # Grandmaster is a complete engine, use directly
            return EngineRegistry.get_engine('grandmaster')
        else:
            # For greedy, heuristic, random - use registry directly
            return EngineRegistry.get_engine(engine_type)
        
        # Add features
        if 'opening_book' in features:
            builder.with_opening_book()
        
        if 'parallel' in features:
            builder.with_parallel_search()
        
        if 'transposition_table' in features:
            builder.with_transposition_table()
        
        if 'advanced_eval' in features:
            builder.with_advanced_evaluator()
        
        return builder.build()
    
    @staticmethod
    def _build_advanced_engine(engine_type: str, config: dict, kwargs: dict):
        """Build engine with advanced configuration."""
        builder = EngineBuilder()
        
        # Base engine
        if config.get('use_bitboard'):
            builder.use_bitboard()
        else:
            builder.use_minimax()
        
        # Features
        if config.get('advanced_evaluator'):
            builder.with_advanced_evaluator()
        
        if config.get('opening_book'):
            builder.with_opening_book()
        
        if config.get('parallel_threads'):
            threads = kwargs.get('threads', config['parallel_threads'])
            builder.with_parallel_search(threads=threads)
        
        if config.get('transposition_table_mb'):
            builder.with_transposition_table(size_mb=config['transposition_table_mb'])
        
        return builder.build()
    
    @staticmethod
    def list_available() -> list:
        """
        List all available preset names.
        
        Returns:
            List of preset names
        """
        return list(PLAYER_PRESETS.keys())
    
    @staticmethod
    def get_metadata(preset_name: str) -> dict:
        """
        Get metadata for a preset.
        
        Args:
            preset_name: Preset name
        
        Returns:
            Metadata dict
        """
        if preset_name not in PLAYER_PRESETS:
            raise KeyError(f"Preset '{preset_name}' not found")
        
        return PLAYER_PRESETS[preset_name].copy()


__all__ = ['PresetFactory']

