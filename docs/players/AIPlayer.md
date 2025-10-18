# Alpha-Beta AI (AIPlayer)

## Overview

The `AIPlayer` is the classic minimax AI with alpha-beta pruning. It's the foundation AI player in Reversi42, providing solid, reliable gameplay through deep search and strategic evaluation. This is the standard implementation that all advanced AI players build upon.

## Class Definition

```python
class AIPlayer(Player):
    """Classic minimax with alpha-beta pruning - solid and reliable"""
```

## Location
`src/Players/AIPlayer.py`

## Key Features

### 1. Minimax Search
- Full game tree exploration
- Looks ahead multiple moves (configurable depth)
- Evaluates future positions
- Finds optimal move sequences

### 2. Alpha-Beta Pruning
- Eliminates unnecessary branches
- Typically prunes 50-70% of tree
- Maintains optimal play while reducing computation
- Essential for practical search depths

### 3. Configurable Depth
- Depth 1-10 supported
- Higher depth = stronger play
- Default depth: 6 (good balance)
- Depth 10+ feasible only for endgame

### 4. Position Evaluation
- Uses `MinimaxEngine` evaluation function
- Considers position value, mobility, stability
- Balanced early/mid/late game play

## How It Works

### Minimax Algorithm

The minimax algorithm assumes both players play optimally:

```
MAX player (us):     Choose move that maximizes score
MIN player (opponent): Choose move that minimizes our score
```

### Algorithm Flow

```python
def minimax(game, depth, is_maximizing):
    if depth == 0 or game_over:
        return evaluate(game)
    
    if is_maximizing:
        max_score = -infinity
        for move in valid_moves:
            game.move(move)
            score = minimax(game, depth-1, False)
            game.undo_move()
            max_score = max(max_score, score)
        return max_score
    else:
        min_score = +infinity
        for move in valid_moves:
            game.move(move)
            score = minimax(game, depth-1, True)
            game.undo_move()
            min_score = min(min_score, score)
        return min_score
```

### Alpha-Beta Pruning

Optimization that skips branches that can't affect the final decision:

```python
def alphabeta(game, depth, alpha, beta, is_maximizing):
    if depth == 0 or game_over:
        return evaluate(game)
    
    if is_maximizing:
        for move in valid_moves:
            game.move(move)
            score = alphabeta(game, depth-1, alpha, beta, False)
            game.undo_move()
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Beta cutoff - prune this branch
        return alpha
    else:
        for move in valid_moves:
            game.move(move)
            score = alphabeta(game, depth-1, alpha, beta, True)
            game.undo_move()
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cutoff - prune this branch
        return beta
```

### Evaluation Function

The `MinimaxEngine` evaluates positions based on:

1. **Material**: Piece count (weighted by game phase)
2. **Mobility**: Number of available moves
3. **Position**: Corner and edge control
4. **Stability**: Pieces that cannot be flipped

## Configuration

### Metadata

```python
PLAYER_METADATA = {
    'display_name': 'Alpha-Beta AI',
    'description': 'Classic minimax with alpha-beta pruning - solid and reliable',
    'enabled': True,
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
}
```

### Initialization

```python
# Default depth 6
ai = AIPlayer(deep=6)

# Easy opponent (depth 3)
easy_ai = AIPlayer(deep=3)

# Strong opponent (depth 8)
strong_ai = AIPlayer(deep=8)

# Maximum strength (depth 10)
expert_ai = AIPlayer(deep=10)
```

## Performance Characteristics

### Search Depth Guide

| Depth | Skill Level | Time per Move | Positions Evaluated | Use Case |
|-------|-------------|---------------|---------------------|----------|
| 1 | Weak | <0.01s | ~10 | Testing only |
| 2 | Beginner | ~0.05s | ~100 | Very easy |
| 3 | Novice | ~0.1s | ~1,000 | Easy opponent |
| 4 | Intermediate | ~0.5s | ~10,000 | Moderate challenge |
| 5 | Advanced | ~2s | ~100,000 | Good player |
| 6 | Strong | ~5-10s | ~1,000,000 | Default setting |
| 7 | Expert | ~30s | ~10,000,000 | Tough opponent |
| 8 | Master | ~2min | ~100,000,000 | Very strong |
| 9 | Grandmaster | ~10min | ~1,000,000,000 | Extremely strong |
| 10 | Super-GM | ~30min+ | ~10,000,000,000 | Maximum strength |

**Note**: Times are approximate and vary by position complexity.

### Branching Factor

Average branching factor in Reversi: ~10-15 moves
- Early game: 8-12 moves
- Mid game: 10-15 moves
- Late game: 5-10 moves
- Endgame: 1-5 moves

### Pruning Efficiency

Alpha-beta typically achieves:
- **Best case**: √(positions) - 50% reduction per ply
- **Average case**: 50-70% pruning
- **Worst case**: No pruning (rare)

Move ordering improves pruning:
- Good ordering → 70-80% pruning
- Poor ordering → 40-50% pruning

## Strengths

### 1. Optimal Play (at given depth)
- Finds best move within search horizon
- Guaranteed not to miss forced wins
- Sound tactical play

### 2. Consistent Strength
- Depth directly correlates to strength
- Predictable difficulty scaling
- No random variation

### 3. Complete Search
- Evaluates all legal moves
- No blind spots within depth
- Thorough position analysis

### 4. Well-Tested Algorithm
- Decades of game AI research
- Proven effective for Reversi
- Reliable implementation

## Weaknesses

### 1. Speed Limitations
- Exponential time complexity: O(b^d)
- Depth 8+ takes significant time
- Not suitable for quick games at high depth

### 2. Horizon Effect
- Can only see within search depth
- May make moves that look good at depth but fail later
- Long-term plans beyond depth are invisible

### 3. Static Evaluation
- Evaluation function is hand-crafted
- Doesn't learn or adapt
- May miss subtle positional factors

### 4. No Opening Knowledge
- Must compute every move from scratch
- Wastes time on known theory
- Can make suboptimal early moves

## Example Usage

### Basic Usage

```python
from Players.AIPlayer import AIPlayer

# Create AI at depth 6
ai = AIPlayer(deep=6)

# Get move
move = ai.get_move(game, valid_moves, control)

# Execute move
game.move(move)
```

### Difficulty Progression

```python
# Create opponents of increasing difficulty
beginner = AIPlayer(deep=3)    # Easy
intermediate = AIPlayer(deep=4) # Medium
advanced = AIPlayer(deep=6)     # Hard
expert = AIPlayer(deep=8)       # Very Hard
```

### Adaptive Depth

```python
class AdaptiveAI(AIPlayer):
    """AI that adjusts depth based on game phase"""
    
    def get_move(self, game, moves, control):
        # Deeper search in endgame
        pieces = game.black_cnt + game.white_cnt
        
        if pieces < 20:
            self.deep = 6   # Opening: moderate
        elif pieces < 50:
            self.deep = 6   # Midgame: moderate
        else:
            self.deep = 10  # Endgame: deep
        
        return super().get_move(game, moves, control)
```

### Tournament Usage

```python
# Standard competitive depth
tournament_ai = AIPlayer(deep=6)

# Run tournament
results = []
for opponent in all_opponents:
    result = game.play(tournament_ai, opponent)
    results.append(result)

print(f"Tournament results: {calculate_stats(results)}")
```

## Win Rates (Approximate)

| Opponent | AIPlayer(6) Win Rate |
|----------|----------------------|
| Random Chaos | ~100% |
| Greedy Goblin | ~95% |
| Heuristic Scout | ~90% |
| AIPlayer(4) | ~75% |
| AIPlayer(6) mirror | ~52% (first-player advantage) |
| AIPlayer(8) | ~30% |
| Bitboard Blitz(8) | ~30% (same algorithm, faster) |
| The Oracle(8) | ~25% (opening book advantage) |
| Grandmaster(9) | ~10% |

## Advanced Techniques

### Move Ordering

Improve pruning with better move ordering:

```python
def order_moves(moves, game):
    """Order moves to improve alpha-beta pruning"""
    corners = []
    edges = []
    others = []
    
    for move in moves:
        if is_corner(move):
            corners.append(move)
        elif is_edge(move):
            edges.append(move)
        else:
            others.append(move)
    
    # Search corners first (likely best)
    return corners + edges + others
```

### Iterative Deepening

```python
class IterativeDeepAI(AIPlayer):
    """Gradually increase depth until time limit"""
    
    def get_move(self, game, moves, control):
        best_move = moves[0]
        time_limit = 10.0  # seconds
        start_time = time.time()
        
        for depth in range(1, 12):
            if time.time() - start_time > time_limit:
                break
            
            self.deep = depth
            best_move = super().get_move(game, moves, control)
        
        return best_move
```

### Transposition Tables

```python
class TTAIPlayer(AIPlayer):
    """AI with transposition table for speed"""
    
    def __init__(self, deep=6):
        super().__init__(deep)
        self.tt = {}  # Transposition table
    
    def evaluate_position(self, game, depth):
        # Hash the position
        position_hash = game.get_hash()
        
        # Check if we've seen this position
        if position_hash in self.tt:
            cached_depth, cached_score = self.tt[position_hash]
            if cached_depth >= depth:
                return cached_score
        
        # Evaluate and cache
        score = self.minimax(game, depth)
        self.tt[position_hash] = (depth, score)
        return score
```

## Debugging

### Verbose Mode

```python
class VerboseAI(AIPlayer):
    """AI that explains its thinking"""
    
    def get_move(self, game, moves, control):
        print(f"\n{'='*60}")
        print(f"ALPHA-BETA AI - Depth {self.deep}")
        print(f"Turn {game.turn_cnt}, {len(moves)} legal moves")
        print(f"{'='*60}")
        
        move = super().get_move(game, moves, control)
        
        print(f"Selected: {move}")
        print(f"Expected outcome: {self.last_score}")
        print(f"Positions evaluated: {self.positions_evaluated}")
        print(f"Time taken: {self.last_time:.2f}s")
        print(f"{'='*60}\n")
        
        return move
```

## Integration with MinimaxEngine

AIPlayer delegates to `MinimaxEngine`:

```python
from AI.MinimaxEngine import MinimaxEngine

def __init__(self, deep=6):
    self.depth = deep
    self.deep = deep
    self.name = f'AlphaBeta{deep}'
    self.engine = MinimaxEngine()

def get_move(self, game, moves, control):
    return self.engine.get_best_move(game, self.deep, player_name=self.name)
```

See `src/AI/MinimaxEngine.py` for engine implementation details.

## See Also

- [Base Player Class](Player.md)
- [Heuristic Scout](HeuristicPlayer.md) - Simpler alternative
- [Opening Scholar](AIPlayerBook.md) - With opening book
- [Bitboard Blitz](AIPlayerBitboard.md) - Faster version
- [Minimax Engine Documentation](../AI_ENGINES.md)

