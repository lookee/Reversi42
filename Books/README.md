# Opening Books

This directory contains opening book files for Reversi42.

## File Format

Opening books use a simple text format:

```
# Comments start with #
F5d6C3      # Each line is a sequence of moves
F5d6C5      # Uppercase = Black, lowercase = White
F5f6E6f4    # Multiple variations can be listed
```

### Move Notation

- **Columns**: A-H (letters)
- **Rows**: 1-8 (numbers)
- **Color**: Uppercase for Black, lowercase for White
- **Example**: `F5d6C3` = Black F5, White d6, Black C3

## Files

- `opening_book.txt` - Main opening book with classic Reversi openings

## Using Opening Books

The `AIPlayerBook` player automatically uses the opening book:

```python
from Players.AIPlayerBook import AIPlayerBook

# Create player with book support
player = AIPlayerBook(deep=6)
```

The player will:
1. Consult the book for current position (O(m) lookup via Trie)
2. If multiple book moves exist, choose randomly among them
3. When out of book, use standard minimax search

## Adding New Openings

To add new openings to `opening_book.txt`:

1. Add move sequences, one per line
2. Use format: `F5d6C3d3C4...`
3. Add comments with `#`
4. Longer sequences are better (8-12 moves recommended)

Example:
```
# My favorite opening
F5d6C5f4F6f3E3d3C3
```

## Performance

The Trie-based structure provides:
- **O(m)** lookup time where m = number of moves played
- **Instant** move selection from book (<< 1ms)
- **Efficient** memory usage with shared prefixes

## Opening Theory

The default book includes:
- **Diagonal Opening** (most popular)
- **Perpendicular Opening**
- **Tiger Opening**
- **Buffalo/Cow Opening**
- **Rose Opening** (Mimura)
- **And many more classic lines**

For more information on Reversi opening theory, see:
- [World Othello Federation](https://www.worldothello.org/)
- [Logistello's Opening Book](http://www.radagast.se/othello/)

