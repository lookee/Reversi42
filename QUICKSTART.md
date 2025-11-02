# 🚀 Quick Start - Reversi42

Get started playing in less than 1 minute!

---

## ⚡ Installation (1 minute)

**Requirements:**
- Python 3.9 or higher

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 🎮 Starting the Game

```bash
./reversi42
```

Then open your browser at: **http://localhost:8000**

---

## 🎯 How to Play

1. **Choose your AI opponent** from the web interface
2. **Click on valid squares** to make your move
3. **Objective:** Capture as many opponent pieces as possible
4. **Opening hints** (golden badges) can be toggled on/off with the book button 📚

### Basic Rules

- Played on an 8×8 board
- You must "sandwich" opponent pieces between two of your pieces to capture them
- You can only move where you capture at least one opponent piece
- The player with the most pieces at the end wins

---

## 🤖 Choose Your Opponent

**Beginners:**
- 🧘 **ZEN MASTER** (ELO 1250) - Perfect to start, very fast

**Intermediate:**
- ⚡ **LIGHTNING STRIKE** (ELO 1400) - Balanced between strength and speed
- 👑 **CORNER REAPER** (ELO 1720) - Positional play

**Expert:**
- 🛡️ **FORTRESS ETERNAL** (ELO 1800) - Impenetrable defense
- 🔮 **THE ORACLE** (ELO 1850) - Endgame master

**Final Boss:**
- 💀 **DIVZERO.EXE** (ELO 1880) - The strongest of them all!

---

## 🏆 Tournament Mode (AI vs AI)

Want to watch the AIs battle each other?

```bash
python3 tournament/quick_tournament.py
```

---

## 💾 Save Your Game

Games are automatically saved in the `saves/` folder in XOT format (human-readable text).

---

## 📚 Want to Learn More?

- **Complete README:** [README.md](README.md) - All features and documentation
- **Documentation:** [docs/](docs/) - Detailed guides
- **AI Gladiators:** [docs/EPIC_GLADIATORS.md](docs/EPIC_GLADIATORS.md) - Epic descriptions of all AIs

---

## 🆘 Problems?

**Server won't start?**
```bash
# Try with:
python3 src/webgui/backend_server.py
```

**Dependency errors?**
```bash
pip install fastapi uvicorn
```

---

**Have fun! 🎉**

