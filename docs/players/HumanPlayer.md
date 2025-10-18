# Human Player

## Overview

The `HumanPlayer` class provides interactive gameplay where moves are selected by the user through mouse clicks or keyboard controls. This is the primary player type for human users.

## Class Definition

```python
class HumanPlayer(Player):
    """You! Play with mouse or keyboard controls"""
```

## Location
`src/Players/HumanPlayer.py`

## Key Features

### 1. Dual Input Modes
- **Mouse Mode**: Click on squares to make moves
- **Keyboard Mode**: Use arrow keys + Enter to select moves

### 2. Move Validation
- Visual feedback for valid moves (highlighted squares)
- Invalid move attempts are rejected with console message
- Only valid moves from `move_list` are accepted

### 3. Opening Book Integration
- Displays opening information when hovering over valid moves
- Shows opening names and variations
- Fixed tooltip position for stable UI
- Updates only when hover changes (performance optimization)

### 4. Game Controls
- Pause menu support (ESC key)
- Exit handling
- 60 FPS frame limiting for smooth experience

## How It Works

### Initialization

```python
def __init__(self, name='Human'):
    self.name = name
```

Simple initialization with customizable player name.

### Move Selection Process

1. **Setup Phase**
   - Cursor changes to hand icon
   - Input waiting mode enabled
   - Previous selection cleared

2. **Input Loop** (60 FPS)
   - Process pygame events
   - Check for pause/exit requests
   - Monitor mouse/keyboard input
   - Update opening book tooltips

3. **Move Validation**
   - When user selects a square:
     - Convert screen coordinates to board position
     - Create Move object
     - Validate against legal moves
     - Accept if valid, reject if invalid

4. **Opening Book Display**
   - Determines hovered move (mouse or cursor)
   - Queries opening book for that position
   - Displays tooltip with opening information
   - Clears tooltip when hover changes

### Control Flow

```
get_move() called
    ↓
Enable input, show cursor
    ↓
Wait for user input (loop)
    ↓
User selects square
    ↓
Validate move
    ↓
    Valid? → Return move
    Invalid? → Show error, continue loop
```

## User Interface

### Visual Feedback

- **Valid moves**: Highlighted on the board
- **Current position**: Cursor or mouse hover indicator
- **Opening info**: Tooltip showing opening names (if enabled)
- **Invalid moves**: Console message "This move is not valid!"

### Controls

| Input | Action |
|-------|--------|
| **Mouse Click** | Select square to play move |
| **Arrow Keys** | Move cursor (keyboard mode) |
| **Enter** | Confirm move (keyboard mode) |
| **ESC** | Open pause menu |
| **Q** | Quit game |
| **Hover over move** | Show opening book info (if available) |

## Opening Book Integration

When opening book is loaded and enabled:

```python
if control.show_opening and control.opening_book:
    # Get opening info for hovered move
    current_opening_info = control.opening_book.get_openings_for_move(
        game.history, 
        hover_move
    )
    
    # Display in fixed position tooltip
    control.view.draw_opening_info_fixed()
```

### Tooltip Behavior

- **Fixed position**: Tooltip doesn't follow cursor (stable UI)
- **Update on change**: Only redraws when different move hovered
- **Clear on unhover**: Removes tooltip when no valid move hovered
- **Performance**: Minimizes redraws for smooth 60 FPS

## Performance Optimizations

### Frame Rate Limiting
```python
clock.tick(60)  # Limit to 60 FPS
```
Prevents excessive CPU usage while maintaining smooth gameplay.

### Selective Updates
```python
if info_changed:
    # Full redraw only when tooltip changes
    control.view.clear_tooltip_area()
    control.renderModel()
    control.view.draw_opening_info_fixed()
else:
    # Normal partial update
    control.view.update(control.cursor_mode)
```

## Configuration

### Metadata

```python
PLAYER_METADATA = {
    'display_name': 'Human Player',
    'description': 'You! Play with mouse or keyboard controls',
    'enabled': True,
    'parameters': []  # No configurable parameters
}
```

### Customization

```python
# Create human player with custom name
player = HumanPlayer(name='Alice')
```

## Example Usage

```python
from Players.HumanPlayer import HumanPlayer

# Create human player
human = HumanPlayer(name='Player 1')

# In game loop
move = human.get_move(game, valid_moves, board_control)

# Move will be None if game is paused/exited
if move is None:
    # Handle pause or exit
    pass
else:
    # Execute the move
    game.move(move)
```

## Edge Cases Handled

1. **No valid moves**: Returns None (pass turn)
2. **Game pause**: Returns None, preserves pause state
3. **Game exit**: Returns None, exits cleanly
4. **Invalid selection**: Resets and waits for new input
5. **Opening book disabled**: Works without tooltips

## Integration with Control

The HumanPlayer requires a properly configured `control` object with:

- `control.cursorHand()` - Change cursor appearance
- `control.action()` - Process pygame events
- `control.renderModel()` - Redraw board
- `control.view.update()` - Update display
- `control.opening_book` - (Optional) Opening book for tooltips

## Advantages

- **Intuitive**: Natural mouse/keyboard interface
- **Informative**: Opening book integration helps learning
- **Responsive**: 60 FPS smooth gameplay
- **Forgiving**: Clear feedback on invalid moves

## See Also

- [Base Player Class](Player.md)
- [Opening Book Documentation](../OPENING_BOOK.md)
- [Game Controls](../FEATURES.md)

