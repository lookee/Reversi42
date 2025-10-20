# Changelog

All notable changes to Reversi42 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Image Widget**: Auto-resizing image component with fit modes (contain, cover, fill, none)
- **TextArea Widget**: Multi-line text editor with scrolling and line numbers
- **Epic Gladiators System**: 10 legendary AI opponents with unique fighting styles
  - DIVZERO.EXE 💀 - Ultimate singularity (adaptive 8/12/16, ELO ~1880)
  - LIGHTNING STRIKE ⚡ - Blitz master (<100ms, ELO ~1400)
  - THE STRANGLER 🎯 - Mobility assassin (3x mobility focus, ELO ~1750)
  - FORTRESS ETERNAL 🛡️ - Defensive master (2x stability, ELO ~1800)
  - CORNER REAPER 👑 - Corner specialist (2.5x corner value, ELO ~1720)
  - THE ORACLE 🔮 - Endgame prophet (adaptive 7/9/14, ELO ~1850)
  - BLITZ DEMON 🔥 - Speed incarnate (<50ms, ELO ~1350)
  - THE EXECUTIONER ⚔️ - Hybrid destroyer (mobility+positional, ELO ~1770)
  - GLITCH_LORD 👾 - Chaotic anomaly (parity-only, ELO ~1500±200)
  - ZEN MASTER 🧘 - Minimalist monk (depth 3, no opts, ELO ~1250)
- **SearchStrategy Pattern**: Flexible search strategy architecture
  - `FixedDepthStrategy` - Direct search at target depth (no iterative deepening)
  - `IterativeDeepeningStrategy` - Progressive depth 1→N (default behavior)
  - `AdaptiveDepthStrategy` - Depth varies by game phase (opening/midgame/endgame)
- **Dynamic Evaluator Configuration**: Create players with custom evaluator combinations
  - Support for single-evaluator configurations (mobility-only, positional-only, etc.)
  - Custom weight multipliers per evaluator
  - Mix-and-match evaluator combinations
- **ApocalyptronConfigBuilder Extensions**: New fluent API methods
  - `with_fixed_depth_search()` - Disable iterative deepening
  - `with_adaptive_depth(opening, midgame, endgame)` - Phase-based depth
  - `with_only_mobility()`, `with_only_positional()`, etc. - Single evaluator configs
  - `disable_all_pruning()` - Pure alpha-beta mode
- **New Factory Presets**: 5 additional engine configurations
  - `create_speed_demon()` - Maximum speed, minimal intelligence
  - `create_mobility_obsessed()` - Mobility-only evaluator
  - `create_corner_hunter()` - Corner-focused positional play
  - `create_pure_alphabeta()` - No optimizations (educational)
  - `create_adaptive_player()` - Custom adaptive depth configuration

### Changed
- **InputBox**: Updated to support `center_in_parent` and absolute coordinates
- **ApocalyptronEngine**: Now uses SearchStrategy pattern (backward compatible)
- **ApocalyptronConfig**: Extended with `search_strategy`, `evaluators`, `adaptive_depths` fields
- **PlayerApocalyptron**: Added `search_strategy` and `config_builder` parameters (backward compatible)

### Fixed

### Technical Notes
- All 206 existing tests pass (100% backward compatibility)
- Added 35 new tests for new features
- Zero breaking changes - default behavior identical to before
- Menu automatically displays all 10 new gladiators (via PlayerFactory)


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



