# Opening Scholar (AIPlayerBook)

## Overview

The `AIPlayerBook` combines opening book knowledge with minimax search. It consults a database of 57 professional opening sequences for instant, tournament-level early game play, then seamlessly transitions to standard minimax search when out of book.

## Class Definition

```python
class AIPlayerBook(Player):
    """AI Player that uses opening book for early game."""
```

## Location
`src/Players/AIPlayerBook.py`

## Key Features

### 1. Opening Book Integration
- 57 professional opening sequences
- Trie-based O(m) position lookup
- Instant responses in known positions
- Multiple variations supported

### 2. Intelligent Fallback
- Seamless transition to minimax when out of book
- No performance penalty at transition
- Tracks when leaving book for statistics

### 3. Random Selection
- Multiple book moves → random choice
- Adds unpredictability
- Explores different variations

### 4. Opening Information Display
- Shows current opening name
- Lists available continuations
- Educational feedback during play

## How It Works

### Two-Phase Strategy

```
Phase 1 (Opening Book):
    - Query opening book with game history
    - If position found in book:
        → Return random book move (instant)
    - Else: Switch to Phase 2

Phase 2 (Minimax Search):
    - Use standard alpha-beta search
    - Depth configurable (default 6)
    - Same as AIPlayer from this point
```

### Opening Book Lookup

```python
def get_move(self, game, moves, control):
    # Get game history string (e.g., "F5d6C3")
    game_history = game.history
    
    # Query opening book
    book_moves = opening_book.get_book_moves(game_history)
    
    # Filter to valid moves only
    valid_book_moves = [m for m in book_moves if m in moves]
    
    if valid_book_moves:
        # In book! Choose randomly among valid options
        move = random.choice(valid_book_moves)
        self.moves_from_book += 1
        return move
    else:
        # Out of book - use minimax engine
        move = self.engine.get_best_move(game, self.deep)
        self.moves_from_engine += 1
        return move
```

### Opening Book Structure

The opening book uses a Trie data structure:

```
Root
 ├─ F5 (first move)
 │   ├─ d6 (second move)
 │   │   ├─ C3 (Perpendicular Opening)
 │   │   ├─ C4 (Diagonal Opening)
 │   │   ├─ D3 (Diagonal Opening)
 │   │   └─ E6 (Tiger)
 │   └─ f4 (Parallel Opening)
 └─ (other first moves)
```

**Lookup Complexity**: O(m) where m = number of moves played

**Memory**: ~1-2 MB for 57 opening sequences

## Opening Book Database

### 57 Professional Openings

The book includes master-level openings:

**Popular Openings:**
- Perpendicular
- Diagonal
- Buffalo
- Tiger
- Rose
- Cow
- Heath
- And 50+ more variations

### Opening Format

```
Opening Name: Perpendicular
Move Sequence: F5d6C3d3C4f4F3

Variation: Perpendicular - Tiger
Move Sequence: F5d6C3d3C4f4F3f6E6e3D2
```

### Coverage

- **Moves 1-8**: High coverage (many book options)
- **Moves 9-15**: Moderate coverage (some positions)
- **Moves 16+**: Low coverage (out of book)

Typical book exit: Moves 8-12

## Configuration

### Metadata

```python
PLAYER_METADATA = {
    'display_name': 'Opening Scholar',
    'description': 'Opening book AI - 57 master sequences + minimax search',
    'enabled': True,
    'parameters': {
        'difficulty': {
            'type': int,
            'min': 1,
            'max': 10,
            'default': 6,
            'description': 'Search depth when out of book (higher = stronger but slower)'
        }
    }
}
```

### Initialization

```python
# Default: depth 6, show options
scholar = AIPlayerBook(deep=6, show_book_options=True)

# Quiet mode (no book info display)
quiet_scholar = AIPlayerBook(deep=6, show_book_options=False)

# Strong search when out of book
strong_scholar = AIPlayerBook(deep=8)
```

## Performance Characteristics

### Opening Phase (In Book)

| Metric | Value |
|--------|-------|
| **Response Time** | < 1ms (instant) |
| **Strength** | Master-level opening theory |
| **Positions Evaluated** | 0 (lookup only) |
| **Coverage** | Moves 1-12 typically |

### Search Phase (Out of Book)

Same as `AIPlayer` at configured depth:

| Depth | Time per Move | Strength |
|-------|---------------|----------|
| 4 | ~0.5s | Good |
| 6 | ~5-10s | Strong |
| 8 | ~2min | Very Strong |

## Strengths

### 1. Perfect Opening Play
- Master-level opening theory
- No computation wasted on known positions
- Instant early game responses

### 2. Multiple Variations
- 57 different opening sequences
- Random selection adds variety
- Explores different strategies

### 3. Smooth Transition
- Seamless switch to search
- No weakness at transition point
- Maintains strength throughout game

### 4. Educational Value
- Shows opening names
- Teaches opening theory
- Helps players learn

### 5. Time Efficiency
- Saves 5-10 moves of search time
- Focus computation on mid/late game
- Better time management in tournaments

## Weaknesses

### 1. Book Dependence
- Only as good as book quality
- Limited opening coverage
- May exit book in uncommon lines

### 2. Predictability
- Repeated games may show patterns
- Opponents can study book
- Limited opening variety

### 3. Static Opening Knowledge
- Doesn't learn new openings
- Can't adapt to opponent tendencies
- Fixed evaluation of positions

### 4. Same Search Weaknesses
- Inherits all `AIPlayer` limitations once out of book
- No speed advantage in search phase
- Same horizon effect

## Example Usage

### Basic Usage

```python
from Players.AIPlayerBook import AIPlayerBook

# Create opening book AI
scholar = AIPlayerBook(deep=6, show_book_options=True)

# Play game
move = scholar.get_move(game, valid_moves, control)
game.move(move)
```

### Tournament Setup

```python
# Opening book gives ~5% strength improvement
scholar6 = AIPlayerBook(deep=6)
standard6 = AIPlayer(deep=6)

# Scholar should win ~55% vs standard
results = tournament.run(scholar6, standard6, num_games=100)
```

### Study Opening Variations

```python
# Enable detailed output
scholar = AIPlayerBook(deep=6, show_book_options=True)

# Play multiple games to see different openings
for i in range(10):
    game = Game()
    # Scholar will choose different openings randomly
    result = play_game(scholar, opponent)
    print(f"Game {i}: {scholar.opening_used}")
```

### Custom Book

```python
# Load custom opening book
from AI.OpeningBook import OpeningBook

custom_book = OpeningBook()
custom_book.load_from_file('my_openings.txt')

scholar = AIPlayerBook(deep=6)
scholar.opening_book = custom_book
```

## Opening Book Display

When `show_book_options=True`:

```
================================================================================
📚 OPENING BOOK - Scholar6
================================================================================
Current Opening: Perpendicular
Available Openings (12): Perpendicular, Tiger, Rose, Buffalo, ...
  ... and 8 more
================================================================================
Available book moves (4):
  ⭐ 1. C3 → Perpendicular
     2. C4 → Diagonal
     3. D3 → Diagonal
     4. E6 → Tiger
--------------------------------------------------------------------------------
Selected: C3 (random choice from 4 options)
================================================================================
```

## Statistics

### Get Usage Statistics

```python
scholar = AIPlayerBook(deep=6)

# Play some games
play_multiple_games(scholar, opponent, num_games=10)

# Get statistics
stats = scholar.get_statistics()

print(stats)
# Output:
# {
#     'moves_from_book': 87,
#     'moves_from_engine': 213,
#     'book_percentage': 29.0,
#     'left_book_at_move': 9
# }
```

## Advanced Usage

### Early Exit Detection

```python
class EarlyExitScholar(AIPlayerBook):
    """Detect when exiting book earlier than expected"""
    
    def get_move(self, game, moves, control):
        move = super().get_move(game, moves, control)
        
        # Alert if exiting book very early
        if self.left_book_at_move and self.left_book_at_move < 6:
            print(f"⚠️  Early book exit at move {self.left_book_at_move}")
            print(f"   Opponent may be playing unusual opening")
        
        return move
```

### Prefer Specific Openings

```python
class FavoriteOpeningScholar(AIPlayerBook):
    """Prefer certain openings when available"""
    
    def __init__(self, deep=6, favorite_openings=None):
        super().__init__(deep)
        self.favorites = favorite_openings or ['Tiger', 'Rose']
    
    def get_move(self, game, moves, control):
        # Get book moves
        book_moves = self.opening_book.get_book_moves(game.history)
        valid_book_moves = [m for m in book_moves if m in moves]
        
        if valid_book_moves:
            # Check which lead to favorite openings
            for move in valid_book_moves:
                test_history = game.history + str(move).upper()
                opening_name = self.opening_book.get_current_opening_name(test_history)
                
                if opening_name in self.favorites:
                    print(f"📖 Choosing {move} → {opening_name} (favorite!)")
                    return move
            
            # No favorite found, random choice
            return random.choice(valid_book_moves)
        else:
            # Out of book
            return self.engine.get_best_move(game, self.deep)
```

## Win Rates (Approximate)

| Opponent | Scholar(6) Win Rate |
|----------|-------------------|
| Random Chaos | ~100% |
| Greedy Goblin | ~97% |
| Heuristic Scout | ~92% |
| AIPlayer(6) | ~55% |
| Scholar(6) mirror | ~52% |
| AIPlayer(8) | ~32% |
| Bitboard Blitz(8) | ~28% |
| The Oracle(8) | ~48% (both have book) |
| Grandmaster(9) | ~12% |

## Integration with OpeningBook

```python
from AI.OpeningBook import get_default_opening_book

# Load book
self.opening_book = get_default_opening_book()

# Get statistics
stats = self.opening_book.get_statistics()
# {
#     'lines_loaded': 57,
#     'total_positions': 1247,
#     'max_depth': 15
# }
```

See `src/AI/OpeningBook.py` for book implementation.

## See Also

- [Base Player Class](Player.md)
- [Alpha-Beta AI](AIPlayer.md) - Without opening book
- [The Oracle](AIPlayerBitboardBook.md) - Bitboard + book
- [Opening Book Documentation](../OPENING_BOOK.md)
- [Opening Book Demo](../../src/examples/opening_book_demo.py)

