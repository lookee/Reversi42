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
# Start the web server
./reversi42
```

### 3. Play!

1. Open your browser at **http://localhost:8000**
2. Web interface loads automatically
3. Click on highlighted squares to make moves
4. Enjoy your first game!

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
```

### Method 2: Direct Download

1. Download ZIP from [GitHub](https://github.com/lucaamore/reversi42)
2. Extract to your preferred location
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `./reversi42`

## First Game Tutorial

### Step 1: Launch the Server

```bash
./reversi42
```

The server will start and display:
```
Server running at http://localhost:8000
```

### Step 2: Open Browser

Open your web browser and navigate to:
```
http://localhost:8000
```

### Step 3: Start Playing

The web interface will load with:
- Game board visualization
- Move indicators
- Score display
- Game controls

Click on any valid square (highlighted) to make your move!

## Game Modes

### Web Interface (Default)

The modern web-based interface provides:
- Real-time game updates via WebSocket
- Interactive board
- Visual move validation
- Game statistics

**Usage:**
```bash
./reversi42
# Open browser at http://localhost:8000
```

### Tournament Mode

For AI vs AI competitions:

```bash
cd tournament
python3 quick_tournament.py
```

### Python Library

Use Reversi42 in your own code:

```python
from Reversi.BitboardGame import BitboardGame
from Players.PlayerFactory import PlayerFactory

# Create game
game = BitboardGame()

# Create AI player
ai_player = PlayerFactory.create_apocalyptron(depth=9)

# Your game logic here...
```

## Game Controls

### Web Interface

- **Click** on highlighted squares to make moves
- **Real-time updates** - no refresh needed
- **Visual feedback** - see valid moves instantly
- **Score tracking** - automatic score updates

## Choosing Your Opponent

Reversi42 features **12 AI opponents** with different difficulty levels:

### Beginner
- 🧘 **ZEN MASTER** (ELO 1250) - Easiest, great for learning

### Easy
- 🔥 **BLITZ DEMON** (ELO 1350) - Fast and simple
- ⚡ **LIGHTNING STRIKE** (ELO 1400) - Quick responses

### Medium
- 👾 **GLITCH_LORD** (ELO 1500) - Unpredictable
- 👑 **CORNER REAPER** (ELO 1720) - Corner specialist

### Hard
- 🎯 **THE STRANGLER** (ELO 1750) - Mobility focus
- ⚔️ **THE EXECUTIONER** (ELO 1770) - Aggressive

### Very Hard
- 🛡️ **FORTRESS ETERNAL** (ELO 1800) - Defensive master
- 🏆 **Apocalyptron** (ELO 1850) - Balanced strength

### Expert
- 🔮 **THE ORACLE** (ELO 1850) - Endgame prophet

### Final Boss
- 💀 **DIVZERO.EXE** (ELO 1880) - Ultimate challenge

## Troubleshooting

### Server won't start

**Problem**: Port 8000 already in use

**Solution**:
```bash
# Kill existing process
pkill -f backend_server

# Or use different port
python3 -m src.webgui.backend_server --port 8001
```

### Can't connect to server

**Problem**: Browser shows "connection refused"

**Solution**:
1. Check server is running
2. Verify correct URL: `http://localhost:8000`
3. Check firewall settings
4. Try different browser

### Dependencies missing

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
pip install -r requirements.txt
```

## Next Steps

Now that you've played your first game:

1. **Try different AI opponents** - Challenge yourself with harder opponents
2. **Run tournaments** - See AI battles with `python3 tournament/quick_tournament.py`
3. **Explore the code** - Use Reversi42 as a Python library
4. **Read documentation** - Learn about game strategy and AI techniques

## Additional Resources

- [FAQ](faq.md) - Common questions and answers
- [Game Rules](game-rules.md) - Complete Reversi/Othello rules
- [Epic Gladiators Guide](../EPIC_GLADIATORS.md) - Detailed AI opponent guide
- [Tournament System](../../tournament/README.md) - Running AI competitions
- [Architecture Documentation](../architecture/README.md) - Technical details

## Getting Help

- **Documentation**: See [User Guide](README.md)
- **Issues**: [GitHub Issues](https://github.com/lucaamore/reversi42/issues)
- **Source Code**: [GitHub Repository](https://github.com/lucaamore/reversi42)

---

**Enjoy playing Reversi42!** 🎮
