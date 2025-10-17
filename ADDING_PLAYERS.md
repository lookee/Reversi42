# Adding New Player Types to Reversi42

## Overview

Reversi42 uses a metadata-driven system for player types. The menu automatically generates options based on player metadata, making it easy to add new player types without modifying menu code.

## Quick Start

### 1. Create Your Player Class

Create a new file in `src/Players/`:

```python
from Players.Player import Player
from Reversi.Game import Move

class MyCustomPlayer(Player):
    
    # Define metadata for automatic menu integration
    PLAYER_METADATA = {
        'display_name': 'MyPlayer',
        'description': 'My custom AI strategy',
        'enabled': True,  # Set to False to hide from menu
        'parameters': [
            {
                'name': 'difficulty',
                'display_name': 'Difficulty',
                'type': 'int',
                'min': 1,
                'max': 10,
                'default': 5,
                'description': 'How strong the player is'
            }
        ]
    }
    
    def __init__(self, name='MyPlayer', difficulty=5):
        self.name = name
        self.difficulty = difficulty
    
    def get_move(self, game, moves, control):
        # Your move selection logic here
        return moves[0] if moves else None
```

### 2. Register in PlayerFactory

Edit `src/Players/PlayerFactory.py`:

```python
from Players.MyCustomPlayer import MyCustomPlayer

class PlayerFactory:
    ALL_PLAYER_CLASSES = [
        HumanPlayer,
        AIPlayer,
        MyCustomPlayer,  # Add your player here
        ...
    ]
```

### 3. Done!

Your player will automatically appear in:
- ✓ Main menu player selection
- ✓ Help screen with description
- ✓ Tournament system
- ✓ PlayerFactory API

## Metadata Reference

### Required Fields

```python
PLAYER_METADATA = {
    'display_name': str,    # Name shown in menus
    'description': str,     # Short description
    'enabled': bool,        # True to show in menu
    'parameters': list      # List of parameter definitions
}
```

### Parameter Definition

Each parameter in the `parameters` list is a dict:

```python
{
    'name': str,           # Parameter name (used in __init__)
    'display_name': str,   # Displayed in menu
    'type': str,           # 'int', 'float', 'str', 'bool', 'choice'
    'min': int/float,      # Minimum value (for int/float)
    'max': int/float,      # Maximum value (for int/float)
    'choices': list,       # Available choices (for 'choice' type)
    'default': any,        # Default value
    'description': str     # Help text
}
```

### Parameter Types

**int**: Integer value with min/max
```python
{
    'name': 'depth',
    'type': 'int',
    'min': 1,
    'max': 10,
    'default': 6,
    ...
}
```

**float**: Floating point with min/max
```python
{
    'name': 'temperature',
    'type': 'float',
    'min': 0.0,
    'max': 1.0,
    'default': 0.5,
    ...
}
```

**str**: String value
```python
{
    'name': 'server_url',
    'type': 'str',
    'default': 'localhost:8080',
    ...
}
```

**bool**: Boolean flag
```python
{
    'name': 'use_opening_book',
    'type': 'bool',
    'default': True,
    ...
}
```

**choice**: Selection from predefined options
```python
{
    'name': 'strategy',
    'type': 'choice',
    'choices': ['Aggressive', 'Defensive', 'Balanced'],
    'default': 'Balanced',
    ...
}
```

## Complete Examples

### Example 1: Simple Player (No Parameters)

```python
class SimpleAI(Player):
    PLAYER_METADATA = {
        'display_name': 'Simple',
        'description': 'Basic AI for beginners',
        'enabled': True,
        'parameters': []
    }
    
    def __init__(self, name='Simple'):
        self.name = name
    
    def get_move(self, game, moves, control):
        # Simple strategy
        return moves[0] if moves else None
```

### Example 2: Configurable AI

```python
class ConfigurableAI(Player):
    PLAYER_METADATA = {
        'display_name': 'Configurable',
        'description': 'AI with multiple settings',
        'enabled': True,
        'parameters': [
            {
                'name': 'strength',
                'display_name': 'Strength',
                'type': 'int',
                'min': 1,
                'max': 10,
                'default': 5,
                'description': 'AI strength level'
            },
            {
                'name': 'style',
                'display_name': 'Playing Style',
                'type': 'choice',
                'choices': ['Aggressive', 'Defensive', 'Balanced'],
                'default': 'Balanced',
                'description': 'Preferred playing style'
            }
        ]
    }
    
    def __init__(self, name='Configurable', strength=5, style='Balanced'):
        self.name = name
        self.strength = strength
        self.style = style
```

### Example 3: Disabled Player (Development/Testing)

```python
class ExperimentalAI(Player):
    PLAYER_METADATA = {
        'display_name': 'Experimental',
        'description': 'Work in progress - not ready',
        'enabled': False,  # Not shown in menu
        'parameters': []
    }
    
    # Can still be created programmatically via PlayerFactory
    # Just won't appear in menu selection
```

## Disabling Players

To temporarily disable a player:

1. **Set enabled=False** in metadata:
   ```python
   PLAYER_METADATA = {
       ...
       'enabled': False,
   }
   ```

2. Player will be hidden from menus but still available via PlayerFactory

Use cases:
- Players under development
- Experimental features
- Platform-specific players (e.g., NetworkPlayer)
- Debugging/testing

## Benefits of This System

✅ **Automatic Menu Generation**: No manual menu editing
✅ **Self-Documenting**: Descriptions in metadata
✅ **Type Safety**: Parameter types defined
✅ **Easy to Extend**: Just add a class
✅ **Enable/Disable**: Simple flag toggle
✅ **Consistent**: All players follow same pattern

## Testing Your Player

```python
# Test programmatically first
from Players.PlayerFactory import PlayerFactory

# Create player
player = PlayerFactory.create_player('MyPlayer', difficulty=7)

# Test in game
from Reversi.Game import Game
g = Game(8)
moves = g.get_move_list()
move = player.get_move(g, moves, None)
print(f"Selected: {move}")
```

## Complete Workflow

1. **Create** player class with metadata
2. **Add** to PlayerFactory.ALL_PLAYER_CLASSES
3. **Test** programmatically
4. **Enable** in metadata when ready
5. **Done** - automatically in all menus!

---

See `src/Players/CustomPlayerExample.py` for a complete working example.

