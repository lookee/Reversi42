# Board Module - Modular MVC Architecture

## Overview

The Board module implements a clean Model-View-Controller architecture with **pluggable views**. As of v5.0.0, the primary interface is web-based (WebGUI), with headless mode for tournaments and automated testing.

## Components

### Model
- **BoardModel.py** - Board state (matrix representation)

### View (Modular!)
- **AbstractBoardView.py** - Abstract interface for all views
- **HeadlessBoardView.py** - No-rendering view for tournaments and testing
- **ViewFactory.py** - Factory for creating views

### Controller
- **BoardControl.py** - Manages Model-View interaction

## Available Views

### HeadlessBoardView (Default)

**Zero rendering overhead**
- All rendering methods are no-ops
- Maximum performance
- Minimal memory footprint
- Perfect for automation

**Use for**: Tournaments, batch processing, CI/CD, benchmarking, testing

```python
from Board.BoardControl import BoardControl
from ui.implementations.headless import HeadlessBoardView

control = BoardControl(8, 8, view_class=HeadlessBoardView)
```

### WebGUI (Recommended for Interactive Play)

For interactive play, use the web-based interface. See [WebGUI Documentation](../../docs/WEBGUI.md).

## Using ViewFactory

Simplest way to create views:

```python
from Board.ViewFactory import ViewFactory

# Create headless view (default)
headless_view = ViewFactory.create_view('headless', 8, 8)
```

## Dependency Injection

BoardControl supports view injection:

```python
from Board.BoardControl import BoardControl
from ui.implementations.headless import HeadlessBoardView

# Inject custom view
control = BoardControl(8, 8, view_class=HeadlessBoardView)
```

## Creating Custom Views

### Step 1: Inherit from AbstractBoardView

```python
from Board.AbstractBoardView import AbstractBoardView

class MyCustomView(AbstractBoardView):
    def initialize(self):
        # Your init code
        pass
    
    def update(self, cursor_mode=False):
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

## Performance

The headless view has:
- **Rendering**: 0ms (no-op)
- **Memory**: ~100KB
- **Best for**: Tournaments, testing, automation

## Architecture Diagram

```
Game Logic (Reversi.Game)
    ↓
BoardControl (MVC Controller)
    ├── BoardModel (State)
    └── AbstractBoardView (Interface)
            ├── HeadlessBoardView (None)
            └── [Your Custom View]
```

## Benefits

1. **Multiple UIs** - Swap views without changing code
2. **Testing** - Headless view for automated tests
3. **Performance** - Optimal performance with headless view
4. **Extensibility** - Easy to add new view types
5. **Clean Design** - Perfect separation of concerns

## See Also

- [WebGUI Documentation](../../docs/WEBGUI.md) - Web-based interface
- [Main README](../../README.md) - Project overview
- [Architecture Documentation](../../docs/architecture/README.md) - System architecture

---

**Reversi42 v5.0.0 - Modular View Architecture** 🎨
