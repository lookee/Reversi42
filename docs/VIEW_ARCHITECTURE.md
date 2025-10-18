# View Architecture - Modular Board Visualization

## Overview

Reversi42 v3.1.0 introduces a **modular view architecture** that allows multiple UI implementations without changing game logic. The system uses the **Strategy Pattern** with dependency injection.

## Architecture

```
AbstractBoardView (interface)
    ├── PygameBoardView (graphical - default)
    ├── TerminalBoardView (ASCII art)
    ├── HeadlessBoardView (no rendering)
    └── [Your Custom View]
```

## Components

### 1. AbstractBoardView

**File**: `src/Board/AbstractBoardView.py`

Abstract interface defining required methods for all views:

```python
class AbstractBoardView(ABC):
    @abstractmethod
    def initialize(self): pass
    
    @abstractmethod
    def render_board(self, model): pass
    
    @abstractmethod
    def render_piece(self, x, y, color): pass
    
    @abstractmethod
    def highlight_valid_moves(self, moves): pass
    
    # ... and more
```

### 2. PygameBoardView

**File**: `src/Board/PygameBoardView.py`

Full-featured graphical view with Pygame:
- Professional tournament-style interface
- Smooth anti-aliased rendering
- Opening book visual integration
- Resizable window
- Mouse and keyboard support

**Performance**: Standard (baseline)

### 3. TerminalBoardView

**File**: `src/Board/TerminalBoardView.py`

Beautiful ASCII art rendering for terminal:
- Unicode box drawing characters
- ANSI color codes
- Keyboard-only input
- Works over SSH
- Lightweight (<1KB memory)

**Performance**: Fast (no graphics overhead)

### 4. HeadlessBoardView

**File**: `src/Board/HeadlessBoardView.py`

No-rendering view for maximum performance:
- All rendering methods are no-ops
- Zero graphics overhead
- Perfect for tournaments
- Batch processing
- Automated testing

**Performance**: Maximum (0ms rendering)

## Usage

### Default (Pygame View)

```python
from Board.BoardControl import BoardControl

# Creates Pygame view automatically
control = BoardControl(8, 8)
```

### Terminal View

```python
from Board.BoardControl import BoardControl
from Board.TerminalBoardView import TerminalBoardView

# Use ASCII art terminal view
control = BoardControl(8, 8, view_class=TerminalBoardView)
```

### Headless View (Tournaments)

```python
from Board.BoardControl import BoardControl
from Board.HeadlessBoardView import HeadlessBoardView

# No rendering - maximum speed
control = BoardControl(8, 8, view_class=HeadlessBoardView)
```

### Using ViewFactory

```python
from Board.ViewFactory import ViewFactory

# Create different views easily
pygame_view = ViewFactory.create_view('pygame', 8, 8)
terminal_view = ViewFactory.create_view('terminal', 8, 8)
headless_view = ViewFactory.create_view('headless', 8, 8)
```

## Backward Compatibility

**100% backward compatible!**

Old code works without changes:
```python
from Board.BoardView import BoardView

# BoardView is now an alias for PygameBoardView
view = BoardView(8, 8, 800, 600)
# Works exactly as before!
```

## Creating Custom Views

### Step 1: Inherit from AbstractBoardView

```python
from Board.AbstractBoardView import AbstractBoardView

class MyCustomView(AbstractBoardView):
    def __init__(self, sizex, sizey, width, height):
        super().__init__(sizex, sizey, width, height)
        # Your initialization
    
    def initialize(self):
        # Setup your display
        pass
    
    def render_board(self, model):
        # Render the board
        pass
    
    # Implement all abstract methods...
```

### Step 2: Use in Game

```python
from Board.BoardControl import BoardControl
from my_views import MyCustomView

control = BoardControl(8, 8, view_class=MyCustomView)
```

### Step 3: Register in ViewFactory (Optional)

```python
from Board.ViewFactory import ViewFactory
from my_views import MyCustomView

ViewFactory.register_view('custom', MyCustomView)

# Now can use:
view = ViewFactory.create_view('custom', 8, 8)
```

## Performance Comparison

| View Type | Rendering Time | Memory | Use Case |
|-----------|---------------|--------|----------|
| **Pygame** | 10-50ms/frame | ~50MB | Interactive play, learning |
| **Terminal** | 5-15ms/frame | ~1MB | SSH, terminal purists |
| **Headless** | 0ms | ~100KB | Tournaments, testing, CI/CD |

## Examples

### Example 1: Tournament with Headless View

```python
from Board.BoardControl import BoardControl
from Board.HeadlessBoardView import HeadlessBoardView
from Reversi.Game import Game
from Players.AIPlayer import AIPlayer

# No graphics overhead!
control = BoardControl(8, 8, view_class=HeadlessBoardView)
game = Game(8)

# Run tournament games at maximum speed
for i in range(100):
    # Play game...
    pass
```

### Example 2: Terminal Mode Game

See `src/examples/terminal_mode_demo.py`

### Example 3: Custom Web View

```python
from Board.AbstractBoardView import AbstractBoardView
import json

class WebBoardView(AbstractBoardView):
    def __init__(self, sizex, sizey, width, height, websocket=None):
        super().__init__(sizex, sizey, width, height)
        self.ws = websocket
    
    def render_board(self, model):
        # Send JSON to web client
        board_json = {
            'board': [[model.getPoint(x, y) for x in range(8)] 
                     for y in range(8)],
            'black_count': self.black_count,
            'white_count': self.white_count,
        }
        if self.ws:
            self.ws.send(json.dumps(board_json))
    
    # Implement other methods...
```

## Benefits

1. **Multiple UIs** - Pygame, Terminal, Web, Mobile
2. **Testing** - Headless view for automated tests
3. **Performance** - Choose optimal view for use case
4. **Flexibility** - Easy to add new view types
5. **Separation** - Clean Model-View-Controller
6. **Accessibility** - Terminal view for screen readers

## Migration Guide

### For Existing Code

No changes needed! `BoardView` still works:

```python
from Board.BoardView import BoardView
view = BoardView(8, 8, 800, 600)
# Automatically uses PygameBoardView
```

### For New Code

Use dependency injection:

```python
from Board.BoardControl import BoardControl
from Board.TerminalBoardView import TerminalBoardView

control = BoardControl(8, 8, view_class=TerminalBoardView)
```

Or use ViewFactory:

```python
from Board.ViewFactory import ViewFactory

view = ViewFactory.create_view('terminal', 8, 8)
```

## Future Possibilities

With the modular architecture, we can easily add:

- **WebBoardView** - HTML5/WebSocket for browser play
- **MobileBoardView** - Touch-optimized interface
- **VRBoardView** - Virtual reality (why not!)
- **DiscordBotView** - Discord bot integration
- **APIBoardView** - REST API for remote play

## Files Created/Modified

### New Files
- `src/Board/AbstractBoardView.py` - Abstract interface
- `src/Board/PygameBoardView.py` - Pygame implementation
- `src/Board/HeadlessBoardView.py` - No-rendering implementation
- `src/Board/TerminalBoardView.py` - ASCII art implementation
- `src/Board/ViewFactory.py` - Factory for view creation
- `src/examples/terminal_mode_demo.py` - Terminal demo
- `src/examples/headless_tournament_demo.py` - Headless demo

### Modified Files
- `src/Board/BoardView.py` - Now backward-compatible wrapper
- `src/Board/BoardControl.py` - Added dependency injection

## See Also

- [Player Documentation](players/README.md)
- [Tournament System](../tournament/README.md)
- [Features Guide](FEATURES.md)

---

**Reversi42 v3.1.0 - Modular View Architecture** 🎨

