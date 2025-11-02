# Reversi42 AI Player Configuration Index

Complete directory of all AI players organized by tier and specialty.

## 📁 Directory Structure

```
players/configs/
├── 00_AI_CONFIG_TEMPLATE.yaml          # Complete configuration template
├── README.md                  # Main configuration guide
├── INDEX.md                   # This file - complete player directory
├── champion/                  # ELO 1800+ (3 players)
│   ├── divzero.yaml          # 💀 ELO 1880 - Ultimate Singularity
│   ├── the_oracle.yaml       # 🔮 ELO 1850 - Endgame Prophet
│   ├── fortress_eternal.yaml # 🏰 ELO 1800 - Defensive Master
│   └── README.md
├── advanced/                  # ELO 1600-1800 (3 players)
│   ├── the_strangler.yaml    # 🐙 ELO 1750 - Mobility Assassin
│   ├── the_executioner.yaml  # ⚔️  ELO 1770 - Ruthless Destroyer
│   ├── corner_reaper.yaml    # 👹 ELO 1720 - Corner Specialist
│   └── README.md
├── intermediate/              # ELO 1300-1600 (2 players)
│   ├── lightning_strike.yaml # ⚡ ELO 1400 - Blitz Master
│   ├── glitch_lord.yaml      # 👾 ELO 1500 - Chaotic Anomaly
│   └── README.md
├── beginner/                  # ELO 1000-1300 (2 players)
│   ├── blitz_demon.yaml      # 😈 ELO 1350 - Speed Incarnate
│   ├── zen_master.yaml       # 🧘 ELO 1250 - Enlightened One
│   └── README.md
└── premium/                   # Configurable (1 player)
    ├── apocalyptron.yaml     # ⚡ ELO varies - Ultimate Engine
    └── README.md
```

## 🏆 Complete Player Roster (11 Players)

### Champion Tier (ELO 1800+)

#### 💀 DIVZERO.EXE (ELO 1880)
- **File:** `champion/divzero.yaml`
- **Specialty:** Adaptive depth, ultimate power
- **Depth:** 8/12/16 (adaptive)
- **Speed:** Slow (10-30s/move)
- **Style:** Balanced ultra-deep
- **Best For:** Maximum challenge, tournament finals

#### 🔮 THE ORACLE (ELO 1850)
- **File:** `champion/the_oracle.yaml`
- **Specialty:** Endgame prophesy
- **Depth:** 7/9/14 (adaptive)
- **Speed:** Moderate (3-15s/move)
- **Style:** Endgame specialist (parity focus)
- **Best For:** Endgame mastery, prophetic calculation

#### 🏰 FORTRESS ETERNAL (ELO 1800)
- **File:** `champion/fortress_eternal.yaml`
- **Specialty:** Defensive stability
- **Depth:** 10 (iterative)
- **Speed:** Moderate (5-20s/move)
- **Style:** Defensive (stability 2.5x)
- **Best For:** Defensive play, solid positions

---

### Advanced Tier (ELO 1600-1800)

#### 🐙 THE STRANGLER (ELO 1750)
- **File:** `advanced/the_strangler.yaml`
- **Specialty:** Mobility warfare
- **Depth:** 9 (iterative)
- **Speed:** Fast-Moderate (2-8s/move)
- **Style:** Aggressive mobility (2.5x)
- **Best For:** Suffocation strategy, tempo control

#### ⚔️ THE EXECUTIONER (ELO 1770)
- **File:** `advanced/the_executioner.yaml`
- **Specialty:** Tactical destruction
- **Depth:** 9 (iterative)
- **Speed:** Moderate (2-8s/move)
- **Style:** Aggressive tactical
- **Best For:** Ruthless finishing, aggressive play

#### 👹 CORNER REAPER (ELO 1720)
- **File:** `advanced/corner_reaper.yaml`
- **Specialty:** Corner domination
- **Depth:** 9 (iterative)
- **Speed:** Moderate (2-8s/move)
- **Style:** Positional (corner 2x)
- **Best For:** Corner battles, positional mastery

---

### Intermediate Tier (ELO 1300-1600)

#### ⚡ LIGHTNING STRIKE (ELO 1400)
- **File:** `intermediate/lightning_strike.yaml`
- **Specialty:** Speed and instinct
- **Depth:** 4 (fixed)
- **Speed:** Instant (<100ms/move)
- **Style:** Positional-only
- **Best For:** Blitz games, rapid play

#### 👾 GLITCH LORD (ELO 1500)
- **File:** `intermediate/glitch_lord.yaml`
- **Specialty:** Unpredictable variety
- **Depth:** 7 (iterative)
- **Speed:** Fast (0.5-2s/move)
- **Style:** Balanced with randomization
- **Best For:** Varied games, fun matches

---

### Beginner Tier (ELO 1000-1300)

#### 😈 BLITZ DEMON (ELO 1350)
- **File:** `beginner/blitz_demon.yaml`
- **Specialty:** Pure speed
- **Depth:** 3 (fixed)
- **Speed:** Ultra-fast (<50ms/move)
- **Style:** Minimal (positional only)
- **Best For:** Bullet chess, instant feedback

#### 🧘 ZEN MASTER (ELO 1250)
- **File:** `beginner/zen_master.yaml`
- **Specialty:** Educational balance
- **Depth:** 5 (iterative)
- **Speed:** Patient (0.7-1.3s/move)
- **Style:** Perfectly balanced
- **Best For:** Learning, training, first AI opponent

---

### Premium Tier (Configurable)

#### ⚡ APOCALYPTRON (ELO 1600-1900+)
- **File:** `premium/apocalyptron.yaml`
- **Specialty:** Ultimate flexibility
- **Depth:** Configurable (7-16)
- **Speed:** Configurable
- **Style:** Fully customizable
- **Best For:** Custom tuning, tournament prep

---

## 📊 Quick Selection Guide

### By Playing Style

**Defensive Play:**
1. 🏰 FORTRESS ETERNAL (stability focus)
2. 🧘 ZEN MASTER (balanced defense)

**Aggressive Play:**
1. ⚔️ THE EXECUTIONER (ruthless)
2. 🐙 THE STRANGLER (mobility warfare)

**Positional Play:**
1. 👹 CORNER REAPER (corner specialist)
2. 🏰 FORTRESS ETERNAL (stable positions)

**Tactical Play:**
1. ⚔️ THE EXECUTIONER (tactical battles)
2. 💀 DIVZERO.EXE (deep tactics)

**Speed Play:**
1. 😈 BLITZ DEMON (ultra-fast)
2. ⚡ LIGHTNING STRIKE (blitz master)

**Learning:**
1. 🧘 ZEN MASTER (educational)
2. 👾 GLITCH LORD (varied games)

---

### By Time Available

**< 1 minute per game:**
- 😈 BLITZ DEMON (depth 3, <50ms)
- ⚡ LIGHTNING STRIKE (depth 4, <100ms)

**1-3 minutes per game:**
- 👾 GLITCH LORD (depth 7, ~1s)
- 🧘 ZEN MASTER (depth 5, ~1s)

**3-10 minutes per game:**
- 🐙 THE STRANGLER (depth 9, ~5s)
- ⚔️ THE EXECUTIONER (depth 9, ~5s)
- 👹 CORNER REAPER (depth 9, ~5s)

**10-30 minutes per game:**
- 🏰 FORTRESS ETERNAL (depth 10, ~10s)
- 🔮 THE ORACLE (depth 9 adaptive, ~8s)

**30+ minutes per game:**
- 💀 DIVZERO.EXE (depth 12 adaptive, ~20s)

---

### By Skill Level

**I'm New to Reversi:**
1. Start: 🧘 ZEN MASTER (learning)
2. Next: ⚡ LIGHTNING STRIKE (faster games)
3. Then: 👾 GLITCH LORD (variety)

**I'm Intermediate:**
1. Start: 👾 GLITCH LORD
2. Next: 👹 CORNER REAPER (positional)
3. Then: 🐙 THE STRANGLER (tactical)

**I'm Advanced:**
1. Start: ⚔️ THE EXECUTIONER
2. Next: 🏰 FORTRESS ETERNAL
3. Then: 🔮 THE ORACLE

**I'm Expert:**
1. Fight: 💀 DIVZERO.EXE
2. Tune: ⚡ APOCALYPTRON (custom)

---

## 🎯 Special Use Cases

### Tournament Play
- **Round Robin:** 🔮 THE ORACLE or 🏰 FORTRESS ETERNAL
- **Knockout:** 💀 DIVZERO.EXE
- **Blitz:** ⚡ LIGHTNING STRIKE

### Training
- **Beginner Training:** 🧘 ZEN MASTER (verbose mode)
- **Intermediate Training:** 👾 GLITCH LORD (variety)
- **Advanced Training:** Champion tier players

### Analysis
- **Position Analysis:** 💀 DIVZERO.EXE (deep calculation)
- **Opening Study:** Any with `show_options: true`
- **Endgame Study:** 🔮 THE ORACLE (depth 14)

### Entertainment
- **Varied Games:** 👾 GLITCH LORD (randomization)
- **Speed Chess:** 😈 BLITZ DEMON or ⚡ LIGHTNING STRIKE
- **Epic Battles:** 💀 DIVZERO vs 🔮 ORACLE

---

## 📈 ELO Progression Path

```
1250  🧘 ZEN MASTER (learning basics)
  ↓
1350  😈 BLITZ DEMON (speed practice)
  ↓
1400  ⚡ LIGHTNING STRIKE (tactical basics)
  ↓
1500  👾 GLITCH LORD (varied experience)
  ↓
1720  👹 CORNER REAPER (positional mastery)
  ↓
1750  🐙 THE STRANGLER (mobility warfare)
  ↓
1770  ⚔️ THE EXECUTIONER (tactical excellence)
  ↓
1800  🏰 FORTRESS ETERNAL (defensive mastery)
  ↓
1850  🔮 THE ORACLE (endgame prophesy)
  ↓
1880  💀 DIVZERO.EXE (the singularity)
  ↓
1900+ ⚡ APOCALYPTRON (fully optimized)
```

---

## 🔧 Quick Modifications

### Make Any Player Faster
```yaml
engine:
  depth:
    base: [reduce by 2-3]
  parallel:
    num_workers: [reduce or disable]
```

### Make Any Player Stronger
```yaml
engine:
  depth:
    base: [increase by 1-2]
  transposition_table:
    size_mb: [double the value]
```

### Add Learning Mode
```yaml
behavior:
  logging:
    level: "verbose"
    show_statistics: true
    show_thinking: true
opening_book:
  display:
    show_options: true
```

---

## 📝 File Naming Convention

Pattern: `[specialty]_[descriptor].yaml`

Examples:
- `divzero.yaml` - Single word name
- `the_oracle.yaml` - Prefix + name
- `fortress_eternal.yaml` - Compound name
- `lightning_strike.yaml` - Compound name

---

## 🎨 Avatar Files

Each player has a corresponding avatar in:
```
players/avatars/[tier]/[player_name].png
```

Example:
- Config: `champion/divzero.yaml`
- Avatar: `avatars/champion/divzero.png`

---

## 📚 Documentation

- **Complete Template:** `00_AI_CONFIG_TEMPLATE.yaml` (1500+ lines)
- **Usage Guide:** `README.md`
- **This Index:** `INDEX.md`
- **Tier Guides:** `[tier]/README.md`
- **Avatar Guide:** `../avatars/README.md`

---

## 🚀 Getting Started

1. **Choose a player** from the table above
2. **Load the config:**
   ```python
   from Players.config_loader import ConfigurableAIPlayer
   player = ConfigurableAIPlayer("players/configs/beginner/zen_master.yaml")
   ```
3. **Play a game!**

---

## 💡 Pro Tips

1. **Start with Beginner tier** even if experienced
2. **Enable verbose mode** for learning
3. **Try different styles** to find your favorite
4. **Customize configurations** for specific needs
5. **Use INDEX.md** (this file) as quick reference

---

Last Updated: 2025-11-02
Total Players: 11 (3 Champion, 3 Advanced, 2 Intermediate, 2 Beginner, 1 Premium)

