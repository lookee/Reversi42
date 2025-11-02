# UI Package - Professional MVC Architecture

## 📖 Overview

This package provides a professional, framework-agnostic Model-View-Controller (MVC) architecture for Reversi42's user interface.

**Version**: 5.0.0  
**Architecture**: Clean MVC with Dependency Inversion  
**Status**: Production Ready

---

## 🏗️ Architecture

### Design Principles

1. **Separation of Concerns** - Model/View/Input/Controller completely separated
2. **Dependency Inversion** - Depend on abstractions, not implementations
3. **Framework Independence** - Core has zero framework dependencies
4. **Single Responsibility** - Each class has one job
5. **Open/Closed** - Open for extension, closed for modification

### Directory Structure

```
ui/
├── core/                    # MVC Core (Framework-Agnostic)
│   ├── model.py            # BoardModel - Domain logic
│   ├── state.py            # GameState - Shared state
│   └── controller.py       # BoardController - Orchestration
│
├── abstractions/           # Abstract Interfaces
│   ├── view_interface.py   # AbstractView - Rendering contract
│   └── input_interface.py  # AbstractInputHandler - Input contract
│
├── implementations/        # Concrete Implementations
│   ├── pygame/            # Pygame-specific code
│   │   ├── input_handler.py
│   │   ├── view.py
│   │   └── components/
│   │       ├── menu.py
│   │       ├── game_over.py
│   │       ├── pause_menu.py
│   │       └── dialog_box.py
│   │
│   ├── terminal/          # Terminal-specific code
│   │   └── input_handler.py
│   │
│   └── headless/          # Headless (no UI)
│       └── input_handler.py
│
├── factories/             # Factory Pattern
│   ├── view_factory.py    # ViewFactory
│   └── ui_factory.py      # UIFactory (complete UI creation)
│
├── utils/                 # Shared Utilities
│   └── (future utilities)
│
└── legacy/                # Backward Compatibility
    └── __init__.py        # Wrappers to src/Board/
```

---

## 🎯 Usage

### Quick Start with UIFactory

```python
from ui.factories.ui_factory import UIFactory

# Create complete UI stack (one line!)
controller, model, view, input_handler, state = UIFactory.create_pygame_ui()

# Game loop
while not state.should_exit:
    controller.update()  # Input → Logic → Render
```

### Manual Component Creation

```python
from ui.core.model import BoardModel
from ui.core.state import GameState
from ui.core.controller import BoardController
from ui.implementations.pygame.input_handler import PygameInputHandler
from ui.implementations.pygame.view import PygameBoardView

# Create components
model = BoardModel(8, 8)
state = GameState()
input_handler = PygameInputHandler()
view = PygameBoardView(8, 8, 800, 600)

# Create controller
controller = BoardController(model, view, input_handler, state)

# Use
controller.process_input()
controller.render()
```

### Creating Different UI Types

```python
from ui.factories.ui_factory import UIFactory

# Pygame (graphical)
controller, *rest = UIFactory.create_pygame_ui()

# Terminal (ASCII art)
controller, *rest = UIFactory.create_terminal_ui()

# Headless (no UI - for tournaments)
controller, *rest = UIFactory.create_headless_ui()
```

---

## 📦 Components

### Core (`core/`)

#### BoardModel
Pure domain logic for board state.

```python
model = BoardModel(8, 8)
model.setPoint(3, 3, 'B')  # Set black piece
value = model.getPoint(3, 3)  # Get cell value
board = model.to_2d_array()  # Get 2D array
```

**Responsibilities**: Board state only  
**NO**: UI, input, rendering

#### GameState
Shared state container using dataclass.

```python
state = GameState()
state.black_score = 10
state.white_score = 8
state.current_turn = 'W'
```

**Responsibilities**: State management  
**NO**: Logic, UI

#### BoardController
Framework-agnostic orchestrator.

```python
controller = BoardController(model, view, input_handler, state)
controller.update()  # One update cycle
```

**Responsibilities**: Coordination  
**NO**: Framework specifics, rendering, input

### Abstractions (`abstractions/`)

#### AbstractView
Pure rendering interface.

**Methods**:
- `render_board(board_state)` - Render board
- `show_game_info(info)` - Display scores, turn
- `highlight_cells(positions, type)` - Highlight cells
- `update_display()` - Refresh display

**NOT included**: Input handling (that's InputHandler's job)

#### AbstractInputHandler
Pure input interface.

**Methods**:
- `poll_events()` - Get input events
- `get_pointer_position()` - Get mouse/cursor position
- `is_available()` - Check if input ready

**Returns**: Standard `InputEvent` enum

### Implementations (`implementations/`)

#### Pygame Implementation (`implementations/pygame/`)

**Structure**:
```
pygame/
├── input_handler.py    # PygameInputHandler
├── view.py            # PygameView (BoardView)
└── components/        # UI components
    ├── menu.py
    ├── game_over.py
    ├── pause_menu.py
    └── dialog_box.py
```

**Features**:
- Mouse + keyboard input
- Graphical rendering
- Full UI components

#### Terminal Implementation (`implementations/terminal/`)

**Structure**:
```
terminal/
└── input_handler.py    # TerminalInputHandler
```

**Features**:
- Keyboard-only input
- Cross-platform (readchar/termios)
- No mouse support

#### Headless Implementation (`implementations/headless/`)

**Structure**:
```
headless/
└── input_handler.py    # HeadlessInputHandler (no-op)
```

**Features**:
- No rendering
- No input
- Maximum performance

### Factories (`factories/`)

#### ViewFactory
Creates view instances by type.

```python
from ui.factories.view_factory import ViewFactory

view = ViewFactory.create_view('pygame', 8, 8, 800, 600)
view = ViewFactory.create_view('terminal', 8, 8, 80, 24)
view = ViewFactory.create_view('headless', 8, 8)
```

#### UIFactory
Creates complete UI stacks.

```python
from ui.factories.ui_factory import UIFactory

# Get everything you need
controller, model, view, input_handler, state = UIFactory.create_pygame_ui()
```

---

## 🎨 Architecture Benefits

### 1. Framework Independence

**Controller has NO framework dependencies**:
```python
# ui/core/controller.py
# NO import pygame ✅
# NO import curses ✅
# NO framework imports ✅

# Imports ONLY abstractions
from ui.abstractions.view_interface import AbstractView
from ui.abstractions.input_interface import AbstractInputHandler
```

**Benefit**: Controller works with ANY view implementation!

### 2. Easy Testing

**Mock dependencies easily**:
```python
class MockView(AbstractView):
    def render_board(self, state): self.rendered = True
    def update_display(self): pass
    # ... implement interface

class MockInput(AbstractInputHandler):
    def poll_events(self): return []
    # ... implement interface

# Test controller without ANY framework
controller = BoardController(model, MockView(), MockInput())
# Pure logic testing ✅
```

### 3. Easy Extension

**Add new view** (e.g., Web):
```
1. Create implementations/web/
2. Create view.py (implement AbstractView)
3. Create input_handler.py (implement AbstractInputHandler)
4. Done!
```

**No changes needed**:
- Core ✓
- Other views ✓
- Controller ✓

### 4. Maintainability

- **Pygame code**: ONE location (`implementations/pygame/`)
- **Terminal code**: ONE location (`implementations/terminal/`)
- **Core logic**: Separate from UI

**Result**: Easy to find, modify, and maintain!

---

## 🔧 Adding New View Types

### Step-by-Step Guide

1. **Create directory**:
   ```bash
   mkdir -p src/ui/implementations/myview/
   ```

2. **Implement AbstractView**:
   ```python
   # implementations/myview/view.py
   from ui.abstractions.view_interface import AbstractView
   
   class MyView(AbstractView):
       def render_board(self, board_state):
           # Your rendering code
           pass
       
       # ... implement all abstract methods
   ```

3. **Implement AbstractInputHandler**:
   ```python
   # implementations/myview/input_handler.py
   from ui.abstractions.input_interface import AbstractInputHandler, InputEvent
   
   class MyInputHandler(AbstractInputHandler):
       def poll_events(self):
           # Your input handling
           return []
       
       # ... implement all abstract methods
   ```

4. **Create package**:
   ```python
   # implementations/myview/__init__.py
   from .view import MyView
   from .input_handler import MyInputHandler
   
   __all__ = ['MyView', 'MyInputHandler']
   ```

5. **Use it**:
   ```python
   from ui.core.controller import BoardController
   from ui.implementations.myview import MyView, MyInputHandler
   
   controller = BoardController(model, MyView(), MyInputHandler())
   ```

---

## 📊 Metrics

### Code Organization

| Component | Files | Lines | Framework Deps |
|-----------|-------|-------|----------------|
| Core | 3 | 342 | 0 ✅ |
| Abstractions | 2 | 331 | 0 ✅ |
| Factories | 2 | 170 | 0 ✅ |
| Pygame Impl | 6 | 2,476 | Pygame only ✅ |
| Terminal Impl | 1 | 200 | 0 ✅ |
| Headless Impl | 1 | 60 | 0 ✅ |
| **TOTAL** | **15** | **3,579** | **Isolated** ✅ |

### Pygame Isolation Score: 100%

- Core: 0/3 files with pygame (0%) ✅
- Abstractions: 0/2 files with pygame (0%) ✅
- Factories: 0/2 files with pygame (0%) ✅
- Pygame Impl: 6/6 files (100% - expected) ✅
- Other Impl: 0/2 files with pygame (0%) ✅

**Overall Score**: ✅ Perfect Isolation

---

## 🚀 Migration from Legacy Board Module

### Compatibility Layer

The `ui/legacy/` module provides compatibility with existing `src/Board/` code:

```python
# Old code (still works)
from Board.BoardControl import BoardControl
control = BoardControl(8, 8)

# New code (recommended)
from ui.factories.ui_factory import UIFactory
controller, *_ = UIFactory.create_pygame_ui()
```

**Both work!** ✓

### Migration Timeline

- **v5.0.0** (Current): Pygame/Terminal views removed, Web interface primary
- **v4.0.0** (Future): Full migration to web-only architecture

---

## 📚 See Also

- **ARCHITECTURE_ANALYSIS.md** - Complete architectural analysis
- **ARCHITECTURE_EVOLUTION.md** - Implementation report
- **PYGAME_ISOLATION_COMPLETE.md** - Isolation verification
- **docs/VIEW_ARCHITECTURE.md** - View system documentation

---

**Reversi42 v5.0.0 - Web-First MVC Architecture** ✨

