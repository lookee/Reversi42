"""
Factory for creating Apocalyptron engines.

Provides convenient methods for creating pre-configured engines.
"""

from AI.Apocalyptron.core.engine import ApocalyptronEngine
from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder
from AI.Apocalyptron.weights.weight_presets import get_preset_weights


class ApocalyptronFactory:
    """
    Factory for creating Apocalyptron engines.
    
    Provides convenient methods for common configurations.
    """
    
    @staticmethod
    def create_engine(config: ApocalyptronConfig = None) -> ApocalyptronEngine:
        """
        Create engine from configuration.
        
        Args:
            config: ApocalyptronConfig instance (None = default)
            
        Returns:
            ApocalyptronEngine instance
        """
        return ApocalyptronEngine(config=config)
    
    @staticmethod
    def create_default(depth: int = 9) -> ApocalyptronEngine:
        """
        Create engine with default settings.
        
        Args:
            depth: Search depth (default: 9)
            
        Returns:
            ApocalyptronEngine with default configuration
        """
        config = (ApocalyptronConfigBuilder()
            .with_depth(depth)
            .enable_all_optimizations()
            .build())
        
        return ApocalyptronEngine(config=config)
    
    @staticmethod
    def create_aggressive(depth: int = 9) -> ApocalyptronEngine:
        """
        Create aggressive mobility-focused engine.
        
        Args:
            depth: Search depth (default: 9)
            
        Returns:
            ApocalyptronEngine with aggressive weights
        """
        config = (ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_preset_weights('aggressive')
            .enable_all_optimizations()
            .build())
        
        return ApocalyptronEngine(config=config)
    
    @staticmethod
    def create_defensive(depth: int = 9) -> ApocalyptronEngine:
        """
        Create defensive stability-focused engine.
        
        Args:
            depth: Search depth (default: 9)
            
        Returns:
            ApocalyptronEngine with defensive weights
        """
        config = (ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_preset_weights('defensive')
            .enable_all_optimizations()
            .build())
        
        return ApocalyptronEngine(config=config)
    
    @staticmethod
    def create_tournament(depth: int = 10) -> ApocalyptronEngine:
        """
        Create tournament-optimized engine.
        
        Args:
            depth: Search depth (default: 10)
            
        Returns:
            ApocalyptronEngine optimized for tournament play
        """
        config = (ApocalyptronConfigBuilder()
            .with_depth(depth)
            .enable_all_optimizations()
            .quiet_mode()  # No output in tournament
            .build())
        
        return ApocalyptronEngine(config=config)
    
    @staticmethod
    def create_analysis(depth: int = 12) -> ApocalyptronEngine:
        """
        Create analysis engine (deep search, verbose).
        
        Args:
            depth: Search depth (default: 12)
            
        Returns:
            ApocalyptronEngine for deep position analysis
        """
        config = (ApocalyptronConfigBuilder()
            .with_depth(depth)
            .enable_all_optimizations()
            .verbose_mode()
            .build())
        
        return ApocalyptronEngine(config=config)

