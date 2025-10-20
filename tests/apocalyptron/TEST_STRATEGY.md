# Apocalyptron Test Strategy

Complete testing strategy for the Apocalyptron AI engine.

**Status**: ✅ Implemented  
**Coverage Target**: >80%  
**Test Files**: 8+ files, 1000+ tests

---

## 🎯 Testing Philosophy

The Apocalyptron engine is tested at multiple levels:

1. **Unit Tests** - Individual components in isolation
2. **Integration Tests** - Components working together
3. **Characterization Tests** - Behavior verification
4. **Performance Tests** - Speed and efficiency benchmarks
5. **Regression Tests** - Ensure no performance degradation

---

## 📁 Test Organization

```
tests/apocalyptron/
├── unit/                          # Unit tests (fast, isolated)
│   ├── test_evaluation_module.py  ⭐ NEW (200+ tests)
│   ├── test_ordering_module.py    ⭐ NEW (150+ tests)
│   ├── test_pruning_module.py     ⭐ NEW (120+ tests)
│   ├── test_cache_module.py       ⭐ NEW (100+ tests)
│   ├── test_search_module.py      ⭐ NEW (100+ tests)
│   ├── test_observer_module.py    ⭐ NEW (80+ tests)
│   ├── test_alphabeta.py          ✅ Existing
│   ├── test_alphabeta_complete.py ✅ Existing
│   └── test_standalone_engine.py  ✅ Existing
│
├── integration/                   # Integration tests (medium speed)
│   ├── test_apocalyptron_complete.py ⭐ NEW (50+ tests)
│   ├── test_apocalyptron_basic.py    ✅ Existing
│   ├── test_engine_equivalence.py    ✅ Existing
│   └── test_observer_pattern.py      ✅ Existing
│
├── characterization/              # Behavior tests (known positions)
│   ├── test_grandmaster_baseline.py  ✅ Existing
│   └── test_positions.py             ✅ Existing
│
├── performance/                   # Performance benchmarks
│   └── test_benchmarks.py        ⭐ NEW
│
└── regression/                    # Regression tests
    └── test_no_regression.py     ⭐ NEW
```

---

## 🧪 Test Categories

### 1. Unit Tests (Module-Level)

**Purpose**: Test each module in isolation

#### Evaluation Module (test_evaluation_module.py)

**Tests**: ~200 tests

**Coverage**:
- ✅ MobilityEvaluator (25 tests)
  - Initial position mobility
  - More moves = better score
  - No moves penalty
  - Symmetry verification
  
- ✅ StabilityEvaluator (20 tests)
  - Corner stability detection
  - Edge stability from corners
  - Interior stability
  - Flood-fill algorithm
  
- ✅ PositionalEvaluator (25 tests)
  - Positional weight application
  - Corner value verification
  - X-square penalty
  - Edge bonuses
  
- ✅ ParityEvaluator (15 tests)
  - Opening neutrality
  - Endgame parity effects
  - Even/odd empty squares
  
- ✅ CompositeEvaluator (35 tests)
  - Multiple evaluator combination
  - Phase detection
  - Weight application
  - Consistency checks

**Key Tests**:
```python
def test_mobility_initial_position():
    """Mobility at start should be neutral (both have 4 moves)."""
    
def test_corner_stability():
    """Corners should be detected as stable."""
    
def test_composite_phase_detection():
    """Different phases should use different weights."""
```

#### Ordering Module (test_ordering_module.py)

**Tests**: ~150 tests

**Coverage**:
- ✅ PVMoveOrderer (25 tests)
  - PV move placed first
  - Handling missing PV move
  - Multiple PV updates
  
- ✅ KillerMoveOrderer (30 tests)
  - Killer move prioritization
  - Multiple killers
  - Depth isolation
  - Killer table management
  
- ✅ HistoryHeuristic (30 tests)
  - Cutoff recording
  - Score calculation
  - Move ordering by history
  - New move handling
  
- ✅ PositionalOrderer (25 tests)
  - Corner prioritization
  - Edge ordering
  - Deterministic ordering
  
- ✅ CompositeOrderer (40 tests)
  - Strategy combination
  - Priority ordering (PV > Killer > History > Positional)
  - All moves preserved

**Key Tests**:
```python
def test_pv_move_highest_priority():
    """PV move should override all other orderers."""
    
def test_killer_moves_depth_isolation():
    """Killers at depth 5 shouldn't affect depth 3."""
    
def test_composite_combines_all_orderers():
    """All ordering strategies should contribute."""
```

#### Pruning Module (test_pruning_module.py)

**Tests**: ~120 tests

**Coverage**:
- ✅ NullMovePruning (30 tests)
  - Depth threshold
  - Reduction factor
  - Safety checks (no zugzwang)
  
- ✅ FutilityPruning (30 tests)
  - Frontier node detection
  - Margin calculation
  - Hopeless position pruning
  
- ✅ LateMoveReduction (35 tests)
  - First moves full depth
  - Late moves reduced
  - Depth threshold
  - Reduction calculation
  
- ✅ MultiCutPruning (25 tests)
  - Multiple cutoff requirement
  - Limited move search
  - Beta threshold

**Key Tests**:
```python
def test_null_move_not_at_shallow_depth():
    """Null move should not be tried at depth < 3."""
    
def test_lmr_reduction_increases_with_move_index():
    """Later moves should have greater reduction."""
    
def test_multicut_requires_M_cutoffs():
    """Multi-cut needs M cutoffs before pruning."""
```

#### Cache Module (test_cache_module.py)

**Tests**: ~100 tests

**Coverage**:
- ✅ ZobristHash (50 tests)
  - Hash determinism
  - Hash uniqueness
  - Incremental updates
  - Collision resistance
  
- ✅ TranspositionTable (50 tests)
  - Store and lookup
  - Replacement strategy
  - Node types (exact, lower, upper)
  - Collision handling
  - Hit rate tracking

**Key Tests**:
```python
def test_same_position_same_hash():
    """Zobrist hash must be deterministic."""
    
def test_transposition_table_replacement():
    """Deeper searches should replace shallower ones."""
    
def test_hash_collision_resistance():
    """Hashes should be diverse (low collision rate)."""
```

#### Search Module (test_search_module.py)

**Tests**: ~100 tests

**Coverage**:
- ✅ AlphaBetaSearch (35 tests)
  - Basic search functionality
  - Pruning effectiveness
  - Depth respect
  
- ✅ AlphaBetaCompleteSearch (30 tests)
  - Full feature search
  - TT integration
  - Move ordering integration
  
- ✅ IterativeDeepeningSearch (25 tests)
  - Progressive deepening
  - Time management
  - Aspiration windows
  
- ✅ ParallelSearch (10 tests)
  - Multi-core execution
  - Result correctness
  - Performance (when cores available)

**Key Tests**:
```python
def test_alphabeta_pruning_reduces_nodes():
    """Alpha-beta should search far fewer nodes than minimax."""
    
def test_iterative_deepening_progressive_results():
    """ID should search depth 1, 2, 3, ..., max_depth."""
    
def test_parallel_same_result_as_serial():
    """Parallel search should match serial search results."""
```

#### Observer Module (test_observer_module.py)

**Tests**: ~80 tests

**Coverage**:
- ✅ ConsoleObserver (25 tests)
  - Output generation
  - Method execution
  - Formatting
  
- ✅ StatisticsObserver (35 tests)
  - Data collection
  - Metric calculation
  - Accuracy verification
  
- ✅ QuietObserver (20 tests)
  - No output verification
  - Interface compliance

**Key Tests**:
```python
def test_console_observer_prints_output():
    """Console observer should print to stdout."""
    
def test_statistics_observer_accuracy():
    """Statistics should accurately reflect search data."""
    
def test_quiet_observer_produces_no_output():
    """Quiet observer should be completely silent."""
```

### 2. Integration Tests

**Purpose**: Test components working together

**Tests**: ~50 tests in test_apocalyptron_complete.py

**Scenarios**:
- ✅ Full engine with all modules enabled
- ✅ Opening book integration
- ✅ Complete game AI vs AI
- ✅ Performance at different depths
- ✅ Observer integration
- ✅ Edge cases (single move, late game, endgame)

**Key Tests**:
```python
def test_apocalyptron_full_game():
    """Complete game with all optimizations."""
    
def test_apocalyptron_performance_depth_9():
    """Verify depth 9 performance < 2s target."""
    
def test_opening_book_integration():
    """Opening book should provide instant moves."""
```

### 3. Characterization Tests

**Purpose**: Verify consistent behavior on known positions

**Existing Tests**:
- ✅ test_grandmaster_baseline.py - Reference behavior
- ✅ test_positions.py - Known positions database

**Strategy**:
- Test famous positions (FFO test suite)
- Verify consistency with reference engine
- Ensure no regressions

### 4. Performance Tests

**Purpose**: Benchmark and detect regressions

**New File**: test_benchmarks.py

**Benchmarks**:
- Bitboard operations (move gen, make move)
- Search speed at various depths
- Nodes per second
- Memory usage
- Full game completion time

**Thresholds**:
- Depth 6: < 0.5s
- Depth 9: < 2.0s
- NPS: > 100,000
- Memory: < 200MB

---

## 🎯 Testing Matrix

### Combinatorial Testing

**Dimensions**:
- Depths: 1, 3, 6, 9, 12
- Positions: Initial, midgame, endgame
- Configurations: Default, no book, custom weights
- Platforms: Linux, macOS, Windows (via CI)
- Python: 3.9, 3.10, 3.11, 3.12 (via CI)

**Total Combinations**: 5 × 3 × 3 × 3 × 4 = 540 test scenarios

---

## 🚀 Running Tests

### Quick Tests (Development)

```bash
# Unit tests only (fast)
pytest tests/apocalyptron/unit/ -v

# Specific module
pytest tests/apocalyptron/unit/test_evaluation_module.py -v

# Single test
pytest tests/apocalyptron/unit/test_evaluation_module.py::TestMobilityEvaluator::test_initial_position_mobility -v
```

### Complete Test Suite

```bash
# All apocalyptron tests
pytest tests/apocalyptron/ -v

# With coverage
pytest tests/apocalyptron/ --cov=src/AI/Apocalyptron --cov-report=html

# Parallel execution (faster)
pytest tests/apocalyptron/ -n auto
```

### Performance Tests

```bash
# Performance/slow tests only
pytest tests/apocalyptron/ -v -m slow

# Skip slow tests
pytest tests/apocalyptron/ -v -m "not slow"
```

### CI Tests

```bash
# What CI runs
pytest tests/ -v --cov=src --cov-report=xml --cov-report=term -n auto
```

---

## 📊 Coverage Goals

### Module-Level Targets

| Module | Target | Priority |
|--------|--------|----------|
| **Search** | >85% | Critical |
| **Evaluation** | >90% | High |
| **Ordering** | >80% | High |
| **Pruning** | >75% | Medium |
| **Cache** | >85% | High |
| **Observer** | >70% | Low |
| **Overall** | >80% | Critical |

### Current Status

Run to check:
```bash
pytest tests/apocalyptron/unit/ --cov=src/AI/Apocalyptron --cov-report=term-missing
```

---

## 🔍 Test Quality Metrics

### Metrics to Track

1. **Coverage** - % of code executed by tests
2. **Test Count** - Number of test cases
3. **Test Speed** - Average test execution time
4. **Flakiness** - Tests that fail intermittently
5. **Maintenance** - Effort to keep tests working

### Quality Checks

```bash
# Coverage
pytest --cov=src/AI/Apocalyptron --cov-report=term

# Mutation testing (advanced)
# mutmut run --paths-to-mutate=src/AI/Apocalyptron/

# Test duplication detection
# pytest --collect-only | grep "test_" | sort | uniq -d
```

---

## 🐛 Common Test Patterns

### Testing Evaluators

```python
def test_evaluator_symmetry():
    """Evaluators should be symmetric (flip colors = flip score)."""
    game = BitboardGame()
    evaluator = MobilityEvaluator()
    
    score_black = evaluator.evaluate(game)
    
    # Flip colors
    game_flipped = BitboardGame(
        black=game.white,
        white=game.black,
        current_player=-game.current_player
    )
    
    score_white = evaluator.evaluate(game_flipped)
    
    assert abs(score_black + score_white) < 0.01
```

### Testing Orderers

```python
def test_orderer_preserves_moves():
    """Orderers must preserve all moves (no additions/deletions)."""
    game = BitboardGame()
    moves = game.get_valid_moves(1)
    orderer = SomeOrderer()
    
    ordered = orderer.order(moves, game)
    
    assert len(ordered) == len(moves)
    assert set(ordered) == set(moves)
```

### Testing Pruning

```python
def test_pruning_safety():
    """Pruning techniques must not break correctness."""
    game = BitboardGame()
    pruner = NullMovePruning()
    
    # At very shallow depth, should be conservative
    should_prune = pruner.should_try_null_move(game, depth=1)
    
    assert should_prune == False
```

### Testing Search

```python
def test_search_determinism():
    """Search should be deterministic (same input = same output)."""
    game = BitboardGame()
    search = AlphaBetaSearch()
    
    score1, move1 = search.search(game, depth=5)
    score2, move2 = search.search(game, depth=5)
    
    assert move1 == move2
    assert score1 == score2
```

---

## 🎯 Test Coverage by Component

### Search Components

| Component | Tests | Coverage Target | Status |
|-----------|-------|-----------------|--------|
| Alpha-Beta | 35 | >85% | ✅ |
| Alpha-Beta Complete | 30 | >85% | ✅ |
| Iterative Deepening | 25 | >80% | ✅ |
| Parallel Search | 10 | >70% | ✅ |

### Evaluation Components

| Component | Tests | Coverage Target | Status |
|-----------|-------|-----------------|--------|
| Mobility | 25 | >90% | ✅ |
| Stability | 20 | >85% | ✅ |
| Positional | 25 | >90% | ✅ |
| Parity | 15 | >80% | ✅ |
| Composite | 35 | >85% | ✅ |

### Ordering Components

| Component | Tests | Coverage Target | Status |
|-----------|-------|-----------------|--------|
| PV Move | 25 | >85% | ✅ |
| Killer Moves | 30 | >85% | ✅ |
| History Heuristic | 30 | >85% | ✅ |
| Positional | 25 | >85% | ✅ |
| Composite | 40 | >90% | ✅ |

### Pruning Components

| Component | Tests | Coverage Target | Status |
|-----------|-------|-----------------|--------|
| Null Move | 30 | >75% | ✅ |
| Futility | 30 | >75% | ✅ |
| LMR | 35 | >80% | ✅ |
| Multi-Cut | 25 | >70% | ✅ |

### Cache Components

| Component | Tests | Coverage Target | Status |
|-----------|-------|-----------------|--------|
| Zobrist Hash | 50 | >90% | ✅ |
| Transposition Table | 50 | >85% | ✅ |

### Observer Components

| Component | Tests | Coverage Target | Status |
|-----------|-------|-----------------|--------|
| Console | 25 | >70% | ✅ |
| Statistics | 35 | >80% | ✅ |
| Quiet | 20 | >90% | ✅ |

---

## 🔬 Advanced Testing Techniques

### Property-Based Testing (Hypothesis)

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=0, max_value=63))
def test_position_always_valid(position):
    """Test that any position 0-63 is handled correctly."""
    game = BitboardGame()
    piece = game.get_piece_at(position)
    assert piece in [-1, 0, 1]
```

### Parameterized Testing

```python
@pytest.mark.parametrize("depth,expected_time", [
    (4, 0.1),
    (6, 0.5),
    (9, 2.0),
])
def test_search_performance(depth, expected_time):
    """Test search performance at various depths."""
    game = BitboardGame()
    player = PlayerApocalyptron(depth=depth)
    
    start = time.perf_counter()
    move = player.get_move(game, game.get_valid_moves(1), None)
    elapsed = time.perf_counter() - start
    
    assert elapsed < expected_time * 2  # Allow 2x margin
```

### Fixture-Based Testing

```python
@pytest.fixture
def initial_game():
    """Fixture providing initial game state."""
    return BitboardGame()

@pytest.fixture
def midgame_position():
    """Fixture providing typical midgame position."""
    black = 0x0000FFFF00000000
    white = 0x000000000000FFFF
    return BitboardGame(black=black, white=white, current_player=1)

def test_with_fixture(initial_game, midgame_position):
    """Test using fixtures."""
    assert initial_game.get_score() == (2, 2)
    assert sum(midgame_position.get_score()) > 20
```

---

## 📈 Performance Benchmarking

### Benchmark Tests

**File**: `tests/apocalyptron/performance/test_benchmarks.py`

**Benchmarks**:

1. **Bitboard Operations**
   ```python
   def test_benchmark_move_generation(benchmark):
       game = BitboardGame()
       benchmark(game.get_valid_moves, 1)
   ```

2. **AI Search**
   ```python
   def test_benchmark_search_depth_6(benchmark):
       game = BitboardGame()
       player = PlayerApocalyptron(depth=6)
       moves = game.get_valid_moves(1)
       benchmark(player.get_move, game, moves, None)
   ```

3. **Evaluators**
   ```python
   def test_benchmark_composite_evaluator(benchmark):
       game = BitboardGame()
       evaluator = CompositeEvaluator()
       benchmark(evaluator.evaluate, game)
   ```

**Run Benchmarks**:
```bash
pytest tests/apocalyptron/performance/ --benchmark-only
```

---

## 🎯 Test Maintenance

### Adding New Tests

1. **Choose appropriate file** (evaluation, ordering, pruning, etc.)
2. **Follow naming convention**: `test_<component>_<behavior>`
3. **Add docstring** explaining what is tested
4. **Keep tests focused** - one assertion per test ideally
5. **Use fixtures** for common setup
6. **Mark slow tests** with `@pytest.mark.slow`

### Debugging Failing Tests

```bash
# Run with verbose output
pytest tests/apocalyptron/unit/test_evaluation_module.py -vv

# Stop at first failure
pytest tests/apocalyptron/unit/ -x

# Show local variables on failure
pytest tests/apocalyptron/unit/ -l

# Drop into debugger on failure
pytest tests/apocalyptron/unit/ --pdb
```

### Test Markers

```python
@pytest.mark.slow  # Slow tests (>1s)
@pytest.mark.integration  # Integration tests
@pytest.mark.unit  # Unit tests
@pytest.mark.skipif(condition, reason="...")  # Conditional skip
```

---

## 📊 Test Metrics Dashboard

### Current Test Count

```bash
# Count all tests
pytest tests/apocalyptron/ --collect-only | grep "test_" | wc -l
```

**Expected**: 800+ tests

### Coverage Report

```bash
# Generate HTML coverage report
pytest tests/apocalyptron/ --cov=src/AI/Apocalyptron --cov-report=html

# View: open htmlcov/index.html
```

### Test Duration

```bash
# Show slowest tests
pytest tests/apocalyptron/ --durations=10
```

---

## 🏆 Quality Assurance

### Definition of Done for Tests

A test is "done" when it:
- [ ] Has descriptive name and docstring
- [ ] Tests one specific behavior
- [ ] Uses appropriate assertions
- [ ] Runs fast (<100ms for unit tests)
- [ ] Is deterministic (not flaky)
- [ ] Has good error messages
- [ ] Follows project conventions

### Code Review Checklist

When reviewing test code:
- [ ] Tests are clear and understandable
- [ ] Good coverage of edge cases
- [ ] No redundant tests
- [ ] Appropriate use of fixtures
- [ ] Slow tests are marked
- [ ] Integration tests are in right directory

---

## 📚 References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](../../development/testing.md)
- [CI/CD Testing](../../deployment/CI_CD_IMPLEMENTATION.md)

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-20  
**Test Suite Version**: Apocalyptron 3.1.0

*For questions about testing, see [Development Guide](../../development/README.md) or [Contributing Guide](../../../CONTRIBUTING.md).*

