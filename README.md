# Reversi42

**Ultra-Fast Reversi (Othello) with Bitboard AI and Opening Book Learning**

Version: **3.0.0** 🚀  
Originally released: 2011-03-07  
Major Update: 2025-10-18

Copyright (C) 2011-2025 Luca Amore  
Website: https://www.lucaamore.com

---

## 📖 Description

Reversi42 is a tournament-grade implementation of Reversi (Othello) featuring ultra-fast bitboard AI, interactive opening book learning, and comprehensive competitive features. The **3.0.0 release** introduces production-ready bitboard engines with 50-100x performance improvements.

### 🌟 What's New in 3.0.0

- ⚡ **Bitboard Engine Production Ready** - Complete rewrite with fixed edge-wrapping bugs
- 📚 **Interactive Opening Book** - Visual learning with golden move highlighting
- 🎓 **Opening Database** - 57 professional openings with real-time tooltips
- 🔢 **Opening Count Badges** - See how many openings each move leads to
- 🎮 **Enhanced Menu** - New About screen, Show/Hide Opening toggle
- 💨 **50-100x Faster AI** - Bitboard operations for lightning-fast gameplay

### Key Features

- 🎮 **Modern GUI** - Professional tournament-style interface with Pygame
- ⚡ **Ultra-Fast Bitboard AI** - 50-100x faster than standard implementation
- 🤖 **Multiple AI Types** - From random to deep bitboard search (depth 1-12)
- 📚 **Opening Book System** - 57+ classic openings with visual learning mode
- 🏆 **Tournament System** - Automated competitions with detailed analytics
- 💾 **Save/Load** - XOT (eXtended Othello Transcript) format
- 🎯 **Modular Design** - Metadata-driven player system
- 🔄 **Resizable Window** - Adaptive graphics
- 📊 **Real-time Statistics** - Move history, timing, book usage

---

## 🎮 Player Types

The game features a **metadata-driven player system** with automatic menu integration.

### Available Players (v3.0.0)

1. **Human** - Interactive player with mouse/keyboard navigation
2. **AI Player** - Advanced minimax with alpha-beta pruning (depth 1-10)
3. **AI with Opening Book** - Minimax + 57 opening sequences ⭐
4. **AI Bitboard (Ultra-Fast)** - 50-100x faster using bitboard representation (depth 1-12) ⚡
5. **AI Bitboard with Book (Fastest)** - Ultimate AI: Bitboard speed + Opening book 🏆 **RECOMMENDED**
6. **Heuristic Player** - Fast positional evaluation
7. **Greedy Player** - Maximizes immediate captures
8. **Monkey** - Random moves (for testing)

### Performance Comparison

| Player Type | Speed | Depth | Opening Book |
|------------|-------|-------|--------------|
| AI Player | 1x | 1-10 | ❌ |
| AI with Book | 1x | 1-10 | ✅ |
| AI Bitboard | **50-100x** | 1-12 | ❌ |
| **Bitboard with Book** | **50-100x** | 1-12 | ✅ |

*See `ADDING_PLAYERS.md` for creating custom player types*

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

Run automated AI vs AI tournaments with comprehensive analysis:

```bash
cd tournament
python3 tournament.py
```

### Features

- **Round-Robin Format** - Every AI plays every other AI
- **Both Colors** - Each matchup played as Black and White
- **Detailed Statistics** - Win rates, scores, move times, color advantage
- **Move History** - Optional complete game transcripts
- **Auto-Discovery** - Automatically finds all available AI types
- **Reports** - Saved to `tournament/reports/` with timestamps

*See `tournament/README.md` for complete documentation*

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
# Main entry point
./reversi42

# Or using Python
python3 src/reversi42.py
```

### Game Controls

**Mouse:**
- Click on highlighted squares to make moves
- Hover over golden moves to see opening names (when Show Opening enabled)

**Keyboard:**
- `C` - Toggle cursor navigation mode
- `Arrow Keys` - Move cursor (in cursor mode)
- `ENTER/SPACE` - Select move at cursor
- `ESC` - Pause menu (save/load/resume)
- `Q` - Quick exit

### Menu Options (NEW in 3.0.0)

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
│   ├── Board/         # GUI and board rendering
│   ├── AI/            # AI engines and evaluators
│   ├── Players/       # Player implementations
│   ├── examples/      # Demo scripts
│   └── reversi42.py   # Main entry point
├── tournament/        # Tournament system
├── Books/             # Opening book library
├── saves/             # Saved games (XOT format)
├── build/             # Build scripts
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

## 📚 Resources

**Learn More About Reversi:**
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

