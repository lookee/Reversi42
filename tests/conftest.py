"""
Central pytest configuration for Reversi42 test suite.

Provides shared fixtures, helpers, and configuration for all tests.
"""

import os

import pytest

# ==================== CI Detection ====================

# Detect CI environment
IS_CI = os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

# CI-specific configuration
CI_TIMEOUT_MULTIPLIER = 2.0 if IS_CI else 1.0  # Double timeouts in CI
CI_NPS_THRESHOLD_MULTIPLIER = 0.3 if IS_CI else 1.0  # Much lower NPS threshold in CI


def skip_if_ci(reason: str = "Test skipped in CI environment"):
    """Skip test if running in CI environment."""
    return pytest.mark.skipif(IS_CI, reason=reason)


def skip_performance_assertions_in_ci():
    """
    Helper to determine if performance assertions should be skipped in CI.

    Returns:
        bool: True if performance assertions should be skipped
    """
    return IS_CI


def get_ci_nps_threshold(base_threshold: float) -> float:
    """
    Get NPS threshold adjusted for CI environment.

    Args:
        base_threshold: Base NPS threshold for local development

    Returns:
        Adjusted threshold for CI (much lower) or base threshold locally
    """
    return base_threshold * CI_NPS_THRESHOLD_MULTIPLIER


def get_ci_timeout(base_timeout: float) -> float:
    """
    Get timeout adjusted for CI environment.

    Args:
        base_timeout: Base timeout for local development

    Returns:
        Adjusted timeout for CI (longer) or base timeout locally
    """
    return base_timeout * CI_TIMEOUT_MULTIPLIER


# ==================== Pytest Configuration ====================


def pytest_configure(config):
    """Configure pytest with custom markers and CI detection."""
    # Register markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "performance: marks tests as performance benchmarks")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end test")
    config.addinivalue_line("markers", "ci_skip_performance: skip performance assertions in CI")

    # Print CI detection status
    if IS_CI:
        print("\n[CI] CI environment detected - performance thresholds will be relaxed")


def pytest_collection_modifyitems(config, items):  # pylint: disable=unused-argument
    """
    Modify test collection to handle CI-specific behavior.

    - Performance tests marked with 'ci_skip_performance' will have relaxed assertions in CI

    Args:
        config: pytest config object (required by pytest hook signature)
        items: list of test items to modify
    """
    for item in items:
        # Auto-mark performance tests
        if "/performance/" in str(item.fspath):
            item.add_marker(pytest.mark.performance)

        # Auto-mark slow tests by name
        if "performance" in item.name.lower() or "benchmark" in item.name.lower():
            item.add_marker(pytest.mark.slow)
