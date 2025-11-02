# WebGUI Guide

**Reversi42 Modern Web Interface - Play Through Your Browser**

Version: 5.0.0  
Last Updated: 2025-11-02

---

## Overview

Reversi42's WebGUI provides a modern, real-time browser-based interface for playing Reversi. Built with **FastAPI** and **WebSockets**, it offers instant updates and seamless gameplay.

## Quick Start

```bash
# Start the server
./reversi42

# Open browser
http://localhost:8000
```

That's it! 🎮

## Features

### Real-Time Gameplay
- ⚡ **WebSocket Communication** - Instant game state updates
- 🎯 **Interactive Board** - Click to play
- ✨ **Visual Feedback** - Highlights valid moves
- 📊 **Live Statistics** - Real-time score and analysis

### AI Opponents
- 🤖 **12 AI Gladiators** - Choose your opponent
- 👤 **Human Player** - Play as either color
- 🔄 **Switch Players** - Change opponents mid-game
- 💪 **Difficulty Levels** - From beginner to expert

### Game Management
- 💾 **Save/Load** - XOT format with auto-detect
- 📋 **Copy/Paste** - Quick game sharing
- ↩️ **Undo/Redo** - Fix mistakes
- 🔄 **Reset** - Start fresh anytime

### Analysis Tools
- 📚 **Opening Book** - See professional openings
- 🎯 **Move History** - Full game replay
- 📊 **AI Statistics** - Depth, nodes, evaluation
- 🌲 **Opening Tree** - Visual opening explorer

## Architecture

### Backend (FastAPI + Uvicorn)

```
src/webgui/
├── reversi42_server.py       # Main FastAPI server
├── backend_monitor.py      # Auto-restart monitor
├── start_server.sh         # Simple launcher
└── start_server_robust.sh  # Production launcher
```

**Key Features:**
- Async WebSocket handling
- Session management
- AI move processing
- Opening book integration
- Auto-restart on crash

### Frontend (HTML + JavaScript)

```
src/webgui/
└── game_websocket.html    # Complete web app (single file)
```

**Technologies:**
- Vanilla JavaScript (no frameworks)
- Tailwind CSS (via CDN)
- WebSocket for real-time updates
- XOT format parsing/generation

## How It Works

### Connection Flow

```
Browser → WebSocket → Backend Server → Game Engine
   ↑                                         |
   └─────────── Real-time Updates ──────────┘
```

### Message Types

**Client → Server:**
- `init` - Initialize session
- `set_players` - Configure players
- `human_move` - Player makes move
- `ai_move_request` - Request AI move
- `undo`, `redo` - History navigation
- `reset_game` - New game
- `load_history` - Load saved game

**Server → Client:**
- `board_update` - Complete game state
- `ai_thinking` - AI is calculating
- `ai_move` - AI made a move
- `game_over` - Game finished
- `error` - Error occurred

### Game State Synchronization

```javascript
// Frontend receives update
{
  "type": "board_update",
  "data": {
    "positions": [...],      // Board state
    "moves": ["C4", "e3"],   // Move history
    "valid_by_ply": [...],   // Valid moves
    "players": {...},        // Player info
    "status": {...}          // Game status
  }
}
```

## Configuration

### Server Options

```bash
# Default (port 8000, DIVZERO.EXE)
./reversi42

# Custom port
python3 -m src.webgui.server.reversi42_server --port 8001

# Custom AI
python3 -m src.webgui.server.reversi42_server --player "THE STRANGLER"
```

### Monitor Settings

```python
# backend_monitor.py
class BackendMonitor:
    def __init__(self):
        self.port = 8000
        self.max_restarts = 10
        self.restart_delay = 5  # seconds
        self.healthcheck_timeout = None  # No timeout (allow long AI thinking)
```

## File Format Support

### Save (XOT Format)

```javascript
// generateXOT()
function generateXOT() {
  // Creates complete XOT file with:
  // - Metadata (players, scores)
  // - Move history (compact notation)
  // - Board state (visual)
  return xotContent;
}
```

### Load (Auto-Detect)

```javascript
// Auto-detects XOT vs Compact
function detectFileFormat(content) {
  if (content.includes('[GAME]')) return 'xot';
  if (/^[A-Ha-h][1-8]+$/.test(content)) return 'compact';
  return 'unknown';
}
```

**Supported Formats:**
- `.xot` - XOT format (recommended)
- `.rev`, `.r42` - Compact format
- `.txt` - Auto-detected

## UI Components

### Main Board
- 8×8 grid with visual pieces
- Click interaction
- Move validation
- Last move indicator

### Player Panels
- Player names and avatars
- Score counters
- Turn indicators
- Player type (Human/AI)
- Change player buttons

### Control Toolbar
- Undo/Redo buttons
- Save/Load buttons
- Copy/Paste buttons
- Reset button
- AI Play/Pause toggle

### Side Panels
- **AI Analysis** - Real-time statistics
- **Move History** - Game replay
- **Opening Tree** - Book explorer
- **Developer Logs** - Debug panel

## Advanced Features

### Opening Book Integration

```javascript
// Visual opening moves
{
  "opening_by_ply": [
    {"move": "C4", "variants": 42},
    {"move": "E3", "variants": 28}
  ],
  "opening_tree": {
    "current_opening": "Perpendicular Opening",
    "children": [...]
  }
}
```

### AI Statistics Display

```javascript
// Real-time AI metrics
{
  "nodes_searched": 1250000,
  "pruning_ratio": 0.87,
  "depth": 9,
  "evaluation": +2.5,
  "last_search_time_ms": 1850
}
```

### Session Persistence

- Sessions survive disconnections
- Auto-reconnect on network issues
- State preserved during AI thinking
- Graceful error handling

## Deployment

### Development

```bash
# Simple startup
./reversi42

# Or manually
cd src/webgui
python3 -m uvicorn reversi42_server:app --host 0.0.0.0 --port 8000
```

### Production

```bash
# With monitor (auto-restart)
./reversi42

# Or manually
nohup python3 -m src.webgui.backend_monitor --port 8000 &
```

### Docker

```dockerfile
# Future: Docker deployment
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "-m", "src.webgui.backend_monitor"]
```

## Troubleshooting

### Server Won't Start

```bash
# Check if port is in use
lsof -i :8000

# Kill existing processes
pkill -f reversi42_server
pkill -f backend_monitor

# Restart
./reversi42
```

### Connection Issues

1. **Check server is running**
   ```bash
   tail -f /tmp/backend_detailed.log
   ```

2. **Verify URL**
   - Correct: `http://localhost:8000`
   - Not: `https://` or `127.0.0.1`

3. **Check firewall**
   - Allow port 8000
   - Disable VPN if blocking

4. **Try different browser**
   - Chrome, Firefox, Safari all supported

### WebSocket Errors

**Problem**: Connection drops during AI thinking

**Solution**: Already fixed in v5.0.0
- Monitor timeout disabled
- Sessions kept alive
- Auto-reconnect implemented

### Performance Issues

**Problem**: Slow AI response

**Cause**: Deep search with complex position

**Solutions:**
- Choose faster AI (BLITZ DEMON, ZEN MASTER)
- Use AI Play/Pause to control timing
- Monitor logs: `/tmp/backend_detailed.log`

## Browser Compatibility

### Supported Browsers

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Fully Supported |
| Firefox | 88+ | ✅ Fully Supported |
| Safari | 14+ | ✅ Fully Supported |
| Edge | 90+ | ✅ Fully Supported |

### Required Features
- WebSocket API
- ES6 JavaScript
- CSS Grid
- Fetch API

## Security

### Network Security
- No external connections
- Localhost by default
- CORS not required (same origin)

### Data Privacy
- No data collection
- No analytics
- No cookies
- Local storage only for settings

## Future Enhancements

Planned features for future versions:

- [ ] **Multiplayer** - Network play support
- [ ] **User Accounts** - Save progress
- [ ] **Game History** - Persistent storage
- [ ] **Analysis Mode** - Deep position analysis
- [ ] **Custom Themes** - UI customization
- [ ] **Mobile App** - Native mobile support
- [ ] **Spectator Mode** - Watch AI battles

## See Also

- [XOT Format Guide](XOT_FORMAT.md) - Save file format
- [Getting Started](user-guide/getting-started.md) - Installation
- [FAQ](user-guide/faq.md) - Common questions
- [Architecture](architecture/README.md) - Technical details

---

**Last Updated:** 2025-11-02  
**WebGUI Version:** 5.0.0

