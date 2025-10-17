# Reversi42

**A sophisticated Reversi (Othello) implementation with advanced AI**

Version: 0.2.0  
Originally released: 2011-03-07  
Enhanced: 2025-01-17

Copyright (C) 2011-2025 Luca Amore  
Website: https://www.lucaamore.com

---

## 📖 Description

Reversi42 is a feature-rich implementation of the classic Reversi (Othello) board game written in Python with Pygame. The game includes multiple AI opponents with different strategies, an opening book system, a comprehensive tournament mode, and extensive customization options.

### Key Features

- 🎮 **Full GUI** - Modern Pygame-based graphical interface
- 🤖 **Multiple AI Types** - From random to advanced alpha-beta pruning
- 📚 **Opening Book** - 57+ classic opening sequences for strong early game
- 🏆 **Tournament System** - Automated AI vs AI competitions with detailed statistics
- 💾 **Save/Load** - XOT (eXtended Othello Transcript) format support
- 🎯 **Modular Design** - Easy to extend with custom players and evaluators
- 🔄 **Resizable Window** - Adaptive graphics that scale with window size

---

## 🎮 Player Types

The game features a **metadata-driven player system** that automatically generates menu options from player definitions.

### Available Players

1. **Human** - Interactive player using mouse or keyboard
2. **AIPlayer** - Advanced AI with alpha-beta pruning (difficulty 1-10)
3. **AIPlayerBook** - AI with opening book support + minimax search ⭐ **RECOMMENDED**
4. **HeuristicPlayer** - Fast AI using position heuristics
5. **GreedyPlayer** - Maximizes immediate piece captures
6. **Monkey** - Random move selection (for testing)

### Experimental (Disabled)

- **AIPlayerBitboard** - Bitboard AI (disabled: bugs in late-game)
- **AIPlayerBitboardBook** - Bitboard + Book (disabled: uses bitboard internally)

*See `ADDING_PLAYERS.md` for creating custom player types*

---

## 🧠 AI Strategy

The AI system uses state-of-the-art game tree search techniques:

- **Alpha-Beta Pruning** - Efficient search tree exploration
- **Transposition Tables** - Position caching for speed
- **Move Ordering** - Prioritizes promising moves (corners, edges, mobility)
- **Opening Book** - Trie-based O(m) lookup for 57+ opening lines
- **Bitboard Representation** - 64-bit integer board state for 10-15x speedup
- **Modular Evaluators** - Pluggable evaluation functions

### Evaluation Functions

1. **StandardEvaluator** - Mobility and corner control
2. **SimpleEvaluator** - Basic piece count
3. **AdvancedEvaluator** - Weighted positions with game phase awareness
4. **GreedyEvaluator** - Immediate piece count maximization

---

## 📚 Opening Book System

AIPlayerBook uses a sophisticated opening book for tournament-level early game play:

- **57+ Opening Lines** - Diagonal, Tiger, Buffalo, Rose, and more
- **Named Openings** - Each sequence has a recognized name
- **Trie Structure** - O(m) lookup time where m = moves played
- **Instant Responses** - Book moves in << 1ms
- **Smart Fallback** - Minimax search when out of book

The opening book includes classic Reversi theory from masters and can be extended with custom sequences.

*Location: `Books/opening_book.txt`*  
*Format: `Opening Name | Move Sequence`*

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

**Keyboard:**
- `C` - Toggle cursor navigation mode
- `Arrow Keys` - Move cursor (in cursor mode)
- `ENTER/SPACE` - Select move at cursor
- `ESC` - Pause menu (save/load/resume)
- `Q` - Quick exit

### Pause Menu (ESC)

- Resume Game
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

