# Reversi42

<p align="center">
  <img src="https://raw.githubusercontent.com/lookee/Reversi42/refs/heads/master/icons/reversi42.png" alt="Reversi42 Logo" width="200" style="max-width: 100%; height: auto;">
</p>

<p align="center">
  <a href="https://github.com/lookee/Reversi42/actions/workflows/ci.yml">
    <img src="https://github.com/lookee/Reversi42/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  </a>
  <a href="https://github.com/lookee/Reversi42/actions/workflows/release.yml">
    <img src="https://github.com/lookee/Reversi42/actions/workflows/release.yml/badge.svg" alt="Release Status">
  </a>
  <a href="https://github.com/lookee/Reversi42/actions/workflows/docs.yml">
    <img src="https://github.com/lookee/Reversi42/actions/workflows/docs.yml/badge.svg" alt="Documentation Status">
  </a>
  <a href="https://github.com/lookee/Reversi42/actions/workflows/security.yml">
    <img src="https://github.com/lookee/Reversi42/actions/workflows/security.yml/badge.svg" alt="Security Status">
  </a>
  <a href="https://pypi.org/project/reversi42/">
    <img src="https://img.shields.io/pypi/v/reversi42.svg" alt="PyPI Version">
  </a>
  <a href="https://pypi.org/project/reversi42/">
    <img src="https://img.shields.io/pypi/pyversions/reversi42.svg" alt="Python Versions">
  </a>
  <a href="https://pypi.org/project/reversi42/">
    <img src="https://img.shields.io/pypi/dm/reversi42.svg" alt="PyPI Downloads">
  </a>
  <a href="https://github.com/lookee/Reversi42/blob/master/COPYING">
    <img src="https://img.shields.io/badge/license-GPL--3.0--or--later-blue.svg" alt="License">
  </a>
  <a href="https://github.com/lookee/Reversi42">
    <img src="https://img.shields.io/github/stars/lookee/Reversi42.svg?style=social&label=Star" alt="GitHub Stars">
  </a>
  <a href="https://github.com/lookee/Reversi42/issues">
    <img src="https://img.shields.io/github/issues/lookee/Reversi42.svg" alt="GitHub Issues">
  </a>
  <a href="https://github.com/lookee/Reversi42/releases">
    <img src="https://img.shields.io/github/release/lookee/Reversi42.svg" alt="GitHub Release">
  </a>
  <a href="https://codecov.io/gh/lookee/Reversi42">
    <img src="https://codecov.io/gh/lookee/Reversi42/branch/master/graph/badge.svg" alt="Code Coverage">
  </a>
</p>

**Reversi42: Fast AI Reversi**

A tournament-grade Reversi implementation featuring high-performance bitboard-based AI engine, comprehensive opening book system, and modern web-based interface. Designed for both casual play and competitive AI research.

**Copyright (C) 2011-2025 Luca Amore**  
**Website:** https://www.lucaamore.com

---

## Overview

Reversi42 is a Reversi implementation that combines classical game AI techniques with modern software engineering practices. The engine utilizes bitboard representation for optimal performance, achieving 50-100x speedup over standard implementations through efficient 64-bit integer operations.

The system includes 12 pre-configured AI players with ELO ratings ranging from 1250 to 1880, a comprehensive opening book with 644 professional sequences, and a fully-featured tournament system for AI benchmarking and competition.

---

## Key Features

### Core Engine
- **Bitboard-Based Architecture**: 64-bit integer operations for O(1) board operations
- **Advanced Search Algorithms**: Alpha-beta pruning with transposition tables, null-move pruning, futility pruning, late move reduction (LMR), and multi-cut pruning
- **Multiple Search Strategies**: Fixed depth, iterative deepening, and adaptive depth search
- **Parallel Processing**: Multi-core support for parallel search execution
- **Evaluation Functions**: Four specialized evaluators (Mobility, Positional, Stability, Parity) with configurable weights

### AI Players
- **12 Pre-configured Players**: Ranging from beginner (ELO 1250) to expert level (ELO 1880)
- **Configurable Difficulty**: Each player features unique strategies and evaluation profiles
- **YAML-Based Configuration**: No-code AI player creation through declarative configuration files
- **Custom Avatars**: Support for custom player avatars (PNG/JPEG, 512x512 recommended)

### Opening Book System
- **644 Professional Sequences**: Comprehensive opening book derived from tournament play
- **Trie-Based Lookup**: O(m) complexity for efficient sequence matching
- **Multiple Modes**: Instant play and evaluated modes for flexible gameplay

### User Interface
- **Modern Web Interface**: Browser-based UI built with FastAPI and WebSocket for real-time updates
- **Game Management**: Save and load functionality using XOT (eXtended Othello Transcript) format
- **Real-time Analysis**: Live move evaluation and game state visualization

### Tournament System
- **AI Competitions**: Automated tournament mode for benchmarking and competition
- **Statistical Analysis**: Comprehensive statistics and performance metrics
- **Custom Configurations**: Flexible tournament setup through JSON configuration files

---

## Installation

### Requirements
- Python 3.9 or higher
- pip package manager

### Install from PyPI

```bash
pip install reversi42
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/lucaamore/reversi42.git
cd reversi42

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

---

## Quick Start

### Web Interface (Recommended)

Launch the web-based interface:

```bash
reversi42
```

The interface will be available at `http://localhost:8000` in your web browser.

### Python API

Use Reversi42 as a Python library:

```python
from Reversi.BitboardGame import BitboardGame
from Players.PlayerFactory import PlayerFactory

# Initialize game
game = BitboardGame()

# Create AI player from YAML configuration
player = PlayerFactory.create_from_yaml("config/players/enabled/divzero.yaml")

# Play game programmatically
# ... game logic ...
```

### Tournament Mode

Run AI competitions:

```bash
# Quick tournament match
python tournament/quick_tournament.py

# Custom tournament configuration
python tournament/tournament.py ring/config.json
```

---

## AI Players

Reversi42 includes 12 pre-configured AI players with varying skill levels and strategies:

| Player | ELO Rating | Strategy | Search Depth | Description |
|:------:|:----------:|:--------:|:------------:|:------------|
| DIVZERO.EXE | 1880 | Adaptive | 8/12/16 | Maximum strength player with adaptive depth and parallel processing |
| The Oracle | 1850 | Endgame Focus | 7/9/14 | Specialized in endgame positions with parity evaluation |
| Apocalyptron | 1850 | Balanced | Adaptive | Standard strong AI with balanced evaluation |
| Fortress Eternal | 1800 | Defensive | 10 | Defensive specialist with stability focus |
| The Executioner | 1770 | Aggressive | 9 | Aggressive player with mobility emphasis |
| The Strangler | 1750 | Mobility Control | 11 | Focuses on restricting opponent mobility |
| Corner Reaper | 1720 | Positional | 8 | Positional player with corner control emphasis |
| Glitch Lord | 1500±200 | Chaotic | Variable | Unpredictable player with randomized behavior |
| Lightning Strike | 1400 | Speed | 4 | Fast-playing player for rapid games |
| Blitz Demon | 1350 | Rapid Fire | 5 | Ultra-fast player optimized for speed |
| Zen Master | 1250 | Balanced | 3 | Beginner-friendly balanced player |

For detailed player profiles and configurations, see [EPIC_GLADIATORS.md](docs/EPIC_GLADIATORS.md).

---

## Custom AI Player Configuration

Create custom AI players using YAML configuration files without programming:

### Quick Start

```bash
# Copy template
cp config/players/00_AI_CONFIG_TEMPLATE.yaml config/players/enabled/my_ai.yaml

# Edit configuration
vim config/players/enabled/my_ai.yaml

# Player is automatically discovered on startup
reversi42
```

### Configuration Options

- **Search Depth** (4-16): Controls AI strength vs. speed tradeoff
- **Search Strategy**: `fixed`, `iterative`, or `adaptive`
- **Evaluation Presets**: `balanced`, `aggressive`, `defensive`, `endgame_specialist`
- **Parallel Search**: Enable multi-core processing
- **Pruning Techniques**: Configure null-move, futility, LMR, and multi-cut pruning
- **Opening Book**: Enable/disable and configure opening book usage
- **Custom Avatars**: Specify custom avatar images (PNG/JPEG)

### Example Configurations

**Speed-Optimized Player** (ELO ~1400):
- Depth: 4-5
- Minimal pruning
- Average move time: <100ms

**Tactical Player** (ELO ~1750):
- Depth: 9
- Mobility weight: ×2.5
- Average move time: ~5s

**Defensive Specialist** (ELO ~1800):
- Depth: 10
- Stability weight: ×2.5
- Average move time: ~10s

**Endgame Specialist** (ELO ~1850):
- Adaptive depth: 7/9/14
- Parity weight: ×2.0
- Variable move time

For comprehensive configuration documentation, see [CREATE_CUSTOM_PLAYER.md](docs/tutorials/CREATE_CUSTOM_PLAYER.md) and [AI_CONFIGURATION_SYSTEM.md](docs/AI_CONFIGURATION_SYSTEM.md).

---

## Technical Architecture

### Core Technologies

- **Bitboard Representation**: 64-bit integers for efficient board state manipulation
- **Classical AI Algorithms**: Minimax with alpha-beta pruning (no neural networks)
- **Advanced Pruning**: Null-move, futility, LMR, and multi-cut techniques
- **Transposition Tables**: Efficient position caching for improved performance
- **Move Ordering**: PV-move, killer moves, and history heuristic optimization

### Performance Characteristics

- **Speed**: 50-100x faster than standard array-based implementations
- **Search Depth**: Configurable from 4 to 16 ply
- **Parallel Processing**: Multi-core support for parallel search
- **Memory Efficiency**: Optimized data structures for minimal memory footprint

### Project Statistics

- **Codebase**: ~12,000 lines of Python code
- **Test Coverage**: 220+ unit and integration tests
- **Documentation**: 40+ documentation files
- **AI Players**: 12 pre-configured players
- **Opening Sequences**: 644 professional opening sequences

For detailed technical documentation, see:
- [Apocalyptron Engine Architecture](docs/architecture/apocalyptron-engine.md)
- [Bitboard Implementation](docs/architecture/bitboard.md)
- [System Architecture](docs/architecture/README.md)

---

## Project Structure

```
Reversi42/
├── src/                      # Source code
│   ├── Reversi/              # Core game engine (BitboardGame, Game)
│   ├── AI/Apocalyptron/      # AI engine (search, evaluation, pruning, caching)
│   ├── Players/              # Player system and configurations
│   ├── webgui/               # FastAPI WebSocket server
│   ├── domain/               # Opening book system
│   └── ui/                   # UI implementations
├── config/                   # YAML configurations
│   └── players/enabled/      # AI player configurations
├── docs/                     # Comprehensive documentation
├── tests/                    # Test suite (220+ tests)
├── tournament/               # Tournament system
└── saves/                    # Saved games (XOT format)
```

---

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[User Guide](docs/user-guide/README.md)**: Getting started, game rules, strategies, and FAQ
- **[API Reference](docs/api/README.md)**: Complete API documentation for BitboardGame, Player, and View classes
- **[Architecture Documentation](docs/architecture/README.md)**: System design, engine architecture, and technical details
- **[Tutorials](docs/tutorials/CREATE_CUSTOM_PLAYER.md)**: Step-by-step guides for creating custom AI players
- **[Tournament System](tournament/README.md)**: Tournament configuration and usage
- **[Development Guide](docs/development/README.md)**: Setup, testing, and contribution guidelines

---

## Testing

Run the comprehensive test suite:

```bash
# Full test suite
./scripts/run_tests.sh

# Quick unit tests
pytest tests/apocalyptron/unit/ -v

# With coverage
pytest --cov=src tests/
```

The project includes 220+ tests covering unit, integration, and characterization scenarios. See [test documentation](tests/apocalyptron/README.md) for details.

---

## Game File Format

Games are saved in **XOT** (eXtended Othello Transcript) format, a human-readable format that stores complete move history, game metadata, and player information. Saved games are stored in the `saves/` directory.

---

## License

This project is licensed under the GNU General Public License v3.0 or later. See the [LICENSE](COPYING) file for details.

---

## Development

Reversi42 was developed using modern software engineering practices and AI-assisted development tools. The codebase demonstrates:

- SOLID principles and clean architecture
- Comprehensive test coverage
- Extensive documentation
- Type hints and static analysis
- CI/CD integration

For development setup and contribution guidelines, see [Development Guide](docs/development/README.md).

---

## Acknowledgments

- **Donato Barnaba** and **Federazione Italiana Gioco Othello (FNGO)** - Reversi expertise and guidance
- **PointyStone3 Project** - Opening book data contributions
- **Cursor** - AI-powered development environment

---

## Author

**Luca Amore**  
Email: luca.amore@gmail.com  
Website: https://www.lucaamore.com

---

## Links

- **Homepage**: https://www.lucaamore.com
- **Repository**: https://github.com/lucaamore/reversi42
- **Documentation**: https://github.com/lucaamore/reversi42/tree/main/docs
- **Issue Tracker**: https://github.com/lucaamore/reversi42/issues

---

**Reversi42** - Professional-grade Reversi implementation for players and researchers alike.
