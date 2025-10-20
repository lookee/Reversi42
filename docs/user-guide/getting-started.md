# Getting Started with Reversi42

Welcome to Reversi42! This guide will help you install and play your first game.

## Quick Start (5 Minutes)

### 1. Install

```bash
# Clone the repository
git clone https://github.com/lucaamore/reversi42.git
cd reversi42

# Install dependencies
pip install -r requirements.txt
```

### 2. Run

```bash
# Start the game
./reversi42
```

### 3. Play!

1. Main menu appears
2. Select **Black Player** → Choose "Human Player"
3. Select **White Player** → Choose "Alpha-Beta AI" (Level 3)
4. Click **Start Game**
5. Click on highlighted squares to make moves
6. Enjoy your first game!

## Installation Methods

### Method 1: From Source (Recommended)

**Requirements:**
- Python 3.9 or higher
- pip (Python package manager)
- git

**Steps:**

```bash
# 1. Clone repository
git clone https://github.com/lucaamore/reversi42.git
cd reversi42

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
./reversi42
# or
python3 src/reversi42.py
```

### Method 2: Direct Download

1. Download ZIP from [GitHub](https://github.com/lucaamore/reversi42)
2. Extract to your preferred location
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `./reversi42` or `python3 src/reversi42.py`

### Method 3: Pre-built Binary (Coming Soon)

Download from [Releases](https://github.com/lucaamore/reversi42/releases):
- macOS: `reversi42-macos.dmg`
- Windows: `reversi42-windows.exe`
- Linux: `reversi42-linux.AppImage`

## First Game Tutorial

### Step 1: Launch the Game

```bash
./reversi42
```

You'll see the main menu with the Reversi42 logo.

### Step 2: Choose Players

**Black Player (You):**
1. Click "Black Player"
2. Select "Human Player"
3. Click "Confirm"

**White Player (AI):**
1. Click "White Player"
2. Select "Alpha-Beta AI"
3. Choose difficulty level: **3** (good for beginners)
4. Click "Confirm"

### Step 3: Optional - Enable Opening Book

1. Click "Show Opening" toggle
2. This will highlight professional opening moves in gold
3. Helps you learn strong opening sequences!

### Step 4: Start Game

1. Click "Start Game"
2. Board appears with 4 pieces in the center
3. Black (you) moves first
4. Valid moves are highlighted

### Step 5: Make Your First Move

1. Look for highlighted squares (valid moves)
2. Click on any highlighted square
3. Your piece is placed and opponent pieces flip
4. AI automatically makes its move

### Step 6: Continue Playing

- Keep making moves when it's your turn
- Try to capture corners (they can't be flipped!)
- Plan ahead - think about your opponent's responses
- Game ends when neither player can move

### Step 7: View Results

When game ends:
- Final scores are displayed
- Winner is announced
- You can start a new game or return to menu

## Understanding the Interface

### Main Menu

- **Black Player**: Choose player type and difficulty for black
- **White Player**: Choose player type and difficulty for white
- **Show Opening / Hide Opening**: Toggle opening book highlights
- **Start Game**: Begin the match
- **Help**: View controls and player descriptions
- **About**: Game rules, credits, version info
- **Exit**: Quit the game

### Game Board

- **Board**: 8x8 grid with pieces
- **Valid Moves**: Highlighted in green/yellow
- **Golden Moves**: Opening book moves (when enabled)
- **Score Display**: Current piece count for each player
- **Move History**: List of moves made

### Controls

**Mouse:**
- Click highlighted squares to move
- Hover over golden moves to see opening names
- Click UI buttons to interact

**Keyboard:**
- `C` - Toggle cursor navigation mode
- `Arrow Keys` - Move cursor
- `ENTER` / `SPACE` - Select move at cursor
- `ESC` - Pause menu
- `Q` - Quick quit

## Choosing Your First AI Opponent

### For Complete Beginners

**Random Chaos**
- Makes random moves
- No strategy at all
- Good for: Understanding how pieces flip

**Greedy Goblin**
- Always takes maximum pieces
- Demonstrates why greedy play fails
- Good for: Learning not to be too greedy

### For Learning Players

**Heuristic Scout**
- Fast, position-based evaluation
- Medium difficulty
- Good for: Quick practice games

**Alpha-Beta AI (Level 1-3)**
- Classic AI with depth search
- Configurable difficulty
- Good for: Learning the game

### For Intermediate Players

**Alpha-Beta AI (Level 4-6)**
- Stronger depth search
- Good tactical play
- Good for: Improving your skills

**Opening Scholar**
- Knows 57 professional openings
- Strong early game
- Good for: Learning openings

### For Advanced Players

**Bitboard Blitz (Level 7-9)**
- Ultra-fast deep search
- Strong tactical play
- Good for: Serious challenge

**The Oracle**
- Bitboard + opening book
- Very strong play
- Good for: Testing your best strategies

**Apocalyptron (Level 9)** ⚡
- Default AI, grandmaster level
- All optimizations enabled
- Good for: Maximum challenge

## Interface Modes

### Pygame (Graphical) - Default

Beautiful graphical interface with:
- Resizable window
- Smooth animations
- Mouse controls
- Visual opening book highlights

**Best for:** Regular play, learning

### Terminal (ASCII)

Pure text interface:
- Works over SSH
- No graphics needed
- Keyboard-only controls
- Perfect for remote servers

**Usage:**
```bash
./reversi42 --view terminal
```

**Best for:** Remote play, minimal systems

### Headless (No UI)

No interface, automated only:
- For tournaments
- For testing
- For analysis

**Usage:**
```bash
./reversi42 --view headless
```

**Best for:** AI tournaments, benchmarking

## Common Beginner Questions

### How do I win?

The player with the most pieces at the end wins. Focus on:
1. Controlling corners
2. Maintaining mobility (having moves available)
3. Building stable pieces (can't be flipped)

### What are the golden highlighted moves?

When "Show Opening" is enabled, moves that appear in professional opening theory are highlighted in gold. Hover over them to see the opening name.

### Can I undo a move?

Yes! Press `ESC` and select "Undo Move" from the pause menu.

### Can I save my game?

Yes! Press `ESC` and select "Save Game". Games are saved in XOT format in the `saves/` directory.

### Why did the AI pass its turn?

If a player has no valid moves, they must pass. This is a normal part of the game.

### How do I make the AI easier/harder?

Change the AI difficulty level when selecting the player. Lower levels (1-3) are easier, higher levels (10-12) are extremely difficult.

## Next Steps

Now that you've played your first game:

1. **Learn the rules** - Read [Game Rules](game-rules.md)
2. **Improve your play** - See [Strategies Guide](strategies.md)
3. **Try different AIs** - Read [AI Opponents Guide](ai-opponents.md)
4. **Explore openings** - Check out [Opening Book Guide](opening-book.md)
5. **Run tournaments** - See [Tournament Guide](tournaments.md)

## Troubleshooting

### Game won't start

```bash
# Check Python version (need 3.9+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt

# Try running directly
python3 src/reversi42.py
```

### "pygame not found" error

```bash
pip install pygame
```

### Display issues

```bash
# Try terminal mode
./reversi42 --view terminal
```

### Need more help?

- Check the [FAQ](faq.md)
- Visit [GitHub Issues](https://github.com/lucaamore/reversi42/issues)
- Email: luca.amore@gmail.com

## Welcome to Reversi42!

You're now ready to enjoy Reversi42. Have fun, and may the best player win! 🎮

---

**Quick Reference Card:**

| Action | Command |
|--------|---------|
| Run game | `./reversi42` |
| Terminal mode | `./reversi42 --view terminal` |
| Pause game | `ESC` |
| Undo move | `ESC` → Undo Move |
| Save game | `ESC` → Save Game |
| Quit | `Q` or `ESC` → Exit |

**Remember:** Corners are powerful, mobility matters, and don't be too greedy!

