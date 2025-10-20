# Changelog

All notable changes to Reversi42 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed


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



