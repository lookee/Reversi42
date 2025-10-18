"""
Player Factory V2 - Epic Players Edition!

Uses metadata-driven system with all 9 epic AI warriors!

Version: 3.1.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from typing import Dict, Any

# Lazy load to avoid circular imports
PLAYER_PRESETS = None
PresetFactory = None

def _lazy_load():
    """Lazy load presets to avoid circular imports."""
    global PLAYER_PRESETS, PresetFactory
    if PLAYER_PRESETS is None:
        from Players.presets.metadata import PLAYER_PRESETS as _PRESETS
        from Players.presets.factory import PresetFactory as _Factory
        PLAYER_PRESETS = _PRESETS
        PresetFactory = _Factory
    return PLAYER_PRESETS, PresetFactory


class PlayerFactoryV2:
    """Epic Player Factory - Creates legendary AI warriors!"""
    
    @classmethod
    def create_player(cls, player_type: str, **kwargs):
        """Create any epic player!"""
        presets, factory = _lazy_load()
        
        if player_type in ['Human Player', 'HumanPlayer']:
            from Players.HumanPlayer import HumanPlayer
            return HumanPlayer()
        
        if player_type == 'Terminal Human':
            from ui.implementations.terminal.player import TerminalHumanPlayer
            return TerminalHumanPlayer(name=kwargs.get('name', 'Terminal Human'))
        
        if player_type in ['Network Player', 'NetworkPlayer']:
            from Players.NetworkPlayer import NetworkPlayer
            return NetworkPlayer()
        
        if player_type in presets:
            # NOTE: PresetFactory.create() is the correct method!
            return factory.create(player_type, **kwargs)
        
        available = ', '.join(presets.keys())
        raise ValueError(f"Unknown player type: {player_type}. Available: {available}")
    
    @classmethod
    def create_ai_player(cls, engine_type: str = 'Minimax', difficulty: int = 6):
        """Create AI by engine type."""
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
        
        return {'display_name': player_type, 'description': f'{player_type} player', 'enabled': True}
    
    @classmethod
    def list_available_players(cls) -> Dict[str, Dict[str, Any]]:
        """List ALL available epic players!"""
        presets, _ = _lazy_load()
        result = {}
        
        from Players.HumanPlayer import HumanPlayer
        result['Human Player'] = HumanPlayer.PLAYER_METADATA.copy()
        
        for name, metadata in presets.items():
            result[name] = metadata.copy()
        
        return result


__all__ = ['PlayerFactoryV2']
