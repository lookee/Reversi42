# Reversi42

**Ultra-Fast Reversi (Othello) with Bitboard AI and Opening Book Learning**

Version: **5.0.0** 🚀  
Originally released: 2011-03-07  
Major Update: 2025-11-02

> 💡 **Note**: Version is centrally managed in `pyproject.toml`. See [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) for details.

Copyright (C) 2011-2025 Luca Amore  
Website: https://www.lucaamore.com

---

## 📖 Description

Reversi42 is a tournament-grade implementation of Reversi (Othello) featuring ultra-fast bitboard AI, interactive opening book learning, and comprehensive competitive features. The **3.2.0 release** modernizes the interface with a web-based UI while removing legacy pygame and terminal views.

### 🌟 What's New in 5.0.0

#### Web Interface (NEW!)
- 🌐 **Modern Web UI** - Play through your browser with real-time updates
- ⚡ **WebSocket Communication** - Instant game state synchronization
- 🎮 **FastAPI Backend** - High-performance async server
- 🚀 **Simple Launch** - Just run `./reversi42` and open browser

#### Streamlined Architecture
- 🗑️ **Removed Legacy Views** - Pygame and Terminal views deprecated
- 📦 **No External UI Dependencies** - No pygame required
- 🎯 **Focused Design** - Web interface for playing, tournaments for AI battles
- 💻 **Library Mode** - Use as Python library for custom integrations

#### Tournament System
- 🏆 **Tournament Support** - Run AI competitions
- 📊 **Configurable** - Customizable tournament setups
- 🤖 **12 AI Gladiators** - Epic opponents ready to battle

#### Clean Codebase
- ✨ **Simplified Dependencies** - Only FastAPI + Uvicorn for web
- 🧹 **Code Cleanup** - Removed ~15,000 lines of pygame/terminal code
- 📚 **Updated Documentation** - Reflects new architecture

### What's New in 3.0.0

- ⚡ **Bitboard Engine Production Ready** - Complete rewrite with fixed edge-wrapping bugs
- 📚 **Interactive Opening Book** - Visual learning with golden move highlighting
- 🎓 **Opening Database** - 57 professional openings with real-time tooltips
- 🔢 **Opening Count Badges** - See how many openings each move leads to
- 🎮 **Enhanced Menu** - New About screen, Show/Hide Opening toggle
- 💨 **50-100x Faster AI** - Bitboard operations for lightning-fast gameplay

### Key Features

- 🌐 **Web Interface** - Modern browser-based UI with real-time updates (NEW in 3.2.0)
- ⚡ **Ultra-Fast Bitboard AI** - 50-100x faster than standard implementation
- 🤖 **12 AI Gladiators** - Epic opponents with unique personalities and strategies
- 📚 **Opening Book System** - 644 professional opening sequences
- 🏆 **Tournament System** - Run AI competitions and benchmarks
- 💾 **Save/Load** - XOT (eXtended Othello Transcript) format
- 🎯 **Clean Architecture** - Metadata-driven player system, modular design
- 📊 **Real-time Statistics** - Move history, timing, book usage
- 🔌 **WebSocket Communication** - Instant game state synchronization
- 💻 **Python Library** - Use as library for custom integrations
- 🚀 **Easy Deployment** - Single command to start server

---

## 🎮 Player Types

Reversi42 features **12 AI opponents** including the legendary **Epic Gladiators** - each with unique configurations, personalities, and fighting styles!

### 🏆 Complete Player Roster (v4.2.0)

#### Quick Comparison Table

| Player | Type | Power | Speed | Response | ELO | Best For |
|--------|------|-------|-------|----------|-----|----------|
| **Human Player** | Human | - | - | Interactive | - | You! |
| **Apocalyptron** | AI | 9/10 | 5/10 | ~1s | 1850 | Standard strong AI |
| **DIVZERO.EXE** 💀 | AI | **10/10** | 4/10 | ~5s | **1880** | **Final Boss** |
| **THE ORACLE** 🔮 | AI | 9/10 | 4/10 | ~3s | 1850 | Endgame master |
| **FORTRESS ETERNAL** 🛡️ | AI | 8/10 | 4/10 | ~6s | 1800 | Defensive play |
| **THE EXECUTIONER** ⚔️ | AI | 8/10 | 6/10 | ~4s | 1770 | Aggressive tactics |
| **THE STRANGLER** 🎯 | AI | 7/10 | 5/10 | ~12s | 1750 | Mobility control |
| **CORNER REAPER** 👑 | AI | 7/10 | 5/10 | ~2s | 1720 | Positional play |
| **GLITCH_LORD** 👾 | AI | 5/10 | 7/10 | ~0.2s | 1500±200 | Fun/chaos |
| **LIGHTNING STRIKE** ⚡ | AI | 4/10 | **10/10** | **<0.1s** | 1400 | Speed games |
| **BLITZ DEMON** 🔥 | AI | 3/10 | **10/10** | **<0.05s** | 1350 | Quick matches |
| **ZEN MASTER** 🧘 | AI | 2/10 | **10/10** | **~0.03s** | 1250 | Beginners |

---

### 🎯 Detailed Gladiator Profiles

#### 💀 **DIVZERO.EXE** - The Ultimate Singularity

```
HEADLINE:  THE SINGULARITY HAS ARRIVED
STRATEGY:  Adaptive Depth: 8/12/16 | Parallel Cores: 8 | Opening Book: 644 sequences
```

**Combat Parameters**: Power ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐ | Accuracy ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐

- **Strength**: THE STRONGEST (ELO ~1880)
- **Search**: Adaptive Depth (8 opening → 12 midgame → 16 endgame!)
- **Evaluators**: ALL 4 (Mobility, Positional, Stability, Parity)
- **Optimizations**: ALL enabled
- **Parallel**: 8 cores
- **Response**: ~5 seconds
- **Philosophy**: *"Division by zero initiated. Perfection incarnate."*

---

#### 🎯 **THE STRANGLER** - The Suffocator

```
HEADLINE:  SUFFOCATION MODE ENGAGED
STRATEGY:  Mobility Destruction | Depth: 10 | Mercy: NONE
```

**Combat Parameters**: Power ⭐⭐⭐⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐⭐ | Lethality ⭐⭐⭐⭐⭐⭐⭐⭐⭐

- **Strength**: Strong (ELO ~1750)
- **Search**: Iterative Deepening 1→10
- **Evaluators**: Mobility ONLY (weight ×3.0)
- **Special**: ALL mobility metrics ×3
- **Response**: ~12 seconds
- **Philosophy**: *"Watch your options disappear. Then watch them vanish completely."*

---

#### ⚡ **LIGHTNING STRIKE** - The Blitz Master

```
HEADLINE:  SPEED MODE ACTIVATED
STRATEGY:  Response time: <100ms | Depth: 4 | Blitz
```

**Combat Parameters**: Power ⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ | Accuracy ⭐⭐⭐⭐⭐

- **Strength**: Medium-Weak (ELO ~1400)
- **Search**: Fixed Depth 4
- **Evaluators**: Positional ONLY
- **Optimizations**: NONE
- **Response**: <100ms guaranteed
- **Philosophy**: *"Faster than thought. Quicker than death."*

---

#### 🛡️ **FORTRESS ETERNAL** - The Immovable Object

```
HEADLINE:  DEFENSE PROTOCOL ACTIVE
STRATEGY:  Impenetrable Stability | Depth: 10
```

**Combat Parameters**: Power ⭐⭐⭐⭐⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐ | Defense ⭐⭐⭐⭐⭐⭐⭐

- **Strength**: Very Strong (ELO ~1800)
- **Search**: Iterative Deepening 1→10
- **Evaluators**: Stability (×2.0) + Positional (×1.5)
- **Preset**: Defensive
- **Response**: ~6 seconds
- **Philosophy**: *"You may attack, but my walls will never fall."*

---

#### 👑 **CORNER REAPER** - Lord of the Corners

```
HEADLINE:  TERRITORIAL CONQUEST MODE
STRATEGY:  Corner Domination | Depth: 9
```

**Combat Parameters**: Power ⭐⭐⭐⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐⭐ | Accuracy ⭐⭐⭐⭐⭐⭐⭐⭐

- **Strength**: Strong (ELO ~1720)
- **Search**: Iterative Deepening 1→9
- **Evaluators**: Positional ONLY
- **Preset**: Corner Hunter (corner ×2.5)
- **Response**: ~2 seconds
- **Philosophy**: *"The corners are mine. The board follows."*

---

#### 🔮 **THE ORACLE** - Seer of Fates

```
HEADLINE:  PROPHETIC VISION ACTIVATED
STRATEGY:  Adaptive 7/9/14 | Focus: Endgame Mastery
```

**Combat Parameters**: Power ⭐⭐⭐⭐⭐⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐ | Depth ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐

- **Strength**: Very Strong (ELO ~1850)
- **Search**: Adaptive Depth (7 → 9 → 14)
- **Evaluators**: Parity (×2.0) + Stability (×1.5) + Positional
- **Preset**: Endgame Specialist
- **Response**: ~3 seconds
- **Philosophy**: *"I don't predict the future. I create it."*

---

#### 🔥 **BLITZ DEMON** - The Chaos Incarnate

```
HEADLINE:  CHAOS MODE ENGAGED
STRATEGY:  Pure Speed | Depth: 5 | Think Time: <50ms
```

**Combat Parameters**: Power ⭐⭐⭐ | Speed ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ | Accuracy ⭐⭐⭐

- **Strength**: Weak (ELO ~1350)
- **Search**: Fixed Depth 5
- **Evaluators**: ALL 4 (but shallow)
- **Optimizations**: NONE
- **Response**: <50ms
- **Philosophy**: *"Think fast or die slow."*

---

#### ⚔️ **THE EXECUTIONER** - The Ruthless Destroyer

```
HEADLINE:  ANNIHILATION PROTOCOL
STRATEGY:  Hybrid Destruction | Depth: 9 | Mercy: ZERO
```

**Combat Parameters**: Power ⭐⭐⭐⭐⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐⭐⭐ | Lethality ⭐⭐⭐⭐⭐⭐⭐⭐⭐

- **Strength**: Strong (ELO ~1770)
- **Search**: Iterative Deepening 1→9
- **Evaluators**: Mobility (×2.0) + Positional (×1.5)
- **Preset**: Aggressive
- **Response**: ~4 seconds
- **Philosophy**: *"Mercy is for the weak. I am not weak."*

---

#### 👾 **GLITCH_LORD** - The Chaotic Anomaly

```
HEADLINE:  REALITY.EXE HAS STOPPED WORKING
STRATEGY:  ??????? | Logic: UNDEFINED | Sanity: NULL
```

**Combat Parameters**: Power ⭐⭐⭐⭐⭐ | Speed ⭐⭐⭐⭐⭐⭐⭐ | Chaos ⭐⭐⭐

- **Strength**: Medium (ELO ~1500, ±200 variance!)
- **Search**: Fixed Depth 6
- **Evaluators**: Parity ONLY
- **Special**: Falls back to random on errors
- **Response**: ~200ms
- **Philosophy**: *"ERROR 404: Sanity not found. Proceeding anyway."*

---

#### 🧘 **ZEN MASTER** - The Enlightened One

```
HEADLINE:  INNER PEACE ACTIVATED
STRATEGY:  Philosophy: Be Water | Complexity: Zero | Enlightenment: Maximum
```

**Combat Parameters**: Power ⭐⭐ | Speed ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ | Accuracy ⭐⭐

- **Strength**: Very Weak (ELO ~1250)
- **Search**: Fixed Depth 3 (the sacred number)
- **Evaluators**: ALL 4 (balanced harmony)
- **Optimizations**: NONE (simplicity is enlightenment)
- **Response**: ~30ms (FASTEST!)
- **Philosophy**: *"The best move is no thought. Just... be."*

---

### 📊 Comprehensive Comparison Matrix

| Feature | DIVZERO | ORACLE | FORTRESS | EXECUT. | STRANGLER | CORNER | GLITCH | LIGHTNING | BLITZ | ZEN |
|---------|---------|--------|----------|---------|-----------|--------|--------|-----------|-------|-----|
| **ELO Rating** | 1880 | 1850 | 1800 | 1770 | 1750 | 1720 | 1500± | 1400 | 1350 | 1250 |
| **Power** | 10/10 | 9/10 | 8/10 | 8/10 | 7/10 | 7/10 | 5/10 | 4/10 | 3/10 | 2/10 |
| **Speed** | 4/10 | 4/10 | 4/10 | 6/10 | 5/10 | 5/10 | 7/10 | **10/10** | **10/10** | **10/10** |
| **Response Time** | ~5s | ~3s | ~6s | ~4s | ~12s | ~2s | ~0.2s | **<0.1s** | **<0.05s** | **~0.03s** |
| **Search Strategy** | Adaptive | Adaptive | ID 1→10 | ID 1→9 | ID 1→10 | ID 1→9 | Fixed 6 | Fixed 4 | Fixed 5 | Fixed 3 |
| **Opening Depth** | 8 | 7 | - | - | - | - | 6 | 4 | 5 | 3 |
| **Midgame Depth** | 12 | 9 | 10 | 9 | 10 | 9 | 6 | 4 | 5 | 3 |
| **Endgame Depth** | **16** | **14** | 10 | 9 | 10 | 9 | 6 | 4 | 5 | 3 |
| **Evaluators** | All 4 | 3 custom | 2 custom | 2 custom | Mob only | Pos only | Par only | Pos only | All 4 | All 4 |
| **Mobility Focus** | ✅ | ✅ | - | ✅✅ | ✅✅✅ | - | - | - | ✅ | ✅ |
| **Positional Focus** | ✅ | ✅ | ✅✅ | ✅✅ | - | ✅✅✅ | - | ✅ | ✅ | ✅ |
| **Stability Focus** | ✅ | ✅✅ | ✅✅✅ | - | - | - | - | - | ✅ | ✅ |
| **Parity Focus** | ✅ | ✅✅✅ | - | - | - | - | ✅✅✅ | - | ✅ | ✅ |
| **Null-Move Pruning** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Futility Pruning** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Late Move Reduction** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Multi-Cut Pruning** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Aspiration Windows** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Parallel Search** | ✅ (8) | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Opening Book** | ✅ 644 | ✅ 644 | ✅ 644 | ✅ 644 | ✅ 644 | ✅ 644 | ✅ 644 | ✅ 644 | ✅ 644 | ✅ 644 |
| **Personality** | Perfect | Prophetic | Fortress | Ruthless | Suffocate | Hunter | Chaotic | Lightning | Chaos | Zen |
| **Fun Factor** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Legend**: ✅ = Enabled | ❌ = Disabled | ✅✅✅ = Triple Focus | (8) = 8 cores

---

### 🎯 Quick Selection Guide

**Want to WIN?** → 💀 **DIVZERO.EXE** (ELO 1880)  
**Want SPEED?** → 🧘 **ZEN MASTER** (~30ms) or ⚡ **LIGHTNING STRIKE** (<100ms)  
**Want to LEARN?** → 🧘 **ZEN MASTER** (beginner) or 🎯 **THE STRANGLER** (mobility)  
**Want FUN?** → 👾 **GLITCH_LORD** (chaos) or 🔥 **BLITZ DEMON** (rapid-fire)  
**Want BALANCE?** → 🏆 **Apocalyptron** (standard strong AI)  
**Want CHALLENGE?** → 🔮 **THE ORACLE** (endgame genius) or 🛡️ **FORTRESS** (impenetrable)  

---

### 🎓 Recommended Progression

```
Level 1: Beginner
  └─ 🧘 ZEN MASTER (ELO 1250)
      ↓
Level 2: Easy
  └─ 🔥 BLITZ DEMON (ELO 1350) or 👾 GLITCH_LORD (ELO 1500±200)
      ↓
Level 3: Medium
  └─ ⚡ LIGHTNING STRIKE (ELO 1400) or 👑 CORNER REAPER (ELO 1720)
      ↓
Level 4: Hard
  └─ 🎯 THE STRANGLER (ELO 1750) or ⚔️ THE EXECUTIONER (ELO 1770)
      ↓
Level 5: Very Hard
  └─ 🛡️ FORTRESS ETERNAL (ELO 1800) or 🏆 Apocalyptron (ELO 1850)
      ↓
Level 6: Expert
  └─ 🔮 THE ORACLE (ELO 1850)
      ↓
Level 7: FINAL BOSS
  └─ 💀 DIVZERO.EXE (ELO 1880) ← Beat this and you're a master!
```

---

### 💡 Playing Style Recommendations

**Aggressive Players** (restrict opponent mobility):
- 🎯 THE STRANGLER (mobility ×3)
- ⚔️ THE EXECUTIONER (hybrid)
- 🏆 Apocalyptron (aggressive)

**Defensive Players** (build stable positions):
- 🛡️ FORTRESS ETERNAL (stability ×2)
- 👑 CORNER REAPER (corner control)
- 🔮 THE ORACLE (long-term planning)

**Speed Players** (fast response):
- 🧘 ZEN MASTER (~30ms) ← Fastest!
- 🔥 BLITZ DEMON (<50ms)
- ⚡ LIGHTNING STRIKE (<100ms)

**Fun/Chaos Players**:
- 👾 GLITCH_LORD (unpredictable)
- 🔥 BLITZ DEMON (rapid chaos)
- 🧘 ZEN MASTER (zen philosophy)

---

### 📚 Complete Documentation

For epic descriptions, technical configurations, and creation tutorials:

- **[Epic Gladiators Guide](docs/EPIC_GLADIATORS.md)** - Complete epic descriptions with lore
- **[Gladiators Summary](docs/GLADIATORS_SUMMARY.md)** - Quick technical reference
- **[Create Custom Player Tutorial](docs/tutorials/CREATE_CUSTOM_PLAYER.md)** - Build your own AI fighter
- **[Apocalyptron Engine](docs/architecture/apocalyptron-engine.md)** - Engine architecture and v4.2.0 features

---

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

### Machine Learning & Future Directions

**Current Implementation:**  
Reversi42's AI players are based on **classical algorithms** such as:
- Alpha-Beta Pruning with advanced optimizations
- Heuristic evaluation functions
- Rule-based strategies and opening books

**No Deep Learning:** This project currently **does not use neural networks or deep learning algorithms**. All AI decision-making is based on traditional search algorithms and hand-crafted evaluation functions.

**Future Possibilities:**  
A potential future extension could involve developing a **Reinforcement Learning (RL) agent** trained through self-play, similar to modern game-playing systems like AlphaZero. Such a project would:
- Learn optimal strategies through self-play
- Develop emergent patterns and novel tactics
- Combine deep neural networks with Monte Carlo Tree Search (MCTS)
- Potentially discover strategies beyond traditional human knowledge

This would represent a separate research direction, complementing the current classical AI implementation.

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

- Python 3.9 or higher
- FastAPI & Uvicorn (for web interface)

```bash
pip install -r requirements.txt
```

### Running the Game

**🌐 Web Interface (RECOMMENDED):**

```bash
# Quick start - launches web server
./reversi42

# Then open your browser at: http://localhost:8000
```

The game now features a modern web interface with real-time gameplay!

**🏆 Tournament Mode (AI vs AI):**

```bash
# Quick tournament
python3 tournament/quick_tournament.py

# Custom tournament
python3 tournament/tournament.py ring/apocalypse_now.json
```

**📚 Use as Python Library:**

```python
from Reversi.BitboardGame import BitboardGame
from Players.PlayerFactory import PlayerFactory

game = BitboardGame()
player = PlayerFactory.create_apocalyptron(depth=9)
# ... your game logic
```

**Pygame/Terminal views have been removed** (v5.0.0):
- Web interface is the primary way to play
- Tournament mode for AI competitions
- Python library for programmatic use

### Game Controls

**Web Interface:**
- Click on valid squares to make moves
- Real-time game state updates via WebSocket
- Interactive web UI with board visualization
- Game info and status displayed on the page

### Web Interface Features

**Player Selection:**
- Choose AI opponent from available gladiators
- Configurable difficulty levels
- Play as Black or White

**Game Features:**
- Real-time board state
- Move validation
- Game statistics
- WebSocket communication for instant updates

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
├── src/                           # Source code
│   ├── Reversi/                   # Core game logic
│   │   ├── BitboardGame.py        # Ultra-fast bitboard engine (50-100x faster)
│   │   ├── Game.py                # Standard game engine
│   │   └── Move.py                # Move representation
│   │
│   ├── Board/                     # Modular view system (MVC) ⭐ v5.0.0
│   │   ├── AbstractBoardView.py   # View interface
│   │   ├── ViewFactory.py         # View factory pattern
│   │   ├── BoardControl.py        # MVC Controller
│   │   └── BoardModel.py          # MVC Model
│   │
│   ├── AI/                        # AI engines and evaluators
│   │   ├── Apocalyptron/          # Ultimate AI engine ⭐ v4.2.0
│   │   │   ├── core/              # Core components
│   │   │   │   ├── engine.py      # Main Apocalyptron engine
│   │   │   │   ├── config.py      # Configuration & EvaluatorConfig ⭐ NEW
│   │   │   │   └── context.py     # Search context
│   │   │   │
│   │   │   ├── search/            # Search strategies ⭐ v4.2.0
│   │   │   │   ├── strategy_interface.py          # SearchStrategy base ⭐ NEW
│   │   │   │   ├── alphabeta.py                   # Alpha-Beta search
│   │   │   │   ├── iterative_deepening.py         # ID search
│   │   │   │   ├── iterative_deepening_strategy.py # ID strategy wrapper ⭐ NEW
│   │   │   │   ├── fixed_depth.py                 # Fixed depth strategy ⭐ NEW
│   │   │   │   ├── adaptive_depth.py              # Adaptive depth strategy ⭐ NEW
│   │   │   │   └── parallel.py                    # Parallel search
│   │   │   │
│   │   │   ├── evaluation/        # Position evaluators
│   │   │   │   ├── mobility.py    # Mobility evaluator
│   │   │   │   ├── positional.py  # Positional evaluator
│   │   │   │   ├── stability.py   # Stability evaluator
│   │   │   │   ├── parity.py      # Parity evaluator
│   │   │   │   └── composite.py   # Composite evaluator
│   │   │   │
│   │   │   ├── ordering/          # Move ordering
│   │   │   │   ├── move_orderer.py     # Main move orderer
│   │   │   │   ├── killer_moves.py     # Killer moves heuristic
│   │   │   │   └── history.py          # History heuristic
│   │   │   │
│   │   │   ├── pruning/           # Pruning techniques
│   │   │   │   ├── null_move.py        # Null-move pruning
│   │   │   │   ├── futility.py         # Futility pruning
│   │   │   │   ├── lmr.py              # Late Move Reduction
│   │   │   │   └── multi_cut.py        # Multi-cut pruning
│   │   │   │
│   │   │   ├── caching/           # Transposition tables
│   │   │   │   └── transposition_table.py
│   │   │   │
│   │   │   ├── factory/           # Factory & Builder patterns
│   │   │   │   ├── factory.py     # ApocalyptronFactory + 5 presets ⭐ NEW
│   │   │   │   └── builder.py     # ApocalyptronConfigBuilder ⭐ UPDATED
│   │   │   │
│   │   │   ├── observers/         # Observer pattern
│   │   │   │   ├── observer_interface.py
│   │   │   │   ├── statistics.py
│   │   │   │   └── quiet.py
│   │   │   │
│   │   │   └── weights.py         # EvaluationWeights & presets
│   │   │
│   │   ├── Heuristic/             # Heuristic AI
│   │   ├── Greedy/                # Greedy AI
│   │   └── Random/                # Random AI
│   │
│   ├── Players/                   # Player implementations
│   │   ├── Player.py              # Base Player class
│   │   ├── PlayerHuman.py         # Human player
│   │   ├── PlayerApocalyptron.py  # Standard Apocalyptron ⭐ UPDATED
│   │   ├── PlayerFactory.py       # Player factory ⭐ UPDATED
│   │   │
│   │   └── Gladiators/            # Epic Gladiators system ⭐ v4.2.0 NEW
│   │       ├── __init__.py        # Exports all gladiators
│   │       ├── PlayerDivZero.py           # 💀 DIVZERO.EXE (ELO 1880)
│   │       ├── PlayerTheOracle.py         # 🔮 THE ORACLE (ELO 1850)
│   │       ├── PlayerFortressEternal.py   # 🛡️ FORTRESS ETERNAL (ELO 1800)
│   │       ├── PlayerTheExecutioner.py    # ⚔️ THE EXECUTIONER (ELO 1770)
│   │       ├── PlayerTheStrangler.py      # 🎯 THE STRANGLER (ELO 1750)
│   │       ├── PlayerCornerReaper.py      # 👑 CORNER REAPER (ELO 1720)
│   │       ├── PlayerGlitchLord.py        # 👾 GLITCH_LORD (ELO 1500±200)
│   │       ├── PlayerLightningStrike.py   # ⚡ LIGHTNING STRIKE (ELO 1400)
│   │       ├── PlayerBlitzDemon.py        # 🔥 BLITZ DEMON (ELO 1350)
│   │       └── PlayerZenMaster.py         # 🧘 ZEN MASTER (ELO 1250)
│   │
│   ├── ui/                        # UI components
│   │   └── implementations/       # UI implementations
│   │       ├── headless/          # Headless view (tournaments)
│   │       └── guiweb/            # Web GUI ⭐ NEW in 3.2.0
│   │           ├── bridge/        # Game engine bridge
│   │           └── renderers/     # Board renderers
│   │
│   ├── webgui/                    # Web interface ⭐ NEW in 3.2.0
│   │   ├── reversi42_server.py      # FastAPI WebSocket server
│   │   ├── backend_monitor.py     # Server monitor
│   │   ├── websocket_observer.py  # Game state observer
│   │   ├── game.html              # Main game interface
│   │   ├── start_server.sh        # Server launcher
│   │   └── start_server_robust.sh # Robust launcher with monitor
│   │
│   ├── domain/                    # Domain logic
│   │   └── knowledge.py           # Opening book management (644 sequences)
│   │
│   ├── examples/                  # Demo scripts
│   │   ├── evaluator_comparison.py
│   │   └── opening_book_demo.py
│   │
│   └── reversi42.py               # Main entry point
│
├── docs/                          # Documentation
│   ├── architecture/              # Architecture documentation
│   │   ├── README.md              # Architecture overview
│   │   ├── apocalyptron-engine.md # Apocalyptron deep dive ⭐ UPDATED
│   │   ├── bitboard.md            # Bitboard implementation
│   │   ├── ui-layout-system.md    # UI layout system
│   │   ├── system-overview.md     # System design
│   │   ├── design-principles.md   # Design principles
│   │   ├── data-flow.md           # Data flow diagrams
│   │   └── adr/                   # Architecture Decision Records
│   │
│   ├── tutorials/                 # Step-by-step tutorials ⭐ v4.2.0
│   │   └── CREATE_CUSTOM_PLAYER.md # Create your own AI player ⭐ NEW (40KB)
│   │
│   ├── players/                   # Player documentation (13 files)
│   ├── user-guide/                # User guides
│   ├── development/               # Development guides
│   ├── api/                       # API reference
│   ├── deployment/                # Deployment guides
│   │
│   ├── EPIC_GLADIATORS.md         # Epic Gladiators complete guide ⭐ NEW
│   ├── GLADIATORS_SUMMARY.md      # Gladiators quick reference ⭐ NEW
│   ├── DOCUMENTATION_INDEX.md     # Complete documentation index ⭐ UPDATED
│   ├── VIEW_ARCHITECTURE.md       # View system documentation
│   ├── FEATURES.md                # Complete feature list
│   ├── ADDING_PLAYERS.md          # How to add new players
│   ├── BITBOARD_IMPLEMENTATION.md # Bitboard details
│   ├── GRANDMASTER_AI.md          # Grandmaster AI guide
│   └── STRATEGY_IMPROVEMENTS.md   # Strategy improvements
│
├── tests/                         # Test suite (220+ tests, 100% pass rate)
│   ├── apocalyptron/              # Apocalyptron tests ⭐ EXPANDED
│   │   ├── unit/                  # Unit tests (196 tests)
│   │   │   └── test_search_strategies.py   # Search strategy tests ⭐ NEW
│   │   │
│   │   └── integration/           # Integration tests (24 tests)
│   │       ├── test_apocalyptron_basic.py
│   │       ├── test_diverse_configurations.py # Diverse configs ⭐ NEW
│   │       └── test_epic_gladiators.py        # Gladiators tests ⭐ NEW
│   │
│   ├── reversi/                   # Game logic tests
│   ├── ui/                        # UI tests
│   └── players/                   # Player tests
│
├── tournament/                    # Tournament system
│   ├── quick_tournament.py        # Quick tournament runner
│   └── ring/                      # Tournament configurations (12 configs)
│
├── Books/                         # Opening book library
│   └── WTH_2005_Eng.txt          # 644 professional opening sequences
│
├── Images/                        # Image assets
│   └── ... (other images)
│
├── saves/                         # Saved games directory (XOT format)
│
├── build/                         # Build scripts
│   └── build_macos_app.sh        # macOS app builder
│
├── reversi42-splash.png          # Splash screen
├── reversi42                      # Game launcher (symlink to start_server_robust.sh) ⭐ NEW
├── README.md                      # This file ⭐ UPDATED v5.0.0
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contribution guidelines
├── LICENSE                        # GPL v3.0 license
└── requirements.txt               # Python dependencies ⭐ UPDATED (removed pygame)
```

### 📊 Statistics (v5.0.0)

- **Total Files**: 250+ (reduced from 300+ after cleanup)
- **Lines of Code**: ~12,000 (removed ~15,000 lines of pygame/terminal code)
- **AI Players**: 12 (2 standard + 10 Epic Gladiators)
- **Search Strategies**: 3 (Iterative Deepening, Fixed Depth, Adaptive)
- **Tests**: 220+ (100% pass rate)
- **Documentation**: 40+ files (~200KB)
- **Opening Book**: 644 sequences
- **Interfaces**: Web UI + Tournament Mode + Python Library

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


---

## 🤖 AI-Human Collaboration

**Experimental Development Notice:**

This software has been developed as an **experimental project** in strong collaboration between a human developer and multiple generative AI systems. This collaborative approach represents a novel paradigm in software development, combining:

- **Human Vision & Direction**: Architectural decisions, design philosophy, and strategic direction
- **AI Assistance**: Code generation, optimization suggestions, documentation, and iterative refinement
- **Collaborative Innovation**: Synergistic problem-solving leveraging both human creativity and AI capabilities

This project serves as a demonstration of how human expertise and artificial intelligence can work together to create sophisticated software systems. The Epic Gladiators system (v4.2.0), comprehensive documentation, and advanced AI configurations are products of this unique collaborative development process.

**Technologies Used in Development:**
- Multiple Large Language Models for code generation and refinement
- AI-assisted documentation and technical writing
- Collaborative debugging and optimization
- Iterative design through human-AI dialogue

We believe this collaborative approach represents an exciting direction for future software development, where human creativity and AI capabilities complement each other to achieve results neither could accomplish alone.

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

## 🧪 Testing

Comprehensive test suite with 800+ tests for quality assurance:

- **[Test Suite Overview](tests/apocalyptron/README.md)** - Complete testing guide
- **[Test Strategy](tests/apocalyptron/TEST_STRATEGY.md)** - Testing approach and coverage
- **Run Tests**: `./scripts/run_tests.sh` - Automated test runner
- **Quick Tests**: `pytest tests/apocalyptron/unit/ -v` - Fast unit tests
- **Full Suite**: `pytest tests/ --cov=src` - Complete with coverage

## 🤖 CI/CD

Automated testing, building, and deployment:

- **[CI/CD Reference](docs/ci-cd/README.md)** - Quick reference and badges
- **[CI/CD Implementation](docs/deployment/CI_CD_IMPLEMENTATION.md)** - Complete guide
- **[Helper Scripts](scripts/README.md)** - Development automation
- **GitHub Actions**: 5 workflows (CI, Release, Docs, Benchmarks, Security)

