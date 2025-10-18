# Random Chaos (Monkey)

## Overview

The `Monkey` player is a simple random move generator that selects moves uniformly at random from the list of valid moves. It's useful for testing, debugging, and as a baseline opponent.

## Class Definition

```python
class Monkey(Player):
    """Random move generator - pure RNG for testing"""
```

## Location
`src/Players/Monkey.py`

## Key Features

### 1. Pure Randomness
- No strategy or evaluation
- Uniform random selection from valid moves
- Completely unpredictable gameplay

### 2. Instant Response
- No computation required
- O(1) move selection
- Perfect for rapid testing

### 3. Deterministic Seed Support
- Uses Python's `random` module
- Can be seeded for reproducible games

## How It Works

### Initialization

```python
def __init__(self):
    self.name = 'Monkey'
```

Simple initialization with fixed name.

### Move Selection

```python
def get_move(self, game, moves, control):
    move = moves[random.randint(0, len(moves)-1)]
    return move
```

**Algorithm:**
1. Get random index from 0 to len(moves)-1
2. Return move at that index

**Time Complexity:** O(1)

**Space Complexity:** O(1)

## Use Cases

### 1. Testing and Debugging

Perfect for testing game logic without AI complexity:

```python
# Test game flow with random players
black = Monkey()
white = Monkey()

# Games complete quickly
game.play(black, white)
```

### 2. Baseline Comparison

Measure AI performance against random play:

```python
# Tournament: AI vs Random
results = tournament.run(
    AIPlayer(depth=6),  # Your AI
    Monkey(),           # Random baseline
    num_games=100
)

# Win rate should be high (>90%) for good AI
```

### 3. Monte Carlo Simulations

Random playouts for evaluation:

```python
def evaluate_position(game):
    """Evaluate position with random playouts"""
    wins = 0
    for _ in range(1000):
        result = random_playout(game, Monkey(), Monkey())
        if result == current_player:
            wins += 1
    return wins / 1000
```

### 4. Learning and Education

Help beginners learn game rules without pressure:

```python
# Beginner's first opponent
human_player = HumanPlayer()
random_opponent = Monkey()
```

## Configuration

### Metadata

```python
PLAYER_METADATA = {
    'display_name': 'Random Chaos',
    'description': 'Random move generator - pure RNG for testing',
    'enabled': True,
    'parameters': []  # No configurable parameters
}
```

### No Parameters

The Monkey player has no configuration options - it's purely random.

## Example Usage

### Basic Usage

```python
from Players.Monkey import Monkey

# Create random player
monkey = Monkey()

# Get random move
move = monkey.get_move(game, valid_moves, control)
```

### Reproducible Games

```python
import random

# Set seed for reproducibility
random.seed(42)

# Games will be identical with same seed
game1 = play_game(Monkey(), Monkey())
random.seed(42)
game2 = play_game(Monkey(), Monkey())

# game1 and game2 will have identical move sequences
```

### Tournament Testing

```python
# Quick tournament for testing
results = []
for i in range(100):
    monkey1 = Monkey()
    monkey2 = Monkey()
    result = game.play(monkey1, monkey2)
    results.append(result)

# Should be roughly 50/50 (with first-move advantage)
```

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Speed** | Instant (< 1ms) |
| **Skill Level** | Very Weak |
| **Determinism** | Non-deterministic (unless seeded) |
| **Memory Usage** | Minimal |
| **CPU Usage** | Minimal |

## Statistical Properties

### Move Distribution

All valid moves have equal probability:
```
P(move_i) = 1 / n  (where n = number of valid moves)
```

### Expected Performance

Against perfect play:
- Win rate: ~0% (negligible)
- Loss rate: ~100%
- Average game length: ~45-55 moves

Against itself:
- Win rate: ~50% (with first-move advantage ~52-53%)
- High variance in game outcomes

### Randomness Quality

Uses Python's Mersenne Twister PRNG:
- Period: 2^19937 - 1
- Good statistical properties
- Sufficient for game purposes

## Limitations

1. **No Strategy**: Makes terrible moves regularly
2. **No Learning**: Never improves
3. **Unpredictable**: Can make brilliant or awful moves by chance
4. **Poor Teacher**: Doesn't demonstrate good play

## Comparison with Other Players

| Player | Strength vs Monkey | Typical Win Rate |
|--------|-------------------|------------------|
| GreedyPlayer | Much stronger | ~95% |
| HeuristicPlayer | Much stronger | ~98% |
| AIPlayer (depth 4) | Much stronger | ~100% |
| AIPlayer (depth 6) | Much stronger | ~100% |

## Implementation Notes

### Why Use `random.randint()`?

```python
# Current implementation
move = moves[random.randint(0, len(moves)-1)]

# Equivalent alternatives:
# move = random.choice(moves)  # More Pythonic
# move = moves[random.randrange(len(moves))]  # Equivalent
```

The current implementation works but could use `random.choice()` for clarity:

```python
def get_move(self, game, moves, control):
    return random.choice(moves)
```

## Advanced Usage

### Custom Random Strategy

```python
class WeightedMonkey(Monkey):
    """Monkey that prefers corners"""
    
    def get_move(self, game, moves, control):
        # Prefer corners if available
        corners = [(1,1), (1,8), (8,1), (8,8)]
        corner_moves = [m for m in moves 
                       if (m.x, m.y) in corners]
        
        if corner_moves:
            return random.choice(corner_moves)
        else:
            return random.choice(moves)
```

### Seeded Monkey for Testing

```python
class SeededMonkey(Monkey):
    """Monkey with reproducible behavior"""
    
    def __init__(self, seed=42):
        super().__init__()
        self.rng = random.Random(seed)
        self.name = f'Monkey{seed}'
    
    def get_move(self, game, moves, control):
        return self.rng.choice(moves)
```

## Debugging Tips

### Track Random Decisions

```python
class DebugMonkey(Monkey):
    """Monkey that logs its choices"""
    
    def __init__(self):
        super().__init__()
        self.moves_made = []
    
    def get_move(self, game, moves, control):
        move = random.choice(moves)
        self.moves_made.append({
            'turn': game.turn_cnt,
            'options': len(moves),
            'chosen': move
        })
        return move
```

## Fun Facts

1. **Name Origin**: "Monkey" suggests random/chaotic behavior (infinite monkeys theorem)
2. **First Player**: Often the first opponent in learning mode
3. **Surprisingly Tough**: Can occasionally beat weak players by luck
4. **Testing Favorite**: Most used player for automated testing

## See Also

- [Base Player Class](Player.md)
- [Greedy Player](GreedyPlayer.md) - Simple strategy (next step up)
- [Heuristic Player](HeuristicPlayer.md) - Positional strategy

