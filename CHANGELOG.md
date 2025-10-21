# Changelog

All notable changes to Reversi42 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **EnhancedOpeningBook - Advanced Opening Book System** 📚✨
  - **NEW CLASS**: `EnhancedOpeningBook` extends `OpeningBook` (100% retrocompatibile)
  - **Parametric Filtering**: Configurable score thresholds (default: only moves > 0)
  - **Multi-Criteria Scoring**: advantage + variety + safety bonus
  - **Selection Modes**: BEST_SCORE, WEIGHTED_RANDOM, VARIETY_FIRST, SAFE_FIRST, AGGRESSIVE
  - **Detailed Evaluation**: `MoveEvaluation` dataclass with complete move analysis
  - **Dynamic Thresholds**: Use average score as threshold (adaptive filtering)
  - **NOT USED** by any existing players (backward compatibility guaranteed!)
  - Files: `src/domain/knowledge/enhanced_opening_book.py`
  - Docs: `src/domain/knowledge/ENHANCED_OPENING_BOOK.md`
  - Tests: `tests/domain/test_enhanced_opening_book.py` (13 tests, all pass)

- **Unicode Board Representation (Default)** 🎨
  - New methods: `Game.get_unicode_view()`, `BitboardGame.get_unicode_view()`
  - **○ = Nero**, **◉ = Bianco**, **· = Vuoto**
  - Compact and elegant (10 lines vs 17)
  - Now DEFAULT for `game.view()` and `print(game)`
  - Used in tournament verbose mode

- **Verbose Mode in Tournaments (Default: ON)** 🔍
  - Shows Unicode board after each move
  - Move number, time, pieces flipped, score, history
  - **Default: True** (can disable with `"verbose": false`)
  - Perfect for debugging and game analysis
  
- **Complete Board Integrity Test Suite** (24 tests)
  - Rigorous forward/backward testing
  - File: `tests/integration/test_board_integrity.py`

- **BitboardGame Comprehensive Test Suite** (25 tests)
  - 2000+ positions verified
  - All edges, corners, directions tested
  - File: `tests/bitboard/test_bitboard_moves_comprehensive.py`

- **BitboardGame False Moves Regression Test** (2 tests)
  - Detects false positive moves
  - File: `tests/regression/test_bitboard_false_moves.py`

### Changed

- **Opening Book Evaluation Mode (NEW Default!)** 📚🔍
  - **NEW PARAMETER**: `book_instant=False` in `PlayerApocalyptron` and `PlayerDivZero`
  - **OLD BEHAVIOR** (`book_instant=True`): Book moves used instantly (no engine evaluation)
  - **NEW BEHAVIOR** (`book_instant=False`, **DEFAULT**): Book moves prioritized but evaluated by engine
  - **Benefit**: AI can choose better moves based on position, not just book score
  - **How it works**: 
    1. Opening book filters and ranks moves by score (with configurable threshold)
    2. Best book moves added to top of evaluation list
    3. Engine evaluates ALL moves (book + non-book) normally
    4. Selects the move with highest engine score (not just best book score)
  - **Impact**: More intelligent play - combines book knowledge with tactical evaluation
  - **Evolved Display**: When `show_book_options=True` and `book_instant=False`:
    - Shows elegant table with book moves, scores, advantages, continuations
    - ★ marks highest-scored move
    - Displays ON TOP priority moves vs filtered out
    - Shows non-book moves separately
    - Clear explanation of what engine will do
  - **Backward Compatibility**: Set `book_instant=True` to restore legacy instant behavior
  - Files modified: `src/Players/PlayerApocalyptron.py`, `src/Players/Gladiators/PlayerDivZero.py`

- **Cleaner Console Output** 🧹
  - Removed verbose "Ready for Phase 2 parallel search" message
  - Silenced pygame welcome message (`PYGAME_HIDE_SUPPORT_PROMPT`)
  - **NEW**: Summary shows "📚 Book moves prioritized: X, Y, Z" to confirm evaluation mode works
  - Visible even with `show_book_options=False` (tournaments)
  - Cleaner output during tournaments and gameplay
  - Fixed: Empty game_history (`""`) was treated as falsy, now correctly handled
  - Files modified: `src/AI/Apocalyptron/observers/console.py`, `src/reversi42.py`

### Fixed

- **CRITICAL: BitboardGame Generates Invalid Moves** 🔴✅
  - **Issue**: BitboardGame.get_valid_moves() generated FALSE POSITIVE moves
    - After specific game sequences, returned A5 and A3 as valid moves
    - Game.get_move_list() correctly excluded these moves (they don't capture anything!)
    - **Effect**: AI selects invalid moves → game corruption → unexpected behavior
  - **Root Cause**: Wrong edge mask for NE (North-East) direction
    - Bug: `(-7, 0xFEFEFEFEFEFEFE00)` ← masks column A instead of H!
    - NE = up + right → must mask row 1 (top) AND column H (right edge)
    - The mask was masking column A (left) instead of column H (right)
  - **Solution**: Corrected NE edge mask
    - Fixed: `(-7, 0x7F7F7F7F7F7F7F00)` ← now correctly masks column H
    - Added detailed comments explaining each mask
  - **Impact**: 
    - This bug affected ALL Apocalyptron-based players (DIVZERO, ORACLE, etc.)
    - Caused invalid move selection in tournaments
    - Explained mysterious "wins" at unexpected moments
  - **Test Coverage**: 
    - ✅ test_bitboard_false_positive_a5 (regression test)
    - ✅ test_bitboard_game_move_parity (10 random games, 200 moves total)
  - **Files Modified**: `src/Reversi/BitboardGame.py` (1 line fix)

- **Critical: Incorrect undo_move() Implementation** 🔴✅
  - **Issue**: Stack saved only board, not turn/turn_cnt
  - **Solution**: Save tuple `(board, turn, turn_cnt)` with backward compatibility
  - **Files Modified**: `src/Reversi/Game.py`

- **Tournament Position Detection** ✅
  - Include turn in position key: `(board, turn)`
  - **Files Modified**: `tournament/tournament.py`


## [4.1.16] - 2025-10-20

### Added - Epic Gladiators Edition 🏆

#### 10 Epic Gladiators System ⚔️
- **Complete Gladiator Roster**: 10 legendary AI fighters with unique personalities and configurations
  - 💀 **DIVZERO.EXE** - The Ultimate Singularity (ELO 1880, Adaptive 8/12/16, 8 cores)
  - 🔮 **THE ORACLE** - Seer of Fates (ELO 1850, Adaptive 7/9/14, Endgame specialist)
  - 🛡️ **FORTRESS ETERNAL** - The Immovable Object (ELO 1800, Stability ×2.0, Defensive)
  - ⚔️ **THE EXECUTIONER** - The Ruthless Destroyer (ELO 1770, Mobility ×2.0 + Positional ×1.5)
  - 🎯 **THE STRANGLER** - The Suffocator (ELO 1750, Mobility ×3.0, Aggressive ×3)
  - 👑 **CORNER REAPER** - Lord of the Corners (ELO 1720, Positional-only, Corner ×2.5)
  - 👾 **GLITCH_LORD** - The Chaotic Anomaly (ELO 1500±200, Parity-only, Unpredictable)
  - ⚡ **LIGHTNING STRIKE** - The Blitz Master (ELO 1400, Fixed depth 4, <100ms response)
  - 🔥 **BLITZ DEMON** - Chaos Incarnate (ELO 1350, Fixed depth 5, <50ms response)
  - 🧘 **ZEN MASTER** - The Enlightened One (ELO 1250, Fixed depth 3, ~30ms response)

- **Modular Gladiator Files**: Each gladiator in separate file (`src/Players/Gladiators/`)
  - Individual class files for better organization and maintainability
  - Complete epic descriptions (max 250 words) in each file
  - Combat parameters with star ratings (⭐⭐⭐⭐⭐)
  - Technical configuration documentation
  - Metadata with headline and strategy fields

#### SearchStrategy Pattern & Engine Flexibility 🎯
- **SearchStrategy Interface**: Abstract base class for pluggable search strategies
  - `FixedDepthStrategy` - Direct search at target depth (no iterative deepening overhead)
  - `IterativeDeepeningStrategy` - Progressive depth 1→N with aspiration windows (default)
  - `AdaptiveDepthStrategy` - Dynamic depth by game phase (opening/midgame/endgame)

- **Dynamic Evaluator Configuration**: Create players with custom evaluator combinations
  - `EvaluatorConfig` dataclass for explicit evaluator settings (type, weight, custom_weights)
  - Support for single-evaluator configurations (mobility-only, positional-only, stability-only, parity-only)
  - Custom weight multipliers per evaluator (e.g., mobility ×3.0 for THE STRANGLER)
  - Mix-and-match evaluator combinations (e.g., stability ×2.0 + positional ×1.5)

- **ApocalyptronConfigBuilder Extensions**: 10+ new fluent API methods
  - `with_search_strategy(strategy)` - Set search strategy type
  - `with_fixed_depth_search()` - Disable iterative deepening
  - `with_adaptive_depth(opening, midgame, endgame)` - Phase-based depth
  - `with_evaluators(configs)` - Set evaluators explicitly
  - `with_only_mobility()`, `with_only_positional()`, `with_only_stability()`, `with_only_parity()` - Single evaluator shortcuts
  - `add_evaluator(type, weight)` - Add single evaluator to configuration
  - `disable_all_pruning()` - Pure alpha-beta mode (educational)

- **New Factory Presets**: 5 additional pre-configured engines
  - `create_speed_demon()` - Maximum speed, minimal intelligence (fixed depth 4, no opts)
  - `create_mobility_obsessed()` - Mobility-only evaluator (all optimizations)
  - `create_corner_hunter()` - Corner-focused positional play (corner_hunter weights)
  - `create_pure_alphabeta()` - No optimizations, all evaluators (educational baseline)
  - `create_adaptive_player()` - Custom adaptive depth configuration

#### Tournament System Expansion 🏆
- **14 Epic Tournament Configurations**: Pre-configured battles in `tournament/ring/`
  - ⚡ **Quick Battle** - 4 top gladiators, fast testing (2 games, ~5 min)
  - 👑 **Ultimate Arena** - ALL 10 gladiators battle royale (2 games, ~60 min)
  - ⚡⚡⚡ **Speed Demons** - Ultra-fast tournament (<200ms per move, 10 games)
  - 💀 **Titans Clash** - Top 5 strongest (ELO 1750+, 4 games, ~30 min)
  - 👾 **Chaos Realm** - Unpredictable madness (6 games, ~10 min)
  - 🔮 **Endgame Masters** - Strategic prophets (4 games, ~20 min)
  - 🎯 **Mobility Assassins** - Suffocation league (3 games, ~15 min)
  - 👑 **Corner Wars** - Territorial conquest (3 games, ~15 min)
  - 🧘 **Zen vs Chaos** - Philosophy wars (8 games, ~10 min)
  - 💀 **Final Boss Challenge** - Can anyone beat DIVZERO? (2 games, ~25 min)
  - 🎓 **Training Ground** - Beginners arena (4 games, ~15 min)
  - 💥 **Apocalypse Now** - Maximum carnage (6 games, ~90 min, with move history)
  - 🔥 **Blitz Madness** - Rapid fire championship (20 games!, ~5 min)
  - ⚔️ **David vs Goliath** - Underdogs challenge (3 games, ~20 min)

- **Quick Tournament Launcher** (`tournament/quick_tournament.py`)
  - Command-line launcher for all 14 tournaments
  - Simple shortcuts: `python quick_tournament.py quick|all|speed|boss|...`
  - `--list` flag to display all available tournaments
  - Automatic configuration loading from ring/ directory

- **Tournament Documentation** (`tournament/ring/README.md`)
  - Complete guide to all 14 tournaments
  - Statistics by speed, player count, and difficulty
  - Recommended tournament progression paths
  - Quick reference comparison table
  - Tips for tournament running and analysis

#### Documentation Expansion 📚
- **Epic Gladiators Documentation**:
  - `docs/EPIC_GLADIATORS.md` (19KB) - Complete epic descriptions, combat parameters, technical specs
  - `docs/GLADIATORS_SUMMARY.md` (5.7KB) - Quick reference with ELO ladder and matchup predictions
  - Each gladiator file includes inline epic description and philosophy

- **Create Custom Player Tutorial** (`docs/tutorials/CREATE_CUSTOM_PLAYER.md`, 40KB)
  - Complete step-by-step guide (500+ lines)
  - Quick start template with copy-paste code
  - Architecture diagrams (ASCII art)
  - 5 complete working examples (Speed Demon, Mobility Master, Adaptive Genius, Corner Fanatic, Tutorial Bot)
  - Advanced techniques (custom weights, dynamic configuration, preset mixing)
  - Visual guides (decision tree, weight impact chart, comparison matrix)
  - Comprehensive troubleshooting section
  - Complete API reference for builder methods
  - Learning path (beginner → intermediate → advanced)

- **Apocalyptron Engine Documentation Update** (`docs/architecture/apocalyptron-engine.md`)
  - New section: "NEW in v4.2.0: SearchStrategy Pattern & Custom Configurations"
  - Complete documentation of 3 search strategies with code examples
  - Custom evaluator combinations guide
  - 5 new factory presets documented with use cases
  - Epic Gladiators configuration table

- **Documentation Index Update** (`docs/DOCUMENTATION_INDEX.md`)
  - Added Epic Gladiators links to user documentation
  - Added CREATE_CUSTOM_PLAYER tutorial to developer guides
  - All new documents marked with ⭐ NEW

- **README Major Update**:
  - Complete player roster table (12 players: Human + Apocalyptron + 10 Gladiators)
  - Detailed gladiator profiles with HEADLINE and STRATEGY for each
  - Comprehensive comparison matrix (21 characteristics: ELO, Power, Speed, Response Time, Search Strategy, Depths, Evaluators, Focus levels, Optimizations, Parallel, Opening Book, Personality, Fun Factor)
  - Quick selection guide (Want to WIN? → DIVZERO, Want SPEED? → ZEN, etc.)
  - Recommended 7-level progression (Beginner → Final Boss)
  - Playing style recommendations (Aggressive/Defensive/Speed/Fun)
  - Complete project structure regenerated with all new files and ⭐ markers
  - Statistics section (300+ files, 15K LoC, 12 AI players, 3 strategies, 220+ tests, 40+ docs)

#### UI/UX Improvements 🎨
- **Menu Optimization**: Player selection panel maximized and compacted
  - Panel size increased: 95% width × 90% height (was 500px × 500px)
  - Title removed for more space (was occupying ~60px)
  - Button height reduced: 35px (was 40px) for vertical compaction
  - Dynamic spacing: 3-30px (adapts to player count)
  - Font size: 18 (optimized for compact display)
  - Capacity: Now supports 15-20 players comfortably (was ~7-8)
  - All 12 current players fit with optimal spacing (~17px)

- **Image Widget**: Auto-resizing image component with fit modes (contain, cover, fill, none)
- **TextArea Widget**: Multi-line text editor with scrolling and line numbers

#### Testing & Quality 🧪
- **35 New Tests Added** (Total: 220+ tests, 100% pass rate)
  - `tests/apocalyptron/unit/test_search_strategies.py` (10 tests)
    - Fixed depth strategy validation (no progressive deepening)
    - Adaptive depth strategy with phase detection
    - Strategy interface compliance
  - `tests/apocalyptron/integration/test_diverse_configurations.py` (15 tests)
    - Mobility-only player (3x weight)
    - Positional-only player
    - Stability-focused player (2x weight)
    - Hybrid configurations
    - Factory preset validation
  - `tests/apocalyptron/integration/test_epic_gladiators.py` (10 tests)
    - All 10 gladiators instantiation
    - Configuration verification (depth, strategy, evaluators)
    - Valid move generation
    - Specific player traits (LIGHTNING fast, STRANGLER mobility focus, etc.)

### Changed

- **ApocalyptronEngine**: Now uses SearchStrategy pattern via `_build_search_strategy()` method
  - Backward compatible: default behavior identical to v4.1.15
  - `ParallelSearch` now wraps `SearchStrategy` instead of direct search
  - Print statements updated to show selected search strategy

- **ApocalyptronConfig**: Extended with 3 new fields
  - `search_strategy: str = 'iterative_deepening'` - Strategy type selector
  - `evaluators: List[EvaluatorConfig]` - Explicit evaluator configuration (replaces default all-4)
  - `adaptive_depths: Dict[str, int]` - Phase-specific depth settings
  - `to_dict()` updated to serialize new fields

- **PlayerApocalyptron**: Enhanced with new optional parameters
  - `search_strategy` parameter for strategy selection (default: None → iterative_deepening)
  - `config_builder` parameter for advanced configuration (default: None → auto-build)
  - Backward compatible: all existing code works unchanged

- **PlayerFactory**: Updated to register all 10 Epic Gladiators
  - Imports from `Players.Gladiators` module
  - Automatic discovery and registration
  - Display names without emoji for menu compatibility

- **Menu System** (`src/ui/implementations/pygame/components/menu.py`):
  - `_build_player_selection_menu()` completely rewritten for compaction
  - Panel dimensions: responsive (95% × 90%) instead of fixed (500×500)
  - Button dimensions: 35px height (from 45px), adaptive width
  - Spacing algorithm: dynamic 3-30px (from fixed 55px)
  - Back button: compacted to 50px from bottom (from 70px)

- **Splashscreen Asset**: Moved `reversi42-splash.png` from `Images/` to project root
  - Updated reference in `src/ui/implementations/pygame/components/menu.py`

- **InputBox Widget**: Updated to support `center_in_parent` and absolute coordinates

### Fixed

- **Adaptive Depth Phase Detection**: Fixed `BitboardGame` instantiation in tests
  - Changed from `BitboardGame(black=..., white=...)` to `BitboardGame.create_empty()` with manual setup
  - Properly handles empty board creation for phase testing

- **Strategy Observer Compatibility**: Added `observers` property to all search strategies
  - `FixedDepthStrategy` and `IterativeDeepeningStrategy` now expose observers
  - `ParallelSearch` can now properly access and modify observers for all strategy types

- **Emoji in Display Names**: Removed all emoji from `PLAYER_METADATA["display_name"]`
  - Ensures menu compatibility and `PlayerFactory.create_player()` calls
  - Emojis retained in documentation and comments for visual appeal

### Documentation

- **AI-Human Collaboration Section**: Added to README
  - Recognizes experimental development process
  - Documents collaboration between human vision and AI assistance
  - Describes technologies used and development paradigm
  - Vision for future of collaborative software development

### Technical Notes

- **100% Backward Compatibility**: All existing code works unchanged
  - Default configuration identical to v4.1.15
  - All 220+ tests pass (100% success rate)
  - Zero breaking changes in API or behavior
  - Players created with old API continue to work

- **File Organization**: ~50 new files created, well-organized structure
  - `src/Players/Gladiators/` - 11 files (10 gladiators + `__init__.py`)
  - `src/AI/Apocalyptron/search/` - 4 new strategy files
  - `tournament/ring/` - 14 tournament configs + README + launcher
  - `docs/` - 3 new major docs + 2 updated
  - `tests/apocalyptron/` - 3 new test files

- **Code Quality**:
  - Zero linter errors
  - Consistent formatting throughout
  - Comprehensive inline documentation
  - Epic descriptions for all gladiators

- **Performance**: No regression in existing functionality
  - Speed tests validate all gladiators perform as expected
  - LIGHTNING STRIKE <100ms, BLITZ DEMON <50ms, ZEN MASTER ~30ms verified
  - Adaptive depth strategies perform efficient resource allocation

- **Menu Capacity**: Supports up to 18 players comfortably
  - Current 12 players (Human + Apocalyptron + 10 Gladiators) fit with optimal spacing
  - Room for 6 more players before requiring scroll or panel adjustment

### Upgrade Notes

To use the new features:

```python
# Create gladiator
from Players.PlayerFactory import PlayerFactory
divzero = PlayerFactory.create_player('DIVZERO.EXE')

# Custom configuration
from AI.Apocalyptron import ApocalyptronConfigBuilder
config = (
    ApocalyptronConfigBuilder()
    .with_adaptive_depth(opening=8, midgame=12, endgame=16)
    .with_evaluators([...])
    .enable_all_optimizations()
    .build()
)

# Run tournament
python tournament/quick_tournament.py all
```

See `docs/tutorials/CREATE_CUSTOM_PLAYER.md` for complete guide.


## [4.1.15] - 2025-10-20

### Added
- **Bootstrap-like Layout System**: New declarative UI primitives for responsive layouts
  - `Stack` (enhanced VBox with justify), `Center`, `Row/Col` (12-column grid), `Spacer`, `Divider`
  - `center_in_parent` parameter for automatic widget centering
  - `Title()` helper function for one-line centered titles
  - Complete documentation in `docs/architecture/ui-layout-system.md`

### Changed
- **UI Code Reduction**: Refactored all GUI components with new layout system
  - Main menu: 120 LoC → 60 LoC (-50%)
  - Pause menu: 95 LoC → 50 LoC (-47%)
  - Game over screen: 140 LoC → 70 LoC (-50%)
- **Widget System**: VBox/HBox now respect explicit dimensions and auto-centering preferences


## [4.1.14] - 2025-10-20

### Added
- **Comprehensive Test Suite for Apocalyptron Engine**: Added 185 automated tests covering all engine components
  - 23 performance benchmark tests measuring NPS, pruning effectiveness, and scaling
  - 12 AlphaBeta search tests with transposition table validation
  - 17 cache module tests (Zobrist hashing, transposition table)
  - 21 evaluation module tests (mobility, stability, positional, parity)
  - 19 observer pattern tests (console, statistics, quiet observers)
  - 20 move ordering tests (PV, killer moves, history heuristic, positional)
  - 26 pruning tests (null move, futility, LMR, multi-cut)
  - 24 search algorithm tests (iterative deepening, parallel search)
  - 20 integration tests (end-to-end engine validation)
- **Performance Benchmarks**: Automated performance tracking for:
  - Search speed at various depths (depth 1-9)
  - Nodes per second (NPS) metrics (>1000 NPS baseline, up to 13,000 NPS)
  - Pruning effectiveness (alpha-beta: 10-30%, null move: 30-50%, LMR: 10-20%)
  - Transposition table hit rates and efficiency
  - Memory usage and scaling characteristics
  - Opening book response time validation (<10ms)

### Changed
- **Code Formatting**: Applied Black and isort to entire codebase (141 files formatted)
- **Test Infrastructure**: Aligned all test APIs with current Apocalyptron architecture
  - Updated BitboardGame API usage (move(), turn, get_move_list())
  - Fixed SearchContext and SearchResult integration
  - Corrected observer pattern implementation

### Fixed
- Removed legacy characterization tests incompatible with current Apocalyptron API
- Fixed pytest configuration warnings (removed unsupported pythonpath option)
- Corrected test function return values (pytest compliance)
- Aligned pruning tests with should_prune(SearchContext) API

### Performance
- Test suite executes in 14.6s for full 185 tests
- All performance benchmarks validate expected speedups and optimization effectiveness
- Confirmed alpha-beta pruning: 22-28% node reduction
- Confirmed null move pruning: 30-50% success rate in midgame
- Confirmed LMR: <20% re-search rate (excellent efficiency)


## Links

- [Documentation](docs/)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [License](COPYING)

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes
- **Performance**: Performance improvements



