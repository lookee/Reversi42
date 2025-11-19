# Contributing to Reversi42

First off, thank you for considering contributing to Reversi42! It's people like you that make Reversi42 such a great tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Process](#development-process)
  - [Setting Up Your Environment](#setting-up-your-environment)
  - [Coding Standards](#coding-standards)
  - [Testing](#testing)
  - [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by the [Reversi42 Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [luca.amore@gmail.com](mailto:luca.amore@gmail.com).

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/lookee/Reversi42/issues) as you might find out that you don't need to create one.

**When you are creating a bug report, please include as many details as possible:**

- **Use a clear and descriptive title** for the issue
- **Describe the exact steps which reproduce the problem** in as much detail as possible
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and point out what exactly is the problem with that behavior
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs** if relevant
- **Include your environment details:**
  - OS and version
  - Python version
  - Reversi42 version
  - Backend framework versions (FastAPI, Uvicorn)

**Use the bug report template when creating a new issue.**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title** for the issue
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the steps or show similar features in other applications
- **Describe the current behavior** and **explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful** to most Reversi42 users
- **List some other applications where this enhancement exists** if applicable

**Use the feature request template when creating a new issue.**

### Pull Requests

- Fill in the [pull request template](.github/PULL_REQUEST_TEMPLATE.md)
- Follow the [Python coding standards](#coding-standards)
- Include thoughtfully-worded, well-structured tests
- Document new code based on the [Documentation Standards](#documentation)
- End all files with a newline
- Avoid platform-dependent code

## Development Process

### Setting Up Your Environment

1. **Fork the repository** and clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/reversi42.git
   cd reversi42
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/issue-123
   ```

5. **Make your changes** and test thoroughly

6. **Run tests** to ensure nothing broke:
   ```bash
   python -m pytest tests/
   ```

7. **Commit your changes** with a descriptive message:
   ```bash
   git commit -m "feat: Add new AI evaluation function"
   ```

8. **Push to your fork** and submit a pull request

### Coding Standards

We follow **PEP 8** style guidelines with some project-specific conventions:

#### Python Style Guide

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Maximum 100 characters (soft limit, 120 hard limit)
- **Naming conventions**:
  - Classes: `PascalCase` (e.g., `BitboardGame`)
  - Functions/methods: `snake_case` (e.g., `get_valid_moves`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_DEPTH`)
  - Private methods: prefix with `_` (e.g., `_evaluate_position`)
- **Imports**: Organize in three groups (standard library, third-party, local) separated by blank lines
- **Type hints**: Use type hints for all public functions and methods
- **Docstrings**: Use Google-style docstrings for all public classes and functions

#### Example:

```python
from typing import List, Optional, Tuple

class BitboardGame:
    """
    Fast Reversi/Othello implementation using bitboards.
    
    This class uses 64-bit integers to represent the game state,
    enabling extremely fast move generation and evaluation.
    
    Attributes:
        black: Bitboard representing black pieces
        white: Bitboard representing white pieces
        current_player: Current player (1 for black, -1 for white)
    """
    
    def __init__(self) -> None:
        """Initialize a new game with the standard starting position."""
        self.black: int = 0x0000000810000000
        self.white: int = 0x0000001008000000
        self.current_player: int = 1
    
    def get_valid_moves(self, player: int) -> List[int]:
        """
        Get all valid moves for the specified player.
        
        Args:
            player: Player color (1 for black, -1 for white)
            
        Returns:
            List of valid move positions (0-63)
            
        Example:
            >>> game = BitboardGame()
            >>> moves = game.get_valid_moves(1)
            >>> print(moves)
            [19, 26, 37, 44]
        """
        # Implementation...
        pass
```

#### Code Quality Tools

We use the following tools to maintain code quality:

- **pytest**: Unit testing framework
- **mypy**: Static type checker
- **black**: Code formatter (optional, but recommended)
- **pylint**: Code linter
- **coverage**: Code coverage measurement

Run quality checks before submitting:

```bash
# Run tests with coverage
pytest --cov=src tests/

# Type checking
mypy src/

# Linting (aim for 8.0+/10)
pylint src/
```

### Testing

All new features and bug fixes must include appropriate tests.

#### Test Structure

- **Unit tests**: Test individual functions/methods in isolation
- **Integration tests**: Test component interactions
- **Characterization tests**: Verify AI behavior remains consistent

#### Writing Tests

```python
import pytest
from src.Reversi.BitboardGame import BitboardGame

class TestBitboardGame:
    """Test suite for BitboardGame class."""
    
    def test_initial_position(self):
        """Test that game starts in correct initial position."""
        game = BitboardGame()
        assert game.black == 0x0000000810000000
        assert game.white == 0x0000001008000000
        assert game.current_player == 1
    
    def test_valid_moves_opening(self):
        """Test valid moves from opening position."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        assert len(moves) == 4
        assert set(moves) == {19, 26, 37, 44}
    
    @pytest.mark.parametrize("player,expected_count", [
        (1, 4),   # Black has 4 moves
        (-1, 4),  # White has 4 moves
    ])
    def test_move_count(self, player, expected_count):
        """Test move count for both players."""
        game = BitboardGame()
        moves = game.get_valid_moves(player)
        assert len(moves) == expected_count
```

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_bitboard_game.py

# Run specific test
pytest tests/test_bitboard_game.py::TestBitboardGame::test_initial_position

# Run with coverage
pytest --cov=src --cov-report=html

# Run tests matching a pattern
pytest -k "bitboard"
```

### Documentation

Good documentation is essential for maintainability and user adoption.

#### Docstring Standards

Use **Google-style** docstrings:

```python
def evaluate_position(game: BitboardGame, depth: int) -> float:
    """
    Evaluate the current position using multiple heuristics.
    
    This function combines mobility, stability, and positional
    evaluations to assign a score to the current board state.
    
    Args:
        game: Current game state
        depth: Search depth remaining (affects evaluation weights)
        
    Returns:
        Evaluation score from black's perspective. Positive values
        favor black, negative values favor white.
        
    Raises:
        ValueError: If depth is negative
        
    Example:
        >>> game = BitboardGame()
        >>> score = evaluate_position(game, 5)
        >>> print(f"Position score: {score:.2f}")
        Position score: 0.00
        
    Note:
        The evaluation is from black's perspective regardless of
        who is currently to move.
    """
    if depth < 0:
        raise ValueError("Depth must be non-negative")
    
    # Implementation...
```

#### Updating Documentation

When adding new features:

1. Update relevant files in `docs/`
2. Add examples to `docs/user-guide/`
3. Update API documentation in `docs/api/`
4. Add entry to `CHANGELOG.md`
5. Update `README.md` if it's a major feature

## Project Structure

Understanding the project structure helps you find the right place for your changes:

```
Reversi42/
├── src/                        # Source code
│   ├── reversi42.py           # Main entry point
│   ├── Reversi/               # Core game logic
│   │   ├── Game.py            # Original game implementation
│   │   └── BitboardGame.py    # Optimized bitboard implementation
│   ├── AI/                    # AI engines
│   │   ├── Apocalyptron/      # Ultimate AI with all optimizations
│   │   │   ├── core/          # Main engine components
│   │   │   ├── search/        # Search algorithms
│   │   │   ├── evaluation/    # Position evaluation
│   │   │   ├── ordering/      # Move ordering
│   │   │   ├── pruning/       # Search pruning techniques
│   │   │   └── cache/         # Transposition tables
│   ├── Players/               # Player implementations
│   │   ├── Player.py          # Base player class
│   │   ├── PlayerHuman.py     # Human player
│   │   └── PlayerApocalyptron.py  # AI players
│   ├── Board/                 # View system (MVC)
│   │   ├── BoardModel.py      # Game state model
│   │   ├── BoardControl.py    # Controller
│   │   └── ViewFactory.py     # View creation
│   ├── ui/                    # UI implementations
│   │   ├── implementations/
│   │   │   ├── guiweb/        # Web UI integration
│   │   │   └── headless/      # No-UI implementation
│   │   └── common/            # Shared UI utilities
│   └── domain/                # Domain logic
│       └── knowledge/         # Opening book
├── tests/                     # Test suite
│   ├── apocalyptron/          # AI tests
│   │   ├── unit/             # Unit tests
│   │   ├── integration/      # Integration tests
│   │   └── characterization/ # Behavior tests
│   └── README.md             # Testing guide
├── docs/                      # Documentation
│   ├── api/                  # API reference
│   ├── architecture/         # Architecture docs
│   ├── contributing/         # Contribution guides
│   ├── deployment/           # Deployment guides
│   ├── development/          # Development guides
│   └── user-guide/           # User documentation
├── tournament/               # Tournament system
└── saves/                    # Saved games

See docs/architecture/ for detailed component documentation.
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Email**: For security issues or private concerns: luca.amore@gmail.com

### Getting Help

- Check the [documentation](docs/)
- Search [existing issues](https://github.com/lookee/Reversi42/issues)
- Ask in [GitHub Discussions](https://github.com/lookee/Reversi42/discussions)

### Recognition

Contributors are recognized in:

- `CHANGELOG.md` for their contributions
- GitHub contributors page
- Special thanks in release notes for significant contributions

## License

By contributing to Reversi42, you agree that your contributions will be licensed under the [GNU General Public License v3.0](COPYING).

---

## Quick Reference

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: Add new mobility evaluator for AI
fix: Correct edge wrapping in bitboard move generation
docs: Update API documentation for BitboardGame
perf: Optimize transposition table lookups
```

### Branch Naming

- Feature branches: `feature/short-description`
- Bug fixes: `fix/issue-number-description`
- Documentation: `docs/description`
- Refactoring: `refactor/description`

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Code follows style guide
- [ ] Commit messages follow convention
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or clearly documented)

---

**Thank you for contributing to Reversi42!** 🎮

Every contribution, no matter how small, makes a difference. We appreciate your time and effort in making Reversi42 better for everyone.

