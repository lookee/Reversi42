# Reversi42 GuiWeb - JSON Schema Complete

**Version:** 1.0.0  
**Purpose:** Schema completo per alimentare tutte le componenti GUI  
**Format:** JSON (TypeScript-style documentation)

---

## 🎯 Schema Overview

Il JSON è l'**unico punto di verità** per la GUI. Modificando il JSON, tutta la GUI si aggiorna automaticamente.

---

## 📋 Complete JSON Schema

```typescript
interface Reversi42GameData {
  // Meta informazioni
  version: string;                    // "1.0.0"
  meta: MetaInfo;
  
  // Giocatori
  players: Players;
  
  // Stato del gioco
  game_state: GameState;
  
  // Status e timing
  status: Status;
  
  // Posizioni board per ogni ply
  positions: string[];                // Array di 64-char strings
  
  // Mosse giocate
  moves: string[];                    // ["C4", "E3", "F5", ...]
  
  // Dettagli delle mosse
  move_details: MoveDetail[];
  
  // Mosse valide per ogni ply
  valid_by_ply: string[][];          // [["C4","D3"], ["E3","C3"], ...]
  
  // Suggerimenti opening per ogni ply
  opening_by_ply: OpeningSuggestion[][];
  
  // Statistiche AI per ogni ply
  ai_stats_by_ply: (AIStats | null)[];
  
  // Informazioni torneo (opzionale)
  tournament?: TournamentInfo;
  
  // Annotazioni (opzionale)
  annotations?: Annotation[];
  
  // Impostazioni UI
  ui_settings: UISettings;
}

// ============================================================================
// SUB-SCHEMAS
// ============================================================================

interface MetaInfo {
  variant: string;                    // "Reversi/Othello"
  size: number;                       // 8
  theme: string;                      // "green-elegant-light"
  timestamp: string;                  // ISO 8601
  game_id: string;                    // "match-001"
}

interface Players {
  black: PlayerInfo;
  white: PlayerInfo;
}

interface PlayerInfo {
  name: string;                       // "Luca Amore"
  avatar: string;                     // "LA" (2 char)
  type: "human" | "ai";              // Player type
  rating?: number;                    // ELO rating
  config?: PlayerConfig | null;       // AI configuration
}

interface PlayerConfig {
  engine: string;                     // "Apocalyptron"
  depth: number;                      // 9
  search_strategy?: string;           // "iterative_deepening"
  show_book_options?: boolean;
  book_instant?: boolean;
  time_limit_ms?: number;             // Time limit
  [key: string]: any;                 // Extra config
}

interface GameState {
  current_ply: number;                // 0-based ply index
  max_ply: number;                    // Total plies in game
  current_move: number;               // 1-based move number
  game_over: boolean;
  winner: "black" | "white" | "draw" | null;
  final_score: {
    black: number;
    white: number;
  } | null;
}

interface Status {
  round?: number;                     // Tournament round
  board_no?: number;                  // Board number
  turn_by_ply: string[];             // ["B", "W", "B", "W", ...]
  match_time_start: number;           // Timestamp
  clock: ClockInfo;
}

interface ClockInfo {
  match_ms: number;                   // Total match time
  black_ms: number;                   // Black total time
  white_ms: number;                   // White total time
  black_partial_ms?: number;          // Black time for current move
  white_partial_ms?: number;          // White time for current move
  byoyomi_s?: number;                 // Byoyomi seconds
  inc_ms?: number;                    // Increment per move
}

interface MoveDetail {
  ply: number;                        // 1-based ply number
  move: string;                       // "C4"
  player: "black" | "white";
  pieces_flipped: number;             // Count
  time_ms: number;                    // Time taken
  value?: number;                     // Engine evaluation
  is_book_move: boolean;
  opening_name?: string | null;
}

interface OpeningSuggestion {
  move: string;                       // "C4"
  score: string;                      // "99+", "88", etc.
  line: string;                       // "C4 c3 D3 c5 B3 f4"
  opening_name?: string;              // "Diagonal Opening"
  advantage?: string;                 // "=", "w", "w+", "b", etc.
  continuations?: number;             // Number of book continuations
  tags: string[];                     // ["book", "classic"]
}

interface AIStats {
  engine: string;                     // "Apocalyptron"
  version?: string;                   // "4.1.16"
  depth: number;                      // Final depth reached
  nodes: number;                      // Total nodes searched
  
  // Pruning statistics
  alpha_beta_pruned?: number;
  alpha_beta_pct?: number;
  lmr_reductions?: number;
  lmr_researches?: number;
  lmr_research_pct?: number;
  futility_cut?: number;
  null_move_cutoffs?: number;
  null_move_trials?: number;
  null_move_success_pct?: number;
  
  // Other stats
  history_entries?: number;
  aspiration_hits?: number;
  aspiration_fails?: number;
  transposition_hits?: number;
  
  // Results
  time_ms: number;                    // Time in milliseconds
  nps: number;                        // Nodes per second
  selected_move: string;              // "E3"
  selected_value: number;             // Evaluation score
  pv_line?: string[];                 // Principal variation
  book_moves_prioritized?: string[];  // Book moves evaluated
}

interface TournamentInfo {
  name: string;                       // "Blitz Madness Championship"
  round: number;
  board: number;
  format: string;                     // "best-of-3"
  time_control: string;               // "5+2"
  verbose: boolean;
}

interface Annotation {
  ply: number;
  type: "opening" | "excellent" | "good" | "inaccuracy" | "mistake" | "blunder";
  text: string;
  suggested_move?: string;
}

interface UISettings {
  show_valid_moves: boolean;
  show_opening_hints: boolean;
  show_coordinates: boolean;
  show_hoshi: boolean;
  animation_speed: "slow" | "normal" | "fast" | "instant";
  sound_enabled: boolean;
  show_ai_thinking: boolean;
  auto_advance: boolean;
  highlight_last_move: boolean;
}
```

---

## 📄 Complete Example JSON

```json
{
  "version": "1.0.0",
  "meta": {
    "variant": "Reversi/Othello",
    "size": 8,
    "theme": "green-elegant-light",
    "timestamp": "2025-10-21T15:30:00Z",
    "game_id": "match-blitz-001"
  },
  
  "players": {
    "black": {
      "name": "Luca Amore",
      "avatar": "LA",
      "type": "human",
      "rating": 1850,
      "config": null
    },
    "white": {
      "name": "Apocalyptron",
      "avatar": "AP",
      "type": "ai",
      "rating": 2400,
      "config": {
        "engine": "Apocalyptron",
        "depth": 9,
        "search_strategy": "iterative_deepening",
        "show_book_options": false,
        "book_instant": false
      }
    }
  },
  
  "game_state": {
    "current_ply": 5,
    "max_ply": 5,
    "current_move": 3,
    "game_over": false,
    "winner": null,
    "final_score": null
  },
  
  "status": {
    "round": 1,
    "board_no": 1,
    "turn_by_ply": ["B", "W", "B", "W", "B", "W"],
    "match_time_start": 1729517400000,
    "clock": {
      "match_ms": 45230,
      "black_ms": 12340,
      "white_ms": 32890,
      "black_partial_ms": 1200,
      "white_partial_ms": 0,
      "byoyomi_s": 30,
      "inc_ms": 2000
    }
  },
  
  "positions": [
    "...........................WB......BW...........................",
    "..........................BBB......BW...........................",
    "....................W.....BBW......BW...........................",
    "....................W.....BBW......BBB..........................",
    "..................W.W.....BBW......BBB..........................",
    "..................W.W.....BBBBBBBBBBB.........................."
  ],
  
  "moves": ["C4", "E3", "F5", "D3", "E6"],
  
  "move_details": [
    {
      "ply": 1,
      "move": "C4",
      "player": "black",
      "pieces_flipped": 1,
      "time_ms": 234,
      "value": 0,
      "is_book_move": true,
      "opening_name": "Diagonal Opening"
    },
    {
      "ply": 2,
      "move": "E3",
      "player": "white",
      "pieces_flipped": 2,
      "time_ms": 1850,
      "value": -10,
      "is_book_move": true,
      "opening_name": "Diagonal - Perpendicular"
    },
    {
      "ply": 3,
      "move": "F5",
      "player": "black",
      "pieces_flipped": 1,
      "time_ms": 145,
      "value": 20,
      "is_book_move": false,
      "opening_name": null
    },
    {
      "ply": 4,
      "move": "D3",
      "player": "white",
      "pieces_flipped": 3,
      "time_ms": 2145,
      "value": -15,
      "is_book_move": false,
      "opening_name": null
    },
    {
      "ply": 5,
      "move": "E6",
      "player": "black",
      "pieces_flipped": 5,
      "time_ms": 198,
      "value": 35,
      "is_book_move": false,
      "opening_name": null
    }
  ],
  
  "valid_by_ply": [
    ["C4", "D3", "E6", "F5"],
    ["C3", "C5", "E3"],
    ["F2", "F3", "F4", "F5", "F6"],
    ["B4", "C5", "C6", "E6", "G6"],
    ["C5", "D6", "E6", "F4", "G5"],
    ["C3", "C5", "D2", "E2", "F2"]
  ],
  
  "opening_by_ply": [
    [
      {
        "move": "C4",
        "score": "99+",
        "line": "C4 c3 D3 c5 B3 f4",
        "opening_name": "Diagonal Opening",
        "advantage": "=",
        "continuations": 586,
        "tags": ["book", "classic", "balanced"]
      },
      {
        "move": "E6",
        "score": "72",
        "line": "E6 f4 D3 c4 C3 d2",
        "opening_name": "Perpendicular",
        "advantage": "w",
        "continuations": 24,
        "tags": ["book", "sharp"]
      }
    ],
    [
      {
        "move": "E3",
        "score": "88+",
        "line": "E3 f4 F5 c5 D3",
        "opening_name": "Diagonal - Perpendicular",
        "advantage": "=",
        "continuations": 142,
        "tags": ["book", "main-line"]
      },
      {
        "move": "C3",
        "score": "65",
        "line": "C3 d3 C5 b4",
        "opening_name": "Parallel Opening",
        "advantage": "b",
        "continuations": 18,
        "tags": ["book", "aggressive"]
      }
    ],
    [],
    [],
    [],
    []
  ],
  
  "ai_stats_by_ply": [
    null,
    {
      "engine": "Apocalyptron",
      "version": "4.1.16",
      "depth": 8,
      "nodes": 6825,
      "alpha_beta_pruned": 1729,
      "alpha_beta_pct": 25.3,
      "lmr_reductions": 253,
      "lmr_researches": 46,
      "lmr_research_pct": 18.2,
      "futility_cut": 1,
      "null_move_cutoffs": 63,
      "null_move_trials": 144,
      "null_move_success_pct": 43.8,
      "history_entries": 50,
      "aspiration_hits": 12,
      "aspiration_fails": 0,
      "transposition_hits": 234,
      "time_ms": 823,
      "nps": 8291,
      "selected_move": "E3",
      "selected_value": -10,
      "pv_line": ["E3", "F4", "F5", "D6", "C5"],
      "book_moves_prioritized": ["E3", "C3"]
    },
    null,
    {
      "engine": "Apocalyptron",
      "depth": 9,
      "nodes": 15234,
      "alpha_beta_pruned": 4521,
      "alpha_beta_pct": 29.7,
      "lmr_reductions": 412,
      "lmr_researches": 87,
      "lmr_research_pct": 21.1,
      "futility_cut": 8,
      "null_move_cutoffs": 142,
      "null_move_trials": 298,
      "null_move_success_pct": 47.7,
      "history_entries": 68,
      "time_ms": 1456,
      "nps": 10465,
      "selected_move": "D3",
      "selected_value": -15,
      "pv_line": ["D3", "C5", "D6", "E6"]
    },
    null,
    {
      "engine": "Apocalyptron",
      "depth": 10,
      "nodes": 28456,
      "time_ms": 2341,
      "nps": 12154,
      "selected_move": "E6",
      "selected_value": 35
    }
  ],
  
  "tournament": {
    "name": "Blitz Madness Championship 2025",
    "round": 1,
    "board": 1,
    "format": "best-of-3",
    "time_control": "5+2",
    "verbose": true
  },
  
  "annotations": [
    {
      "ply": 1,
      "type": "opening",
      "text": "Standard Diagonal Opening. Balanced position favoring neither player."
    },
    {
      "ply": 2,
      "type": "excellent",
      "text": "Strong book response. Maintains equality."
    },
    {
      "ply": 3,
      "type": "good",
      "text": "Out of book but solid positional move."
    },
    {
      "ply": 4,
      "type": "inaccuracy",
      "text": "Slightly passive. F4 might be stronger.",
      "suggested_move": "F4"
    }
  ],
  
  "ui_settings": {
    "show_valid_moves": true,
    "show_opening_hints": true,
    "show_coordinates": true,
    "show_hoshi": true,
    "animation_speed": "normal",
    "sound_enabled": false,
    "show_ai_thinking": true,
    "auto_advance": false,
    "highlight_last_move": true
  }
}
```

---

## 📊 Field Descriptions

### `positions` Format

**String di 64 caratteri** che rappresenta la board:

```
Position 0:  "...........................WB......BW..........................."
              ^row 0, col 0 (A1)
                                       ^row 3, col 3 (D4) = W
                                        ^row 3, col 4 (E4) = B
              
Mapping:
- '.' or ' ' = Empty
- 'B' or 'X' = Black piece
- 'W' or 'O' = White piece

Index = row * 8 + col
A1 = 0*8 + 0 = 0
D4 = 3*8 + 3 = 27
E4 = 3*8 + 4 = 28
```

### `turn_by_ply` Format

Array che indica chi muove ad ogni ply:

```json
["B", "W", "B", "W", "B", "W"]
 ^ply0 ^ply1 ^ply2 ^ply3 ^ply4 ^ply5
```

### `ai_stats_by_ply` Format

Array parallelo alle posizioni. `null` per mosse umane, oggetto per mosse AI:

```json
[
  null,        // ply 0 (initial)
  {...},       // ply 1 (AI move)
  null,        // ply 2 (human move)
  {...},       // ply 3 (AI move)
]
```

---

## 🔄 Data Flow

```
JSON Modified
    ↓
JavaScript detects change
    ↓
Parse & validate
    ↓
Update global gameData
    ↓
Call render()
    ↓
GUI updates automatically
```

---

## 🎨 UI Component Mapping

| JSON Field | UI Component |
|------------|-------------|
| `players.black.name` | Header left player name |
| `players.white.name` | Header right player name |
| `positions[ply]` | Board grid |
| `valid_by_ply[ply]` | Valid move indicators |
| `opening_by_ply[ply]` | Opening suggestions panel |
| `ai_stats_by_ply[ply]` | AI stats panel |
| `status.clock.*` | Clock displays |
| `moves` | Move history list |
| `annotations` | Move annotations |
| `ui_settings.*` | UI behavior |

---

## ✅ Validation Rules

### Required Fields

- `meta.size` must be 8
- `positions` must be array of 64-char strings
- `moves.length` must equal `positions.length - 1`
- `turn_by_ply.length` must equal `positions.length`
- `valid_by_ply.length` must equal `positions.length`

### Data Consistency

- Each position must have 64 characters
- `current_ply` must be <= `max_ply`
- `max_ply` must equal `positions.length - 1`
- Player types must be "human" or "ai"
- AI players must have `config`

---

## 🚀 Usage Examples

### Example 1: Initial Game

```json
{
  "version": "1.0.0",
  "meta": {"variant": "Reversi/Othello", "size": 8},
  "players": {
    "black": {"name": "Player 1", "avatar": "P1", "type": "human"},
    "white": {"name": "Player 2", "avatar": "P2", "type": "human"}
  },
  "game_state": {"current_ply": 0, "max_ply": 0, "game_over": false},
  "positions": ["...........................WB......BW..........................."],
  "moves": [],
  "valid_by_ply": [["C4","D3","E6","F5"]],
  "opening_by_ply": [[]],
  "ai_stats_by_ply": [null]
}
```

### Example 2: AI vs AI Game

```json
{
  "players": {
    "black": {
      "name": "Apocalyptron",
      "type": "ai",
      "config": {"engine": "Apocalyptron", "depth": 9}
    },
    "white": {
      "name": "DivZero",
      "type": "ai",
      "config": {"engine": "DivZero", "depth": 12}
    }
  }
}
```

### Example 3: Tournament Game

```json
{
  "tournament": {
    "name": "World Championship 2025",
    "round": 3,
    "board": 12,
    "format": "best-of-5",
    "time_control": "10+5",
    "verbose": true
  }
}
```

---

**Schema completo e pronto all'uso!** 📋✨



