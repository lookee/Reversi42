# Enhanced Opening Book

Versione avanzata dell'opening book con sistema di scoring sofisticato e filtri parametrici.

## 🎯 Caratteristiche

### Retrocompatibilità ✅
- Estende `OpeningBook` - può essere usato come drop-in replacement
- Mantiene tutti i metodi esistenti
- Aggiunge nuove funzionalità senza breaking changes

### Novità Rispetto a OpeningBook

#### 1. Sistema di Scoring Multi-Criterio
```python
score = advantage_score + variety_score + safety_bonus

# Dove:
# - advantage_score = numeric_value × advantage_weight
# - variety_score = log(1 + continuations) × variety_weight  
# - safety_bonus = safety_weight (se advantage = "=")
```

#### 2. Filtri Parametrici
- **score_threshold**: Soglia minima per accettare mosse (default: 0.0)
- **use_average_threshold**: Usa media come soglia dinamica (default: True)
- **only_evaluated_openings**: Filtra aperture senza advantage data

#### 3. Modalità di Selezione
- `BEST_SCORE`: Migliore punteggio assoluto (default)
- `WEIGHTED_RANDOM`: Random pesato per score
- `VARIETY_FIRST`: Preferisce più continuazioni
- `SAFE_FIRST`: Preferisce mosse bilanciate (=)
- `AGGRESSIVE`: Preferisce vantaggi forti (w++, w+)

#### 4. Valutazione Dettagliata
Ogni mossa viene valutata con `MoveEvaluation`:
- `score`: Punteggio finale
- `advantage_score`: Da advantage
- `variety_score`: Da varietà
- `count_continuations`: Numero continuazioni
- `has_evaluation`: Se ha dati advantage
- `advantage_symbol`: Simbolo (=, w, w+, etc.)
- `is_above_threshold`: Se supera soglia

## 📖 Utilizzo

### Esempio Base

```python
from domain.knowledge import get_enhanced_opening_book, SelectionMode

# Crea enhanced book con default
book = get_enhanced_opening_book()

# Oppure con configurazione custom
book = get_enhanced_opening_book(
    score_threshold=0.1,          # Solo mosse con score > 0.1
    use_average_threshold=True,   # Usa media come soglia dinamica
    selection_mode=SelectionMode.BEST_SCORE
)

# Ottieni mosse rankkate
game_history = "C4e3"
moves = game.get_move_list()

ranked_moves = book.get_ranked_moves(game_history, moves)
for eval_result in ranked_moves:
    print(f"{eval_result.move}: score={eval_result.score:.3f}")

# Seleziona migliore mossa
best_move = book.select_best_move(game_history, moves)
```

### Esempio con Filtri

```python
# Solo mosse > 0 con media
book = get_enhanced_opening_book(
    score_threshold=0.0,
    use_average_threshold=True
)

# Mosse filtrate
filtered = book.get_filtered_moves(game_history, moves)
print(f"Filtered to {len(filtered)} moves (above threshold)")

# Statistiche dettagliate
stats = book.get_move_statistics(game_history, moves)
print(f"Best move: {stats['best_move']}")
print(f"Best score: {stats['best_score']:.3f}")
print(f"Average score: {stats['average_score']:.3f}")
```

### Esempio con Modalità Diverse

```python
# Modalità aggressiva
book_aggressive = get_enhanced_opening_book(
    selection_mode=SelectionMode.AGGRESSIVE
)
move = book_aggressive.select_best_move(game_history, moves)

# Modalità varietà
book_variety = get_enhanced_opening_book(
    selection_mode=SelectionMode.VARIETY_FIRST
)
move = book_variety.select_best_move(game_history, moves)

# Random pesato (per evitare determinismo)
book_random = get_enhanced_opening_book(
    selection_mode=SelectionMode.WEIGHTED_RANDOM
)
move = book_random.select_best_move(game_history, moves)
```

## 🔧 Integrazione con Giocatori

### Player Template (NON utilizzato attualmente)

```python
from domain.knowledge import get_enhanced_opening_book, SelectionMode

class PlayerEnhancedBook(Player):
    """
    Player che usa EnhancedOpeningBook.
    
    TEMPLATE - non utilizzato da giocatori esistenti.
    """
    
    def __init__(self, depth=6, selection_mode=SelectionMode.BEST_SCORE):
        Player.__init__(self)
        self.depth = depth
        self.name = f"EnhancedBook-{depth}"
        
        # Usa enhanced book
        self.opening_book = get_enhanced_opening_book(
            score_threshold=0.0,
            use_average_threshold=True,
            selection_mode=selection_mode
        )
        
        # Engine per mosse fuori dal book
        from AI.Apocalyptron import ApocalyptronEngine
        self.engine = ApocalyptronEngine(...)
    
    def get_move(self, game, moves, control):
        # Prova opening book enhanced
        book_move = self.opening_book.select_best_move(
            game.history,
            moves,
            mode=None  # Usa self.selection_mode
        )
        
        if book_move:
            # Converti stringa a Move object
            col = ord(book_move[0]) - ord('A') + 1
            row = int(book_move[1])
            move = Move(col, row)
            
            if game.valid_move(move):
                return move
        
        # Fallback a engine
        return self.engine.get_best_move(...)
```

## 📊 Parametri Configurabili

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `score_threshold` | 0.0 | Soglia minima score (solo mosse >= threshold) |
| `use_average_threshold` | True | Usa media come soglia dinamica |
| `selection_mode` | BEST_SCORE | Modalità selezione mossa |
| `advantage_weight` | 0.2 | Peso per advantage evaluation |
| `variety_weight` | 0.1 | Peso per varietà continuazioni |
| `safety_weight` | 0.05 | Bonus per mosse sicure (=) |
| `only_evaluated_openings` | True | Filtra aperture senza advantage |

## 🧪 Testing

```python
# Test basic functionality
from domain.knowledge import get_enhanced_opening_book

book = get_enhanced_opening_book()
assert book is not None
assert isinstance(book, EnhancedOpeningBook)

# Test retrocompatibilità
moves = book.get_book_moves("C4")  # Metodo di OpeningBook
assert moves is not None  # Funziona!

# Test nuove funzionalità
from Reversi.Game import Game
game = Game(8)
valid_moves = game.get_move_list()

ranked = book.get_ranked_moves("", valid_moves)
assert len(ranked) > 0
assert ranked[0].score >= ranked[-1].score  # Ordinate per score
```

## 🚀 Future Enhancements

Possibili estensioni future (non implementate):
- [ ] Machine learning per score optimization
- [ ] Statistiche win rate per apertura
- [ ] Database SQLite per aperture
- [ ] Import da PGN/SGF
- [ ] Export configurazioni custom
- [ ] A/B testing tra modalità diverse
- [ ] Adaptive selection basata su opponent

## 📝 Note

**IMPORTANTE**: Questa versione è disponibile ma **NON utilizzata da nessun giocatore esistente**.

È stata creata per:
- Future implementazioni
- Testing di strategie avanzate
- Backward compatibility garantita
- Estensibilità senza modificare il core

Per usarla, crea un nuovo giocatore che la importi esplicitamente.

