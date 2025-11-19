# AI Player Configurations

This directory contains YAML configuration files for creating custom AI players in Reversi42 without writing any Python code.

## 📋 Quick Start

### 1. Use an Existing Player

```python
from Players.config_loader import ConfigurableAIPlayer

# Load a pre-configured player
divzero = ConfigurableAIPlayer("players/configs/divzero.yaml")
lightning = ConfigurableAIPlayer("players/configs/lightning_strike.yaml")

# Use in a game
game.set_players(divzero, lightning)
```

### 2. Create Your Own Player

```bash
# Copy the template
cp 00_AI_CONFIG_TEMPLATE.yaml my_custom_player.yaml

# Edit with your favorite editor
vim my_custom_player.yaml

# Load in Python
my_player = ConfigurableAIPlayer("players/configs/my_custom_player.yaml")
```

### 3. Auto-Discovery (Factory Pattern)

```python
from Players.config_loader import ConfigPlayerFactory

# Automatically discover all .yaml files in this directory
factory = ConfigPlayerFactory("players/configs")

# List all available players
factory.list_players()

# Create player by name
oracle = factory.create_player("THE ORACLE")
```

## 📁 Files in This Directory

### Core Files

| File | Description |
|------|-------------|
| `00_AI_CONFIG_TEMPLATE.yaml` | **Complete reference template** with all parameters documented |
| `README.md` | This file - usage guide and documentation |

### Example Players

| File | Avatar | ELO | Speed | Description |
|------|--------|-----|-------|-------------|
| `divzero.yaml` | 💀 | 1880 | Slow | Champion-tier maximum power configuration |
| `lightning_strike.yaml` | ⚡ | 1400 | Instant | Blitz master optimized for <100ms responses |
| `the_oracle.yaml` | 🔮 | 1850 | Moderate | Endgame prophet with adaptive depth |

### Avatar Directory

Player avatar images are stored in `players/avatars/`:
- **Format:** PNG with transparency (recommended)
- **Size:** 512x512 pixels (square)
- **Naming:** `player_name.png` (lowercase, underscores)
- **Style:** Match player personality and theme

## 🎯 Configuration Categories

### By Strength

- **Beginner** (ELO 1000-1300): Depth 3-5, minimal optimizations
- **Intermediate** (ELO 1300-1600): Depth 5-8, standard optimizations  
- **Advanced** (ELO 1600-1800): Depth 8-11, all optimizations
- **Champion** (ELO 1800+): Depth 11+, maximum power

### By Speed

- **Instant** (<100ms): Depth 3-4, no parallelization
- **Fast** (100-500ms): Depth 5-6, light optimizations
- **Standard** (1-5s): Depth 7-9, full optimizations
- **Deep** (5-30s): Depth 10-12, adaptive depth
- **Extreme** (30s+): Depth 13+, tournament analysis

### By Style

- **Aggressive**: High mobility weight, fast tempo
- **Defensive**: High stability weight, solid positions
- **Balanced**: Equal weights, all-around play
- **Endgame Specialist**: Adaptive depth with deep endgame

## 🔧 Key Configuration Sections

### 1. Metadata (Cosmetic)

Defines how the player appears in menus and logs.

```yaml
metadata:
  name: "My AI"
  description: "Custom player description"
  estimated_elo: 1500
  icon: "🤖"
  avatar: "players/avatars/my_ai.png"  # Optional: Path to avatar image
```

**Avatar Support:**
- Supported formats: PNG, JPEG, SVG, GIF, WebP
- Recommended size: 512x512 pixels (square)
- Paths: Relative (from project root), absolute, or URL
- Fallback: If not found or null, uses icon emoji
- Used in: GUI, tournaments, player selection screens

### 2. Engine (Performance Critical)

Core search settings - biggest impact on strength and speed.

```yaml
engine:
  depth:
    base: 8              # Search depth (4-16)
    strategy: "iterative"  # fixed | iterative | adaptive
  parallel:
    enabled: true
    num_workers: null    # Auto-detect cores
```

**Key Trade-offs:**
- Depth +1 = ~3-10x slower (exponential)
- Parallel = 2-5x faster (with 4-8 cores)
- Iterative = ~20% overhead but better move ordering

### 3. Evaluation (Playing Style)

How positions are scored.

```yaml
evaluation:
  preset: "balanced"     # Quick start
  # OR custom evaluators:
  evaluators:
    - name: "mobility"
      weight: 1.0
    - name: "positional"
      weight: 1.5        # Emphasize corners/edges
```

**Presets:**
- `balanced`: Equal weights (safe default)
- `aggressive`: High mobility (attacking play)
- `defensive`: High stability (solid positions)
- `endgame_specialist`: Heavy parity (endgame focus)

### 4. Pruning (Speed Optimizations)

Advanced techniques for 10-100x speedup.

```yaml
pruning:
  null_move:
    enabled: true        # 30-60% speedup
  futility:
    enabled: true        # 15-30% speedup
  late_move_reduction:
    enabled: true        # 40-80% speedup
```

**Recommendation:** Enable all for maximum speed (no strength loss)

### 5. Opening Book

Professional opening theory integration.

```yaml
opening_book:
  enabled: true
  strategy: "evaluated"  # instant | evaluated | disabled
```

**Strategies:**
- `instant`: Play book move immediately (0ms)
- `evaluated`: Validate book with engine (modern)
- `disabled`: Engine only (no book)

## 📊 Example Configurations

### Speed Demon (Blitz)

```yaml
metadata:
  name: "Speed Demon"
  estimated_elo: 1350

engine:
  depth:
    base: 4
    strategy: "fixed"
  parallel:
    enabled: false

evaluation:
  evaluators:
    - name: "positional"
      enabled: true
      weight: 1.0
    # All others disabled

pruning:
  # All disabled (overhead not worth it at depth 4)

opening_book:
  strategy: "instant"
```

**Performance:** <100ms per move, ELO ~1350

### Balanced Player (Standard)

```yaml
metadata:
  name: "Balanced Bot"
  estimated_elo: 1600

engine:
  depth:
    base: 8
    strategy: "iterative"
  parallel:
    enabled: true
    num_workers: null

evaluation:
  preset: "balanced"

pruning:
  null_move:
    enabled: true
  futility:
    enabled: true
  late_move_reduction:
    enabled: true
  multi_cut:
    enabled: true

opening_book:
  strategy: "evaluated"
```

**Performance:** 1-3s per move, ELO ~1600

### Endgame Specialist

```yaml
metadata:
  name: "The Closer"
  estimated_elo: 1800

engine:
  depth:
    base: 9
    strategy: "adaptive"
    adaptive:
      opening: 7
      midgame: 9
      endgame: 14      # Deep endgame

evaluation:
  preset: "endgame_specialist"

pruning:
  # All enabled

opening_book:
  strategy: "evaluated"
```

**Performance:** 2-10s per move (faster in endgame), ELO ~1800

## 🎓 Tuning Guide

### Increase Strength

1. **Increase depth** (+1 ply = +100-150 ELO typically)
2. **Enable all pruning** (faster = can search deeper)
3. **Use iterative deepening** (better move ordering)
4. **Increase parallelization** (faster = deeper search)
5. **Tune evaluation weights** (playing style)

### Increase Speed

1. **Decrease depth** (-1 ply = ~3-10x faster)
2. **Use fixed strategy** (no iterative overhead)
3. **Disable parallel** (no distribution overhead, if depth < 6)
4. **Reduce evaluators** (positional only is fastest)
5. **Use instant book** (0ms for book moves)

### Common Mistakes

❌ **Too many evaluators at depth 4**
- Evaluation overhead dominates at shallow depth
- Use only positional for depth ≤ 5

❌ **Parallelization at depth 4-5**
- Overhead exceeds benefit
- Only enable for depth ≥ 6

❌ **Transposition table disabled**
- Almost always a net win (2-5x speedup)
- Only disable for extreme memory constraints

❌ **All pruning disabled**
- Loses 10-100x speedup
- Modern engines require pruning to be competitive

## 📈 Performance Expectations

### Time per Move by Depth (4 cores, all optimizations)

| Depth | Time | Nodes | Strength |
|-------|------|-------|----------|
| 4 | 50-100ms | 2K-5K | Beginner (1300) |
| 6 | 200-500ms | 20K-50K | Intermediate (1450) |
| 8 | 1-3s | 200K-500K | Advanced (1600) |
| 10 | 5-15s | 2M-5M | Expert (1750) |
| 12 | 20-60s | 20M-50M | Master (1850) |
| 14 | 1-5min | 200M-500M | Grandmaster (1950) |

**Notes:**
- Times assume midgame (moves 25-40)
- Endgame is faster (fewer legal moves)
- Opening with book is instant
- All optimizations enabled

### Speedup by Optimization

| Technique | Speedup | Risk |
|-----------|---------|------|
| Transposition table | 2-5x | None (always enable) |
| Parallel (4 cores) | 3-4x | None (if depth ≥ 6) |
| Null move pruning | 1.5-2.5x | None (safe) |
| Late move reduction | 1.4-2x | None (safe) |
| Futility pruning | 1.15-1.3x | None (safe) |
| Multi-cut | 1.15-1.25x | None (safe) |
| Aspiration windows | 1.2-1.3x | None (with iterative) |

**Total:** 10-100x faster than naive minimax

## 🔍 Validation

### Check Configuration Syntax

```python
from Players.config_loader import ConfigurableAIPlayer

try:
    player = ConfigurableAIPlayer("my_config.yaml")
    print("✅ Configuration valid!")
    print(f"Player: {player.name}")
    print(f"Icon: {player.metadata.get('icon', '🤖')}")
    print(f"Avatar: {player.metadata.get('avatar', 'None')}")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

### Verify Avatar Loading

```python
from Players.config_loader import ConfigurableAIPlayer
import os

player = ConfigurableAIPlayer("divzero.yaml")

# Check if avatar file exists
avatar_path = player.metadata.get('avatar')
if avatar_path:
    if os.path.exists(avatar_path):
        print(f"✅ Avatar found: {avatar_path}")
        file_size = os.path.getsize(avatar_path)
        print(f"   File size: {file_size / 1024:.1f} KB")
    else:
        print(f"⚠️  Avatar not found: {avatar_path}")
        print(f"   Using fallback icon: {player.metadata['icon']}")
else:
    print(f"ℹ️  No avatar configured, using icon: {player.metadata['icon']}")
```

### Test Performance

```python
import time

# Create player
player = ConfigurableAIPlayer("my_config.yaml")

# Time a move
start = time.time()
move = player.get_move(game, moves, None)
elapsed = time.time() - start

print(f"Move: {move}")
print(f"Time: {elapsed*1000:.1f} ms")
```

### Benchmark Against Others

```python
from tournament import run_match

player1 = ConfigurableAIPlayer("my_config.yaml")
player2 = ConfigurableAIPlayer("divzero.yaml")

results = run_match(player1, player2, num_games=10)
print(f"Score: {results['wins_p1']}-{results['wins_p2']}")
```

## 📚 Advanced Topics

### Time Management

```yaml
behavior:
  time:
    max_time_ms: 3000    # 3 second limit per move
```

Requires `strategy: "iterative"` to work properly. Engine will:
1. Complete depth 1, 2, 3... sequentially
2. Stop when time limit reached
3. Return best move from deepest complete iteration

### Adaptive Depth by Game Phase

```yaml
engine:
  depth:
    strategy: "adaptive"
    adaptive:
      opening: 7     # Moves 1-20: Shallow (rely on book)
      midgame: 10    # Moves 21-50: Deep (complex tactics)
      endgame: 14    # Moves 51-60: Very deep (exact calculation)
```

Best for **endgame specialists** - can see 14 moves ahead when it matters most.

### Custom Evaluation Weights

```yaml
evaluation:
  preset: null  # Disable preset
  evaluators:
    - name: "mobility"
      weight: 2.0  # Double weight (aggressive style)
    - name: "stability"
      weight: 0.5  # Half weight (less defensive)
  weights:
    corner_weight: 150  # Extra emphasis on corners
```

For **expert tuning** only - requires deep understanding.

## 🐛 Troubleshooting

### "Config file not found"

- Check file path (use absolute or relative to working directory)
- Verify file extension is `.yaml`

### "Missing required section: engine"

- Ensure all required sections present
- Use `00_AI_CONFIG_TEMPLATE.yaml` as starting point

### "Invalid depth value"

- Depth must be integer 1-20
- Practical range: 4-16

### Player is too slow

- Reduce `depth.base`
- Disable `parallel` if depth < 6
- Use `strategy: "fixed"`
- Reduce number of evaluators

### Player is too weak

- Increase `depth.base`
- Enable all pruning (faster = can search deeper)
- Use `preset: "balanced"`
- Enable all move ordering strategies

## 📖 Further Reading

- **Template:** `00_AI_CONFIG_TEMPLATE.yaml` - Complete parameter reference
- **Architecture:** `docs/architecture/apocalyptron-engine.md`
- **Tuning:** `docs/tutorials/CREATE_CUSTOM_PLAYER.md`
- **Tournament:** `tournament/README.md`

## 💡 Contributing

Created a great configuration? Share it!

1. Test thoroughly (10+ games against various opponents)
2. Document strategy and performance
3. Submit PR with config file
4. Include ELO estimate and tuning notes

## 📧 Support

Questions? Issues? Suggestions?

- GitHub: https://github.com/lookee/Reversi42
- Docs: See `docs/` directory
- Issues: GitHub issue tracker

