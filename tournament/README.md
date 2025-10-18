# Reversi42 Tournament System 🏆

Epic automated tournaments between legendary AI warriors with advanced statistical analysis!

## 🚀 Quick Start

### Method 1: Quick Battle (15 minutes) ⚡
```bash
cd tournament
./tournament.py --config ring/quick_battle.json
```

### Method 2: Interactive Setup
```bash
cd tournament
python3 tournament.py
```

Configure interactively:
- Number of players (2-8)
- AI type for each player
- Difficulty levels
- Games per matchup

---

## 🎮 6 Epic Tournaments

### ⚡ **Quick Battle** (15 min)
**File**: `quick_battle.json`  
**Players**: 5 | **Games**: 20 | **Est. Time**: 10-15 minutes

Fast-paced tournament for testing and practice!

```json
Players: Hungry Hippo, Berserker, Zen Master, The Shadow, Ancient Sage
```

**Perfect for**: Quick testing, practice sessions

---

### 🏛️ **Arena of Legends** (2-3 hours)
**File**: `arena_of_legends.json`  
**Players**: 8 | **Games**: 112 | **Est. Time**: 2-3 hours

Epic battle royale - ALL tiers compete for supremacy!

```json
Players: Random Chaos, Hungry Hippo, Berserker, Zen Master, 
         The Trickster, The Shadow, Ancient Sage, Quantum Mind
```

**Perfect for**: Complete tier analysis, comprehensive testing

---

### 🌑 **Shadow Wars** (1 hour)
**File**: `shadow_wars.json`  
**Players**: 4 | **Games**: 36 | **Est. Time**: 45-60 minutes

Defensive vs Aggressive - Strategic patience battles brutal force!

```json
Players: Berserker, The Shadow, Zen Master, Ancient Sage
```

**Perfect for**: Studying defensive vs aggressive strategies

---

### 🎭 **Mind Games Championship** (1.5 hours)
**File**: `mind_games.json`  
**Players**: 4 | **Games**: 48 | **Est. Time**: 1-1.5 hours

Psychological warfare - Trickster vs balanced minds vs shadow tactics!

```json
Players: The Trickster, Zen Master, The Shadow, Ancient Sage
```

**Perfect for**: Testing unconventional strategies and adaptability

---

### 🎲 **Chaos Unleashed** (25 min)
**File**: `chaos_unleashed.json`  
**Players**: 5 | **Games**: 40 | **Est. Time**: 15-25 minutes

Beginner's Arena - Pure chaos meets greedy hunger and berserker rage!

```json
Players: Random Chaos, Hungry Hippo (depth 2), Hungry Hippo (depth 4), 
         Berserker (depth 4), Berserker (depth 6)
```

**Perfect for**: Learning how depth affects performance

---

### 💀 **Apocalypse Rising** (3-5 HOURS) ⚠️
**File**: `apocalypse_rising.json`  
**Players**: 5 | **Games**: 40 | **Est. Time**: 3-5 hours

THE FINAL CHALLENGE - Elite warriors face the ultimate destroyer!

```json
Players: Ancient Sage, Quantum Mind, Zen Master, The Shadow, APOCALYPSE
```

**⚠️ WARNINGS**:
- EXTREMELY SLOW - Apocalypse at depth 10
- Requires powerful CPU (8+ cores recommended)
- Best run overnight or during breaks

**Perfect for**: Ultimate challenge - can anyone survive?

---

## 📋 Tournament Comparison

| Tournament | Players | Games | Time | Difficulty | Purpose |
|------------|---------|-------|------|------------|---------|
| ⚡ Quick Battle | 5 | 20 | 15 min | Easy | Quick testing |
| 🏛️ Arena of Legends | 8 | 112 | 2-3 hrs | All Tiers | Complete analysis |
| 🌑 Shadow Wars | 4 | 36 | 1 hr | Advanced | Strategy study |
| 🎭 Mind Games | 4 | 48 | 1.5 hrs | Advanced | Tactical analysis |
| 🎲 Chaos Unleashed | 5 | 40 | 25 min | Beginner | Learning |
| 💀 Apocalypse Rising | 5 | 40 | 3-5 hrs | LEGENDARY | Ultimate test |

---

## 🎯 Choose Your Tournament

### I want to...

**Quick test** → ⚡ Quick Battle (15 min)  
**Learn basics** → 🎲 Chaos Unleashed (25 min)  
**Study strategy** → 🌑 Shadow Wars (1 hr)  
**Test tactics** → 🎭 Mind Games (1.5 hrs)  
**Complete analysis** → 🏛️ Arena of Legends (2-3 hrs)  
**Ultimate challenge** → 💀 Apocalypse Rising (3-5 hrs) ⚠️

---

## 📁 Directory Structure

```
tournament/
├── README.md                    # This file
├── tournament.py                # Main tournament system
├── quick_tournament.py          # Quick tournament launcher
├── ring/                        # Tournament configurations
│   ├── quick_battle.json        # ⚡ Quick testing
│   ├── arena_of_legends.json   # 🏛️ All tiers compete
│   ├── shadow_wars.json         # 🌑 Defense vs Aggression
│   ├── mind_games.json          # 🎭 Psychological warfare
│   ├── chaos_unleashed.json    # 🎲 Beginner learning
│   └── apocalypse_rising.json  # 💀 FINAL BOSS
└── reports/                     # Auto-generated reports
    └── tournament_report_*.txt
```

---

## 🎯 Features

### Tournament System v3.1

✅ **JSON Configuration System**
- Reusable tournament configs
- Easy sharing and customization
- Save/load tournament setups

✅ **Advanced AI Support**
- All 8 epic players supported
- Custom depth configuration
- Thread configuration for parallel AIs

✅ **Statistical Analysis**
- Win/loss/draw statistics
- Head-to-head matchups
- Performance rankings
- Detailed move analysis

✅ **Report Generation**
- Comprehensive text reports
- Matchup matrices
- Performance statistics
- Auto-saved to `reports/`

---

## 💻 Running Tournaments

### From Config File
```bash
cd tournament
./tournament.py --config ring/quick_battle.json
```

### Save Current Tournament
```bash
./tournament.py --save-config ring/my_tournament.json
```

### Interactive Mode
```bash
./tournament.py
# Follow prompts to configure
```

---

## 📊 Configuration Format

### Example: `quick_battle.json`
```json
{
  "name": "Quick Battle",
  "description": "Fast-paced tournament for quick testing",
  "players": [
    {"type": "Hungry Hippo", "depth": 3},
    {"type": "Berserker", "depth": 5},
    {"type": "Zen Master", "depth": 6},
    {"type": "The Shadow", "depth": 6},
    {"type": "Ancient Sage", "depth": 6}
  ],
  "games_per_matchup": 2,
  "total_games": 20,
  "estimated_time": "10-15 minutes",
  "category": "QUICK",
  "purpose": "Quick testing and practice"
}
```

### Available Player Types

**Beginner Tier**:
- `Random Chaos` 🎲 - Pure randomness
- `Hungry Hippo` 🦛 - Greedy with lookahead

**Intermediate Tier**:
- `Berserker` ⚔️ - Aggressive
- `Zen Master` 🧘 - Balanced
- `The Trickster` 🎭 - Psychological

**Advanced Tier**:
- `The Shadow` 🌑 - Defensive
- `Ancient Sage` 📜 - Classical

**Expert/Legendary Tier**:
- `Quantum Mind` 🌌 - Parallel computation
- `Apocalypse` 💀 - GODLIKE (⚠️ SLOW)

---

## 📈 Understanding Results

### Report Sections

1. **Tournament Summary**
   - Total games played
   - Duration
   - Participants

2. **Final Rankings**
   - Win percentage
   - Total wins/losses/draws
   - Points (win=3, draw=1, loss=0)

3. **Head-to-Head Matrix**
   - Direct matchup results
   - Win rates between specific players

4. **Detailed Statistics**
   - Average game length
   - Performance consistency
   - Strength ratings

---

## 🎓 Tournament Strategy Guide

### For Learning
1. Start with **Chaos Unleashed** (beginner)
2. Progress to **Quick Battle** (mixed)
3. Try **Shadow Wars** or **Mind Games** (advanced)
4. Master **Arena of Legends** (all tiers)
5. Face **Apocalypse Rising** (legendary) ⚠️

### For Testing
- **Quick Battle**: Fast AI testing
- **Shadow Wars**: Strategy comparison
- **Mind Games**: Tactical analysis
- **Arena of Legends**: Comprehensive benchmarking

### For Fun
- **Chaos Unleashed**: Watch chaos unfold
- **Mind Games**: Psychological battles
- **Apocalypse Rising**: Watch the world burn 💀

---

## ⚙️ Advanced Configuration

### Custom Depth
```json
{
  "type": "Zen Master",
  "depth": 10,
  "description": "Deep meditation mode"
}
```

### Parallel Threads (Quantum Mind, Apocalypse)
```json
{
  "type": "Quantum Mind",
  "depth": 9,
  "threads": 16
}
```

### Multiple Depth Comparison
```json
"players": [
  {"type": "Berserker", "depth": 4},
  {"type": "Berserker", "depth": 6},
  {"type": "Berserker", "depth": 8}
]
```

---

## 💡 Pro Tips

1. **Start small**: Run Quick Battle before Arena of Legends
2. **Watch resources**: Quantum Mind and Apocalypse are CPU-hungry
3. **Save configs**: Create custom tournaments and share them
4. **Learn from results**: Study why certain AIs win
5. **Adjust depth**: Balance strength vs speed
6. **Be patient**: Apocalypse tournaments take HOURS

---

## 🐛 Troubleshooting

### Tournament too slow?
- Use lower depths
- Avoid Apocalypse or Quantum Mind (depth >9)
- Run Quick Battle or Chaos Unleashed instead

### Out of memory?
- Reduce thread count for Quantum Mind/Apocalypse
- Close other applications
- Use smaller tournaments

### CPU overheating?
- Lower thread counts
- Reduce depth
- Take breaks between tournaments

---

## 📚 Additional Resources

- [Player Documentation](../docs/players/README.md) - All AI players explained
- [Main README](../README.md) - Project overview
- [Features Guide](../docs/FEATURES.md) - All features

---

## 🎮 Quick Examples

### Run Quick Battle
```bash
cd tournament
./tournament.py --config ring/quick_battle.json
```

### Run Apocalypse Challenge
```bash
# ⚠️ WARNING: This will take 3-5 HOURS!
./tournament.py --config ring/apocalypse_rising.json
```

### Create Custom Tournament
```bash
# 1. Run interactive mode
./tournament.py

# 2. Configure your tournament
# 3. Save it
./tournament.py --save-config ring/my_custom.json

# 4. Run it anytime
./tournament.py --config ring/my_custom.json
```

---

**Ready to battle?** Choose your tournament and let the games begin! 🏆

*May the strongest AI win!* 💪
