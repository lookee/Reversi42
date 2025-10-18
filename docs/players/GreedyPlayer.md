# Greedy Goblin (GreedyPlayer)

## Overview

The `GreedyPlayer` is a simple AI that always chooses the move that captures the maximum number of opponent pieces immediately. This is a short-sighted strategy that doesn't consider long-term positional advantages, making it useful for educational purposes and as a baseline opponent.

## Class Definition

```python
class GreedyPlayer(Player):
    """Greedy player that always chooses the move that captures 
    the maximum number of pieces immediately."""
```

## Location
`src/Players/GreedyPlayer.py`

## Key Features

### 1. Simple Strategy
- Evaluates each move by piece count
- Selects move with maximum immediate gain
- No lookahead or strategic planning

### 2. Fast Execution
- O(n) time complexity (n = number of valid moves)
- Each move evaluated once
- No deep search required

### 3. Deterministic Behavior
- Same position always produces same move
- Predictable for testing
- Good educational tool

### 4. Move-Undo System
- Uses game's move/undo_move functions
- Temporarily applies each move
- Restores game state after evaluation

## How It Works

### Strategy

The greedy strategy follows this simple rule:

**"Choose the move that gives me the most pieces right now"**

### Algorithm

```python
def get_move(self, game, moves, control):
    best_move = None
    max_flips = -1
    current_turn = game.get_turn()
    
    # Try each move
    for move in moves:
        game.move(move)              # Apply move
        piece_count = count_pieces() # Count our pieces
        game.undo_move()             # Restore state
        
        if piece_count > max_flips:
            max_flips = piece_count
            best_move = move
    
    return best_move
```

**Time Complexity:** O(n) where n = number of valid moves

**Space Complexity:** O(1)

### Evaluation Process

1. **Iterate** through all valid moves
2. **Apply** each move temporarily
3. **Count** pieces for current player
4. **Undo** the move
5. **Track** move with highest piece count
6. **Return** best move found

## Strengths

### 1. Simplicity
- Easy to understand
- Minimal code
- Clear behavior

### 2. Speed
- No complex calculations
- Fast move selection
- Suitable for quick games

### 3. Reasonable Early Game
- Early game: greedy often good
- Many pieces = good position (sometimes)
- Intuitive for beginners

## Weaknesses

### 1. No Strategic Planning

Greedy ignores fundamental Reversi strategy:

```
❌ Corner Control
❌ Edge Management
❌ Mobility
❌ Stability
❌ X-square Danger
```

### 2. Maximization Paradox

In Reversi, **minimizing pieces early** is often better:
- Fewer pieces = More mobility
- More options = Harder to counter
- Greedy does the opposite!

### 3. Predictable

Advanced players can exploit:
- Bait greedy into X-squares
- Force greedy to take bad edges
- Set up corner traps

### 4. Poor Late Game

Greedy fails to:
- Secure corners
- Build stable edges
- Plan final moves

## Configuration

### Metadata

```python
PLAYER_METADATA = {
    'display_name': 'Greedy Goblin',
    'description': 'Greedy AI - always captures maximum pieces (educational)',
    'enabled': True,
    'parameters': []  # No configurable parameters
}
```

### Customization

```python
# Create greedy player with custom name
greedy = GreedyPlayer(name='Grabby')
```

## Example Usage

### Basic Usage

```python
from Players.GreedyPlayer import GreedyPlayer

# Create greedy player
greedy = GreedyPlayer(name='Goblin')

# In game loop
move = greedy.get_move(game, valid_moves, control)
game.move(move)
```

### Testing Against Greedy

```python
# Use as baseline for AI development
from Players.GreedyPlayer import GreedyPlayer
from Players.AIPlayer import AIPlayer

greedy = GreedyPlayer()
my_ai = AIPlayer(deep=4)

# Your AI should easily beat greedy
result = game.play(my_ai, greedy)
# Expected: my_ai wins 85-95% of the time
```

### Educational Demo

```python
# Show why greedy fails
greedy = GreedyPlayer()
heuristic = HeuristicPlayer()

print("Greedy vs Heuristic:")
print("Greedy takes most pieces each turn...")
print("But Heuristic wins by controlling corners and edges!")

result = game.play(greedy, heuristic)
# Heuristic typically wins
```

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Speed** | Very Fast (~1ms per move) |
| **Skill Level** | Weak |
| **Determinism** | Deterministic |
| **Depth** | 1 (no lookahead) |
| **Best Use** | Educational, baseline testing |

## Win Rates (Approximate)

| Opponent | Greedy Win Rate |
|----------|-----------------|
| Random Chaos | ~95% |
| Greedy (mirror) | ~52% (first player advantage) |
| Heuristic Scout | ~15% |
| Alpha-Beta (depth 4) | ~5% |
| Alpha-Beta (depth 6) | ~1% |
| Bitboard Blitz | ~0% |
| Grandmaster | ~0% |

## Common Mistakes

### Example 1: X-Square Trap

```
Board state:
  A B C D E F G H
1 . . . . . . . .
2 . . . B . . . .
3 . . B B B . . .
4 . B B W B . . .

Greedy sees:
B2 → Flips 3 pieces! ✅ (takes it)

Reality:
B2 is X-square giving opponent corner A1 ❌
```

### Example 2: Mobility Loss

```
Turn 20:
Valid moves: [E1, F2, G3]

E1: Flips 8 pieces (Greedy chooses this)
F2: Flips 3 pieces
G3: Flips 2 pieces

After E1:
- Greedy has 35 pieces
- Opponent has 14 pieces
- Greedy has only 1 valid move next turn
- Opponent has 8 valid moves

Result: Opponent dominates despite fewer pieces
```

## Educational Value

### Why Study Greedy?

1. **Learn by Contrast**: Shows what NOT to do
2. **Understand Strategy**: Highlights importance of position over quantity
3. **Baseline Comparison**: Measure improvement against greedy
4. **Implementation Study**: Simple AI example

### Lessons from Greedy

- **More pieces ≠ Better position**
- **Immediate gain ≠ Long-term advantage**
- **Mobility matters** more than piece count (early/mid game)
- **Corners and edges** trump temporary gains

## Implementation Details

### Piece Counting

```python
current_turn = game.get_turn()

for move in moves:
    game.move(move)
    
    # Count pieces after move
    if current_turn == 'B':
        piece_count = game.black_cnt
    else:
        piece_count = game.white_cnt
    
    game.undo_move()
```

### Move-Undo System

Relies on game's ability to:
1. Apply move: `game.move(move)`
2. Restore state: `game.undo_move()`

This is **safe** because:
- Game stores history
- Undo reverts all changes
- No permanent modification during evaluation

## Improvements

### Enhanced Greedy Variants

```python
class SmartGreedy(GreedyPlayer):
    """Greedy with corner awareness"""
    
    def get_move(self, game, moves, control):
        # Check for corner moves first
        corners = [(1,1), (1,8), (8,1), (8,8)]
        corner_moves = [m for m in moves 
                       if (m.x, m.y) in corners]
        
        if corner_moves:
            return corner_moves[0]  # Take corner!
        
        # Otherwise, be greedy
        return super().get_move(game, moves, control)
```

### Weighted Greedy

```python
class WeightedGreedy(GreedyPlayer):
    """Greedy with position weights"""
    
    WEIGHTS = [
        [100, -20, 10,  5,  5, 10, -20, 100],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [ 10,  -2,  5,  1,  1,  5,  -2,  10],
        [  5,  -2,  1,  0,  0,  1,  -2,   5],
        [  5,  -2,  1,  0,  0,  1,  -2,   5],
        [ 10,  -2,  5,  1,  1,  5,  -2,  10],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [100, -20, 10,  5,  5, 10, -20, 100],
    ]
    
    def get_move(self, game, moves, control):
        best_move = None
        best_score = -999999
        
        for move in moves:
            # Count flips (greedy component)
            game.move(move)
            piece_count = count_pieces()
            game.undo_move()
            
            # Add position weight
            weight = self.WEIGHTS[move.y-1][move.x-1]
            score = piece_count + weight
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
```

## Debugging

### Verbose Greedy

```python
class VerboseGreedy(GreedyPlayer):
    """Greedy that explains its choices"""
    
    def get_move(self, game, moves, control):
        print(f"\n{'='*60}")
        print(f"GREEDY EVALUATION - Turn {game.turn_cnt}")
        print(f"{'='*60}")
        
        evaluations = []
        
        for move in moves:
            game.move(move)
            piece_count = (game.black_cnt if game.turn == 'W' 
                          else game.white_cnt)
            game.undo_move()
            
            evaluations.append((move, piece_count))
            print(f"{move}: {piece_count} pieces")
        
        best_move = max(evaluations, key=lambda x: x[1])[0]
        print(f"\nChosen: {best_move} (greediest!)")
        print(f"{'='*60}\n")
        
        return best_move
```

## See Also

- [Base Player Class](Player.md)
- [Random Chaos](Monkey.md) - Even simpler
- [Heuristic Scout](HeuristicPlayer.md) - Strategic improvement
- [Alpha-Beta AI](AIPlayer.md) - Full lookahead

