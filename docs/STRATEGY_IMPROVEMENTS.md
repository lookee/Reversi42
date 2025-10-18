# Miglioramenti Strategici per Parallel Oracle

## 🎯 Analisi Strategia Attuale

### ✅ Cosa Già Funziona Bene

1. **Bitboard Representation** - Ultra veloce (50-100x)
2. **Alpha-Beta Pruning** - Riduzione albero di ricerca
3. **Transposition Table** - Evita ricalcoli con Zobrist hashing
4. **Opening Book** - 57 aperture professionali (instant response)
5. **Parallel Search** - 2-5x speedup su root level

### 🔧 Cosa Si Può Migliorare

#### Problemi Attuali:

1. **No Move Ordering** ❌
   ```python
   # Attualmente
   for move in move_list:  # Ordine casuale
       game.move(move)
       value = -self.alphabeta(...)
   ```
   **Impatto**: Pruning inefficiente (50-70% dei nodi)

2. **Evaluation Semplice** ⚠️
   ```python
   # Attualmente
   return mobility * 3 + corner_score + edge_score
   ```
   **Manca**:
   - Stability (pezzi stabili)
   - Parity (chi fa l'ultima mossa)
   - X-squares (caselle vicine agli angoli)
   - Frontier discs (pezzi esposti)

3. **No Iterative Deepening** ❌
   - Cerca direttamente a depth 8
   - Non usa info da depth 6-7 per ordinare mosse
   
4. **No Endgame Solver** ❌
   - A depth 8, con 10 mosse rimaste, potrebbe risolvere perfettamente
   - Ultime 15-20 mosse risolvibili in secondi

---

## 🚀 Miglioramenti Proposti (Ordinati per Impatto)

### 1. 🏆 Move Ordering (ALTO IMPATTO - ~2-4x speedup)

**Principio**: Cerca prima le mosse più promettenti → più cutoff → meno nodi

```python
def order_moves(self, game, move_list):
    """Order moves by expected strength"""
    
    # Priorità:
    # 1. Corners (massima priorità)
    # 2. Edges stable
    # 3. Mosse che riducono mobilità avversario
    # 4. Mosse centrali
    # 5. Altre
    
    corner_mask = 0x8100000000000081
    stable_edge_mask = 0x7E0000000000007E  # Bordi senza X-squares
    
    scored_moves = []
    for move in move_list:
        score = 0
        bit = move.get_bit_position()
        
        # Corner: +1000
        if (1 << bit) & corner_mask:
            score += 1000
        
        # Stable edge: +500  
        elif (1 << bit) & stable_edge_mask:
            score += 500
        
        # Center 4x4: +100
        elif 27 <= bit <= 36 and bit not in [27, 28, 35, 36]:
            score += 100
        
        # Check mobility reduction
        game.move(move)
        opponent_mobility = len(game.get_move_list())
        game.undo_move()
        score -= opponent_mobility * 10  # Meno mosse per avversario = meglio
        
        scored_moves.append((score, move))
    
    # Ordina per score decrescente
    scored_moves.sort(reverse=True, key=lambda x: x[0])
    return [move for _, move in scored_moves]
```

**Speedup Atteso**: 2-4x (più cutoff, meno nodi esplorati)

---

### 2. 🎯 Iterative Deepening (MEDIO IMPATTO - ~1.5-2x speedup + bonus)

**Principio**: Cerca depth 1, 2, 3... fino a target. Usa risultati precedenti per ordinare mosse.

```python
def iterative_deepening(self, game, max_depth):
    """Iterative deepening with move ordering from previous iteration"""
    
    best_move = None
    best_moves_history = []  # Migliori mosse da iterazioni precedenti
    
    for current_depth in range(1, max_depth + 1):
        # Ordina mosse usando info da depth precedente
        move_list = game.get_move_list()
        
        if current_depth > 1 and best_moves_history:
            # Cerca prima le mosse che erano migliori a depth-1
            ordered_moves = []
            for move in best_moves_history:
                if move in move_list:
                    ordered_moves.append(move)
            # Aggiungi le altre
            for move in move_list:
                if move not in ordered_moves:
                    ordered_moves.append(move)
            move_list = ordered_moves
        
        # Cerca a current_depth
        best_value = -INFINITY
        temp_best = None
        
        for move in move_list:
            game.move(move)
            value = -self.alphabeta(game, current_depth - 1, -INFINITY, -best_value)
            game.undo_move()
            
            if value > best_value:
                best_value = value
                temp_best = move
        
        best_move = temp_best
        best_moves_history.insert(0, best_move)  # Aggiungi in testa
        
        print(f"  Depth {current_depth}: Best = {best_move} (value: {best_value})")
    
    return best_move
```

**Vantaggi**:
- ✅ Move ordering migliorato ad ogni depth
- ✅ Può essere interrotto (time management)
- ✅ Sempre ha una risposta (best move da depth precedente)

**Speedup**: ~1.5-2x (miglior ordering + early cutoff)

---

### 3. 🧠 Evaluation Function Avanzata (ALTO IMPATTO - Forza +30%)

**Principio**: Valuta posizione considerando più fattori strategici

```python
def evaluate_advanced(self, game):
    """Advanced evaluation with multiple strategic factors"""
    
    player, opponent = game._get_player_boards()
    piece_count = game.black_cnt + game.white_cnt
    
    # Phase detection
    if piece_count < 20:
        phase = 'opening'
    elif piece_count < 50:
        phase = 'midgame'
    else:
        phase = 'endgame'
    
    score = 0
    
    # 1. MOBILITY (critical in midgame)
    mobility = game._count_bits(game.get_valid_moves())
    game.pass_turn()
    opponent_mobility = game._count_bits(game.get_valid_moves())
    game.undo_move()
    
    if phase == 'midgame':
        score += (mobility - opponent_mobility) * 10
    else:
        score += (mobility - opponent_mobility) * 5
    
    # 2. CORNERS (always critical)
    corner_mask = 0x8100000000000081
    player_corners = game._count_bits(player & corner_mask)
    opponent_corners = game._count_bits(opponent & corner_mask)
    score += (player_corners - opponent_corners) * 100
    
    # 3. X-SQUARES (adjacent to corners - BAD if corner is empty)
    x_square_mask = 0x4200000000000042
    for corner_bit in [0, 7, 56, 63]:
        corner_occupied = ((player | opponent) >> corner_bit) & 1
        
        # X-square positions relative to corner
        x_bits = {
            0: 9,   # a1 → b2
            7: 14,  # h1 → g2
            56: 49, # a8 → b7
            63: 54  # h8 → g7
        }
        
        x_bit = x_bits[corner_bit]
        
        if not corner_occupied:
            # Corner empty - X-square is BAD
            if (player >> x_bit) & 1:
                score -= 50
            if (opponent >> x_bit) & 1:
                score += 50
    
    # 4. STABILITY (pieces that cannot be flipped)
    # Approximate: corners + edges adjacent to corners
    stable_mask = 0x8100000000000081  # Corners always stable
    player_stable = game._count_bits(player & stable_mask)
    opponent_stable = game._count_bits(opponent & stable_mask)
    score += (player_stable - opponent_stable) * 30
    
    # 5. FRONTIER DISCS (pieces with empty neighbors - bad in midgame)
    if phase == 'midgame':
        empty = ~(player | opponent) & 0xFFFFFFFFFFFFFFFF
        
        # Player frontier (has empty neighbor)
        player_frontier = 0
        for direction in [1, -1, 8, -8, 9, -9, 7, -7]:  # 8 directions
            if direction > 0:
                shifted = (player << direction) & 0xFFFFFFFFFFFFFFFF
            else:
                shifted = player >> -direction
            player_frontier |= (shifted & empty)
        
        player_frontier_count = game._count_bits(player_frontier)
        
        # Same for opponent
        opponent_frontier = 0
        for direction in [1, -1, 8, -8, 9, -9, 7, -7]:
            if direction > 0:
                shifted = (opponent << direction) & 0xFFFFFFFFFFFFFFFF
            else:
                shifted = opponent >> -direction
            opponent_frontier |= (shifted & empty)
        
        opponent_frontier_count = game._count_bits(opponent_frontier)
        
        # Fewer frontier discs is better in midgame
        score += (opponent_frontier_count - player_frontier_count) * 3
    
    # 6. PARITY (who makes last move)
    if phase == 'endgame':
        empty_count = 64 - piece_count
        # If we have parity (even number of empty squares), we make last move
        if empty_count % 2 == 0:
            score += 20  # Slight advantage
    
    # 7. PIECE COUNT (only in endgame)
    if phase == 'endgame':
        if game.turn == 'B':
            score += (game.black_cnt - game.white_cnt) * 15
        else:
            score += (game.white_cnt - game.black_cnt) * 15
    
    return score
```

**Improvement**: +30-40% win rate vs current evaluation

---

### 4. 🎲 Killer Move Heuristic (MEDIO IMPATTO - ~1.3-1.5x speedup)

**Principio**: Ricorda mosse che hanno causato beta cutoff a ogni depth

```python
def __init__(self):
    # ...existing...
    self.killer_moves = {}  # {depth: [move1, move2]}

def alphabeta(self, game, depth, alpha, beta):
    # ...existing checks...
    
    # Get moves
    move_list = game.get_move_list()
    
    # Order with killer moves first
    if depth in self.killer_moves:
        killers = self.killer_moves[depth]
        ordered = [m for m in killers if m in move_list]
        ordered += [m for m in move_list if m not in ordered]
        move_list = ordered
    
    # Search
    for move in move_list:
        game.move(move)
        value = -self.alphabeta(game, depth - 1, -beta, -alpha)
        game.undo_move()
        
        if value >= beta:
            # Killer move! Store it
            if depth not in self.killer_moves:
                self.killer_moves[depth] = []
            if move not in self.killer_moves[depth]:
                self.killer_moves[depth].insert(0, move)
                if len(self.killer_moves[depth]) > 2:
                    self.killer_moves[depth].pop()
            
            return beta
```

**Speedup**: ~1.3-1.5x (più cutoff)

---

### 5. 🏁 Perfect Endgame Solver (ALTO IMPATTO - Forza +50% in endgame)

**Principio**: Ultime 12-15 mosse → soluzione perfetta garantita

```python
def solve_endgame(self, game, max_depth=15):
    """Perfect solver for endgame positions"""
    
    empty_count = 64 - game.black_cnt - game.white_cnt
    
    # Only use if few enough empty squares
    if empty_count > max_depth:
        return None  # Too many moves, use heuristic
    
    # Solve perfectly with deep alpha-beta
    best_move = None
    best_value = -INFINITY
    
    for move in game.get_move_list():
        game.move(move)
        
        # Search to the end (no depth limit)
        value = -self._solve_to_end(game, -INFINITY, -best_value)
        
        game.undo_move()
        
        if value > best_value:
            best_value = value
            best_move = move
    
    return best_move, best_value

def _solve_to_end(self, game, alpha, beta):
    """Solve to game end (no depth limit)"""
    
    if game.is_finish():
        # Game over - return exact score
        if game.turn == 'B':
            return (game.black_cnt - game.white_cnt) * 100
        else:
            return (game.white_cnt - game.black_cnt) * 100
    
    move_list = game.get_move_list()
    
    if len(move_list) == 0:
        # Pass
        game.pass_turn()
        value = -self._solve_to_end(game, -beta, -alpha)
        game.undo_move()
        return value
    
    best_value = -INFINITY
    
    for move in move_list:
        game.move(move)
        value = -self._solve_to_end(game, -beta, -alpha)
        game.undo_move()
        
        if value > best_value:
            best_value = value
        if value > alpha:
            alpha = value
        if alpha >= beta:
            return beta
    
    return best_value
```

**Improvement**: Perfetto in endgame (win rate 95-100%)

---

### 6. 📊 Principal Variation Search (PVS) (MEDIO IMPATTO - ~1.5-2x)

**Principio**: Prima mossa con full window, altre con null window (verifica)

```python
def pvs(self, game, depth, alpha, beta):
    """Principal Variation Search (more efficient than plain alpha-beta)"""
    
    # ... transposition, terminal checks ...
    
    move_list = self.order_moves(game, game.get_move_list())
    best_value = -INFINITY
    is_first_move = True
    
    for move in move_list:
        game.move(move)
        
        if is_first_move:
            # Full window search for first move
            value = -self.pvs(game, depth - 1, -beta, -alpha)
            is_first_move = False
        else:
            # Null window search
            value = -self.pvs(game, depth - 1, -alpha - 1, -alpha)
            
            # Re-search if it's better than expected
            if alpha < value < beta:
                value = -self.pvs(game, depth - 1, -beta, -value)
        
        game.undo_move()
        
        if value > best_value:
            best_value = value
        if value > alpha:
            alpha = value
        if alpha >= beta:
            return beta
    
    return best_value
```

**Speedup**: ~1.5-2x (meno re-searches)

---

## 🎯 Piano di Implementazione

### Quick Wins (1-2 ore)

1. ✅ **Move Ordering Base**
   - Corner first
   - Edge second
   - Center third
   - **Speedup**: 2-3x
   - **Effort**: Basso

2. ✅ **Evaluation Migliorata**
   - Aggiungi X-squares penalty
   - Aggiungi stability
   - Aggiungi frontier discs
   - **Improvement**: +20-30%
   - **Effort**: Medio

### Medium Wins (2-4 ore)

3. ✅ **Killer Move Heuristic**
   - Memorizza 2 killer moves per depth
   - **Speedup**: 1.3-1.5x
   - **Effort**: Basso

4. ✅ **Iterative Deepening**
   - Search 1, 2, 3... fino a target
   - Usa PV da iterazione precedente
   - **Speedup**: 1.5-2x
   - **Effort**: Medio

### Advanced (4-8 ore)

5. ✅ **Perfect Endgame Solver**
   - Solve perfettamente ultime 12-15 mosse
   - **Improvement**: Win rate 95-100% in endgame
   - **Effort**: Alto

6. ✅ **Principal Variation Search**
   - Null window + re-search
   - **Speedup**: 1.5-2x
   - **Effort**: Alto

---

## 📊 Speedup Cumulativo Atteso

| Implementazione | Speedup | Strength | Totale vs Standard |
|-----------------|---------|----------|-------------------|
| **Attuale** | 1x | Base | 50-100x |
| + Move Ordering | 2.5x | +10% | 125-250x |
| + Eval Avanzata | 2.5x | +30% | 125-250x |
| + Killer Moves | 3.5x | +30% | 175-350x |
| + Iter. Deepening | 5x | +40% | 250-500x |
| + Endgame Solver | 5x | +60% | 250-500x |
| + PVS | 7-8x | +60% | **350-800x** 🚀 |

---

## 🏆 Raccomandazione Implementativa

### Phase 1: Quick Wins (IMPLEMENTA SUBITO)

```python
class ImprovedBitboardEngine(BitboardMinimaxEngine):
    def __init__(self):
        super().__init__()
        self.killer_moves = {}
    
    def order_moves(self, move_list, game):
        """Simple but effective move ordering"""
        # Order: Corners > Stable Edges > Mobility Reduction > Others
        # (codice sopra)
    
    def evaluate_bitboard(self, game):
        """Advanced evaluation"""
        # (codice sopra con X-squares, stability, frontier, parity)
    
    def alphabeta(self, game, depth, alpha, beta):
        # Add killer move ordering
        # (codice sopra)
```

**Effort**: 1-2 ore
**Benefit**: 3-4x speedup, +20-30% strength

### Phase 2: Endgame Mastery

```python
def get_best_move(self, game, depth):
    empty = 64 - game.black_cnt - game.white_cnt
    
    # Perfect endgame solver
    if empty <= 12:
        return self.solve_endgame(game)
    
    # Iterative deepening for midgame
    return self.iterative_deepening(game, depth)
```

**Effort**: 2-3 ore
**Benefit**: Perfect endgame, +40% overall

---

## 💡 Priorità Consigliate

### 1. Move Ordering (MASSIMA PRIORITÀ) 🏆
- **Effort**: 1 ora
- **Speedup**: 2-3x
- **ROI**: Altissimo

### 2. Evaluation Avanzata
- **Effort**: 1-2 ore
- **Strength**: +30%
- **ROI**: Alto

### 3. Killer Moves
- **Effort**: 30 min
- **Speedup**: 1.3x
- **ROI**: Ottimo

### 4. Endgame Solver
- **Effort**: 2-3 ore
- **Strength**: +50% in endgame
- **ROI**: Alto (endgame critico)

### 5. Iterative Deepening + PVS
- **Effort**: 3-4 ore
- **Speedup**: 2x
- **ROI**: Medio (più complesso)

---

## 🚀 Implementazione Immediata

Vuoi che implementi:

### Opzione A: Quick Win Package (1-2 ore)
- ✅ Move Ordering
- ✅ Killer Moves
- ✅ Evaluation Base migliorata
- **Speedup**: 3-4x
- **Strength**: +20%

### Opzione B: Complete Package (4-6 ore)
- ✅ Move Ordering
- ✅ Killer Moves
- ✅ Evaluation Avanzata
- ✅ Iterative Deepening
- ✅ Endgame Solver
- **Speedup**: 6-8x
- **Strength**: +60%

### Opzione C: Custom
Dimmi quali features vuoi e le implemento

---

## 📚 Riferimenti

### Papers Classici
- **Logistello** (Michael Buro) - Campione mondiale AI
  - Evaluation con pattern recognition
  - Endgame database
  
- **Edax** - Engine open source molto forte
  - Move ordering sofisticato
  - Perfect endgame solver

### Tecniche Avanzate
- **Multi-PV**: Mostra top 3 mosse
- **Aspiration Windows**: Finestre ristrette per depth successive
- **Quiescence Search**: Ricerca estesa per posizioni instabili
- **Selectivity**: Estendi search per mosse critiche

---

**Quale opzione preferisci? A, B, o Custom?** 🎯

