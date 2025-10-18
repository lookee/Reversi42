"""
Player Metadata System

Provides metadata for player discovery and configuration.

Version: 3.2.0
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class PlayerMetadata:
    """
    Metadata for player registration and discovery.
    
    Attributes:
        name: Internal player name
        display_name: User-friendly name
        description: Player description
        category: Player category (human/ai/network)
        enabled: Whether selectable in menus
        parameters: Configurable parameters
    """
    
    name: str
    display_name: str
    description: str
    category: str = "ai"
    enabled: bool = True
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'enabled': self.enabled,
            'parameters': self.parameters
        }

