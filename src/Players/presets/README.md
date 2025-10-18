# Player Presets - Pure Metadata Approach

**Configuration as Data** - All players defined declaratively using metadata only.

## Philosophy

Instead of creating redundant `create_*()` functions for each player, we use a **pure declarative approach**:

- **ONE metadata file** (`metadata.py`) with all player configurations
- **ONE generic factory** (`PresetFactory`) that creates players from metadata
- **DRY principle** - Don't Repeat Yourself
- **Single Source of Truth** - All configuration in one place

## Structure

```
src/Players/presets/
├── __init__.py       # Exports + backward compatibility
├── metadata.py       # PLAYER_PRESETS (pure configuration)
├── factory.py        # PresetFactory (generic logic)
└── README.md         # This file
```

**Just 4 files** - Clean, simple, maintainable!

---

## Quick Start

### Method 1: PresetFactory (Recommended)

```python
from Players.presets import PresetFactory

# Create any player
player = PresetFactory.create('Grandmaster')
player = PresetFactory.create('Bitboard Blitz', depth=7)
player = PresetFactory.create('Ultimate AI', depth=10, threads=8)

# List available
presets = PresetFactory.list_available()
# → ['Random Chaos', 'Alpha-Beta AI', ...]

# Get metadata
meta = PresetFactory.get_metadata('Grandmaster')
print(meta['icon'])          # 👑
print(meta['description'])   # "Ultimate AI - All techniques combined"
print(meta['difficulty'])    # "expert"
```

### Method 2: Convenience Functions (Backward Compatible)

```python
from Players.presets import create_grandmaster, create_bitboard_blitz

player1 = create_grandmaster(depth=9)
player2 = create_bitboard_blitz(depth=7)
```

### Method 3: Direct Metadata Access

```python
from Players.presets import PLAYER_PRESETS, PresetFactory

# Browse all configurations
for name, config in PLAYER_PRESETS.items():
    print(f"{config['icon']} {name} - {config['description']}")

# Create from configuration
player = PresetFactory.create('Grandmaster', depth=12)
```

---

## Available Presets

| Icon | Name | Engine | Difficulty | Speed | Strength | Features |
|------|------|--------|------------|-------|----------|----------|
| 🎲 | Random Chaos | random | beginner | instant | very_weak | - |
| 🎯 | Alpha-Beta AI | minimax | intermediate | medium | medium | Alpha-beta pruning |
| 📚 | Opening Scholar | minimax | intermediate | medium | medium_strong | Opening book |
| ⚡ | Bitboard Blitz | bitboard | advanced | fast | strong | Bitboard (10x faster) |
| 🔮 | The Oracle | bitboard | advanced | fast | strong | Bitboard + Book |
| 🍖 | Greedy Gobbler | greedy | beginner | fast | weak | Maximize captures |
| 🎓 | Positional Master | heuristic | intermediate | medium | medium | Strategic positioning |
| 👑 | Grandmaster | grandmaster | expert | slow | master | All techniques |
| 🚀 | Ultimate AI | bitboard | expert | medium | very_strong | All features + parallel |

---

## Adding New Presets

**Super simple** - just add an entry to `metadata.py`:

```python
# In metadata.py, add to PLAYER_PRESETS dict:
'My Awesome Player': {
    'engine_type': 'minimax',        # Engine to use
    'default_depth': 5,              # Default search depth
    'name': 'My Awesome Player',     # Display name
    'description': 'Does awesome things',
    'difficulty': 'intermediate',    # beginner/intermediate/advanced/expert
    'speed': 'medium',               # instant/fast/medium/slow
    'strength': 'medium',            # very_weak/weak/medium/strong/very_strong/master
    'enabled': True,                 # Enable/disable
    'icon': '🌟',                    # Optional icon
    'features': ['opening_book'],    # Optional features
    'parameters': [                  # Optional configurable parameters
        {
            'name': 'depth',
            'type': 'int',
            'default': 5,
            'min': 1,
            'max': 10,
            'description': 'Search depth'
        }
    ]
}
```

**That's it!** No additional code needed - `PresetFactory` handles everything automatically.

---

## Architecture Benefits

### DRY (Don't Repeat Yourself)
- No redundant `create_*()` functions
- Single generic factory handles all players
- Metadata defined once, used everywhere

### Declarative
- **Configuration as data**, not code
- Easy to understand at a glance
- Could be loaded from JSON/YAML if needed

### Single Source of Truth
- All player configurations in `metadata.py`
- Change in one place, affects everywhere
- No synchronization issues

### Maintainable
- 4 files instead of 13
- Clear separation: data (`metadata.py`) vs logic (`factory.py`)
- Easy to test (metadata is just data)

### Extensible
- Add new player: add metadata entry
- Modify player: edit metadata
- No code changes needed!

---

## Configuration Fields

### Required Fields
- `engine_type`: Engine to use ('random', 'minimax', 'bitboard', 'grandmaster', 'greedy', 'heuristic')
- `name`: Display name
- `description`: Short description
- `difficulty`: Player difficulty level
- `speed`: Execution speed
- `strength`: Playing strength
- `enabled`: Whether preset is active

### Optional Fields
- `icon`: Emoji icon for display
- `default_depth`: Default search depth
- `features`: List of features to enable
- `engine_config`: Advanced engine configuration
- `parameters`: Configurable parameters with UI metadata

---

## Examples

### Simple Player
```python
player = PresetFactory.create('Random Chaos')
# Uses default configuration from metadata
```

### With Custom Depth
```python
player = PresetFactory.create('Grandmaster', depth=12)
# Override default_depth (9) with 12
```

### With All Parameters
```python
player = PresetFactory.create('Ultimate AI', depth=10, threads=8)
# Custom depth and parallel threads
```

### Browse and Create Programmatically
```python
from Players.presets import PLAYER_PRESETS, PresetFactory

# Show all available
for name, config in PLAYER_PRESETS.items():
    if config['difficulty'] == 'expert':
        print(f"{config['icon']} {name} - {config['description']}")
        player = PresetFactory.create(name)
        # Use player...
```

---

## Metadata Structure

```python
PLAYER_PRESETS = {
    'Player Name': {
        # Engine configuration
        'engine_type': 'minimax',
        'default_depth': 5,
        
        # Display information
        'name': 'Player Name',
        'description': 'Short description',
        'icon': '🌟',
        
        # Classification
        'difficulty': 'intermediate',
        'speed': 'medium',
        'strength': 'medium',
        'enabled': True,
        
        # Optional: Features
        'features': ['opening_book', 'parallel'],
        
        # Optional: Advanced engine config
        'engine_config': {
            'use_bitboard': True,
            'parallel_threads': 4
        },
        
        # Optional: UI parameters
        'parameters': [
            {
                'name': 'depth',
                'type': 'int',
                'default': 5,
                'min': 1,
                'max': 10,
                'description': 'Search depth'
            }
        ]
    }
}
```

---

## Migration from Old Approach

**Before** (9 separate files):
```python
# File: grandmaster.py
def create_grandmaster(depth=9, name="Grandmaster"):
    from Players.ai.ai_player import AIPlayer
    engine = EngineRegistry.get_engine('grandmaster')()
    return AIPlayer(engine=engine, depth=depth, name=name)
```

**After** (Pure metadata):
```python
# File: metadata.py
'Grandmaster': {
    'engine_type': 'grandmaster',
    'default_depth': 9,
    'name': 'Grandmaster',
    ...
}

# Usage:
player = PresetFactory.create('Grandmaster', depth=9)
```

**Result**: Same functionality, 70% less code!

---

## Design Principles

1. **Configuration as Data** - Metadata is just data, not code
2. **Generic Logic** - One factory handles all cases
3. **DRY** - Don't Repeat Yourself
4. **SOLID** - Open/Closed principle (open for extension via metadata)
5. **Clean Code** - Minimal, focused files

---

## Future Enhancements

Possible extensions (without breaking changes):

- Load presets from JSON/YAML files
- User-defined presets in `~/.reversi42/presets/`
- Preset inheritance (base + overrides)
- Preset versioning
- Preset validation schema

All achievable by just modifying `metadata.py` and `factory.py`!

---

**Version**: 3.2.0  
**Last Updated**: 2025-10-18  
**Architecture**: Pure Declarative Configuration
