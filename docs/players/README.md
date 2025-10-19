# Reversi42 Players Documentation

This directory contains detailed documentation for all available player types in Reversi42.

## Player Types Overview

Reversi42 is focused on the **Grandmaster AI** - the ultimate Reversi player combining all advanced technologies. Additional players are available for testing and comparison.

### Human Players
- **[Human Player](HumanPlayer.md)** - Interactive player controlled by mouse or keyboard

### AI Players
- **[Random Chaos (Monkey)](Monkey.md)** - Random move generator for testing and baseline comparison
- **[Grandmaster](AIPlayerGrandmaster.md)** - **THE** ultimate AI with all advanced features
  - Opening book (644 professional sequences)
  - Advanced bitboard engine (400-1000x speed)
  - Multi-core parallel processing
  - Enhanced evaluation with 15 configurable parameters
  - Multiple playing styles through weight customization

### Experimental
- **[Network Player](NetworkPlayer.md)** - Placeholder for remote network play (not implemented)

## Player Selection Guide

### For Learning
- Start with **Random Chaos (Monkey)** to understand the rules
- Play against **Human Player** for practice
- Challenge **Grandmaster** at depth 5-7 for learning

### For Challenge
- **Grandmaster** depth 7-8 - Strong gameplay
- **Grandmaster** depth 9-10 - Very strong  
- **Grandmaster** depth 11-12 - Ultimate challenge
- **Custom Grandmaster** - Create your own playing style with weight customization!

### For Development/Testing
- **Random Chaos (Monkey)** - Random baseline for testing
- **Human Player** - Manual testing
- **Grandmaster** with custom weights - Test different strategies

## Available Playing Styles (Grandmaster)

The Grandmaster AI can be customized with different weight configurations:

| Style | Focus | Best For |
|-------|-------|----------|
| **Default** | Balanced | General play, tournaments |
| **Aggressive** | Mobility restriction | Controlling tempo |
| **Defensive** | Stability & safety | Positional play |
| **Corner Hunter** | Corner conquest | Aggressive corner play |
| **Edge Control** | Border domination | Territorial control |
| **Endgame Specialist** | Parity & counting | Converting endgame advantages |
| **Custom** | Your choice! | Experimentation |

## Technical Architecture

All players inherit from the base `Player` class and implement the `get_move()` method. For detailed technical information, see the [Base Player](Player.md) documentation.

### Grandmaster Features

**Advanced Technologies**:
- **Bitboard representation**: 64-bit integer board (50-100x faster than arrays)
- **Opening book**: 644 professional sequences with HYBRID evaluation
- **Parallel processing**: Multi-core CPU utilization (2-5x speedup)
- **Advanced pruning**: Iterative deepening, null move, LMR, futility pruning
- **Enhanced evaluation**: 15 configurable parameters for different playing styles

**Key Optimizations**:
- Move ordering (corner/edge/mobility priority)
- Killer move heuristic
- History heuristic (global move success tracking)
- Aspiration windows
- Transposition table
- **Total Performance**: 400-1000x vs standard minimax

**Customization**:
- Fully parametric weights system
- 6 ready-to-use presets
- Create unlimited custom playing styles
- Save/load configurations via JSON

## Documentation Index

1. [Base Player Class](Player.md)
2. [Human Player](HumanPlayer.md)
3. [Random Chaos (Monkey)](Monkey.md)
4. **[Grandmaster](AIPlayerGrandmaster.md)** ⭐ **Main AI**
5. [Grandmaster Weights System](../../GRANDMASTER_WEIGHTS.md) - Customization guide
6. [Network Player](NetworkPlayer.md)

## Dependencies (Internal)

The following player classes exist as dependencies for Grandmaster but are not intended for direct use:
- `AIPlayerBitboardBook` - Bitboard + opening book (parent class)
- `AIPlayerBitboardBookParallel` - Adds parallel processing (parent class)

## Customizing Grandmaster

For information on customizing Grandmaster weights and creating your own playing styles, see:
- **[Grandmaster Weights Documentation](../../GRANDMASTER_WEIGHTS.md)**
- **[Grandmaster Weights Demo](../../src/examples/grandmaster_weights_demo.py)**

