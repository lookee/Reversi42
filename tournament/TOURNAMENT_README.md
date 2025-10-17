# Reversi42 Tournament System

## Overview

The Reversi42 Tournament System allows you to run automated tournaments between AI players with comprehensive statistical analysis. Perfect for comparing different AI strategies, evaluators, and difficulty levels.

## Features

### 🎮 Tournament Capabilities
- **Multiple AI Types**: Minimax, Heuristic, Greedy, Random
- **Multiple Evaluators**: Standard, Advanced, Greedy
- **Configurable Difficulty**: Levels 1-10 for Minimax AI
- **Round-Robin Format**: Every player plays against every other player
- **Balanced Colors**: Equal games as Black and White

### 📊 Comprehensive Statistics

The tournament generates a detailed report including:

1. **Overall Rankings**
   - Win/Loss/Draw records
   - Win percentages
   - Average scores

2. **Detailed Player Analysis**
   - Performance as Black
   - Performance as White
   - Timing analysis (avg, median, min, max, std dev)
   - Total thinking time
   - Color advantage analysis

3. **Head-to-Head Matrix**
   - Win-Loss-Draw records for each matchup
   - Easy-to-read matchup table

4. **Game Duration Analysis**
   - Average, median, fastest, slowest
   - Total playing time

5. **Move Count Analysis**
   - Average moves per game
   - Min/max moves
   - Total moves played

6. **Expert Analysis**
   - Tournament champion
   - Most consistent player
   - Fastest thinker
   - Most aggressive player
   - Color advantage insights

## Quick Start

### Interactive Mode

Run the tournament with interactive configuration:

```bash
python3 tournament.py
```

You'll be asked to configure:
1. Number of AI players (2-10)
2. AI type for each player
3. Difficulty levels (for Minimax)
4. Games per matchup (1-20)

### Quick Tournament (Pre-configured)

Run a fast tournament with pre-configured players:

```bash
python3 quick_tournament.py
```

This runs a quick 4-player tournament with 2 games per matchup.

## AI Types Available

### 1. Minimax (Standard Evaluator)
- **Strategy**: Alpha-beta pruning with mobility and corner control
- **Strengths**: Balanced, strategic play
- **Best for**: General-purpose strong AI

### 2. Minimax (Advanced Evaluator)
- **Strategy**: Weighted positions with dynamic game phase evaluation
- **Strengths**: Sophisticated positional play
- **Best for**: Advanced strategic analysis

### 3. Minimax (Greedy Evaluator)
- **Strategy**: Minimax with piece count maximization
- **Strengths**: Aggressive immediate gains
- **Best for**: Short-term tactical play

### 4. Heuristic
- **Strategy**: Simple heuristics without full search
- **Strengths**: Fast, good enough for testing
- **Best for**: Baseline comparison

### 5. Greedy
- **Strategy**: Always captures maximum pieces immediately
- **Strengths**: Simple, predictable
- **Best for**: Demonstrating tactical weaknesses

### 6. Monkey (Random)
- **Strategy**: Random move selection
- **Strengths**: Baseline for comparison
- **Best for**: Control group

## Example Configuration

### Competitive Tournament
```python
players_config = [
    ("AI", "Minimax-Std-6", 6, "Minimax", "Standard"),
    ("AI", "Minimax-Adv-6", 6, "Minimax", "Advanced"),
    ("AI", "Minimax-Std-8", 8, "Minimax", "Standard"),
    ("AI", "Minimax-Adv-8", 8, "Minimax", "Advanced"),
]
games_per_matchup = 5
```

### Strategy Comparison
```python
players_config = [
    ("AI", "Standard-Eval", 6, "Minimax", "Standard"),
    ("AI", "Advanced-Eval", 6, "Minimax", "Advanced"),
    ("AI", "Greedy-Eval", 6, "Minimax", "Greedy"),
    ("AI", "Simple-Eval", 6, "Minimax", "Simple"),
]
games_per_matchup = 10
```

### Difficulty Ladder
```python
players_config = [
    ("AI", "Minimax-Level-4", 4, "Minimax", "Standard"),
    ("AI", "Minimax-Level-6", 6, "Minimax", "Standard"),
    ("AI", "Minimax-Level-8", 8, "Minimax", "Standard"),
    ("AI", "Minimax-Level-10", 10, "Minimax", "Standard"),
]
games_per_matchup = 3
```

## Sample Report

```
================================================================================
REVERSI42 TOURNAMENT - COMPREHENSIVE STATISTICAL REPORT
================================================================================

─────────────────────────────────────────────────────────────────────────────
1. TOURNAMENT OVERVIEW
─────────────────────────────────────────────────────────────────────────────
Total Players: 4
Total Games Played: 24
Games per Matchup: 2
Average Game Duration: 2.345s
Total Tournament Time: 56.28s
Average Moves per Game: 58.3

─────────────────────────────────────────────────────────────────────────────
2. OVERALL RANKINGS
─────────────────────────────────────────────────────────────────────────────
Rank  Player                      W     L     D    Win%   Avg Score
─────────────────────────────────────────────────────────────────────────────
1     Minimax-Adv-4              10     2     0    83.3%      35.42
2     Minimax-Std-4               8     4     0    66.7%      33.17
3     Minimax-Greedy-4            3     9     0    25.0%      28.83
4     GreedyPlayer                1    11     0     8.3%      22.58

[... detailed player analysis ...]
```

## Performance Metrics

### What is Tracked

For each player:
- **Games**: Total, as Black, as White
- **Results**: Wins, Losses, Draws (overall and by color)
- **Scores**: Total, average, by color
- **Timing**: Every move is timed
  - Average move time
  - Median move time
  - Fastest/slowest moves
  - Standard deviation
  - Total thinking time
- **Color Performance**: Win rates as Black vs White

### What You Can Learn

- **Best Overall Player**: Highest win rate
- **Color Bias**: Which players perform better with specific colors
- **Speed vs Quality**: Fast thinkers vs deep thinkers
- **Consistency**: Standard deviation in performance
- **Matchup Advantages**: Head-to-head performance
- **Evaluation Quality**: Compare different evaluators at same depth

## Tips for Analysis

### Comparing Evaluators
Set same difficulty for all Minimax players, vary only the evaluator:
- Shows which evaluation function is most effective
- All players search to same depth, fair comparison

### Finding Optimal Difficulty
Create players at different difficulties with same evaluator:
- Shows diminishing returns of deeper search
- Helps find sweet spot for speed vs strength

### Testing New Strategies
Add your custom player against established baselines:
- Compare against Minimax-Standard as reference
- Check timing to ensure reasonable speed
- Analyze color performance for balance

## Output Files

Report files are automatically saved with timestamp:
```
tournament_report_20241017_143025.txt
```

Contains full statistical analysis ready for review.

## Technical Details

- **Headless Mode**: No GUI, maximum speed
- **Timing Precision**: Uses `perf_counter()` for accurate microsecond timing
- **Statistics**: Uses Python's `statistics` module for robust calculations
- **Round-Robin**: Every player plays against every other player
- **Color Balance**: Each matchup played with reversed colors

## Limitations

- **AI Players Only**: No human players in tournaments
- **Fixed Board Size**: 8x8 standard Reversi
- **No Opening Books**: All games start from standard position
- **Memory**: Large tournaments (many games) keep all data in memory

## Future Enhancements

Potential additions:
- Swiss-system tournaments
- ELO rating system
- Opening book support
- Parallel game execution
- Real-time progress visualization
- JSON/CSV export for external analysis

---

Happy tournament running! 🎮🏆

