# Tournament Configuration System

## Overview

Reversi42 Tournament System now supports JSON-based configuration files, allowing you to define tournament settings once and run them repeatedly without manual configuration.

## Quick Start

```bash
# Run quick tournament
cd tournament
./run_quick_tournament.sh

# Run specific configuration
./run_tournament.sh speed_test.json

# List available configurations
./run_tournament.sh
```

## Configuration Files

Configuration files are stored in the `tournament/ring/` directory.

### File Structure

```json
{
  "name": "Tournament Name",
  "description": "Description of tournament purpose",
  "games_per_matchup": 2,
  "include_move_history": true,
  "players": [
    {
      "type": "AI",
      "name": "PlayerName",
      "difficulty": 6,
      "engine": "Minimax",
      "evaluator": "Standard"
    }
  ]
}
```

### Pre-Loaded Configurations

Four ready-to-use configurations are included:

1. **quick_tournament.json** - Comprehensive test of 8 AI players
2. **speed_test.json** - Performance benchmark with fast players
3. **evaluator_comparison.json** - Compare evaluation functions
4. **opening_book_test.json** - Test opening book effectiveness

## Usage Methods

### 1. Shell Scripts (Recommended)

```bash
# Quick tournament
./run_quick_tournament.sh

# Specific configuration
./run_tournament.sh quick_tournament.json
./run_tournament.sh evaluator_comparison.json
```

### 2. Python Direct

```bash
# Load and run configuration
python3 tournament.py --config ring/my_tournament.json

# Save interactive configuration
python3 tournament.py --save-config ring/my_tournament.json
```

### 3. Python API

```python
from tournament import Tournament

# Load from file
tournament = Tournament.from_config_file('ring/quick_tournament.json')
tournament.run()

# Create and save
tournament = Tournament(
    players_config=[...],
    games_per_matchup=3,
    name="My Tournament"
)
tournament.save_config('ring/my_tournament.json')
```

## Creating Custom Configurations

### Method 1: Manual JSON

Create `ring/custom.json`:

```json
{
  "name": "Custom Tournament",
  "description": "My custom configuration",
  "games_per_matchup": 3,
  "include_move_history": true,
  "players": [
    {"type": "AI", "name": "Player1", "difficulty": 6, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "AIBook", "name": "Player2", "difficulty": 6, "engine": "Minimax", "evaluator": "Standard"}
  ]
}
```

Run: `./run_tournament.sh custom.json`

### Method 2: Interactive Save

```bash
python3 tournament.py --save-config ring/custom.json
```

Follow prompts to configure, then the configuration is saved for reuse.

### Method 3: Programmatic

```python
from tournament import Tournament

# Create configuration
config = {
    'name': 'My Tournament',
    'description': 'Programmatically created',
    'games_per_matchup': 5,
    'include_move_history': True,
    'players': [
        {'type': 'AI', 'name': 'Player1', 'difficulty': 6, 
         'engine': 'Minimax', 'evaluator': 'Standard'},
        {'type': 'AI', 'name': 'Player2', 'difficulty': 8, 
         'engine': 'Minimax', 'evaluator': 'Advanced'}
    ]
}

# Save to file
import json
with open('ring/programmatic.json', 'w') as f:
    json.dump(config, f, indent=2)
```

## Player Types

### AI Types

- **`AI`** - Standard minimax with alpha-beta pruning
  - `difficulty`: 1-10 (search depth)
  - `evaluator`: Standard, Advanced, Simple, Greedy

- **`AIBook`** - AI with opening book support
  - Same parameters as AI
  - Uses 57 professional opening sequences

- **`Heuristic`** - Fast heuristic player
  - `difficulty`: 1 (not used)

- **`Greedy`** - Greedy player (max captures)
  - `difficulty`: 1 (not used)

- **`Monkey`** - Random player
  - `difficulty`: 1 (not used)

### Engine Types

- `Minimax` - Alpha-beta minimax search
- `Heuristic` - Heuristic evaluation
- `Random` - Random move selection

### Evaluator Types

- `Standard` - Balanced evaluation function
- `Advanced` - Enhanced positional evaluation
- `Simple` - Basic evaluation
- `Greedy` - Piece count focused

## Configuration Fields

### Tournament Settings

- **`name`** (string): Tournament display name
- **`description`** (string, optional): Tournament description
- **`games_per_matchup`** (integer): Games per player pair (each color)
- **`include_move_history`** (boolean): Include full game notation in report

### Player Configuration

Each player object:

- **`type`** (string): Player type (AI, AIBook, Heuristic, Greedy, Monkey)
- **`name`** (string): Unique display name
- **`difficulty`** (integer): Search depth for AI players (1-10)
- **`engine`** (string): Engine type (Minimax, Heuristic, Random)
- **`evaluator`** (string): Evaluation function (Standard, Advanced, Simple, Greedy)

## Examples

### Strong AI Battle

```json
{
  "name": "Strong AI Battle",
  "description": "High-level competition at depth 8",
  "games_per_matchup": 5,
  "include_move_history": true,
  "players": [
    {"type": "AI", "name": "Standard-8", "difficulty": 8, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "AI", "name": "Advanced-8", "difficulty": 8, "engine": "Minimax", "evaluator": "Advanced"},
    {"type": "AIBook", "name": "BookMaster-8", "difficulty": 8, "engine": "Minimax", "evaluator": "Standard"}
  ]
}
```

### Difficulty Ladder

```json
{
  "name": "Difficulty Ladder",
  "description": "Progressive difficulty levels",
  "games_per_matchup": 3,
  "include_move_history": false,
  "players": [
    {"type": "AI", "name": "Easy-3", "difficulty": 3, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "AI", "name": "Medium-5", "difficulty": 5, "engine": "Minimax", "evaluator": "Standard"},
    {"type": "AI", "name": "Hard-7", "difficulty": 7, "engine": "Minimax", "evaluator": "Standard"}
  ]
}
```

## Directory Structure

```
tournament/
├── tournament.py                # Main tournament system
├── quick_tournament.py          # Quick tournament runner
├── run_tournament.sh            # Configuration runner script ⭐
├── run_quick_tournament.sh      # Quick tournament script ⭐
└── ring/                        # Configuration directory ⭐
    ├── README.md                # Configuration guide
    ├── quick_tournament.json    # Pre-configured tournaments
    ├── speed_test.json
    ├── evaluator_comparison.json
    ├── opening_book_test.json
    └── (your custom configs)
```

## Benefits

1. **Reusability**: Define once, run multiple times
2. **Version Control**: Track tournament configurations in git
3. **Sharing**: Share configurations with other users
4. **Consistency**: Ensure identical setups across runs
5. **Documentation**: Configurations serve as documentation
6. **Automation**: Easy to integrate into CI/CD pipelines

## Best Practices

1. **Naming**: Use descriptive names for configurations
2. **Description**: Always include a description field
3. **Comments**: JSON doesn't support comments, use description field
4. **Organization**: Group similar tournaments in subdirectories if needed
5. **Validation**: Test configurations with small games_per_matchup first
6. **Backup**: Keep working configurations for reference

## Troubleshooting

### Configuration not found
```
ERROR: Configuration file not found: ring/my_tournament.json
```
- Check file exists in `ring/` directory
- Verify filename spelling
- Use `./run_tournament.sh` without arguments to list available configs

### Invalid JSON
```
ERROR: Invalid JSON in configuration file
```
- Validate JSON syntax (use online JSON validator)
- Check for missing commas, brackets
- Ensure all strings are quoted

### Player creation failed
```
ERROR: Failed to create player
```
- Verify player `type` is valid (AI, AIBook, Heuristic, Greedy, Monkey)
- Check `difficulty` is between 1-10
- Ensure `engine` and `evaluator` are valid

## Migration from Legacy

Old Python-based configuration:
```python
players_config = [
    ("AI", "Player-6", 6, "Minimax", "Standard"),
]
```

New JSON configuration:
```json
{
  "players": [
    {"type": "AI", "name": "Player-6", "difficulty": 6, 
     "engine": "Minimax", "evaluator": "Standard"}
  ]
}
```

Use `--save-config` to migrate existing tournaments to JSON format.

## See Also

- [ring/README.md](ring/README.md) - Detailed configuration guide
- [README.md](README.md) - Tournament system overview
- [TOURNAMENT_USAGE.txt](TOURNAMENT_USAGE.txt) - Usage guide

---

**Happy Tournament Configuration!** 🏆

