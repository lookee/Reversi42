# 🏆 Tournament Ring - Epic Gladiator Battles

This directory contains pre-configured tournament files for the Reversi42 Epic Gladiators system.

## 📋 Available Tournaments (14 Total)

### ⚡ Quick & Fast Tournaments

#### 1. **Quick Battle** (`quick_battle.json`)
- **Players**: 4 (DIVZERO, ORACLE, FORTRESS, STRANGLER)
- **Games**: 2 per matchup
- **Speed**: Fast (~5 minutes)
- **Best For**: Quick testing, warm-up

#### 2. **Speed Demons** (`speed_demons.json`)
- **Players**: 4 (ZEN, BLITZ, LIGHTNING, GLITCH)
- **Games**: 10 per matchup
- **Speed**: ULTRA FAST (<200ms per move!)
- **Best For**: Speed benchmarking, rapid testing

#### 3. **Blitz Madness** (`blitz_madness.json`)
- **Players**: 3 (LIGHTNING, BLITZ, ZEN)
- **Games**: 20 per matchup (!!)
- **Speed**: INSANELY FAST
- **Best For**: Rapid-fire action, speed records

---

### 👑 Championship Tournaments

#### 4. **Ultimate Arena** (`ultimate_arena.json`)
- **Players**: ALL 10 GLADIATORS
- **Games**: 2 per matchup
- **Duration**: ~1 hour
- **Best For**: Complete rankings, full leaderboard

#### 5. **Titans Clash** (`titans_clash.json`)
- **Players**: 5 strongest (ELO 1750+)
- **Games**: 4 per matchup
- **Duration**: ~30 minutes
- **Best For**: Elite competition, high-level play

#### 6. **Final Boss Challenge** (`final_boss_challenge.json`)
- **Players**: 6 (DIVZERO + 5 challengers)
- **Games**: 2 per matchup
- **Focus**: Can anyone defeat DIVZERO?
- **Best For**: Testing against the strongest

---

### 🎯 Specialized Tournaments

#### 7. **Mobility Assassins** (`mobility_assassins.json`)
- **Players**: 4 (STRANGLER, EXECUTIONER, CORNER, DIVZERO)
- **Focus**: Mobility control specialists
- **Games**: 3 per matchup
- **Best For**: Studying mobility strategies

#### 8. **Corner Wars** (`corner_wars.json`)
- **Players**: 4 (CORNER REAPER, FORTRESS, EXECUTIONER, DIVZERO)
- **Focus**: Positional and corner control
- **Games**: 3 per matchup
- **Best For**: Positional strategy analysis

#### 9. **Endgame Masters** (`endgame_masters.json`)
- **Players**: 3 (ORACLE, DIVZERO, FORTRESS)
- **Focus**: Long-term planning, endgame specialists
- **Games**: 4 per matchup
- **Best For**: Strategic depth analysis

---

### 👾 Fun & Chaotic Tournaments

#### 10. **Chaos Realm** (`chaos_realm.json`)
- **Players**: 4 (GLITCH, ZEN, Greedy, Random)
- **Style**: Unpredictable, bizarre
- **Games**: 6 per matchup
- **Best For**: Entertainment, chaos theory

#### 11. **Zen vs Chaos** (`zen_vs_chaos.json`)
- **Players**: 4 (ZEN, GLITCH, BLITZ, Random)
- **Theme**: Philosophy wars
- **Games**: 8 per matchup
- **Best For**: Fun, philosophical contrast

#### 12. **David vs Goliath** (`david_vs_goliath.json`)
- **Players**: 6 (titans vs underdogs)
- **Theme**: Weak vs Strong
- **Games**: 3 per matchup
- **Best For**: Upset potential, variety

---

### 🔥 Epic Long Tournaments

#### 13. **Apocalypse Now** (`apocalypse_now.json`)
- **Players**: 6 strongest
- **Games**: 6 per matchup
- **Duration**: ~1.5 hours
- **Special**: Includes move history
- **Best For**: Deep analysis, maximum carnage

#### 14. **Training Ground** (`training_ground.json`)
- **Players**: 5 weaker gladiators
- **Games**: 4 per matchup
- **Difficulty**: Beginner-friendly
- **Best For**: Testing weak players, learning

---

## 🚀 How to Run Tournaments

### Method 1: Quick Tournament Script (Recommended)

```bash
# List all tournaments
python quick_tournament.py --list

# Run a specific tournament
python quick_tournament.py quick      # Quick battle
python quick_tournament.py all        # All gladiators
python quick_tournament.py speed      # Speed demons
python quick_tournament.py boss       # Final boss challenge
```

### Method 2: Direct Tournament Script

```bash
# Run with config file
python tournament.py --config ring/quick_battle.json

# Run with custom settings
python tournament.py --config ring/ultimate_arena.json
```

---

## 📊 Tournament Quick Reference

| Tournament | Players | Games | Duration | Speed | Difficulty |
|------------|---------|-------|----------|-------|------------|
| Quick Battle | 4 | 2 | 5 min | Fast | Medium |
| Ultimate Arena | 10 | 2 | 60 min | Medium | High |
| Speed Demons | 4 | 10 | 5 min | **Ultra** | Low |
| Titans Clash | 5 | 4 | 30 min | Medium | **Very High** |
| Chaos Realm | 4 | 6 | 10 min | Fast | Low |
| Endgame Masters | 3 | 4 | 20 min | Slow | **Very High** |
| Mobility Assassins | 4 | 3 | 15 min | Medium | High |
| Corner Wars | 4 | 3 | 15 min | Medium | High |
| Zen vs Chaos | 4 | 8 | 10 min | Fast | Low |
| Final Boss | 6 | 2 | 25 min | Medium | **Max** |
| Training Ground | 5 | 4 | 15 min | Fast | **Low** |
| Apocalypse Now | 6 | 6 | 90 min | Slow | **Very High** |
| Blitz Madness | 3 | 20 | 5 min | **Ultra** | Low |
| David vs Goliath | 6 | 3 | 20 min | Mixed | Mixed |

---

## 🎯 Recommended Tournament Progression

### Beginner Path
1. **Training Ground** - Learn the basics
2. **Speed Demons** - Fast games, get comfortable
3. **Quick Battle** - Your first real challenge

### Intermediate Path
1. **Quick Battle** - Warm up
2. **Mobility Assassins** - Learn mobility control
3. **Corner Wars** - Master positional play
4. **David vs Goliath** - Mixed difficulty

### Advanced Path
1. **Titans Clash** - Elite competition
2. **Endgame Masters** - Strategic depth
3. **Final Boss Challenge** - Test against DIVZERO
4. **Ultimate Arena** - Complete rankings

### Expert Path
1. **Apocalypse Now** - Maximum carnage
2. **Final Boss Challenge** - Beat the singularity
3. **Titans Clash** - Prove your dominance

### Fun Path (Any Time!)
1. **Chaos Realm** - Unpredictable madness
2. **Zen vs Chaos** - Philosophy wars
3. **Blitz Madness** - Rapid fire action

---

## 🏅 Tournament Statistics

### By Speed
- **Ultra Fast (<10 min)**: 3 tournaments (Speed Demons, Blitz Madness, Chaos Realm)
- **Fast (10-20 min)**: 5 tournaments
- **Medium (20-40 min)**: 4 tournaments
- **Slow (>60 min)**: 2 tournaments (Ultimate Arena, Apocalypse Now)

### By Player Count
- **3 players**: 2 tournaments
- **4 players**: 7 tournaments
- **5 players**: 2 tournaments
- **6 players**: 3 tournaments
- **10 players**: 1 tournament (Ultimate Arena)

### By Difficulty
- **Low**: 4 tournaments (training-oriented)
- **Medium**: 4 tournaments
- **High**: 4 tournaments
- **Very High/Expert**: 2 tournaments (Titans, Apocalypse)

---

## 📝 Creating Custom Tournaments

To create your own tournament configuration:

1. Copy an existing JSON file as template
2. Edit the configuration:
   ```json
   {
     "name": "Your Tournament Name",
     "description": "Tournament description",
     "players": [
       {
         "type": "Apocalyptron",
         "name": "PLAYER_NAME",
         "difficulty": 9,
         "engine": "Apocalyptron",
         "evaluator": "Composite"
       }
     ],
     "games_per_matchup": 2,
     "include_move_history": false
   }
   ```
3. Save to `ring/your_tournament.json`
4. Run with: `python tournament.py --config ring/your_tournament.json`

### Available Player Types
- **Apocalyptron**: All gladiators (DIVZERO, ORACLE, FORTRESS, etc.)
- **Greedy**: Greedy Goblin
- **Monkey**: Random Chaos
- **Heuristic**: Heuristic Scout

---

## 🎮 Tips for Tournament Running

### Performance Tips
- Use `speed` tournament for quick benchmarking
- Use `blitz` for maximum speed testing
- Disable move history for faster tournaments

### Analysis Tips
- Enable move history in config for deep analysis
- Use `apocalypse` tournament for comprehensive stats
- Compare results across multiple runs

### Fun Tips
- Try `chaos` for entertainment
- Mix strong and weak players for upsets
- Create themed tournaments (speed only, mobility focus, etc.)

---

## 📚 Documentation

For more information:
- [Epic Gladiators Guide](../../docs/EPIC_GLADIATORS.md)
- [Gladiators Summary](../../docs/GLADIATORS_SUMMARY.md)
- [Tournament System Docs](../README.md)
- [Create Custom Player Tutorial](../../docs/tutorials/CREATE_CUSTOM_PLAYER.md)

---

**Total Tournaments**: 14 epic configurations ready to run!  
**Last Updated**: October 2025  
**Version**: 4.2.0

🏆 **CHOOSE YOUR ARENA. BEGIN THE BATTLE!** ⚔️

