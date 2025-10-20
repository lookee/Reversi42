# Development Guide

Complete guide for developing Reversi42.

## Quick Links

- [**Getting Started**](getting-started.md) - Set up your dev environment
- [**Project Structure**](project-structure.md) - Understanding the codebase
- [**Testing Guide**](testing.md) - Writing and running tests
- [**Debugging**](debugging.md) - Debugging techniques and tools
- [**Performance**](performance.md) - Profiling and optimization
- [**Code Style**](code-style.md) - Coding standards
- [**Best Practices**](best-practices.md) - Development patterns

## Development Setup

### Prerequisites

- **Python 3.9+** (3.11 recommended)
- **pip** (latest version)
- **git**
- **virtualenv** (recommended)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/lucaamore/reversi42.git
cd reversi42

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests to verify setup
pytest tests/

# Run the game
./reversi42
```

## Development Workflow

### 1. Create a Branch

```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Or bug fix branch
git checkout -b fix/issue-123
```

### 2. Make Changes

Edit files following our [Code Style Guide](code-style.md).

### 3. Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_bitboard_game.py

# Run with coverage
pytest --cov=src --cov-report=html

# Watch mode (re-run on changes)
pytest-watch
```

### 4. Check Code Quality

```bash
# Type checking
mypy src/

# Linting
pylint src/

# Code formatting (optional)
black src/

# Check imports
isort src/ --check-only
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional message
git commit -m "feat: add new evaluation function"
```

See [Commit Message Guidelines](commit-messages.md).

### 6. Push and Create PR

```bash
# Push to your fork
git push origin feature/my-new-feature

# Create PR on GitHub
```

## Project Structure

```
reversi42/
├── src/                    # Source code
│   ├── reversi42.py       # Main entry point
│   ├── Reversi/           # Core game logic
│   │   ├── Game.py        # Original implementation
│   │   └── BitboardGame.py  # Bitboard implementation
│   ├── AI/                # AI engines
│   │   └── Apocalyptron/  # Ultimate AI
│   │       ├── core/      # Engine core
│   │       ├── search/    # Search algorithms
│   │       ├── evaluation/  # Position evaluation
│   │       ├── ordering/  # Move ordering
│   │       ├── pruning/   # Pruning techniques
│   │       └── cache/     # Transposition tables
│   ├── Players/           # Player implementations
│   │   ├── Player.py      # Base player class
│   │   ├── PlayerHuman.py  # Human player
│   │   └── PlayerApocalyptron.py  # AI players
│   ├── Board/             # MVC board system
│   │   ├── BoardModel.py  # Game state model
│   │   ├── BoardControl.py  # Controller
│   │   └── ViewFactory.py  # View creation
│   ├── ui/                # UI implementations
│   │   ├── implementations/
│   │   │   ├── pygame/    # Graphical UI
│   │   │   ├── terminal/  # Terminal UI
│   │   │   └── headless/  # No UI
│   │   └── widgets/       # UI components
│   ├── domain/            # Domain logic
│   │   └── knowledge/     # Opening book
│   ├── infrastructure/    # Infrastructure layer
│   │   └── persistence/   # Save/load
│   └── core/              # Configuration
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   ├── characterization/  # AI behavior tests
│   └── performance/      # Performance benchmarks
├── docs/                  # Documentation
├── tournament/            # Tournament system
├── build/                 # Build scripts
└── requirements.txt       # Dependencies
```

## Common Development Tasks

### Running the Game

```bash
# Default (Pygame GUI)
./reversi42

# Terminal mode
./reversi42 --view terminal

# Headless (for testing)
./reversi42 --view headless
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Specific test
pytest tests/unit/test_bitboard_game.py::TestBitboardGame::test_initial_position

# With coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Code Quality Checks

```bash
# Type checking
mypy src/

# Linting (aim for 8.0+/10)
pylint src/

# Format code
black src/

# Sort imports
isort src/

# All checks at once
./scripts/check.sh
```

### Debugging

```bash
# Run with debugger
python -m pdb src/reversi42.py

# Or use IDE debugger (VS Code, PyCharm)
```

See [Debugging Guide](debugging.md).

### Profiling

```python
# Profile AI performance
python -m cProfile -o profile.prof src/reversi42.py
python -m pstats profile.prof
```

See [Performance Guide](performance.md).

### Building Documentation

```bash
# Generate API docs (if using Sphinx)
cd docs/
make html

# View docs
open _build/html/index.html
```

## Development Tools

### Recommended IDE

- **VS Code** with extensions:
  - Python
  - Pylance
  - Python Test Explorer
  - GitLens

- **PyCharm** (Professional or Community)

### Useful Tools

- **pytest**: Testing framework
- **mypy**: Static type checker
- **pylint**: Code linter
- **black**: Code formatter
- **isort**: Import sorter
- **pytest-cov**: Coverage measurement
- **ipdb**: Interactive debugger
- **memory_profiler**: Memory profiling

### Installation

```bash
pip install -r requirements-dev.txt
```

## Testing

### Test Types

1. **Unit Tests** - Test individual functions/classes
2. **Integration Tests** - Test component interactions
3. **Characterization Tests** - Verify AI behavior
4. **Performance Tests** - Benchmark critical paths

### Writing Tests

```python
import pytest
from src.Reversi.BitboardGame import BitboardGame

class TestBitboardGame:
    def test_initial_position(self):
        """Test game starts in correct position."""
        game = BitboardGame()
        assert game.current_player == 1
        assert len(game.get_valid_moves(1)) == 4
    
    @pytest.mark.parametrize("position,expected", [
        (19, True),   # D3 is valid
        (0, False),   # A1 is not valid
    ])
    def test_valid_moves(self, position, expected):
        """Test move validation."""
        game = BitboardGame()
        assert game.is_valid_move(position, 1) == expected
```

See [Testing Guide](testing.md) for more.

## Debugging

### Common Issues

#### Import Errors

```bash
# Ensure you're in the project root
cd reversi42/

# Ensure virtual environment is activated
source venv/bin/activate

# Install in development mode
pip install -e .
```

#### Test Failures

```bash
# Run with verbose output
pytest -v

# Run with print statements
pytest -s

# Stop on first failure
pytest -x
```

#### Performance Issues

```bash
# Profile the code
python -m cProfile -o profile.prof src/reversi42.py

# Analyze profile
python -m pstats profile.prof
> sort cumtime
> stats 20
```

See [Debugging Guide](debugging.md) for more.

## Code Style

We follow **PEP 8** with these specifics:

- **Line length**: 100 characters (soft), 120 (hard)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Type hints**: Required for all public APIs
- **Docstrings**: Google-style

Example:

```python
from typing import List, Optional

def get_valid_moves(game: BitboardGame, player: int) -> List[int]:
    """
    Get all valid moves for the specified player.
    
    Args:
        game: Current game state
        player: Player color (1 or -1)
        
    Returns:
        List of valid move positions (0-63)
        
    Raises:
        ValueError: If player is invalid
    """
    if player not in (1, -1):
        raise ValueError("Player must be 1 or -1")
    
    return game.get_valid_moves(player)
```

See [Code Style Guide](code-style.md) for details.

## Performance Optimization

### Profiling

```bash
# CPU profiling
python -m cProfile -o profile.prof src/reversi42.py
python -m pstats profile.prof

# Memory profiling
python -m memory_profiler src/reversi42.py

# Line profiling
kernprof -l -v src/reversi42.py
```

### Optimization Guidelines

1. **Measure first** - Always profile before optimizing
2. **Focus on hot paths** - Optimize critical sections only
3. **Use appropriate data structures** - e.g., bitboards for game state
4. **Avoid premature optimization** - Readability first
5. **Test after optimizing** - Ensure correctness

See [Performance Guide](performance.md) for more.

## Best Practices

### Code Organization

- One class per file (usually)
- Group related functionality in modules
- Use clear, descriptive names
- Keep functions small and focused

### Error Handling

```python
# Good
def make_move(position: int) -> BitboardGame:
    if not self.is_valid_move(position, self.current_player):
        raise ValueError(f"Invalid move at position {position}")
    # ...

# Bad
def make_move(position: int) -> Optional[BitboardGame]:
    if not self.is_valid_move(position, self.current_player):
        return None  # Loses error information
    # ...
```

### Documentation

- Document **why**, not just **what**
- Include examples in docstrings
- Keep docs up-to-date with code
- Use type hints

### Testing

- Test edge cases
- Test error conditions
- Use descriptive test names
- One assertion per test (usually)

See [Best Practices Guide](best-practices.md) for more.

## Git Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring
- `perf/description` - Performance improvements

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new evaluation function
fix: correct edge wrapping in bitboard
docs: update API documentation
style: format code with black
refactor: extract common functionality
perf: optimize transposition table lookup
test: add tests for move generation
chore: update dependencies
```

See [Commit Message Guide](commit-messages.md).

## Resources

### Documentation

- [API Reference](../api/)
- [Architecture Guide](../architecture/)
- [User Guide](../user-guide/)
- [Contributing Guide](../../CONTRIBUTING.md)

### External Resources

- [Python Official Docs](https://docs.python.org/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)
- [Type Hints (mypy)](https://mypy.readthedocs.io/)

### Othello/Reversi Resources

- [World Othello Federation](https://www.worldothello.org/)
- [FNGO (Italian Federation)](http://www.fngo.it/)
- [Othello Strategy](https://en.wikipedia.org/wiki/Reversi#Strategy)

## Getting Help

- Check the [FAQ](faq.md)
- Ask in [GitHub Discussions](https://github.com/lucaamore/reversi42/discussions)
- Read existing code and tests
- Email: luca.amore@gmail.com

---

**Happy Coding!** 🚀

