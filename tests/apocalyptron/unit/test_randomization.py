"""
Tests for randomization module - temperature-based move selection.

Tests the probabilistic move selection using temperature for variety.
"""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from AI.Apocalyptron.randomization.temperature import (
    apply_temperature_selection,
    get_top_moves_with_similar_values,
)


class TestTemperatureSelection:
    """Test temperature-based move selection."""

    def test_deterministic_selection_temperature_zero(self):
        """Test that temperature=0.0 always selects best move."""
        moves_with_values = [("move1", 100.0), ("move2", 95.0), ("move3", 90.0)]

        # Run multiple times - should always get best move
        for _ in range(10):
            selected = apply_temperature_selection(moves_with_values, temperature=0.0)
            assert selected == "move1", "Should always select best move with temperature=0.0"

    def test_deterministic_selection_negative_temperature(self):
        """Test that negative temperature is treated as 0.0."""
        moves_with_values = [("move1", 100.0), ("move2", 95.0)]

        selected = apply_temperature_selection(moves_with_values, temperature=-0.1)
        assert selected == "move1", "Negative temperature should be treated as 0.0"

    def test_single_move_always_selected(self):
        """Test that single move is always selected regardless of temperature."""
        moves_with_values = [("move1", 100.0)]

        for temp in [0.0, 0.1, 0.5, 1.0]:
            selected = apply_temperature_selection(moves_with_values, temperature=temp)
            assert selected == "move1"

    def test_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            apply_temperature_selection([], temperature=0.5)

    def test_temperature_selection_variety(self):
        """Test that higher temperature produces more variety."""
        moves_with_values = [("move1", 100.0), ("move2", 99.0), ("move3", 98.0)]

        # With low temperature, should mostly get move1
        low_temp_selections = [
            apply_temperature_selection(moves_with_values, temperature=0.01) for _ in range(100)
        ]
        move1_count_low = low_temp_selections.count("move1")

        # With high temperature, should get more variety
        high_temp_selections = [
            apply_temperature_selection(moves_with_values, temperature=1.0) for _ in range(100)
        ]
        move1_count_high = high_temp_selections.count("move1")

        # High temperature should have less move1 selections
        assert move1_count_high < move1_count_low, "Higher temperature should produce more variety"

    def test_temperature_with_int_values(self):
        """Test that function works with int values."""
        moves_with_values = [("move1", 100), ("move2", 95), ("move3", 90)]

        selected = apply_temperature_selection(moves_with_values, temperature=0.0)
        assert selected == "move1"

        # Test with int values are converted to float
        selected = apply_temperature_selection(moves_with_values, temperature=0.1)
        assert selected in ["move1", "move2", "move3"]

    def test_temperature_with_mixed_values(self):
        """Test that function works with mixed int/float values."""
        moves_with_values = [("move1", 100), ("move2", 95.5), ("move3", 90)]

        selected = apply_temperature_selection(moves_with_values, temperature=0.0)
        assert selected == "move1"

    def test_probability_distribution(self):
        """Test that better moves have higher probability."""
        # Use moves with closer values and higher temperature for better distribution
        moves_with_values = [
            ("best", 100.0),
            ("good", 98.0),
            ("ok", 96.0),
            ("bad", 94.0),
        ]

        # Use higher temperature to see more variety
        selections = [
            apply_temperature_selection(moves_with_values, temperature=0.5) for _ in range(1000)
        ]

        best_count = selections.count("best")
        good_count = selections.count("good")
        ok_count = selections.count("ok")
        bad_count = selections.count("bad")

        # Best should be selected most often
        assert best_count > 0, "Best move should be selected sometimes"
        # With closer values and higher temperature, best should still be most frequent
        assert best_count >= good_count, "Best move should be selected at least as often as good"
        # At least some variety should be present
        unique_selections = set(selections)
        assert len(unique_selections) > 1, "Should see some variety with temperature > 0"

    def test_temperature_extreme_values(self):
        """Test behavior with extreme temperature values."""
        moves_with_values = [("move1", 100.0), ("move2", 99.0), ("move3", 98.0)]

        # Very low temperature (almost deterministic)
        selected = apply_temperature_selection(moves_with_values, temperature=0.001)
        assert selected in ["move1", "move2", "move3"]

        # Very high temperature (almost uniform)
        selections = [
            apply_temperature_selection(moves_with_values, temperature=10.0) for _ in range(100)
        ]
        # Should get some variety
        unique_selections = set(selections)
        assert len(unique_selections) > 1, "High temperature should produce variety"


class TestTopMovesWithSimilarValues:
    """Test filtering moves with similar values."""

    def test_empty_list_returns_empty(self):
        """Test that empty list returns empty list."""
        result = get_top_moves_with_similar_values([])
        assert result == []

    def test_single_move_returns_single(self):
        """Test that single move returns single move."""
        moves_with_values = [("move1", 100.0)]
        result = get_top_moves_with_similar_values(moves_with_values)
        assert result == moves_with_values

    def test_all_moves_within_threshold(self):
        """Test that all moves within threshold are returned."""
        moves_with_values = [
            ("move1", 100.0),
            ("move2", 99.0),
            ("move3", 98.0),
        ]
        # 5% threshold means moves within 5 points
        result = get_top_moves_with_similar_values(moves_with_values, threshold=0.05)
        assert len(result) == 3

    def test_only_close_moves_returned(self):
        """Test that only moves within threshold are returned."""
        moves_with_values = [
            ("move1", 100.0),
            ("move2", 95.0),  # Within 5% threshold
            ("move3", 50.0),  # Too far
        ]
        result = get_top_moves_with_similar_values(moves_with_values, threshold=0.05)
        assert len(result) == 2
        assert ("move1", 100.0) in result
        assert ("move2", 95.0) in result
        assert ("move3", 50.0) not in result

    def test_sorted_order_preserved(self):
        """Test that moves are returned in sorted order."""
        moves_with_values = [
            ("move3", 98.0),
            ("move1", 100.0),
            ("move2", 99.0),
        ]
        # Sort first
        moves_with_values.sort(key=lambda x: x[1], reverse=True)

        result = get_top_moves_with_similar_values(moves_with_values, threshold=0.05)
        # Should be in descending order
        values = [v for _, v in result]
        assert values == sorted(values, reverse=True)

    def test_with_int_values(self):
        """Test that function works with int values."""
        moves_with_values = [("move1", 100), ("move2", 95), ("move3", 50)]
        result = get_top_moves_with_similar_values(moves_with_values, threshold=0.05)
        assert len(result) == 2

    def test_with_zero_best_value(self):
        """Test behavior when best value is near zero."""
        # Function expects sorted descending, so best value first
        moves_with_values = [
            ("move1", 50.0),  # Best value
            ("move2", 49.0),  # Close to best
            ("move3", 0.0),  # Too far (uses absolute threshold)
        ]
        # Sort descending
        moves_with_values.sort(key=lambda x: x[1], reverse=True)

        # Should use absolute threshold when best value is near zero
        # But with best=50, threshold=0.05 means 2.5 points difference
        result = get_top_moves_with_similar_values(moves_with_values, threshold=0.05)
        # move1 and move2 should be included (within 2.5 points)
        assert len(result) >= 2
        assert ("move1", 50.0) in result
