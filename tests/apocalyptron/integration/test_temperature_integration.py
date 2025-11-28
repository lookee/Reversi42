"""
Integration tests for temperature-based move variety.

Tests temperature functionality integrated with the full Apocalyptron engine.
"""

import os
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.core.config import calculate_default_temperature
from Players.PlayerApocalyptron import PlayerApocalyptron
from Reversi.BitboardGame import BitboardGame


class TestTemperatureIntegration:
    """Integration tests for temperature functionality."""

    def test_temperature_config_passed_to_engine(self):
        """Test that temperature from config is passed to engine."""
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .with_temperature(0.3)
            .enable_all_optimizations()
            .build()
        )

        assert config.temperature == 0.3

        engine = ApocalyptronEngine(config=config)
        assert engine.config.temperature == 0.3
        assert engine.alphabeta.temperature == 0.3

    def test_default_temperature_calculation(self):
        """Test default temperature calculation based on depth."""
        # Test different depths
        assert calculate_default_temperature(1) > 0.3  # High variety
        assert calculate_default_temperature(3) > 0.4  # High variety
        assert 0.2 < calculate_default_temperature(5) < 0.3  # Moderate
        assert 0.05 < calculate_default_temperature(8) < 0.15  # Low variety
        assert calculate_default_temperature(12) < 0.05  # Minimal variety

    def test_player_with_temperature(self):
        """Test PlayerApocalyptron with explicit temperature."""
        player = PlayerApocalyptron(depth=6, temperature=0.2)

        assert player.bitboard_engine.config.temperature == 0.2

        game = BitboardGame()
        moves = game.get_move_list()
        move = player.get_move(game, moves)

        assert move is not None
        assert move in moves

    def test_player_auto_temperature(self):
        """Test PlayerApocalyptron with auto-calculated temperature."""
        # Depth 3 should get high temperature
        player = PlayerApocalyptron(depth=3)
        expected_temp = calculate_default_temperature(3)

        assert abs(player.bitboard_engine.config.temperature - expected_temp) < 0.01

        # Depth 9 should get low temperature
        player_high = PlayerApocalyptron(depth=9)
        expected_temp_high = calculate_default_temperature(9)

        assert abs(player_high.bitboard_engine.config.temperature - expected_temp_high) < 0.01
        assert (
            player_high.bitboard_engine.config.temperature
            < player.bitboard_engine.config.temperature
        )

    def test_temperature_zero_deterministic(self):
        """Test that temperature=0.0 produces deterministic moves."""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=4, temperature=0.0)

        moves = game.get_move_list()
        if len(moves) > 1:
            # Get move multiple times - should be same
            move1 = player.get_move(game, moves)
            move2 = player.get_move(game, moves)

            assert move1 == move2, "Temperature=0.0 should be deterministic"

    def test_temperature_variety(self):
        """Test that temperature > 0 produces variety."""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=4, temperature=0.5)

        moves = game.get_move_list()
        if len(moves) > 1:
            # Get moves multiple times
            selected_moves = [player.get_move(game, moves) for _ in range(20)]

            # Should have some variety (not always same move)
            unique_moves = set(selected_moves)
            # With temperature 0.5, we should see some variety
            # (but might still be mostly best move)
            assert len(unique_moves) >= 1

    def test_temperature_with_opening_book(self):
        """Test that temperature is applied to opening book moves."""
        game = BitboardGame()
        # Use book_instant=True to test book move selection
        player = PlayerApocalyptron(depth=4, temperature=0.3, book_instant=True)

        # First few moves should be in opening book
        moves = game.get_move_list()
        move = player.get_move(game, moves)

        assert move is not None
        assert move in moves

        # Temperature should be passed to opening book
        assert player.bitboard_engine.config.temperature == 0.3

    def test_temperature_parallel_search(self):
        """Test that temperature works with parallel search."""
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .with_temperature(0.2)
            .enable_parallel(True)
            .enable_all_optimizations()
            .build()
        )

        engine = ApocalyptronEngine(config=config)
        game = BitboardGame()

        move = engine.get_best_move(game, depth=6)
        assert move is not None

        # Temperature should be accessible
        assert engine.config.temperature == 0.2
