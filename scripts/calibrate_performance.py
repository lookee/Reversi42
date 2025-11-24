#!/usr/bin/env python3
"""
Performance calibration script for Reversi42.

This script runs performance benchmarks to establish baseline thresholds
for the current machine. The results are saved to a JSON file that can
be used by performance tests to adapt to the hardware.

Usage:
    python scripts/calibrate_performance.py

The calibration file will be saved to:
    tests/_performance/.performance_baseline.json
"""

import json
import os
import sys
import time
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder
from AI.Apocalyptron.factory.factory import ApocalyptronFactory
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def run_calibration_test(name, test_func, runs=3):
    """
    Run a calibration test multiple times and return statistics.

    Args:
        name: Test name for logging
        test_func: Function that returns (elapsed_time, nps, nodes)
        runs: Number of runs to average

    Returns:
        dict with avg_elapsed, avg_nps, min_nps, max_nps, avg_nodes
    """
    print(f"  Running {name}...", end=" ", flush=True)

    elapsed_times = []
    nps_values = []
    nodes_values = []

    for i in range(runs):
        elapsed, nps, nodes = test_func()
        elapsed_times.append(elapsed)
        nps_values.append(nps)
        nodes_values.append(nodes)
        print(".", end="", flush=True)

    avg_elapsed = sum(elapsed_times) / len(elapsed_times)
    avg_nps = sum(nps_values) / len(nps_values)
    min_nps = min(nps_values)
    max_nps = max(nps_values)
    avg_nodes = sum(nodes_values) / len(nodes_values)

    print(f" Done ({avg_elapsed:.2f}s, {avg_nps:.0f} NPS)")

    return {
        "avg_elapsed": avg_elapsed,
        "avg_nps": avg_nps,
        "min_nps": min_nps,
        "max_nps": max_nps,
        "avg_nodes": avg_nodes,
        "runs": runs,
    }


def calibrate_initial_position_depth_6():
    """Calibrate depth 6 search from initial position."""

    def test():
        game = BitboardGame()
        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .enable_all_optimizations()
            .quiet_mode()
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=6)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nodes = stats["search_stats"]["nodes"]
        nps = nodes / elapsed if elapsed > 0 else 0

        return elapsed, nps, nodes

    return run_calibration_test("Initial position depth 6", test)


def calibrate_midgame_position_depth_8():
    """Calibrate depth 8 search from midgame position."""

    def test():
        game = BitboardGame()
        # Create midgame position
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6), Move(6, 6), Move(7, 6)]:
            if game.valid_move(m):
                game.move(m)

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(8)
            .enable_all_optimizations()
            .quiet_mode()
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=8)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nodes = stats["search_stats"]["nodes"]
        nps = nodes / elapsed if elapsed > 0 else 0

        return elapsed, nps, nodes

    return run_calibration_test("Midgame position depth 8", test)


def calibrate_depth_5_baseline():
    """Calibrate depth 5 baseline."""

    def test():
        game = BitboardGame()
        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)
            .enable_all_optimizations()
            .quiet_mode()
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=5)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nodes = stats["search_stats"]["nodes"]
        nps = nodes / elapsed if elapsed > 0 else 0

        return elapsed, nps, nodes

    return run_calibration_test("Depth 5 baseline", test)


def calibrate_nps_opening_vs_midgame():
    """Calibrate NPS comparison between opening and midgame."""

    def test_opening():
        game = BitboardGame()
        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)
            .enable_all_optimizations()
            .quiet_mode()
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        engine.get_best_move(game, depth=5)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nodes = stats["search_stats"]["nodes"]
        nps = nodes / elapsed if elapsed > 0 else 0

        return elapsed, nps, nodes

    def test_midgame():
        game = BitboardGame()
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6), Move(6, 6), Move(7, 6)]:
            if game.valid_move(m):
                game.move(m)

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)
            .enable_all_optimizations()
            .quiet_mode()
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        engine.get_best_move(game, depth=5)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nodes = stats["search_stats"]["nodes"]
        nps = nodes / elapsed if elapsed > 0 else 0

        return elapsed, nps, nodes

    opening = run_calibration_test("Opening NPS (depth 5)", test_opening)
    midgame = run_calibration_test("Midgame NPS (depth 5)", test_midgame)

    return {"opening": opening, "midgame": midgame}


def calculate_thresholds(calibration_data, safety_margin=0.7):
    """
    Calculate performance thresholds from calibration data.

    Args:
        calibration_data: Raw calibration results
        safety_margin: Multiplier for thresholds (0.7 = 70% of measured performance)

    Returns:
        dict with thresholds for each test
    """
    thresholds = {}

    # Depth 6 initial position
    if "initial_position_depth_6" in calibration_data:
        data = calibration_data["initial_position_depth_6"]
        thresholds["initial_position_depth_6"] = {
            "max_elapsed": data["avg_elapsed"] * 1.5,  # 50% margin for timing
            "min_nps": data["min_nps"] * safety_margin,  # 70% of minimum measured
        }

    # Depth 8 midgame
    if "midgame_position_depth_8" in calibration_data:
        data = calibration_data["midgame_position_depth_8"]
        thresholds["midgame_position_depth_8"] = {
            "max_elapsed": data["avg_elapsed"] * 1.5,
            "min_nps": data["min_nps"] * safety_margin,
        }

    # Depth 5 baseline
    if "depth_5_baseline" in calibration_data:
        data = calibration_data["depth_5_baseline"]
        thresholds["depth_5_baseline"] = {
            "max_elapsed": data["avg_elapsed"] * 1.5,
            "min_nps": data["min_nps"] * safety_margin,
        }

    # NPS opening vs midgame
    if "nps_opening_vs_midgame" in calibration_data:
        data = calibration_data["nps_opening_vs_midgame"]
        thresholds["nps_opening_vs_midgame"] = {
            "opening_min_nps": data["opening"]["min_nps"] * safety_margin,
            "midgame_min_nps": data["midgame"]["min_nps"] * safety_margin,
        }

    return thresholds


def main():
    """Run performance calibration and save results."""
    print("=" * 60)
    print("Performance Calibration for Reversi42")
    print("=" * 60)
    print("\nThis will run performance benchmarks to establish")
    print("baseline thresholds for this machine.")
    print("\nThis may take a few minutes...\n")

    calibration_data = {}

    # Run calibration tests
    print("Running calibration tests:")
    print("-" * 60)

    calibration_data["initial_position_depth_6"] = calibrate_initial_position_depth_6()
    calibration_data["midgame_position_depth_8"] = calibrate_midgame_position_depth_8()
    calibration_data["depth_5_baseline"] = calibrate_depth_5_baseline()
    calibration_data["nps_opening_vs_midgame"] = calibrate_nps_opening_vs_midgame()

    # Calculate thresholds
    print("\nCalculating thresholds...")
    thresholds = calculate_thresholds(calibration_data)

    # Prepare output
    output = {
        "calibration_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "machine_info": {
            "platform": sys.platform,
            "python_version": sys.version.split()[0],
        },
        "raw_data": calibration_data,
        "thresholds": thresholds,
    }

    # Save to file
    baseline_file = project_root / "tests" / "_performance" / ".performance_baseline.json"
    baseline_file.parent.mkdir(parents=True, exist_ok=True)

    with open(baseline_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nCalibration complete!")
    print(f"Results saved to: {baseline_file}")
    print("\nSummary:")
    print("-" * 60)
    for test_name, data in calibration_data.items():
        if isinstance(data, dict) and "avg_nps" in data:
            print(f"  {test_name}:")
            print(f"    Time: {data['avg_elapsed']:.2f}s")
            print(
                f"    NPS:  {data['min_nps']:.0f} - {data['max_nps']:.0f} (avg: {data['avg_nps']:.0f})"
            )
        elif isinstance(data, dict) and "opening" in data:
            print(f"  {test_name}:")
            print(f"    Opening NPS: {data['opening']['avg_nps']:.0f}")
            print(f"    Midgame NPS: {data['midgame']['avg_nps']:.0f}")

    print("\n" + "=" * 60)
    print("You can now run performance tests with calibrated thresholds:")
    print("  pytest tests/_performance/ -v")
    print("=" * 60)


if __name__ == "__main__":
    main()
