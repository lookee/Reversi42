"""
Engine Metadata System

Provides metadata for engine discovery and configuration.

Version: 3.2.0
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class EngineMetadata:
    """
    Metadata for engine registration and discovery.
    
    Attributes:
        name: Internal engine name
        display_name: User-friendly name
        description: Engine description
        complexity: Computational complexity (low/medium/high)
        speed: Relative speed (fast/medium/slow)
        strength: Playing strength (weak/medium/strong/master)
        features: List of supported features
        parameters: Configurable parameters
        author: Engine author
        version: Engine version
    """
    
    name: str
    display_name: str
    description: str
    complexity: str = "medium"
    speed: str = "medium"
    strength: str = "medium"
    features: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    author: str = "Reversi42"
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'complexity': self.complexity,
            'speed': self.speed,
            'strength': self.strength,
            'features': self.features,
            'parameters': self.parameters,
            'author': self.author,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EngineMetadata':
        """Create metadata from dictionary."""
        return cls(**data)

