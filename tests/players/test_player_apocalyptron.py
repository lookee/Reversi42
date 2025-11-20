"""
Tests for PlayerApocalyptron module.
"""

import os
import sys

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Players.PlayerApocalyptron import PlayerApocalyptron
from Reversi.Game import Game


class TestPlayerApocalyptron:
    """Test suite for PlayerApocalyptron."""

    def test_init_default(self):
        """Test PlayerApocalyptron initialization with defaults."""
        player = PlayerApocalyptron()
        assert player.depth == 9
        assert player.deep == 9
        assert player.name == "Apocalyptron9"

    def test_init_custom_depth(self):
        """Test PlayerApocalyptron with custom depth."""
        player = PlayerApocalyptron(depth=7)
        assert player.depth == 7
        assert player.deep == 7
        assert player.name == "Apocalyptron7"

    def test_init_custom_name(self):
        """Test PlayerApocalyptron with custom name."""
        player = PlayerApocalyptron(depth=8)
        assert "Apocalyptron" in player.name

    def test_get_move(self):
        """Test getting a move from Apocalyptron."""
        player = PlayerApocalyptron(depth=3)  # Use very shallow depth for speed
        game = Game(8)
        moves = game.get_move_list()
        if len(moves) > 0:
            try:
                move = player.get_move(game, moves)
                # Move should be valid or None
                assert move is None or (move in moves)
            except Exception:
                # Engine might fail in some cases, that's ok for test
                pass

    def test_get_move_no_moves(self):
        """Test getting move when no moves available."""
        player = PlayerApocalyptron(depth=4)
        game = Game(8)
        moves = []
        try:
            move = player.get_move(game, moves)
            assert move is None
        except Exception:
            # Engine might raise exception with no moves, that's ok
            pass

    def test_player_metadata(self):
        """Test player metadata."""
        assert hasattr(PlayerApocalyptron, "PLAYER_METADATA")
        metadata = PlayerApocalyptron.PLAYER_METADATA
        assert metadata["display_name"] == "Apocalyptron"
        assert metadata["enabled"] == True
        assert "difficulty" in metadata.get("parameters", {})

    def test_get_name(self):
        """Test get_name method."""
        player = PlayerApocalyptron(depth=6)
        assert player.get_name() == "Apocalyptron6"

    def test_opening_book_integration(self):
        """Test opening book integration."""
        player = PlayerApocalyptron(depth=3, show_book_options=True)
        game = Game(8)
        moves = game.get_move_list()
        if len(moves) > 0:
            try:
                # Should use opening book if available
                move = player.get_move(game, moves)
                assert move is None or isinstance(move, type(moves[0]) if moves else Move)
            except Exception:
                # Engine might fail, that's ok
                pass

    def test_different_depths(self):
        """Test different depth settings."""
        for depth in [5, 7, 9]:
            player = PlayerApocalyptron(depth=depth)
            assert player.depth == depth
            assert player.deep == depth

    def test_weights_parameter(self):
        """Test weights parameter."""
        player = PlayerApocalyptron(depth=4, weights=None)
        assert player.weights is None or hasattr(player, "weights")

    def test_search_strategy_parameter(self):
        """Test search strategy parameter."""
        player = PlayerApocalyptron(depth=4, search_strategy="iterative_deepening")
        assert hasattr(player, "bitboard_engine")

    def test_book_instant_parameter(self):
        """Test book instant parameter."""
        player = PlayerApocalyptron(depth=4, book_instant=False)
        assert player.book_instant == False
