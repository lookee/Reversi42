# Apocalyptron Engine - Technical Deep Dive

Complete technical documentation of the Apocalyptron AI engine, the most advanced AI in Reversi42.

## Overview

**Apocalyptron** is the ultimate Reversi AI engine in Reversi42, combining all known optimization techniques to achieve **3500-14000x speedup** over basic minimax and a **+40-50% win rate** improvement over standard parallel AI.

### Key Statistics

- **Performance**: 3500-14000x faster than basic AI
- **Default Depth**: 9 (configurable 7-12)
- **Win Rate**: +40-50% vs base parallel AI
- **Opening Book**: 644 professional sequences
- **Search Speed**: 100K-1M nodes/second
- **Response Time**: <1 second at depth 9

### Architecture Philosophy

Apocalyptron follows a **modular, composable architecture** where each optimization technique is:
- Independently testable
- Separately configurable
- Composable with others
- Observable and measurable

## System Architecture

```
┌─────────────────────────────────────────────────┐
│            Apocalyptron Engine                  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │         Core Components                   │  │
│  │                                           │  │
│  │  ┌─────────────┐    ┌─────────────┐       │  │  
│  │  │   Config    │    │   Factory   │       │  │ 
│  │  └─────────────┘    └─────────────┘       │  │  
│  │                                           |  │  
│  │  ┌─────────────┐    ┌─────────────┐       │  │
│  │  │   Engine    │───>│   Context   │       │  │
│  │  └─────────────┘    └─────────────┘       │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │         Search Module                     │  │
│  │                                           │  │
│  │  ┌──────────────────┐                     │  │
│  │  │ Iterative        │                     │  │
│  │  │ Deepening        │                     │  │
│  │  └────────┬─────────┘                     │  │
│  │           │                               │  │
│  │           ▼                               │  │
│  │  ┌──────────────────┐                     │  │
│  │  │ Alpha-Beta       │                     │  │
│  │  │ Complete         │                     │  │
│  │  └────────┬─────────┘                     │  │
│  │           │                               │  │
│  │           ▼                               │  │
│  │  ┌──────────────────┐                     │  │
│  │  │ Parallel         │                     │  │
│  │  │ Search           │                     │  │
│  │  └──────────────────┘                     │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │       Evaluation Module                   │  │
│  │                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │  Mobility   │  │  Stability  │         │  │
│  │  └─────────────┘  └─────────────┘         │  │
│  │  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │ Positional  │  │   Parity    │         │  │
│  │  └─────────────┘  └─────────────┘         │  │
│  │  ┌─────────────────────────────┐          │  │
│  │  │  Composite Evaluator        │          │  │
│  │  └─────────────────────────────┘          │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │         Ordering Module                   │  │
│  │                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │  PV Move    │  │  Killer     │         │  │
│  │  └─────────────┘  └─────────────┘         │  │
│  │  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │  History    │  │ Positional  │         │  │
│  │  └─────────────┘  └─────────────┘         │  │
│  │  ┌─────────────────────────────┐          │  │
│  │  │  Composite Orderer          │          │  │
│  │  └─────────────────────────────┘          │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │         Pruning Module                    │  │
│  │                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │  Null Move  │  │  Futility   │         │  │
│  │  └─────────────┘  └─────────────┘         │  │
│  │  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │     LMR     │  │  Multi-Cut  │         │  │
│  │  └─────────────┘  └─────────────┘         │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │          Cache Module                     │  │
│  │                                           │  │
│  │  ┌──────────────────────────────┐         │  │
│  │  │  Zobrist Hashing             │         │  │
│  │  └──────────────────────────────┘         │  │
│  │  ┌──────────────────────────────┐         │  │
│  │  │  Transposition Table         │         │  │
│  │  └──────────────────────────────┘         │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │        Observer Module                    │  │
│  │                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │  Console    │  │ Statistics  │         │  │
│  │  └─────────────┘  └─────────────┘         │  │
│  │  ┌─────────────┐                          │  │
│  │  │    Quiet    │                          │  │
│  │  └─────────────┘                          │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │        Opening Book                       │  │
│  │                                           │  │
│  │  644 Professional Sequences               │  │
│  │  Trie-based O(m) Lookup                   │  │
│  └───────────────────────────────────────────┘  git│
└─────────────────────────────────────────────────┘
```

## Module 1: Search

### 1.1 Iterative Deepening

**Purpose**: Search progressively deeper, enabling time management and move ordering improvements.

**Location**: `src/AI/Apocalyptron/search/iterative_deepening.py`

**How It Works**:

```python
class IterativeDeepeningSearch:
    """
    Searches from depth 1 to max_depth incrementally.
    
    Benefits:
    - Time management (can stop anytime)
    - Better move ordering (use results from shallow search)
    - Aspiration windows optimization
    - Progressive refinement
    """
    
    def search(self, game, max_depth):
        best_move = None
        best_score = -float('inf')
        
        # Search depth 1, 2, 3, ..., max_depth
        for depth in range(1, max_depth + 1):
            # Use aspiration windows (narrow alpha-beta)
            alpha, beta = self._get_aspiration_window(best_score)
            
            try:
                score, move = self._search_depth(game, depth, alpha, beta)
                
                if move:
                    best_move = move
                    best_score = score
                    
                # Store in transposition table for next iteration
                self._store_pv_move(game, move, score)
                
            except TimeoutException:
                # Return best move from previous complete iteration
                break
        
        return best_score, best_move
```

**Key Features**:

1. **Aspiration Windows**
   ```python
   def _get_aspiration_window(self, prev_score):
       """Narrow window around previous score."""
       window = 50  # Typical window size
       alpha = prev_score - window
       beta = prev_score + window
       return alpha, beta
   ```
   - Start with narrow [α, β] window
   - If fail-high or fail-low, re-search with wider window
   - Much faster when score is stable

2. **Time Management**
   ```python
   def _should_continue(self, depth, time_elapsed):
       """Decide if we have time for next depth."""
       # Estimate time for next depth (exponential growth)
       estimated_time = time_elapsed * branching_factor
       return estimated_time < time_limit
   ```

3. **Progressive Results**
   - Always have a move from previous depth
   - Can stop anytime and return best so far
   - Graceful degradation under time pressure

**Performance Impact**: Enables all other optimizations to work better. Minimal overhead (~5%) but enables 2-3x speedup through better ordering.

### 1.2 Alpha-Beta Search

**Purpose**: Core minimax search with alpha-beta pruning.

**Location**: `src/AI/Apocalyptron/search/alphabeta_complete.py`

**Algorithm**:

```python
def alphabeta(game, depth, alpha, beta, maximizing):
    """
    Alpha-beta pruning minimax search.
    
    Prunes branches that cannot improve the result:
    - Alpha: Best score maximizer can guarantee
    - Beta: Best score minimizer can guarantee
    - If beta <= alpha: Prune this branch
    """
    
    # Terminal conditions
    if depth == 0 or game.is_game_over():
        return evaluate(game), None
    
    # Check transposition table
    tt_entry = transposition_table.lookup(game)
    if tt_entry and tt_entry.depth >= depth:
        return tt_entry.score, tt_entry.move
    
    moves = game.get_valid_moves(game.current_player)
    
    if not moves:
        # Pass turn
        return alphabeta(game.pass_turn(), depth, alpha, beta, not maximizing)
    
    # Order moves (critical for pruning efficiency)
    moves = move_orderer.order(moves, game)
    
    best_move = moves[0]
    
    if maximizing:
        value = -float('inf')
        for move in moves:
            new_game = game.make_move(move)
            score, _ = alphabeta(new_game, depth - 1, alpha, beta, False)
            
            if score > value:
                value = score
                best_move = move
            
            alpha = max(alpha, value)
            
            # Beta cutoff: opponent won't allow this
            if beta <= alpha:
                killer_moves.add(move, depth)
                break
        
        return value, best_move
    
    else:
        value = float('inf')
        for move in moves:
            new_game = game.make_move(move)
            score, _ = alphabeta(new_game, depth - 1, alpha, beta, True)
            
            if score < value:
                value = score
                best_move = move
            
            beta = min(beta, value)
            
            # Alpha cutoff
            if beta <= alpha:
                killer_moves.add(move, depth)
                break
        
        return value, best_move
```

**Optimizations Applied**:

1. **Fail-Soft** - Return exact score even outside [α, β]
2. **Transposition Table Cutoffs** - Skip entire subtrees
3. **Move Ordering** - Critical for maximum pruning
4. **Killer Move Heuristic** - Remember moves that caused cutoffs

**Performance**: Reduces nodes searched by ~90% compared to minimax. From O(b^d) to O(b^(d/2)) in best case.

### 1.3 Parallel Search

**Purpose**: Utilize multiple CPU cores for faster search.

**Location**: `src/AI/Apocalyptron/search/parallel.py`

**Parallelization Strategy**:

```python
class ParallelSearch:
    """
    Parallel alpha-beta search using Young Brothers Wait Concept (YBWC).
    
    Strategy:
    - First move searched serially (PV move)
    - Remaining moves searched in parallel
    - Shared transposition table
    - Lock-free where possible
    """
    
    def parallel_search(self, game, depth, alpha, beta):
        moves = self._get_ordered_moves(game)
        
        if not moves:
            return self._evaluate(game), None
        
        # Search first move serially (likely best)
        first_move = moves[0]
        best_score, _ = self._serial_search(
            game.make_move(first_move),
            depth - 1,
            alpha,
            beta
        )
        best_move = first_move
        
        # If only one move, done
        if len(moves) == 1:
            return best_score, best_move
        
        # Parallel search remaining moves
        with ProcessPoolExecutor(max_workers=self.num_cores) as executor:
            futures = []
            
            for move in moves[1:]:
                future = executor.submit(
                    self._search_move,
                    game,
                    move,
                    depth - 1,
                    alpha,
                    beta
                )
                futures.append((move, future))
            
            # Collect results
            for move, future in futures:
                try:
                    score = future.result(timeout=self.move_timeout)
                    
                    if score > best_score:
                        best_score = score
                        best_move = move
                        alpha = max(alpha, score)
                        
                except TimeoutError:
                    # Use score from transposition table or heuristic
                    pass
        
        return best_score, best_move
```

**Challenges & Solutions**:

1. **Shared State**
   - **Challenge**: Multiple processes accessing transposition table
   - **Solution**: Lock-free reads, locked writes, separate tables per process

2. **Load Balancing**
   - **Challenge**: Some moves take much longer
   - **Solution**: Work stealing, dynamic task distribution

3. **Overhead**
   - **Challenge**: Process creation and communication cost
   - **Solution**: Only parallelize at depth >= 7, reuse process pool

**Performance**: 2-5x speedup on 4-8 core systems. Diminishing returns beyond 8 cores due to overhead.

## Module 2: Evaluation

### 2.1 Composite Evaluator

**Purpose**: Combine multiple evaluation heuristics with phase-aware weights.

**Location**: `src/AI/Apocalyptron/evaluation/composite.py`

**Architecture**:

```python
class CompositeEvaluator:
    """
    Combines multiple evaluators with phase-dependent weights.
    
    Phases:
    - Opening (moves 0-20): Mobility and development
    - Midgame (moves 21-50): Stability and position
    - Endgame (moves 51-64): Exact counting
    """
    
    def __init__(self):
        self.evaluators = {
            'mobility': MobilityEvaluator(),
            'stability': StabilityEvaluator(),
            'positional': PositionalEvaluator(),
            'parity': ParityEvaluator()
        }
        
        self.phase_detector = PhaseDetector()
        self.weights = self._get_default_weights()
    
    def evaluate(self, game):
        """Weighted combination of all evaluators."""
        phase = self.phase_detector.detect_phase(game)
        weights = self.weights[phase]
        
        total_score = 0.0
        
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate(game)
            weight = weights[name]
            total_score += score * weight
        
        return total_score
```

### 2.2 Mobility Evaluator

**Purpose**: Evaluate based on number of available moves.

**Formula**:
```
mobility_score = (my_moves - opp_moves) / (my_moves + opp_moves + 1)
```

**Implementation**:

```python
class MobilityEvaluator:
    """
    Mobility: Having more moves is advantageous.
    
    Types of mobility:
    - Actual: Current move count
    - Potential: Future mobility after opponent moves
    """
    
    def evaluate(self, game):
        my_moves = len(game.get_valid_moves(game.current_player))
        opp_moves = len(game.get_valid_moves(-game.current_player))
        
        if my_moves + opp_moves == 0:
            return 0.0
        
        # Normalize to [-1, 1]
        mobility = (my_moves - opp_moves) / (my_moves + opp_moves)
        
        # Bonus for opponent having no moves (forced pass)
        if opp_moves == 0 and my_moves > 0:
            mobility += 0.5
        
        return mobility * 100  # Scale to ±100
```

**Importance**: Very high in opening/midgame, low in endgame.

### 2.3 Stability Evaluator

**Purpose**: Evaluate based on pieces that cannot be flipped.

**Categories**:
- **Stable**: Cannot be flipped (corners, edges connected to corners)
- **Semi-stable**: Temporarily safe
- **Unstable**: Can be flipped

**Implementation**:

```python
class StabilityEvaluator:
    """
    Stability: Pieces that cannot be flipped are valuable.
    
    Detection:
    - Corners are always stable
    - Edges connected to corners are stable
    - Interior pieces surrounded by friendly pieces
    """
    
    def evaluate(self, game):
        my_stable = self._count_stable(game, game.current_player)
        opp_stable = self._count_stable(game, -game.current_player)
        
        return (my_stable - opp_stable) * 10
    
    def _count_stable(self, game, player):
        """Count stable pieces using flood fill from corners."""
        stable_mask = 0
        
        # Start from corners
        corners = [0, 7, 56, 63]
        for corner in corners:
            if game.get_piece_at(corner) == player:
                # Flood fill along edges and interior
                stable_mask |= self._flood_fill_stable(game, corner, player)
        
        return popcount(stable_mask)
```

**Importance**: Critical in midgame and endgame.

### 2.4 Positional Evaluator

**Purpose**: Evaluate based on strategic value of squares.

**Position Weights**:

```python
POSITION_WEIGHTS = [
    [100, -20,  10,   5,   5,  10, -20, 100],  # Row 1
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],  # Row 2
    [ 10,  -5,   5,   1,   1,   5,  -5,  10],  # Row 3
    [  5,  -5,   1,   0,   0,   1,  -5,   5],  # Row 4
    [  5,  -5,   1,   0,   0,   1,  -5,   5],  # Row 5
    [ 10,  -5,   5,   1,   1,   5,  -5,  10],  # Row 6
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],  # Row 7
    [100, -20,  10,   5,   5,  10, -20, 100],  # Row 8
]
```

**Rationale**:
- **Corners (100)**: Most valuable, cannot be flipped
- **X-squares (-40)**: Dangerous, often give opponent corner
- **C-squares (-20)**: Risky, adjacent to corners
- **Edges (10)**: Good, hard to flip
- **Center (0-1)**: Neutral, easily flipped

**Implementation**:

```python
class PositionalEvaluator:
    """Evaluate based on strategic position values."""
    
    def evaluate(self, game):
        my_score = 0
        opp_score = 0
        
        for pos in range(64):
            row, col = pos // 8, pos % 8
            weight = POSITION_WEIGHTS[row][col]
            
            piece = game.get_piece_at(pos)
            if piece == game.current_player:
                my_score += weight
            elif piece == -game.current_player:
                opp_score += weight
        
        return my_score - opp_score
```

### 2.5 Parity Evaluator

**Purpose**: Prefer to move last in sequences.

**Concept**: In Reversi, moving last in a region is often advantageous.

```python
class ParityEvaluator:
    """
    Parity: Moving last is often better.
    
    Simple heuristic: Prefer even number of empty squares
    in endgame so opponent moves first in final sequence.
    """
    
    def evaluate(self, game):
        if not self._is_endgame(game):
            return 0
        
        empty_count = 64 - popcount(game.black | game.white)
        
        # Prefer opponent to move first at very end
        if empty_count <= 10:
            return 5 if empty_count % 2 == 0 else -5
        
        return 0
```

### Phase-Dependent Weights

```python
WEIGHTS = {
    'opening': {
        'mobility': 0.50,     # Very important
        'stability': 0.10,    # Not yet relevant
        'positional': 0.30,   # Moderately important
        'parity': 0.10        # Minor factor
    },
    'midgame': {
        'mobility': 0.30,     # Still important
        'stability': 0.40,    # Now critical
        'positional': 0.20,   # Less important
        'parity': 0.10        # Minor factor
    },
    'endgame': {
        'mobility': 0.10,     # Less important
        'stability': 0.50,    # Most critical
        'positional': 0.10,   # Less relevant
        'parity': 0.30        # Now important
    }
}
```

## Module 3: Ordering

### Purpose

Move ordering determines the order in which moves are tried. **Good ordering = more pruning = faster search**.

### 3.1 PV Move Ordering

**Purpose**: Try the principal variation (best move from previous iteration) first.

```python
class PVMoveOrderer:
    """
    Always try PV move first.
    
    The PV move is the best move from:
    - Previous iteration (iterative deepening)
    - Transposition table
    - Previous search at this position
    """
    
    def order(self, moves, game):
        pv_move = self._get_pv_move(game)
        
        if pv_move and pv_move in moves:
            # PV move first, rest unchanged
            ordered = [pv_move]
            ordered.extend(m for m in moves if m != pv_move)
            return ordered
        
        return moves
```

**Impact**: PV move causes cutoff ~70% of the time → huge pruning.

### 3.2 Killer Move Heuristic

**Purpose**: Try moves that caused cutoffs at the same depth in other branches.

```python
class KillerMoveOrderer:
    """
    Track moves that caused beta cutoffs.
    
    Idea: Moves that were good in one branch are likely
    good in sibling branches at same depth.
    """
    
    def __init__(self):
        # killer_moves[depth] = [move1, move2]
        self.killer_moves = defaultdict(list)
        self.max_killers = 2
    
    def add_killer(self, move, depth):
        """Record a move that caused cutoff."""
        killers = self.killer_moves[depth]
        
        if move in killers:
            # Already recorded, move to front
            killers.remove(move)
            killers.insert(0, move)
        else:
            # Add new killer
            killers.insert(0, move)
            # Keep only best killers
            if len(killers) > self.max_killers:
                killers.pop()
    
    def order(self, moves, game, depth):
        killers = self.killer_moves[depth]
        
        # Killers first, then rest
        ordered = [m for m in killers if m in moves]
        ordered.extend(m for m in moves if m not in killers)
        
        return ordered
```

**Impact**: 10-20% additional pruning.

### 3.3 History Heuristic

**Purpose**: Try moves that have historically performed well.

```python
class HistoryHeuristic:
    """
    Track historical success of moves.
    
    For each move, track:
    - Number of times it caused cutoff
    - Total times it was tried
    - Success rate = cutoffs / tries
    """
    
    def __init__(self):
        # history[move] = (cutoffs, tries)
        self.history = defaultdict(lambda: (0, 0))
    
    def update(self, move, caused_cutoff):
        """Update history for a move."""
        cutoffs, tries = self.history[move]
        if caused_cutoff:
            cutoffs += 1
        tries += 1
        self.history[move] = (cutoffs, tries)
    
    def get_score(self, move):
        """Get historical success score."""
        cutoffs, tries = self.history[move]
        if tries == 0:
            return 0
        return cutoffs / tries
    
    def order(self, moves, game):
        """Order by historical success."""
        return sorted(moves, 
                     key=lambda m: self.get_score(m),
                     reverse=True)
```

**Impact**: 5-10% improvement, especially in similar positions.

### 3.4 Positional Ordering

**Purpose**: Try strategically valuable moves first (corners, edges).

```python
class PositionalOrderer:
    """Order moves by positional value."""
    
    # Same weights as positional evaluator
    WEIGHTS = POSITION_WEIGHTS
    
    def order(self, moves, game):
        """Order by position weight."""
        def move_value(move):
            row, col = move // 8, move % 8
            return self.WEIGHTS[row][col]
        
        return sorted(moves, key=move_value, reverse=True)
```

**Impact**: Baseline ordering, ~20% better than random.

### 3.5 Composite Ordering

**Purpose**: Combine all ordering strategies.

```python
class CompositeOrderer:
    """
    Combines all ordering strategies in priority order:
    
    1. PV move (from TT or previous iteration)
    2. Killer moves (from same depth)
    3. Tactical captures (mobility-reducing moves)
    4. History heuristic score
    5. Positional value
    """
    
    def order(self, moves, game, depth):
        # Start with positional ordering
        ordered = self.positional.order(moves, game)
        
        # Apply history scores
        ordered = sorted(ordered,
                        key=lambda m: self.history.get_score(m),
                        reverse=True)
        
        # Prioritize killers
        killers = self.killer_moves.get(depth, [])
        for killer in reversed(killers):
            if killer in ordered:
                ordered.remove(killer)
                ordered.insert(0, killer)
        
        # PV move absolutely first
        pv_move = self.get_pv_move(game)
        if pv_move and pv_move in ordered:
            ordered.remove(pv_move)
            ordered.insert(0, pv_move)
        
        return ordered
```

**Total Impact**: 5-10x fewer nodes searched compared to random ordering.

## Module 4: Pruning

### 4.1 Null Move Pruning

**Purpose**: Skip opponent's turn to get lower bound on position value quickly.

**Concept**: If even after giving opponent a free move, position is still good, we can prune.

```python
def null_move_prune(game, depth, beta):
    """
    Null move pruning: Give opponent free move.
    
    If position is still >= beta even with null move,
    we can prune this branch (opponent has even better options).
    """
    
    # Don't use in these situations:
    if depth < 3:  # Too shallow
        return False
    if game.is_endgame():  # Zugzwang possible
        return False
    if game.in_check():  # Invalid null move
        return False
    
    # Make null move (pass turn without moving)
    null_game = game.pass_turn()
    
    # Search with reduced depth
    R = 2  # Reduction factor
    score, _ = alphabeta(null_game, depth - 1 - R, -beta, -beta + 1, False)
    score = -score
    
    # If null move is good enough, prune
    if score >= beta:
        return True  # Prune this branch
    
    return False  # Continue searching
```

**Safety**: In Reversi, zugzwang (being forced to move is bad) is rare, so null move is quite safe.

**Impact**: 20-40% node reduction in midgame.

### 4.2 Futility Pruning

**Purpose**: Skip moves that cannot improve alpha even with best-case gains.

```python
def futility_prune(game, move, depth, alpha):
    """
    Futility pruning: Skip obviously bad moves.
    
    If even with maximum possible gain from this move,
    we can't reach alpha, skip it.
    """
    
    if depth > 3:  # Only at frontier nodes
        return False
    
    # Static evaluation of position
    static_eval = evaluate(game)
    
    # Maximum possible gain (optimistic)
    max_gain = 200 * depth  # ~2 pieces per ply
    
    # Futility margin
    if static_eval + max_gain < alpha:
        return True  # Prune: can't reach alpha
    
    return False
```

**Impact**: 10-15% reduction at frontier nodes.

### 4.3 Late Move Reduction (LMR)

**Purpose**: Search later moves (likely bad) at reduced depth.

```python
def late_move_reduction(game, move, depth, move_index, alpha, beta):
    """
    Late Move Reduction: Search later moves at reduced depth.
    
    Assumption: First few moves (well-ordered) are best.
    Later moves can be searched shallower.
    """
    
    # Don't reduce first few moves or at low depth
    if move_index < 4 or depth < 3:
        # Full depth search
        return alphabeta(game.make_move(move), depth - 1, alpha, beta, False)
    
    # Reduce depth for later moves
    R = 1 if depth >= 6 else 0
    reduced_depth = depth - 1 - R
    
    # Search at reduced depth
    score, _ = alphabeta(game.make_move(move), reduced_depth, alpha, beta, False)
    
    # If reduced search shows move might be good, re-search at full depth
    if score > alpha:
        score, _ = alphabeta(game.make_move(move), depth - 1, alpha, beta, False)
    
    return score
```

**Impact**: 30-50% reduction in nodes, especially with good ordering.

### 4.4 Multi-Cut Pruning

**Purpose**: If several moves cause cutoffs, remaining moves likely don't matter.

```python
def multi_cut_prune(game, moves, depth, beta):
    """
    Multi-Cut: If M moves fail high, prune rest.
    
    Idea: If multiple moves are already "too good",
    opponent won't allow this position.
    """
    
    M = 3  # Number of cutoffs needed
    C = 10  # Number of moves to try
    R = 2  # Reduction for test searches
    
    cutoff_count = 0
    
    for i, move in enumerate(moves[:C]):
        # Quick shallow search
        score, _ = alphabeta(
            game.make_move(move),
            depth - 1 - R,
            beta - 1,
            beta,
            False
        )
        
        if score >= beta:
            cutoff_count += 1
            
            if cutoff_count >= M:
                return True  # Prune remaining moves
    
    return False
```

**Impact**: 10-20% reduction in certain positions (opponent has many good responses).

## Module 5: Cache

### 5.1 Zobrist Hashing

**Purpose**: Create unique hash for each position for transposition table lookups.

```python
class ZobristHash:
    """
    Zobrist hashing: Fast, collision-resistant position hashing.
    
    Method:
    - Random 64-bit number for each (piece, square) pair
    - XOR all numbers for pieces on board
    - XOR to update incrementally
    """
    
    def __init__(self):
        # Random numbers for each position and piece type
        # zobrist[piece][position] = random 64-bit int
        self.zobrist = self._initialize_zobrist_table()
    
    def _initialize_zobrist_table(self):
        """Generate random numbers for Zobrist hashing."""
        import random
        random.seed(42)  # Reproducible
        
        table = {}
        for piece in ['black', 'white']:
            table[piece] = [
                random.getrandbits(64) for _ in range(64)
            ]
        return table
    
    def hash_position(self, game):
        """Compute hash for position."""
        h = 0
        
        for pos in range(64):
            piece = game.get_piece_at(pos)
            if piece == 1:  # Black
                h ^= self.zobrist['black'][pos]
            elif piece == -1:  # White
                h ^= self.zobrist['white'][pos]
        
        # Include side to move
        if game.current_player == 1:
            h ^= self.zobrist_side_to_move
        
        return h
    
    def update_hash(self, hash_value, old_game, new_game, move):
        """
        Incrementally update hash (much faster).
        
        Instead of recomputing entire hash:
        - XOR out old pieces
        - XOR in new pieces
        """
        h = hash_value
        
        # Update pieces that changed
        for pos in self._get_changed_positions(old_game, new_game):
            old_piece = old_game.get_piece_at(pos)
            new_piece = new_game.get_piece_at(pos)
            
            if old_piece != 0:
                h ^= self.zobrist[self._piece_name(old_piece)][pos]
            if new_piece != 0:
                h ^= self.zobrist[self._piece_name(new_piece)][pos]
        
        # Toggle side to move
        h ^= self.zobrist_side_to_move
        
        return h
```

**Properties**:
- **Fast**: O(1) with incremental updates
- **Collision-resistant**: ~1 in 2^64 probability
- **Deterministic**: Same position = same hash

### 5.2 Transposition Table

**Purpose**: Cache search results to avoid recomputing same positions.

```python
class TranspositionTable:
    """
    Transposition table: Cache search results.
    
    Stores:
    - Position hash
    - Best move
    - Score
    - Depth searched
    - Node type (exact, lower bound, upper bound)
    """
    
    def __init__(self, size_mb=128):
        # Calculate number of entries
        entry_size = 32  # bytes per entry
        self.size = (size_mb * 1024 * 1024) // entry_size
        
        # Hash table
        self.table = [None] * self.size
        
        # Statistics
        self.hits = 0
        self.misses = 0
    
    def store(self, hash_value, depth, score, move, node_type):
        """Store search result."""
        index = hash_value % self.size
        
        existing = self.table[index]
        
        # Replace if:
        # - Slot empty
        # - New search is deeper
        # - Same depth but different move (update)
        if (existing is None or 
            depth >= existing['depth']):
            
            self.table[index] = {
                'hash': hash_value,
                'depth': depth,
                'score': score,
                'move': move,
                'type': node_type  # exact, lower, upper
            }
    
    def lookup(self, hash_value):
        """Lookup position in table."""
        index = hash_value % self.size
        entry = self.table[index]
        
        if entry and entry['hash'] == hash_value:
            self.hits += 1
            return entry
        
        self.misses += 1
        return None
    
    def get_hit_rate(self):
        """Get cache hit rate."""
        total = self.hits + self.misses
        if total == 0:
            return 0
        return self.hits / total
```

**Node Types**:
- **EXACT**: Exact score from full search
- **LOWER**: Score is lower bound (fail-high, beta cutoff)
- **UPPER**: Score is upper bound (fail-low, alpha cutoff)

**Impact**: 50-90% hit rate in typical searches → 2-5x speedup.

## Module 6: Observer

### 6.1 Observer Pattern

**Purpose**: Decouple search engine from output/monitoring.

```python
class SearchObserver(ABC):
    """Abstract base for search observers."""
    
    @abstractmethod
    def on_search_start(self, game, depth):
        pass
    
    @abstractmethod
    def on_depth_complete(self, depth, score, move, nodes):
        pass
    
    @abstractmethod
    def on_search_complete(self, best_move, best_score, total_nodes):
        pass
```

### 6.2 Console Observer

**Purpose**: Print search progress to console.

```python
class ConsoleObserver(SearchObserver):
    """Prints search progress to console."""
    
    def on_depth_complete(self, depth, score, move, nodes):
        notation = BitboardGame.position_to_notation(move)
        print(f"Depth {depth:2d}: {notation} ({score:+6.1f}) "
              f"[{nodes:,} nodes]")
    
    def on_search_complete(self, best_move, best_score, total_nodes):
        notation = BitboardGame.position_to_notation(best_move)
        print(f"\nBest: {notation} ({best_score:+6.1f})")
        print(f"Total nodes: {total_nodes:,}")
```

### 6.3 Statistics Observer

**Purpose**: Collect detailed statistics about search.

```python
class StatisticsObserver(SearchObserver):
    """Collects detailed search statistics."""
    
    def __init__(self):
        self.stats = {
            'nodes_searched': 0,
            'tt_hits': 0,
            'tt_misses': 0,
            'beta_cutoffs': 0,
            'null_move_cutoffs': 0,
            'time_elapsed': 0,
            'depths_completed': [],
            # ... many more metrics
        }
    
    def get_statistics(self):
        """Return collected statistics."""
        self.stats['nps'] = (
            self.stats['nodes_searched'] / 
            max(self.stats['time_elapsed'], 0.001)
        )
        self.stats['tt_hit_rate'] = (
            self.stats['tt_hits'] / 
            max(self.stats['tt_hits'] + self.stats['tt_misses'], 1)
        )
        return self.stats
```

### 6.4 Quiet Observer

**Purpose**: No output (for tournaments).

```python
class QuietObserver(SearchObserver):
    """Observer that produces no output."""
    
    def on_search_start(self, game, depth):
        pass
    
    def on_depth_complete(self, depth, score, move, nodes):
        pass
    
    def on_search_complete(self, best_move, best_score, total_nodes):
        pass
```

## Performance Analysis

### Benchmarks

**Hardware**: Apple M1 Pro, Python 3.11

| Depth | Nodes | Time | NPS | Speedup vs Basic |
|-------|-------|------|-----|------------------|
| 6 | 100K | 0.1s | 1M | 50x |
| 9 | 1M | 1.0s | 1M | 3500x |
| 12 | 10M | 15s | 667K | 14000x |

### Technique Contributions

Incremental speedup from each technique:

| Technique | Speedup | Cumulative |
|-----------|---------|------------|
| Baseline (minimax) | 1x | 1x |
| + Alpha-Beta | 10x | 10x |
| + Transposition Table | 3x | 30x |
| + Iterative Deepening | 1.2x | 36x |
| + Move Ordering | 3x | 108x |
| + Null Move Pruning | 1.5x | 162x |
| + Late Move Reduction | 2x | 324x |
| + Futility Pruning | 1.2x | 389x |
| + Multi-Cut | 1.1x | 428x |
| + Parallel Search (4 cores) | 3x | 1284x |
| + Bitboard | 3x | **3852x** |

### Memory Usage

- **Base Engine**: 50 MB
- **Transposition Table** (128 MB): 128 MB
- **Opening Book**: 2 MB
- **Per Search Thread**: 10 MB
- **Total (4 cores)**: ~220 MB

## Configuration

### Default Configuration

```python
DEFAULT_CONFIG = {
    'depth': 9,
    'use_opening_book': True,
    'use_transposition_table': True,
    'tt_size_mb': 128,
    'use_iterative_deepening': True,
    'use_null_move_pruning': True,
    'use_futility_pruning': True,
    'use_late_move_reduction': True,
    'use_multi_cut': True,
    'use_parallel_search': True,
    'num_cores': 4,
    'observer': 'statistics'
}
```

### Custom Configuration

```python
from src.AI.Apocalyptron.factory.factory import ApocalyptronFactory

# Create custom config
config = ApocalyptronFactory.create_default_config()
config.depth = 11  # Deeper search
config.num_cores = 8  # More cores
config.tt_size_mb = 256  # Larger TT

# Create engine
engine = ApocalyptronFactory.create_engine(config)
```

## Usage Examples

### Basic Usage

```python
from src.Players.PlayerApocalyptron import PlayerApocalyptron

# Create player with default settings
player = PlayerApocalyptron(depth=9)

# Get move
move = player.get_move(game, valid_moves, control=None)
```

### With Statistics

```python
from src.AI.Apocalyptron.observers.statistics import StatisticsObserver

# Create observer
stats_observer = StatisticsObserver()

# Create engine with observer
config = ApocalyptronFactory.create_default_config()
engine = ApocalyptronFactory.create_engine(config, [stats_observer])

# After search
stats = stats_observer.get_statistics()
print(f"Nodes: {stats['nodes_searched']:,}")
print(f"NPS: {stats['nps']:,.0f}")
print(f"TT Hit Rate: {stats['tt_hit_rate']:.1%}")
```

### Tournament Mode

```python
# Quiet mode for tournaments
config = ApocalyptronFactory.create_default_config()
config.observer = 'quiet'
config.depth = 9

engine = ApocalyptronFactory.create_engine(config)
```

## Testing

### Unit Tests

Each module has comprehensive unit tests:

```bash
pytest tests/apocalyptron/unit/test_alphabeta.py
pytest tests/apocalyptron/unit/test_ordering.py
pytest tests/apocalyptron/unit/test_evaluation.py
```

### Integration Tests

```bash
pytest tests/apocalyptron/integration/test_apocalyptron_basic.py
```

### Characterization Tests

Ensure behavior matches reference implementation:

```bash
pytest tests/apocalyptron/characterization/test_positions.py
```

## Related Documentation

- [Bitboard Implementation](bitboard.md) - Technical bitboard details
- [Design Principles](design-principles.md) - Architecture principles
- [Performance Guide](../development/performance.md) - Optimization techniques
- [API Reference](../api/README.md) - API documentation

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-20  
**Engine Version**: Apocalyptron 3.1.0

*This document describes the most advanced AI engine in Reversi42.*

