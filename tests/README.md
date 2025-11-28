# Reversi42 - Test Suite

Comprehensive test suite for the Reversi42 project.

## 📊 Test Statistics

- **Total Tests**: 572+
- **Test Files**: 44
- **Coverage Target**: 80%+
- **Test Categories**: Unit, Integration, Characterization, Performance, E2E

## 🧪 Test Organization

### Apocalyptron AI Engine (`tests/apocalyptron/`)
- **Unit Tests**: 750+ tests covering evaluation, ordering, pruning, cache, search, observers, randomization
- **Integration Tests**: 50+ tests for complete engine functionality (including temperature-based move variety)
- **Characterization Tests**: Known position verification
- **Performance Tests**: Benchmarks and speed tests

### Board Module (`tests/board/`)
- **test_board_model.py**: 9 tests - BoardModel functionality
- **test_board_control.py**: 18 tests - BoardControl MVC controller
- **test_view_factory.py**: 7 tests - ViewFactory for creating views

### Players Module (`tests/players/`)
- **test_player_factory.py**: 11 tests - PlayerFactory for creating players
- **test_player_human.py**: 9 tests - Human player implementation
- **test_player_apocalyptron.py**: 12 tests - Apocalyptron AI player
- **test_config_factory.py**: 12 tests - Config-based player factory
- **test_config_loader.py**: 8 tests - YAML configuration loader
- **test_config_validator.py**: 9 tests - Configuration validation
- **test_config_discovery.py**: 8 tests - Player configuration discovery

### Core Module (`tests/core/`)
- **test_config.py**: 23 tests - Core configuration constants
- **test_game_config.py**: 11 tests - Game configuration loader

### Infrastructure (`tests/infrastructure/`)
- **test_game_io.py**: 10 tests - Game save/load functionality (XOT format)

### Integration Tests (`tests/integration/`)
- **test_board_integrity.py**: Board state integrity tests
- **test_player_isolation.py**: Player isolation tests
- **test_book_instant_mode.py**: Opening book instant mode tests
- **test_webgui_player_isolation.py**: WebGUI player isolation

### Bitboard Tests (`tests/bitboard/`)
- **test_bitboard_moves_comprehensive.py**: Comprehensive bitboard move generation tests

### Domain Tests (`tests/domain/`)
- **test_enhanced_opening_book.py**: Enhanced opening book functionality

### Randomization Tests (`tests/apocalyptron/unit/`)
- **test_randomization.py**: 16 tests - Temperature-based move selection and probabilistic move variety

### Temperature Integration Tests (`tests/apocalyptron/integration/`)
- **test_temperature_integration.py**: 8 tests - Temperature functionality integrated with engine, player, opening book, and parallel search

### WebGUI Tests (`tests/webgui/`)
- **test_backend_server.py**: Backend server tests
- **test_websocket_observer.py**: WebSocket observer tests
- **test_e2e.py**: End-to-end tests

### Regression Tests (`tests/regression/`)
- **test_bitboard_false_moves.py**: Regression tests for bitboard move validation

## 🚀 Running Tests

### Run All Tests
```bash
# From project root
./scripts/run_tests.sh

# Or with pytest
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest --cov=src --cov-report=html --cov-report=term tests/
```

### Run Specific Test Suites
```bash
# Apocalyptron tests
pytest tests/apocalyptron/ -v

# Board tests
pytest tests/board/ -v

# Players tests
pytest tests/players/ -v

# Integration tests
pytest tests/integration/ -v
```

### Run Individual Test Files
```bash
# Board model tests
pytest tests/board/test_board_model.py -v

# Player factory tests
pytest tests/players/test_player_factory.py -v

# Game config tests
pytest tests/core/test_game_config.py -v
```

## ✅ Test Status

| Test Suite | Status | Tests | Coverage |
|------------|--------|-------|----------|
| Apocalyptron Engine | ✅ | 800+ | >80% |
| Board Module | ✅ | 34 | >70% |
| Players Module | ✅ | 60+ | >75% |
| Core Module | ✅ | 34 | >80% |
| Infrastructure | ✅ | 10 | >70% |
| Integration | ✅ | 50+ | >70% |
| Bitboard | ✅ | Comprehensive | >80% |
| WebGUI | ✅ | Multiple | >70% |

## 📝 Adding New Tests

1. Create test file in appropriate `tests/` subdirectory
2. Name it `test_*.py`
3. Follow existing test patterns and use pytest fixtures
4. Add docstrings describing what is tested
5. Update this README with new test information

## 🎯 Coverage Goals

- **Overall Coverage**: 80%+
- **Critical Modules**: 90%+ (Apocalyptron engine, Game logic)
- **Support Modules**: 70%+ (UI, configuration, persistence)

## 📚 Test Documentation

- **TEST_BATTERIES_SUMMARY.md**: Summary of Apocalyptron test batteries
- **apocalyptron/TEST_STRATEGY.md**: Detailed testing strategy for Apocalyptron
- **apocalyptron/README.md**: Apocalyptron test suite documentation
- **integration/README.md**: Integration test documentation
- **webgui/README.md**: WebGUI test documentation
