# Performance Tests and Calibration

This directory contains optional performance tests for Reversi42. These tests are excluded from default test runs but can be executed explicitly for performance benchmarking and regression detection.

## Overview

Performance tests verify that the Apocalyptron AI engine meets performance expectations:
- Search speed at various depths
- Nodes per second (NPS) metrics
- Pruning effectiveness
- Transposition table hit rates

## Calibration System

The performance tests use a **calibration system** that adapts thresholds to your machine's hardware capabilities.

### How It Works

1. **Run Calibration**: Execute the calibration script to measure your machine's performance
2. **Save Baseline**: Results are saved to `.performance_baseline.json` (gitignored)
3. **Auto-Detection**: Tests automatically use calibrated thresholds if available
4. **Fallback**: If no baseline exists, tests use default thresholds

### Running Calibration

```bash
python scripts/calibrate_performance.py
```

This will:
- Run performance benchmarks multiple times
- Calculate average and minimum values
- Apply safety margins (70% for NPS, 150% for timing)
- Save thresholds to `tests/_performance/.performance_baseline.json`

**When to calibrate**:
- First time setting up on a new machine
- After hardware upgrades
- When performance tests fail unexpectedly
- To establish local performance baselines

### Running Performance Tests

**Locally** (with calibration):
```bash
# Run all performance tests
pytest tests/_performance/ -v

# Run specific test
pytest tests/_performance/apocalyptron/test_performance_benchmarks.py::TestPerformanceBaseline::test_initial_position_depth_6_speed -v
```

**In CI**:
Performance tests are automatically skipped in CI unless `RUN_PERFORMANCE_TESTS=1` is set:
```bash
RUN_PERFORMANCE_TESTS=1 pytest tests/_performance/ -v
```

## Test Structure

### Test Classes

- **TestPerformanceBaseline**: Basic performance benchmarks
- **TestNodesPerSecond**: NPS metrics and comparisons
- **TestOptimizationImpact**: Impact of optimizations
- **TestPruningPerformance**: Individual pruning techniques
- **TestTranspositionTablePerformance**: TT efficiency
- **TestPlayerApocalyptronPerformance**: Player-level performance
- **TestParallelPerformance**: Parallel search performance
- **TestRegressionPerformance**: Regression detection

### Threshold Types

- **max_elapsed**: Maximum allowed time for a search
- **min_nps**: Minimum nodes per second required

## Calibration File Format

The `.performance_baseline.json` file contains:

```json
{
  "calibration_date": "2025-01-20 10:30:00",
  "machine_info": {
    "platform": "darwin",
    "python_version": "3.11.0"
  },
  "raw_data": {
    "initial_position_depth_6": {
      "avg_elapsed": 1.23,
      "avg_nps": 1250,
      "min_nps": 1100,
      "max_nps": 1400,
      "avg_nodes": 1537,
      "runs": 3
    },
    ...
  },
  "thresholds": {
    "initial_position_depth_6": {
      "max_elapsed": 1.85,
      "min_nps": 770
    },
    ...
  }
}
```

## CI Behavior

In CI environments:
- Performance tests are **skipped by default** (non-blocking)
- Can be enabled with `RUN_PERFORMANCE_TESTS=1`
- When enabled, NPS assertions are relaxed (only verify > 0)
- Timing assertions use CI-adjusted multipliers

This ensures:
- ✅ CI pipeline remains stable
- ✅ Performance tests don't fail due to variable CI hardware
- ✅ Tests can still be run explicitly for monitoring

## Troubleshooting

### Tests fail with "NPS too low"

1. **Run calibration**: `python scripts/calibrate_performance.py`
2. **Re-run tests**: `pytest tests/_performance/ -v`
3. **Check baseline**: Verify `.performance_baseline.json` exists

### Tests fail with "elapsed time exceeded"

1. **Check system load**: Ensure no other heavy processes running
2. **Re-calibrate**: Run calibration again to update thresholds
3. **Check hardware**: Verify CPU performance hasn't degraded

### Baseline file not found

- This is normal if you haven't run calibration yet
- Tests will use default thresholds
- Run calibration to create machine-specific baseline

## Best Practices

1. **Calibrate regularly**: Re-run calibration after system changes
2. **Don't commit baseline**: The `.performance_baseline.json` file is gitignored
3. **Use in CI sparingly**: Only enable with `RUN_PERFORMANCE_TESTS=1` for monitoring
4. **Monitor trends**: Track performance over time to detect regressions

## Related Documentation

- [Performance Benchmarks](../../scripts/README.md#-calibrate_performancepy)
- [CI/CD Configuration](../../docs/ci-cd/README.md)
- [Apocalyptron Architecture](../../docs/architecture/apocalyptron-engine.md)

