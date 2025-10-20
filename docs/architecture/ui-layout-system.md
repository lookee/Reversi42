# UI Layout System - Bootstrap-like Primitives

**Author:** Luca Amore  
**Date:** October 2025  
**Status:** Active  
**Version:** 1.0

## Overview

Reversi42 utilizza un sistema di layout dichiarativo ispirato a Bootstrap e CSS Flexbox per costruire interfacce utente responsive e manutenibili. Il sistema riduce drasticamente il boilerplate code e elimina i calcoli manuali di posizionamento.

### Design Goals

1. **Dichiarativo**: Layout definiti tramite composizione di container, non calcoli
2. **Responsive**: Adattamento automatico alle dimensioni dello schermo
3. **Manutenibile**: Codice pulito, leggibile e facile da modificare
4. **Riusabile**: Primitive composabili per qualsiasi tipo di layout
5. **Type-Safe**: Supporto completo per type hints Python

### Impact

Il sistema ha ridotto il codice UI del **47-50%**:
- `menu.py`: 120 LoC → 60 LoC (-50%)
- `pause_menu.py`: 95 LoC → 50 LoC (-47%)
- `game_over.py`: 140 LoC → 70 LoC (-50%)

## Architecture

### Component Hierarchy

```
Widget (base)
├── Container
│   ├── VBox (vertical layout)
│   ├── HBox (horizontal layout)
│   └── Grid (grid layout)
└── Layout Primitives
    ├── Stack (enhanced VBox)
    ├── Center (auto-centering)
    ├── Row/Col (12-column grid)
    ├── Spacer (flexible spacing)
    └── Divider (visual separator)
```

### Design Patterns

1. **Composite Pattern**: Hierarchical widget composition
2. **Strategy Pattern**: Flexible alignment and distribution strategies
3. **Decorator Pattern**: Layout containers enhance widget positioning
4. **Template Method**: Consistent layout calculation pipeline

## Visual Layout Guide

### Layout Comparison: Before vs After

**Before (Manual Positioning):**
```
┌─────────────────────────────────────┐
│                                     │
│  x = (800 - 300) // 2  → ❌ Math   │
│  y = (600 - 400) // 2  → ❌ Math   │
│                                     │
│         ┌───────────┐               │
│         │  Widget   │  ← Manual    │
│         │  (x, y)   │  ← Position  │
│         └───────────┘               │
│                                     │
└─────────────────────────────────────┘
```

**After (Declarative Layout):**
```
┌─────────────────────────────────────┐
│    Center(width=800, height=600)    │
│                                     │
│         ┌───────────┐               │
│         │  Widget   │  ← Auto      │
│         │ Centered! │  ← Centered! │
│         └───────────┘               │
│                                     │
└─────────────────────────────────────┘
```

## Auto-Centering System

### Widget Parameter: `center_in_parent`

**Ogni widget** può ora essere automaticamente centrato nel suo parent container semplicemente impostando `center_in_parent=True`.

**Vantaggi:**
- ✅ Zero calcoli manuali
- ✅ Funziona con qualsiasi container (VBox, HBox, Stack)
- ✅ Override automatico dell'allineamento del container
- ✅ Codice ultra-pulito

**Example:**
```python
# Prima (manuale)
label = Label("Title")
label_x = (container_width - label_width) // 2
label.set_position(label_x, y)

# Dopo (automatico)
label = Label("Title")
label.center_in_parent = True
container.add(label)  # Centrato automaticamente! ✨
```

**Visual:**
```
Container senza center_in_parent:    Container con center_in_parent:
┌────────────────────────────┐      ┌────────────────────────────┐
│ [Widget]                   │      │      [Widget]              │
│  ↑ aligned by container    │      │   ↑ forced centered!       │
└────────────────────────────┘      └────────────────────────────┘
```

### Title() Helper Function

**Helper function** per creare titoli centrati automaticamente.

```python
from ui.widgets.primitives import Title

# Crea un Label con center_in_parent=True automaticamente!
layout = Stack(gap=20)
layout.add(Title("Game Menu"))  # ← Auto-centered! ✨
layout.add(Button("Start"))
```

**Signature:**
```python
def Title(
    text: str, 
    font_size: int = 48, 
    color: Tuple[int, int, int] = (230, 240, 235)
) -> Label
```

**Equivalente a:**
```python
label = Label(text, font_size=font_size, color=color)
label.center_in_parent = True
return label
```

## Core Primitives

### Stack - Enhanced Vertical Layout

Stack è un VBox potenziato con capacità di allineamento e distribuzione tipo CSS Flexbox.

**Visual Diagram:**
```
Stack(gap=20, align="center", justify="start")
┌─────────────────────────────────────┐
│           Stack Container           │
│  padding                            │
│  ┌─────────────────────────────┐   │
│  │      Title (centered)       │   │
│  └─────────────────────────────┘   │
│             ↕ gap=20                │
│  ┌─────────────────────────────┐   │
│  │     Button (centered)       │   │
│  └─────────────────────────────┘   │
│             ↕ gap=20                │
│  ┌─────────────────────────────┐   │
│  │     Button (centered)       │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Features:**
- Allineamento orizzontale degli elementi
- Distribuzione verticale (justify-content)
- Gap semantico invece di spacing
- Supporto per stretch e space-between

**API:**
```python
Stack(
    gap: int = 0,                    # Space between items
    align: Literal["start", "center", "end", "stretch"] = "start",
    justify: Literal["start", "center", "end", "space-between", "space-around"] = "start",
    **kwargs
)
```

**Example:**
```python
from ui.widgets.base import Stack
from ui.widgets.primitives import Label, Button

# Vertical stack with centered items
menu = Stack(gap=20, align="center", justify="center")
menu.set_size(800, 600)

menu.add(Label("Game Menu", font_size=48))
menu.add(Button("Start Game", width=300))
menu.add(Button("Quit", width=300))
```

**Alignment Options (Horizontal):**

```
align="start"          align="center"         align="end"
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ [Small]      │      │    [Small]   │      │      [Small] │
│ [Medium Btn] │      │ [Medium Btn] │      │ [Medium Btn] │
│ [Big Button] │      │ [Big Button] │      │ [Big Button] │
└──────────────┘      └──────────────┘      └──────────────┘
```

**Justify Options (Vertical Distribution):**

```
justify="start"       justify="center"      justify="end"
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ [Button 1]   │      │              │      │              │
│ [Button 2]   │      │              │      │              │
│ [Button 3]   │      │ [Button 1]   │      │              │
│              │      │ [Button 2]   │      │              │
│              │      │ [Button 3]   │      │ [Button 1]   │
│              │      │              │      │ [Button 2]   │
│              │      │              │      │ [Button 3]   │
└──────────────┘      └──────────────┘      └──────────────┘

justify="space-between"                justify="space-around"
┌──────────────┐                       ┌──────────────┐
│ [Button 1]   │                       │              │
│              │                       │ [Button 1]   │
│              │                       │              │
│ [Button 2]   │                       │ [Button 2]   │
│              │                       │              │
│              │                       │ [Button 3]   │
│ [Button 3]   │                       │              │
└──────────────┘                       └──────────────┘
```

### Center - Automatic Centering

Center automatically centers its child widget, eliminating manual position calculations.

**Visual Diagram:**
```
Center(width=800, height=600, horizontal=True, vertical=True)
┌───────────────────────────────────────────────────────────┐
│                                                           │
│                                                           │
│                                                           │
│                  ┌─────────────────┐                     │
│                  │                 │                     │
│                  │  Child Widget   │  ← Auto centered!   │
│                  │    (centered)   │                     │
│                  │                 │                     │
│                  └─────────────────┘                     │
│                                                           │
│                                                           │
│                                                           │
└───────────────────────────────────────────────────────────┘

Center(horizontal=True, vertical=False)
┌───────────────────────────────────────────────────────────┐
│                  ┌─────────────────┐                     │
│                  │  Child (top)    │  ← Centered X only  │
│                  └─────────────────┘                     │
│                                                           │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

**API:**
```python
Center(
    width: int = 0,
    height: int = 0,
    horizontal: bool = True,
    vertical: bool = True
)
```

**Example:**
```python
from ui.widgets.base import Center

# Center a panel on screen
center = Center(width=800, height=600)
center.add(game_panel)  # Automatically centered!

# Only horizontal centering
center = Center(width=800, height=600, horizontal=True, vertical=False)
```

**Before (manual):**
```python
panel_x = (screen_width - panel_width) // 2
panel_y = (screen_height - panel_height) // 2
panel.set_position(panel_x, panel_y)
```

**After (declarative):**
```python
center = Center(width=screen_width, height=screen_height)
center.add(panel)
```

### Row/Col - Bootstrap Grid System

12-column grid system for responsive layouts, identical to Bootstrap's grid.

**Visual Diagram - 12 Column Grid:**
```
Full Row (12 columns)
┌─────────────────────────────────────────────────────────────┐
│ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │ 10 │ 11 │ 12 │
└─────────────────────────────────────────────────────────────┘

Row with Col(span=6) + Col(span=6) - 50/50 split
┌─────────────────────────────────────────────────────────────┐
│                Left (6/12)              │    Right (6/12)    │
│            Col(span=6)                  │   Col(span=6)      │
└─────────────────────────────────────────────────────────────┘

Row with Col(span=4) + Col(span=4) + Col(span=4) - Three columns
┌─────────────────────────────────────────────────────────────┐
│       Col 1       │       Col 2       │       Col 3        │
│    Col(span=4)    │    Col(span=4)    │    Col(span=4)     │
└─────────────────────────────────────────────────────────────┘

Row with Col(span=3) + Col(span=6) + Col(span=3) - Sidebar layout
┌─────────────────────────────────────────────────────────────┐
│   Side  │            Main Content            │   Side      │
│  (3/12) │              (6/12)                │  (3/12)     │
└─────────────────────────────────────────────────────────────┘

Row with Col(span=2) + Col(span=8) + Col(span=2) - Wide center
┌─────────────────────────────────────────────────────────────┐
│ Nav │              Content (8/12)               │  Sidebar │
│(2/12)│                                           │  (2/12)  │
└─────────────────────────────────────────────────────────────┘
```

**Common Layouts:**
```
Full Width:        Col(span=12)           → 100%
Half Width:        Col(span=6)            → 50%
Third Width:       Col(span=4)            → 33.33%
Quarter Width:     Col(span=3)            → 25%
Two Thirds:        Col(span=8)            → 66.66%
```

**API:**
```python
Row(gap: int = 10, align: str = "top", **kwargs)
Col(span: int = 12, child: Widget = None, **kwargs)
```

**Column Spans:**
- `span=12`: Full width (100%)
- `span=6`: Half width (50%)
- `span=4`: Third width (33.33%)
- `span=3`: Quarter width (25%)
- `span=2`: Sixth width (16.66%)

**Example:**
```python
from ui.widgets.base import Row, Col
from ui.widgets.primitives import Button

# Two-column layout (50/50)
row = Row(gap=20)
row.add(Col(span=6, child=Button("Left", width=280)))
row.add(Col(span=6, child=Button("Right", width=280)))

# Three-column layout (25/50/25)
row = Row(gap=10)
row.add(Col(span=3, child=sidebar))
row.add(Col(span=6, child=main_content))
row.add(Col(span=3, child=sidebar2))
```

### HBox - Horizontal Layout

Arranges widgets horizontally with vertical alignment options.

**Visual Diagram:**
```
HBox(spacing=30, align="center")
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌──────┐  ←30px→  ┌──────┐  ←30px→  ┌──────┐        │
│  │ Btn1 │          │ Btn2 │          │ Btn3 │  ← All  │
│  └──────┘          └──────┘          └──────┘    center│
│                                                   aligned│
└─────────────────────────────────────────────────────────┘

HBox Alignment Options:
┌──────────────────────────────────────────────────────────┐
│ align="top"           align="center"        align="bottom"│
│ ┌──────┐ ┌──────┐    ┌──────┐ ┌──────┐    ┌──────┐ ┌──────┐│
│ │Small │ │Tall  │    │      │ │      │    │      │ │      ││
│ └──────┘ │      │    │Small │ │Tall  │    │Small │ │Tall  ││
│          │      │    └──────┘ │      │    └──────┘ │      ││
│          └──────┘             └──────┘             └──────┘│
└──────────────────────────────────────────────────────────┘
```

**API:**
```python
HBox(
    spacing: int = 5,
    align: Literal["top", "center", "bottom"] = "top",
    **kwargs
)
```

**Example:**
```python
from ui.widgets.base import HBox
from ui.widgets.primitives import Button

# Horizontal button row with center alignment
buttons = HBox(spacing=30, align="center")
buttons.add(Button("Help", width=150, height=40))
buttons.add(Button("About", width=150, height=40))
buttons.add(Button("Quit", width=150, height=40))
```

### Spacer - Flexible Spacing

Invisible component for adding space between widgets.

**API:**
```python
Spacer(width: int = 0, height: int = 0)
```

**Example:**
```python
from ui.widgets.base import HBox, Spacer
from ui.widgets.primitives import Button

# Buttons with fixed spacing
row = HBox()
row.add(Button("Left"))
row.add(Spacer(width=100))  # 100px gap
row.add(Button("Right"))
```

### Divider - Visual Separator

Line separator for visual grouping.

**API:**
```python
Divider(
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    width: int = 100,
    height: int = 1,
    color: tuple = (100, 100, 110),
    thickness: int = 1
)
```

**Example:**
```python
from ui.widgets.base import Stack, Divider
from ui.widgets.primitives import Label

menu = Stack(gap=15)
menu.add(Label("Section 1"))
menu.add(Divider(orientation="horizontal", width=200))
menu.add(Label("Section 2"))
```

## Real-World Examples

### Complete Layout Diagrams

**Example 1: Main Menu Layout (Stack + HBox)**
```
┌───────────────────────────────────────────────────────┐
│              Stack(justify="center")                  │
│                                                       │
│              ┌─────────────────┐                     │
│              │   Reversi42     │  ← Title            │
│              └─────────────────┘                     │
│                     ↕ gap=40                         │
│    ┌──────────────────────────────────────┐         │
│    │ Stack(align="center") - Game Panel   │         │
│    │  padding=20                           │         │
│    │  ┌────────────────────────────────┐  │         │
│    │  │  HBox(spacing=30)              │  │         │
│    │  │  ┌──────────┐  ┌──────────┐   │  │         │
│    │  │  │ Black: AI│  │ White: AI│   │  │         │
│    │  │  └──────────┘  └──────────┘   │  │         │
│    │  └────────────────────────────────┘  │         │
│    │              ↕ gap=15                 │         │
│    │  ┌────────────────────────────────┐  │         │
│    │  │      [Start Game]              │  │         │
│    │  └────────────────────────────────┘  │         │
│    │              ↕ gap=15                 │         │
│    │  ┌────────────────────────────────┐  │         │
│    │  │       [Book: ON]               │  │         │
│    │  └────────────────────────────────┘  │         │
│    └──────────────────────────────────────┘         │
│                     ↕ gap=40                         │
│         ┌─────────────────────────────┐              │
│         │ HBox(spacing=30)            │              │
│         │ [Help] [About] [Quit]       │              │
│         └─────────────────────────────┘              │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Example 2: Pause Menu (Center + Stack)**
```
┌───────────────────────────────────────────────────────┐
│         Center(width=800, height=600)                 │
│                                                       │
│         ┌──────────────────────────┐                 │
│         │ Stack(gap=20, center)    │                 │
│         │  padding=30              │                 │
│         │  ┌────────────────────┐  │                 │
│         │  │   GAME PAUSED      │  │                 │
│         │  └────────────────────┘  │                 │
│         │          ↕ gap=20        │                 │
│         │  ┌────────────────────┐  │                 │
│         │  │  [Resume Game]     │  │                 │
│         │  └────────────────────┘  │                 │
│         │  ┌────────────────────┐  │                 │
│         │  │  [Save Game]       │  │  All buttons   │
│         │  └────────────────────┘  │  centered      │
│         │  ┌────────────────────┐  │  automatically!│
│         │  │  [Load Game]       │  │                 │
│         │  └────────────────────┘  │                 │
│         │  ┌────────────────────┐  │                 │
│         │  │  [Return to Menu]  │  │                 │
│         │  └────────────────────┘  │                 │
│         │  ┌────────────────────┐  │                 │
│         │  │      [Quit]        │  │                 │
│         │  └────────────────────┘  │                 │
│         └──────────────────────────┘                 │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Example 3: Dashboard (Row + Col)**
```
┌───────────────────────────────────────────────────────┐
│                Row (Header - span=12)                 │
│  ┌────────────────────────────────────────────────┐  │
│  │              Dashboard Title                   │  │
│  └────────────────────────────────────────────────┘  │
├───────────────────────────────────────────────────────┤
│          Row (Main Content - sidebar + content)       │
│  ┌──────────┐ │ ┌───────────────────────────────┐   │
│  │          │ │ │                               │   │
│  │ Sidebar  │ │ │      Main Content             │   │
│  │ Col(3)   │ │ │      Col(9)                   │   │
│  │          │ │ │                               │   │
│  └──────────┘ │ └───────────────────────────────┘   │
├───────────────────────────────────────────────────────┤
│              Row (Footer - 3 columns)                 │
│  ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐        │
│  │ Col(4)   │ │ │ Col(4)   │ │ │ Col(4)   │        │
│  │ [Stats]  │ │ │[Settings]│ │ │  [Help]  │        │
│  └──────────┘ │ └──────────┘ │ └──────────┘        │
└───────────────────────────────────────────────────────┘
```

### Main Menu with Auto-Centering

**New in 2025: Ultra-Clean with Title() and center_in_parent!**

```python
def _build_main_menu(self):
    # Main layout
    layout = Stack(gap=40, align="center", justify="center")
    layout.set_size(self.width, self.height)
    
    # Title - auto-centered with Title()!
    layout.add(Title("Reversi42"))  # ← 1 line instead of 3!
    
    # Panel - centered with center_in_parent!
    panel = Stack(gap=15, align="center")
    panel.background_color = (30, 50, 40)
    panel.padding = 20
    panel.center_in_parent = True  # ← Magic! ✨
    panel.set_size(int(self.width * 0.85), 0)  # 85% wide
    
    # Players row
    players = HBox(spacing=30)
    players.add(Button("Black: AI"))
    players.add(Button("White: AI"))
    panel.add(players)
    
    panel.add(Button("Start Game", width=300))
    panel.add(Button("Book: ON", width=280))
    layout.add(panel)
    
    # Bottom buttons
    sections = HBox(spacing=30)
    sections.add(Button("Help", width=150))
    sections.add(Button("About", width=150))
    sections.add(Button("Quit", width=150))
    layout.add(sections)
    
    return layout  # Done! 🎉
```

**Visual Result:**
```
┌───────────────────────────────────────────────┐
│                                               │
│                 Reversi42                     │ ← Title()
│                ↑ centered                     │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │  [Black: AI]      [White: AI]           │ │ ← Panel
│  │         [Start Game]                     │ │   85% wide
│  │          [Book: ON]                      │ │   centered!
│  └─────────────────────────────────────────┘ │
│                                               │
│         [Help]  [About]  [Quit]              │
│                                               │
└───────────────────────────────────────────────┘
```

### Main Menu Layout (Old Style)

**Before (Manual Positioning):**
```python
def _build_main_menu(self):
    # Title positioning
    title = Label("Reversi42", font_size=48)
    title_x = (self.width - title.rect.width) // 2
    title.set_position(title_x, 50)
    
    # Panel positioning
    panel = VBox(spacing=15)
    panel.background_color = (30, 50, 40)
    panel_x = (self.width - panel.rect.width) // 2
    panel_y = (self.height - panel.rect.height) // 2
    panel.set_position(panel_x, panel_y)
    
    # Button positioning inside panel
    players_row = HBox(spacing=30)
    # ... manual positioning for each button
    button_x = (panel_width - button_width) // 2
    # ... repeated 10+ times
```

**After (Declarative Layout):**
```python
def _build_main_menu(self):
    # Stack with auto-centering - SO CLEAN!
    layout = Stack(gap=40, align="center", justify="center")
    layout.set_size(self.width, self.height)
    
    # Title
    layout.add(Label("Reversi42", font_size=48, color=TITLE_COLOR))
    
    # Game controls panel
    panel = Stack(gap=15, align="center")
    panel.background_color = (30, 50, 40)
    panel.padding = 20
    
    # Player buttons
    players = HBox(spacing=30)
    players.add(Button("Black Player", width=280))
    players.add(Button("White Player", width=280))
    panel.add(players)
    
    panel.add(Button("Start Game", width=300))
    panel.add(Button("Book: ON", width=280))
    layout.add(panel)
    
    # Bottom buttons
    sections = HBox(spacing=30)
    sections.add(Button("Help", width=150))
    sections.add(Button("About", width=150))
    sections.add(Button("Quit", width=150))
    layout.add(sections)
    
    self.main_layout = layout
```

**Result:** 120 lines → 60 lines (-50% code reduction)

### Pause Menu Layout

```python
def _build_ui(self):
    # Panel with centered buttons
    panel = Stack(gap=20, align="center")
    panel.background_color = (0, 65, 50)
    panel.border_color = TITLE_COLOR
    panel.padding = 30
    
    # Title
    panel.add(Label("GAME PAUSED", font_size=56))
    
    # Buttons - ultra simple!
    for text, action, color in menu_items:
        btn = Button(text, width=300, on_click=lambda: do_action(action), color=color)
        panel.add(btn)
    
    # Center the panel on screen
    center = Center(width=self.width, height=self.height)
    center.add(panel)
    
    self.container = center
```

**Result:** 95 lines → 50 lines (-47% code reduction)

### Game Over Screen

```python
def _build_ui(self):
    # Centered vertical layout
    layout = Stack(gap=30, align="center", justify="center")
    layout.set_size(self.width, self.height)
    
    # Title and winner
    layout.add(Label("GAME OVER", font_size=72))
    layout.add(Label(f"{winner} WINS!", font_size=56, color=GOLD))
    
    # Scores
    layout.add(Label(f"Black: {black_score}", font_size=42))
    layout.add(Label(f"White: {white_score}", font_size=42))
    
    # Buttons
    buttons = HBox(spacing=40)
    buttons.add(Button("Menu", width=200))
    buttons.add(Button("Exit", width=200))
    layout.add(buttons)
    
    self.container = layout
```

**Result:** 140 lines → 70 lines (-50% code reduction)

### Complex Dashboard Layout

```python
def _build_dashboard(self):
    # Main container
    page = Stack(gap=20, align="center")
    page.set_size(self.width, self.height)
    
    # Header (full width)
    header = Row(gap=0)
    header.add(Col(span=12, child=Label("Dashboard")))
    page.add(header)
    
    # Main content (sidebar + content)
    content = Row(gap=20)
    content.add(Col(span=3, child=self._build_sidebar()))
    content.add(Col(span=9, child=self._build_content()))
    page.add(content)
    
    # Footer (3 equal columns)
    footer = Row(gap=10)
    footer.add(Col(span=4, child=Button("Stats")))
    footer.add(Col(span=4, child=Button("Settings")))
    footer.add(Col(span=4, child=Button("Help")))
    page.add(footer)
    
    return page
```

## Implementation Details

### Coordinate System

The layout system uses a two-level coordinate system:

1. **Relative Coordinates**: Widget position relative to parent
2. **Absolute Coordinates**: Widget position on screen

**Key Methods:**
- `set_position(x, y)`: Sets relative coordinates
- `get_absolute_rect()`: Computes absolute screen coordinates
- `render(surface)`: Uses absolute coordinates for drawing

**Example:**
```python
# Widget tree
screen (0, 0)
  └─ Stack (100, 50)
      └─ Button (20, 30)  # Relative to Stack

# Rendering
button.get_absolute_rect()  # Returns (120, 80) - absolute position
```

### Layout Algorithm

Layout calculation follows this pipeline:

1. **Add Phase**: Widget added to container
2. **Measure Phase**: Calculate widget sizes
3. **Layout Phase**: Calculate positions based on alignment
4. **Update Phase**: Update container size
5. **Render Phase**: Draw with absolute coordinates

**Stack Layout Algorithm:**
```python
def _layout(self):
    # 1. Calculate max width
    max_width = max(child.rect.width for child in self.children)
    
    # 2. Position children with alignment
    current_y = self.padding
    for child in self.children:
        if self.align == "center":
            child_x = self.padding + (max_width - child.rect.width) // 2
        # ... apply alignment
        
        child.set_position(child_x, current_y)
        current_y += child.rect.height + self.gap
    
    # 3. Apply justify (vertical distribution)
    if self.justify == "center":
        # Center all items vertically
        total_height = sum(child heights) + gaps
        offset = (container_height - total_height) // 2
        # ... adjust positions
    
    # 4. Update container size
    self.set_size(max_width + 2*padding, current_y - gap + padding)
```

### Event Propagation

Events propagate through the widget tree from top to bottom:

```python
def handle_event(self, event):
    if not self.enabled or not self.visible:
        return False
    
    # Propagate to children (reverse order for z-index)
    for child in reversed(self.children):
        if child.handle_event(event):
            return True  # Event consumed
    
    return False  # Event not handled
```

**Collision Detection:**
```python
def contains_point(self, x, y):
    # Use absolute rect for screen coordinates
    abs_rect = self.get_absolute_rect()
    return abs_rect.collidepoint(x, y)
```

## Best Practices

### 1. Use Title() for Titles

✅ **Do:**
```python
layout.add(Title("Game Menu"))  # Auto-centered!
```

❌ **Don't:**
```python
title = Label("Game Menu", font_size=48)
title_x = (width - title.rect.width) // 2
title.set_position(title_x, y)
```

### 2. Use center_in_parent for Single Widgets

✅ **Do:**
```python
panel = Stack()
panel.center_in_parent = True
main_layout.add(panel)  # Panel auto-centered!
```

❌ **Don't:**
```python
panel = Stack()
panel_x = (screen_width - panel.rect.width) // 2
panel.set_position(panel_x, y)
```

### 3. Combine Title() + center_in_parent for Clean Code

✅ **Do:**
```python
layout = Stack(gap=30, justify="center")
layout.add(Title("Welcome"))  # Title centered
panel = Panel()
panel.center_in_parent = True  # Panel centered
layout.add(panel)
```

### 4. Use Stack for New Layouts

✅ **Do:**
```python
menu = Stack(gap=20, align="center")
menu.add(title)
menu.add(button)
```

❌ **Don't:**
```python
menu = VBox(spacing=20)
# Manual centering
button_x = (menu_width - button_width) // 2
```

### 2. Use Center for Centering

✅ **Do:**
```python
center = Center(width=800, height=600)
center.add(panel)
```

❌ **Don't:**
```python
x = (800 - panel.rect.width) // 2
y = (600 - panel.rect.height) // 2
panel.set_position(x, y)
```

### 3. Use Row/Col for Multi-Column Layouts

✅ **Do:**
```python
row = Row(gap=20)
row.add(Col(span=6, child=left))
row.add(Col(span=6, child=right))
```

❌ **Don't:**
```python
hbox = HBox()
left = Panel(width=400)
right = Panel(width=400)
```

### 4. Compose Layouts Hierarchically

✅ **Do:**
```python
# Build from inside out
buttons = HBox(spacing=20)
buttons.add(Button("OK"))
buttons.add(Button("Cancel"))

panel = Stack(gap=15)
panel.add(Label("Confirm?"))
panel.add(buttons)

center = Center(width=800, height=600)
center.add(panel)
```

### 5. Use Spacer for Flexible Spacing

✅ **Do:**
```python
row = HBox()
row.add(Button("Left"))
row.add(Spacer(width=50))
row.add(Button("Right"))
```

## Performance Considerations

### Layout Recalculation

Layout is recalculated when:
- Widget is added to container
- Widget size changes
- Container is resized

**Optimization:** Batch widget additions before adding to container:

✅ **Efficient:**
```python
# Build completely, then add to parent
panel = Stack(gap=20)
for item in items:
    panel.add(Button(item))

main_layout.add(panel)  # Single layout recalc
```

❌ **Inefficient:**
```python
# Multiple reflows
main_layout.add(panel)
for item in items:
    panel.add(Button(item))  # Reflows for each add
```

### Rendering

Rendering is optimized with:
- Visibility checks (invisible widgets skip rendering)
- Absolute rect caching (computed once per frame)
- Dirty rectangles (future enhancement)

## Migration Guide

### From Manual to Declarative

**Step 1: Identify Layout Structure**
```python
# Manual code
title = Label("Menu")
title.set_position(300, 50)

button1 = Button("Start")
button1.set_position(280, 200)

button2 = Button("Quit")
button2.set_position(280, 260)
```

**Step 2: Group Related Widgets**
```python
# Vertical group: title, button1, button2
# All centered horizontally
```

**Step 3: Use Stack**
```python
menu = Stack(gap=20, align="center")
menu.add(Label("Menu"))
menu.add(Button("Start", width=300))
menu.add(Button("Quit", width=300))
```

**Step 4: Apply Centering**
```python
center = Center(width=800, height=600)
center.add(menu)
```

### Common Patterns

| Old Pattern | New Pattern |
|-------------|-------------|
| Manual x/y calculation | `Center()` |
| VBox + manual centering | `Stack(align="center")` |
| HBox + manual spacing | `HBox(spacing=N)` |
| Multiple columns | `Row() + Col()` |
| Fixed gaps | `Spacer()` |
| Section separators | `Divider()` |

## Testing

### Unit Tests

```python
def test_stack_centering():
    stack = Stack(gap=20, align="center")
    stack.set_size(800, 600)
    
    button = Button("Test", width=200, height=50)
    stack.add(button)
    
    # Button should be centered horizontally
    assert button.rect.x == (800 - 200) // 2
```

### Visual Testing

Run the game and verify:
1. All widgets are properly positioned
2. Centering works correctly
3. Responsive to window resize
4. No visual glitches

## Future Enhancements

### Planned Features

1. **Flex Layout**: Full flexbox implementation
2. **Grid Template Areas**: Named grid areas like CSS Grid
3. **Responsive Breakpoints**: Different layouts for different sizes
4. **Animations**: Smooth layout transitions
5. **Constraints**: Min/max width, aspect ratios
6. **Padding/Margin**: Individual control per side

### Example Future API

```python
# Flexbox-style
flex = Flex(direction="row", justify="space-between", align="center")

# Grid template areas
grid = Grid(template="""
    header header header
    sidebar content content
    footer footer footer
""")

# Responsive
layout = Responsive({
    "small": Stack(gap=10),
    "medium": Row(gap=20),
    "large": Grid(rows=2, cols=3)
})
```

## References

- [CSS Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Bootstrap Grid System](https://getbootstrap.com/docs/5.0/layout/grid/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- Widget System: `src/ui/widgets/`
- Layout Implementation: `src/ui/widgets/base/layout.py`

## API Quick Reference

### Widget (Base Class) - NEW Parameter!

```python
Widget(
    x: int = 0,
    y: int = 0,
    width: int = 0,
    height: int = 0,
    center_in_parent: bool = False  # ✨ NEW in 2025!
)
```

**New Parameter:**
- `center_in_parent`: If `True`, widget is automatically centered in its parent container

### Title() Helper - NEW!

```python
def Title(
    text: str,
    font_size: int = 48,
    color: Tuple[int, int, int] = (230, 240, 235)
) -> Label
```

**Returns:** Label with `center_in_parent=True` automatically set

**Example:**
```python
from ui.widgets.primitives import Title

layout = Stack()
layout.add(Title("Game Menu"))  # 1 line instead of 3!
```

### Stack (Enhanced VBox)

```python
Stack(
    gap: int = 0,
    align: str = "start",        # "start", "center", "end"
    justify: str = "start",      # "start", "center", "end", "space-between", "space-around"
    **kwargs
)
```

### Center (Auto-Centering Container)

```python
Center(
    width: int = 0,
    height: int = 0,
    horizontal: bool = True,
    vertical: bool = True
)
```

### Row / Col (Grid System)

```python
Row(gap: int = 10, align: str = "top", **kwargs)
Col(span: int = 12, child: Widget = None, **kwargs)  # span: 1-12
```

### HBox / VBox

```python
HBox(spacing: int = 5, align: str = "top", **kwargs)  # align: "top", "center", "bottom"
VBox(spacing: int = 5, align: str = "left", **kwargs)  # align: "left", "center", "right"
```

## Conclusion

The Bootstrap-like layout system with auto-centering represents a significant architectural improvement:

### Achievements

- **50-70% less code** in UI components
- **Zero manual positioning** calculations with `center_in_parent`
- **1-line titles** with `Title()` helper
- **Declarative, readable** layout definitions
- **Composable, reusable** primitives
- **Responsive by design**
- **Auto-centering** for widgets and panels

### Code Reduction Examples

| Component | Before | After | Reduction |
|-----------|--------|-------|-----------|
| Title centering | 3-4 lines | 1 line | -75% |
| Panel centering | 3 lines | 1 property | -66% |
| Menu layout | 120 LoC | 60 LoC | -50% |
| Pause menu | 95 LoC | 50 LoC | -47% |
| Game over | 140 LoC | 70 LoC | -50% |

### New in 2025

✅ **`center_in_parent` parameter** - Auto-center any widget  
✅ **`Title()` helper** - One-line centered titles  
✅ **VBox/HBox respect centering** - Containers honor widget preferences  
✅ **Ultra-clean code** - Even simpler than before!

This foundation enables rapid UI development and easy maintenance going forward.

