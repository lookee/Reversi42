"""
Player Factory V2 - Epic Players Edition!

Loads all 9 epic AI warriors dynamically from metadata!

Version: 3.1.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from typing import Dict, Any

# Lazy load to avoid circular imports
_PLAYER_PRESETS = None
_PresetFactory = None

def _lazy_load():
    """Lazy load epic players from metadata."""
    global _PLAYER_PRESETS, _PresetFactory
    if _PLAYER_PRESETS is None:
        from Players.presets.metadata import PLAYER_PRESETS
        from Players.presets.factory import PresetFactory
        _PLAYER_PRESETS = PLAYER_PRESETS
        _PresetFactory = PresetFactory
    return _PLAYER_PRESETS, _PresetFactory


class PlayerFactoryV2:
    """Epic Player Factory - Creates all 9 legendary AI warriors!"""
    
    @classmethod
    def create_player(cls, player_type: str, **kwargs):
        """Create any epic player by name!"""
        presets, factory = _lazy_load()
        
        # Human players
        if player_type in ['Human Player', 'HumanPlayer']:
            from Players.HumanPlayer import HumanPlayer
            return HumanPlayer()
        
        if player_type == 'Terminal Human':
            from ui.implementations.terminal.player import TerminalHumanPlayer
            return TerminalHumanPlayer(name=kwargs.get('name', 'Terminal Human'))
        
        # Network player
        if player_type in ['Network Player', 'NetworkPlayer']:
            from Players.NetworkPlayer import NetworkPlayer
            return NetworkPlayer()
        
        # Epic AI players from metadata
        if player_type in presets:
            return factory.create(player_type, **kwargs)
        
        # Unknown player
        available = ', '.join(presets.keys())
        raise ValueError(f"Unknown player: {player_type}. Available: {available}")
    
    @classmethod
    def create_ai_player(cls, engine_type: str = 'Minimax', difficulty: int = 6):
        """Create AI by engine type (maps to epic players)."""
        mapping = {
            'minimax': 'Zen Master',
            'bitboard': 'Ancient Sage',
            'grandmaster': 'Apocalypse',
            'random': 'Random Chaos',
            'greedy': 'Hungry Hippo',
            'heuristic': 'The Shadow'
        }
        player_type = mapping.get(engine_type.lower(), 'Zen Master')
        return cls.create_player(player_type, depth=difficulty)
    
    @classmethod
    def get_player_metadata(cls, player_type: str) -> Dict[str, Any]:
        """Get metadata for any player."""
        presets, _ = _lazy_load()
        
        if player_type == 'Human Player':
            from Players.HumanPlayer import HumanPlayer
            return HumanPlayer.PLAYER_METADATA.copy()
        
        if player_type in presets:
            return presets[player_type].copy()
        
        return {'display_name': player_type, 'description': f'{player_type}', 'enabled': True}
    
    @classmethod
    def list_available_players(cls) -> Dict[str, Dict[str, Any]]:
        """List ALL 10 epic players (Human + 9 AI)!"""
        presets, _ = _lazy_load()
        result = {}
        
        # Human Player first
        from Players.HumanPlayer import HumanPlayer
        result['Human Player'] = HumanPlayer.PLAYER_METADATA.copy()
        
        # All 9 epic AI players from metadata
        for name, metadata in presets.items():
            result[name] = metadata.copy()
        
        return result


__all__ = ['PlayerFactoryV2']
