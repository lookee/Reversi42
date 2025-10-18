# Reversi42 - Test Suite

This directory contains all test files for the Reversi42 project.

## 🧪 Available Tests

### Core Tests
- **test_bitboard_book.py** - Comprehensive bitboard and opening book integration tests (37 tests)
- **test_parallel_engine.py** - Parallel engine functionality and performance benchmarks

### Tournament Tests
- **test_tournament.py** - Tournament system tests
- **test_move_history.py** - Move history recording tests
- **test_report_save.py** - Tournament report generation tests

## 🚀 Running Tests

### Run All Tests
```bash
# From project root
python run_tests.py
```

### Run Individual Tests
```bash
# Bitboard tests
python tests/test_bitboard_book.py

# Parallel engine tests
python tests/test_parallel_engine.py

# Tournament tests
python tests/test_tournament.py
```

## ✅ Test Status (v3.0.0)

| Test Suite | Status | Tests | Pass Rate |
|------------|--------|-------|-----------|
| Bitboard Integration | ✅ | 37 | 100% |
| Parallel Engine | ✅ | 3 | 100% |
| Tournament System | ✅ | - | 100% |

## 📝 Adding New Tests

1. Create test file in `tests/` directory
2. Name it `test_*.py`
3. Add to `run_tests.py` if it should run automatically
4. Document in this README

