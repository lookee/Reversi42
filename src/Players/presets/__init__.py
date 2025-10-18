"""
Player Presets Module - Pure Metadata Approach

All players defined declaratively using metadata only.
No redundant create_*() functions - just use PresetFactory!

Quick Start:
    from Players.presets import PresetFactory
    
    # Create any player
    player = PresetFactory.create('Grandmaster')
    player = PresetFactory.create('Bitboard Blitz', depth=7)
    
    # List available
    presets = PresetFactory.list_available()
    
    # Get metadata
    meta = PresetFactory.get_metadata('Grandmaster')

Available Presets:
- Random Chaos 🎲: Completely random moves
- Alpha-Beta AI 🎯: Classic minimax
- Opening Scholar 📚: Minimax + opening book
- Bitboard Blitz ⚡: Ultra-fast bitboard
- The Oracle 🔮: Bitboard + opening book
- Greedy Gobbler 🍖: Maximize captures
- Positional Master 🎓: Strategic positioning
- Grandmaster 👑: Ultimate challenge
- Ultimate AI 🚀: All features enabled
"""

from Players.presets.metadata import PLAYER_PRESETS, get_preset, list_presets
from Players.presets.factory import PresetFactory

# Backward compatibility - create convenience functions
def create_random_chaos(name="Random Chaos"):
    """Create Random Chaos player."""
    return PresetFactory.create('Random Chaos', name=name)

def create_alpha_beta(depth=4, name="Alpha-Beta AI"):
    """Create Alpha-Beta AI player."""
    return PresetFactory.create('Alpha-Beta AI', depth=depth, name=name)

def create_opening_scholar(depth=5, name="Opening Scholar"):
    """Create Opening Scholar player."""
    return PresetFactory.create('Opening Scholar', depth=depth, name=name)

def create_bitboard_blitz(depth=6, name="Bitboard Blitz"):
    """Create Bitboard Blitz player."""
    return PresetFactory.create('Bitboard Blitz', depth=depth, name=name)

def create_the_oracle(depth=6, name="The Oracle"):
    """Create The Oracle player."""
    return PresetFactory.create('The Oracle', depth=depth, name=name)

def create_greedy_gobbler(name="Greedy Gobbler"):
    """Create Greedy Gobbler player."""
    return PresetFactory.create('Greedy Gobbler', name=name)

def create_positional_master(depth=4, name="Positional Master"):
    """Create Positional Master player."""
    return PresetFactory.create('Positional Master', depth=depth, name=name)

def create_grandmaster(depth=9, name="Grandmaster"):
    """Create Grandmaster player."""
    return PresetFactory.create('Grandmaster', depth=depth, name=name)

def create_ultimate_ai(depth=8, threads=4, name="Ultimate AI"):
    """Create Ultimate AI player."""
    return PresetFactory.create('Ultimate AI', depth=depth, threads=threads, name=name)


# Build ALL_PRESETS for compatibility
ALL_PRESETS = {
    name: {
        'create': lambda n=name, **kw: PresetFactory.create(n, **kw),
        'metadata': metadata
    }
    for name, metadata in PLAYER_PRESETS.items()
}


__all__ = [
    # Primary interface (recommended)
    'PresetFactory',
    'PLAYER_PRESETS',
    'get_preset',
    'list_presets',
    
    # Convenience functions (backward compatibility)
    'create_random_chaos',
    'create_alpha_beta',
    'create_opening_scholar',
    'create_bitboard_blitz',
    'create_the_oracle',
    'create_greedy_gobbler',
    'create_positional_master',
    'create_grandmaster',
    'create_ultimate_ai',
    
    # Legacy
    'ALL_PRESETS'
]
