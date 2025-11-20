# Reversi42

<p align="center">
  <img src="https://raw.githubusercontent.com/lookee/Reversi42/refs/heads/master/icons/reversi42.png" alt="Reversi42 Logo" width="200" style="max-width: 100%; height: auto;">
</p>

<p align="center">
  <a href="https://pypi.org/project/reversi42/">
    <img src="https://img.shields.io/pypi/v/reversi42.svg?logo=pypi&logoColor=white" alt="PyPI Version">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-%3E%3D3.9-blue.svg?logo=python&logoColor=white" alt="Python >= 3.9">
  </a>
  <a href="https://pypi.org/project/reversi42/">
    <img src="https://img.shields.io/pypi/dm/reversi42.svg?logo=pypi&logoColor=white" alt="PyPI Downloads">
  </a>
  <a href="https://pypi.org/project/reversi42/">
    <img src="https://img.shields.io/pypi/status/reversi42.svg?logo=pypi&logoColor=white" alt="PyPI Status">
  </a>
  <a href="https://pypi.org/project/reversi42/">
    <img src="https://img.shields.io/pypi/format/reversi42.svg?logo=pypi&logoColor=white" alt="PyPI Format">
  </a>
  <a href="https://codecov.io/gh/lookee/Reversi42">
    <img src="https://codecov.io/gh/lookee/Reversi42/branch/master/graph/badge.svg" alt="Code Coverage">
  </a>
  <a href="https://github.com/lookee/Reversi42/actions/workflows/security.yml">
    <img src="https://github.com/lookee/Reversi42/actions/workflows/security.yml/badge.svg" alt="Security">
  </a>
  <a href="https://github.com/lookee/Reversi42/actions/workflows/docs.yml">
    <img src="https://github.com/lookee/Reversi42/actions/workflows/docs.yml/badge.svg" alt="Docs">
  </a>
  <a href="https://github.com/lookee/Reversi42/blob/master/COPYING">
    <img src="https://img.shields.io/pypi/l/reversi42.svg?logo=gnu&logoColor=white" alt="License">
  </a>
</p>

<p align="center">
  <strong>Tournament-grade Reversi with AI-powered opponents</strong><br>
  <em>50-100x faster • 11 AI players • 644 opening sequences • Modern web interface</em>
</p>

---

<p align="center">
  <img src="https://raw.githubusercontent.com/lookee/Reversi42/refs/heads/master/screen/reversi42-screen-1.png" alt="Reversi42 Screenshot" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</p>

---

## 🚀 Quick Start

```bash
pip install reversi42
reversi42
```

Open `http://localhost:8000` in your browser and start playing!

---

## ✨ Features

### 🎯 **High-Performance Engine**
- **Bitboard architecture** - 50-100x faster than traditional implementations
- **Advanced AI algorithms** - Alpha-beta pruning, transposition tables, parallel search
- **Configurable depth** - From beginner (3 ply) to expert (16 ply)

### 🤖 **11 AI Opponents**
- **ELO ratings**: 1250-1880 (beginner to expert)
- **Unique strategies**: Adaptive, defensive, aggressive, tactical, chaotic
- **YAML-based configuration** - Create custom AI players without coding

### 📚 **Professional Opening Book**
- **644 tournament sequences** - Derived from professional play
- **Trie-based lookup** - Instant move suggestions
- **Multiple evaluation modes** - Balanced and tactical openings

### 🌐 **Modern Web Interface**
- **Real-time gameplay** - FastAPI + WebSocket for instant updates
- **Game management** - Save/load games in XOT format
- **Live analysis** - Move evaluation and position visualization

### 🏆 **Tournament System**
- **Automated competitions** - Benchmark AI players
- **Statistical analysis** - Comprehensive performance metrics
- **Custom configurations** - Flexible tournament setups

---

## 🎮 AI Players

| Player | ELO | Strategy | Depth | Style |
|:------:|:---:|:--------:|:-----:|:-----:|
| **DIVZERO.EXE** | 1880 | Adaptive | 8/12/16 | Maximum strength, parallel processing |
| **The Oracle** | 1850 | Endgame Focus | 7/9/14 | Endgame specialist, parity evaluation |
| **Apocalyptron** | 1850 | Balanced | Adaptive | Strong balanced AI |
| **Fortress Eternal** | 1800 | Defensive | 10 | Defensive specialist |
| **The Executioner** | 1770 | Aggressive | 9 | Aggressive, mobility-focused |
| **The Strangler** | 1750 | Mobility Control | 11 | Restricts opponent mobility |
| **Corner Reaper** | 1720 | Positional | 8 | Corner control specialist |
| **Glitch Lord** | 1500±200 | Chaotic | Variable | Unpredictable, randomized |
| **Lightning Strike** | 1400 | Speed | 4 | Fast-playing |
| **Blitz Demon** | 1350 | Rapid Fire | 5 | Ultra-fast |
| **Zen Master** | 1250 | Balanced | 3 | Beginner-friendly |

📖 [View detailed player profiles →](https://github.com/lookee/Reversi42/blob/master/docs/EPIC_GLADIATORS.md)

---

## 📦 Installation

### From PyPI
```bash
pip install reversi42
```

### From Source
```bash
git clone https://github.com/lookee/Reversi42.git
cd Reversi42
pip install -e .
```

**Requirements**: Python 3.9+

---

## 🎨 Custom AI Players

Create your own AI opponents using YAML configuration files—no programming required!

```bash
cp config/players/00_AI_CONFIG_TEMPLATE.yaml config/players/enabled/my_ai.yaml
# Edit the configuration file
reversi42  # Your player is automatically discovered!
```

📚 [Configuration Guide →](https://github.com/lookee/Reversi42/blob/master/docs/tutorials/CREATE_CUSTOM_PLAYER.md)

---

## 📊 Performance

- **Speed**: 50-100x faster than array-based implementations
- **Search Depth**: 4-16 ply (configurable)
- **Parallel Processing**: Multi-core support
- **Memory**: Optimized data structures

---

## 📖 Documentation

- **[User Guide](https://github.com/lookee/Reversi42/blob/master/docs/user-guide/README.md)** - Getting started, rules, strategies
- **[API Reference](https://github.com/lookee/Reversi42/blob/master/docs/api/README.md)** - Complete API documentation
- **[Architecture](https://github.com/lookee/Reversi42/blob/master/docs/architecture/README.md)** - System design and technical details
- **[Tutorials](https://github.com/lookee/Reversi42/blob/master/docs/tutorials/CREATE_CUSTOM_PLAYER.md)** - Create custom AI players
- **[Tournament Guide](https://github.com/lookee/Reversi42/blob/master/tournament/README.md)** - Tournament system usage

---

## 🧪 Testing

```bash
# Run test suite
./scripts/run_tests.sh

# With coverage
pytest --cov=src tests/
```

**571+ tests** covering unit, integration, and characterization scenarios.

### Test Coverage by Module

- **Apocalyptron AI Engine**: 800+ tests (evaluation, ordering, pruning, cache, search, observers)
- **Board Module**: 34 tests (BoardModel, BoardControl, ViewFactory)
- **Players Module**: 60+ tests (PlayerFactory, PlayerHuman, PlayerApocalyptron, config system)
- **Core Module**: 34 tests (config, game_config)
- **Infrastructure**: 10 tests (persistence/game_io)
- **Integration Tests**: 50+ tests (board integrity, player isolation, book instant mode)
- **Bitboard Tests**: Comprehensive move generation tests
- **WebGUI Tests**: Backend server, WebSocket observer, E2E tests

---

## 📈 Project Stats

- **~17,000 lines** of Python code
- **571+ tests** with comprehensive coverage (target: 80%+)
- **42 test files** organized by module
- **40+ documentation files**
- **11 AI players** pre-configured
- **644 opening sequences** from professional play

---

## 📄 License

GNU General Public License v3.0 or later  
See [LICENSE](https://github.com/lookee/Reversi42/blob/master/COPYING) for details.

---

## 👤 Author

**Luca Amore**  
🌐 [www.lucaamore.com](https://www.lucaamore.com)  
📧 luca.amore@gmail.com

---

## 🙏 Acknowledgments

- **Donato Barnaba** and **Federazione Italiana Gioco Othello (FNGO)** - Reversi expertise
- **PointyStone3 Project** - Opening book contributions

---

<p align="center">
  <strong>Reversi42</strong> - Professional-grade Reversi for players and researchers<br>
  <a href="https://github.com/lookee/Reversi42">GitHub</a> • 
  <a href="https://pypi.org/project/reversi42/">PyPI</a> • 
  <a href="https://github.com/lookee/Reversi42/issues">Issues</a>
</p>
