"""
Player Presets - Pure Metadata Approach

All player configurations defined declaratively using metadata only.
No redundant create_*() functions needed.

A generic factory creates players from these metadata configurations.
"""

# All player presets defined as pure metadata
PLAYER_PRESETS = {
    'Random Chaos': {
        'engine_type': 'random',
        'default_depth': 1,
        'name': 'Random Chaos',
        'description': 'Random Chaos - Unpredictable moves',
        'difficulty': 'beginner',
        'speed': 'instant',
        'strength': 'very_weak',
        'enabled': True,
        'icon': '🎲'
    },
    
    'Alpha-Beta AI': {
        'engine_type': 'minimax',
        'default_depth': 4,
        'name': 'Alpha-Beta AI',
        'description': 'Classic minimax with alpha-beta pruning',
        'difficulty': 'intermediate',
        'speed': 'medium',
        'strength': 'medium',
        'enabled': True,
        'icon': '🎯',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 4,
                'min': 1,
                'max': 8,
                'description': 'Search depth (higher = stronger but slower)'
            }
        ]
    },
    
    'Opening Scholar': {
        'engine_type': 'minimax',
        'default_depth': 5,
        'name': 'Opening Scholar',
        'description': 'Minimax with opening book knowledge',
        'difficulty': 'intermediate',
        'speed': 'medium',
        'strength': 'medium_strong',
        'enabled': True,
        'icon': '📚',
        'features': ['opening_book'],
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 5,
                'min': 1,
                'max': 8,
                'description': 'Search depth'
            }
        ]
    },
    
    'Bitboard Blitz': {
        'engine_type': 'bitboard',
        'default_depth': 6,
        'name': 'Bitboard Blitz',
        'description': 'Ultra-fast bitboard - 10x faster',
        'difficulty': 'advanced',
        'speed': 'fast',
        'strength': 'strong',
        'enabled': True,
        'icon': '⚡',
        'features': ['bitboard', 'optimized'],
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 6,
                'min': 1,
                'max': 10,
                'description': 'Search depth (can go deeper due to speed)'
            }
        ]
    },
    
    'The Oracle': {
        'engine_type': 'bitboard',
        'default_depth': 6,
        'name': 'The Oracle',
        'description': 'Bitboard + opening book - Fast & knowledgeable',
        'difficulty': 'advanced',
        'speed': 'fast',
        'strength': 'strong',
        'enabled': True,
        'icon': '🔮',
        'features': ['bitboard', 'opening_book'],
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 6,
                'min': 1,
                'max': 10,
                'description': 'Search depth'
            }
        ]
    },
    
    'Greedy Gobbler': {
        'engine_type': 'greedy',
        'default_depth': 1,
        'name': 'Greedy Gobbler',
        'description': 'Aggressive - Maximizes captures',
        'difficulty': 'beginner',
        'speed': 'fast',
        'strength': 'weak',
        'enabled': True,
        'icon': '🍖'
    },
    
    'Positional Master': {
        'engine_type': 'heuristic',
        'default_depth': 4,
        'name': 'Positional Master',
        'description': 'Strategic positioning - Corners & edges',
        'difficulty': 'intermediate',
        'speed': 'medium',
        'strength': 'medium',
        'enabled': True,
        'icon': '🎓',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 4,
                'min': 1,
                'max': 8,
                'description': 'Search depth'
            }
        ]
    },
    
    'Grandmaster': {
        'engine_type': 'grandmaster',
        'default_depth': 9,
        'name': 'Grandmaster',
        'description': 'Ultimate AI - All techniques combined',
        'difficulty': 'expert',
        'speed': 'slow',
        'strength': 'master',
        'enabled': True,
        'icon': '👑',
        'features': ['bitboard', 'advanced_eval', 'move_ordering', 'killer_moves'],
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 9,
                'min': 1,
                'max': 12,
                'description': 'Search depth (very slow at high depths)'
            }
        ]
    },
    
    'Ultimate AI': {
        'engine_type': 'bitboard',
        'default_depth': 8,
        'name': 'Ultimate AI',
        'description': 'Maximum power - All features enabled',
        'difficulty': 'expert',
        'speed': 'medium',
        'strength': 'very_strong',
        'enabled': True,
        'icon': '🚀',
        'features': ['bitboard', 'opening_book', 'parallel', 'transposition_table', 'advanced_eval'],
        'engine_config': {
            'use_bitboard': True,
            'opening_book': True,
            'parallel_threads': 4,
            'transposition_table_mb': 128,
            'advanced_evaluator': True
        },
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 8,
                'min': 1,
                'max': 10,
                'description': 'Search depth'
            },
            {
                'name': 'threads',
                'type': 'int',
                'default': 4,
                'min': 1,
                'max': 16,
                'description': 'Parallel threads'
            }
        ]
    }
}


def get_preset(name: str) -> dict:
    """
    Get preset metadata by name.
    
    Args:
        name: Preset name
    
    Returns:
        Preset metadata dict
    
    Raises:
        KeyError: If preset not found
    """
    if name not in PLAYER_PRESETS:
        available = ', '.join(PLAYER_PRESETS.keys())
        raise KeyError(f"Preset '{name}' not found. Available: {available}")
    
    return PLAYER_PRESETS[name].copy()


def list_presets() -> dict:
    """
    Get all available presets.
    
    Returns:
        Dict of all presets
    """
    return PLAYER_PRESETS.copy()


__all__ = ['PLAYER_PRESETS', 'get_preset', 'list_presets']

