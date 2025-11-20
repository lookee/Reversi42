"""
Tests for infrastructure.persistence.game_io module.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from infrastructure.persistence.game_io import GameIO


class MockGame:
    """Mock game for testing."""

    def __init__(self):
        self.turn = "B"
        self.black_cnt = 2
        self.white_cnt = 2
        self.size = 8
        self.matrix = [["." for _ in range(8)] for _ in range(8)]
        self.matrix[3][3] = "W"
        self.matrix[4][4] = "W"
        self.matrix[3][4] = "B"
        self.matrix[4][3] = "B"

    def export_str(self):
        """Export board as string."""
        result = []
        for row in self.matrix:
            result.extend(row)
        return "".join(result)


class TestGameIO:
    """Test suite for GameIO."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_saves_dir = None

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_get_saves_directory(self):
        """Test getting saves directory."""
        saves_dir = GameIO.get_saves_directory()
        assert os.path.exists(saves_dir)
        assert os.path.isdir(saves_dir)

    def test_save_game(self):
        """Test saving a game."""
        game = MockGame()
        filename = "test_game"
        black_player = "Player1"
        white_player = "Player2"
        move_history = "D3E3"

        filepath = GameIO.save_game(game, filename, black_player, white_player, move_history)
        assert os.path.exists(filepath)
        assert filepath.endswith(".xot")

    def test_save_game_creates_directory(self):
        """Test that save creates directory if needed."""
        game = MockGame()
        filepath = GameIO.save_game(game, "test", "Black", "White", "D3E3")
        assert os.path.exists(filepath)
        assert os.path.exists(os.path.dirname(filepath))

    def test_save_game_content(self):
        """Test saved game content."""
        game = MockGame()
        filename = "test_content"
        filepath = GameIO.save_game(game, filename, "Black", "White", "D3E3")

        with open(filepath, "r") as f:
            content = f.read()
            assert "Reversi42 Game Save" in content
            assert "Black=Black" in content
            assert "White=White" in content
            assert "History=D3E3" in content

    def test_load_game(self):
        """Test loading a game."""
        game = MockGame()
        filename = "test_load"
        filepath = GameIO.save_game(game, filename, "Black", "White", "D3E3")

        game_data = GameIO.load_game(filepath)
        assert game_data["black_player"] == "Black"
        assert game_data["white_player"] == "White"
        assert game_data["move_history"] == "D3E3"
        assert game_data["turn"] == "B"

    def test_load_game_relative_path(self):
        """Test loading game with relative path."""
        game = MockGame()
        filename = "test_relative"
        GameIO.save_game(game, filename, "Black", "White", "D3E3")

        # Load with just filename
        game_data = GameIO.load_game(filename + ".xot")
        assert game_data["black_player"] == "Black"

    def test_load_game_not_found(self):
        """Test loading non-existent game."""
        with pytest.raises(FileNotFoundError):
            GameIO.load_game("nonexistent.xot")

    def test_list_saved_games(self):
        """Test listing saved games."""
        game = MockGame()
        GameIO.save_game(game, "game1", "Black", "White", "D3E3")
        GameIO.save_game(game, "game2", "Black", "White", "D3E3")

        games = GameIO.list_saved_games()
        assert len(games) >= 2
        assert "game1.xot" in games or any("game1" in g for g in games)
        assert "game2.xot" in games or any("game2" in g for g in games)

    def test_list_saved_games_empty_directory(self):
        """Test listing games in empty directory."""
        # Use a temporary empty directory
        with tempfile.TemporaryDirectory() as temp_dir:
            games = GameIO.list_saved_games(temp_dir)
            assert games == []

    def test_list_saved_games_nonexistent_directory(self):
        """Test listing games in nonexistent directory."""
        games = GameIO.list_saved_games("/nonexistent/directory")
        assert games == []

    def test_save_game_metadata(self):
        """Test saving game with metadata."""
        game = MockGame()
        filepath = GameIO.save_game(game, "metadata_test", "Player1", "Player2", "D3E3")

        game_data = GameIO.load_game(filepath)
        assert game_data["black_score"] == 2
        assert game_data["white_score"] == 2
        assert game_data["size"] == 8

    def test_load_game_board_state(self):
        """Test loading game with board state."""
        game = MockGame()
        filepath = GameIO.save_game(game, "board_test", "Black", "White", "D3E3")

        game_data = GameIO.load_game(filepath)
        assert game_data["board_state"] is not None
        assert len(game_data["board_state"]) == 64  # 8x8 board

    def test_xot_version(self):
        """Test XOT version constant."""
        assert hasattr(GameIO, "XOT_VERSION")
        assert isinstance(GameIO.XOT_VERSION, str)
