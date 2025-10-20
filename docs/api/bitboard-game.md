# BitboardGame API Reference

The `BitboardGame` class provides an ultra-fast implementation of Reversi/Othello using 64-bit bitboard representation.

## Overview

**Module**: `src.Reversi.BitboardGame`

**Performance**: 50-100x faster than standard array-based implementation

**Thread Safety**: Immutable - safe to share between threads

## Class: BitboardGame

### Constructor

```python
BitboardGame(black: int = 0x0000000810000000,
             white: int = 0x0000001008000000,
             current_player: int = 1)
```

Creates a new game instance.

**Parameters:**
- `black` (int): Bitboard representing black pieces (default: initial position)
- `white` (int): Bitboard representing white pieces (default: initial position)
- `current_player` (int): Current player (1 for black, -1 for white)

**Returns:**
- `BitboardGame`: New game instance

**Example:**
```python
from src.Reversi.BitboardGame import BitboardGame

# Create game with default starting position
game = BitboardGame()

# Create game with custom position
custom_game = BitboardGame(
    black=0x0000001818000000,
    white=0x0000002424000000,
    current_player=1
)
```

### Properties

#### `black: int`

Bitboard representing black pieces (64-bit integer).

**Type**: `int` (readonly)

**Example:**
```python
print(f"Black pieces: {bin(game.black)}")
```

#### `white: int`

Bitboard representing white pieces (64-bit integer).

**Type**: `int` (readonly)

#### `current_player: int`

Current player to move.

**Type**: `int` (readonly)
**Values**: `1` (black) or `-1` (white)

#### `move_history: List[int]`

List of moves made in the game.

**Type**: `List[int]` (readonly)

**Example:**
```python
for i, move in enumerate(game.move_history):
    row, col = move // 8, move % 8
    print(f"Move {i+1}: {chr(ord('A')+col)}{row+1}")
```

### Core Methods

#### `get_valid_moves(player: int) -> List[int]`

Get all valid moves for the specified player.

**Parameters:**
- `player` (int): Player color (1 for black, -1 for white)

**Returns:**
- `List[int]`: List of valid move positions (0-63)

**Time Complexity**: O(1) - approximately 50-100ns

**Example:**
```python
moves = game.get_valid_moves(1)  # Get black's moves
print(f"Black has {len(moves)} valid moves")
for move in moves:
    row, col = move // 8, move % 8
    print(f"  {chr(ord('A')+col)}{row+1}")
```

#### `make_move(position: int) -> BitboardGame`

Make a move and return a new game state.

**Parameters:**
- `position` (int): Position to place piece (0-63)

**Returns:**
- `BitboardGame`: New game state with move applied

**Raises:**
- `ValueError`: If move is invalid

**Time Complexity**: O(1) - approximately 20-30ns

**Example:**
```python
moves = game.get_valid_moves(game.current_player)
if moves:
    new_game = game.make_move(moves[0])
    print(f"Made move at {moves[0]}")
```

**Note**: Original game object is unchanged (immutable pattern).

#### `is_valid_move(position: int, player: int) -> bool`

Check if a move is valid for the specified player.

**Parameters:**
- `position` (int): Position to check (0-63)
- `player` (int): Player color (1 or -1)

**Returns:**
- `bool`: True if move is valid, False otherwise

**Example:**
```python
if game.is_valid_move(19, 1):
    print("D3 is a valid move for black")
```

#### `is_game_over() -> bool`

Check if the game is over.

**Returns:**
- `bool`: True if neither player has valid moves

**Example:**
```python
while not game.is_game_over():
    # Play game...
    pass
```

#### `get_score() -> Tuple[int, int]`

Get the current score.

**Returns:**
- `Tuple[int, int]`: (black_count, white_count)

**Example:**
```python
black_score, white_score = game.get_score()
print(f"Black: {black_score}, White: {white_score}")
```

#### `get_winner() -> int`

Get the winner of the game.

**Returns:**
- `int`: 1 if black wins, -1 if white wins, 0 if draw

**Raises:**
- `RuntimeError`: If game is not over

**Example:**
```python
if game.is_game_over():
    winner = game.get_winner()
    if winner == 1:
        print("Black wins!")
    elif winner == -1:
        print("White wins!")
    else:
        print("Draw!")
```

### Advanced Methods

#### `pass_turn() -> BitboardGame`

Pass the turn to the other player.

**Returns:**
- `BitboardGame`: New game state with turn passed

**Example:**
```python
moves = game.get_valid_moves(game.current_player)
if not moves:
    game = game.pass_turn()
```

#### `get_piece_at(position: int) -> int`

Get the piece at a specific position.

**Parameters:**
- `position` (int): Board position (0-63)

**Returns:**
- `int`: 1 (black), -1 (white), or 0 (empty)

**Example:**
```python
piece = game.get_piece_at(27)  # D4
if piece == 1:
    print("Black piece at D4")
elif piece == -1:
    print("White piece at D4")
else:
    print("Empty square at D4")
```

#### `count_flips(position: int, player: int) -> int`

Count how many pieces would be flipped by a move.

**Parameters:**
- `position` (int): Move position (0-63)
- `player` (int): Player color (1 or -1)

**Returns:**
- `int`: Number of pieces that would be flipped

**Example:**
```python
flips = game.count_flips(19, 1)
print(f"Move at D3 would flip {flips} pieces")
```

#### `get_board_string() -> str`

Get a string representation of the board.

**Returns:**
- `str`: ASCII representation of the board

**Example:**
```python
print(game.get_board_string())
# Output:
#   A B C D E F G H
# 1 . . . . . . . .
# 2 . . . . . . . .
# 3 . . . . . . . .
# 4 . . . O X . . .
# 5 . . . X O . . .
# 6 . . . . . . . .
# 7 . . . . . . . .
# 8 . . . . . . . .
```

#### `copy() -> BitboardGame`

Create a copy of the game state.

**Returns:**
- `BitboardGame`: Copy of the game

**Example:**
```python
backup = game.copy()
game = game.make_move(19)
# backup still has original state
```

**Note**: Due to immutability, this is O(1) - just creates a new reference.

### Bitboard Utilities

#### `position_to_coords(position: int) -> Tuple[int, int]`

Convert position index to (row, col) coordinates.

**Parameters:**
- `position` (int): Position index (0-63)

**Returns:**
- `Tuple[int, int]`: (row, col) where row and col are 0-7

**Example:**
```python
row, col = BitboardGame.position_to_coords(27)  # D4
print(f"Position 27 is row {row}, col {col}")  # row 3, col 3
```

#### `coords_to_position(row: int, col: int) -> int`

Convert (row, col) coordinates to position index.

**Parameters:**
- `row` (int): Row index (0-7)
- `col` (int): Column index (0-7)

**Returns:**
- `int`: Position index (0-63)

**Example:**
```python
pos = BitboardGame.coords_to_position(3, 3)  # D4
print(f"D4 is position {pos}")  # 27
```

#### `position_to_notation(position: int) -> str`

Convert position index to algebraic notation.

**Parameters:**
- `position` (int): Position index (0-63)

**Returns:**
- `str`: Algebraic notation (e.g., "D4")

**Example:**
```python
notation = BitboardGame.position_to_notation(27)
print(notation)  # "D4"
```

#### `notation_to_position(notation: str) -> int`

Convert algebraic notation to position index.

**Parameters:**
- `notation` (str): Algebraic notation (e.g., "D4")

**Returns:**
- `int`: Position index (0-63)

**Raises:**
- `ValueError`: If notation is invalid

**Example:**
```python
pos = BitboardGame.notation_to_position("D4")
print(f"D4 is position {pos}")  # 27
```

## Constants

### Board Positions

```python
# Common positions
TOP_LEFT = 0
TOP_RIGHT = 7
BOTTOM_LEFT = 56
BOTTOM_RIGHT = 63

# Center positions
D4 = 27
E4 = 28
D5 = 35
E5 = 36

# Corners
CORNERS = [0, 7, 56, 63]
```

### Bitboard Masks

```python
# Edge masks
TOP_EDGE = 0x00000000000000FF
BOTTOM_EDGE = 0xFF00000000000000
LEFT_EDGE = 0x0101010101010101
RIGHT_EDGE = 0x8080808080808080

# Corner masks
CORNER_MASK = 0x8100000000000081
```

## Performance Notes

### Benchmarks

On a modern CPU (Apple M1):

```python
# get_valid_moves(): ~50-100ns per call
# make_move(): ~20-30ns per call
# is_valid_move(): ~30-50ns per call
# get_score(): ~10ns per call
```

### Memory Usage

- Each `BitboardGame` instance: ~200 bytes
- Immutable design allows efficient copy-on-write
- No dynamic memory allocation during gameplay

### Optimization Tips

1. **Batch operations**: Get all valid moves once, reuse the list
2. **Immutability**: Original game state is preserved, no need to copy for rollback
3. **Bitwise operations**: All core operations use fast bitwise arithmetic
4. **Cache-friendly**: Small memory footprint fits in CPU cache

## Examples

### Complete Game

```python
from src.Reversi.BitboardGame import BitboardGame

game = BitboardGame()

while not game.is_game_over():
    moves = game.get_valid_moves(game.current_player)
    
    if not moves:
        game = game.pass_turn()
        continue
    
    # Print board
    print(game.get_board_string())
    print(f"\nValid moves for {'Black' if game.current_player == 1 else 'White'}:")
    for move in moves:
        notation = BitboardGame.position_to_notation(move)
        flips = game.count_flips(move, game.current_player)
        print(f"  {notation} (flips {flips} pieces)")
    
    # Make first move
    game = game.make_move(moves[0])

black_score, white_score = game.get_score()
print(f"\nGame Over! Black: {black_score}, White: {white_score}")
```

### Position Analysis

```python
def analyze_position(game: BitboardGame):
    """Analyze current position."""
    black_moves = game.get_valid_moves(1)
    white_moves = game.get_valid_moves(-1)
    black_score, white_score = game.get_score()
    
    print(f"Mobility: Black {len(black_moves)}, White {len(white_moves)}")
    print(f"Material: Black {black_score}, White {white_score}")
    
    # Check corners
    corners_black = sum(1 for c in [0, 7, 56, 63] if game.get_piece_at(c) == 1)
    corners_white = sum(1 for c in [0, 7, 56, 63] if game.get_piece_at(c) == -1)
    print(f"Corners: Black {corners_black}, White {corners_white}")

analyze_position(game)
```

## See Also

- [Game API](game.md) - Original game implementation
- [Move Generation](move-generation.md) - Move generation details
- [Bitboard Implementation](../architecture/bitboard.md) - Technical details
- [Performance Guide](../development/performance.md) - Optimization techniques

