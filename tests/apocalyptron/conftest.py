"""
Pytest configuration and fixtures for Apocalyptron tests.

Provides common fixtures and configuration for all Apocalyptron test suites.
"""

import os
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from AI.Apocalyptron.factory.factory import ApocalyptronFactory
from Reversi.BitboardGame import BitboardGame

# ==================== Fixtures ====================


@pytest.fixture
def initial_game():
    """
    Fixture providing a fresh initial game state.

    Returns:
        BitboardGame at starting position
    """
    return BitboardGame()


@pytest.fixture
def midgame_position():
    """
    Fixture providing a typical midgame position.

    Returns:
        BitboardGame with ~30 pieces on board
    """
    black = 0x0000FFFF00000000  # ~16 pieces
    white = 0x000000000000FFFF  # ~16 pieces
    return BitboardGame(black=black, white=white, current_player=1)


@pytest.fixture
def endgame_position():
    """
    Fixture providing a typical endgame position.

    Returns:
        BitboardGame with ~56+ pieces (8 empty squares)
    """
    black = 0xFFFFFFFF00000000  # ~32 pieces
    white = 0x00000000FFFFFFF0  # ~28 pieces, some empty
    return BitboardGame(black=black, white=white, current_player=1)


@pytest.fixture
def corner_position():
    """
    Fixture providing position with corners captured.

    Returns:
        BitboardGame with some corners owned
    """
    black = 0x0000000810000001  # Corner A1 + center
    white = 0x0000001008000000  # Center only
    return BitboardGame(black=black, white=white, current_player=1)


@pytest.fixture
def apocalyptron_config_default():
    """
    Fixture providing default Apocalyptron configuration.

    Returns:
        Default ApocalyptronConfig object
    """
    return ApocalyptronFactory.create_default_config(depth=6)


@pytest.fixture
def apocalyptron_config_fast():
    """
    Fixture providing fast Apocalyptron configuration for tests.

    Returns:
        Fast ApocalyptronConfig (depth 4, minimal features)
    """
    config = ApocalyptronFactory.create_default_config(depth=4)
    config.use_opening_book = False  # Faster for tests
    return config


@pytest.fixture
def apocalyptron_player_fast():
    """
    Fixture providing fast Apocalyptron player for integration tests.

    Returns:
        PlayerApocalyptron configured for fast testing
    """
    from src.Players.PlayerApocalyptron import PlayerApocalyptron

    return PlayerApocalyptron(depth=4)


@pytest.fixture
def apocalyptron_player_default():
    """
    Fixture providing default Apocalyptron player.

    Returns:
        PlayerApocalyptron with default settings (depth 6 for tests)
    """
    from src.Players.PlayerApocalyptron import PlayerApocalyptron

    return PlayerApocalyptron(depth=6)


# ==================== Test Configuration ====================


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "performance: marks tests as performance benchmarks")
    config.addinivalue_line("markers", "characterization: marks tests as characterization tests")


# ==================== Test Collection ====================


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers automatically.

    - Tests in unit/ directory get 'unit' marker
    - Tests in integration/ get 'integration' marker
    - Tests with 'benchmark' in name get 'performance' marker
    - Tests taking >1s get 'slow' marker (after first run)
    """
    for item in items:
        # Auto-mark by directory
        if "/unit/" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "/characterization/" in str(item.fspath):
            item.add_marker(pytest.mark.characterization)
        elif "/performance/" in str(item.fspath):
            item.add_marker(pytest.mark.performance)

        # Auto-mark slow tests by name
        if "performance" in item.name.lower() or "benchmark" in item.name.lower():
            item.add_marker(pytest.mark.slow)


# ==================== Helper Functions ====================


def assert_valid_move(game, move):
    """
    Helper to assert a move is valid.

    Args:
        game: BitboardGame instance
        move: Move position (0-63)

    Raises:
        AssertionError: If move is not valid
    """
    # BitboardGame.get_valid_moves() doesn't take parameters - it uses game.turn internally
    valid_moves = game.get_move_list()
    assert move in valid_moves, f"Move {move} not in valid moves {valid_moves}"


def assert_score_in_range(score, min_score=-10000, max_score=10000):
    """
    Helper to assert score is in reasonable range.

    Args:
        score: Evaluation score
        min_score: Minimum expected score
        max_score: Maximum expected score

    Raises:
        AssertionError: If score is out of range
    """
    assert min_score <= score <= max_score, f"Score {score} out of range [{min_score}, {max_score}]"


# ==================== Custom Assertions ====================


class ApocalyptronAssertions:
    """Custom assertions for Apocalyptron tests."""

    @staticmethod
    def assert_moves_preserved(original_moves, ordered_moves):
        """Assert that move ordering preserves all moves."""
        assert len(ordered_moves) == len(original_moves), "Move count should be preserved"
        assert set(ordered_moves) == set(original_moves), "Move set should be preserved"

    @staticmethod
    def assert_deterministic_search(search_fn, game, depth):
        """Assert that search is deterministic."""
        score1, move1 = search_fn(game, depth)
        score2, move2 = search_fn(game, depth)

        assert move1 == move2, "Search should be deterministic"
        assert abs(score1 - score2) < 0.01, "Scores should match"

    @staticmethod
    def assert_pruning_safe(pruner, game):
        """Assert that pruning doesn't break correctness."""
        # Pruning at depth 1 should be very conservative
        # (Implementation-specific, but generally true)
        pass  # Placeholder for custom checks


# Make helper available to all tests
@pytest.fixture
def apocalyptron_assertions():
    """Fixture providing custom assertions."""
    return ApocalyptronAssertions()


# ==================== Performance Tracking ====================


@pytest.fixture(scope="session")
def performance_tracker():
    """
    Session-scoped fixture for tracking performance across tests.

    Can be used to detect performance regressions.
    """

    class PerformanceTracker:
        def __init__(self):
            self.timings = {}

        def record(self, name, duration):
            """Record timing for a test."""
            if name not in self.timings:
                self.timings[name] = []
            self.timings[name].append(duration)

        def get_average(self, name):
            """Get average time for a test."""
            if name in self.timings and self.timings[name]:
                return sum(self.timings[name]) / len(self.timings[name])
            return None

    return PerformanceTracker()


# ==================== Cleanup ====================


@pytest.fixture(autouse=True)
def reset_singletons():
    """
    Auto-used fixture to reset any singleton state between tests.

    Ensures test isolation.
    """
    yield
    # Cleanup after test
    # (Add any singleton reset logic here if needed)
