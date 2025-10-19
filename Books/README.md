# Opening Books

This directory contains professional opening book files for Reversi42.

## 🔄 Automatic Loading System

**All `.txt` files in this directory are automatically loaded at startup!**

- Files are loaded in **alphabetical order** (use numeric prefixes like `00_`, `01_` to control order)
- The system displays detailed statistics for each book loaded
- Duplicate openings are automatically merged
- Mixed formats are supported (with/without advantage evaluations)

## 📚 Current Books

### 1. **00_opening_ffo.txt** (FFO Professional Repertoire)
- **Source**: Fédération Française d'Othello
- **URL**: https://www.ffothello.org/strategie/repertoire-douvertures/
- **Repository**: https://github.com/jonkr2/PointyStone3
- **Content**: Professional C4-based openings
- **Format**: `NAME | MOVES | ADVANTAGE`
- **Features**: Includes positional evaluations (=, w, w+, w++, b, b+, b++)

### 2. **01_opening_pointystone.txt** (PointyStone3 Collection)
- **Source**: PointyStone3 Reversi Engine
- **Repository**: https://github.com/jonkr2/PointyStone3
- **Content**: Popular F5-based tactical openings
- **Format**: `NAME | MOVES`
- **Features**: Community-tested variations, tactical diversity

## File Formats

### FFO Format (with advantages)
```
# NAME | MOVES | ADVANTAGE
Diagonal Opening | C4c3D3c5 | =
Heath | C4c3D3c5B4 | w
Tiger Opening | C4c3D3c5B4e3D2b5 | w+
```

### PointyStone3 Format (legacy)
```
# NAME | MOVES
Diagonal Opening | F5d6C3
Tiger Opening | F5f6E6f4
```

### Move Notation

- **Columns**: A-H (letters)
- **Rows**: 1-8 (numbers)
- **Color**: Uppercase for Black, lowercase for White
- **Example**: `F5d6C3` = Black F5, White d6, Black C3

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

### Option 1: Add to Existing File
Edit any existing `.txt` file and add new lines:

```
# My new opening
My Opening Name | F5d6C5f4F6f3E3d3C3 | =
```

### Option 2: Create New Book File
Create a new `.txt` file in this directory:

1. **Choose a prefix** (e.g., `02_my_book.txt`, `99_experimental.txt`)
   - Use numeric prefix to control load order
   - Lower numbers = loaded first

2. **Use correct format**:
   ```
   # Comments start with #
   Opening Name | MOVES | ADVANTAGE
   Opening Name | MOVES
   ```

3. **Example new file** (`02_my_custom.txt`):
   ```
   # My Custom Opening Book
   # Author: Your Name
   
   My Favorite | F5d6C5f4F6 | w
   My Second Opening | C4c3D3c5B4 | =
   ```

4. **Restart the game** - your book will be automatically loaded!

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

