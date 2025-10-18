"""
Player Factory V2

Backward-compatible factory using new architecture.
Replaces Players/PlayerFactory.py with modular design.

Version: 3.2.0
Architecture: Abstract Factory Pattern
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from typing import Dict, Any
from Players.ai.ai_player import AIPlayer
from Players.factory.player_presets import PlayerPresets


class PlayerFactoryV2:
    """
    Smart player factory with backward compatibility.
    
    Replaces the old hardcoded PlayerFactory with a modular design.
    Maintains compatibility with existing code while using new architecture.
    
    Example:
        # Old style (still works)
        player = PlayerFactoryV2.create_player('Alpha-Beta AI', deep=6)
        
        # New style (more flexible)
        from engines.factory.engine_builder import EngineBuilder
        engine = EngineBuilder().use_bitboard().with_opening_book().build()
        player = AIPlayer(engine, depth=8)
    """
    
    # Mapping from old display names to new preset methods
    PRESET_MAPPING = {
        'Random Chaos': lambda **kwargs: PlayerPresets.create_random(),
        'Alpha-Beta AI': lambda deep=6, **kwargs: PlayerPresets.create_alpha_beta(depth=deep),
        'Opening Scholar': lambda deep=6, **kwargs: PlayerPresets.create_opening_scholar(depth=deep),
        'Bitboard Blitz': lambda deep=6, **kwargs: PlayerPresets.create_bitboard_blitz(depth=deep),
        'The Oracle': lambda deep=7, **kwargs: PlayerPresets.create_oracle(depth=deep),
        'Parallel Oracle': lambda deep=7, threads=4, **kwargs: PlayerPresets.create_parallel_oracle(depth=deep, threads=threads),
        'Grandmaster': lambda deep=9, **kwargs: PlayerPresets.create_grandmaster(depth=deep),
        'Greedy Gobbler': lambda **kwargs: PlayerPresets.create_greedy(),
        'Heuristic Hero': lambda deep=4, **kwargs: PlayerPresets.create_heuristic(depth=deep),
    }
    
    @classmethod
    def create_player(cls, player_type: str, **kwargs) -> 'Player':
        """
        Create player by type name (backward compatible).
        
        Args:
            player_type: Player type name
            **kwargs: Configuration parameters (deep, threads, etc.)
        
        Returns:
            Player: Configured player instance
        
        Raises:
            ValueError: If player type unknown
        """
        # Handle AI players using presets
        if player_type in cls.PRESET_MAPPING:
            return cls.PRESET_MAPPING[player_type](**kwargs)
        
        # Handle human players
        if player_type in ['Human Player', 'HumanPlayer']:
            from Players.HumanPlayer import HumanPlayer
            return HumanPlayer()
        
        if player_type == 'Terminal Human':
            from ui.implementations.terminal.player import TerminalHumanPlayer
            return TerminalHumanPlayer(name=kwargs.get('name', 'Terminal Human'))
        
        # Handle network player
        if player_type in ['Network Player', 'NetworkPlayer']:
            from Players.NetworkPlayer import NetworkPlayer
            return NetworkPlayer()
        
        # Unknown player type
        available = ', '.join(cls.PRESET_MAPPING.keys())
        raise ValueError(
            f"Unknown player type: {player_type}. "
            f"Available types: {available}, Human Player, Terminal Human, Network Player"
        )
    
    @classmethod
    def create_ai_player(cls, engine_type: str = 'Minimax', difficulty: int = 6) -> AIPlayer:
        """
        Create AI player with specific engine type.
        
        Args:
            engine_type: Engine type ('Minimax', 'Bitboard', 'Grandmaster')
            difficulty: Depth level (1-12)
        
        Returns:
            AIPlayer: Configured AI player
        """
        engine_type_lower = engine_type.lower()
        
        if engine_type_lower == 'minimax':
            return PlayerPresets.create_alpha_beta(depth=difficulty)
        elif engine_type_lower == 'bitboard':
            return PlayerPresets.create_bitboard_blitz(depth=difficulty)
        elif engine_type_lower == 'grandmaster':
            return PlayerPresets.create_grandmaster(depth=difficulty)
        else:
            # Default to minimax
            return PlayerPresets.create_alpha_beta(depth=difficulty)
    
    @classmethod
    def get_player_metadata(cls, player_type: str) -> Dict[str, Any]:
        """
        Get metadata for player type (backward compatible).
        
        Args:
            player_type: Player type name
        
        Returns:
            dict: Player metadata
        """
        # Check if Human Player
        if player_type == 'Human Player':
            from Players.HumanPlayer import HumanPlayer
            return HumanPlayer.PLAYER_METADATA.copy()
        
        # Fallback to default
        return {
            'display_name': player_type,
            'description': f'{player_type} player',
            'enabled': True,
            'parameters': []
        }
    
    @classmethod
    def list_available_players(cls) -> Dict[str, Dict[str, Any]]:
        """
        List all available players with metadata.
        
        Returns:
            Dict mapping player names to metadata
        """
        result = {}
        
        # Add Human Player FIRST
        from Players.HumanPlayer import HumanPlayer
        result['Human Player'] = HumanPlayer.PLAYER_METADATA.copy()
        
        # Add all AI presets
        for preset_name in cls.PRESET_MAPPING.keys():
            result[preset_name] = {
                'display_name': preset_name,
                'description': f'{preset_name} player',
                'enabled': True,
                'type': 'AI',
                'parameters': []
            }
        
        return result
