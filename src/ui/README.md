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
├── abstractions/           # Abstract Interfaces
│   ├── view_interface.py   # AbstractView - Rendering contract
│   └── input_interface.py  # AbstractInputHandler - Input contract
│
├── implementations/        # Concrete Implementations
│   ├── headless/          # Headless (no UI)
│   │   ├── input_handler.py
│   │   ├── view.py
│   │   └── input_providers/
│   │       ├── mock_input_provider.py
│   │       └── replay_input_provider.py
│   │
│   └── guiweb/            # Web UI integration
│       ├── bridge/
│       └── renderers/
│
├── factories/             # Factory Pattern
│   └── view_factory.py    # ViewFactory
│
└── common/               # Shared Utilities
    ├── event_bus.py
    └── theme.py
```

---

## 🎯 Usage

### Quick Start with Headless View

```python
from Board.BoardControl import BoardControl
from ui.implementations.headless import HeadlessBoardView

# Create headless view for tournaments/automation
control = BoardControl(8, 8, view_class=HeadlessBoardView)
```

### Using ViewFactory

```python
from Board.ViewFactory import ViewFactory

# Create headless view (default)
view = ViewFactory.create_view('headless', 8, 8)
```

### Manual Component Creation

```python
from Board.BoardModel import BoardModel
from ui.implementations.headless import HeadlessBoardView

# Create components
model = BoardModel(8, 8)
view = HeadlessBoardView(8, 8, 800, 600)

# Use for automated games
```

---

## 📦 Components

### Abstractions (`abstractions/`)

#### AbstractView
Pure rendering interface.

**Methods**:
- `update(cursor_mode)` - Render board update
- `setBoxWhite(x, y)` - Display white piece
- `setBoxBlack(x, y)` - Display black piece
- `setCanMoveWhite(x, y)` - Highlight white move
- `setCanMoveBlack(x, y)` - Highlight black move

#### AbstractInputHandler
Pure input interface.

**Methods**:
- `poll_events()` - Get input events
- `get_pointer_position()` - Get mouse/cursor position
- `is_available()` - Check if input ready

**Returns**: Standard `InputEvent` enum

### Implementations (`implementations/`)

#### Headless Implementation (`implementations/headless/`)

**Structure**:
```
headless/
├── input_handler.py        # HeadlessInputHandler (no-op)
├── view.py                # HeadlessBoardView (no-op)
└── input_providers/
    ├── mock_input_provider.py
    └── replay_input_provider.py
```

**Features**:
- No rendering (0ms overhead)
- No input required
- Maximum performance
- Perfect for tournaments and automation

**Use for**: Tournaments, batch processing, CI/CD, benchmarking

### Factories (`factories/`)

#### ViewFactory
Creates view instances by type.

```python
from ui.factories.view_factory import ViewFactory

# Create headless view
view = ViewFactory.create_view('headless', 8, 8)
```

---

## 🎨 Architecture Benefits

### 1. Framework Independence

**Core has NO framework dependencies**:
```python
# ui/abstractions/*.py
# NO framework imports ✅

# Imports ONLY abstractions
from ui.abstractions.view_interface import AbstractView
from ui.abstractions.input_interface import AbstractInputHandler
```

**Benefit**: Works with ANY view implementation!

### 2. Easy Testing

**Mock dependencies easily**:
```python
from ui.abstractions.view_interface import AbstractView

class MockView(AbstractView):
    def update(self, cursor_mode=False): 
        self.rendered = True
    # ... implement interface

# Test without ANY framework
model = BoardModel(8, 8)
view = MockView(8, 8, 800, 600)
# Pure logic testing ✅
```

### 3. Easy Extension

**Add new view** (e.g., custom renderer):
```
1. Create implementations/custom/
2. Create view.py (implement AbstractView)
3. Create input_handler.py (implement AbstractInputHandler)
4. Done!
```

**No changes needed**:
- Core ✓
- Other views ✓
- Abstractions ✓

### 4. Maintainability

- **Headless code**: ONE location (`implementations/headless/`)
- **Web code**: ONE location (`implementations/guiweb/`)
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
   from Board.AbstractBoardView import AbstractBoardView
   
   class MyView(AbstractBoardView):
       def update(self, cursor_mode=False):
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

4. **Use it**:
   ```python
   from Board.BoardControl import BoardControl
   from ui.implementations.myview import MyView
   
   control = BoardControl(8, 8, view_class=MyView)
   ```

---

## 📊 Metrics

### Code Organization

| Component | Files | Lines | Framework Deps |
|-----------|-------|-------|----------------|
| Abstractions | 3 | 400 | 0 ✅ |
| Factories | 1 | 85 | 0 ✅ |
| Headless Impl | 5 | 350 | 0 ✅ |
| Common | 3 | 200 | 0 ✅ |
| **TOTAL** | **12** | **1,035** | **None** ✅ |

---

## 🚀 Web Interface

For interactive play, use the **WebGUI** interface. See [WebGUI Documentation](../../docs/WEBGUI.md) for details.

The web interface provides:
- Real-time game visualization
- WebSocket communication
- Modern browser-based UI
- Cross-platform compatibility

---

## 📚 See Also

- **[WEBGUI.md](../../docs/WEBGUI.md)** - Web interface documentation
- **[Board/README.md](../Board/README.md)** - Board module documentation
- **[Architecture Documentation](../../docs/architecture/README.md)** - System architecture

---

**Reversi42 v5.0.0 - Web-First MVC Architecture** ✨
