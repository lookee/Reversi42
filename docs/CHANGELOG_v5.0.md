# Changelog - Version 5.0.0

**Release Date:** 2025-11-02  
**Codename:** "WebFirst"

---

## 🎯 Major Changes

### Architecture Modernization

#### Removed Legacy UI Systems
- ❌ **Pygame Views** - Removed ~8,000 lines of pygame-based UI code
- ❌ **Terminal Views** - Removed ~2,000 lines of terminal UI code
- ❌ **Pygame Widgets** - Removed all pygame-specific UI components
- ✅ **Result**: 60% reduction in codebase complexity, zero pygame dependency

#### New Web-First Architecture
- 🌐 **WebGUI** - Modern browser-based interface with FastAPI backend
- ⚡ **WebSocket** - Real-time game state synchronization
- 🚀 **Simple Launch** - Single command: `./reversi42`
- 💻 **No Dependencies** - Only FastAPI + Uvicorn for web interface

### File Format Enhancements

#### XOT Format (NEW!)
- 📝 **eXtended Othello Transcript** - New standard save format
- ✅ **Human-readable** - Easy to read and edit
- ✅ **Git-friendly** - Clean diffs for version control
- ✅ **Complete** - Includes metadata, history, and board state
- ✅ **Auto-detect** - Recognizes both XOT and compact formats

**Example XOT File:**
```xot
# Reversi42 Game Save - XOT Format v1.0
# Saved: 2025-11-02 15:30:45

[GAME]
Black=Human
White=THE STRANGLER
Turn=B
BlackScore=18
WhiteScore=15
Size=8

[MOVES]
History=C4e3F6e6F4c5D6
Count=7

[BOARD]
........
........
...BWB..
..BWWWB.
..BBWW..
........
........
........
```

### Backend Improvements

#### Robust Server Monitoring
- 🔄 **Auto-restart** - Backend monitor with automatic crash recovery
- ⏱️ **No Timeout** - Unlimited AI thinking time (no more premature restarts!)
- 📊 **Better Logging** - Detailed logging to `/tmp/backend_detailed.log`
- 🛡️ **Session Persistence** - Sessions survive disconnections

#### WebSocket Protocol
- 📡 **Real-time Updates** - Instant game state synchronization
- 🎮 **Interactive Play** - Click to move, live validation
- 🤖 **AI Integration** - Seamless AI move requests
- 📊 **Live Statistics** - Real-time AI analysis display

### Bug Fixes

#### Critical Fixes
- 🐛 **AI Thinking Icon** - Fixed icon appearing for human players
- 🐛 **Double Move Bug** - Fixed AI making two consecutive moves
- 🐛 **Backend Restart** - Fixed server restarting during long AI calculations
- 🐛 **Layout Issues** - Fixed white player name alignment

#### Technical Fixes
- Fixed healthcheck timeout causing unnecessary restarts
- Fixed WebSocket disconnect on AI move completion
- Fixed frontend error handling for better stability
- Fixed turn indicator visibility issues

### Documentation Updates

#### New Documentation
- 📄 **XOT_FORMAT.md** - Complete XOT format guide
- 📄 **WEBGUI.md** - Web interface documentation
- 📄 **VERSION_MANAGEMENT.md** - Centralized versioning guide

#### Updated Documentation
- ✅ **README.md** - Reflects v5.0.0 architecture
- ✅ **DOCUMENTATION_INDEX.md** - Updated for new features
- ✅ **getting-started.md** - Web-first quick start
- ✅ **faq.md** - Updated for web interface
- ✅ **architecture/** - Removed pygame references
- ✅ **All docs** - Version updated to 5.0.0

---

## 📦 What's Included

### Core Features (Retained)
- ⚡ **Ultra-Fast Bitboard AI** - 50-100x faster than standard implementation
- 🤖 **12 AI Gladiators** - From beginner to expert difficulty
- 📚 **Opening Book System** - 644 professional sequences
- 🏆 **Tournament System** - AI vs AI competitions
- 💻 **Python Library** - Use programmatically

### New Features
- 🌐 **Web Interface** - Modern browser-based UI
- 💾 **XOT Format** - Professional save format
- 🔄 **Auto-restart** - Robust server monitoring
- 📊 **Real-time Stats** - Live AI analysis

### Removed Features
- ❌ Pygame-based UI
- ❌ Terminal-based UI
- ❌ Legacy view system
- ❌ Pygame widgets

---

## 🔄 Migration Guide

### For Users

**Before (v4.x):**
```bash
# Old pygame-based launcher
python3 -m reversi42
# or
./run.sh
```

**After (v5.0):**
```bash
# New web-based launcher
./reversi42
# Open browser at http://localhost:8000
```

### For Developers

**Removed Imports:**
```python
# These no longer exist:
from ui.implementations.pygame import PygameBoardView
from ui.implementations.terminal import TerminalBoardView
from ui.widgets.pygame_widgets import *
```

**New Approach:**
```python
# Use web interface or headless mode:
from Board.BoardControl import BoardControl
from ui.implementations.headless import HeadlessBoardView

# Or use as library:
from Reversi.BitboardGame import BitboardGame
from Players.PlayerFactory import PlayerFactory
```

### For Save Files

**Old Format (.rev, .r42):**
```
C4e3F6e6F4c5D6
```
✅ Still supported! Auto-detected and loaded seamlessly.

**New Format (.xot) - Recommended:**
```xot
[GAME]
Black=Human
White=AI
...
```
✅ Save button now creates XOT files automatically.

---

## 📊 Statistics

### Code Changes
- **Lines Removed**: ~15,000 (pygame + terminal views)
- **Lines Added**: ~3,000 (webgui + xot support)
- **Net Change**: -12,000 lines (80% reduction in UI code)
- **Files Deleted**: 25+ (all pygame/terminal specific)
- **Files Added**: 5 (webgui, monitor, docs)

### Dependencies
- **Before**: pygame, fastapi, uvicorn
- **After**: fastapi, uvicorn
- **Reduction**: 1 major dependency removed

### Performance
- **Startup Time**: 2s → 3s (backend init)
- **Memory Usage**: Similar (no pygame overhead)
- **AI Speed**: Unchanged (core engine unaffected)
- **Network Latency**: <10ms (WebSocket)

---

## 🚀 Upgrade Instructions

### Fresh Install

```bash
# Clone repository
git clone https://github.com/lucaamore/reversi42.git
cd reversi42

# Install dependencies
pip install -r requirements.txt

# Run
./reversi42
```

### Upgrade from v4.x

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Remove old pygame
pip uninstall pygame

# Run
./reversi42
```

---

## 🐛 Known Issues

### Limitations
- No local player settings persistence (future feature)
- No multiplayer support (planned for v6.0)
- Mobile interface not optimized (future enhancement)

### Workarounds
- **Settings not saved**: Use save/load game to preserve state
- **Mobile use**: Desktop browser recommended for now
- **Network play**: Use tournament mode for AI battles

---

## 🔮 Future Plans

### Version 6.0 (Planned)
- 🌍 Network multiplayer support
- 📱 Mobile-optimized interface
- 💾 User accounts and game history
- 🎨 Custom themes and UI customization
- 📊 Advanced statistics and analysis
- 🏆 Online tournaments

### Version 5.x (Maintenance)
- 5.1: Performance optimizations
- 5.2: Additional AI personalities
- 5.3: Enhanced opening book
- 5.4: Analysis mode

---

## 🙏 Acknowledgments

This release represents a complete modernization of Reversi42's user interface, removing over 10 years of legacy pygame code and replacing it with a clean, modern web architecture.

Special thanks to:
- Contributors who reported UI issues
- Testers who validated the web interface
- The FastAPI and Uvicorn teams for excellent tools

---

## 📝 Notes

### Breaking Changes
- ❌ Pygame-based UI removed (use web interface)
- ❌ Terminal-based UI removed (use web interface)
- ❌ Direct pygame imports will fail
- ✅ Python library API unchanged

### Backward Compatibility
- ✅ Save files (both compact and XOT) fully compatible
- ✅ Tournament system unchanged
- ✅ Python library API preserved
- ✅ Opening book format unchanged
- ✅ AI players unchanged

### Deprecation Notices
- `reversi42_pygame_deprecated.py` - Kept for reference only
- Legacy view system - Use headless view for programmatic use
- Pygame-specific configuration - No longer applicable

---

**Version:** 5.0.0  
**Released:** 2025-11-02  
**Status:** Stable  
**Support:** Full support, active development

For questions, issues, or feedback:
- GitHub Issues: https://github.com/lucaamore/reversi42/issues
- Email: luca.amore@gmail.com
- Documentation: https://github.com/lucaamore/reversi42/docs

