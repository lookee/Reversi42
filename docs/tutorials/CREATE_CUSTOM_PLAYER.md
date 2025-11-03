# 🎓 Tutorial: Create Your Custom AI Player

**Complete step-by-step guide to creating custom Reversi AI players**

**Two Methods Available:**
1. **YAML Configuration** (RECOMMENDED) - No coding required! ✨
2. **Python Programming** - For advanced customization

---

## 🎯 Method 1: YAML Configuration (RECOMMENDED)

**Difficulty**: Beginner  
**Time**: 15-30 minutes  
**Prerequisites**: Basic text editor skills

### ⚡ Why YAML?

- ✅ **No coding required** - Just edit simple text values
- ✅ **200+ parameters** - Complete control over AI behavior
- ✅ **Auto-discovery** - Drop file in folder, instantly available
- ✅ **Production-ready** - Same system used for all 11 built-in AIs
- ✅ **Hot-reload** - Changes take effect on next game
- ✅ **1,587-line template** - Every parameter documented

### 🚀 Quick Start - YAML Method

#### Step 1: Copy the Template

```bash
cp config/players/00_AI_CONFIG_TEMPLATE.yaml \
   config/players/enabled/gladiators/my_custom_ai.yaml
```

#### Step 2: Edit Basic Metadata

Open `my_custom_ai.yaml` and customize:

```yaml
metadata:
  name: "MY AWESOME AI"
  display_name: "My Awesome AI"
  description: "My custom AI fighter"
  headline: "AWESOME MODE ACTIVATED"
  enabled: true
  icon: "🤖"
  category: "custom"
  estimated_elo: 1600
```

#### Step 3: Configure Engine Settings

```yaml
engine:
  depth:
    base: 9                    # Search depth (4-16)
    strategy: "iterative"      # fixed | iterative | adaptive
  
  parallel:
    enabled: true
    num_workers: 4             # Number of CPU cores to use
  
  transposition_table:
    enabled: true
    size_mb: 128               # Cache size
```

#### Step 4: Choose Playing Style

**Option A: Use a Preset** (Easiest)
```yaml
evaluation:
  preset: "balanced"           # balanced | aggressive | defensive | endgame_specialist
```

**Option B: Custom Weights** (Advanced)
```yaml
evaluation:
  preset: null
  evaluators:
    - name: "mobility"
      weight: 2.0              # 2x mobility = aggressive
    - name: "positional"
      weight: 1.5
    - name: "stability"
      weight: 1.0
    - name: "parity"
      weight: 1.0
```

#### Step 5: Enable Optimizations

```yaml
pruning:
  null_move:
    enabled: true              # 30-60% speedup
  futility:
    enabled: true              # 15-30% speedup
  late_move_reduction:
    enabled: true              # 40-80% speedup
  multi_cut:
    enabled: true              # 15-25% speedup
```

#### Step 6: Test Your AI

```bash
python start_game.py --list-players
# You should see your AI in the list!

# Play against it
python start_game.py  # Then select your AI from the web interface
```

### 🎨 Configuration Examples

#### Example 1: Speed Demon
```yaml
metadata:
  name: "SPEED DEMON"
  estimated_elo: 1400

engine:
  depth:
    base: 5
    strategy: "fixed"
  parallel:
    enabled: false

evaluation:
  preset: null
  evaluators:
    - name: "positional"
      enabled: true
      weight: 1.0
    # All others disabled

pruning:
  # All disabled for simplicity
```

#### Example 2: Defensive Wall
```yaml
metadata:
  name: "DEFENSIVE WALL"
  estimated_elo: 1750

engine:
  depth:
    base: 10
    strategy: "iterative"

evaluation:
  preset: "defensive"

pruning:
  # All enabled
```

#### Example 3: Endgame Specialist
```yaml
metadata:
  name: "ENDGAME MASTER"
  estimated_elo: 1850

engine:
  depth:
    base: 9
    strategy: "adaptive"
    adaptive:
      opening: 7
      midgame: 9
      endgame: 14

evaluation:
  preset: "endgame_specialist"
```

### 📚 Complete Resources

- **Full Template**: `config/players/00_AI_CONFIG_TEMPLATE.yaml` (1,587 lines)
- **Configuration Guide**: `config/players/README.md`
- **Player Directory**: `config/players/INDEX.md`
- **11 Working Examples**: `config/players/enabled/gladiators/*.yaml`

---

## 🐍 Method 2: Python Programming (Advanced)

**Difficulty**: Intermediate-Advanced  
**Time**: 30-60 minutes  
**Prerequisites**: Python programming knowledge

### When to Use Python Method?

- Need dynamic behavior based on game state
- Want to implement custom evaluation functions
- Require special move selection logic
- Advanced research/experimentation

---

## 📋 Table of Contents (Python Method)

1. [Quick Start - Python](#quick-start-python)
2. [Understanding the Architecture](#architecture)
3. [Configuration Options](#configuration-options)
4. [Complete Examples](#complete-examples)
5. [Advanced Techniques](#advanced-techniques)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start - Python Method {#quick-start-python}

### Step 1: Create the Player File

Create a new file: `src/Players/PlayerMyCustom.py`

```python
"""
My Custom Player - A unique AI fighter
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerMyCustom(Player):
    """
    My Custom Player - Your unique AI personality
    """
    
    PLAYER_METADATA = {
        "display_name": "MY CUSTOM PLAYER",
        "description": "My unique AI fighter",
        "headline": "CUSTOM MODE ACTIVATED",
        "strategy": "Your strategy here",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "MY CUSTOM PLAYER"
        self.depth = 9
        self.deep = 9
        
        # BUILD YOUR CONFIGURATION HERE
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(9)
            .enable_all_optimizations()  # Start with everything
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print(f"\n🎮 {self.name} - INITIALIZED 🎮\n")
    
    def get_move(self, game, moves, control):
        """Get best move for current position"""
        if len(moves) == 0:
            return None
        
        try:
            bitboard_game = self._convert_to_bitboard(game)
            move = self.bitboard_engine.get_best_move(bitboard_game, self.deep)
            if move and game.valid_move(move):
                return move
        except:
            return moves[0]  # Fallback
    
    def _convert_to_bitboard(self, game):
        """Convert standard game to bitboard representation"""
        from Reversi.BitboardGame import BitboardGame
        bitboard = BitboardGame.create_empty()
        
        for y in range(1, 9):
            for x in range(1, 9):
                cell = game.matrix[y][x]
                bit = (y - 1) * 8 + (x - 1)
                if cell == "B":
                    bitboard.black |= 1 << bit
                elif cell == "W":
                    bitboard.white |= 1 << bit
        
        bitboard.turn = game.turn
        bitboard.turn_cnt = game.turn_cnt
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)
        bitboard._create_virtual_matrix()
        
        return bitboard
    
    @classmethod
    def get_metadata(cls):
        return cls.PLAYER_METADATA
```

### Step 2: Register Your Player

Add to `src/Players/PlayerFactory.py`:

```python
from Players.PlayerMyCustom import PlayerMyCustom

class PlayerFactory:
    ALL_PLAYER_CLASSES = [
        # ... existing players ...
        PlayerMyCustom,  # Add your player here
    ]
```

### Step 3: Test It!

```python
from Players.PlayerFactory import PlayerFactory

player = PlayerFactory.create_player('MY CUSTOM PLAYER')
# Your player is now available in the menu!
```

**Congratulations!** 🎉 You've created your first custom player!

---

## 🏗️ Understanding the Architecture

### Component Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         YOUR CUSTOM PLAYER                          │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Player Metadata                             │  │
│  │  • display_name: "MY CUSTOM PLAYER"                          │  │
│  │  • description: "..."                                        │  │
│  │  • headline: "..."                                           │  │
│  │  • strategy: "..."                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              ApocalyptronConfigBuilder                       │  │
│  │                                                              │  │
│  │  .with_depth(9)              ← Search depth                 │  │
│  │  .with_search_strategy(...)  ← Fixed/ID/Adaptive            │  │
│  │  .with_evaluators(...)       ← Which evaluators             │  │
│  │  .with_weights(...)          ← Custom weights               │  │
│  │  .enable/disable opts        ← Optimizations                │  │
│  │  .build()                    → ApocalyptronConfig            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                 ApocalyptronEngine                           │  │
│  │                                                              │  │
│  │  ┌─────────────────┐  ┌──────────────────┐                 │  │
│  │  │ SearchStrategy  │  │ CompositeEvaluator│                │  │
│  │  │ - Fixed Depth   │  │ - Mobility        │                │  │
│  │  │ - Iterative Deep│  │ - Positional      │                │  │
│  │  │ - Adaptive      │  │ - Stability       │                │  │
│  │  └─────────────────┘  │ - Parity          │                │  │
│  │                       └──────────────────┘                  │  │
│  │  ┌─────────────────┐  ┌──────────────────┐                 │  │
│  │  │ MoveOrderer     │  │ PruningTechniques│                │  │
│  │  │ - PV Move       │  │ - Null Move      │                │  │
│  │  │ - Killer Moves  │  │ - Futility       │                │  │
│  │  │ - History       │  │ - LMR            │                │  │
│  │  │ - Positional    │  │ - Multi-Cut      │                │  │
│  │  └─────────────────┘  └──────────────────┘                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   get_move()                                 │  │
│  │  Returns best move for current position                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. **Player Metadata**
Defines how your player appears in the menu:

```python
PLAYER_METADATA = {
    "display_name": "PLAYER NAME",      # Name in menu (no emoji!)
    "description": "Short description",  # Tooltip/description
    "headline": "ACTIVATION MESSAGE",    # Shown when player loads
    "strategy": "Technical details",     # Strategy description
    "enabled": True,                     # Show in menu
    "parameters": {},                    # Optional parameters
}
```

#### 2. **ApocalyptronConfigBuilder**
Fluent API for building configurations:

```python
builder = ApocalyptronConfigBuilder()

# Method chaining for clean configuration
config = (
    builder
    .with_depth(9)                  # Search depth
    .with_search_strategy('...')    # Strategy type
    .with_evaluators([...])         # Which evaluators
    .enable_all_optimizations()     # Enable everything
    .build()                        # Create config
)
```

#### 3. **ApocalyptronEngine**
The actual AI engine that searches for moves:

```python
engine = ApocalyptronEngine(config=config)

# Use it to get moves
move = engine.get_best_move(game, depth=9)
```

---

## ⚙️ Configuration Options

### Search Strategy Options

#### Option 1: Iterative Deepening (Default)
Progressive depth 1 → N with aspiration windows.

```python
.with_search_strategy('iterative_deepening')
# OR
.enable_iterative_deepening(True)
```

**Best for**: Standard strong play, time management

#### Option 2: Fixed Depth (NEW!)
Direct search at target depth (no progression).

```python
.with_fixed_depth_search()
# OR
.with_search_strategy('fixed_depth')
```

**Best for**: Speed, consistent difficulty, educational

#### Option 3: Adaptive Depth (NEW!)
Depth varies by game phase.

```python
.with_adaptive_depth(
    opening=7,   # Shallow in opening (less critical)
    midgame=9,   # Standard in midgame
    endgame=14   # Deep in endgame (exactness matters)
)
```

**Best for**: Tournament play, maximum strength, resource optimization

### Evaluator Options

#### Use All 4 Evaluators (Default)
```python
# Don't specify evaluators - uses all 4 by default
config = ApocalyptronConfigBuilder().with_depth(9).build()
# → Mobility, Positional, Stability, Parity (all weight 1.0)
```

#### Use Single Evaluator

```python
# Mobility only
.with_only_mobility(weight=1.0)

# Positional only
.with_only_positional(weight=1.0)

# Stability only
.with_only_stability(weight=1.0)

# Parity only
.with_only_parity(weight=1.0)
```

#### Custom Evaluator Mix

```python
from AI.Apocalyptron.core.config import EvaluatorConfig

.with_evaluators([
    EvaluatorConfig('mobility', weight=2.0),     # Double weight
    EvaluatorConfig('stability', weight=0.5),    # Half weight
    # Don't include positional or parity at all!
])
```

### Weight Preset Options

Seven preset weight configurations:

```python
# Default balanced weights
.with_preset_weights('default')

# Aggressive (high mobility focus)
.with_preset_weights('aggressive')

# Defensive (high stability focus)
.with_preset_weights('defensive')

# Corner hunter (extreme corner priority)
.with_preset_weights('corner_hunter')

# Edge control specialist
.with_preset_weights('edge_control')

# Endgame specialist (parity focus)
.with_preset_weights('endgame_specialist')

# Balanced (same as default)
.with_preset_weights('balanced')
```

### Optimization Options

#### Enable All (Recommended)
```python
.enable_all_optimizations()
# Enables: Null-Move, Futility, LMR, Multi-Cut, Aspiration, Parallel
```

#### Disable All (Educational/Speed)
```python
.disable_all_pruning()
.enable_parallel(False)
.enable_iterative_deepening(False)
# Pure alpha-beta search
```

#### Custom Mix
```python
.enable_null_move_pruning(True)
.enable_futility_pruning(True)
.enable_late_move_reduction(False)  # Disable this one
.enable_multi_cut_pruning(True)
.enable_parallel(True)
```

### Parallel Processing Options

```python
# Auto-detect cores
.enable_parallel(True)
.with_num_workers(None)  # Auto

# Specific core count
.enable_parallel(True)
.with_num_workers(4)  # Use 4 cores

# Disable parallel (for shallow depths)
.enable_parallel(False)
```

---

## 💡 Complete Examples

### Example 1: Speed Demon
**Goal**: Fastest possible response time

```python
"""
Speed Demon - Ultra fast AI for rapid games
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerSpeedDemon(Player):
    PLAYER_METADATA = {
        "display_name": "SPEED DEMON",
        "description": "Ultra Fast - Minimal Intelligence",
        "headline": "MAXIMUM SPEED MODE",
        "strategy": "Fixed Depth 4 | Response: <50ms",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "SPEED DEMON"
        self.depth = 4
        self.deep = 4
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(4)                    # Shallow depth
            .with_fixed_depth_search()        # No iterative deepening overhead
            .with_only_positional()           # Single evaluator (fast)
            .disable_all_pruning()            # No pruning overhead
            .enable_parallel(False)           # No parallel overhead
            .quiet_mode()                     # No output overhead
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n⚡ SPEED DEMON ACTIVATED ⚡\n")
    
    def get_move(self, game, moves, control):
        if not moves:
            return None
        try:
            bitboard = self._convert_to_bitboard(game)
            move = self.bitboard_engine.get_best_move(bitboard, self.deep)
            if move and game.valid_move(move):
                return move
        except:
            return moves[0]
    
    def _convert_to_bitboard(self, game):
        from Reversi.BitboardGame import BitboardGame
        bitboard = BitboardGame.create_empty()
        for y in range(1, 9):
            for x in range(1, 9):
                cell, bit = game.matrix[y][x], (y - 1) * 8 + (x - 1)
                if cell == "B": bitboard.black |= 1 << bit
                elif cell == "W": bitboard.white |= 1 << bit
        bitboard.turn = game.turn
        bitboard.turn_cnt = game.turn_cnt
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)
        bitboard._create_virtual_matrix()
        return bitboard
    
    @classmethod
    def get_metadata(cls):
        return cls.PLAYER_METADATA
```

**Result**: Response time <50ms, ELO ~1400

---

### Example 2: Mobility Master
**Goal**: Maximize opponent mobility restriction

```python
"""
Mobility Master - Focuses exclusively on mobility control
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.weights import get_preset_weights


class PlayerMobilityMaster(Player):
    PLAYER_METADATA = {
        "display_name": "MOBILITY MASTER",
        "description": "Mobility Control Specialist",
        "headline": "MOBILITY CONTROL ENGAGED",
        "strategy": "Mobility Focus x5 | Depth: 10",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "MOBILITY MASTER"
        self.depth = 10
        self.deep = 10
        
        # Custom mobility-focused weights
        weights = get_preset_weights('aggressive')
        weights.mobility_opening = 50   # 5x boost!
        weights.mobility_midgame = 75   # 5x boost!
        weights.mobility_endgame = 25   # 5x boost!
        weights.move_order_mobility_penalty = 75  # 5x boost!
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(10)
            .with_only_mobility(weight=5.0)   # ONLY mobility, 5x weight
            .with_weights(weights)             # Custom enhanced weights
            .enable_all_optimizations()        # All optimizations
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n🎯 MOBILITY MASTER - RESTRICTION MODE 🎯\n")
    
    # ... rest of standard methods ...
```

**Result**: Extreme mobility focus, ELO ~1780

---

### Example 3: Adaptive Genius
**Goal**: Maximum strength through adaptive depth

```python
"""
Adaptive Genius - Adjusts depth by game phase for optimal play
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerAdaptiveGenius(Player):
    PLAYER_METADATA = {
        "display_name": "ADAPTIVE GENIUS",
        "description": "Phase-Adaptive Master",
        "headline": "ADAPTIVE INTELLIGENCE ONLINE",
        "strategy": "Adaptive 6/10/15 | Phase-Optimized",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "ADAPTIVE GENIUS"
        self.depth = 10
        self.deep = 10
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(10)                    # Base depth
            .with_adaptive_depth(
                opening=6,    # Fast opening (less critical)
                midgame=10,   # Standard midgame
                endgame=15    # DEEP endgame (critical!)
            )
            .enable_all_optimizations()        # All optimizations
            .with_num_workers(8)               # Maximum parallelization
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n🧠 ADAPTIVE GENIUS - PHASE OPTIMIZATION ACTIVE 🧠\n")
    
    # ... rest of standard methods ...
```

**Result**: Optimal resource allocation, ELO ~1870

---

### Example 4: Corner Fanatic
**Goal**: Obsessed with corners above all else

```python
"""
Corner Fanatic - Will sacrifice everything for corners
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.weights import get_preset_weights


class PlayerCornerFanatic(Player):
    PLAYER_METADATA = {
        "display_name": "CORNER FANATIC",
        "description": "Corner Obsession - Throne Hunter",
        "headline": "CORNER ACQUISITION MODE",
        "strategy": "Positional Only | Corner x5 | Depth: 9",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "CORNER FANATIC"
        self.depth = 9
        self.deep = 9
        
        # EXTREME corner weights
        weights = get_preset_weights('corner_hunter')
        weights.corner_weight = 500           # 5x boost! (vs 100 normal)
        weights.x_square_penalty = 200        # Avoid X-squares at all costs
        weights.move_order_corner = 3000      # Corner moves first always
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(9)
            .with_only_positional()            # Only positional evaluator
            .with_weights(weights)             # Extreme corner weights
            .enable_all_optimizations()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n👑 CORNER FANATIC - THRONE OBSESSION MODE 👑\n")
    
    # ... rest of standard methods ...
```

**Result**: Extreme corner focus, ELO ~1740

---

### Example 5: Balanced Hybrid
**Goal**: Mix of mobility and stability

```python
"""
Balanced Hybrid - Perfect balance of mobility and stability
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.core.config import EvaluatorConfig


class PlayerBalancedHybrid(Player):
    PLAYER_METADATA = {
        "display_name": "BALANCED HYBRID",
        "description": "Perfect Balance - Mobility + Stability",
        "headline": "HYBRID INTELLIGENCE ACTIVE",
        "strategy": "Mobility x2 + Stability x2 | Depth: 9",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "BALANCED HYBRID"
        self.depth = 9
        self.deep = 9
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(9)
            .with_evaluators([
                EvaluatorConfig('mobility', weight=2.0),   # Double mobility
                EvaluatorConfig('stability', weight=2.0),  # Double stability
                # No positional or parity - focused build
            ])
            .enable_all_optimizations()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n⚖️  BALANCED HYBRID - EQUILIBRIUM MODE ⚖️\n")
    
    # ... rest of standard methods ...
```

**Result**: Balanced play, ELO ~1780

---

## 🎨 Visual Configuration Guide

### Configuration Decision Tree

```
START: What kind of player do you want?
│
├─ SPEED PRIORITY?
│  ├─ Yes → Fixed Depth (4-6)
│  │        + Single evaluator (Positional)
│  │        + No optimizations
│  │        = RESULT: <100ms response
│  │
│  └─ No → Continue ↓
│
├─ STRENGTH PRIORITY?
│  ├─ Maximum → Adaptive Depth (8/12/16)
│  │            + All 4 evaluators
│  │            + All optimizations
│  │            + 8 cores
│  │            = RESULT: ELO 1880
│  │
│  └─ Balanced → Iterative Deepening (9)
│                + All/Custom evaluators
│                + All optimizations
│                = RESULT: ELO 1750-1850
│
├─ SPECIALTY FOCUS?
│  ├─ Mobility → Mobility-only, weight x3-5
│  │             = Crushes opponent options
│  │
│  ├─ Corners → Positional-only, corner_hunter weights
│  │            = Throne seeker
│  │
│  ├─ Defense → Stability×2 + Positional×1.5, defensive weights
│  │            = Impenetrable fortress
│  │
│  └─ Chaos → Parity-only, minimal opts
│               = Unpredictable madness
│
└─ BEGINNER FRIENDLY?
   └─ Yes → Fixed Depth 3
            + All evaluators
            + No optimizations
            = RESULT: ELO 1250, ~30ms
```

### Weight Impact Chart

```
Parameter              Low (0.5x)    Default (1.0x)    High (2.0x)    Extreme (5.0x)
─────────────────────────────────────────────────────────────────────────────────
Mobility Focus         Passive       Balanced          Aggressive     STRANGLER
Corner Priority        Ignore        Standard          Hunter         FANATIC
Stability Focus        Risky         Normal            Defensive      FORTRESS
Parity Awareness       Ignore        Aware             Focused        ORACLE
```

---

## 🎯 Step-by-Step: Create "THE DESTROYER"

Let's create a complete custom player from scratch!

### Goal
Create an aggressive player that:
- Focuses on mobility AND positional play
- Uses adaptive depth for smart resource allocation
- Has aggressive weights
- ELO target: ~1800

### Step 1: Plan the Configuration

```
Strategy:    Adaptive (7/9/12) - smart depth allocation
Evaluators:  Mobility (x2.5) + Positional (x1.5)
Weights:     Aggressive preset
Opts:        ALL enabled
Cores:       4-8
```

### Step 2: Create the File

File: `src/Players/Gladiators/PlayerTheDestroyer.py`

```python
"""
THE DESTROYER - Aggressive Hybrid Master

Combines mobility control with territorial domination.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.core.config import EvaluatorConfig
from AI.Apocalyptron.weights import get_preset_weights


class PlayerTheDestroyer(Player):
    """
    THE DESTROYER - Aggressive Hybrid Master
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    THE DESTROYER combines the best of two worlds: mobility suffocation and 
    territorial domination. This ruthless AI doesn't just win—it annihilates 
    opponents through coordinated dual-threat assault.
    
    With adaptive depth that grows from efficient openings to devastating endgame 
    calculations, THE DESTROYER knows exactly when to strike and when to calculate 
    deeper. Fear the perfect synthesis of aggression and intelligence.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐⭐⭐⭐⭐☆ 9/10   (Devastating Force)
    ⚡  SPEED:      ⭐⭐⭐⭐⭐☆☆☆☆☆ 5/10   (Methodical Destruction)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐⭐⭐⭐⭐☆ 9/10   (Precision Strikes)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Deep Tactical Vision)
    💀  LETHALITY:  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Total Annihilation)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Adaptive Hybrid Destroyer
    Strategy:         Adaptive Depth (7 → 9 → 12 by game phase)
    
    Evaluators:
      • Mobility      (weight: 2.5)
      • Positional    (weight: 1.5)
    
    Weight Preset:    Aggressive
      • mobility_midgame:  25 (enhanced)
      • corner_weight:    150 (balanced)
    
    Optimizations:    ALL enabled
    Parallel Workers: 6
    
    Estimated ELO:    ~1820
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "THE DESTROYER",
        "description": "Aggressive Hybrid Master - Dual Threat",
        "headline": "DESTRUCTION PROTOCOL ACTIVE",
        "strategy": "Adaptive 7/9/12 | Mobility x2.5 + Positional x1.5",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "THE DESTROYER"
        self.depth = 9
        self.deep = 9
        
        # Build aggressive hybrid configuration
        weights = get_preset_weights('aggressive')
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(9)
            .with_adaptive_depth(
                opening=7,    # Fast opening
                midgame=9,    # Standard midgame
                endgame=12    # Deep endgame
            )
            .with_evaluators([
                EvaluatorConfig('mobility', weight=2.5),    # 2.5x mobility
                EvaluatorConfig('positional', weight=1.5),  # 1.5x positional
            ])
            .with_weights(weights)
            .enable_all_optimizations()
            .with_num_workers(6)
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n💥 THE DESTROYER - ANNIHILATION PROTOCOL 💥")
        print("Dual Threat: Mobility x2.5 + Positional x1.5 | Adaptive 7/9/12\n")
    
    def get_move(self, game, moves, control):
        if not moves:
            return None
        try:
            bitboard = self._convert_to_bitboard(game)
            move = self.bitboard_engine.get_best_move(bitboard, self.deep)
            if move and game.valid_move(move):
                return move
        except:
            return moves[0]
    
    def _convert_to_bitboard(self, game):
        from Reversi.BitboardGame import BitboardGame
        bitboard = BitboardGame.create_empty()
        for y in range(1, 9):
            for x in range(1, 9):
                cell, bit = game.matrix[y][x], (y - 1) * 8 + (x - 1)
                if cell == "B": bitboard.black |= 1 << bit
                elif cell == "W": bitboard.white |= 1 << bit
        bitboard.turn = game.turn
        bitboard.turn_cnt = game.turn_cnt
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)
        bitboard._create_virtual_matrix()
        return bitboard
    
    @classmethod
    def get_metadata(cls):
        return cls.PLAYER_METADATA
```

**Result**: Adaptive hybrid destroyer, ELO ~1820

---

### Example 5: Educational Bot
**Goal**: Weak player for beginners

```python
"""
Tutorial Bot - Simple AI for learning
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerTutorialBot(Player):
    PLAYER_METADATA = {
        "display_name": "TUTORIAL BOT",
        "description": "Beginner-Friendly AI - Learn the Game",
        "headline": "TUTORIAL MODE - BEGINNER FRIENDLY",
        "strategy": "Fixed Depth 2 | No Optimizations | Perfect for Learning",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "TUTORIAL BOT"
        self.depth = 2
        self.deep = 2
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(2)                     # Very shallow
            .with_fixed_depth_search()         # No iterative deepening
            .disable_all_pruning()             # No optimizations (weaker)
            .enable_parallel(False)            # No parallel
            .quiet_mode()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n📚 TUTORIAL BOT - BEGINNER MODE 📚")
        print("Depth: 2 | Perfect for learning the game!\n")
    
    # ... rest of standard methods ...
```

**Result**: Very weak for beginners, ELO ~1100

---

## 🔧 Advanced Techniques

### Custom Weight Presets

Create your own weight preset class:

```python
from AI.Apocalyptron.weights import EvaluationWeights

class MyCustomWeights(EvaluationWeights):
    """My custom weight configuration"""
    
    def __init__(self):
        super().__init__()
        
        # Customize weights
        self.mobility_opening = 25      # Higher than default (10)
        self.mobility_midgame = 30      # Higher than default (15)
        self.corner_weight = 200        # Higher than default (150)
        self.stability_weight = 60      # Higher than default (40)
        
        # ... customize all weights as needed ...

# Use in configuration
weights = MyCustomWeights()
config = builder.with_weights(weights).build()
```

### Dynamic Configuration

Adjust configuration based on game state:

```python
class PlayerDynamicAdaptive(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "DYNAMIC ADAPTIVE"
        
        # Start with one configuration
        self.current_depth = 9
        self._rebuild_engine()
    
    def _rebuild_engine(self):
        """Rebuild engine with current depth"""
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(self.current_depth)
            .enable_all_optimizations()
            .build()
        )
        self.bitboard_engine = ApocalyptronEngine(config=config)
    
    def get_move(self, game, moves, control):
        # Adjust depth based on situation
        piece_count = game.black_cnt + game.white_cnt
        
        if piece_count > 55:  # Endgame
            if self.current_depth != 14:
                self.current_depth = 14
                self._rebuild_engine()
        elif piece_count > 30:  # Midgame
            if self.current_depth != 10:
                self.current_depth = 10
                self._rebuild_engine()
        else:  # Opening
            if self.current_depth != 7:
                self.current_depth = 7
                self._rebuild_engine()
        
        # Standard move search
        bitboard = self._convert_to_bitboard(game)
        return self.bitboard_engine.get_best_move(bitboard, self.current_depth)
```

### Mix Multiple Weight Presets

```python
from AI.Apocalyptron.weights import get_preset_weights

# Start with aggressive
weights = get_preset_weights('aggressive')

# Add some defensive elements
defensive = get_preset_weights('defensive')
weights.stability_weight = defensive.stability_weight  # Copy stability weight
weights.frontier_weight = defensive.frontier_weight    # Copy frontier weight

# Hybrid: Aggressive mobility + Defensive stability
config = builder.with_weights(weights).build()
```

---

## 📊 Configuration Comparison Matrix

| Feature | Speed Demon | Standard | Adaptive Genius | Tutorial Bot |
|---------|-------------|----------|-----------------|--------------|
| **Strategy** | Fixed 4 | ID 1→9 | Adaptive 7/9/12 | Fixed 2 |
| **Evaluators** | Positional only | All 4 | All 4 | All 4 |
| **Optimizations** | None | All | All | None |
| **Parallel** | No | Yes | Yes (8 cores) | No |
| **Response Time** | <50ms | ~1s | ~3s | <20ms |
| **Strength (ELO)** | 1400 | 1850 | 1870 | 1100 |
| **Best For** | Speed | General | Tournament | Learning |

---

## 🐛 Troubleshooting

### Player Not Showing in Menu

**Problem**: Created player but not visible in menu

**Solution**:
1. Check `PLAYER_METADATA["enabled"] = True`
2. Register in `PlayerFactory.ALL_PLAYER_CLASSES`
3. Verify `display_name` has no emoji (menu compatibility)

### Player Too Slow

**Problem**: Player takes too long to move

**Solutions**:
- Reduce depth: `.with_depth(6)` instead of 9
- Use fixed depth: `.with_fixed_depth_search()`
- Reduce evaluators: `.with_only_positional()`
- Disable parallel: `.enable_parallel(False)`
- Disable pruning for very shallow: `.disable_all_pruning()`

### Player Too Weak

**Problem**: Player loses too easily

**Solutions**:
- Increase depth: `.with_depth(11)` or higher
- Use adaptive depth: `.with_adaptive_depth(8, 10, 14)`
- Enable all optimizations: `.enable_all_optimizations()`
- Use all evaluators (default)
- Enable parallel: `.with_num_workers(8)`

### Unpredictable Behavior

**Problem**: Player makes strange moves

**Possible Causes**:
- Single evaluator (limited view): Try adding more evaluators
- Extreme weights: Reduce weight multipliers
- Parity-only: Intentionally chaotic (like GLITCH_LORD)

**Solutions**:
- Use balanced weights
- Include multiple evaluators
- Test with depth 6-9 for stability

---

## 📚 Reference: All Builder Methods

### Depth Configuration
```python
.with_depth(9)                    # Set search depth
```

### Search Strategy
```python
.with_search_strategy('iterative_deepening')  # Default
.with_search_strategy('fixed_depth')          # No ID
.with_search_strategy('adaptive')             # Phase-based
.with_fixed_depth_search()                    # Shortcut for fixed
.with_adaptive_depth(7, 9, 12)                # Shortcut for adaptive
```

### Evaluators
```python
.with_only_mobility(weight=1.0)               # Mobility only
.with_only_positional(weight=1.0)             # Positional only
.with_only_stability(weight=1.0)              # Stability only
.with_only_parity(weight=1.0)                 # Parity only
.with_evaluators([...])                       # Custom mix
.add_evaluator('mobility', weight=2.0)        # Add single
```

### Weights
```python
.with_weights(custom_weights)                 # Custom EvaluationWeights
.with_preset_weights('aggressive')            # Use preset
.with_preset_weights('defensive')
.with_preset_weights('corner_hunter')
.with_preset_weights('edge_control')
.with_preset_weights('endgame_specialist')
.with_preset_weights('balanced')
```

### Optimizations
```python
.enable_all_optimizations()                   # Enable everything
.disable_all_pruning()                        # Disable all pruning
.enable_null_move_pruning(True/False)
.enable_futility_pruning(True/False)
.enable_late_move_reduction(True/False)
.enable_multi_cut_pruning(True/False)
.enable_iterative_deepening(True/False)
.enable_aspiration_windows(True/False)
```

### Parallel Processing
```python
.enable_parallel(True/False)                  # Enable/disable
.with_num_workers(8)                          # Specific core count
.with_num_workers(None)                       # Auto-detect
```

### Output
```python
.quiet_mode()                                 # No output
.verbose_mode()                               # Maximum output
.enable_output(True/False)                    # Toggle output
```

---

## 🎓 Learning Path

### Beginner
1. Start with template (Example 1: Speed Demon)
2. Modify depth only
3. Try different presets
4. Test and iterate

### Intermediate
1. Experiment with single evaluators
2. Try adaptive depth
3. Mix evaluators with custom weights
4. Create specialty players

### Advanced
1. Create custom weight classes
2. Dynamic reconfiguration during game
3. Tournament optimization
4. Performance tuning

---

## 📖 Related Documentation

- [Apocalyptron Engine](../architecture/apocalyptron-engine.md) - Engine architecture
- [Epic Gladiators](../EPIC_GLADIATORS.md) - 10 example configurations
- [Evaluation Weights](../api/evaluation-weights.md) - Weight parameter reference
- [API Reference](../api/README.md) - Complete API documentation

---

**Tutorial Version**: 1.0  
**Last Updated**: 2025-10-20  
**Engine Version**: Apocalyptron 4.2.0

*Ready to create your legendary AI fighter? Let's build!* ⚔️🎮

