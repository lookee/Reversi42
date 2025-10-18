# Heuristic Scout (HeuristicPlayer)

## Overview

The `HeuristicPlayer` uses intelligent heuristic evaluation to select moves without performing deep minimax search. It evaluates positions based on corner control, edge stability, mobility, and positional weights, making it faster than full AI while still playing strategically sound Reversi.

## Class Definition

```python
class HeuristicPlayer(Player):
    """Heuristic player that uses simple heuristics 
    without full minimax search."""
```

## Location
`src/Players/HeuristicPlayer.py`

## Key Features

### 1. Positional Evaluation
- Corner priority (highest value)
- Edge management
- Position-based scoring matrix
- Avoids dangerous squares (X-squares)

### 2. Mobility Analysis
- Counts available moves after placement
- Prefers moves that maintain/increase options
- Reduces opponent mobility

### 3. Fast Execution
- No deep search (depth 1)
- Single-ply evaluation
- Suitable for quick games

### 4. Strategic Without Search
- Captures Reversi principles in heuristics
- Good play without computational expense
- Educational demonstration of evaluation functions

## How It Works

### Strategy

The heuristic strategy combines multiple factors:

1. **Positional Value**: Each square has inherent value
2. **Corner Control**: Corners are extremely valuable (stable)
3. **Edge Strategy**: Edges are valuable if not adjacent to corners
4. **Mobility**: Number of moves available
5. **Piece Count**: Secondary consideration

### HeuristicEngine

Uses the `HeuristicEngine` which evaluates based on:

```python
# Evaluation components (typical weights)
score = (
    100 * corner_value +
    50 * edge_value +
    10 * mobility +
    1 * piece_count
)
```

### Position Weights Matrix

Standard positional matrix (approximate):

```
    A    B    C   D   E   F    G    H
1  100  -20   10   5   5  10  -20  100
2  -20  -50   -2  -2  -2  -2  -50  -20
3   10   -2    5   1   1   5   -2   10
4    5   -2    1   0   0   1   -2    5
5    5   -2    1   0   0   1   -2    5
6   10   -2    5   1   1   5   -2   10
7  -20  -50   -2  -2  -2  -2  -50  -20
8  100  -20   10   5   5  10  -20  100

Key:
100 = Corners (stable, never flipped)
-50 = X-squares (give opponent corner access)
-20 = C-squares (adjacent to corners)
 10 = Edges (relatively stable)
  0 = Center (neutral)
```

### Move Selection Process

```python
def get_move(self, game, moves, control):
    # Use HeuristicEngine for evaluation
    # Depth parameter is ignored (always 1-ply)
    move = self.engine.get_best_move(game, depth=1, player_name=self.name)
    return move
```

The engine:
1. Evaluates each valid move
2. Applies heuristic scoring
3. Returns move with highest score

## Strategic Principles

### 1. Corner Priority

Corners are **golden** in Reversi:
- Cannot be flipped once captured
- Provide stable anchor for edge building
- Control significant board area

Heuristic heavily prioritizes corner moves.

### 2. X-Square Avoidance

X-squares (B2, B7, G2, G7) are **dangerous**:
- Give opponent access to adjacent corner
- Should be avoided unless:
  - Corner already secured
  - No better alternative
  - Endgame situation

### 3. Edge Building

Edges (rows 1 and 8, columns A and H):
- Second most valuable positions
- Relatively stable
- Can create chains leading to corners

### 4. Mobility Preference

More moves = More control:
- Prefer moves that preserve options
- Avoid moves that restrict future plays
- Force opponent into fewer options

### 5. Piece Count (Secondary)

Unlike greedy, piece count is **least important**:
- Early/mid game: Fewer pieces often better
- Late game: Piece count becomes more relevant
- Heuristic balances this appropriately

## Strengths

### 1. Strategic Play
- Respects Reversi fundamentals
- Corner-focused strategy
- Mobility awareness

### 2. Fast Execution
- No deep search required
- Instant move selection
- Suitable for real-time play

### 3. Good Teaching Tool
- Demonstrates evaluation functions
- Shows importance of position
- Bridges gap between greedy and minimax

### 4. Consistent Performance
- Deterministic behavior
- Reliable strength level
- Good for intermediate players

## Weaknesses

### 1. No Lookahead

Single-ply evaluation misses:
- Multi-move combinations
- Opponent's counter-moves
- Deep tactical sequences

### 2. Static Evaluation

Heuristics don't adapt:
- Same weights for all game phases
- Doesn't learn from experience
- May miss game-specific patterns

### 3. Tactical Blindness

Can fall into traps:
- Complex tactical sequences
- Forced move combinations
- Endgame precision

### 4. Beaten by Deep Search

Minimax AI with depth ≥4 typically wins:
- Lookahead beats heuristics
- Tactical combinations found
- Better endgame play

## Configuration

### Metadata

```python
PLAYER_METADATA = {
    'display_name': 'Heuristic Scout',
    'description': 'Fast heuristic AI - positional evaluation without deep search',
    'enabled': True,
    'parameters': []  # No configurable parameters
}
```

### Customization

```python
# Create heuristic player with custom name
heuristic = HeuristicPlayer(name='Scout')
```

## Example Usage

### Basic Usage

```python
from Players.HeuristicPlayer import HeuristicPlayer

# Create heuristic player
scout = HeuristicPlayer(name='Scout')

# In game loop
move = scout.get_move(game, valid_moves, control)
game.move(move)
```

### As Teaching Opponent

```python
# Good opponent for learning
human = HumanPlayer()
scout = HeuristicPlayer()

print("Play against Heuristic Scout to learn:")
print("- Corner importance")
print("- Edge building")
print("- X-square dangers")

game.play(human, scout)
```

### Baseline for AI Development

```python
# Compare your AI against heuristic baseline
my_ai = AIPlayer(deep=4)
scout = HeuristicPlayer()

results = tournament.run(my_ai, scout, num_games=50)

# Good AI at depth 4 should win 70-80%
# At depth 6: 85-95%
```

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Speed** | Very Fast (~2-5ms per move) |
| **Skill Level** | Moderate |
| **Determinism** | Deterministic |
| **Depth** | 1 (single-ply) |
| **Best Use** | Fast games, learning, baseline |

## Win Rates (Approximate)

| Opponent | Heuristic Win Rate |
|----------|-------------------|
| Random Chaos | ~98% |
| Greedy Goblin | ~85% |
| Heuristic (mirror) | ~52% (first player advantage) |
| Alpha-Beta (depth 3) | ~40% |
| Alpha-Beta (depth 4) | ~25% |
| Alpha-Beta (depth 6) | ~10% |
| Bitboard Blitz (depth 8) | ~3% |
| Grandmaster | ~0% |

## Advanced Usage

### Custom Heuristic Weights

```python
class CustomHeuristic(HeuristicPlayer):
    """Heuristic with custom evaluation weights"""
    
    def __init__(self, name='CustomHeuristic'):
        super().__init__(name)
        # Could modify engine weights here
        self.engine.corner_weight = 150  # Increase corner priority
        self.engine.mobility_weight = 15  # Increase mobility value
```

### Verbose Evaluation

```python
class VerboseHeuristic(HeuristicPlayer):
    """Shows evaluation reasoning"""
    
    def get_move(self, game, moves, control):
        print(f"\n{'='*60}")
        print(f"HEURISTIC EVALUATION - Turn {game.turn_cnt}")
        print(f"{'='*60}")
        
        for move in moves:
            score = self.engine.evaluate_move(game, move)
            print(f"{move}: Score = {score}")
            
            # Show breakdown
            if is_corner(move):
                print(f"  -> Corner! (+100)")
            elif is_x_square(move):
                print(f"  -> X-square! (-50)")
            elif is_edge(move):
                print(f"  -> Edge (+10)")
        
        move = super().get_move(game, moves, control)
        print(f"\nChosen: {move}")
        print(f"{'='*60}\n")
        
        return move
```

### Hybrid Player

```python
class HybridPlayer(HeuristicPlayer):
    """Use heuristic early, minimax late"""
    
    def __init__(self, switch_turn=30):
        super().__init__()
        self.switch_turn = switch_turn
        self.minimax_engine = MinimaxEngine()
    
    def get_move(self, game, moves, control):
        if game.turn_cnt < self.switch_turn:
            # Early game: fast heuristic
            return self.engine.get_best_move(game, 1, self.name)
        else:
            # Late game: deep search
            return self.minimax_engine.get_best_move(game, 8, self.name)
```

## Debugging

### Evaluation Tracer

```python
# Track heuristic decisions
tracer = HeuristicEvaluationTracer()

scout = HeuristicPlayer()
scout.engine.set_tracer(tracer)

game.play(scout, opponent)

# Analyze decisions
tracer.show_statistics()
tracer.show_mistakes()  # Where heuristic failed
```

## Integration with HeuristicEngine

The HeuristicPlayer delegates to `HeuristicEngine`:

```python
from AI.HeuristicEngine import HeuristicEngine

# Engine handles the actual evaluation
self.engine = HeuristicEngine()

# Get best move using heuristics
move = self.engine.get_best_move(game, depth=1, player_name=self.name)
```

See `src/AI/HeuristicEngine.py` for evaluation details.

## Educational Value

### Learning Points

1. **Evaluation Functions**: Shows how to score positions
2. **Strategic Principles**: Demonstrates Reversi strategy
3. **Speed vs Depth**: Tradeoff between fast heuristic and slow search
4. **Position Over Pieces**: Values position more than piece count

### Progression Path

```
Random → Greedy → Heuristic → Minimax → Advanced AI
  ↓        ↓         ↓           ↓            ↓
No      Piece   Position +   Lookahead +  All Advanced
Strategy Count  Mobility     Tactics      Optimizations
```

## See Also

- [Base Player Class](Player.md)
- [Greedy Goblin](GreedyPlayer.md) - Simpler strategy
- [Alpha-Beta AI](AIPlayer.md) - Full search
- [Heuristic Engine Documentation](../AI_ENGINES.md)

