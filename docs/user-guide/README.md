# User Guide

Complete user guide for playing and enjoying Reversi42.

## Quick Links

- [**Getting Started**](getting-started.md) - Install and play your first game
- [**Game Rules**](game-rules.md) - Learn how to play Reversi/Othello
- [**Playing the Game**](playing.md) - Controls and features
- [**AI Opponents**](ai-opponents.md) - Understanding AI players
- [**Opening Book**](opening-book.md) - Learn opening theory
- [**Tournament Mode**](tournaments.md) - Run AI tournaments
- [**Tips & Strategies**](strategies.md) - Improve your game
- [**FAQ**](faq.md) - Frequently asked questions

## What is Reversi42?

Reversi42 is a feature-rich implementation of the classic board game Reversi (also known as Othello). It features:

- 🎮 **Multiple interfaces**: Graphical (Pygame), Terminal (ASCII), or Headless
- 🤖 **Powerful AI**: From beginner to grandmaster level
- 📚 **Opening book**: Learn from 644 professional opening sequences
- 🏆 **Tournament system**: Pit AIs against each other
- 💾 **Save/Load games**: Resume games anytime
- ⚡ **Lightning fast**: Bitboard engine for instant moves

## Quick Start

### 1. Installation

```bash
# Clone and install
git clone https://github.com/lucaamore/reversi42.git
cd reversi42
pip install -r requirements.txt

# Or just download and run
./reversi42
```

### 2. Start Playing

```bash
# Graphical interface (default)
./reversi42

# Terminal interface (SSH-friendly)
./reversi42 --view terminal

# Choose your opponent and start!
```

### 3. Your First Game

1. **Main Menu** appears
2. Select **Black Player** (you can be Human)
3. Select **White Player** (try Alpha-Beta AI at level 3)
4. Click **Start Game**
5. Click on highlighted squares to make moves
6. Enjoy!

## Game Modes

### Single Player

Play against AI opponents of varying difficulty:

- **Beginner**: Random Chaos, Greedy Goblin
- **Intermediate**: Heuristic Scout, Alpha-Beta AI (1-5)
- **Advanced**: Bitboard Blitz, The Oracle (6-8)
- **Expert**: Apocalyptron (9-12)

### AI vs AI

Watch AI players compete:

1. Select AI for both players
2. Enable **Show Opening** to see opening theory
3. Sit back and watch the battle!

### Tournament Mode

Run systematic AI competitions:

```bash
cd tournament
./select_tournament.sh
```

See [Tournament Guide](tournaments.md).

## Interface Guide

### Pygame (Graphical) Interface

**Mouse Controls**:
- Click on highlighted squares to make moves
- Hover over golden moves (with Show Opening) to see opening names
- Click menu buttons

**Keyboard Controls**:
- `C` - Toggle cursor navigation
- `Arrow Keys` - Move cursor
- `ENTER`/`SPACE` - Select move
- `ESC` - Pause menu
- `Q` - Quit

### Terminal (ASCII) Interface

**Input Methods**:
- Type coordinates: `D3`, `E4`, etc.
- Or use move numbers: `1`, `2`, `3`

**Commands**:
- `q` - Quit game
- `h` - Show help
- `u` - Undo move (if available)

### Headless (No UI) Interface

For automated testing and tournaments only.

## Understanding the AI

### AI Levels

| Level | Depth | Strength | Speed | Best For |
|-------|-------|----------|-------|----------|
| 1-3   | 1-3   | Beginner | Instant | Learning |
| 4-6   | 4-6   | Intermediate | Fast | Practice |
| 7-9   | 7-9   | Advanced | 1-5s | Challenge |
| 10-12 | 10-12 | Expert | 5-30s | Analysis |

### AI Player Types

**Random Chaos** - Completely random moves
- **Strength**: None
- **Best for**: Testing, fun
- **Strategy**: None!

**Greedy Goblin** - Always captures maximum pieces
- **Strength**: Weak
- **Best for**: Understanding why greedy play fails
- **Strategy**: Short-sighted

**Heuristic Scout** - Fast positional evaluation
- **Strength**: Medium
- **Best for**: Quick games
- **Strategy**: Position-based

**Alpha-Beta AI** - Classic minimax with pruning
- **Strength**: Configurable (depth 1-10)
- **Best for**: Learning, practice
- **Strategy**: Deep search

**Bitboard Blitz** - Ultra-fast bitboard engine
- **Strength**: Strong (depth 1-12)
- **Best for**: Fast analysis
- **Strategy**: Deep tactical search

**The Oracle** - Bitboard + opening book
- **Strength**: Very strong
- **Best for**: Serious challenge
- **Strategy**: Perfect openings + deep search

**Apocalyptron** (Default) - Ultimate AI
- **Strength**: Grandmaster
- **Best for**: Maximum challenge
- **Strategy**: Everything optimized!

See [AI Opponents Guide](ai-opponents.md) for details.

## Opening Book System

The opening book helps you learn professional opening sequences.

### Using Opening Book

1. **Enable**: Menu → "Show Opening"
2. **Golden Moves**: Moves in opening book glow gold
3. **Hover**: See opening names and move counts
4. **Learn**: Discover new openings naturally

### Opening Types

- **Diagonal Openings**: D3, C4, F5, E6
- **Perpendicular Openings**: C4, D3, C5, D6
- **Tiger Variants**: Complex tactical openings
- **Buffalo Variants**: Solid positional openings

See [Opening Book Guide](opening-book.md).

## Features

### Save/Load Games

**Save a Game**:
1. Press `ESC` during game
2. Select "Save Game"
3. Enter filename
4. Game saved to `saves/` directory

**Load a Game**:
1. Main Menu → Pause Menu
2. Select "Load Game"
3. Choose saved game file
4. Game state restored

**File Format**: XOT (eXtended Othello Transcript) - human-readable text

### Undo Moves

During gameplay:
1. Press `ESC`
2. Select "Undo Move"
3. Last move is undone

**Note**: May not work in all game modes

### Statistics

During gameplay, view:
- Current score (piece count)
- Move history
- Time per move (for AI)
- Opening name (if in book)

## Tips for Beginners

### Basic Strategy

1. **Corners are powerful** - Once captured, can't be flipped
2. **Edges are valuable** - Hard to flank
3. **Mobility matters** - More moves = more options
4. **Don't be greedy** - Having more pieces isn't always better
5. **Think ahead** - Consider your opponent's responses

### Learning Path

1. **Start with easy AI** (Alpha-Beta level 2-3)
2. **Enable opening book** to learn professional moves
3. **Watch AI vs AI** games to see strategies
4. **Try harder AIs** as you improve
5. **Study your losses** - Learn from mistakes

See [Strategies Guide](strategies.md) for advanced tips.

## Customization

### Configuration

Edit `~/.reversi42/config.json`:

```json
{
  "default_view": "pygame",
  "ai_depth": 9,
  "show_opening": true,
  "window_size": [1280, 720],
  "theme": "default"
}
```

### Custom Opening Books

Add your own opening books:

1. Create text file in `src/domain/knowledge/data/`
2. Format: `Opening Name | Move1 Move2 Move3`
3. Reload game

## Troubleshooting

### Common Issues

**Game won't start**:
- Ensure Python 3.9+ is installed
- Install dependencies: `pip install -r requirements.txt`
- Check error messages

**Slow AI moves**:
- Lower AI depth (use level 6-8 instead of 10-12)
- Ensure no background processes
- Try different AI type

**Display issues**:
- Try terminal mode: `./reversi42 --view terminal`
- Update graphics drivers
- Check SDL2 installation (Linux)

See [FAQ](faq.md) for more.

## Advanced Features

### Tournament System

Run sophisticated AI tournaments:

```bash
cd tournament
./select_tournament.sh
```

Features:
- Round-robin format
- Statistical analysis
- JSON configuration
- Batch execution

See [Tournament Guide](tournaments.md).

### Custom AI Development

Create your own AI players:

1. Inherit from `Player` class
2. Implement `get_move()` method
3. Register in `PlayerFactory`

See [AI Development Guide](../development/ai-development.md).

## Getting Help

### Documentation

- [Game Rules](game-rules.md) - How to play
- [FAQ](faq.md) - Common questions
- [API Documentation](../api/) - For developers

### Community

- [GitHub Issues](https://github.com/lucaamore/reversi42/issues) - Bug reports
- [GitHub Discussions](https://github.com/lucaamore/reversi42/discussions) - Questions
- Email: luca.amore@gmail.com

### External Resources

- [World Othello Federation](https://www.worldothello.org/)
- [FNGO (Italian)](http://www.fngo.it/)
- [Othello Strategy Wikipedia](https://en.wikipedia.org/wiki/Reversi#Strategy)

## Keyboard Shortcuts

### During Gameplay

| Key | Action |
|-----|--------|
| `C` | Toggle cursor mode |
| `↑↓←→` | Move cursor |
| `ENTER`/`SPACE` | Make move |
| `ESC` | Pause menu |
| `Q` | Quit |

### In Menus

| Key | Action |
|-----|--------|
| `↑↓` | Navigate options |
| `ENTER` | Select |
| `ESC` | Back |
| `Q` | Quit to main menu |

## Tips for Advanced Players

### Opening Theory

- Learn standard openings (Diagonal, Perpendicular)
- Understand opening variations
- Practice with Opening Scholar AI
- Study professional games

### Mid-game Strategy

- Maintain mobility
- Control key squares
- Build stable pieces
- Set up endgame

### Endgame Technique

- Count empty squares
- Calculate forced sequences
- Maximize score difference
- Perfect play when possible

See [Advanced Strategies](strategies-advanced.md).

## Accessibility

- **Keyboard navigation**: Full game playable with keyboard
- **Terminal mode**: Screen reader compatible
- **Adjustable speeds**: Configure AI thinking time
- **Clear visual feedback**: Color-coded moves

## Contributing

Found a bug? Want a feature?

- [Report bugs](https://github.com/lucaamore/reversi42/issues)
- [Suggest features](https://github.com/lucaamore/reversi42/discussions)
- [Contribute code](../../CONTRIBUTING.md)

---

**Enjoy playing Reversi42!** 🎮

*Need more help? Check the [FAQ](faq.md) or ask in [Discussions](https://github.com/lucaamore/reversi42/discussions)*

