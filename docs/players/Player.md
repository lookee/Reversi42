# Player - Base Player Class

## Overview

The `Player` class is the base class for all player types in Reversi42. It defines the core interface that all players must implement and provides metadata support for automatic menu generation.

## Class Definition

```python
class Player(object):
    """Base class for all players."""
```

## Location
`src/Players/Player.py`

## Key Features

### 1. Player Metadata System
All player classes can define a `PLAYER_METADATA` dictionary for automatic menu generation:

```python
PLAYER_METADATA = {
    'display_name': 'Player',      # Name shown in menus
    'description': 'Description',   # Help text for users
    'enabled': False,               # Whether selectable in menu
    'parameters': []                # Configurable parameters
}
```

### 2. Core Interface

Every player must implement:

#### `__init__()`
Initialize the player with any required configuration.

#### `get_name()`
Returns the player's name as a string.

#### `get_move(game, move_list, control)`
The core method that returns the player's chosen move.

**Parameters:**
- `game`: Current game state (Game object)
- `move_list`: List of valid Move objects
- `control`: Board control interface (for GUI updates)

**Returns:**
- `Move` object representing the chosen move
- `None` if no move is possible (pass turn)

## Parameter Configuration

Players can define configurable parameters in their metadata:

```python
'parameters': [
    {
        'name': 'difficulty',
        'display_name': 'Difficulty Level',
        'type': 'int',
        'min': 1,
        'max': 10,
        'default': 6,
        'description': 'Search depth (higher = stronger but slower)'
    }
]
```

## Implementation Example

```python
from Players.Player import Player

class MyCustomPlayer(Player):
    PLAYER_METADATA = {
        'display_name': 'My Custom Player',
        'description': 'A custom player implementation',
        'enabled': True,
        'parameters': []
    }
    
    def __init__(self):
        self.name = 'CustomPlayer'
    
    def get_name(self):
        return self.name
    
    def get_move(self, game, move_list, control):
        # Implement your move selection logic here
        return move_list[0]  # Simple: return first available move
```

## Usage in Game

The Player class is instantiated by the PlayerFactory and used by the game loop:

1. Game requests available moves from the current game state
2. Game calls `player.get_move(game, moves, control)`
3. Player returns a Move object
4. Game validates and executes the move

## Design Philosophy

The Player base class follows these principles:

1. **Simplicity**: Minimal interface (just `get_move()`)
2. **Flexibility**: Subclasses can implement any strategy
3. **Metadata-driven**: Configuration without code changes
4. **GUI-agnostic**: Works with or without visual interface

## Subclasses

All player types in Reversi42 inherit from this base class:

- `HumanPlayer` - Interactive player
- `AIPlayer` - Minimax AI
- `Monkey` - Random player
- `GreedyPlayer` - Greedy strategy
- `HeuristicPlayer` - Heuristic evaluation
- `AIPlayerBitboard` - Bitboard-based AI
- `AIPlayerBook` - Opening book AI
- `AIPlayerBitboardBook` - Combined bitboard + book
- `AIPlayerBitboardBookParallel` - Parallel version
- `AIPlayerGrandmaster` - Ultimate AI
- `NetworkPlayer` - Network play placeholder

## See Also

- [Adding Custom Players](../ADDING_PLAYERS.md)
- [Human Player](HumanPlayer.md)
- [AI Player](AIPlayer.md)

