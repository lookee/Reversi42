# XOT Format Guide

**eXtended Othello Transcript (XOT) - The Standard Save Format for Reversi42**

Version: 1.0  
Last Updated: 2025-11-02

---

## Overview

XOT (eXtended Othello Transcript) is Reversi42's standard save format, designed to be:

- ✅ **Human-readable** - Easy to read and understand
- ✅ **Git-friendly** - Clean diffs for version control
- ✅ **Complete** - Includes metadata, history, and board state
- ✅ **Extensible** - Future-proof with section-based structure
- ✅ **Compatible** - Works with analysis tools

## File Structure

### Complete Example

```xot
# Reversi42 Game Save - XOT Format v1.0
# Saved: 2025-11-02 15:30:45

[GAME]
Black=Human
White=THE STRANGLER
Turn=B
BlackScore=18
WhiteScore=15
Size=8

[MOVES]
History=C4e3F6e6F4c5D6c6D7e7F5c7
Count=12

[BOARD]
........
........
...BWB..
..BWWWB.
..BBWW..
...BWW..
........
........
```

## Sections

### Header Section

```xot
# Reversi42 Game Save - XOT Format v1.0
# Saved: 2025-11-02 15:30:45
```

- **Line 1**: Format identifier and version
- **Line 2**: Timestamp in ISO 8601 format
- Lines starting with `#` are comments

### [GAME] Section

Game metadata and current state:

```xot
[GAME]
Black=Human              # Black player name
White=THE STRANGLER      # White player name  
Turn=B                   # Current turn (B or W)
BlackScore=18            # Black piece count
WhiteScore=15            # White piece count
Size=8                   # Board size (always 8 for standard Reversi)
```

**Fields:**
- `Black` - Name of Black player (Human or AI name)
- `White` - Name of White player (Human or AI name)
- `Turn` - Current player's turn (`B` or `W`)
- `BlackScore` - Number of black pieces on board
- `WhiteScore` - Number of white pieces on board
- `Size` - Board size (8×8 for standard Reversi)

### [MOVES] Section

Move history in compact notation:

```xot
[MOVES]
History=C4e3F6e6F4c5D6c6D7e7F5c7
Count=12
```

**Fields:**
- `History` - Compact move notation (case indicates player):
  - **Uppercase** = Black moves (e.g., `C4`, `F6`)
  - **Lowercase** = White moves (e.g., `e3`, `e6`)
- `Count` - Total number of moves (History length ÷ 2)

**Move Notation:**
- Format: `[Column][Row]` (e.g., `D3`, `e6`)
- Columns: A-H (left to right)
- Rows: 1-8 (top to bottom)
- Case: UPPERCASE = Black, lowercase = White

### [BOARD] Section

Visual board state (8 rows × 8 columns):

```xot
[BOARD]
........
........
...BWB..
..BWWWB.
..BBWW..
...BWW..
........
........
```

**Characters:**
- `.` = Empty square
- `B` = Black piece
- `W` = White piece

## Usage

### Saving Games

In the **Web Interface**:

1. Click **Save** button (💾)
2. File downloads automatically as `reversi42_YYYYMMDD_HHMMSS.xot`
3. File contains complete game state

### Loading Games

In the **Web Interface**:

1. Click **Load** button (📂)
2. Select `.xot` file (or `.rev`, `.r42` - auto-detected)
3. Game loads from saved state

**Supported formats:**
- `.xot` - XOT format (recommended)
- `.rev`, `.r42` - Compact format (legacy)
- `.txt` - Auto-detected

### Auto-Detection

Reversi42 automatically detects file format:

```javascript
// XOT format - detected by section markers
[GAME]
Black=Human
...

// Compact format - detected by pattern
C4e3F6e6F4c5...
```

## Programmatic Use

### Python - Parsing XOT

```python
def parse_xot(filepath):
    """Parse XOT file"""
    with open(filepath, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    
    data = {'game': {}, 'moves': {}, 'board': []}
    section = None
    
    for line in lines:
        if line.startswith('['):
            section = line[1:-1].lower()
        elif '=' in line and section == 'game':
            key, value = line.split('=', 1)
            data['game'][key.lower()] = value
        elif line.startswith('History=') and section == 'moves':
            data['moves']['history'] = line.split('=', 1)[1]
        elif section == 'board' and len(line) == 8:
            data['board'].append(line)
    
    return data

# Usage
game_data = parse_xot('saved_game.xot')
print(f"Black: {game_data['game']['black']}")
print(f"Moves: {game_data['moves']['history']}")
```

### JavaScript - Generating XOT

```javascript
function generateXOT(gameState) {
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  
  let xot = [];
  xot.push('# Reversi42 Game Save - XOT Format v1.0');
  xot.push(`# Saved: ${timestamp}`);
  xot.push('');
  xot.push('[GAME]');
  xot.push(`Black=${gameState.players.black.name}`);
  xot.push(`White=${gameState.players.white.name}`);
  xot.push(`Turn=${gameState.turn}`);
  xot.push(`BlackScore=${gameState.blackScore}`);
  xot.push(`WhiteScore=${gameState.whiteScore}`);
  xot.push(`Size=8`);
  xot.push('');
  xot.push('[MOVES]');
  xot.push(`History=${gameState.history}`);
  xot.push(`Count=${Math.floor(gameState.history.length / 2)}`);
  xot.push('');
  xot.push('[BOARD]');
  
  // Add board rows
  for (let row = 0; row < 8; row++) {
    xot.push(gameState.board[row]);
  }
  
  return xot.join('\n');
}
```

## Benefits

### vs Compact Format

| Feature | XOT | Compact |
|---------|-----|---------|
| **Readability** | ✅ Excellent | ❌ Poor |
| **Metadata** | ✅ Complete | ❌ None |
| **Board State** | ✅ Visible | ❌ Implicit |
| **Git Diffs** | ✅ Clean | ❌ Opaque |
| **Size** | ~400 bytes | ~40 bytes |
| **Speed** | ✅ Fast | ✅ Fastest |
| **Analysis** | ✅ Easy | ❌ Hard |

### Use Cases

**XOT is best for:**
- 📚 **Archiving** - Save important games
- 📊 **Analysis** - Study game patterns
- 🔍 **Debugging** - Inspect game state
- 📝 **Documentation** - Share games with context
- 🔄 **Version Control** - Track game history in git

**Compact is best for:**
- 💬 **Chat** - Quick sharing
- 📋 **Copy/Paste** - Instant transfer
- 🔗 **URLs** - Embed in links
- ⚡ **Speed** - Minimal overhead

## Examples

### Early Game

```xot
# Reversi42 Game Save - XOT Format v1.0
# Saved: 2025-11-02 15:30:00

[GAME]
Black=Human
White=Apocalyptron
Turn=W
BlackScore=3
WhiteScore=4
Size=8

[MOVES]
History=C4e3F6
Count=3

[BOARD]
........
........
........
...WB...
..BBWB..
........
........
........
```

### Mid Game

```xot
# Reversi42 Game Save - XOT Format v1.0
# Saved: 2025-11-02 16:45:23

[GAME]
Black=Human
White=THE STRANGLER
Turn=B
BlackScore=18
WhiteScore=15
Size=8

[MOVES]
History=C4e3F6e6F4c5D6c6D7e7F5c7D3f3C3
Count=15

[BOARD]
........
........
...BBBBB
..BWWWBB
..BBWWB.
...BWB..
........
........
```

### End Game

```xot
# Reversi42 Game Save - XOT Format v1.0
# Saved: 2025-11-02 17:20:12

[GAME]
Black=Human
White=DIVZERO.EXE
Turn=Game Over
BlackScore=28
WhiteScore=36
Size=8

[MOVES]
History=C4e3F6e6F4c5D6c6D7e7F5c7D3f3C3b4A5b3C2d2E2f2G3...
Count=60

[BOARD]
WWWWWWWW
WWWWWWWW
BWWWWWWW
BBWWWWWW
BBBWWWWW
BBBBWWWW
BBBBBWWW
BBBBBBWW
```

## Future Extensions

The XOT format is designed to be extensible. Potential future sections:

```xot
[ANALYSIS]
OpeningName=Perpendicular Opening
BookMove=Yes
Evaluation=+2.5

[TIMING]
BlackTime=120.5
WhiteTime=98.3
TimeControl=300+0

[METADATA]
Tournament=Reversi42 Championship 2025
Round=3
Event=Quarter Finals
```

## Specification

- **Format Version**: 1.0
- **File Extension**: `.xot`
- **Encoding**: UTF-8
- **Line Endings**: LF or CRLF
- **Section Order**: `[GAME]`, `[MOVES]`, `[BOARD]`
- **Required Sections**: All three sections mandatory
- **Case Sensitivity**: Section names case-insensitive, move notation case-sensitive

## Tools & Libraries

### Reversi42 Built-in
- ✅ Web Interface - Native support
- ✅ Backend Server - Full XOT parsing/generation
- ✅ Auto-detection - Recognizes XOT vs compact

### External Tools
- Git - Excellent diff support
- Text editors - Any editor works
- Version control - All systems supported

## FAQ

**Q: Can I edit XOT files by hand?**  
A: Yes! XOT is designed to be human-editable. Just maintain the structure.

**Q: What if I have a compact format file?**  
A: Reversi42 auto-detects and loads both formats seamlessly.

**Q: How do I convert compact to XOT?**  
A: Load compact file in web interface, then save - it saves as XOT.

**Q: Is XOT compatible with other Reversi programs?**  
A: The format is Reversi42-specific, but the compact history (`[MOVES]`) is portable.

**Q: Can I use XOT in version control?**  
A: Yes! XOT produces clean, readable diffs perfect for git.

---

**See Also:**
- [Getting Started Guide](user-guide/getting-started.md)
- [Web Interface Guide](WEBGUI.md)
- [Save/Load Tutorial](tutorials/save-load.md)

**Last Updated:** 2025-11-02  
**Format Version:** 1.0

