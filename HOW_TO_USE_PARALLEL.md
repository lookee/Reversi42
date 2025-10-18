# Come Usare la Parallelizzazione - Guida Pratica

## 🚀 Quick Start

### Opzione 1: Usa l'Engine Parallelo Direttamente

```python
from AI.ParallelBitboardMinimaxEngine import ParallelBitboardMinimaxEngine
from Reversi.BitboardGame import BitboardGame

# Crea engine con 4 workers (o auto-detect CPU cores)
engine = ParallelBitboardMinimaxEngine(num_workers=4)

# Usa normalmente
game = BitboardGame()
move = engine.get_best_move(game, depth=8)

# Chiudi quando finito
engine.close_pool()
```

### Opzione 2: Modifica AIPlayerBitboardBook

Aggiungi parallelizzazione in `src/Players/AIPlayerBitboardBook.py`:

```python
from AI.ParallelBitboardMinimaxEngine import ParallelBitboardMinimaxEngine

class AIPlayerBitboardBook(Player):
    def __init__(self, deep=6, show_book_options=True, use_parallel=True):
        # ... existing code ...
        
        # Usa engine parallelo se richiesto
        if use_parallel:
            self.bitboard_engine = ParallelBitboardMinimaxEngine()
        else:
            self.bitboard_engine = BitboardMinimaxEngine()
```

### Opzione 3: Player Parallelo Dedicato

Crea nuovo file `src/Players/AIPlayerBitboardBookParallel.py`:

```python
from Players.AIPlayerBitboardBook import AIPlayerBitboardBook
from AI.ParallelBitboardMinimaxEngine import ParallelBitboardMinimaxEngine

class AIPlayerBitboardBookParallel(AIPlayerBitboardBook):
    """
    Parallel version of The Oracle.
    Best for depth >= 7 on multi-core systems.
    """
    
    PLAYER_METADATA = {
        'display_name': 'The Parallel Oracle',
        'description': 'Multi-core AI - Parallel bitboard (2-4x) + Opening book',
        'enabled': True,
        'parameters': {
            'difficulty': {
                'type': int,
                'min': 7,
                'max': 12,
                'default': 8,
                'description': 'Search depth (7-12, parallel optimized)'
            },
            'num_workers': {
                'type': int,
                'min': 2,
                'max': 16,
                'default': None,  # Auto-detect
                'description': 'Worker processes (None = auto)'
            }
        }
    }
    
    def __init__(self, deep=8, num_workers=None, show_book_options=True):
        super().__init__(deep, show_book_options)
        
        # Replace with parallel engine
        self.bitboard_engine = ParallelBitboardMinimaxEngine(num_workers=num_workers)
        self.name = f"ParallelOracle{deep}"
        
        print(f"[{self.name}] Parallel engine active!")
        print(f"  • Workers: {self.bitboard_engine.num_workers}")
        print(f"  • Expected speedup: 2-4x at depth {deep}")
    
    def __del__(self):
        """Cleanup pool"""
        if hasattr(self, 'bitboard_engine'):
            self.bitboard_engine.close_pool()
```

## 🧪 Test Prima di Usare

```bash
# Test l'implementazione
python test_parallel_engine.py

# Output atteso:
# TEST 1 PASSED ✓
# TEST 2 PASSED ✓
# TEST 3 PASSED ✓ (Speedup: 2.5x)
```

## 📊 Quando Usare la Parallelizzazione

### ✅ USA PARALLELO se:

| Condizione | Valore | Motivo |
|------------|--------|--------|
| **Depth** | >= 7 | Abbastanza lavoro per ammortizzare overhead |
| **CPU Cores** | >= 4 | Parallelizzazione efficace |
| **Fase di gioco** | Mid/Late | Molte mosse da valutare (~8-15) |
| **Contesto** | Offline/Analisi | Overhead processo accettabile |

**Esempio**: Partita offline, depth 8, 8 cores → **Speedup 3-4x**

### ❌ NON USARE PARALLELO se:

| Condizione | Valore | Motivo |
|------------|--------|--------|
| **Depth** | <= 6 | Overhead > beneficio |
| **CPU Cores** | <= 2 | Non abbastanza parallelismo |
| **Fase di gioco** | Early + Book | Opening book instant (no search) |
| **Contesto** | UI interattiva | Overhead creazione processi |

**Esempio**: Apertura con book, depth 5 → **Sequential più veloce**

## 🎯 Configurazione Ottimale

### Per CPU a 4 Cores
```python
# Depth 7-8: Usa parallelo
engine = ParallelBitboardMinimaxEngine(num_workers=3)  # 1 core per sistema

# Depth <= 6: Usa sequenziale
engine = BitboardMinimaxEngine()
```

### Per CPU a 8+ Cores
```python
# Depth 7+: Usa parallelo con tutti i core
engine = ParallelBitboardMinimaxEngine(num_workers=7)  # Lascia 1 per sistema

# Speedup atteso: 4-6x
```

### Auto-Adaptive (Consigliato)
```python
# L'engine decide automaticamente
engine = ParallelBitboardMinimaxEngine()

# Logica interna:
# - Depth >= 7 AND moves >= 4 AND cores >= 2 → PARALLELO
# - Altrimenti → SEQUENZIALE
```

## 📈 Performance Attese

### Benchmark Depth 8, Mid-game (10 mosse)

| Setup | Time | Speedup | Note |
|-------|------|---------|------|
| Sequential Bitboard | 0.20s | 1x (baseline) | Già 50x vs standard |
| Parallel 2 cores | 0.12s | 1.7x | Modesto ma utile |
| **Parallel 4 cores** | 0.07s | **2.9x** | Sweet spot ✅ |
| **Parallel 8 cores** | 0.04s | **5.0x** | Ottimale ✅ |

### Speedup Complessivo vs Standard AI

| Setup | vs Standard AI |
|-------|----------------|
| Sequential Bitboard | 50-100x |
| **Parallel 4-core** | **150-300x** 🚀 |
| **Parallel 8-core** | **250-500x** 🚀🚀 |

## 🔧 Troubleshooting

### Problema: "Speedup minore dell'atteso"

**Causa**: Depth troppo basso o poche mosse

**Soluzione**: Usa depth >= 7 o aumenta il numero di mosse (mid/late game)

### Problema: "Process pool non si chiude"

**Causa**: Pool non chiamato `close()`

**Soluzione**:
```python
# Sempre cleanup
engine = ParallelBitboardMinimaxEngine()
try:
    move = engine.get_best_move(game, depth=8)
finally:
    engine.close_pool()

# Oppure usa context manager
# TODO: Implementare __enter__/__exit__
```

### Problema: "Overhead troppo alto su laptop"

**Causa**: CPU con pochi core o throttling

**Soluzione**: Usa engine sequenziale o riduci workers:
```python
engine = ParallelBitboardMinimaxEngine(num_workers=2)
```

## 💡 Best Practices

### 1. Riusa il Pool
```python
# ❌ BAD: Crea pool ad ogni mossa
for move in game:
    engine = ParallelBitboardMinimaxEngine()  # Overhead!
    best_move = engine.get_best_move(...)
    engine.close_pool()

# ✅ GOOD: Crea pool una volta
engine = ParallelBitboardMinimaxEngine()
for move in game:
    best_move = engine.get_best_move(...)  # Riusa pool
engine.close_pool()  # Cleanup alla fine
```

### 2. Adaptive Depth
```python
# Adatta depth in base alla fase di gioco
def get_adaptive_depth(turn_count):
    if turn_count < 20:
        return 6  # Early: usa sequential + book
    elif turn_count < 40:
        return 8  # Mid: usa parallel
    else:
        return 10  # Late: usa parallel con deep search
```

### 3. Profiling
```python
import time

# Misura entrambi
seq_engine = BitboardMinimaxEngine()
par_engine = ParallelBitboardMinimaxEngine()

start = time.perf_counter()
seq_move = seq_engine.get_best_move(game, depth=8)
seq_time = time.perf_counter() - start

start = time.perf_counter()
par_move = par_engine.get_best_move(game, depth=8)
par_time = time.perf_counter() - start

print(f"Speedup: {seq_time/par_time:.2f}x")
```

## 📝 Esempio Completo

```python
from Reversi.BitboardGame import BitboardGame
from AI.ParallelBitboardMinimaxEngine import ParallelBitboardMinimaxEngine

# Setup
game = BitboardGame()
engine = ParallelBitboardMinimaxEngine(num_workers=4)

# Play game
for i in range(20):
    moves = game.get_move_list()
    if not moves:
        game.pass_turn()
        continue
    
    # Get best move (engine auto-chooses parallel/sequential)
    depth = 8 if game.turn_cnt > 10 else 6
    move = engine.get_best_move(game, depth=depth, player_name=f"Move{i+1}")
    
    print(f"\nSelected: {move}")
    game.move(move)

# Cleanup
engine.close_pool()
print(f"\nGame finished! Score: B:{game.black_cnt} W:{game.white_cnt}")
```

## 🎓 Conclusione

**RACCOMANDAZIONE**:
- ✅ Usa **ParallelBitboardMinimaxEngine** per depth >= 7
- ✅ Lascia **auto-detect** per worker count
- ✅ Riusa il pool per l'intera partita
- ✅ Profila sul tuo sistema per confermare benefici

**Speedup realistico**:
- 4 cores: **2-3x** ulteriore
- 8 cores: **4-5x** ulteriore
- **Totale vs standard**: 150-500x 🚀

**Effort**: Minimo - basta cambiare l'engine!

