# Reversi42 - Documentation

This directory contains detailed documentation for the Reversi42 project.

## 📚 Available Documentation

### Player Documentation (`players/`)
- **[players/README.md](players/README.md)** - Complete player types overview and comparison
- **[players/Player.md](players/Player.md)** - Base player class and architecture
- **[players/HumanPlayer.md](players/HumanPlayer.md)** - Human player controls and features
- **[players/Monkey.md](players/Monkey.md)** - Random Chaos player
- **[players/GreedyPlayer.md](players/GreedyPlayer.md)** - Greedy Goblin player
- **[players/HeuristicPlayer.md](players/HeuristicPlayer.md)** - Heuristic Scout player
- **[players/AIPlayer.md](players/AIPlayer.md)** - Alpha-Beta AI player
- **[players/AIPlayerBook.md](players/AIPlayerBook.md)** - Opening Scholar player
- **[players/AIPlayerBitboard.md](players/AIPlayerBitboard.md)** - Bitboard Blitz player
- **[players/AIPlayerBitboardBook.md](players/AIPlayerBitboardBook.md)** - The Oracle player
- **[players/AIPlayerBitboardBookParallel.md](players/AIPlayerBitboardBookParallel.md)** - Parallel Oracle player
- **[players/AIPlayerGrandmaster.md](players/AIPlayerGrandmaster.md)** - Grandmaster player
- **[players/NetworkPlayer.md](players/NetworkPlayer.md)** - Network player (concept)

### AI & Development Documentation
- **ADDING_PLAYERS.md** - Complete guide for creating custom AI players
- **GRANDMASTER_AI.md** - Grandmaster AI technical documentation
- **STRATEGY_IMPROVEMENTS.md** - Advanced AI strategy improvements and techniques
- **HOW_TO_USE_PARALLEL.md** - Guide for using parallel bitboard engine

### Technical Documentation
- **BITBOARD_IMPLEMENTATION.md** - Deep dive into bitboard representation
- **PROJECT_REORGANIZATION.md** - Codebase structure and organization
- **FEATURES.md** - Complete feature list and descriptions

## 🔗 Quick Links

### Root Documentation
Main documentation files are in the project root:
- `README.md` - Project overview and quick start
- `BUILD.md` - Build instructions
- `COPYING` - License (GPL v3)

### Directory-Specific Documentation
- `Books/README.md` - Opening book format
- `build/README.md` - Build system details
- `tournament/README.md` - Tournament system usage
- `saves/README.md` - Save file format

## 📖 Documentation Index

| Document | Description | Audience |
|----------|-------------|----------|
| **Player Documentation** | | |
| players/README.md | Player types overview and comparison | All users |
| players/*.md (13 files) | Detailed documentation for each player type | All users |
| **AI & Development** | | |
| ADDING_PLAYERS.md | Custom player creation guide | Developers |
| GRANDMASTER_AI.md | Grandmaster AI technical details | Advanced users |
| STRATEGY_IMPROVEMENTS.md | AI optimization techniques | Advanced developers |
| HOW_TO_USE_PARALLEL.md | Parallel engine usage | Users/Developers |
| **Technical** | | |
| BITBOARD_IMPLEMENTATION.md | Bitboard internals and algorithms | Advanced developers |
| PROJECT_REORGANIZATION.md | Codebase structure | Contributors |
| FEATURES.md | Complete feature list | Users/Contributors |

## 🎯 For New Users

Start with:
1. `../README.md` - Project overview and quick start
2. `FEATURES.md` - What the project offers
3. `players/README.md` - Player types and selection guide
4. Individual player docs in `players/` - Learn about specific players

## 🎯 For New Contributors

Start with:
1. `../README.md` - Project overview
2. `FEATURES.md` - What the project offers
3. `players/README.md` - Understanding the player system
4. `ADDING_PLAYERS.md` - How to extend the AI
5. `../BUILD.md` - How to build and run

## 📝 Contributing Documentation

When adding new documentation:
1. Place technical docs in this directory
2. Player-specific docs go in `players/` subdirectory
3. Update this README with links
4. Update `../README.md` documentation section
5. Keep root-level docs minimal (README, BUILD, CHANGELOG)
6. Use clear titles and organize by topic
7. Include code examples and cross-references

## 📂 Documentation Structure

```
docs/
├── README.md                      # This file (documentation index)
├── FEATURES.md                    # Complete feature list
├── ADDING_PLAYERS.md              # Player development guide
├── GRANDMASTER_AI.md              # Grandmaster AI documentation
├── STRATEGY_IMPROVEMENTS.md       # Advanced AI techniques
├── HOW_TO_USE_PARALLEL.md         # Parallel engine guide
├── BITBOARD_IMPLEMENTATION.md     # Bitboard technical details
├── PROJECT_REORGANIZATION.md      # Codebase structure
└── players/                       # Player documentation directory
    ├── README.md                  # Player overview and comparison
    ├── Player.md                  # Base player class
    ├── HumanPlayer.md             # Human player
    ├── Monkey.md                  # Random player
    ├── GreedyPlayer.md            # Greedy player
    ├── HeuristicPlayer.md         # Heuristic player
    ├── AIPlayer.md                # Alpha-Beta AI
    ├── AIPlayerBook.md            # Opening Scholar
    ├── AIPlayerBitboard.md        # Bitboard Blitz
    ├── AIPlayerBitboardBook.md    # The Oracle
    ├── AIPlayerBitboardBookParallel.md  # Parallel Oracle
    ├── AIPlayerGrandmaster.md     # Grandmaster
    └── NetworkPlayer.md           # Network player
```

