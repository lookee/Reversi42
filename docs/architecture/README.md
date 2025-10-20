# Architecture Documentation

Comprehensive architecture documentation for Reversi42.

## Overview

Reversi42 is built with a modular, layered architecture that separates concerns and enables extensibility. The system follows SOLID principles and employs various design patterns for maintainability and testability.

## Quick Navigation

### Core Architecture
- [**System Overview**](system-overview.md) - High-level architecture
- [**Design Principles**](design-principles.md) - Guiding principles and patterns
- [**Module Structure**](module-structure.md) - Component organization
- [**Data Flow**](data-flow.md) - How data moves through the system

### Component Documentation
- [**Game Engine**](game-engine.md) - Core game logic and bitboard implementation
- [**AI System**](ai-system.md) - AI architecture and algorithms
- [**UI Layer**](ui-layer.md) - View system and MVP pattern
- [**Player System**](player-system.md) - Player abstractions and implementations

### Technical Deep Dives
- [**Bitboard Implementation**](bitboard.md) - Low-level bitboard details
- [**Search Algorithms**](search-algorithms.md) - AI search implementation
- [**Opening Book System**](opening-book.md) - Opening database architecture
- [**Event System**](event-system.md) - Event bus and pub/sub pattern

### Design Decisions
- [**ADR Index**](adr/README.md) - Architecture Decision Records
- [**Technology Choices**](technology-choices.md) - Why Python, Pygame, etc.
- [**Performance Optimizations**](performance.md) - How we achieve 100x+ speedup
- [**Concurrency Model**](concurrency.md) - Threading and multiprocessing

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                 │
│  (Pygame UI, Terminal UI, Headless)             │
└─────────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────────┐
│            Application Layer                    │
│  (Game Control, Player Management, Events)      │
└─────────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────────┐
│              Domain Layer                       │
│  (Game Logic, AI Engine, Opening Book)          │
└─────────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────────┐
│           Infrastructure Layer                  │
│  (Persistence, Configuration, Utilities)        │
└─────────────────────────────────────────────────┘
```

### Layer Responsibilities

1. **Presentation Layer**
   - User interface rendering
   - Input handling
   - View-specific logic
   - No business logic

2. **Application Layer**
   - Coordinates user actions
   - Manages game flow
   - Player turn management
   - Event distribution

3. **Domain Layer**
   - Core game rules
   - AI algorithms
   - Opening book logic
   - Pure business logic

4. **Infrastructure Layer**
   - File I/O operations
   - Configuration management
   - External dependencies
   - Cross-cutting concerns

## Key Design Patterns

### 1. Model-View-Presenter (MVP)

**Used in**: Board and UI system

```
┌─────────┐      ┌──────────────┐      ┌──────┐
│  Model  │◄─────┤  Presenter   │─────►│ View │
└─────────┘      └──────────────┘      └──────┘
```

**Benefits**:
- Separation of concerns
- Testable business logic in presenter
- View is passive and easily replaceable

### 2. Strategy Pattern

**Used in**: Player system, AI evaluators

```python
class Player(ABC):
    @abstractmethod
    def get_move(self, game, moves, control):
        pass

# Different strategies
class HumanPlayer(Player): ...
class AIPlayer(Player): ...
class RandomPlayer(Player): ...
```

**Benefits**:
- Easy to add new player types
- Runtime strategy selection
- Decoupled algorithms

### 3. Factory Pattern

**Used in**: Player creation, View creation, AI configuration

```python
class PlayerFactory:
    @staticmethod
    def create_player(player_type: str, **config) -> Player:
        if player_type == "human":
            return HumanPlayer(**config)
        elif player_type == "ai":
            return AIPlayer(**config)
        # ...
```

**Benefits**:
- Centralized object creation
- Configuration management
- Dependency injection

### 4. Observer Pattern

**Used in**: Event system, UI updates

```python
class EventBus:
    def subscribe(self, event_type: str, callback: Callable):
        ...
    
    def publish(self, event_type: str, data: Any):
        ...
```

**Benefits**:
- Loose coupling
- Dynamic subscriptions
- Scalable notifications

### 5. Immutable Data Pattern

**Used in**: BitboardGame

```python
class BitboardGame:
    def make_move(self, position: int) -> 'BitboardGame':
        """Returns NEW game state, doesn't modify self."""
        return BitboardGame(new_black, new_white, -self.current_player)
```

**Benefits**:
- Thread safety
- Easy undo/redo
- Functional programming style

## Component Diagram

```
┌────────────────────────────────────────────────────────┐
│                    reversi42.py                        │
│                  (Main Entry Point)                    │
└───────────────────────┬────────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
  ┌─────────▼──────┐     ┌─────────▼──────────┐
  │   UI System    │     │   Player System     │
  │  (View Layer)  │     │  (Controllers)      │
  └────────┬───────┘     └─────────┬───────────┘
           │                       │
           │        ┌──────────────┴─────────────┐
           │        │                            │
    ┌──────▼────────▼──────┐          ┌─────────▼─────────┐
    │   BoardControl (MVP) │          │   Player Types    │
    │    Controller        │          │   (AI, Human)     │
    └──────┬───────────────┘          └─────────┬─────────┘
           │                                     │
    ┌──────▼────────┐                  ┌────────▼─────────┐
    │  BoardModel   │                  │   AI Engine      │
    │  (Game State) │                  │  (Apocalyptron)  │
    └──────┬────────┘                  └────────┬─────────┘
           │                                    │
           │        ┌───────────────────────────┘
           │        │
    ┌──────▼────────▼──────┐
    │   BitboardGame        │
    │  (Core Engine)        │
    └───────────────────────┘
```

## Data Flow Examples

### 1. Human Move Flow

```
User Click
    │
    ▼
Pygame View (handles click)
    │
    ▼
BoardControl (validates move)
    │
    ▼
BoardModel (updates game state)
    │
    ▼
BitboardGame (applies move)
    │
    ▼
Event Bus (publishes move_made event)
    │
    ▼
View Updates (all subscribed views)
```

### 2. AI Move Flow

```
AI Turn Start
    │
    ▼
Player.get_move()
    │
    ▼
Apocalyptron Engine
    │
    ├─→ Opening Book (try lookup)
    │   │
    │   ├─→ Found → Return move
    │   │
    │   └─→ Not found → Continue search
    │
    ├─→ Iterative Deepening Search
    │   │
    │   ├─→ Alpha-Beta Pruning
    │   ├─→ Transposition Table Lookup
    │   ├─→ Move Ordering
    │   ├─→ Null Move Pruning
    │   └─→ Evaluation Function
    │
    └─→ Return best move
```

### 3. Save Game Flow

```
User selects "Save"
    │
    ▼
UI triggers save event
    │
    ▼
Game I/O Module
    │
    ├─→ Serialize game state
    ├─→ Format as XOT
    └─→ Write to file
    │
    ▼
Confirmation to user
```

## Module Dependencies

```
ui/ (Presentation)
 ├─ depends on: Board/ (Application)
 └─ depends on: widgets/ (UI Components)

Board/ (Application)
 ├─ depends on: Reversi/ (Domain)
 └─ depends on: Players/ (Domain)

Players/ (Domain)
 ├─ depends on: Reversi/ (Domain)
 ├─ depends on: AI/ (Domain)
 └─ depends on: domain/knowledge/ (Domain)

AI/ (Domain)
 ├─ depends on: Reversi/ (Domain)
 └─ NO external dependencies

infrastructure/ (Infrastructure)
 └─ depends on: Reversi/ (Domain)
```

### Dependency Rules

1. **Dependencies flow downward** - Upper layers depend on lower layers
2. **Domain layer is independent** - No dependencies on infrastructure or UI
3. **Infrastructure is a plugin** - Implements interfaces defined by domain
4. **No circular dependencies** - Strictly enforced

## Configuration Management

### Configuration Hierarchy

```
Default Config (Code)
    ↓
User Config File (.reversi42rc)
    ↓
Environment Variables (REVERSI42_*)
    ↓
Command-line Arguments (--flag)
    ↓
Runtime Configuration (UI settings)
```

Higher levels override lower levels.

### Configuration Files

```
~/.reversi42/
├── config.json          # User preferences
├── opening_book/        # Custom opening books
├── saves/               # Saved games
└── logs/                # Application logs
```

## Testing Strategy

### Test Pyramid

```
        ┌─────────────┐
        │  End-to-End │  (Few, slow, high value)
        └─────────────┘
      ┌─────────────────┐
      │   Integration   │  (Some, medium speed)
      └─────────────────┘
    ┌───────────────────────┐
    │      Unit Tests       │  (Many, fast, focused)
    └───────────────────────┘
```

### Test Organization

- **Unit Tests**: `tests/unit/` - Test individual functions/classes
- **Integration Tests**: `tests/integration/` - Test component interactions
- **Characterization Tests**: `tests/characterization/` - Verify AI behavior
- **Performance Tests**: `tests/performance/` - Benchmark critical paths

## Performance Architecture

### Critical Performance Paths

1. **Move Generation** (50-100ns)
   - Bitboard representation
   - Bit manipulation
   - Pre-computed masks

2. **AI Search** (0.1-1s per move)
   - Alpha-beta pruning
   - Transposition tables
   - Move ordering
   - Parallel search

3. **Rendering** (16ms target for 60 FPS)
   - Dirty rectangle optimization
   - Sprite caching
   - Event batching

### Performance Monitoring

```python
# Built-in profiling support
from src.AI.Apocalyptron.observers.statistics import StatisticsObserver

observer = StatisticsObserver()
engine.add_observer(observer)
# ... run AI ...
print(observer.get_statistics())
```

## Security Considerations

### Threat Model

1. **Malicious Game Files**
   - XOT files are plain text, parsed safely
   - Path traversal prevention
   - Input validation

2. **Resource Exhaustion**
   - AI depth limits
   - Time limits
   - Memory bounds

3. **Code Injection**
   - No eval() or exec()
   - Safe JSON parsing
   - Validated configuration

### Security Layers

- Input validation at presentation layer
- Business logic validation at domain layer
- Resource limits in infrastructure layer

## Extensibility Points

### Adding New Features

1. **New Player Type**:
   - Inherit from `Player`
   - Implement `get_move()`
   - Register in `PlayerFactory`

2. **New View Type**:
   - Inherit from `AbstractBoardView`
   - Implement required methods
   - Register in `ViewFactory`

3. **New AI Evaluator**:
   - Inherit from `Evaluator`
   - Implement `evaluate()`
   - Add to evaluator registry

4. **New Opening Book Format**:
   - Implement `OpeningBookLoader`
   - Register loader
   - Update configuration

## Future Architecture

### Planned Improvements

1. **Plugin System** - Load external AI engines
2. **Network Play** - Client-server architecture
3. **Database Backend** - Store game history
4. **Web Interface** - Browser-based UI
5. **Mobile Support** - Touch-friendly UI

### Migration Paths

All architecture changes will:
- Maintain backward compatibility (where possible)
- Provide migration tools
- Document breaking changes
- Follow deprecation policy

## Related Documentation

- [API Reference](../api/) - Detailed API documentation
- [Design Principles](design-principles.md) - Guiding principles
- [ADR Index](adr/README.md) - Architecture decisions
- [Contributing Guide](../../CONTRIBUTING.md) - How to contribute

---

For questions about architecture:
- Open a [GitHub Discussion](https://github.com/lucaamore/reversi42/discussions)
- Check [ADRs](adr/README.md) for context on decisions
- Refer to code comments for implementation details

