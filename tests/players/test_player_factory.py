"""
Tests for PlayerFactory module.
"""

import os
import sys

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Board.BoardControl import BoardControl
from Players.PlayerFactory import PlayerFactory


class TestPlayerFactory:
    """Test suite for PlayerFactory."""

    def test_create_human_player(self):
        """Test creating human player."""
        board_control = BoardControl(8, 8)
        PlayerFactory.set_board_control(board_control)
        player = PlayerFactory.create_player("Human Player")
        assert player is not None
        assert hasattr(player, "get_move")

    def test_create_apocalyptron_player(self):
        """Test creating Apocalyptron player."""
        player = PlayerFactory.create_player("Apocalyptron")
        assert player is not None
        assert hasattr(player, "get_move")

    def test_create_apocalyptron_with_depth(self):
        """Test creating Apocalyptron with custom depth."""
        player = PlayerFactory.create_apocalyptron(depth=7)
        assert player is not None
        assert player.depth == 7

    def test_create_grandmaster(self):
        """Test creating Grandmaster (legacy alias)."""
        player = PlayerFactory.create_grandmaster(difficulty=8)
        assert player is not None

    def test_get_available_player_types(self):
        """Test getting available player types."""
        types = PlayerFactory.get_available_player_types()
        assert isinstance(types, list)
        assert "Human Player" in types or "Human" in types
        assert "Apocalyptron" in types

    def test_get_all_player_types(self):
        """Test getting all player types."""
        types = PlayerFactory.get_all_player_types()
        assert isinstance(types, list)
        assert len(types) > 0

    def test_create_player_invalid_type(self):
        """Test creating player with invalid type."""
        with pytest.raises(ValueError):
            PlayerFactory.create_player("InvalidPlayerType")

    def test_set_board_control(self):
        """Test setting board control."""
        board_control = BoardControl(8, 8)
        PlayerFactory.set_board_control(board_control)
        assert PlayerFactory._board_control == board_control

    def test_set_ui_type(self):
        """Test setting UI type."""
        PlayerFactory.set_ui_type("headless")
        assert PlayerFactory._ui_type == "headless"

    def test_get_player_metadata(self):
        """Test getting player metadata."""
        metadata = PlayerFactory.get_player_metadata("Apocalyptron")
        assert metadata is not None
        assert isinstance(metadata, dict)

    def test_get_player_metadata_invalid(self):
        """Test getting metadata for invalid player."""
        metadata = PlayerFactory.get_player_metadata("InvalidPlayer")
        assert metadata is None
