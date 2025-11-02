# API Reference

Complete API documentation for Reversi42.

## Overview

This directory contains detailed API documentation for all major components of Reversi42. The API is organized by module and provides comprehensive information about classes, methods, and their usage.

## Quick Navigation

### Core Game Engine
- [**BitboardGame**](bitboard-game.md) - Ultra-fast bitboard game implementation
- [**Game**](game.md) - Original game implementation
- [**Move Generation**](move-generation.md) - Move validation and generation

### AI System
- [**Apocalyptron Engine**](apocalyptron-engine.md) - Ultimate AI with all optimizations
- [**Search Algorithms**](search-algorithms.md) - Alpha-beta, iterative deepening, parallel search
- [**Evaluation Functions**](evaluation-functions.md) - Position evaluation heuristics
- [**Opening Book**](opening-book.md) - Opening theory database
- [**Transposition Tables**](transposition-tables.md) - Position caching system

### Players
- [**Player Interface**](player-interface.md) - Base player class and protocol
- [**Human Player**](human-player.md) - Interactive human player
- [**AI Players**](ai-players.md) - All AI player implementations

### UI System
- [**View Interface**](view-interface.md) - Abstract view protocol
- [**Pygame View**](pygame-view.md) - Graphical user interface
- [**Terminal View**](terminal-view.md) - ASCII art interface
- [**Headless View**](headless-view.md) - No-UI interface
- [**Widgets**](widgets.md) - Reusable UI components

### Utilities
- [**Configuration**](configuration.md) - Game configuration system
- [**Game I/O**](game-io.md) - Save/load functionality
- [**Event System**](event-system.md) - Event bus and pub/sub

## API Conventions

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `BitboardGame`)
- **Functions/Methods**: `snake_case` (e.g., `get_valid_moves`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_DEPTH`)
- **Private Members**: Prefix with `_` (e.g., `_internal_state`)

### Type Hints

All public APIs use Python type hints:

```python
def get_valid_moves(self, player: int) -> List[int]:
    """Get valid moves for the specified player."""
    pass
```

### Docstring Format

We use Google-style docstrings:

```python
def evaluate_position(game: BitboardGame, depth: int) -> float:
    """
    Evaluate the current position.
    
    Args:
        game: Current game state
        depth: Remaining search depth
        
    Returns:
        Evaluation score from black's perspective
        
    Raises:
        ValueError: If depth is negative
    """
    pass
```

### Error Handling

The API uses standard Python exceptions:

- `ValueError`: Invalid argument values
- `TypeError`: Wrong argument types
- `RuntimeError`: Runtime errors (e.g., invalid game state)
- `FileNotFoundError`: File operations
- `KeyError`: Missing dictionary keys

### Return Values

- **Success**: Return the expected value
- **Not Found**: Return `None` or empty collection
- **Error**: Raise appropriate exception

## Common Patterns

### Creating a Game

```python
from src.Reversi.BitboardGame import BitboardGame

# Create a new game
game = BitboardGame()

# Check initial state
assert game.current_player == 1  # Black starts
assert len(game.get_valid_moves(1)) == 4
```

### Making Moves

```python
# Get valid moves
moves = game.get_valid_moves(game.current_player)

# Make a move (returns new game state)
new_game = game.make_move(moves[0])

# Original game is unchanged (immutable pattern)
assert game.current_player == 1
assert new_game.current_player == -1
```

### Using AI

```python
from src.Players.PlayerApocalyptron import PlayerApocalyptron
from src.AI.Apocalyptron.factory.factory import ApocalyptronFactory

# Create AI player
config = ApocalyptronFactory.create_default_config(depth=9)
player = PlayerApocalyptron(config=config)

# Get AI move
move = player.get_move(game, moves, control=None)
```

### Loading Opening Book

```python
from src.domain.knowledge.opening_book import OpeningBook

# Load opening book
book = OpeningBook()
book.load_from_file('src/domain/knowledge/data/00_opening_ffo.txt')

# Query opening
result = book.get_opening_move(game)
if result:
    move, opening_name = result
    print(f"Opening: {opening_name}, Move: {move}")
```

## API Stability

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking changes
- **Minor** (x.Y.0): New features, backward compatible
- **Patch** (x.y.Z): Bug fixes, backward compatible

### Deprecation Policy

1. Features are marked deprecated in a minor release
2. Deprecated features remain functional for at least one major version
3. Breaking changes are documented in CHANGELOG.md
4. Migration guides are provided for breaking changes

### API Stability Levels

- **Stable**: Production-ready, won't change without major version bump
- **Beta**: Feature-complete, may have minor changes
- **Alpha**: Experimental, may change significantly
- **Internal**: Not part of public API, may change at any time

Current stability:

- Core Game Engine: **Stable**
- Apocalyptron AI: **Stable**
- UI System: **Stable**
- Tournament System: **Beta**
- Network Play: **Not yet implemented**

## Examples

### Complete Game Example

```python
from src.Reversi.BitboardGame import BitboardGame

# Create game
game = BitboardGame()

# Game loop
while not game.is_game_over():
    moves = game.get_valid_moves(game.current_player)
    
    if not moves:
        # No valid moves, pass turn
        game = game.pass_turn()
        continue
    
    # Make first valid move
    game = game.make_move(moves[0])

# Get final score
black_score, white_score = game.get_score()
print(f"Black: {black_score}, White: {white_score}")
```

### AI vs AI Example

```python
from src.Reversi.BitboardGame import BitboardGame
from src.Players.PlayerApocalyptron import PlayerApocalyptron
from src.AI.Apocalyptron.factory.factory import ApocalyptronFactory

# Create players
config1 = ApocalyptronFactory.create_default_config(depth=8)
config2 = ApocalyptronFactory.create_default_config(depth=9)
player1 = PlayerApocalyptron(config=config1)
player2 = PlayerApocalyptron(config=config2)

# Play game
game = BitboardGame()
while not game.is_game_over():
    moves = game.get_valid_moves(game.current_player)
    if not moves:
        game = game.pass_turn()
        continue
    
    # Select player
    player = player1 if game.current_player == 1 else player2
    move = player.get_move(game, moves, None)
    game = game.make_move(move)

print(f"Final score: {game.get_score()}")
```

## Performance Considerations

### Bitboard Operations

Bitboard operations are O(1) but with varying constant factors:

- `get_valid_moves()`: ~50-100ns per call
- `make_move()`: ~20-30ns per call
- `evaluate_position()`: ~1-10µs depending on depth

### Memory Usage

- `BitboardGame`: ~200 bytes per instance
- Transposition Table: Configurable, default 128MB
- Opening Book: ~2MB loaded in memory

### Threading

- Game state is **immutable** - safe to share between threads
- AI search uses **multiprocessing** for parallelism
- UI updates must be on **main thread** (Pygame requirement)

## API Reference by Module

See individual files for detailed documentation:

1. [BitboardGame API](bitboard-game.md) - Core game engine
2. [Apocalyptron API](apocalyptron-engine.md) - AI engine
3. [Player API](player-interface.md) - Player system
4. [View API](view-interface.md) - UI system
5. [Utilities API](utilities.md) - Helper functions

## Contributing to API Documentation

When adding new APIs:

1. Add comprehensive docstrings with Google-style format
2. Include type hints for all parameters and return values
3. Provide usage examples in docstrings
4. Document exceptions that may be raised
5. Add API reference documentation file in this directory
6. Update this README with links to new documentation

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for more details.

---

**Note**: This documentation is for version 5.0.0. For other versions, see the corresponding branch or tag.

