# Reversi42 Players Documentation

This directory contains detailed documentation for all available player types in Reversi42.

## Player Types Overview

Reversi42 offers a wide variety of player types, from human players to advanced AI opponents. Each player type is designed with specific use cases and skill levels in mind.

### Human Players
- **[Human Player](HumanPlayer.md)** - Interactive player controlled by mouse or keyboard

### AI Players - Basic
- **[Random Chaos (Monkey)](Monkey.md)** - Random move generator for testing
- **[Greedy Goblin](GreedyPlayer.md)** - Always captures maximum pieces immediately
- **[Heuristic Scout](HeuristicPlayer.md)** - Fast positional evaluation without deep search

### AI Players - Standard
- **[Alpha-Beta AI](AIPlayer.md)** - Classic minimax with alpha-beta pruning
- **[Opening Scholar](AIPlayerBook.md)** - Standard AI with opening book support

### AI Players - Advanced (Bitboard-based)
- **[Bitboard Blitz](AIPlayerBitboard.md)** - Ultra-fast bitboard engine (50-100x faster)
- **[The Oracle](AIPlayerBitboardBook.md)** - Bitboard speed + opening book intelligence

### AI Players - Expert
- **[Parallel Oracle](AIPlayerBitboardBookParallel.md)** - Multi-core parallel bitboard AI
- **[Grandmaster](AIPlayerGrandmaster.md)** - Ultimate AI with all advanced features

### Experimental
- **[Network Player](NetworkPlayer.md)** - Placeholder for remote network play (not implemented)

## Player Selection Guide

### For Learning
- Start with **Random Chaos** or **Greedy Goblin** to learn the basics
- Move to **Heuristic Scout** for intermediate challenge
- Try **Alpha-Beta AI** at depth 3-4 for solid gameplay

### For Challenge
- **Opening Scholar** depth 6 - Good opening knowledge
- **Bitboard Blitz** depth 8 - Very fast and strong
- **The Oracle** depth 8 - Opening book + bitboard speed
- **Parallel Oracle** depth 9-10 - Multi-core power
- **Grandmaster** depth 9-12 - Ultimate challenge

### For Development/Testing
- **Random Chaos** - Random baseline for testing
- **Greedy Goblin** - Simple deterministic opponent
- **Human Player** - Manual testing

## Performance Comparison

| Player Type | Relative Speed | Strength | Best Use Case |
|-------------|---------------|----------|---------------|
| Random Chaos | Instant | Very Weak | Testing, learning rules |
| Greedy Goblin | Instant | Weak | Educational, baseline |
| Heuristic Scout | Fast | Moderate | Quick games, learning |
| Alpha-Beta AI | 1x (baseline) | Strong | Classic gameplay |
| Opening Scholar | 1x | Strong+ | Better opening play |
| Bitboard Blitz | 50-100x | Strong | Deep analysis |
| The Oracle | 50-100x | Very Strong | Competitive play |
| Parallel Oracle | 150-500x | Very Strong | Deep searches |
| Grandmaster | 400-1000x | Strongest | Maximum challenge |

## Technical Architecture

All players inherit from the base `Player` class and implement the `get_move()` method. For detailed technical information, see the [Base Player](Player.md) documentation.

### Key Features by Category

**Bitboard Players** (`AIPlayerBitboard*`)
- 64-bit integer board representation
- Bitwise operations for move generation
- 50-100x performance improvement
- Supports depths 8-12

**Opening Book Players** (`*Book*`)
- 57 professional opening sequences
- Trie-based position lookup
- Instant early game responses
- Smooth transition to engine search

**Parallel Players** (`*Parallel*`)
- Multi-core CPU utilization
- 2-5x additional speedup
- Process pool for move evaluation
- Auto-adaptive parallelization

**Grandmaster**
- All advanced features combined
- Enhanced evaluation function
- Advanced move ordering
- Killer move heuristic
- Ultimate performance and strength

## Documentation Index

1. [Base Player Class](Player.md)
2. [Human Player](HumanPlayer.md)
3. [Random Chaos (Monkey)](Monkey.md)
4. [Greedy Goblin](GreedyPlayer.md)
5. [Heuristic Scout](HeuristicPlayer.md)
6. [Alpha-Beta AI](AIPlayer.md)
7. [Opening Scholar](AIPlayerBook.md)
8. [Bitboard Blitz](AIPlayerBitboard.md)
9. [The Oracle](AIPlayerBitboardBook.md)
10. [Parallel Oracle](AIPlayerBitboardBookParallel.md)
11. [Grandmaster](AIPlayerGrandmaster.md)
12. [Network Player](NetworkPlayer.md)

## Adding Custom Players

For information on creating your own custom player types, see [ADDING_PLAYERS.md](../ADDING_PLAYERS.md) in the main docs directory.

