# Frequently Asked Questions (FAQ)

Common questions and answers about Reversi42.

## General Questions

### What is Reversi42?

Reversi42 is a feature-rich implementation of the classic board game Reversi (Othello). It includes powerful AI opponents, an opening book system, tournament mode, and multiple interface options.

### Is it free?

Yes! Reversi42 is free and open source software licensed under GPL-3.0.

### What platforms does it support?

- **macOS** (10.14+)
- **Windows** (10+)
- **Linux** (any modern distribution)

### Is Reversi the same as Othello?

Yes, they're the same game with different names. "Othello" is a trademarked name for the same game that is generically called "Reversi."

## Installation & Setup

### How do I install Reversi42?

```bash
git clone https://github.com/lucaamore/reversi42.git
cd reversi42
pip install -r requirements.txt
./reversi42
```

See [Getting Started](getting-started.md) for detailed instructions.

### What Python version do I need?

Python 3.9 or higher. Python 3.11 is recommended for best performance.

### What dependencies do I need?

FastAPI and Uvicorn for the web interface. Install with `pip install -r requirements.txt`.

### Can I run it without a browser?

Yes! Use tournament mode for AI vs AI battles, or use Reversi42 as a Python library in your own code.

## Gameplay Questions

### How do I make a move?

Click on any highlighted (valid) square in the web interface.

### Why can't I move to certain squares?

You can only move to squares that will flip at least one opponent piece. Valid moves are highlighted.

### Can I save my game?

Game saving features are available through the web interface. Games can be saved in XOT format.

### Why did a player pass their turn?

If a player has no valid moves, they must pass. This is a normal part of the game.

### When does the game end?

The game ends when neither player has any valid moves, or when all 64 squares are filled.

### How is the winner determined?

The player with the most pieces when the game ends wins. If both players have the same number of pieces, it's a draw.

## AI Questions

### Which AI should I play against?

**Beginners:** Start with Alpha-Beta AI at level 2-3

**Intermediate:** Try Alpha-Beta AI at level 5-6 or Opening Scholar

**Advanced:** Challenge The Oracle or Bitboard Blitz

**Experts:** Face Apocalyptron at depth 9-12

See [AI Opponents Guide](ai-opponents.md) for details.

### What do the AI levels mean?

The number represents the search depth:
- **Level 1-3:** Quick, beginner-friendly
- **Level 4-6:** Moderate difficulty and speed
- **Level 7-9:** Strong play, slower
- **Level 10-12:** Expert level, can be very slow

### Why is the AI so slow at high levels?

Higher levels search deeper into the game tree, analyzing millions of positions. This takes time but produces very strong play.

### Can I make the AI faster?

Yes:
- Lower the AI depth/level
- Use Bitboard-based AIs (50-100x faster)
- Use Apocalyptron (3500-14000x faster with optimizations)

### What's the difference between AI types?

- **Random Chaos:** Completely random moves
- **Greedy Goblin:** Always takes maximum pieces (weak strategy)
- **Heuristic Scout:** Fast positional evaluation
- **Alpha-Beta AI:** Classic minimax search
- **Opening Scholar:** AI + opening book
- **Bitboard Blitz:** Ultra-fast bitboard engine
- **The Oracle:** Bitboard + opening book
- **Apocalyptron:** All optimizations enabled (default)

### What's the strongest AI?

**Apocalyptron** at depth 11-12 is the strongest, using all optimizations including iterative deepening, null move pruning, late move reductions, and multi-cut pruning.

## Opening Book Questions

### What is the opening book?

A database of 644 professional opening sequences. The AI can use these to make strong opening moves instantly.

### How do I enable the opening book display?

Click "Show Opening" in the main menu. Valid moves that appear in the opening book will glow gold.

### What are opening move counts?

The numbers shown (like "57") indicate how many different known openings that move leads to.

### Can I add my own openings?

Yes! Add them to files in `src/domain/knowledge/data/` following the format:
```
Opening Name | D3 C4 E3 F4 ...
```

### Which openings are included?

The book includes classic openings like:
- Diagonal openings
- Perpendicular openings
- Tiger variants
- Buffalo variants
- Rose variants
- And many more!

## Tournament Questions

### How do I run a tournament?

```bash
cd tournament
./select_tournament.sh
```

Or run a specific configuration:
```bash
./run_tournament.sh elite_tournament.json
```

### What tournaments are available?

12 pre-configured tournaments including:
- Quick Tournament (9 AI, 144 games)
- Tournament of Champions (7 AI, 294 games)
- Elite Tournament (5 AI, 100 games)
- And 9 more!

See [Tournament Guide](tournaments.md).

### Can I create custom tournaments?

Yes! Create a JSON configuration file with your preferred settings. See `tournament/ring/` for examples.

### How long do tournaments take?

- **Quick** tournaments: 1-15 minutes
- **Medium** tournaments: 30-60 minutes
- **Epic** tournaments: 2-4 hours

Time depends on AI depth and number of games.

## Technical Questions

### What's a bitboard?

A bitboard uses 64-bit integers to represent the game board, where each bit represents one square. This allows for extremely fast move generation and evaluation using bitwise operations.

### Why is Reversi42 so fast?

Three key optimizations:
1. **Bitboard representation** - 50-100x faster than arrays
2. **Advanced pruning** - Skips irrelevant positions
3. **Parallel search** - Uses multiple CPU cores

### Can I use multiple CPU cores?

Yes! Parallel AIs automatically use multiple cores. The Apocalyptron and Parallel Oracle are optimized for multi-core systems.

### How much memory does it use?

- Base game: ~50 MB
- With transposition tables: ~200 MB
- During deep search: ~500 MB

### Does it work over SSH?

Yes! You can:
```bash
./reversi42 --view terminal
```

## Troubleshooting

### The game won't start

```bash
# Check Python version
python3 --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt

# Try running directly
python3 src/reversi42.py
```

### "ModuleNotFoundError: No module named 'fastapi'" error

```bash
pip install -r requirements.txt
```

### The game is laggy

- Lower AI depth
- Close other applications
- Try terminal mode
- Update graphics drivers

### Moves aren't registering

- Ensure you're clicking valid (highlighted) moves
- Check browser console for errors
- Check that it's your turn

### AI is taking forever

- Lower the AI depth (use level 6-8 instead of 10-12)
- Use faster AI types (Bitboard, Apocalyptron)
- Be patient - depth 12 can take minutes per move

### Display looks wrong

- Try different view modes
- Update SDL2 libraries (Linux)
- Verify WebSocket connection in browser

### Can't save/load games

- Check `saves/` directory exists
- Verify write permissions
- Try absolute path for save location

## Contributing & Development

### How can I contribute?

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for:
- Reporting bugs
- Suggesting features
- Contributing code
- Improving documentation

### Can I create my own AI?

Yes! See [Adding Players](../../docs/ADDING_PLAYERS.md) for a guide on creating custom AI players.

### Where's the source code?

GitHub: https://github.com/lucaamore/reversi42

### How do I report bugs?

Open an issue on [GitHub Issues](https://github.com/lucaamore/reversi42/issues) using the bug report template.

### Can I suggest new features?

Yes! Use the feature request template on [GitHub Issues](https://github.com/lucaamore/reversi42/issues).

## Performance & Optimization

### How do I benchmark AI performance?

```bash
# Run specific AI vs AI match
python3 src/reversi42.py --view headless

# Or use tournament mode
cd tournament
./run_tournament.sh benchmark.json
```

### Which AI is fastest?

**Apocalyptron** is fastest overall due to advanced optimizations, followed by **Bitboard Blitz**, then **The Oracle**.

### How can I profile the code?

```bash
python -m cProfile -o profile.prof src/reversi42.py
python -m pstats profile.prof
```

See [Performance Guide](../development/performance.md).

## Miscellaneous

### What does "42" mean in Reversi42?

A reference to "The Hitchhiker's Guide to the Galaxy" where 42 is the "Answer to the Ultimate Question of Life, the Universe, and Everything."

### Who created Reversi42?

Luca Amore (luca.amore@gmail.com). Originally released in 2011, with major updates in 2025.

### Can I use this commercially?

Yes, under the terms of the GPL-3.0 license. See [COPYING](../../COPYING) for details.

### How do I cite Reversi42?

```
Reversi42 v5.0.0 (2025)
Luca Amore
https://github.com/lucaamore/reversi42
```

### Is there a mobile version?

Not yet, but it's on the roadmap for future development.

### Can I play online multiplayer?

Not yet, but network play is planned for a future release.

## Still Have Questions?

- Check the [User Guide](README.md)
- Read the [Documentation](../README.md)
- Ask in [GitHub Discussions](https://github.com/lucaamore/reversi42/discussions)
- Email: luca.amore@gmail.com

---

**Can't find your question?** Open a discussion on GitHub or send an email!

