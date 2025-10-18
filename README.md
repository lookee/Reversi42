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
- 🏆 **12 Pre-configured Tournaments** - Ready to run
- 📊 **JSON Configurations** - Reusable tournament setups
- 🎮 **Interactive Selector** - Visual menu for tournament selection
- 🤖 **Full AI Support** - Grandmaster, Parallel, all variants
- ⚡ **Batch Execution** - Run all tournaments with one command

#### Documentation
- 📚 **13 Player Guides** - Complete documentation in docs/players/
- 📖 **View Architecture** - Modular UI system documentation
- 📝 **Tournament Guides** - Complete tournament system docs

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
- 🏆 **Tournament System** - 12 pre-configured tournaments, batch execution
- 💾 **Save/Load** - XOT (eXtended Othello Transcript) format
- 🎯 **Modular Design** - Metadata-driven player system, pluggable views
- 🔄 **Resizable Window** - Adaptive graphics (Pygame mode)
- 📊 **Real-time Statistics** - Move history, timing, book usage
- 🖥️ **SSH-Friendly** - Play over SSH with terminal view

---

## 🎮 Player Types

The game features a **metadata-driven player system** with **9 legendary AI warriors**, each with unique personality and strategy!

### Complete Player Roster (v3.1.0)

| Player | Icon | Difficulty | Style | Strength | Speed | Best For |
|--------|------|------------|-------|----------|-------|----------|
| **Human Player** | 👤 | - | Your Style | You! | - | Interactive play, learning |
| **Random Chaos** | 🎲 | Beginner | Chaotic | ☆☆☆☆☆ | ⚡⚡⚡⚡⚡ | First-time players, testing |
| **Hungry Hippo** | 🦛 | Beginner | Greedy | ★☆☆☆☆ | ⚡⚡⚡⚡⚡ | Learning tactics |
| **Berserker** | ⚔️ | Intermediate | Aggressive | ★★★☆☆ | ⚡⚡⚡⚡☆ | Handling pressure |
| **Zen Master** | 🧘 | Intermediate | Balanced | ★★★★★ | ⚡⚡⚡☆☆ | Balanced strategy |
| **The Trickster** | 🎭 | Intermediate | Psychological | ★★★★☆ | ⚡⚡⚡☆☆ | Unpredictable opponents |
| **The Shadow** | 🌑 | Advanced | Defensive | ★★★★☆ | ⚡⚡⚡☆☆ | Defensive mastery |
| **Ancient Sage** | 📜 | Advanced | Classical | ★★★★★ | ⚡⚡⚡⚡☆ | Opening theory |
| **Quantum Mind** | 🌌 | Expert | Analytical | ★★★★★★ | ⚡⚡⚡☆☆ | Ultimate challenge |
| **Apocalypse** 💀 | 💀 | **LEGENDARY** | **GODLIKE** | **★★★★★★★★** | ⚡⚡☆☆☆ | **FINAL BOSS** ⚠️ |

### Detailed Player Descriptions

For complete details on each player, see [Player Documentation](docs/players/README.md)!

#### 👤 Human Player
**You control the game!**
- **Controls**: Mouse click or keyboard navigation (C + arrows)
- **Features**: Opening book tooltips when enabled
- **Learning**: See golden moves and opening names while you play

#### 🎲 Random Chaos - "Pure Chaos Incarnate"
**Completely unpredictable!**
- **Strength**: Very Weak | **Speed**: Instant
- **Best For**: First-time players, testing, fun
- **Quote**: *"I move without thinking. Predictability is for the weak!"*

#### 🦛 Hungry Hippo - "Greedy but Smarter"
**Maximizes captures with 3-ply lookahead**
- **Strength**: Weak | **Speed**: Very Fast
- **Best For**: Learning tactics, practice opponent
- **Quote**: *"I see food, I eat! MUST. CAPTURE. NOW! 🦛"*

#### ⚔️ Berserker - "Relentless Aggressor"
**Attacks without mercy!**
- **Strength**: Medium-Strong | **Speed**: Very Fast
- **Depth**: 5 (default, range 2-8)
- **Best For**: Learning defensive strategies, handling pressure
- **Quote**: *"ATTACK! Capture everything! No mercy! Only VICTORY! ⚔️"*

#### 🧘 Zen Master - "Perfect Harmony"
**Achieves balance between offense and defense**
- **Strength**: Very Strong | **Speed**: Medium
- **Depth**: 8 (default, range 4-11)
- **Technology**: Minimax with alpha-beta pruning
- **Best For**: Learning balanced strategy, classical Reversi
- **Quote**: *"Flow like water. The path of least resistance leads to victory."*

#### 🎭 The Trickster - "Mind Games Master"
**Makes unconventional moves to confuse opponents**
- **Strength**: Strong | **Speed**: Fast
- **Depth**: 6 (default, range 3-9)
- **Best For**: Handling unpredictable opponents, staying focused
- **Quote**: *"Chaos is a ladder. Are you ready to climb... or fall?"*

#### 🌑 The Shadow - "Silent Defender"
**Lurks in darkness, strikes from shadows**
- **Strength**: Strong | **Speed**: Medium
- **Depth**: 7 (default, range 3-10)
- **Technology**: Heuristic (positional evaluation)
- **Best For**: Defensive mastery, patient gameplay
- **Quote**: *"I am the shadows. I am the watcher. Your defeat is inevitable."*

#### 📜 Ancient Sage - "1000 Years of Wisdom"
**Knows every classical opening by heart!**
- **Strength**: Very Strong | **Speed**: Medium-Fast
- **Depth**: 7 (default, range 4-10)
- **Technology**: Bitboard + Opening Book (depth 20!) + Endgame Solver
- **Best For**: Learning classical theory, perfect openings
- **Quote**: *"I have studied every game ever played. Your moves are already written."*

#### 🌌 Quantum Mind - "Parallel Universe Explorer"
**Calculates 16 futures simultaneously!**
- **Strength**: Master | **Speed**: Fast
- **Depth**: 9 (default, range 5-12)
- **Technology**: Bitboard + 16 Parallel Threads + 256MB Transposition Table
- **Best For**: Ultimate challenge, expert players
- **Requirements**: 8+ CPU cores recommended
- **Quote**: *"I see all possible futures. In every timeline, you lose."*

#### 💀 Apocalypse - "THE ULTIMATE DESTROYER" ⚠️
**Everything. Everywhere. All at once.**
- **Strength**: GODLIKE | **Speed**: Adaptive (SLOW at depth >10)
- **Depth**: 11 (default, range 7-15)
- **Technology**: ALL 12 techniques combined!
  - Grandmaster Engine, Bitboard, Opening Book (depth 30!), 32 Parallel Threads
  - 1GB Transposition Table, Advanced Evaluator, Move Ordering, Killer Moves
  - Endgame Solver, Aspiration Windows, Iterative Deepening, Null-Move Pruning
- **Best For**: The ultimate challenge (defeat is almost certain!)
- **Requirements**: 8+ CPU cores, 2GB RAM, patience
- **⚠️ WARNING**: Depth 11 = 1-3 min/move, Depth 12+ = 5-10 min/move!
- **Quote**: *"I AM INEVITABLE. Resistance is futile. Your defeat is absolute."*

### Quick Comparison

**For Beginners:** Start with Human Player vs Alpha-Beta AI (level 3-4)

**For Learning:** Human Player vs Opening Scholar (level 5) + Show Opening enabled

**For Challenge:** Human Player vs The Oracle (level 5-8)

**For Speed Testing:** Bitboard Blitz vs The Oracle (tournament mode)

*See [ADDING_PLAYERS.md](docs/ADDING_PLAYERS.md) for creating custom player types*

### 📚 Detailed Player Documentation

Complete documentation for each player type is available in the `docs/players/` directory:

- **[Player Types Overview](docs/players/README.md)** - Complete guide and comparison
- **[Base Player Class](docs/players/Player.md)** - Foundation for all players
- **[Human Player](docs/players/HumanPlayer.md)** - Interactive gameplay
- **[Random Chaos](docs/players/Monkey.md)** - Random move generator
- **[Greedy Goblin](docs/players/GreedyPlayer.md)** - Maximize immediate captures
- **[Heuristic Scout](docs/players/HeuristicPlayer.md)** - Fast positional evaluation
- **[Alpha-Beta AI](docs/players/AIPlayer.md)** - Classic minimax implementation
- **[Opening Scholar](docs/players/AIPlayerBook.md)** - AI with opening book
- **[Bitboard Blitz](docs/players/AIPlayerBitboard.md)** - Ultra-fast bitboard engine
- **[The Oracle](docs/players/AIPlayerBitboardBook.md)** - Bitboard + opening book
- **[Parallel Oracle](docs/players/AIPlayerBitboardBookParallel.md)** - Multi-core AI
- **[Grandmaster](docs/players/AIPlayerGrandmaster.md)** - Ultimate AI with all features
- **[Network Player](docs/players/NetworkPlayer.md)** - Network play (not implemented)

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

Comprehensive tournament system with **12 pre-configured tournaments** ready to run!

### Quick Start - Interactive Tournament Selector ⭐

```bash
cd tournament
./select_tournament.sh
```

**Features:**
- ✨ Visual menu with all 12 tournaments
- 📊 Detailed info (players, games, runtime estimates)
- 🎨 Color-coded categories (Quick/Elite/Ultimate/Easy/Test)
- ✓ One-command tournament launch

### Available Tournaments (12 Configurations)

| Tournament | Players | Games | Time | Category |
|------------|---------|-------|------|----------|
| **Quick Tournament** | 9 | 144 | 10-15 min | ⚡ Best AI Showcase |
| **Tournament of Champions** | 7 | 294 | 45-60 min | 🏆 Epic Battle |
| **Grandmaster Challenge** | 6 | 150 | 30-45 min | 👑 Ultimate Test |
| **Elite Tournament** | 5 | 100 | 20-30 min | 🏆 Top Tier |
| **Beginner Friendly** | 5 | 60 | 3-5 min | 🎓 Learning |
| **Rapid Fire** | 3 | 60 | 1-2 min | ⚡ Ultra Fast |
| Plus 6 more specialized tournaments! | | | | |

### Tournament System Features

- **Round-Robin Format** - Every AI plays every other AI
- **Both Colors** - Each matchup played as Black and White
- **JSON Configuration** - Save and reuse tournament setups
- **Detailed Statistics** - Win rates, scores, move times, color advantage
- **Move History** - Optional complete game transcripts
- **Interactive Selection** - Easy-to-use menu system
- **Auto-Discovery** - Automatically finds all available AI types
- **Comprehensive Reports** - Saved to `tournament/reports/` with timestamps

### Running Tournaments

```bash
# Interactive selector (recommended)
./select_tournament.sh

# Quick tournament
./run_quick_tournament.sh

# Specific configuration
./run_tournament.sh elite_tournament.json

# Interactive configuration
python3 tournament.py
```

**Complete Documentation:**
- **[Tournament System Guide](tournament/README.md)** - Complete overview
- **[Tournament Configurations](tournament/ring/README.md)** - All 12 tournaments detailed
- **[Tournaments Guide](tournament/TOURNAMENTS_GUIDE.md)** - Usage guide and tips
- **[Configuration System](tournament/CONFIGURATION_SYSTEM.md)** - Technical reference

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

### Adding Custom Players

1. Create a new class inheriting from `Player`
2. Define `PLAYER_METADATA` with display name, description, and parameters
3. Implement `get_move(game, moves, control)` method
4. Add to `PlayerFactory.ALL_PLAYER_CLASSES`

*See `ADDING_PLAYERS.md` and `src/Players/CustomPlayerExample.py`*

### Creating Custom Evaluators

1. Inherit from `Evaluator`
2. Implement `evaluate(game)` method
3. Register in `PlayerFactory.EVALUATORS`

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

### Player Documentation
- **[Player Types Overview](docs/players/README.md)** - Complete player comparison and guide
- **[Individual Player Docs](docs/players/)** - Detailed documentation for each player type

### Technical Documentation
- **[Features Guide](docs/FEATURES.md)** - Complete feature list
- **[View Architecture](docs/VIEW_ARCHITECTURE.md)** - Modular view system (NEW in 3.1.0)
- **[Board Module](src/Board/README.md)** - Board and view components
- **[Adding Players](docs/ADDING_PLAYERS.md)** - Custom player development
- **[Bitboard Implementation](docs/BITBOARD_IMPLEMENTATION.md)** - Technical deep dive
- **[Grandmaster AI](docs/GRANDMASTER_AI.md)** - Ultimate AI documentation
- **[Strategy Improvements](docs/STRATEGY_IMPROVEMENTS.md)** - Advanced AI techniques
- **[Parallel Engine](docs/HOW_TO_USE_PARALLEL.md)** - Multi-core usage guide
- **[Build Guide](BUILD.md)** - Building distributions
- **[Changelog](CHANGELOG.md)** - Version history

### Tournament System Documentation
- **[Tournament System Guide](tournament/README.md)** - Complete tournament overview
- **[Tournaments Guide](tournament/TOURNAMENTS_GUIDE.md)** - All 12 tournaments detailed
- **[Tournament Configurations](tournament/ring/README.md)** - Configuration guide
- **[Configuration System](tournament/CONFIGURATION_SYSTEM.md)** - Technical reference

### Learn More About Reversi
- Wikipedia: http://en.wikipedia.org/wiki/Reversi
- Official Othello: http://www.fngo.it
- World Othello Federation: https://www.worldothello.org/

---

## 👤 Author

**Luca Amore**  
Email: luca.amore@gmail.com  
Website: https://www.lucaamore.com

---

**Have fun playing Reversi42!** 🎮🎉

