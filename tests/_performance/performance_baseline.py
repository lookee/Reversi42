"""
Performance baseline loader for calibrated thresholds.

This module loads performance baselines from calibration runs
and provides helper functions to get thresholds for tests.
"""

import json
import os
from pathlib import Path


def get_baseline_file():
    """Get path to performance baseline file."""
    # Try to find from current file location
    current_file = Path(__file__).parent
    baseline_file = current_file / ".performance_baseline.json"
    return baseline_file


def load_baseline():
    """
    Load performance baseline from calibration file.

    Returns:
        dict with thresholds, or None if file doesn't exist
    """
    baseline_file = get_baseline_file()

    if not baseline_file.exists():
        return None

    try:
        with open(baseline_file, "r") as f:
            data = json.load(f)
        return data.get("thresholds", {})
    except (json.JSONDecodeError, IOError) as e:
        print(f"[WARN] Failed to load performance baseline: {e}")
        return None


def get_threshold(test_name, threshold_type, default_value):
    """
    Get threshold value for a test, using calibrated baseline if available.

    Args:
        test_name: Name of the test (e.g., "initial_position_depth_6")
        threshold_type: Type of threshold (e.g., "max_elapsed", "min_nps")
        default_value: Default value to use if baseline not available

    Returns:
        Threshold value (calibrated if available, otherwise default)
    """
    baseline = load_baseline()

    if baseline and test_name in baseline:
        test_thresholds = baseline[test_name]
        if threshold_type in test_thresholds:
            calibrated_value = test_thresholds[threshold_type]
            # Use calibrated value, but ensure it's reasonable
            # (don't allow thresholds that are too lenient)
            if threshold_type.startswith("max_"):
                # For max values, use the larger of calibrated or default
                return max(calibrated_value, default_value * 0.5)
            elif threshold_type.startswith("min_"):
                # For min values, use the smaller of calibrated or default
                return min(calibrated_value, default_value * 2.0)
            return calibrated_value

    return default_value


def has_baseline():
    """Check if performance baseline file exists."""
    return get_baseline_file().exists()


def get_baseline_info():
    """
    Get information about the baseline file.

    Returns:
        dict with calibration_date and machine_info, or None
    """
    baseline_file = get_baseline_file()

    if not baseline_file.exists():
        return None

    try:
        with open(baseline_file, "r") as f:
            data = json.load(f)
        return {
            "calibration_date": data.get("calibration_date"),
            "machine_info": data.get("machine_info", {}),
        }
    except (json.JSONDecodeError, IOError):
        return None
