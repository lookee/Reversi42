# Board Module - Modular MVC Architecture

## Overview

The Board module implements a clean Model-View-Controller architecture with **pluggable views**. As of v3.1.0, multiple view implementations are supported without changing game logic.

## Components

### Model
- **BoardModel.py** - Board state (matrix representation)

### View (Modular!)
- **AbstractBoardView.py** - Abstract interface (NEW in 3.1.0)
- **PygameBoardView.py** - Graphical Pygame view (NEW in 3.1.0)
- **TerminalBoardView.py** - ASCII art terminal view (NEW in 3.1.0)
- **HeadlessBoardView.py** - No-rendering view (NEW in 3.1.0)
- **BoardView.py** - Backward compatibility wrapper
- **ViewFactory.py** - Factory for creating views (NEW in 3.1.0)

### Controller
- **BoardControl.py** - Manages Model-View interaction (ENHANCED in 3.1.0)

## Available Views

### 1. PygameBoardView (Default)

**Full-featured graphical UI**
- Professional tournament interface
- Opening book visual integration
- Mouse + keyboard support
- Resizable window
- 60 FPS smooth rendering

**Use for**: Interactive play, learning, demonstrations

```python
from Board.BoardControl import BoardControl

# Default - creates Pygame view
control = BoardControl(8, 8)
```

### 2. TerminalBoardView

**Beautiful ASCII art rendering**
- Unicode box drawing
- ANSI color codes
- Keyboard-only input
- Works over SSH
- Lightweight

**Use for**: Terminal purists, SSH sessions, accessibility

```python
from Board.BoardControl import BoardControl
from Board.TerminalBoardView import TerminalBoardView

control = BoardControl(8, 8, view_class=TerminalBoardView)
```

### 3. HeadlessBoardView

**Zero rendering overhead**
- All rendering methods are no-ops
- Maximum performance
- Minimal memory footprint
- Perfect for automation

**Use for**: Tournaments, batch processing, CI/CD, benchmarking

```python
from Board.BoardControl import BoardControl
from Board.HeadlessBoardView import HeadlessBoardView

control = BoardControl(8, 8, view_class=HeadlessBoardView)
```

## Using ViewFactory

Simplest way to create views:

```python
from Board.ViewFactory import ViewFactory

# Create different views
pygame_view = ViewFactory.create_view('pygame', 8, 8)
terminal_view = ViewFactory.create_view('terminal', 8, 8)
headless_view = ViewFactory.create_view('headless', 8, 8)
```

## Dependency Injection

BoardControl now supports view injection:

```python
from Board.BoardControl import BoardControl
from Board.TerminalBoardView import TerminalBoardView

# Inject custom view
control = BoardControl(8, 8, view_class=TerminalBoardView)

# View is now TerminalBoardView instead of PygameBoardView!
```

## Backward Compatibility

**100% backward compatible!**

All existing code works without changes:

```python
# Old code still works!
from Board.BoardView import BoardView

view = BoardView(8, 8, 800, 600)
# Automatically uses PygameBoardView internally
```

## Creating Custom Views

### Step 1: Inherit from AbstractBoardView

```python
from Board.AbstractBoardView import AbstractBoardView

class MyCustomView(AbstractBoardView):
    def initialize(self):
        # Your init code
        pass
    
    def render_board(self, model):
        # Your rendering
        pass
    
    # Implement all required abstract methods
```

### Step 2: Use in Game

```python
from Board.BoardControl import BoardControl
from my_module import MyCustomView

control = BoardControl(8, 8, view_class=MyCustomView)
```

## Performance Comparison

| View | Rendering | Memory | Best For |
|------|-----------|--------|----------|
| **Pygame** | 10-50ms | ~50MB | Interactive play |
| **Terminal** | 5-15ms | ~1MB | SSH, terminal |
| **Headless** | 0ms | ~100KB | Tournaments, testing |

## Examples

See `src/examples/`:
- `terminal_mode_demo.py` - Terminal view demonstration
- `headless_tournament_demo.py` - Performance comparison

## Architecture Diagram

```
Game Logic (Reversi.Game)
    ↓
BoardControl (MVC Controller)
    ├── BoardModel (State)
    └── AbstractBoardView (Interface)
            ├── PygameBoardView (Pygame)
            ├── TerminalBoardView (ASCII)
            ├── HeadlessBoardView (None)
            └── [Your Custom View]
```

## Benefits

1. **Multiple UIs** - Swap views without changing code
2. **Testing** - Headless view for automated tests
3. **Performance** - Choose optimal view for use case
4. **Accessibility** - Terminal view for screen readers
5. **Extensibility** - Easy to add new view types
6. **Clean Design** - Perfect separation of concerns

## See Also

- [VIEW_ARCHITECTURE.md](../../docs/VIEW_ARCHITECTURE.md) - Detailed architecture documentation
- [Main README](../../README.md) - Project overview
- [Features](../../docs/FEATURES.md) - Complete feature list

---

**Reversi42 v3.1.0 - Modular View Architecture** 🎨

