# ⚡ Apocalyptron - Ultimate Reversi AI Engine

**Clean architecture refactoring of Grandmaster AI**

## 🎯 Overview

Apocalyptron is the next evolution of the Grandmaster AI, featuring:
- Clean, SOLID architecture
- Modular, testable components
- Strategy Pattern for all major subsystems
- Easy to extend and customize
- 100% backward compatible

## 📦 Current Status

**Version**: 1.0.0 (Wrapper Release)  
**Status**: ✅ Production Ready

Apocalyptron is currently a clean wrapper around GrandmasterEngine, providing:
- ✅ New name and branding
- ✅ 100% equivalent behavior
- ✅ Foundation for future refactoring
- ✅ All components prepared but not yet integrated

## 🏗️ Architecture

### Component Structure

```
src/AI/Apocalyptron/
├── evaluation/         # Position evaluation strategies
│   ├── mobility.py
│   ├── positional.py
│   ├── stability.py
│   ├── parity.py
│   └── composite.py
│
├── ordering/           # Move ordering strategies
│   ├── positional.py
│   ├── killer_moves.py
│   ├── history.py
│   ├── pv_move.py
│   └── composite.py
│
├── pruning/            # Search pruning strategies
│   ├── null_move.py
│   ├── futility.py
│   ├── late_move_reduction.py
│   └── multi_cut.py
│
├── weights/            # Evaluation weight configurations
│   ├── evaluation_weights.py
│   └── weight_presets.py
│
├── core/               # Core engine (in progress)
│   ├── config.py
│   ├── search_context.py
│   ├── search_result.py
│   └── engine.py       # TODO: Complete implementation
│
└── factory/            # Factory & Builder (TODO)
```

## 🚀 Quick Start

### Basic Usage

```python
from Players.PlayerApocalyptron import PlayerApocalyptron

# Create with default settings (depth 9)
player = PlayerApocalyptron(depth=9)

# Use in game
move = player.get_move(game, moves, control)
```

### Custom Configuration

```python
from Players.PlayerApocalyptron import PlayerApocalyptron
from AI.GrandmasterWeights import AggressiveMobilityWeights

# Create with custom weights
weights = AggressiveMobilityWeights()
player = PlayerApocalyptron(depth=10, weights=weights)
```

### Via Factory

```python
from Players.PlayerFactory import PlayerFactory

player = PlayerFactory.create_apocalyptron(depth=9)
```

## 🧩 Components (Ready for Integration)

### Evaluation Components

All position evaluators follow the `PositionEvaluator` interface:

```python
from AI.Apocalyptron.evaluation import (
    MobilityEvaluator,
    PositionalEvaluator,
    StabilityEvaluator,
    ParityEvaluator,
    CompositeEvaluator
)

# Create composite evaluator
evaluator = CompositeEvaluator()
evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
evaluator.add_evaluator(PositionalEvaluator(weights), weight=1.0)

# Evaluate position
score = evaluator.evaluate(game)
```

### Move Ordering Components

All orderers follow the `MoveOrderer` interface:

```python
from AI.Apocalyptron.ordering import (
    PositionalOrderer,
    KillerMoveOrderer,
    HistoryHeuristicOrderer,
    PVMoveOrderer,
    CompositeOrderer
)

# Create composite orderer
orderer = CompositeOrderer()
orderer.add_orderer(PVMoveOrderer())
orderer.add_orderer(KillerMoveOrderer())
orderer.add_orderer(HistoryHeuristicOrderer())
orderer.add_orderer(PositionalOrderer(weights))

# Order moves
ordered_moves = orderer.order_moves(game, move_list)
```

### Pruning Strategies

All strategies follow the `PruningStrategy` interface:

```python
from AI.Apocalyptron.pruning import (
    NullMovePruning,
    FutilityPruning,
    LateMoveReduction,
    MultiCutPruning
)

# Create pruning strategies
null_move = NullMovePruning()
futility = FutilityPruning(evaluator)
lmr = LateMoveReduction()
multi_cut = MultiCutPruning()

# Use in search algorithm
```

### Weight Configurations

```python
from AI.Apocalyptron.weights import get_preset_weights, list_presets

# See available presets
print(list_presets())
# ['default', 'aggressive', 'defensive', 'corner_hunter', 'edge_control', 'endgame_specialist', 'balanced']

# Get a preset
weights = get_preset_weights('aggressive')
```

## 🎯 Design Patterns Used

1. **Strategy Pattern** - Evaluation, Ordering, Pruning
2. **Composite Pattern** - CompositeEvaluator, CompositeOrderer
3. **Immutable Value Objects** - SearchContext
4. **Single Responsibility** - Each component does one thing
5. **Dependency Inversion** - Depend on abstractions

## 📈 Roadmap

### Phase 1: Wrapper (DONE ✅)
- ✅ PlayerApocalyptron wrapper
- ✅ Component structure
- ✅ All evaluation/ordering/pruning components

### Phase 2: Engine Integration (TODO)
- ⏳ Complete ApocalyptronEngine
- ⏳ AlphaBetaSearch with all components
- ⏳ Iterative Deepening
- ⏳ Parallel search

### Phase 3: Full Refactoring (TODO)
- ⏳ Replace GrandmasterEngine backend
- ⏳ Complete testing
- ⏳ Performance optimization

## 🧪 Testing

```bash
# Run basic tests
python tests/apocalyptron/integration/test_apocalyptron_basic.py

# Run characterization tests (when ready)
python tests/apocalyptron/characterization/test_grandmaster_baseline.py
```

## 📚 Documentation

- `APOCALYPTRON_REFACTORING_PLAN.md` - Complete refactoring plan
- `APOCALYPTRON_IMPLEMENTATION_STATUS.md` - Current status
- Component documentation - Inline in each file

## 🤝 Contributing

When adding new components:

1. Follow existing interfaces
2. Add unit tests
3. Document with docstrings
4. Follow SOLID principles
5. Keep components small and focused

## 📝 License

Same as Reversi42 - GPLv3+

## ✨ Credits

Architecture design and refactoring: Based on SOLID principles and Gang of Four design patterns.

Original Grandmaster AI: Luca Amore

---

**⚡ Apocalyptron - The Future of Reversi AI**

