# Nuova Architettura Players/AI - Guida per Sviluppatori

**Versione**: 3.2.0  
**Tipo**: Developer Guide

---

## 🎯 Overview

Reversi42 ha una nuova architettura modulare per Players e AI basata su **Design Patterns Enterprise**.

### Obiettivi
- ✅ Eliminare duplicazione codice
- ✅ Separare Player da Engine
- ✅ Permettere configurazioni infinite
- ✅ Facilitare testing
- ✅ Mantenere backward compatibility

---

## 🏗️ Architettura

### Separazione Player/Engine

**Player** = Interfaccia di gioco (chi gioca)  
**Engine** = Logica AI (come decide la mossa)

```python
# Player NON sa nulla dell'algoritmo
class AIPlayer:
    def __init__(self, engine):  # ← Engine INJECTED
        self.engine = engine
    
    def get_move(self, game, moves, control):
        return self.engine.get_best_move(game, depth)
```

---

## 📖 Guida Rapida

### Creare un AI Semplice

```python
from AI.factory.engine_builder import EngineBuilder
from Players.ai.ai_player import AIPlayer

# 1. Crea engine
engine = EngineBuilder().use_minimax().build()

# 2. Crea player
player = AIPlayer(engine=engine, depth=6)
```

### Creare un AI Avanzato

```python
# Grandmaster con tutte le features
engine = (EngineBuilder()
    .use_grandmaster()
    .with_advanced_evaluator()
    .with_opening_book()
    .with_parallel_search(threads=8)
    .with_transposition_table(size_mb=256)
    .with_endgame_solver()
    .build())

player = AIPlayer(engine=engine, depth=9, name="Master")
```

### Usare i Presets

```python
from Players.factory.player_presets import PlayerPresets

# Quick creation
beginner = PlayerPresets.create_beginner(depth=3)
grandmaster = PlayerPresets.create_grandmaster(depth=9)
```

---

## 🔧 Creare un Nuovo Engine

### Step 1: Implementare Interface

```python
# AI/implementations/custom/my_engine.py
from AI.base.engine import Engine
from AI.factory.engine_registry import EngineRegistry

@EngineRegistry.register('myengine', EngineMetadata(
    name='myengine',
    display_name='My Custom Engine',
    description='My awesome AI',
    strength='strong'
))
class MyEngine(Engine):
    def __init__(self, config=None):
        super().__init__("MyEngine", config)
    
    def get_best_move(self, game, depth, **kwargs):
        # Your algorithm here
        moves = game.get_move_list()
        # ... AI logic ...
        return best_move
    
    def evaluate_position(self, game):
        # Your evaluation here
        return score
```

### Step 2: Usare Nuovo Engine

```python
# Immediatamente disponibile via Registry
from AI.factory.engine_registry import EngineRegistry
engine = EngineRegistry.get_engine('myengine')

# O via Builder
from AI.factory.engine_builder import EngineBuilder
engine = EngineBuilder().use_engine(MyEngine).build()
```

---

## 🎨 Design Patterns Spiegati

### 1. Strategy Pattern (Engines Intercambiabili)

```python
# Cambiare algorithm a runtime
player = AIPlayer(engine=MinimaxEngine(), depth=6)
player.set_engine(BitboardEngine())  # Switch!
```

### 2. Dependency Injection (Testabilità)

```python
# Mock per testing
class MockEngine(Engine):
    def get_best_move(self, game, depth):
        return game.get_move_list()[0]

# Test con mock
player = AIPlayer(engine=MockEngine())
assert player.get_move(game, moves, control) == moves[0]
```

### 3. Builder Pattern (Configurazione Fluente)

```python
engine = (EngineBuilder()
    .use_bitboard()          # Step 1
    .with_opening_book()     # Step 2
    .with_parallel_search()  # Step 3
    .build())                # Build
```

### 4. Decorator Pattern (Features Componibili)

```python
# Wrappers che aggiungono funzionalità
base = BitboardEngine()
with_book = OpeningBookDecorator(base)
with_parallel = ParallelSearchDecorator(with_book, threads=8)
# Features stacked!
```

### 5. Registry Pattern (Auto-discovery)

```python
# Engines si auto-registrano
@EngineRegistry.register('myengine')
class MyEngine(Engine):
    pass

# Auto-discovery
EngineRegistry.list_engines()  # {'myengine': metadata}
```

---

## 🔄 Migration Guide (Old → New)

### Da AIPlayerBitboard

```python
# OLD
from Players.AIPlayerBitboard import AIPlayerBitboard
player = AIPlayerBitboard(deep=6)

# NEW
from AI.factory.engine_builder import EngineBuilder
from Players.ai.ai_player import AIPlayer

engine = EngineBuilder().use_bitboard().build()
player = AIPlayer(engine=engine, depth=6)

# O più semplice con Presets
from Players.factory.player_presets import PlayerPresets
player = PlayerPresets.create_bitboard_blitz(depth=6)
```

### Da AIPlayerGrandmaster

```python
# OLD
from Players.AIPlayerGrandmaster import AIPlayerGrandmaster
player = AIPlayerGrandmaster(deep=9)

# NEW
from Players.factory.player_presets import PlayerPresets
player = PlayerPresets.create_grandmaster(depth=9)
```

---

## 📋 API Reference

### EngineBuilder

```python
# Engine Selection
.use_minimax()
.use_bitboard()
.use_grandmaster()
.use_random()
.use_greedy()
.use_heuristic()

# Evaluator Selection
.with_standard_evaluator()
.with_advanced_evaluator()
.with_greedy_evaluator()
.with_positional_evaluator()

# Features (Decorators)
.with_opening_book(path=None)
.with_parallel_search(threads=4)
.with_transposition_table(size_mb=64)
.with_endgame_solver(depth_trigger=12)

# Build
.build() -> Engine
```

### PlayerPresets

```python
PlayerPresets.create_beginner(depth=3)
PlayerPresets.create_intermediate(depth=6)
PlayerPresets.create_advanced(depth=8)
PlayerPresets.create_grandmaster(depth=9)
PlayerPresets.create_alpha_beta(depth=6)
PlayerPresets.create_opening_scholar(depth=6)
PlayerPresets.create_bitboard_blitz(depth=6)
PlayerPresets.create_oracle(depth=7)
PlayerPresets.create_parallel_oracle(depth=7, threads=4)
PlayerPresets.create_random()
PlayerPresets.create_greedy()
PlayerPresets.create_heuristic(depth=4)
```

### PlayerFactoryV2

```python
# Backward compatible API
PlayerFactoryV2.create_player(player_type, **kwargs)
PlayerFactoryV2.create_ai_player(engine_type, difficulty)
```

---

## ✨ Prossimi Passi

### Future Enhancements
1. Implementare MTD(f) algorithm
2. Aggiungere Neural Network engine
3. Implementare Monte Carlo Tree Search
4. Aggiungere Iterative Deepening decorator
5. Implementare Killer Moves decorator

### Come Contribuire
1. Implementare `Engine` interface
2. Registrare con `@EngineRegistry.register`
3. Testare con AIPlayer
4. Submit pull request!

---

**Documento Completo - Architettura Enterprise-Level! 🏆**

