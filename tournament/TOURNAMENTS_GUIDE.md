# Reversi42 Tournament Guide - Complete Reference

## 🎮 Quick Start

### Interactive Selection (Recommended)

The **easiest** way to run tournaments:

```bash
cd tournament
./select_tournament.sh
```

This interactive menu shows all 12 available tournaments with details!

### Run All Tournaments (Batch Mode) 🚀

Execute **all 12 tournaments** automatically:

```bash
cd tournament
./run_all_tournaments.sh
```

**Features:**
- Runs all 1,120 games across 12 tournaments
- Estimated time: ~4 hours
- Generates individual reports + batch summary
- Perfect for overnight testing or comprehensive analysis
- Shows progress for each tournament

**Background execution:**
```bash
# With nohup
nohup ./run_all_tournaments.sh > batch.log 2>&1 &

# With screen
screen -S tournaments
./run_all_tournaments.sh
# Ctrl+A+D to detach
```

## 📊 Tournament Catalog (12 Configurations)

### 🌟 Showcase Tournaments

#### 1. **Quick Tournament - Best AI Showcase**
```bash
./run_tournament.sh quick_tournament.json
```
- **File**: `quick_tournament.json`
- **Players**: 9 (Random → Grandmaster progression)
- **Total Games**: 144
- **Runtime**: ~10-15 minutes
- **Best For**: Overview of all AI capabilities
- **Includes**: Every AI category from weakest to strongest

#### 2. **Tournament of Champions**
```bash
./run_tournament.sh tournament_of_champions.json
```
- **File**: `tournament_of_champions.json`
- **Players**: 7 (one champion from each category)
- **Total Games**: 294
- **Runtime**: ~45-60 minutes
- **Best For**: Epic competitive battle
- **Includes**: Heuristic, Minimax, Book, Speed, Hybrid, Parallel, Ultimate

#### 3. **Grandmaster Challenge**
```bash
./run_tournament.sh grandmaster_challenge.json
```
- **File**: `grandmaster_challenge.json`
- **Players**: 6 (top AI + Grandmaster-11)
- **Total Games**: 150
- **Runtime**: ~30-45 minutes
- **Best For**: Testing if anyone can beat the ultimate AI
- **Challenge**: Grandmaster at depth 11 - can it be defeated?

### 🏆 Competitive Tournaments

#### 4. **Elite Tournament**
```bash
./run_tournament.sh elite_tournament.json
```
- **File**: `elite_tournament.json`
- **Players**: 5 (only the strongest)
- **Total Games**: 100
- **Runtime**: ~20-30 minutes
- **Best For**: High-level competitive analysis
- **Includes**: Opening Scholar-7, Bitboard-9, Oracle-9, Parallel-9, Grandmaster-10

### 📊 Analysis & Testing

#### 5. **Depth Progression**
```bash
./run_tournament.sh depth_progression.json
```
- **File**: `depth_progression.json`
- **Players**: 4 (same AI, depths 3/5/7/9)
- **Total Games**: 36
- **Runtime**: ~15-20 minutes
- **Best For**: Understanding how depth affects strength
- **Analysis**: Clear demonstration of search depth impact

#### 6. **Evaluator Comparison**
```bash
./run_tournament.sh evaluator_comparison.json
```
- **File**: `evaluator_comparison.json`
- **Players**: 4 (Standard/Advanced/Simple/Greedy evaluators)
- **Total Games**: 36
- **Runtime**: ~8-12 minutes
- **Best For**: Comparing evaluation functions
- **Analysis**: Which evaluation strategy works best?

#### 7. **Opening Book Showdown**
```bash
./run_tournament.sh opening_book_showdown.json
```
- **File**: `opening_book_showdown.json`
- **Players**: 4 (with/without book at depths 5 & 7)
- **Total Games**: 60
- **Runtime**: ~12-18 minutes
- **Best For**: Measuring opening book impact
- **Analysis**: Direct comparison of book effectiveness

#### 8. **Opening Book Test**
```bash
./run_tournament.sh opening_book_test.json
```
- **File**: `opening_book_test.json`
- **Players**: 4 (book variants)
- **Total Games**: 60
- **Runtime**: ~10-15 minutes
- **Best For**: Learning opening book value

### ⚡ Speed & Performance

#### 9. **Bitboard Benchmark**
```bash
./run_tournament.sh bitboard_benchmark.json
```
- **File**: `bitboard_benchmark.json`
- **Players**: 6 (all bitboard variants)
- **Total Games**: 60
- **Runtime**: ~8-12 minutes
- **Best For**: Performance showcase
- **Includes**: Bitboard-8/10, Oracle-8/10, Parallel-9, Grandmaster-10

#### 10. **Rapid Fire Championship**
```bash
./run_tournament.sh rapid_fire.json
```
- **File**: `rapid_fire.json`
- **Players**: 3 (instant-response only)
- **Total Games**: 60
- **Runtime**: ~1-2 minutes
- **Best For**: Ultra-fast results
- **Perfect For**: Quick testing

#### 11. **Speed Test**
```bash
./run_tournament.sh speed_test.json
```
- **File**: `speed_test.json`
- **Players**: 4 (fast players)
- **Total Games**: 60
- **Runtime**: ~2-3 minutes
- **Best For**: Performance baseline

### 🎓 Learning & Education

#### 12. **Beginner Friendly**
```bash
./run_tournament.sh beginner_friendly.json
```
- **File**: `beginner_friendly.json`
- **Players**: 5 (Random → AI-4 progression)
- **Total Games**: 60
- **Runtime**: ~3-5 minutes
- **Best For**: Learning AI basics
- **Perfect For**: Beginners understanding AI strength levels

## 📈 Tournament Selection Guide

### By Purpose

| Purpose | Recommended Tournament | Runtime |
|---------|------------------------|---------|
| **Quick overview** | Quick Tournament | ~10-15 min |
| **Learning basics** | Beginner Friendly | ~3-5 min |
| **Performance test** | Rapid Fire | ~1-2 min |
| **Deep analysis** | Tournament of Champions | ~45-60 min |
| **Ultimate challenge** | Grandmaster Challenge | ~30-45 min |
| **Speed showcase** | Bitboard Benchmark | ~8-12 min |
| **Opening study** | Opening Book Showdown | ~12-18 min |
| **Depth analysis** | Depth Progression | ~15-20 min |

### By Time Available

| Time Available | Recommended Tournaments |
|----------------|------------------------|
| **< 5 minutes** | Rapid Fire, Speed Test, Beginner Friendly |
| **5-15 minutes** | Quick Tournament, Bitboard Benchmark, Evaluator Comparison |
| **15-30 minutes** | Elite Tournament, Depth Progression, Opening Book tests |
| **30-60 minutes** | Grandmaster Challenge, Tournament of Champions |

### By Skill Level

| Player Level | Recommended Start |
|--------------|------------------|
| **Beginner** | Beginner Friendly → Quick Tournament |
| **Intermediate** | Quick Tournament → Elite Tournament |
| **Advanced** | Elite Tournament → Grandmaster Challenge |
| **Expert** | Tournament of Champions (full analysis) |

## 🎯 Understanding Results

### What to Look For

1. **Win Rates**: Who wins most games?
2. **Color Advantage**: Does Black or White have advantage?
3. **Average Scores**: How decisive are victories?
4. **Move Times**: Which AI is fastest?
5. **Head-to-Head**: Direct matchup results

### Report Sections

All tournaments generate comprehensive reports with:

1. **Tournament Overview** - Stats summary
2. **Overall Rankings** - Sorted by win rate
3. **Detailed Player Analysis** - Per-player breakdown
4. **Head-to-Head Matrix** - All matchup results
5. **Duration Analysis** - Game length stats
6. **Expert Analysis** - Key insights and recommendations
7. **Move History** - Full games (if enabled)

## 🔧 Advanced Usage

### Creating Custom Tournaments

See [ring/README.md](ring/README.md) for complete guide.

**Quick example:**

```json
{
  "name": "My Custom Tournament",
  "description": "Testing my favorite AI",
  "games_per_matchup": 3,
  "include_move_history": true,
  "players": [
    {"type": "AI", "name": "Player1", "difficulty": 6, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "Grandmaster", "name": "Champion", "difficulty": 10, "engine": "Grandmaster", "evaluator": "Advanced"}
  ]
}
```

Save as `ring/my_tournament.json` and run:
```bash
./run_tournament.sh my_tournament.json
```

### Command Line Options

```bash
# Interactive configuration
python3 tournament.py

# Load from file
python3 tournament.py --config ring/quick_tournament.json

# Save configuration
python3 tournament.py --save-config ring/my_config.json
```

## 📊 Tournament Statistics

| Tournament | Players | Games | Move History | Est. Time |
|------------|---------|-------|--------------|-----------|
| Quick Tournament | 9 | 144 | ✓ | 10-15 min |
| Tournament of Champions | 7 | 294 | ✓ | 45-60 min |
| Grandmaster Challenge | 6 | 150 | ✓ | 30-45 min |
| Elite Tournament | 5 | 100 | ✓ | 20-30 min |
| Depth Progression | 4 | 36 | ✓ | 15-20 min |
| Evaluator Comparison | 4 | 36 | ✓ | 8-12 min |
| Opening Book Showdown | 4 | 60 | ✓ | 12-18 min |
| Opening Book Test | 4 | 60 | ✓ | 10-15 min |
| Bitboard Benchmark | 6 | 60 | ✗ | 8-12 min |
| Rapid Fire | 3 | 60 | ✗ | 1-2 min |
| Speed Test | 4 | 60 | ✗ | 2-3 min |
| Beginner Friendly | 5 | 60 | ✗ | 3-5 min |

**Total Games Across All Tournaments**: 1,120 games!

## 🎓 Tips & Best Practices

### For Learning

1. Start with **Beginner Friendly** to understand basics
2. Move to **Quick Tournament** to see all AI types
3. Try **Depth Progression** to learn about search depth
4. Study **Opening Book Showdown** for opening theory

### For Testing

1. Use **Rapid Fire** for quick sanity checks
2. Use **Speed Test** for performance baseline
3. Use **Bitboard Benchmark** to showcase speed
4. Use **Elite Tournament** for serious testing

### For Competition

1. **Tournament of Champions** for comprehensive analysis
2. **Grandmaster Challenge** to test against the best
3. **Elite Tournament** for high-level competition
4. Custom tournaments for specific matchups

### For Analysis

1. Enable **move history** for detailed analysis
2. Use **Evaluator Comparison** to test strategies
3. Use **Depth Progression** to understand strength scaling
4. Study reports in `tournament/reports/` directory

## 🚀 Next Steps

1. **Run your first tournament**:
   ```bash
   cd tournament
   ./select_tournament.sh
   ```

2. **Try the quick tournament**:
   ```bash
   ./run_quick_tournament.sh
   ```

3. **Run comprehensive batch** (for complete testing):
   ```bash
   ./run_all_tournaments.sh
   ```
   - All 12 tournaments
   - 1,120 total games
   - ~4 hours execution
   - Perfect for overnight runs

4. **Create your own**:
   - See [ring/README.md](ring/README.md)
   - Copy an existing config
   - Modify and test

5. **Analyze results**:
   - Check `tournament/reports/`
   - Study rankings and head-to-head
   - Learn from move histories
   - Review batch summary (if using run_all_tournaments.sh)

## 📚 Additional Resources

- **[ring/README.md](ring/README.md)** - Configuration guide
- **[README.md](README.md)** - Tournament system overview
- **[CONFIGURATION_SYSTEM.md](CONFIGURATION_SYSTEM.md)** - Technical reference
- **[TOURNAMENT_USAGE.txt](TOURNAMENT_USAGE.txt)** - Quick usage guide

---

**Happy Tournament Playing!** 🏆

*Reversi42 Tournament System v3.1.0 - 12 Pre-Configured Tournaments*

