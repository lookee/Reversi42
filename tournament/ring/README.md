# Tournament Ring - Configuration Files

This directory contains JSON configuration files for pre-configured tournaments. These files allow you to define tournament settings once and run them repeatedly without manual configuration.

## 📁 Available Configurations (12 Tournaments)

### Featured Tournaments ⭐

#### `quick_tournament.json` - Best AI Showcase
- **Players**: 9 (comprehensive progression: Random → Grandmaster)
- **Includes**: Full spectrum from basic to ultimate AI
- **Games/Matchup**: 2 | **Total**: 144 games
- **Move History**: ✓ Enabled
- **Runtime**: ~10-15 minutes
- **Best For**: General overview, showcasing all capabilities

#### `tournament_of_champions.json` - Epic Battle 🏆
- **Players**: 7 (one champion from each AI category)
- **Includes**: Heuristic, Minimax, Opening Book, Speed, Hybrid, Parallel, Ultimate
- **Games/Matchup**: 7 | **Total**: 294 games
- **Move History**: ✓ Enabled
- **Runtime**: ~45-60 minutes
- **Best For**: Comprehensive competitive analysis

#### `grandmaster_challenge.json` - Ultimate Challenge 👑
- **Players**: 6 (best AI variants vs Grandmaster-11)
- **Includes**: Expert AI, Scholar, Blitz-10, Oracle-10, Parallel-10, Grandmaster-11
- **Games/Matchup**: 5 | **Total**: 150 games
- **Move History**: ✓ Enabled
- **Runtime**: ~30-45 minutes
- **Best For**: Testing if anyone can beat the champion

### Competitive Tournaments 🏆

#### `elite_tournament.json` - Top Tier Battle
- **Players**: 5 (only the strongest)
- **Includes**: Opening Scholar, Bitboard Blitz, Oracle, Parallel Oracle, Grandmaster
- **Games/Matchup**: 5 | **Total**: 100 games
- **Move History**: ✓ Enabled
- **Runtime**: ~20-30 minutes
- **Best For**: High-level competitive play

### Analysis Tournaments 📊

#### `depth_progression.json` - Search Depth Analysis
- **Players**: 4 (same AI at depths 3, 5, 7, 9)
- **Games/Matchup**: 3 | **Total**: 36 games
- **Move History**: ✓ Enabled
- **Runtime**: ~15-20 minutes
- **Best For**: Understanding depth impact on strength

#### `evaluator_comparison.json` - Evaluation Functions Test
- **Players**: 4 (same depth, different evaluators)
- **Games/Matchup**: 3 | **Total**: 36 games
- **Move History**: ✓ Enabled
- **Runtime**: ~8-12 minutes
- **Best For**: Comparing evaluation strategies

#### `opening_book_showdown.json` - Book Impact Analysis
- **Players**: 4 (AI with/without book at depths 5 & 7)
- **Games/Matchup**: 5 | **Total**: 60 games
- **Move History**: ✓ Enabled
- **Runtime**: ~12-18 minutes
- **Best For**: Measuring opening book effectiveness

### Speed Tournaments ⚡

#### `bitboard_benchmark.json` - Performance Showcase
- **Players**: 6 (all bitboard variants)
- **Includes**: Bitboard-8/10, Oracle-8/10, Parallel-9, Grandmaster-10
- **Games/Matchup**: 2 | **Total**: 60 games
- **Move History**: ✗ Disabled (focus on speed)
- **Runtime**: ~8-12 minutes
- **Best For**: Performance benchmarking

#### `rapid_fire.json` - Ultra Fast Championship
- **Players**: 3 (instant-response only)
- **Includes**: Random, Greedy, Heuristic
- **Games/Matchup**: 10 | **Total**: 60 games
- **Move History**: ✗ Disabled
- **Runtime**: ~1-2 minutes
- **Best For**: Quick testing, rapid results

#### `speed_test.json` - Fast Players Test
- **Players**: 4 (Heuristic, Greedy, Monkey, AI-3)
- **Games/Matchup**: 5 | **Total**: 60 games
- **Move History**: ✗ Disabled
- **Runtime**: ~2-3 minutes
- **Best For**: Performance baseline

### Learning Tournaments 🎓

#### `beginner_friendly.json` - Learning Tournament
- **Players**: 5 (easy progression: Random → AI-4)
- **Includes**: Random, Greedy, Heuristic, AlphaBeta-3/4
- **Games/Matchup**: 3 | **Total**: 60 games
- **Move History**: ✗ Disabled (faster for beginners)
- **Runtime**: ~3-5 minutes
- **Best For**: Learning, understanding AI basics

#### `opening_book_test.json` - Opening Theory Test
- **Players**: 4 (with/without book)
- **Games/Matchup**: 5 | **Total**: 60 games
- **Move History**: ✓ Enabled
- **Runtime**: ~10-15 minutes
- **Best For**: Learning opening book value

## 🚀 Running Tournaments

### Method 1: Interactive Selector (RECOMMENDED) ⭐ NEW

```bash
cd tournament
./select_tournament.sh
```

**Features:**
- ✨ Visual menu with all tournaments
- 📊 Detailed info (players, games, runtime estimate)
- 🎨 Color-coded by category
- ✓ Confirmation before starting
- 🏆 Tournament badges (Quick/Elite/Ultimate/Easy/Test)

**Example Output:**
```
[1] ⚡ QUICK     Quick Tournament - Best AI Showcase
[2] 🏆 ELITE     Tournament of Champions
[3] 👑 ULTIMATE  Grandmaster Challenge
[4] 🎓 EASY      Beginner Friendly Tournament
...
```

### Method 2: Direct Shell Scripts

#### Run Quick Tournament
```bash
cd tournament
./run_quick_tournament.sh
```

#### Run Specific Configuration
```bash
cd tournament
./run_tournament.sh quick_tournament.json
./run_tournament.sh elite_tournament.json
./run_tournament.sh grandmaster_challenge.json
```

### Method 2: Using Python Directly

```bash
cd tournament
python3 tournament.py --config ring/quick_tournament.json
```

### Method 3: Using Relative Paths

```bash
# From anywhere in the project
python3 tournament/tournament.py --config tournament/ring/speed_test.json
```

## 📝 Configuration File Format

Tournament configuration files use JSON format with the following structure:

```json
{
  "name": "Tournament Name",
  "description": "Description of tournament purpose",
  "games_per_matchup": 2,
  "include_move_history": true,
  "players": [
    {
      "type": "AI",
      "name": "PlayerName",
      "difficulty": 6,
      "engine": "Minimax",
      "evaluator": "Standard"
    }
  ]
}
```

### Configuration Fields

#### Tournament Settings
- **`name`** (string): Tournament name displayed in output
- **`description`** (string): Optional description
- **`games_per_matchup`** (integer): Number of games each player pair plays (each color)
- **`include_move_history`** (boolean): Include full game notation in report

#### Player Configuration
Each player in the `players` array:

- **`type`** (string): Player type
  - `"AI"` - Standard minimax AI
  - `"AIBook"` - AI with opening book (57 sequences)
  - `"Bitboard"` - Ultra-fast bitboard AI (50-100x faster) ⭐ NEW
  - `"BitboardBook"` - The Oracle (bitboard + opening book) ⭐ NEW
  - `"ParallelOracle"` - Multi-core parallel AI (150-500x faster) ⭐ NEW
  - `"Grandmaster"` - Ultimate AI with all features (400-1000x faster) ⭐ NEW
  - `"Heuristic"` - Fast heuristic player
  - `"Greedy"` - Greedy player
  - `"Monkey"` - Random player
  
- **`name`** (string): Display name (should be unique)

- **`difficulty`** (integer): Search depth for AI players
  - AI/AIBook: 1-10 (standard)
  - Bitboard/BitboardBook: 1-12 (can go deeper due to speed)
  - ParallelOracle: 7-12 (optimized for parallel)
  - Grandmaster: 7-12 (optimized for deep analysis)
  - Not used for Heuristic, Greedy, Monkey

- **`engine`** (string): Engine type
  - `"Minimax"` - Alpha-beta minimax
  - `"Bitboard"` - Ultra-fast bitboard engine
  - `"ParallelBitboard"` - Multi-core parallel engine
  - `"Grandmaster"` - Advanced strategy engine
  - `"Heuristic"` - Heuristic evaluation
  - `"Random"` - Random selection

- **`evaluator`** (string): Evaluation function
  - `"Standard"` - Balanced evaluation
  - `"Advanced"` - Enhanced positional evaluation (recommended for Grandmaster)
  - `"Simple"` - Basic evaluation
  - `"Greedy"` - Piece count focused

## 🎯 Creating Custom Configurations

### Example: Ultimate AI Battle ⭐

Create `ring/ultimate_battle.json`:

```json
{
  "name": "Ultimate AI Battle",
  "description": "Top-tier AI competition with all advanced features",
  "games_per_matchup": 5,
  "include_move_history": true,
  "players": [
    {
      "type": "BitboardBook",
      "name": "The-Oracle-9",
      "difficulty": 9,
      "engine": "Bitboard",
      "evaluator": "Standard"
    },
    {
      "type": "ParallelOracle",
      "name": "Parallel-Oracle-9",
      "difficulty": 9,
      "engine": "ParallelBitboard",
      "evaluator": "Standard"
    },
    {
      "type": "Grandmaster",
      "name": "Grandmaster-10",
      "difficulty": 10,
      "engine": "Grandmaster",
      "evaluator": "Advanced"
    }
  ]
}
```

Run it:
```bash
./run_tournament.sh ultimate_battle.json
```

### Example: Difficulty Ladder

Create `ring/difficulty_ladder.json`:

```json
{
  "name": "Difficulty Ladder",
  "description": "Test AI at increasing difficulty levels",
  "games_per_matchup": 3,
  "include_move_history": false,
  "players": [
    {"type": "AI", "name": "Easy-3", "difficulty": 3, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "AI", "name": "Medium-5", "difficulty": 5, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "AI", "name": "Hard-7", "difficulty": 7, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "AI", "name": "Expert-9", "difficulty": 9, "engine": "Minimax", "evaluator": "Standard"}
  ]
}
```

## 📊 Output

All tournaments generate:
- **Console output**: Real-time game results
- **Report file**: Saved to `tournament/reports/tournament_report_YYYYMMDD_HHMMSS.txt`

Reports include:
- Overall rankings
- Win/loss/draw statistics
- Performance by color
- Head-to-head matrix
- Timing analysis
- Move history (if enabled)

## 🔧 Advanced Usage

### Save Interactive Configuration

You can save your interactive tournament configuration for later reuse:

```bash
python3 tournament.py --save-config ring/my_tournament.json
```

Then follow the prompts to configure your tournament. The configuration will be saved and can be run later:

```bash
./run_tournament.sh my_tournament.json
```

### Programmatic Creation

Create configurations programmatically in Python:

```python
from tournament import Tournament

# Create tournament
tournament = Tournament(
    players_config=[
        ("AI", "Player1", 6, "Minimax", "Standard"),
        ("AI", "Player2", 6, "Minimax", "Advanced"),
    ],
    games_per_matchup=3,
    include_move_history=True,
    name="My Tournament",
    description="Custom programmatic tournament"
)

# Save configuration
tournament.save_config('ring/my_config.json')
```

## 📚 Tips

1. **Start Small**: Begin with 2-4 players for quick results
2. **Move History**: Disable for large tournaments (saves space and time)
3. **Games per Matchup**: Use 3-5 for statistical significance
4. **Naming**: Use descriptive names for easy identification
5. **Backups**: Keep successful configurations for future reference

## 🎓 Tournament Design Guidelines

### For Testing
- Few players (2-4)
- High games per matchup (5-10)
- Move history optional

### For Showcasing
- Many players (6-8)
- Moderate games (2-3)
- Move history enabled

### For Research
- Controlled variables (same depth, different evaluators)
- High games per matchup (10-20)
- Move history enabled

## 🔗 See Also

- **[Tournament README](../README.md)** - Tournament system overview
- **[Tournament Usage Guide](../TOURNAMENT_USAGE.txt)** - Detailed usage instructions
- **[Main Project README](../../README.md)** - Project documentation

