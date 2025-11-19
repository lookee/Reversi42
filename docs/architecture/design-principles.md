# Design Principles

Core architectural and design principles guiding Reversi42's development.

## Philosophy

Reversi42 is built on the principle that **code should be fast, maintainable, and elegant**. We believe that performance and clean architecture are not mutually exclusive, and that good design makes systems both faster and easier to understand.

## Core Principles

### 1. Separation of Concerns

**Principle**: Each component should have a single, well-defined responsibility.

**Application**:
- **UI Layer**: Only handles presentation and user interaction
- **Application Layer**: Only coordinates between UI and domain
- **Domain Layer**: Only implements business logic
- **Infrastructure Layer**: Only handles external concerns

**Benefits**:
- Easy to test components in isolation
- Changes to one layer don't affect others
- Clear boundaries and interfaces
- Better code organization

**Example**:
```python
# Good: Clear separation
class BitboardGame:  # Domain - game rules only
    def make_move(self, position: int) -> 'BitboardGame':
        # Pure game logic
        
class BoardControl:  # Application - coordination only
    def handle_move(self, position: int):
        # Coordinate between model and view
        
class WebGUIView:  # Presentation - UI only
    def render_board(self, game: BitboardGame):
        # Only rendering logic
```

### 2. Immutability Where Possible

**Principle**: Prefer immutable data structures to prevent unexpected side effects.

**Application**:
- Game state is immutable
- All operations return new instances
- No in-place modifications
- Functional programming style

**Benefits**:
- Thread-safe by default
- Easy to reason about
- Simple undo/redo
- No side effects

**Example**:
```python
# Immutable game state
class BitboardGame:
    def make_move(self, position: int) -> 'BitboardGame':
        # Returns NEW game state, doesn't modify self
        new_black, new_white = self._calculate_new_state(position)
        return BitboardGame(new_black, new_white, -self.current_player)
```

### 3. Dependency Inversion

**Principle**: Depend on abstractions, not concretions. High-level modules should not depend on low-level modules.

**Application**:
- Define interfaces (abstract base classes)
- Depend on interfaces, not implementations
- Inject dependencies
- Inversion of control

**Benefits**:
- Easy to swap implementations
- Better testability (mock interfaces)
- Loose coupling
- Flexibility

**Example**:
```python
# Abstract interface
class Player(ABC):
    @abstractmethod
    def get_move(self, game, moves, control):
        pass

# High-level code depends on interface
class BoardControl:
    def __init__(self, black_player: Player, white_player: Player):
        self.black = black_player  # Could be ANY Player implementation
        self.white = white_player
```

### 4. Composition Over Inheritance

**Principle**: Favor object composition over class inheritance for code reuse.

**Application**:
- Use composition to combine behaviors
- Shallow inheritance hierarchies
- Interface-based design
- Strategy and decorator patterns

**Benefits**:
- More flexible than inheritance
- Easier to test
- No fragile base class problem
- Runtime behavior changes

**Example**:
```python
# Composition: AI composed of evaluators, not inherited
class Apocalyptron:
    def __init__(self):
        self.evaluators = [
            MobilityEvaluator(),
            StabilityEvaluator(),
            PositionalEvaluator()
        ]
        self.search = AlphaBetaSearch()
        self.opening_book = OpeningBook()
```

### 5. Single Responsibility Principle (SOLID-S)

**Principle**: A class should have only one reason to change.

**Application**:
- Each class does one thing well
- Clear naming reflects responsibility
- Small, focused classes
- Easy to understand and test

**Benefits**:
- High cohesion
- Low coupling
- Easy to maintain
- Clear purpose

**Example**:
```python
# Each class has single responsibility
class ZobristHash:  # Only hashing
    def hash_position(self, game): ...

class TranspositionTable:  # Only caching
    def store(self, hash, value): ...
    def lookup(self, hash): ...

class AlphaBetaSearch:  # Only searching
    def search(self, game, depth): ...
```

### 6. Open/Closed Principle (SOLID-O)

**Principle**: Software entities should be open for extension but closed for modification.

**Application**:
- Use interfaces for extensibility
- Factory pattern for object creation
- Strategy pattern for algorithms
- Plugin architecture (planned)

**Benefits**:
- Add features without changing existing code
- Reduced risk of breaking existing functionality
- Better stability
- Easier to extend

**Example**:
```python
# Open for extension via new Player implementations
# Closed for modification - Player interface doesn't change
class NewCustomPlayer(Player):
    def get_move(self, game, moves, control):
        # New behavior without modifying Player interface
        return custom_algorithm(game, moves)
```

### 7. Performance Through Smart Design

**Principle**: Achieve performance through algorithmic improvements and smart data structures, not premature optimization.

**Application**:
- Bitboards: O(1) operations instead of O(n²)
- Transposition tables: Avoid redundant calculations
- Move ordering: Reduce search tree size
- Immutability: Zero-cost copies (just pointers)

**Benefits**:
- 50-14000x speedup through design
- Maintainable high-performance code
- Algorithmic improvements compound
- Profile-guided optimization

**Example**:
```python
# Bitboard design enables O(1) operations
class BitboardGame:
    # Two 64-bit ints instead of 64-element array
    black: int  # Each bit = one square
    white: int
    
    def get_valid_moves(self) -> int:
        # Single bitwise operations, O(1)
        # vs. O(64) array iteration
        return self._compute_moves_bitwise()
```

### 8. Explicit Over Implicit

**Principle**: Code should be explicit about what it does. Avoid hidden behavior and magic.

**Application**:
- Type hints everywhere
- Clear method names
- No hidden side effects
- Explicit error handling
- No "magic" values

**Benefits**:
- Easy to understand
- IDE support (autocomplete, type checking)
- Catches errors early
- Self-documenting

**Example**:
```python
# Explicit types and behavior
def evaluate_position(
    game: BitboardGame,
    depth: int,
    alpha: float,
    beta: float
) -> Tuple[float, Optional[int]]:
    """
    Explicit return type, no surprises.
    Clear parameters with types.
    """
    if game.is_game_over():
        return self._terminal_evaluation(game), None
    # Clear, explicit logic
```

### 9. Fail Fast

**Principle**: Detect and report errors as early as possible.

**Application**:
- Validate inputs at boundaries
- Use type hints and mypy
- Raise exceptions for invalid states
- Assertions for invariants
- No silent failures

**Benefits**:
- Bugs caught early
- Clear error messages
- Easier debugging
- More robust code

**Example**:
```python
def make_move(self, position: int) -> 'BitboardGame':
    if not 0 <= position < 64:
        raise ValueError(f"Position must be 0-63, got {position}")
    if not self.is_valid_move(position, self.current_player):
        raise ValueError(f"Invalid move at position {position}")
    # Fail fast - don't continue with invalid state
```

### 10. Test-Driven Design

**Principle**: Design for testability from the start.

**Application**:
- Dependency injection
- Small, focused functions
- Pure functions where possible
- Clear interfaces
- Mockable dependencies

**Benefits**:
- High test coverage possible
- Tests are easy to write
- Bugs caught early
- Refactoring confidence

**Example**:
```python
# Testable design with dependency injection
class Apocalyptron:
    def __init__(
        self,
        search: SearchAlgorithm,
        evaluator: Evaluator,
        opening_book: Optional[OpeningBook] = None
    ):
        # Dependencies injected - easy to mock in tests
        self.search = search
        self.evaluator = evaluator
        self.opening_book = opening_book
```

## Design Patterns Used

### Creational Patterns

#### Factory Pattern
**Where**: PlayerFactory, ViewFactory, ApocalyptronFactory  
**Why**: Centralized object creation, configuration management  
**Benefit**: Easy to add new types, consistent creation

#### Builder Pattern
**Where**: ApocalyptronBuilder  
**Why**: Complex object construction with many options  
**Benefit**: Fluent API, step-by-step construction

### Structural Patterns

#### Adapter Pattern
**Where**: View implementations (WebGUI, Headless)  
**Why**: Adapt different UI frameworks to common interface  
**Benefit**: Pluggable views, easy to add new ones

#### Composite Pattern
**Where**: Evaluators (CompositeEvaluator), Move ordering  
**Why**: Combine multiple strategies into one  
**Benefit**: Flexible combination of behaviors

#### Facade Pattern
**Where**: Apocalyptron engine  
**Why**: Simple interface to complex subsystem  
**Benefit**: Easy to use, hides complexity

### Behavioral Patterns

#### Strategy Pattern
**Where**: Player types, Evaluators, Search algorithms  
**Why**: Interchangeable algorithms  
**Benefit**: Runtime algorithm selection

#### Observer Pattern
**Where**: Event bus, AI observers, Statistics  
**Why**: Decouple publishers from subscribers  
**Benefit**: Loose coupling, dynamic subscriptions

#### Template Method Pattern
**Where**: Abstract search algorithms  
**Why**: Define algorithm skeleton, subclasses fill details  
**Benefit**: Code reuse, consistent structure

#### Iterator Pattern
**Where**: Move generation  
**Why**: Sequential access to elements  
**Benefit**: Simple, standard interface

## Code Quality Principles

### Readability

**Principle**: Code is read more than written. Optimize for readability.

**Guidelines**:
- Clear, descriptive names
- Short functions (<50 lines)
- One level of abstraction per function
- Comments explain WHY, not WHAT
- Consistent formatting

### Simplicity

**Principle**: The simplest solution that works is usually the best.

**Guidelines**:
- YAGNI (You Aren't Gonna Need It)
- No premature optimization
- No over-engineering
- Direct, straightforward code

### DRY (Don't Repeat Yourself)

**Principle**: Every piece of knowledge should have a single representation.

**Guidelines**:
- Extract common code to functions
- Use inheritance/composition for shared behavior
- Constants for magic numbers
- Configuration for environment-specific values

### KISS (Keep It Simple, Stupid)

**Principle**: Simplicity should be a key goal. Avoid unnecessary complexity.

**Guidelines**:
- Simple algorithms first
- Complexity only when necessary
- Profile before optimizing
- Clear over clever

## Performance Principles

### Measure First

**Principle**: Never optimize without measuring.

**Guidelines**:
- Profile before optimizing
- Use cProfile, memory_profiler
- Benchmark critical paths
- Document performance characteristics

### Optimize Algorithms, Not Code

**Principle**: Better algorithms beat micro-optimizations.

**Examples**:
- Bitboards: O(1) vs O(n²)
- Transposition tables: Memoization
- Alpha-beta: Prune search tree
- Move ordering: Better pruning

### Cache Wisely

**Principle**: Cache expensive computations, but be aware of trade-offs.

**Guidelines**:
- Transposition tables for AI search
- Opening book for instant lookups
- Evaluate cache hit rates
- Monitor memory usage

### Parallelize When Beneficial

**Principle**: Use multiple cores for CPU-bound tasks.

**Guidelines**:
- Parallel search for AI
- Tournaments run games in parallel
- Avoid for I/O-bound tasks
- Overhead vs. benefit analysis

## Documentation Principles

### Self-Documenting Code

**Principle**: Code should be understandable without comments.

**Guidelines**:
- Descriptive names
- Clear structure
- Type hints
- Small functions

### Comment WHY, Not WHAT

**Principle**: Comments explain rationale, not implementation.

**Good Comment**:
```python
# Use null move pruning to reduce search tree
# Safe because zugzwang is rare in Reversi
if depth > 2 and not in_check:
    try_null_move()
```

**Bad Comment**:
```python
# Set x to 0
x = 0
```

### API Documentation

**Principle**: All public APIs must have comprehensive docstrings.

**Guidelines**:
- Google-style docstrings
- Parameters, returns, raises
- Examples for complex APIs
- Type hints always

## Error Handling Principles

### Exceptions for Exceptional Cases

**Principle**: Use exceptions for errors, not control flow.

**Guidelines**:
- Raise exceptions for invalid states
- Use specific exception types
- Clear error messages
- Don't catch and ignore

### Validate at Boundaries

**Principle**: Validate all external inputs.

**Guidelines**:
- User input validation
- File input validation
- API parameter validation
- Clear error messages

### Fail Safely

**Principle**: When something goes wrong, fail in a safe, recoverable way.

**Guidelines**:
- Graceful degradation
- Meaningful error messages
- Clean resource management
- State consistency maintained

## Security Principles

### Defense in Depth

**Principle**: Multiple layers of security.

**Guidelines**:
- Input validation
- Output sanitization
- Principle of least privilege
- No eval() or exec()

### Secure by Default

**Principle**: Secure defaults, opt-in for less secure options.

**Guidelines**:
- Safe defaults
- Explicit unsafe operations
- Clear security warnings
- Audit security-sensitive code

## Conclusion

These principles guide all architectural and implementation decisions in Reversi42. They are not rigid rules but guidelines that help us build a system that is:

- **Fast**: Through smart design, not just optimization
- **Maintainable**: Through clear structure and patterns
- **Extensible**: Through interfaces and loose coupling
- **Robust**: Through validation and error handling
- **Testable**: Through dependency injection and pure functions
- **Understandable**: Through clear code and documentation

When in doubt, **simplicity and clarity win**.

## Related Documentation

- [System Overview](system-overview.md) - High-level architecture
- [Best Practices](../development/best-practices.md) - Implementation guidelines
- [Code Style](../development/code-style.md) - Coding standards
- [ADR Index](adr/README.md) - Specific architectural decisions

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-20  

*These principles evolve as we learn. Suggestions welcome via [GitHub Discussions](https://github.com/lookee/Reversi42/discussions).*

