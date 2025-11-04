# Reversi42

**Ultra-Fast Reversi (Othello) with Bitboard AI and Opening Book Learning**

Version: **5.0.0** 🚀  
Copyright (C) 2011-2025 Luca Amore  
Website: https://www.lucaamore.com

---

## 📖 Description

Tournament-grade Reversi (Othello) implementation featuring ultra-fast bitboard AI, interactive opening book learning, and modern web interface.

### ✨ Key Features

- 🌐 **Modern Web UI** - Browser-based interface with real-time WebSocket updates
- ⚡ **Ultra-Fast Bitboard Engine** - 50-100x faster than standard implementations
- 🤖 **12 AI Gladiators** - Unique opponents from beginner (ELO 1250) to champion (ELO 1880)
- 🎛️ **No-Code AI Creation** - Configure AI players via YAML (zero programming!)
- 📚 **Opening Book System** - 644 professional opening sequences
- 🏆 **Tournament Mode** - Run AI competitions and benchmarks
- 💾 **Save/Load Games** - XOT (eXtended Othello Transcript) format
- 🔧 **Highly Configurable** - 200+ parameters per AI, 4 evaluation presets, parallel search

---

## 🎮 AI Players

### Quick Comparison

| Player | ELO | Speed | Strategy | Best For |
|--------|-----|-------|----------|----------|
| 💀 **DIVZERO.EXE** | 1880 | ~5s | Adaptive 8/12/16, 8 cores | Final Boss |
| 🔮 **THE ORACLE** | 1850 | ~3s | Adaptive 7/9/14, Endgame | Expert Challenge |
| 🏆 **Apocalyptron** | 1850 | ~1s | Standard Strong | Balanced AI |
| 🛡️ **FORTRESS ETERNAL** | 1800 | ~6s | Defensive, Stability ×2 | Defense Master |
| ⚔️ **THE EXECUTIONER** | 1770 | ~4s | Aggressive, Mobility ×2 | Aggressive Play |
| 🎯 **THE STRANGLER** | 1750 | ~12s | Mobility ×3 | Mobility Control |
| 👑 **CORNER REAPER** | 1720 | ~2s | Positional, Corners ×2.5 | Corner Strategy |
| 👾 **GLITCH_LORD** | 1500± | ~0.2s | Chaotic, Unpredictable | Fun/Chaos |
| ⚡ **LIGHTNING STRIKE** | 1400 | <0.1s | Fixed Depth 4 | Speed Games |
| 🔥 **BLITZ DEMON** | 1350 | <0.05s | Fixed Depth 5 | Quick Matches |
| 🧘 **ZEN MASTER** | 1250 | ~0.03s | Fixed Depth 3, Balanced | Beginners |

### Recommended Progression

1. **Beginner**: 🧘 Zen Master (1250)
2. **Easy**: 🔥 Blitz Demon (1350) / 👾 Glitch Lord (1500)
3. **Medium**: ⚡ Lightning Strike (1400) / 👑 Corner Reaper (1720)
4. **Hard**: 🎯 The Strangler (1750) / ⚔️ The Executioner (1770)
5. **Very Hard**: 🛡️ Fortress Eternal (1800) / 🏆 Apocalyptron (1850)
6. **Expert**: 🔮 The Oracle (1850)
7. **Final Boss**: 💀 DIVZERO.EXE (1880)

> 📚 Full player profiles and configurations in [EPIC_GLADIATORS.md](docs/EPIC_GLADIATORS.md)

---

## 🎛️ No-Code AI Creation

Create custom AI players using simple YAML files - no programming required!

### Quick Start

```bash
# 1. Copy template
cp config/players/00_AI_CONFIG_TEMPLATE.yaml config/players/enabled/my_ai.yaml

# 2. Edit configuration (name, depth, weights, etc.)
vim config/players/enabled/my_ai.yaml

# 3. Play! Auto-discovered on startup
./reversi42
```

### Key Configuration Options

- **Search Depth** (4-16): Higher = stronger but slower
- **Strategy**: `fixed` | `iterative` | `adaptive`
- **Evaluation Presets**: `balanced` | `aggressive` | `defensive` | `endgame_specialist`
- **Parallel Search**: Enable multi-core processing
- **Pruning Techniques**: Null-move, futility, LMR, multi-cut (10-100x speedup)
- **Opening Book**: 644 sequences, instant/evaluated modes
- **Custom Avatars**: PNG/JPEG support (512x512 recommended)

### Example Configurations

**Speed Demon**: Depth 4-5, no pruning → <100ms, ELO ~1400  
**Tactical Fighter**: Depth 9, mobility ×2.5 → ~5s, ELO ~1750  
**Defensive Fortress**: Depth 10, stability ×2.5 → ~10s, ELO ~1800  
**Endgame Master**: Adaptive 7/9/14, parity ×2.0 → varies, ELO ~1850

> 📚 See [CREATE_CUSTOM_PLAYER.md](docs/tutorials/CREATE_CUSTOM_PLAYER.md) and [AI_CONFIGURATION_SYSTEM.md](docs/AI_CONFIGURATION_SYSTEM.md) for details

---

## 🧠 AI Technology

**Core Features:**
- ⚡ **Bitboard Engine**: 64-bit integer operations (50-100x faster than standard)
- 🌲 **Alpha-Beta Pruning**: Efficient minimax with transposition tables
- 📊 **4 Evaluators**: Mobility, Positional, Stability, Parity
- 📚 **Opening Book**: 644 sequences, trie-based O(m) lookup
- 🔀 **Move Ordering**: PV-move, killer moves, history heuristic

**Technologies Used:**
- Classical AI (no neural networks/deep learning)
- Bitboard representation for O(1) operations
- Advanced pruning techniques (null-move, futility, LMR, multi-cut)
- Parallel search with multi-core support

> 📖 Technical details in [apocalyptron-engine.md](docs/architecture/apocalyptron-engine.md) and [bitboard.md](docs/architecture/bitboard.md)

---

## 🏆 Tournament System

Run AI competitions and benchmarks:

```bash
python tournament/quick_tournament.py          # Quick match
python tournament/tournament.py ring/config.json  # Custom tournament
```

See [tournament/README.md](tournament/README.md) for details.

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Launch web interface
./reversi42
# Open browser at http://localhost:8000
```

**Requirements**: Python 3.9+, FastAPI, Uvicorn

### Usage Modes

**1. Web Interface** (Recommended)
```bash
./reversi42
```
Browser-based UI with real-time WebSocket updates

**2. Tournament Mode**
```bash
python tournament/quick_tournament.py
```
AI vs AI competitions with detailed statistics

**3. Python Library**
```python
from Reversi.BitboardGame import BitboardGame
from Players.PlayerFactory import PlayerFactory

game = BitboardGame()
player = PlayerFactory.create_from_yaml("config/players/enabled/divzero.yaml")
```

### Save/Load

Games saved in **XOT** (eXtended Othello Transcript) format in `saves/` directory - human-readable, complete move history.

---

## 📁 Project Structure

```
Reversi42/
├── src/                      # Source code
│   ├── Reversi/              # Core game (BitboardGame, Game)
│   ├── AI/Apocalyptron/      # AI engine (search, evaluation, pruning, caching)
│   ├── Players/              # Player system + 12 Gladiators
│   ├── webgui/               # FastAPI WebSocket server
│   ├── domain/               # Opening book (644 sequences)
│   └── ui/                   # UI implementations
├── config/                   # YAML configurations
│   └── players/enabled/      # AI player configs
├── docs/                     # Documentation (40+ files)
├── tests/                    # Test suite (220+ tests)
├── tournament/               # Tournament system
├── saves/                    # Saved games (XOT format)
└── requirements.txt          # Dependencies
```

**Statistics**: 250+ files, ~12K lines of code, 12 AI players, 3 search strategies, 220+ tests, 644 openings

---

## 📚 Documentation

- 📖 **[User Guide](docs/user-guide/README.md)** - Getting started, rules, strategies, FAQ
- 👨‍💻 **[API Reference](docs/api/README.md)** - BitboardGame, Player, View APIs
- 🏗️ **[Architecture](docs/architecture/README.md)** - System design, Apocalyptron engine, bitboard
- 🎓 **[Tutorials](docs/tutorials/CREATE_CUSTOM_PLAYER.md)** - Create custom AI players
- 🏆 **[Tournament System](tournament/README.md)** - AI competitions
- 🔧 **[Development Guide](docs/development/README.md)** - Setup, testing, contributing

---

## 🧪 Testing & CI/CD

```bash
./scripts/run_tests.sh              # Run full test suite (220+ tests)
pytest tests/apocalyptron/unit/ -v  # Quick unit tests
```

See [test documentation](tests/apocalyptron/README.md) and [CI/CD guide](docs/ci-cd/README.md)

---

## 📜 License

GNU General Public License v3.0 - See [LICENSE](COPYING) file for details.

---

## 🙏 Acknowledgments

- **Donato Barnaba** and **Federazione Italiana Gioco Othello (FNGO)** - Invaluable Reversi expertise
- **PointyStone3 Project** - Opening book data
- **AI-Human Collaboration** - Developed through human-AI synergy using advanced LLMs

---

## 👤 Author

**Luca Amore**  
Email: luca.amore@gmail.com  
Website: https://www.lucaamore.com

**Have fun playing Reversi42!** 🎮

