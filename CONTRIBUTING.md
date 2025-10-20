# Contributing to Reversi42

First off, thank you for considering contributing to Reversi42! It's people like you that make Reversi42 such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [What We're Looking For](#what-were-looking-for)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by the [Reversi42 Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to luca.amore@gmail.com.

## What We're Looking For

We love contributions from the community! Here are some ways you can help:

- 🐛 **Bug Reports** - Found something broken? Let us know!
- ✨ **Feature Requests** - Have an idea? We'd love to hear it!
- 📝 **Documentation** - Help improve our docs
- 🧪 **Tests** - More coverage is always better
- 🤖 **AI Improvements** - New evaluation functions, search optimizations
- 🎨 **UI Enhancements** - Better graphics, themes, accessibility
- 🌐 **Internationalization** - Translate Reversi42 to other languages
- 📚 **Opening Book Expansion** - Add more professional opening sequences

## How to Contribute

### Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Reversi42.git
   cd Reversi42
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```
4. **Make your changes** and test them
5. **Commit your changes** with clear messages:
   ```bash
   git commit -m "Add awesome feature"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/my-awesome-feature
   ```
7. **Open a Pull Request** on GitHub

### First-Time Contributors

New to open source? Here are some good first issues to get started:
- Documentation improvements
- Adding unit tests
- Fixing typos
- Adding code comments
- Improving error messages

Look for issues tagged with `good first issue` or `help wanted`.

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Reversi42.git
cd Reversi42

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
./reversi42
```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test suite
python3 -m pytest tests/apocalyptron/unit/

# Run with coverage
python3 -m pytest --cov=src tests/
```

### Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

```
Reversi42/
├── src/              # Source code
│   ├── AI/           # AI engines (Minimax, Bitboard, Apocalyptron)
│   ├── Players/      # Player implementations
│   ├── Board/        # MVC board system
│   ├── Reversi/      # Core game logic
│   ├── ui/           # UI implementations (pygame, terminal, headless)
│   └── domain/       # Business logic (opening book, etc.)
├── tests/            # Test suite
├── docs/             # Documentation
└── tournament/       # Tournament system
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Naming conventions**:
  - Classes: `PascalCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

### Code Quality

- **Type hints**: Use type hints for function signatures
- **Docstrings**: All public methods should have docstrings
- **Comments**: Explain WHY, not WHAT
- **Tests**: Add tests for new features
- **No warnings**: Code should not produce linter warnings

### Example

```python
def evaluate_position(board: Game, depth: int) -> float:
    """
    Evaluate the current board position.
    
    Args:
        board: The game state to evaluate
        depth: Search depth for evaluation
        
    Returns:
        Evaluation score from current player's perspective
        
    Raises:
        ValueError: If depth is negative
    """
    if depth < 0:
        raise ValueError("Depth must be non-negative")
    
    # Use heuristic evaluation
    return _compute_heuristic_score(board)
```

### Architecture Principles

1. **Separation of Concerns**: Keep UI, business logic, and data layers separate
2. **Dependency Injection**: Use dependency injection for testability
3. **Interface Segregation**: Prefer small, focused interfaces
4. **Open/Closed Principle**: Open for extension, closed for modification
5. **Single Responsibility**: Each class should have one reason to change

## Pull Request Process

### Before Submitting

- [ ] Code follows our style guidelines
- [ ] Self-review of code completed
- [ ] Comments added where needed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No linter warnings
- [ ] Commit messages are clear

### PR Template

When you open a PR, please include:

1. **Description**: What does this PR do?
2. **Motivation**: Why is this change needed?
3. **Testing**: How was this tested?
4. **Screenshots**: For UI changes
5. **Breaking Changes**: Any API changes?
6. **Related Issues**: Fixes #123

### Review Process

1. **Automated checks**: CI/CD must pass
2. **Code review**: At least one maintainer approval required
3. **Testing**: Reviewer will test functionality
4. **Merge**: Maintainer will merge when ready

### After Your PR is Merged

- Delete your feature branch
- Update your fork
- Celebrate! 🎉 You're now a Reversi42 contributor!

## Reporting Bugs

### Before Submitting a Bug Report

- **Check existing issues**: Your bug may already be reported
- **Try latest version**: Bug may already be fixed
- **Isolate the problem**: Create minimal reproduction steps

### How to Submit a Good Bug Report

Use the bug report template and include:

- **Clear title**: Descriptive summary of the issue
- **Environment**: OS, Python version, Pygame version
- **Steps to reproduce**: Numbered list of steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Error messages or stack traces
- **Additional context**: Anything else relevant

### Example Bug Report

```markdown
**Title**: Game crashes when loading saved game with invalid format

**Environment**:
- OS: macOS 13.0
- Python: 3.11.0
- Pygame: 2.5.2

**Steps to Reproduce**:
1. Create a saved game
2. Manually edit the .xot file with invalid data
3. Try to load the game
4. Game crashes

**Expected**: Show error message "Invalid save file format"
**Actual**: Game crashes with stack trace

**Stack trace**:
```
[paste stack trace here]
```

**Additional Context**: This happens when the file is corrupted
```

## Suggesting Enhancements

We love new ideas! Before suggesting:

- **Check roadmap**: May already be planned
- **Check existing suggestions**: May already be suggested
- **Consider scope**: Should it be in core or a plugin?

### Enhancement Template

- **Title**: Clear, descriptive title
- **Problem**: What problem does this solve?
- **Solution**: Your proposed solution
- **Alternatives**: Other solutions considered
- **Benefits**: Who benefits and how
- **Implementation**: How could this be implemented?
- **Breaking changes**: Will this break existing code?

## Community

### Getting Help

- 📧 **Email**: luca.amore@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/Reversi42/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/Reversi42/discussions)

### Recognition

All contributors are recognized in:
- README.md contributors section
- CHANGELOG.md release notes
- GitHub contributors graph

### Development Chat

For real-time development discussion:
- Open an issue for technical questions
- Use GitHub Discussions for general questions
- Email for private matters

## Types of Contributions We Need

### AI Development

- New evaluation functions
- Search optimizations
- Pruning techniques
- Machine learning integration
- Opening book expansion

### UI/UX

- New view modes
- Accessibility improvements
- Themes and customization
- Mobile support
- Web interface

### Testing

- Unit tests
- Integration tests
- Performance benchmarks
- Game scenario tests
- AI strength validation

### Documentation

- Code documentation
- User guides
- Architecture documentation
- Video tutorials
- Translations

### Infrastructure

- CI/CD improvements
- Build automation
- Package distribution
- Performance profiling
- Security audits

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0.

---

## Thank You! 🙏

Your contributions make Reversi42 better for everyone. Whether you're fixing a typo or adding a major feature, we appreciate your help!

**Questions?** Don't hesitate to ask! Open an issue or email luca.amore@gmail.com.

Happy coding! 🎮


