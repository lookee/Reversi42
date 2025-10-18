# Adding New Player Types to Reversi42

## Overview (Updated for v3.1.0)

Reversi42 uses a **metadata-driven system** for player types. The menu automatically generates options based on player metadata, making it trivial to add new player types without touching menu code.

**New in 3.1.0**: Tournament system now supports all player types including Grandmaster. Complete player documentation available in docs/players/.

## Quick Start

### 1. Create Your Player Class

Create a new file in `src/Players/`:

```python
from Players.Player import Player
from Reversi.Game import Move
import random

class MyCustomPlayer(Player):
    
    # Define metadata for automatic menu integration
    PLAYER_METADATA = {
        'display_name': 'MyPlayer',
        'description': 'My custom AI strategy',
        'enabled': True,  # Set to False to hide from menu
        'parameters': {
            'difficulty': {
                'type': int,
                'min': 1,
                'max': 10,
                'default': 5,
                'description': 'How strong the player is'
            }
        }
    }
    
    def __init__(self, deep=5):
        super().__init__()
        self.deep = deep
        self.name = f"MyPlayer{deep}"  # Name with difficulty
    
    def get_move(self, game, moves, control):
        # Your move selection logic here
        if not moves:
            return None
        
        # Example: random selection
        return random.choice(moves)
```

**Note**: In v3.1.0, the parameter format uses dict format (see existing players for examples).

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
- ✅ Main menu player selection
- ✅ Help screen with description
- ✅ Tournament system
- ✅ PlayerFactory API
- ✅ Show Opening system (if applicable)

**That's it!** The metadata-driven system handles everything else.

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

## Advanced: Creating Bitboard Players

### Example: Custom Bitboard Player

For maximum performance, use bitboard representation:

```python
from Players.Player import Player
from AI.BitboardMinimaxEngine import BitboardMinimaxEngine
from Reversi.BitboardGame import BitboardGame

class MyBitboardPlayer(Player):
    PLAYER_METADATA = {
        'display_name': 'MyBitboard AI',
        'description': 'Custom bitboard implementation - 50x faster',
        'enabled': True,
        'parameters': {
            'difficulty': {
                'type': int,
                'min': 1,
                'max': 12,  # Bitboard allows deeper search
                'default': 8,
                'description': 'Search depth (1-12)'
            }
        }
    }
    
    def __init__(self, deep=8):
        super().__init__()
        self.deep = deep
        self.name = f'MyBitboard{deep}'
        self.engine = BitboardMinimaxEngine()
    
    def get_move(self, game, moves, control):
        if not moves:
            return None
        
        # Convert to bitboard for speed
        bitboard = self._convert_to_bitboard(game)
        
        # Use ultra-fast bitboard search
        return self.engine.get_best_move(bitboard, self.deep, self.name)
    
    def _convert_to_bitboard(self, game):
        """Convert standard Game to BitboardGame"""
        bitboard = BitboardGame.create_empty()
        
        for y in range(1, 9):
            for x in range(1, 9):
                cell = game.matrix[y][x]
                bit = (y - 1) * 8 + (x - 1)
                
                if cell == 'B':
                    bitboard.black |= (1 << bit)
                elif cell == 'W':
                    bitboard.white |= (1 << bit)
        
        bitboard.turn = game.turn
        bitboard.turn_cnt = game.turn_cnt
        bitboard.history = game.history if hasattr(game, 'history') else ""
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)
        bitboard._create_virtual_matrix()
        
        return bitboard
```

### Example: Bitboard with Custom Opening Book

```python
from Players.AIPlayerBitboardBook import AIPlayerBitboardBook
from AI.OpeningBook import OpeningBook
import random

class MyBookPlayer(AIPlayerBitboardBook):
    def __init__(self, deep=6, custom_book_path=None):
        super().__init__(deep, show_book_options=False)
        
        # Load custom opening book if provided
        if custom_book_path:
            self.opening_book = OpeningBook(custom_book_path)
        
        self.name = f'CustomBook{deep}'
    
    def get_move(self, game, moves, control):
        # Your custom book selection logic here
        # Example: Add weighting to prefer certain openings
        book_moves = self.opening_book.get_book_moves(game.history)
        
        if book_moves:
            # Custom logic: could weight by opening popularity, etc.
            return random.choice(book_moves)
        
        # Fallback to parent implementation
        return super().get_move(game, moves, control)
```

### Key Points for Bitboard Players

1. **Performance**: 50-100x faster than standard
2. **Depth**: Can search deeper (10-12 vs 6-8)
3. **Conversion**: Must convert Game → BitboardGame
4. **Virtual Matrix**: Create for evaluator compatibility
5. **Validation**: Extensive test suite available (`test_bitboard_book.py`)

---

## Testing Your Player

### Unit Testing

```python
# Test programmatically first
from Players.PlayerFactory import PlayerFactory
from Reversi.Game import Game

# Create player
player = PlayerFactory.create_player('MyPlayer', deep=7)

# Test basic functionality
g = Game(8)
moves = g.get_move_list()
move = player.get_move(g, moves, None)
print(f"Selected: {move}")

# Verify move is valid
assert move in moves, "Invalid move returned!"
```

### Integration Testing

```bash
# Run comprehensive test suite
python test_bitboard_book.py

# Test tournament integration
cd tournament
python quick_tournament.py
```

### Performance Benchmarking

```bash
# Compare your player against others
python src/examples/bitboard_benchmark.py
```

---

## Real-World Examples

### Simple: Random Player
See: `src/Players/Monkey.py`

### Intermediate: Heuristic Player  
See: `src/Players/HeuristicPlayer.py`

### Advanced: Standard AI
See: `src/Players/AIPlayer.py`

### Expert: Bitboard with Opening Book
See: `src/Players/AIPlayerBitboardBook.py`

---

See `src/Players/CustomPlayerExample.py` for a complete working example.

