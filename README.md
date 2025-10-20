# Reversi42

**Ultra-Fast Reversi (Othello) with Bitboard AI and Opening Book Learning**

Version: **3.1.0** 🚀  
Originally released: 2011-03-07  
Major Update: 2025-10-18

Copyright (C) 2011-2025 Luca Amore  
Website: https://www.lucaamore.com

---

## 📖 Description

Reversi42 is a tournament-grade implementation of Reversi (Othello) featuring ultra-fast bitboard AI, interactive opening book learning, and comprehensive competitive features. The **3.1.0 release** adds advanced tournament system with 12 pre-configured tournaments and comprehensive player documentation.

### 🌟 What's New in 3.1.0

#### Modular View Architecture
- 🎨 **3 View Types** - Pygame (GUI), Terminal (ASCII), Headless (no UI)
- 🎮 **Command-line Selection** - `--view terminal|pygame|headless`
- 🖥️ **Terminal Mode** - Pure ASCII art, works on any background
- 🚀 **Headless Mode** - Zero rendering overhead for tournaments
- 🔌 **Pluggable Design** - Easy to add new view types

#### Terminal Mode Features
- ⌨️ **Numbered Moves** - Select by number (1-4) or coordinates (D3)
- 🎨 **Pure ASCII** - Works on white or black terminal backgrounds
- 📊 **Compact Layout** - Minimal vertical space usage
- 🌐 **SSH-Friendly** - Perfect for remote play
- ✅ **All 10 Players** - Including Terminal Human Player

#### Tournament System
- 🏆 **Tournament Support** - Run AI competitions
- 📊 **Configurable** - Customizable tournament setups

#### Documentation
- 📚 **Comprehensive Documentation** - Complete guides for users and developers
- 📖 **View Architecture** - Modular UI system documentation
- 📝 **Architecture Documentation** - Technical deep dives and design principles

### What's New in 3.0.0

- ⚡ **Bitboard Engine Production Ready** - Complete rewrite with fixed edge-wrapping bugs
- 📚 **Interactive Opening Book** - Visual learning with golden move highlighting
- 🎓 **Opening Database** - 57 professional openings with real-time tooltips
- 🔢 **Opening Count Badges** - See how many openings each move leads to
- 🎮 **Enhanced Menu** - New About screen, Show/Hide Opening toggle
- 💨 **50-100x Faster AI** - Bitboard operations for lightning-fast gameplay

### Key Features

- 🎮 **Modular View System** - Play in GUI, Terminal, or Headless mode (NEW in 3.1.0)
- 🎨 **Multiple UI Options** - Pygame (graphical), Terminal (ASCII), Headless (no rendering)
- ⚡ **Ultra-Fast Bitboard AI** - 50-100x faster than standard implementation
- 🤖 **Multiple AI Types** - From random to deep bitboard search (depth 1-12)
- 📚 **Opening Book System** - 57+ classic openings with visual learning mode
- 🏆 **Tournament System** - Run AI competitions and benchmarks
- 💾 **Save/Load** - XOT (eXtended Othello Transcript) format
- 🎯 **Modular Design** - Metadata-driven player system, pluggable views
- 🔄 **Resizable Window** - Adaptive graphics (Pygame mode)
- 📊 **Real-time Statistics** - Move history, timing, book usage
- 🖥️ **SSH-Friendly** - Play over SSH with terminal view

---

## 🎮 Player Types

The game features a **metadata-driven player system** with several AI opponents.

### Complete Player Roster (v3.1.0)

| Player Name | Type | Engine | Speed | Depth | Opening Book | Best For |
|------------|------|--------|-------|-------|--------------|----------|
| **Human Player** | Human | Manual | - | - | ❌ | You! Interactive play with visual learning |
| **Alpha-Beta AI** | AI | Minimax | 1x | 1-10 | ❌ | Practice, reliable opponent |
| **Opening Scholar** | AI | Minimax+Book | 1x | 1-10 | ✅ 57 | Learning openings, strong early game |
| **Bitboard Blitz** | AI | Bitboard | **50x** | 1-12 | ❌ | Fast analysis, deep searches |
| **The Oracle** | AI | Bitboard+Book | **100x** | 1-12 | ✅ 57 | Strong challenge, fast games |
| **Parallel Oracle** 🏆 | AI | Parallel+Book | **200-500x** | 7-12 | ✅ 57 | Ultimate AI, multi-core |
| **⚡ Apocalyptron** 🏆⚡ | AI | Ultimate | **3500-14000x** | 7-12 | ✅ 644 | **DEFAULT - All optimizations, depth 9** |
| **Heuristic Scout** | AI | Heuristic | Fast | - | ❌ | Quick games, medium difficulty |
| **Greedy Goblin** | AI | Greedy | Fast | - | ❌ | Educational, shows greedy pitfalls |
| **Random Chaos** | Random | RNG | Instant | - | ❌ | Testing, benchmarking, fun |

### Detailed Player Descriptions

#### 👤 Human Player
**You control the game!**
- **Controls**: Mouse click or keyboard navigation (C + arrows)
- **Features**: Opening book tooltips when enabled
- **Learning**: See golden moves and opening names while you play
- **Best For**: Everyone - this is you!

#### 🤖 Alpha-Beta AI
**Classic AI with proven minimax algorithm**
- **Technology**: Alpha-beta pruning, transposition tables
- **Strength**: Configurable depth 1-10
- **Style**: Strategic, reliable, well-balanced
- **Best For**: Learning AI basics, consistent practice opponent
- **Performance**: ~2,000 nodes/second at depth 6

#### 📚 Opening Scholar  
**Master of opening theory**
- **Technology**: 57 professional openings + minimax fallback
- **Strength**: Instant in book, depth 1-10 when out
- **Style**: Strong early game, follows master sequences
- **Best For**: Learning openings, tournament preparation
- **Special**: Randomly selects from multiple book options for variety
- **Performance**: Instant book moves, standard speed out of book

#### ⚡ Bitboard Blitz
**Pure computational speed**
- **Technology**: 64-bit bitboard representation
- **Strength**: Depth 1-12 practical in real-time
- **Style**: Aggressive deep searches, no opening knowledge
- **Best For**: Analysis, deep tactical positions
- **Performance**: **50-100x faster** - 50,000+ nodes/second
- **Special**: Can search depth 10-12 in seconds

#### 🔮 The Oracle
**Ultimate single-core Reversi AI**
- **Technology**: Bitboard engine + 57 opening sequences
- **Strength**: Depth 1-12 with instant opening responses
- **Style**: Perfect opening play, deep midgame search
- **Best For**: Strong challenge, fast games
- **Performance**: **100x faster** when in book, 50x when searching
- **Special**: Combines speed AND knowledge

#### ⚡ Parallel Oracle 🏆
**Ultimate multi-core Reversi AI**
- **Technology**: Parallel bitboard (2-5x) + 57 opening sequences
- **Strength**: Depth 7-12 with multi-core parallel search
- **Style**: Perfect opening play + ultra-deep parallel search
- **Best For**: Maximum challenge, tournaments, deep analysis (4+ cores)
- **Performance**: **200-500x faster** than standard, 2-5x vs single-core
- **Special**: Auto-adaptive (sequential for depth <7, parallel for >=7)
- **Intelligence**: Master openings + 12+ ply lookahead with multiprocessing

#### ⚡ Apocalyptron (NEW - DEFAULT) 🏆⚡
**The ultimate Reversi AI with all optimizations**
- **Technology**: All techniques combined - Iterative Deepening, Null Move, Futility, LMR, Multi-Cut, Aspiration Windows, History Heuristic
- **Strength**: Depth 7-12, default at depth 9 for optimal play
- **Style**: Perfect opening play (644 sequences) + ultimate search optimizations
- **Best For**: Maximum challenge, tournaments, learning from perfect play
- **Performance**: **3500-14000x faster** than standard AI
- **Win Rate**: +40-50% vs base parallel AI
- **Special**: Clean architecture, all Grandmaster features + new optimizations
- **Default**: Selected by default at depth 9 for new games
- **Intelligence**: Master openings + advanced pruning + parallel power
- **Opening Book**: 644 professional sequences with positional evaluations

#### 🎯 Heuristic Scout
**Fast intuitive player**
- **Technology**: Positional heuristics, pattern recognition
- **Strength**: Medium (no deep search)
- **Style**: Quick decisions, position-based
- **Best For**: Fast games, variety in play style
- **Performance**: Instant moves

#### 👹 Greedy Goblin
**Educational opponent**
- **Technology**: Immediate piece count maximization
- **Strength**: Weak (short-sighted strategy)
- **Style**: Always captures maximum pieces available
- **Best For**: Beginners learning why greedy play fails
- **Educational Value**: Shows importance of position over piece count
- **Performance**: Instant moves

#### 🎲 Random Chaos
**Pure unpredictability**
- **Technology**: Random number generator
- **Strength**: None (random)
- **Style**: Completely unpredictable
- **Best For**: Testing, benchmarking, comic relief
- **Performance**: Instant moves
- **Warning**: Will make terrible moves!

### Quick Comparison

**For Beginners:** Start with Human Player vs Alpha-Beta AI (level 3-4)

**For Learning:** Human Player vs Opening Scholar (level 5) + Show Opening enabled

**For Challenge:** Human Player vs The Oracle (level 5-8)

**For Speed Testing:** Bitboard Blitz vs The Oracle (tournament mode)

For technical details on the AI system, see the [Architecture Documentation](docs/architecture/apocalyptron-engine.md).

---

## 🧠 AI Strategy

### Core Technologies (v3.0.0)

The AI system combines multiple advanced techniques:

- **Bitboard Representation** ⚡ - 64-bit integer board state (50-100x faster)
- **Alpha-Beta Pruning** - Efficient minimax tree exploration
- **Transposition Tables** - Position caching for repeated states
- **Move Ordering** - Prioritizes high-value moves (corners, edges, stability)
- **Opening Book** - Trie-based O(m) instant lookup for 57 professional openings
- **Modular Evaluators** - Pluggable evaluation functions
- **O(1) Undo/Copy** - Bitboard allows instant state management

### Bitboard Engine (NEW in 3.0.0)

The bitboard implementation uses:
- **64-bit integers** to represent Black/White pieces
- **Bit manipulation** for move generation and validation
- **Pre-computed masks** to prevent edge wrapping
- **Shift operations** in all 8 directions
- **Single-pass flip calculation** using bit operations

**Result**: Deep searches (depth 10-12) are practical for real-time play!

### Evaluation Functions

1. **StandardEvaluator** - Mobility, corners, and edge control
2. **SimpleEvaluator** - Basic weighted piece count
3. **AdvancedEvaluator** - Position tables with game phase awareness
4. **GreedyEvaluator** - Immediate piece maximization

---

## 📚 Opening Book System (Enhanced in 3.0.0)

The opening book system now includes **interactive visual learning**:

### Opening Database
- **57 Professional Openings** - Diagonal, Tiger, Buffalo, Rose, and more
- **Named Sequences** - Each opening has a recognized tournament name
- **Trie Structure** - O(m) instant lookup where m = moves played
- **Smart Fallback** - Bitboard search when leaving book theory

### Visual Learning Mode (NEW!)

When "Show Opening" is enabled in the menu:

- ⭐ **Golden Move Highlighting** - Moves that lead to known openings glow gold
- 🔢 **Opening Count Badges** - See how many openings each move opens (e.g., "57")
- 💡 **Real-time Tooltips** - Hover over golden moves to see opening names
- 📖 **Fixed Info Panel** - Professional tooltip in top-right corner
- 🎓 **Learn While Playing** - Discover new openings naturally

**Example**: Initial position shows F5 with badge "57" → hover to see all 57 openings!

*Location: `Books/opening_book.txt`*  
*Format: `Opening Name | Move Sequence`*  
*Toggle: Menu → "Show Opening" / "Hide Opening"*

---

## 🏆 Tournament System

Tournament system for running AI competitions.

```bash
cd tournament
python3 tournament.py
```

See [Tournament Documentation](tournament/README.md) for details.

---

## 🚀 Installation & Usage

### Requirements

- Python 3.6 or higher
- Pygame 2.0+

```bash
pip install pygame
```

### Running the Game

```bash
# Default (Pygame graphical interface)
./reversi42

# Terminal mode (ASCII art - SSH friendly)
./reversi42 --view terminal

# Headless mode (no graphics - for testing)
./reversi42 --view headless

# Show available view types
./reversi42 --list-views

# Show version
./reversi42 --version

# Or using Python directly
python3 src/reversi42.py --view pygame
```

**View Options** (NEW in 3.1.0):
- `--view pygame` (or `gui`) - Graphical interface [default]
- `--view terminal` (or `console`) - ASCII art in terminal  
- `--view headless` (or `none`) - No rendering (tournaments/testing)

### Game Controls

**Mouse:**
- Click on highlighted squares to make moves
- Hover over golden moves to see opening names (when Show Opening enabled)

*Keyboard:*
- `C` - Toggle cursor navigation mode
- `Arrow Keys` - Move cursor (in cursor mode)
- `ENTER/SPACE` - Select move at cursor
- `ESC` - Pause menu (save/load/resume)
- `Q` - Quick exit

**Terminal Mode:**
- Type coordinates: `D3`, `E4`, etc.
- Or use numbers: `1`, `2`, `3` (from numbered move list)
- `q` - Quit game
- `h` - Show help

**Headless Mode:**
- No user controls (automated only)

### Menu Options

**Main Menu:**
- Black Player (choose type and difficulty)
- White Player (choose type and difficulty)
- **Show Opening** / Hide Opening (toggle golden move highlights)
- Start Game
- Help (controls and player descriptions)
- **About** (game rules, version info, credits)
- Exit

### Pause Menu (ESC during game)

- Resume Game
- Undo Move
- Save Game (XOT format)
- Load Game
- Return to Menu
- Exit

---

## 💾 Save/Load System

Games are saved in **XOT** (eXtended Othello Transcript) format:

- Human-readable text format
- Complete move history
- Board state preservation
- Compatible with analysis tools
- Saved to `saves/` directory

---

## 🏗️ Building Distributions

Create standalone executables for Windows, Linux, and macOS:

```bash
cd build
./build_all.sh    # Auto-detects platform

# Or platform-specific:
./build_macos.sh
./build_linux_deb.sh
./build_windows.sh
```

*See `BUILD.md` for complete build documentation*

---

## 📁 Project Structure

```
Reversi42/
├── src/               # Source code
│   ├── Reversi/       # Core game logic
│   ├── Board/         # Modular view system (MVC) ⭐ NEW
│   │   ├── AbstractBoardView.py     # View interface
│   │   ├── PygameBoardView.py       # Pygame UI
│   │   ├── TerminalBoardView.py     # ASCII art
│   │   ├── HeadlessBoardView.py     # No rendering
│   │   ├── ViewFactory.py           # View factory
│   │   ├── BoardControl.py          # MVC Controller
│   │   └── BoardModel.py            # MVC Model
│   ├── AI/            # AI engines and evaluators
│   ├── Players/       # Player implementations
│   ├── examples/      # Demo scripts
│   └── reversi42.py   # Main entry point
├── docs/              # Documentation
│   ├── players/       # Detailed player documentation (13 files)
│   ├── VIEW_ARCHITECTURE.md  # View system docs ⭐ NEW
│   ├── FEATURES.md    # Complete feature list
│   ├── ADDING_PLAYERS.md
│   ├── BITBOARD_IMPLEMENTATION.md
│   ├── GRANDMASTER_AI.md
│   └── STRATEGY_IMPROVEMENTS.md
├── tournament/        # Tournament system (12 configs)
│   └── ring/          # Tournament configurations ⭐
├── Books/             # Opening book library
├── saves/             # Saved games (XOT format)
├── build/             # Build scripts
├── CHANGELOG.md       # Version history ⭐ NEW
├── TERMINAL_MODE_COMPLETE.md          # Terminal mode implementation
└── reversi42          # Executable wrapper
```

---

## 🎓 Examples

### Compare AI Evaluators

```bash
python3 src/examples/evaluator_comparison.py
```

### Opening Book Demo

```bash
python3 src/examples/opening_book_demo.py
```

### Quick Tournament (Pre-configured)

```bash
python3 tournament/quick_tournament.py
```

---

## 🔧 Development

See the [Development Guide](docs/development/README.md) for:
- Setting up your development environment
- Code style guidelines
- Testing and contributing
- Building and packaging

---

## 📜 License

**GNU General Public License v3.0**

Reversi42 is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

---

## 🙏 Acknowledgments

**Special Thanks:**

- **Donato Barnaba** and **Federazione Italiana Gioco Othello (FNGO)**  
  Website: http://www.fngo.it  
  For invaluable support and Reversi expertise

- **PointyStone3 Project**  
  Repository: https://github.com/jonkr2/PointyStone3  
  For opening book data used in this implementation

- **Pygame Community**  
  For the excellent SDL bindings for Python

---

## 📚 Documentation

### 📖 User Documentation
- **[User Guide](docs/user-guide/README.md)** - Complete guide for players
  - [Getting Started](docs/user-guide/getting-started.md) - Quick start guide
  - [Game Rules](docs/user-guide/game-rules.md) - Learn how to play
  - [AI Opponents](docs/user-guide/ai-opponents.md) - Understanding AI players
  - [Strategies](docs/user-guide/strategies.md) - Tips to improve your game
  - [FAQ](docs/user-guide/faq.md) - Frequently asked questions

### 👨‍💻 Developer Documentation
- **[API Reference](docs/api/README.md)** - Complete API documentation
  - [BitboardGame API](docs/api/bitboard-game.md) - Core game engine
  - [Player API](docs/api/player-interface.md) - Player system
  - [View API](docs/api/view-interface.md) - UI system
- **[Architecture Guide](docs/architecture/README.md)** - System architecture
  - [Design Principles](docs/architecture/design-principles.md) - Guiding principles
  - [System Overview](docs/architecture/system-overview.md) - High-level view
- **[Development Guide](docs/development/README.md)** - Development setup and workflow
  - [Getting Started](docs/development/getting-started.md) - Dev environment setup
  - [Testing Guide](docs/development/testing.md) - Writing and running tests
  - [Code Style](docs/development/code-style.md) - Coding standards
  - [Best Practices](docs/development/best-practices.md) - Development patterns

### 🚀 Deployment & Installation
- **[Deployment Guide](docs/deployment/README.md)** - Installation and deployment
  - [Installation](docs/deployment/installation.md) - How to install
  - [Building](docs/deployment/building.md) - Create executables
  - [Configuration](docs/deployment/configuration.md) - Post-install setup

### 🤝 Contributing
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Code of Conduct](docs/contributing/README.md)** - Community guidelines
- **[Security Policy](SECURITY.md)** - Reporting security issues
- **[Changelog](CHANGELOG.md)** - Version history

### 🤖 AI & Technical Documentation
- **[Apocalyptron Engine](docs/architecture/apocalyptron-engine.md)** - Complete AI engine documentation
- **[Bitboard Implementation](docs/architecture/bitboard.md)** - Technical deep dive
- **[System Architecture](docs/architecture/system-overview.md)** - Complete system design
- **[Design Principles](docs/architecture/design-principles.md)** - Architectural principles

### 🏆 Tournament System
- **[Tournament System](tournament/README.md)** - Tournament system overview

### 🎓 Learning Resources
Want to improve your Othello skills? Check out these resources:

**External Resources:**
- [World Othello Federation](https://www.worldothello.org/) - Official international organization
- [FNGO](http://www.fngo.it) - Italian Othello Federation
- [Reversi Wikipedia](http://en.wikipedia.org/wiki/Reversi) - Game history and rules

**Recommended Study Tools:**
- **[WOF Study Support](https://www.worldothello.org/about/study-othello/study-support)** - Tools recommended by World Othello Federation
  - **Egaroucid** - One of the strongest Othello solver AIs
  - **Othello Sensei** - Analysis program by Michele Borassi
  - **SAIO** - Professional engine by 3x Italian Champion Benedetto Romano
  - **WZebra** - Classic analysis tool (still widely used since 2006)
  - **Othello Expert** - Multi-tool with 60,000 endgame puzzles
  - **Smart Othello** - Tutorial and teaching aids
  - **WTHOR Database** - 130,000+ tournament games archive

---

## 🙏 Acknowledgments

**Special thanks to Donato Barnaba** for his invaluable explanations, support, and insights during the development of the first version of this software. His expertise in Reversi/Othello strategy and game theory was fundamental in shaping the initial direction of Reversi42.

The software has since evolved significantly with advanced AI optimizations and features. As I am not an expert player myself, any errors or imperfections in the current implementation are solely my responsibility.

---

## 👤 Author

**Luca Amore**  
Email: luca.amore@gmail.com  
Website: https://www.lucaamore.com

---

**Have fun playing Reversi42!** 🎮🎉

