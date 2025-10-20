# Data Flow

Detailed data flow diagrams and explanations for Reversi42.

## Overview

This document describes how data flows through Reversi42's architecture, from user input to system response. Understanding these flows is crucial for debugging, extending, and optimizing the system.

## Primary Data Flows

### 1. User Move Flow (Human Player)

Complete flow when a human player makes a move:

```
┌─────────────────┐
│   User Action   │  (Mouse click at position X,Y)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Pygame View   │  Detects click, converts to board position
└────────┬────────┘
         │ get_position_from_click(x, y) → position
         ▼
┌─────────────────┐
│  Human Player   │  Receives click notification
└────────┬────────┘
         │ Returns position
         ▼
┌─────────────────┐
│ Board Control   │  Validates move
└────────┬────────┘
         │ is_valid_move(position)
         ▼
┌─────────────────┐
│  Board Model    │  Checks with game engine
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ BitboardGame    │  Validates position
└────────┬────────┘
         │ Returns true/false
         │
         ▼ (if valid)
┌─────────────────┐
│  Board Model    │  Applies move
└────────┬────────┘
         │ make_move(position)
         ▼
┌─────────────────┐
│ BitboardGame    │  Creates new game state
└────────┬────────┘
         │ Returns new BitboardGame instance
         ▼
┌─────────────────┐
│  Board Model    │  Updates state
└────────┬────────┘
         │ Publishes move_made event
         ▼
┌─────────────────┐
│   Event Bus     │  Notifies all observers
└────────┬────────┘
         │ Broadcasts event to subscribers
         │
         ├───────────────┬──────────────────┐
         ▼               ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Pygame View  │  │ Statistics   │  │ Move History │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
  Re-renders       Updates stats      Records move
    board
```

**Timeline**:
1. **0ms**: User clicks
2. **1ms**: View processes click
3. **2ms**: Position validated
4. **3ms**: New game state created
5. **4ms**: Event published
6. **5-10ms**: Views updated

**Data Transformations**:
- `(x, y) → position` - Screen coordinates to board position
- `position → valid/invalid` - Validation
- `old_game → new_game` - Immutable state update
- `game_state → event` - State to event data

### 2. AI Move Flow

Complete flow when AI calculates and makes a move:

```
┌─────────────────┐
│  Turn Manager   │  AI player's turn
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Board Control   │  Requests AI move
└────────┬────────┘
         │ get_move(game, valid_moves)
         ▼
┌─────────────────┐
│  AI Player      │  Receives request
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│           Apocalyptron Engine               │
│                                             │
│  Step 1: Check Opening Book                 │
│  ┌──────────────────┐                       │
│  │  Opening Book    │                       │
│  └────────┬─────────┘                       │
│           │                                 │
│           ├─→ Found: Return book move       │
│           │                                 │
│           └─→ Not found: Continue to search │
│                                             │
│  Step 2: Iterative Deepening                │
│  ┌──────────────────┐                       │
│  │ For depth 1..N:  │                       │
│  │                  │                       │
│  │  ┌────────────┐  │                       │
│  │  │Alpha-Beta  │  │                       │
│  │  │  Search    │  │                       │
│  │  └─────┬──────┘  │                       │
│  │        │         │                       │
│  │        ▼         │                       │
│  │  ┌────────────┐  │                       │
│  │  │Check TT    │──┼─→ Cache hit: return   │
│  │  └─────┬──────┘  │                       │
│  │        │         │                       │
│  │        ▼         │                       │
│  │  ┌────────────┐  │                       │
│  │  │Order Moves │  │                       │
│  │  └─────┬──────┘  │                       │
│  │        │         │                       │
│  │        ▼         │                       │
│  │  ┌────────────┐  │                       │
│  │  │Try Pruning │  │                       │
│  │  └─────┬──────┘  │                       │
│  │        │         │                       │
│  │        ▼         │                       │
│  │  ┌────────────┐  │                       │
│  │  │ Evaluate   │  │                       │
│  │  │ Position   │  │                       │
│  │  └─────┬──────┘  │                       │
│  │        │         │                       │
│  │        ▼         │                       │
│  │  ┌────────────┐  │                       │
│  │  │Store in TT │  │                       │
│  │  └─────┬──────┘  │                       │
│  │        │         │                       │
│  │        ▼         │                       │
│  │   Return best   │                        │
│  │                  │                       │
│  └──────────────────┘                       │
│                                             │
│  Step 3: Return Best Move                   │
│  ┌──────────────────┐                       │
│  │  Best Move       │                       │
│  └────────┬─────────┘                       │
└───────────┼─────────────────────────────────┘
            │
            ▼
┌─────────────────┐
│  AI Player      │  Returns selected move
└────────┬────────┘
         │ position
         ▼
[Continue with same flow as user move from here]
```

**Timeline** (depth 9):
1. **0ms**: AI turn starts
2. **1ms**: Opening book check (instant if found)
3. **2-2000ms**: Search (if not in book)
   - Depth 1: 1ms
   - Depth 3: 10ms
   - Depth 6: 100ms
   - Depth 9: 1000ms
4. **2001ms**: Move returned
5. **2002-2010ms**: Move applied and views updated

**Data Transformations**:
- `game_state → opening_moves[]` - Book lookup
- `game_state → evaluation_score` - Position evaluation
- `(game, depth, α, β) → (score, move)` - Search result
- `search_result → position` - Best move extraction

### 3. Game Initialization Flow

How a new game is created and initialized:

```
┌─────────────────┐
│ Main Menu       │  User clicks "Start Game"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Main Window    │  Collects configuration
└────────┬────────┘
         │ {
         │   black: PlayerType,
         │   white: PlayerType,
         │   show_opening: bool,
         │   ...
         │ }
         ▼
┌─────────────────┐
│ Player Factory  │  Creates players
└────────┬────────┘
         │ create_player(config)
         ├──────────────┬─────────────┐
         ▼              ▼             ▼
┌──────────────┐  ┌──────────┐  ┌──────────┐
│ Human Player │  │ AI Player│  │Opening   │
│              │  │          │  │Book Load │
└──────┬───────┘  └────┬─────┘  └────┬─────┘
       │               │              │
       └───────┬───────┴──────────────┘
               │
               ▼
┌─────────────────┐
│ Board Control   │  Initialize game
└────────┬────────┘
         │ create_game()
         ▼
┌─────────────────┐
│  Board Model    │  Create initial state
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ BitboardGame    │  Initial position
└────────┬────────┘
         │ black: 0x0000000810000000
         │ white: 0x0000001008000000
         │ current: BLACK
         ▼
┌─────────────────┐
│ View Factory    │  Create view
└────────┬────────┘
         │ create_view(type)
         ▼
┌─────────────────┐
│  Pygame View    │  Initialize UI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Event Bus     │  Setup observers
└────────┬────────┘
         │ Subscribe all components
         ▼
┌─────────────────┐
│  Game Loop      │  Start main loop
└─────────────────┘
```

**Data Created**:
- Player objects with configurations
- Initial game state (bitboards)
- View with rendering context
- Event bus with subscribers
- Opening book data (if enabled)

### 4. Save Game Flow

How game state is persisted:

```
┌─────────────────┐
│  User Input     │  Press ESC → Save Game
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pygame View    │  Show save dialog
└────────┬────────┘
         │ User enters filename
         ▼
┌─────────────────┐
│ Board Control   │  save_game(filename)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Board Model    │  get_game_state()
└────────┬────────┘
         │ {
         │   game: BitboardGame,
         │   history: Move[],
         │   metadata: {...}
         │ }
         ▼
┌─────────────────┐
│   Game I/O      │  Serialize to XOT format
└────────┬────────┘
         │ format_as_xot(state)
         │
         │ XOT Format:
         │ ┌────────────────────────┐
         │ │ [Game Info]            │
         │ │ Date: 2025-10-20       │
         │ │ Black: Human           │
         │ │ White: Apocalyptron-9  │
         │ │                        │
         │ │ [Moves]                │
         │ │ 1. F5 D6               │
         │ │ 2. C5 F4               │
         │ │ ...                    │
         │ └────────────────────────┘
         ▼
┌─────────────────┐
│  File System    │  Write to saves/
└────────┬────────┘
         │ saves/game_YYYYMMDD_HHMMSS.xot
         ▼
┌─────────────────┐
│  Confirmation   │  Show success message
└─────────────────┘
```

**Data Transformations**:
- `game_state → XOT_text` - Serialization
- `moves[] → algebraic_notation` - Move formatting
- `metadata → header` - Game info formatting

### 5. Load Game Flow

How saved games are restored:

```
┌─────────────────┐
│  User Input     │  Press ESC → Load Game
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pygame View    │  Show file browser
└────────┬────────┘
         │ User selects file
         ▼
┌─────────────────┐
│ Board Control   │  load_game(filename)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Game I/O      │  Read file
└────────┬────────┘
         │ read(saves/game.xot)
         ▼
┌─────────────────┐
│   Parser        │  Parse XOT format
└────────┬────────┘
         │ parse_xot(text)
         │
         │ Extracted:
         │ {
         │   metadata: {...},
         │   moves: [F5, D6, ...],
         │   black_player: "Human",
         │   white_player: "Apocalyptron-9"
         │ }
         ▼
┌─────────────────┐
│ Game Recreator  │  Replay moves
└────────┬────────┘
         │ game = BitboardGame()
         │ for move in moves:
         │     game = game.make_move(move)
         ▼
┌─────────────────┐
│  Board Model    │  Set state
└────────┬────────┘
         │ set_game(game)
         ▼
┌─────────────────┐
│   Event Bus     │  Publish game_loaded
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  All Views      │  Update to show loaded game
└─────────────────┘
```

**Data Transformations**:
- `XOT_text → game_state` - Deserialization
- `algebraic_notation → positions` - Move parsing
- `positions → game_state` - State reconstruction

### 6. Tournament Flow

How tournaments are executed:

```
┌─────────────────┐
│  Tournament     │  Load config.json
│  Launcher       │
└────────┬────────┘
         │ {
         │   players: [...],
         │   rounds: N,
         │   ...
         │ }
         ▼
┌─────────────────┐
│  Tournament     │  Generate matchups
│  Manager        │
└────────┬────────┘
         │ Round-robin pairings
         │
         ▼
┌────────────────────────────────┐
│  For each matchup:             │
│                                │
│  ┌────────────────┐            │
│  │ Create Game    │            │
│  └────────┬───────┘            │
│           │                    │
│           ▼                    │
│  ┌────────────────┐            │
│  │ Play Game      │            │
│  │ (Headless)     │            │
│  └────────┬───────┘            │
│           │                    │
│           ▼                    │
│  ┌────────────────┐            │
│  │ Record Result  │            │
│  └────────┬───────┘            │
│           │                    │
└───────────┼────────────────────┘
            │
            ▼
┌─────────────────┐
│  Statistics     │  Aggregate results
│  Aggregator     │
└────────┬────────┘
         │ {
         │   wins: {...},
         │   scores: {...},
         │   timings: {...}
         │ }
         ▼
┌─────────────────┐
│  Report         │  Generate report
│  Generator      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  File Output    │  Save to reports/
└─────────────────┘
```

**Parallelization**:
- Multiple games can run concurrently
- Headless mode = zero rendering overhead
- Limited by CPU cores and memory

## Event Flow

### Event Bus Pattern

```
┌──────────────┐
│  Publishers  │
└──────┬───────┘
       │ publish(event_type, data)
       ▼
┌──────────────┐
│  Event Bus   │  Central hub
└──────┬───────┘
       │ notify_subscribers(event_type, data)
       │
       ├─────────┬─────────┬─────────┐
       ▼         ▼         ▼         ▼
   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
   │Sub 1 │ │Sub 2 │ │Sub 3 │ │Sub N │
   └──────┘ └──────┘ └──────┘ └──────┘
```

**Event Types**:

| Event | Data | Subscribers |
|-------|------|-------------|
| `game_started` | game_state | Views, Statistics |
| `move_made` | position, player | Views, History, Stats |
| `turn_changed` | new_player | Views, AI Manager |
| `game_ended` | winner, scores | Views, Statistics, Tournament |
| `ai_thinking` | depth, nodes | Views (show progress) |
| `opening_used` | name, moves | Views, Statistics |

### Event Timing

**Synchronous Events** (immediate):
- `move_made` - Must update views immediately
- `game_ended` - Must show results immediately

**Asynchronous Events** (queued):
- `ai_thinking` - Can update UI when convenient
- `statistics_updated` - Low priority

## Data Structures

### Core Data Structures

#### BitboardGame
```python
class BitboardGame:
    black: int              # 64-bit bitboard
    white: int              # 64-bit bitboard
    current_player: int     # 1 or -1
    move_history: List[int] # Position history
```
**Size**: ~200 bytes  
**Immutable**: Yes  
**Thread-safe**: Yes

#### Game State
```python
@dataclass
class GameState:
    game: BitboardGame
    black_player: Player
    white_player: Player
    opening_book_enabled: bool
    move_count: int
    start_time: float
```

#### Search Result
```python
@dataclass
class SearchResult:
    best_move: int
    score: float
    depth: int
    nodes_searched: int
    time_elapsed: float
    pv_line: List[int]  # Principal variation
```

### Data Transformations

#### Position Representations

```
Screen Coordinates (x, y)
         ↓ [View]
Board Position (0-63)
         ↓ [Game]
Bitboard (bit position)
         ↓ [Engine]
Algebraic Notation (D3, E4, ...)
```

#### State Representations

```
BitboardGame (2 x 64-bit int)
         ↓ [Serialization]
XOT Text (human-readable)
         ↓ [File I/O]
Disk Storage (text file)
```

## Performance Considerations

### Hot Paths

1. **Move Generation** - Called millions of times
   - Must be O(1)
   - Pure bitwise operations
   - No allocations

2. **Position Evaluation** - Called per search node
   - Cached via transposition table
   - Efficient heuristics
   - Early termination

3. **View Rendering** - 60 FPS target
   - Dirty rectangle optimization
   - Sprite caching
   - Event batching

### Data Flow Optimization

- **Immutable State**: Zero-cost copies (just pointers)
- **Event Batching**: Group multiple events
- **Lazy Evaluation**: Compute only when needed
- **Caching**: Transposition table, opening book

## Error Handling in Data Flow

### Validation Points

1. **Input Boundary**: User input validated immediately
2. **Domain Boundary**: Game rules enforced
3. **Persistence Boundary**: File format validated
4. **API Boundary**: Type checking, range validation

### Error Propagation

```
Error Occurs
    ↓
Exception Raised
    ↓
Caught at Appropriate Level
    ↓
Logged
    ↓
User Notified (if applicable)
    ↓
Graceful Recovery or Termination
```

## Related Documentation

- [System Overview](system-overview.md) - Architecture overview
- [Design Principles](design-principles.md) - Design guidelines
- [Performance Guide](../development/performance.md) - Optimization
- [API Reference](../api/README.md) - API details

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-20

*For questions about data flow, see [Architecture Guide](README.md).*

