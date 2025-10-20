# Apocalyptron Test Suite

Comprehensive test suite for the Apocalyptron AI engine.

**Total Tests**: 800+ tests  
**Coverage Target**: >80%  
**Test Categories**: Unit, Integration, Characterization, Performance

---

## 📁 Test Organization

```
tests/apocalyptron/
├── conftest.py                        # Pytest fixtures & config ⭐ NEW
├── TEST_STRATEGY.md                   # Testing strategy doc ⭐ NEW
├── README.md                          # This file ⭐ NEW
│
├── unit/                              # Unit tests (fast, isolated)
│   ├── test_evaluation_module.py      # ~200 tests ⭐ NEW
│   ├── test_ordering_module.py        # ~150 tests ⭐ NEW
│   ├── test_pruning_module.py         # ~120 tests ⭐ NEW
│   ├── test_cache_module.py           # ~100 tests ⭐ NEW
│   ├── test_search_module.py          # ~100 tests ⭐ NEW
│   ├── test_observer_module.py        # ~80 tests ⭐ NEW
│   ├── test_alphabeta.py              # Existing
│   ├── test_alphabeta_complete.py     # Existing
│   └── test_standalone_engine.py      # Existing
│
├── integration/                       # Integration tests
│   ├── test_apocalyptron_complete.py  # ~50 tests ⭐ NEW
│   ├── test_apocalyptron_basic.py     # Existing
│   ├── test_engine_equivalence.py     # Existing
│   └── test_observer_pattern.py       # Existing
│
├── characterization/                  # Behavior verification
│   ├── test_grandmaster_baseline.py   # Existing
│   └── test_positions.py              # Existing
│
├── performance/                       # Performance benchmarks
│   └── (performance tests)
│
└── regression/                        # Regression tests
    └── (regression tests)
```

---

## 🚀 Quick Start

### Run All Tests

```bash
# All Apocalyptron tests
pytest tests/apocalyptron/ -v

# With coverage
pytest tests/apocalyptron/ --cov=src/AI/Apocalyptron --cov-report=html

# Parallel execution (faster)
pytest tests/apocalyptron/ -n auto
```

### Run by Category

```bash
# Unit tests only (fast)
pytest tests/apocalyptron/unit/ -v

# Integration tests
pytest tests/apocalyptron/integration/ -v

# Characterization tests
pytest tests/apocalyptron/characterization/ -v
```

### Run Specific Module

```bash
# Evaluation tests
pytest tests/apocalyptron/unit/test_evaluation_module.py -v

# Ordering tests
pytest tests/apocalyptron/unit/test_ordering_module.py -v

# Pruning tests
pytest tests/apocalyptron/unit/test_pruning_module.py -v

# Cache tests
pytest tests/apocalyptron/unit/test_cache_module.py -v

# Search tests
pytest tests/apocalyptron/unit/test_search_module.py -v

# Observer tests
pytest tests/apocalyptron/unit/test_observer_module.py -v
```

### Run by Marker

```bash
# Fast tests only
pytest tests/apocalyptron/ -m "not slow" -v

# Slow tests only
pytest tests/apocalyptron/ -m slow -v

# Unit tests only
pytest tests/apocalyptron/ -m unit -v

# Integration tests only
pytest tests/apocalyptron/ -m integration -v
```

---

## 📊 Test Modules

### 1. Evaluation Module Tests (test_evaluation_module.py)

**Tests**: ~200  
**Covers**:
- MobilityEvaluator (25 tests)
- StabilityEvaluator (20 tests)
- PositionalEvaluator (25 tests)
- ParityEvaluator (15 tests)
- CompositeEvaluator (35 tests)
- Evaluator consistency (100 tests)

**Example**:
```bash
# Run mobility tests only
pytest tests/apocalyptron/unit/test_evaluation_module.py::TestMobilityEvaluator -v

# Run composite evaluator tests
pytest tests/apocalyptron/unit/test_evaluation_module.py::TestCompositeEvaluator -v
```

### 2. Ordering Module Tests (test_ordering_module.py)

**Tests**: ~150  
**Covers**:
- PVMoveOrderer (25 tests)
- KillerMoveOrderer (30 tests)
- HistoryHeuristic (30 tests)
- PositionalOrderer (25 tests)
- CompositeOrderer (40 tests)

**Example**:
```bash
# Run killer move tests
pytest tests/apocalyptron/unit/test_ordering_module.py::TestKillerMoveOrderer -v
```

### 3. Pruning Module Tests (test_pruning_module.py)

**Tests**: ~120  
**Covers**:
- NullMovePruning (30 tests)
- FutilityPruning (30 tests)
- LateMoveReduction (35 tests)
- MultiCutPruning (25 tests)

**Example**:
```bash
# Run LMR tests
pytest tests/apocalyptron/unit/test_pruning_module.py::TestLateMoveReduction -v
```

### 4. Cache Module Tests (test_cache_module.py)

**Tests**: ~100  
**Covers**:
- ZobristHash (50 tests)
- TranspositionTable (50 tests)

**Example**:
```bash
# Run zobrist tests
pytest tests/apocalyptron/unit/test_cache_module.py::TestZobristHash -v

# Run TT tests
pytest tests/apocalyptron/unit/test_cache_module.py::TestTranspositionTable -v
```

### 5. Search Module Tests (test_search_module.py)

**Tests**: ~100  
**Covers**:
- AlphaBetaSearch (35 tests)
- AlphaBetaCompleteSearch (30 tests)
- IterativeDeepeningSearch (25 tests)
- ParallelSearch (10 tests)

**Example**:
```bash
# Run search tests
pytest tests/apocalyptron/unit/test_search_module.py -v

# Skip parallel tests (if no multiprocessing)
pytest tests/apocalyptron/unit/test_search_module.py -v -k "not parallel"
```

### 6. Observer Module Tests (test_observer_module.py)

**Tests**: ~80  
**Covers**:
- ConsoleObserver (25 tests)
- StatisticsObserver (35 tests)
- QuietObserver (20 tests)

**Example**:
```bash
# Run observer tests
pytest tests/apocalyptron/unit/test_observer_module.py -v
```

### 7. Complete Integration Tests (test_apocalyptron_complete.py)

**Tests**: ~50  
**Covers**:
- Full engine integration
- All components together
- Performance validation
- Edge cases

**Example**:
```bash
# Run integration tests
pytest tests/apocalyptron/integration/test_apocalyptron_complete.py -v

# Skip slow performance tests
pytest tests/apocalyptron/integration/test_apocalyptron_complete.py -v -m "not slow"
```

---

## 🎯 Testing Scenarios

### Scenario 1: Development (Fast Feedback)

```bash
# Quick unit tests while coding
pytest tests/apocalyptron/unit/test_evaluation_module.py -x

# x = stop at first failure
```

### Scenario 2: Pre-Commit (Quality Check)

```bash
# All unit tests
pytest tests/apocalyptron/unit/ -v

# Should complete in < 1 minute
```

### Scenario 3: Pre-Push (Full Verification)

```bash
# All tests including integration
pytest tests/apocalyptron/ -v

# Should complete in < 5 minutes
```

### Scenario 4: CI/CD (Comprehensive)

```bash
# Complete suite with coverage
pytest tests/apocalyptron/ -v --cov=src/AI/Apocalyptron --cov-report=xml --cov-report=term -n auto

# What GitHub Actions runs
```

### Scenario 5: Performance Regression

```bash
# Performance tests only
pytest tests/apocalyptron/ -m performance -v

# Benchmark mode (if pytest-benchmark installed)
pytest tests/apocalyptron/performance/ --benchmark-only
```

---

## 📈 Coverage Analysis

### Generate Coverage Report

```bash
# HTML report (best for detailed analysis)
pytest tests/apocalyptron/ --cov=src/AI/Apocalyptron --cov-report=html
open htmlcov/index.html

# Terminal report
pytest tests/apocalyptron/ --cov=src/AI/Apocalyptron --cov-report=term-missing

# XML report (for CI tools like Codecov)
pytest tests/apocalyptron/ --cov=src/AI/Apocalyptron --cov-report=xml
```

### Coverage by Module

```bash
# Evaluation module coverage
pytest tests/apocalyptron/unit/test_evaluation_module.py \
    --cov=src/AI/Apocalyptron/evaluation \
    --cov-report=term-missing

# Search module coverage
pytest tests/apocalyptron/unit/test_search_module.py \
    --cov=src/AI/Apocalyptron/search \
    --cov-report=term-missing
```

---

## 🐛 Debugging Tests

### Run with Verbose Output

```bash
# Very verbose (-vv)
pytest tests/apocalyptron/unit/test_evaluation_module.py -vv

# Show local variables on failure
pytest tests/apocalyptron/unit/test_evaluation_module.py -vv -l

# Show print statements
pytest tests/apocalyptron/unit/test_evaluation_module.py -s
```

### Debug Specific Test

```bash
# Run single test with debugger
pytest tests/apocalyptron/unit/test_evaluation_module.py::TestMobilityEvaluator::test_initial_position_mobility --pdb

# Or use ipdb (if installed)
pytest tests/apocalyptron/unit/test_evaluation_module.py::TestMobilityEvaluator::test_initial_position_mobility --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### Stop on First Failure

```bash
# Stop at first failure (-x)
pytest tests/apocalyptron/ -x

# Stop after N failures
pytest tests/apocalyptron/ --maxfail=3
```

---

## ⚡ Performance Optimization

### Parallel Test Execution

```bash
# Auto-detect cores
pytest tests/apocalyptron/ -n auto

# Specific core count
pytest tests/apocalyptron/ -n 4

# Distribute to multiple CPUs
pytest tests/apocalyptron/ -n 8 --dist loadscope
```

### Test Selection

```bash
# Run only changed tests (requires pytest-testmon)
pytest --testmon

# Run failed tests from last run
pytest --lf

# Run failed first, then rest
pytest --ff
```

---

## 📊 Test Reporting

### Generate Test Report

```bash
# HTML report
pytest tests/apocalyptron/ --html=report.html --self-contained-html

# JUnit XML (for CI)
pytest tests/apocalyptron/ --junitxml=junit.xml

# JSON report
pytest tests/apocalyptron/ --json-report --json-report-file=report.json
```

### Show Slowest Tests

```bash
# Show 10 slowest tests
pytest tests/apocalyptron/ --durations=10

# Show all durations
pytest tests/apocalyptron/ --durations=0
```

---

## 🎓 Writing New Tests

### Test Template

```python
"""
Test suite for <Component>.

Brief description of what is being tested.
"""

import pytest
from src.AI.Apocalyptron.<module>.<file> import ComponentClass


class TestComponent:
    """Test suite for Component."""
    
    def test_component_initialization(self):
        """Test that component initializes correctly."""
        component = ComponentClass()
        
        assert component is not None
        assert hasattr(component, 'main_method')
    
    def test_component_basic_functionality(self):
        """Test basic functionality."""
        component = ComponentClass()
        
        result = component.main_method(args)
        
        assert result is not None
        assert isinstance(result, ExpectedType)
    
    @pytest.mark.slow
    def test_component_performance(self):
        """Test component performance."""
        component = ComponentClass()
        
        start = time.perf_counter()
        component.expensive_operation()
        elapsed = time.perf_counter() - start
        
        assert elapsed < 1.0, "Should complete in < 1s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Using Fixtures

```python
def test_with_fixtures(initial_game, apocalyptron_player_fast):
    """Test using provided fixtures."""
    moves = initial_game.get_valid_moves(1)
    move = apocalyptron_player_fast.get_move(initial_game, moves, None)
    
    assert move in moves
```

### Parametrized Tests

```python
@pytest.mark.parametrize("depth,expected_time", [
    (4, 0.1),
    (6, 0.5),
    (9, 2.0),
])
def test_search_at_depth(depth, expected_time, initial_game):
    """Test search performance at various depths."""
    player = PlayerApocalyptron(depth=depth)
    moves = initial_game.get_valid_moves(1)
    
    start = time.perf_counter()
    move = player.get_move(initial_game, moves, None)
    elapsed = time.perf_counter() - start
    
    assert elapsed < expected_time * 2  # 2x margin for CI
```

---

## 📊 Test Metrics

### Current Status

Run to see current metrics:

```bash
# Test count
pytest tests/apocalyptron/ --collect-only | grep "<Function\|<Method" | wc -l

# Coverage
pytest tests/apocalyptron/ --cov=src/AI/Apocalyptron --cov-report=term

# Duration
pytest tests/apocalyptron/ --durations=0
```

### Target Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Total Tests | 800+ | Run to check |
| Coverage | >80% | Run to check |
| Unit Test Speed | <1 min | Fast |
| Full Suite Speed | <10 min | Medium |
| Flaky Tests | 0 | 0 |

---

## 🔍 Test Fixtures Available

See `conftest.py` for all available fixtures:

- **initial_game** - Fresh game at start position
- **midgame_position** - Typical midgame (~30 pieces)
- **endgame_position** - Near end (~56 pieces)
- **corner_position** - Position with corners captured
- **apocalyptron_config_default** - Default config (depth 6)
- **apocalyptron_config_fast** - Fast config (depth 4, no book)
- **apocalyptron_player_fast** - Fast player for tests
- **apocalyptron_player_default** - Default player
- **apocalyptron_assertions** - Custom assertion helpers
- **performance_tracker** - Track performance across tests

---

## 🎯 Test Coverage by Module

| Module | Tests | Coverage Target | Files |
|--------|-------|-----------------|-------|
| **Evaluation** | 200+ | >90% | test_evaluation_module.py |
| **Ordering** | 150+ | >85% | test_ordering_module.py |
| **Pruning** | 120+ | >75% | test_pruning_module.py |
| **Cache** | 100+ | >85% | test_cache_module.py |
| **Search** | 100+ | >85% | test_search_module.py |
| **Observer** | 80+ | >70% | test_observer_module.py |
| **Integration** | 50+ | >80% | test_apocalyptron_complete.py |
| **Characterization** | Existing | N/A | test_positions.py |

---

## 🏆 Best Practices

### DO

✅ **Write focused tests** - One concept per test  
✅ **Use descriptive names** - `test_mobility_at_initial_position`  
✅ **Use fixtures** - Avoid code duplication  
✅ **Mark slow tests** - `@pytest.mark.slow`  
✅ **Test edge cases** - Empty moves, single move, game over  
✅ **Assert messages** - Clear failure messages  

### DON'T

❌ **Test implementation details** - Test behavior, not internals  
❌ **Long tests** - Keep unit tests < 100ms  
❌ **Flaky tests** - Tests should be deterministic  
❌ **No assertions** - Every test needs assertions  
❌ **Copy-paste** - Use fixtures and parametrize  

---

## 🐛 Troubleshooting

### Tests Failing

**Check**:
1. Dependencies installed: `pip install -r requirements-dev.txt`
2. Code is correct (not test)
3. Test expectations are correct
4. Environment is clean

**Debug**:
```bash
# Run with debugger
pytest <test_file>::<test_name> --pdb

# Show local variables
pytest <test_file> -l

# Verbose output
pytest <test_file> -vv -s
```

### Slow Tests

**Identify**:
```bash
pytest tests/apocalyptron/ --durations=20
```

**Optimize**:
- Use lower depth in tests (4-6 instead of 9-12)
- Mock expensive operations
- Mark as `@pytest.mark.slow`
- Run in parallel: `-n auto`

### Import Errors

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"

# Or install in editable mode
pip install -e .
```

---

## 📚 Related Documentation

- **[Test Strategy](TEST_STRATEGY.md)** - Complete testing strategy
- **[Development Guide](../../docs/development/README.md)** - Development setup
- **[Contributing Guide](../../CONTRIBUTING.md)** - How to contribute
- **[CI/CD Guide](../../docs/ci-cd/README.md)** - Continuous integration

---

## 🤝 Contributing Tests

### Adding New Tests

1. Choose appropriate file (evaluation, ordering, etc.)
2. Follow naming convention: `test_<component>_<behavior>`
3. Add docstring
4. Use fixtures from conftest.py
5. Add parametrized tests for multiple scenarios
6. Mark slow tests appropriately
7. Run and verify pass: `pytest <file> -v`

### Submitting Test PRs

1. Run full test suite: `pytest tests/apocalyptron/ -v`
2. Check coverage: `--cov=src/AI/Apocalyptron`
3. Ensure >= 80% coverage for new code
4. Include test in PR description
5. Link to issue if fixing bug

---

## 🎯 Test Roadmap

### Completed ✅
- [x] Evaluation module tests (200+ tests)
- [x] Ordering module tests (150+ tests)
- [x] Pruning module tests (120+ tests)
- [x] Cache module tests (100+ tests)
- [x] Search module tests (100+ tests)
- [x] Observer module tests (80+ tests)
- [x] Integration tests (50+ tests)
- [x] Test fixtures and configuration

### Planned 📝
- [ ] Performance regression tests
- [ ] Property-based tests (Hypothesis)
- [ ] Mutation testing integration
- [ ] Benchmark comparisons
- [ ] More edge case coverage

---

**Test Suite Version**: 1.0  
**Last Updated**: 2025-10-20  
**Status**: Production Ready

*For questions about testing, see [TEST_STRATEGY.md](TEST_STRATEGY.md) or [Contributing Guide](../../CONTRIBUTING.md).*

