# Reversi / Othello Rules

Complete rules for playing Reversi (also known as Othello).

## Objective

**Capture more pieces than your opponent by the end of the game.**

## Setup

### The Board

- 8x8 grid (64 squares)
- Initially empty except for the center 4 squares

### Starting Position

```
  A B C D E F G H
1 . . . . . . . .
2 . . . . . . . .
3 . . . . . . . .
4 . . . O X . . .
5 . . . X O . . .
6 . . . . . . . .
7 . . . . . . . .
8 . . . . . . . .
```

- `O` = White pieces
- `X` = Black pieces
- Black moves first

## How to Play

### Making a Move

1. **Place a piece** on an empty square
2. **Flank opponent pieces** - Your move must trap one or more opponent pieces between your new piece and another of your pieces
3. **Flip the pieces** - All trapped opponent pieces in straight lines (horizontal, vertical, or diagonal) flip to your color

### Valid Moves

A move is valid ONLY if it:
1. Is on an empty square
2. Flanks at least one opponent piece
3. Has one of your pieces on the opposite side of the flanked pieces

### Directions

Pieces can be flanked in 8 directions:
- ↑ Up
- ↓ Down
- ← Left
- → Right
- ↖ Diagonal up-left
- ↗ Diagonal up-right
- ↙ Diagonal down-left
- ↘ Diagonal down-right

### Multiple Flips

A single move can flip pieces in multiple directions simultaneously!

**Example:**
```
Before:          After (Black plays E3):
  D E F            D E F
2 . . .          2 . . .
3 O O .    →     3 X X X
4 O X .          4 O X .
```

Black at E3 flips the white pieces at D3 and E3.

## Special Rules

### Passing

If you have **no valid moves**, you must **pass your turn**.

The game continues with your opponent moving again.

### Game End

The game ends when:
- **Both players have no valid moves**, OR
- **The board is full** (all 64 squares occupied)

### Scoring

Count the pieces:
- Player with **more pieces wins**
- Equal pieces = **draw**

## Strategy Basics

### Corner Squares

**Most valuable squares on the board!**

Once captured, corners can NEVER be flipped:
- A1, H1, A8, H8

**Why?** No pieces can exist on all sides of a corner.

### Edge Squares

**Second most valuable!**

Edges are harder to flip than center squares:
- Entire first and last rows/columns

### X-Squares (Danger!)

**Avoid these squares near corners:**
- B2, G2, B7, G7 (diagonal to corners)

**Why?** Often give opponent the corner!

### C-Squares (Risky)

**Squares adjacent to corners:**
- A2, B1, H2, G1, A7, B8, H7, G8

**Be careful:** Can give opponent edges or corners.

### Mobility

**Having more moves available = good!**

Don't just count pieces - count options!

### Stability

**Stable pieces can't be flipped**

Examples:
- Corners (always stable)
- Edges connected to corners
- Pieces surrounded by friendly pieces

### Tempo

**Timing matters!**

Sometimes passing moves to your opponent is good:
- Forces them into bad positions
- Limits their options late game

## Common Mistakes

### 1. Being Too Greedy

**Mistake:** Always capturing the maximum pieces

**Why it fails:** More pieces early = fewer moves later

**Better:** Maintain mobility and position

### 2. Ignoring Corners

**Mistake:** Not prioritizing corner control

**Why it fails:** Corners are extremely powerful

**Better:** Fight for every corner!

### 3. Playing X-Squares Early

**Mistake:** Playing B2, G2, B7, G7 without thinking

**Why it fails:** Often gifts corners to opponent

**Better:** Avoid unless you have a specific plan

### 4. No Long-term Plan

**Mistake:** Only thinking about current move

**Why it fails:** Reversi rewards planning ahead

**Better:** Think 3-5 moves ahead

### 5. Underestimating Edges

**Mistake:** Treating all squares equally

**Why it fails:** Edge control matters enormously

**Better:** Build strong edge positions

## Game Phases

### Opening (Moves 1-20)

**Goals:**
- Control center
- Maintain mobility
- Develop position
- Avoid early edge/corner plays

**Key concept:** Don't capture too many pieces yet!

### Midgame (Moves 21-50)

**Goals:**
- Fight for corners
- Control key edges
- Build stable pieces
- Limit opponent mobility

**Key concept:** Position over piece count

### Endgame (Moves 51-64)

**Goals:**
- Maximize piece count
- Force opponent into bad moves
- Calculate exact sequences
- Don't leave empty squares unreachable

**Key concept:** Precision and calculation

## Notation

### Algebraic Notation

Squares are identified by column letter + row number:

```
  A B C D E F G H
1 □ □ □ □ □ □ □ □
2 □ □ □ □ □ □ □ □
3 □ □ □ □ □ □ □ □
4 □ □ □ D4 □ □ □ □
5 □ □ □ □ E5 □ □ □
6 □ □ □ □ □ F6 □ □
7 □ □ □ □ □ □ G7 □
8 □ □ □ □ □ □ □ H8
```

Examples:
- **D3** = Column D, Row 3
- **F5** = Column F, Row 5
- **A8** = Top-left corner
- **H1** = Bottom-right corner

### Recording Games

Games are recorded as move sequences:

**Example opening:**
```
1. F5 D6
2. C5 F4
3. E3 F6
```

This means:
- Move 1: Black F5, White D6
- Move 2: Black C5, White F4
- Move 3: Black E3, White F6

### XOT Format

Reversi42 uses XOT (eXtended Othello Transcript):
- Human-readable text
- Complete move history
- Game metadata
- Compatible with analysis tools

## Tournament Rules

### Standard Time Controls

- **No time limit** - Casual play
- **Blitz** - 5 minutes per player
- **Rapid** - 15 minutes per player
- **Standard** - 30+ minutes per player

### Tie-breakers

If scores are equal:
1. Player who moved last loses (standard rule)
2. Rematch with colors reversed
3. Or simply declare a draw

### Illegal Moves

If illegal move attempted:
- Move is rejected
- Player must make valid move
- No penalty in casual play

## Variants

### Standard Reversi/Othello

- Black starts
- 4 pieces in center
- Most common variant

### Random Start

- Random initial position
- Increases variety
- Less opening theory

### Custom Boards

- 6x6 or 10x10 boards
- Different starting positions
- Experimental variants

**Note:** Reversi42 implements standard 8x8 Reversi.

## Learning Resources

### In Reversi42

- **Opening Book** - Learn 644 professional sequences
- **Show Opening mode** - Highlights book moves
- **AI opponents** - Practice against various strengths
- **Tournament mode** - Watch AI games to learn

### External Resources

- [World Othello Federation](https://www.worldothello.org/)
- [Othello Strategy Guide](https://www.worldothello.org/about/about-othello/othello-rules/mid-game-through-end-game)
- [FNGO (Italian)](http://www.fngo.it)

## Quick Reference

| Concept | Description |
|---------|-------------|
| **Valid Move** | Must flip ≥1 opponent piece |
| **Corners** | Can never be flipped |
| **Edges** | Hard to flip |
| **X-Squares** | Dangerous! Often lose corners |
| **Mobility** | # of available moves |
| **Stability** | Pieces that can't flip |
| **Passing** | Required if no valid moves |
| **Game End** | Both players can't move OR board full |
| **Winner** | Most pieces at game end |

## FAQs

**Q: Can I capture in multiple directions?**
A: Yes! One move can flip pieces in all 8 directions.

**Q: Must I flip all captured pieces?**
A: Yes, all flanked pieces must flip.

**Q: Can I choose which pieces to flip?**
A: No, all flanked pieces flip automatically.

**Q: What if I have no moves?**
A: You must pass. Your opponent continues.

**Q: Can both players pass?**
A: Yes, this ends the game.

**Q: What if the board fills up?**
A: Game ends immediately, count pieces.

**Q: Is Reversi the same as Othello?**
A: Yes, same game with different names.

**Q: Who moves first?**
A: Black always moves first.

**Q: What's the best first move?**
A: D3, C4, F5, or E6 (the four diagonal moves).

## Now You're Ready!

You understand the rules of Reversi. Time to play and improve!

**Next steps:**
- Play against easy AI to practice
- Enable opening book to learn theory
- Read [Strategies Guide](strategies.md) to improve
- Challenge harder AIs as you get better

Good luck! 🎮

