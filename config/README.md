# Configuration Directory

Central configuration for Reversi42 game and AI players.

## 📁 Structure

```
config/
├── game.yaml              # Default game configuration (Human vs AI)
├── README.md              # This file
└── players/               # AI player configurations
    ├── 00_AI_CONFIG_TEMPLATE.yaml   # Complete configuration template
    ├── INDEX.md           # Player directory
    ├── README.md          # Player configuration guide
    └── enabled/           # ← Auto-discovered players
        └── gladiators/
            ├── divzero.yaml            (11 AI players)
            ├── the_oracle.yaml
            ├── lightning_strike.yaml
            └── ...
```

## 🎮 Game Configuration

**File:** `game.yaml`

Defines the default game setup:

```yaml
players:
  black:
    type: "human"              # You play as Black (moves first)
    name: "Human Player"
    
  white:
    type: "ai"                 # AI plays as White
    ai_player: "LIGHTNING STRIKE"  # ELO 1400 (recommended)
```

### Quick Start

```bash
# Start game with default config
python start_game.py

# List available AI players
python start_game.py --list-players

# Use custom config
python start_game.py --config my_game.yaml
```

### Changing Opponent

Edit `game.yaml` and change `ai_player`:

```yaml
ai_player: "ZEN MASTER"       # Easy (ELO 1250)
ai_player: "LIGHTNING STRIKE" # Medium (ELO 1400) ← Default
ai_player: "THE ORACLE"       # Hard (ELO 1850)
ai_player: "DIVZERO.EXE"      # Extreme (ELO 1880)
```

See `game.yaml` for complete list and descriptions.

## 🤖 AI Players

**Directory:** `players/enabled/gladiators/`

11 AI players available, from beginner to champion:

| Player | ELO | Speed | Config File |
|--------|-----|-------|-------------|
| ZEN MASTER | 1250 | ~1s | zen_master.yaml |
| BLITZ DEMON | 1350 | <50ms | blitz_demon.yaml |
| LIGHTNING STRIKE | 1400 | <100ms | lightning_strike.yaml |
| GLITCH LORD | 1500 | ~1s | glitch_lord.yaml |
| CORNER REAPER | 1720 | ~5s | corner_reaper.yaml |
| THE STRANGLER | 1750 | ~5s | the_strangler.yaml |
| THE EXECUTIONER | 1770 | ~5s | the_executioner.yaml |
| FORTRESS ETERNAL | 1800 | ~10s | fortress_eternal.yaml |
| THE ORACLE | 1850 | ~8s | the_oracle.yaml |
| DIVZERO.EXE | 1880 | ~20s | divzero.yaml |
| APOCALYPTRON | Variable | Variable | apocalyptron.yaml |

### Auto-Discovery System

The Player Registry automatically discovers all `.yaml` files in:
- `config/players/enabled/` (recursive)
- Any subdirectory level
- Excluding templates and hidden files

**Add a new player:**
1. Create YAML file in `enabled/gladiators/`
2. Follow template structure
3. Restart application
4. Player is automatically available!

## 📝 Configuration Files

### game.yaml

**Purpose:** Default game setup  
**Contains:**
- Player selection (Human/AI)
- Game rules
- Display settings
- AI behavior

**Usage:** Loaded automatically by `start_game.py`

### players/00_AI_CONFIG_TEMPLATE.yaml

**Purpose:** Complete reference for creating AI players  
**Contains:**
- All available parameters (1500+ lines)
- Detailed documentation
- Examples and recommendations

**Usage:** Copy and customize to create new AI

### players/enabled/gladiators/*.yaml

**Purpose:** Individual AI player configurations  
**Contains:**
- Engine settings (depth, strategy)
- Evaluation weights
- Pruning optimizations
- Playing style

**Usage:** Auto-loaded by Player Registry

## 🏗️ System Architecture

### Components

1. **PlayerDiscovery** - Scans `enabled/` directory recursively
2. **ConfigLoader** - Loads and parses YAML files
3. **ConfigValidator** - Validates configuration integrity
4. **PlayerFactory** - Creates player instances
5. **PlayerRegistry** - Central orchestration (singleton)

### Flow

```
Application Start
    ↓
PlayerRegistry.init()
    ↓
PlayerDiscovery.discover()  ← Scans config/players/enabled/
    ↓
ConfigLoader.load(files)    ← Loads all YAML files
    ↓
ConfigValidator.validate()  ← Validates each config
    ↓
Registry stores valid configs
    ↓
[On demand]
    ↓
PlayerFactory.create()      ← Creates player instance
    ↓
Player ready for game
```

## 📊 Startup Log Example

```
================================================================================
🎮 Initializing Reversi42 AI Player Registry
================================================================================

📂 Discovering AI players...
  ✅ 💀 DIVZERO.EXE         (ELO: 1880, Category: champion)
  ✅ 🔮 THE ORACLE          (ELO: 1850, Category: champion)
  ✅ 🏰 FORTRESS ETERNAL    (ELO: 1800, Category: champion)
  ✅ ⚡ LIGHTNING STRIKE    (ELO: 1400, Category: intermediate)
  ✅ 🧘 ZEN MASTER          (ELO: 1250, Category: beginner)
  ... (11 total)

================================================================================
📊 Loading Summary:
  • Total configurations found: 11
  • Successfully loaded: 11
  • Failed to load: 0

  Players by category:
    • advanced: 3
    • beginner: 2
    • champion: 3
    • intermediate: 2
    • premium: 1
================================================================================
```

## 🔧 Common Tasks

### View All Players

```bash
python start_game.py --list-players
```

### Change Default Game

```bash
vim config/game.yaml
# Edit ai_player field
python start_game.py
```

### Create Custom AI

```bash
cp config/players/00_AI_CONFIG_TEMPLATE.yaml \
   config/players/enabled/gladiators/my_ai.yaml

vim config/players/enabled/gladiators/my_ai.yaml
# Edit configuration

# Player auto-discovered on next startup!
```

### AI vs AI Match

```yaml
# config/game.yaml
players:
  black:
    type: "ai"
    ai_player: "DIVZERO.EXE"
  white:
    type: "ai"
    ai_player: "THE ORACLE"
```

## 📚 Documentation

- **game.yaml** - Default game setup (196 lines, heavily commented)
- **players/00_AI_CONFIG_TEMPLATE.yaml** - Complete AI template (1587 lines)
- **players/README.md** - Player configuration guide
- **players/INDEX.md** - Player directory and quick reference
- **../GAME_CONFIGURATION.md** - User-friendly quick start guide
- **../docs/architecture/player-configuration-system.md** - Architecture details

## 🎯 Best Practices

1. **Version control:** Commit config files (track game setups)
2. **Backup:** Save custom configs before major changes
3. **Templates:** Use 00_AI_CONFIG_TEMPLATE.yaml as starting point
4. **Testing:** Test new configs with `start_game.py --list-players`
5. **Documentation:** Keep configs well-commented

## 🐛 Troubleshooting

### Player Not Found

```
ERROR: PlayerNotFoundError: Player 'XXX' not found
```

**Solution:**
- Check exact name (case-sensitive)
- Run `--list-players` to see available names
- Verify YAML file in `enabled/gladiators/`

### Invalid Configuration

```
ERROR: InvalidConfigError: Configuration validation failed
```

**Solution:**
- Check YAML syntax (indentation, colons)
- Compare with 00_AI_CONFIG_TEMPLATE.yaml
- Enable debug mode: `debug_mode: true`
- Check logs for specific errors

### Game Won't Start

**Checklist:**
1. Is `game.yaml` valid YAML?
2. Does ai_player match exactly?
3. Run with `--verbose` flag
4. Check `enabled/gladiators/` exists
5. Verify at least one player loaded

## 🔗 Related Files

- `../start_game.py` - Game launcher script
- `../examples/player_registry_demo.py` - System demo
- `../src/Players/config/` - Implementation code
- `../src/core/game_config.py` - Game config loader

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Production Ready

