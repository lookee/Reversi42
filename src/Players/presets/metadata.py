"""
Player Presets - Epic Collection

All player configurations defined declaratively using metadata only.

Epic Players with unique personalities, styles, and strengths!
"""

# All player presets defined as pure metadata
PLAYER_PRESETS = {
    # ═══════════════════════════════════════════════════════════════
    # BEGINNER TIER - Learn the basics
    # ═══════════════════════════════════════════════════════════════
    
    'Random Chaos': {
        'engine_type': 'random',
        'default_depth': 1,
        'name': 'Random Chaos',
        'description': '🎲 Pure randomness - Moves without thinking. Perfect for absolute beginners!',
        'difficulty': 'beginner',
        'speed': 'instant',
        'strength': 'very_weak',
        'enabled': True,
        'icon': '🎲',
        'play_style': 'chaotic',
        'specialty': 'Completely unpredictable, no strategy'
    },
    
    'Hungry Hippo': {
        'engine_type': 'greedy',
        'default_depth': 3,
        'name': 'Hungry Hippo',
        'description': '🦛 Greedy but smarter - Looks 3 moves ahead while maximizing captures',
        'difficulty': 'beginner',
        'speed': 'very_fast',
        'strength': 'weak',
        'enabled': True,
        'icon': '🦛',
        'play_style': 'greedy',
        'specialty': 'Short-term thinking, captures everything in sight',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 3,
                'min': 1,
                'max': 5,
                'description': 'Look-ahead depth'
            }
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # INTERMEDIATE TIER - Develop tactics
    # ═══════════════════════════════════════════════════════════════
    
    'Berserker': {
        'engine_type': 'greedy',
        'default_depth': 5,
        'name': 'Berserker',
        'description': '⚔️ Relentless aggressor - Attacks without mercy!',
        'difficulty': 'intermediate',
        'speed': 'very_fast',
        'strength': 'medium_strong',
        'enabled': True,
        'icon': '⚔️',
        'features': ['aggressive_captures', 'high_mobility'],
        'play_style': 'aggressive',
        'specialty': 'Overwhelming captures, high-pressure attacks',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 5,
                'min': 2,
                'max': 8,
                'description': 'Aggression depth'
            }
        ]
    },
    
    'Zen Master': {
        'engine_type': 'minimax',
        'default_depth': 8,
        'name': 'Zen Master',
        'description': '🧘 Perfect harmony - Achieves balance between offense and defense',
        'difficulty': 'intermediate',
        'speed': 'medium',
        'strength': 'very_strong',
        'enabled': True,
        'icon': '🧘',
        'features': ['balanced_strategy', 'advanced_eval'],
        'play_style': 'balanced',
        'specialty': 'Maintains equilibrium, adapts to opponent style',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 8,
                'min': 4,
                'max': 11,
                'description': 'Meditation depth'
            }
        ]
    },
    
    'The Trickster': {
        'engine_type': 'minimax',
        'default_depth': 6,
        'name': 'The Trickster',
        'description': '🎭 Mind games master - Makes unconventional moves to confuse opponents',
        'difficulty': 'intermediate',
        'speed': 'fast',
        'strength': 'strong',
        'enabled': True,
        'icon': '🎭',
        'features': ['unpredictable', 'psychological'],
        'play_style': 'unconventional',
        'specialty': 'Breaks expectations, creates traps',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 6,
                'min': 3,
                'max': 9,
                'description': 'Trickery depth'
            }
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # ADVANCED TIER - Master strategy
    # ═══════════════════════════════════════════════════════════════
    
    'The Shadow': {
        'engine_type': 'heuristic',
        'default_depth': 7,
        'name': 'The Shadow',
        'description': '🌑 Silent defender - Lurks in darkness, strikes from shadows',
        'difficulty': 'advanced',
        'speed': 'medium',
        'strength': 'strong',
        'enabled': True,
        'icon': '🌑',
        'features': ['defensive_strategy', 'corner_control'],
        'play_style': 'defensive',
        'specialty': 'Controls board edges and waits for opponent mistakes',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 7,
                'min': 3,
                'max': 10,
                'description': 'Calculation depth'
            }
        ]
    },
    
    'Ancient Sage': {
        'engine_type': 'bitboard',
        'default_depth': 7,
        'name': 'Ancient Sage',
        'description': '📜 Wisdom of ages - Knows every classical opening',
        'difficulty': 'advanced',
        'speed': 'medium_fast',
        'strength': 'very_strong',
        'enabled': True,
        'icon': '📜',
        'features': ['bitboard', 'opening_book'],
        'play_style': 'traditional',
        'specialty': 'Perfect openings, legendary endgame technique',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 7,
                'min': 4,
                'max': 10,
                'description': 'Ancient wisdom depth'
            }
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # EXPERT TIER - Ultimate challenge
    # ═══════════════════════════════════════════════════════════════
    
    'Quantum Mind': {
        'engine_type': 'bitboard',
        'default_depth': 9,
        'name': 'Quantum Mind',
        'description': '🌌 Explores infinite possibilities - Thinks in parallel dimensions',
        'difficulty': 'expert',
        'speed': 'fast',
        'strength': 'master',
        'enabled': True,
        'icon': '🌌',
        'features': ['bitboard', 'parallel'],
        'play_style': 'analytical',
        'specialty': 'Multi-threaded deep search',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 9,
                'min': 5,
                'max': 12,
                'description': 'Quantum depth'
            },
            {
                'name': 'threads',
                'type': 'int',
                'default': 16,
                'min': 1,
                'max': 32,
                'description': 'Parallel universes'
            }
        ]
    },
    
    # ═══════════════════════════════════════════════════════════════
    # LEGENDARY TIER - Final Boss
    # ═══════════════════════════════════════════════════════════════
    
    'Apocalypse': {
        'engine_type': 'grandmaster',
        'default_depth': 11,
        'name': 'Apocalypse',
        'description': '💀 THE END IS NEAR - Ultimate AI fusion! Undefeated. Unstoppable.',
        'difficulty': 'LEGENDARY',
        'speed': 'adaptive',
        'strength': 'GODLIKE',
        'enabled': True,
        'icon': '💀',
        'features': [
            'grandmaster_engine',
            'bitboard'
        ],
        'play_style': 'ANNIHILATION',
        'specialty': 'Everything. Everywhere. All at once.',
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 11,
                'min': 7,
                'max': 15,
                'description': '⚠️  WARNING: Depth >12 may take MINUTES per move!'
            },
            {
                'name': 'threads',
                'type': 'int',
                'default': 32,
                'min': 4,
                'max': 64,
                'description': 'CPU cores'
            }
        ],
        'warnings': [
            '⚠️  EXTREMELY SLOW at depth >10',
            '⚠️  Requires 8+ CPU cores',
            '⚠️  May consume 1GB+ RAM'
        ]
    }
}


def get_preset(name: str) -> dict:
    """Get preset metadata by name."""
    if name not in PLAYER_PRESETS:
        available = ', '.join(PLAYER_PRESETS.keys())
        raise KeyError(f"Preset '{name}' not found. Available: {available}")
    return PLAYER_PRESETS[name].copy()


def list_presets() -> dict:
    """Get all available presets."""
    return PLAYER_PRESETS.copy()


__all__ = ['PLAYER_PRESETS', 'get_preset', 'list_presets']
