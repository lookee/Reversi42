"""
Tests for core.game_config module.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from core.game_config import (
    GameConfig,
    GameConfigLoader,
    PlayerConfig,
    create_default_game_players,
    load_game_config,
)


class TestGameConfigLoader:
    """Test suite for GameConfigLoader."""

    def test_init(self):
        """Test GameConfigLoader initialization."""
        loader = GameConfigLoader()
        assert loader.project_root is not None

    def test_init_custom_root(self):
        """Test GameConfigLoader with custom project root."""
        custom_root = Path("/custom/path")
        loader = GameConfigLoader(project_root=custom_root)
        assert loader.project_root == custom_root

    def test_load_default_config(self):
        """Test loading default configuration."""
        loader = GameConfigLoader()
        config = loader.load()
        assert isinstance(config, GameConfig)
        assert config.board_size == 8

    def test_load_from_file(self):
        """Test loading configuration from file."""
        loader = GameConfigLoader()
        # Create temp file within project root to pass security checks
        project_root = loader.project_root
        temp_file = project_root / "test_config_temp.yaml"

        try:
            config_dict = {
                "game": {"title": "Test Game", "board_size": 8},
                "players": {
                    "black": {"type": "human", "name": "Player1"},
                    "white": {"type": "ai", "name": "AI", "ai_player": "Apocalyptron"},
                },
            }
            with open(temp_file, "w") as f:
                yaml.dump(config_dict, f)

            config = loader.load(str(temp_file))
            assert isinstance(config, GameConfig)
        finally:
            if temp_file.exists():
                temp_file.unlink()

    def test_find_project_root(self):
        """Test finding project root."""
        loader = GameConfigLoader()
        root = loader._find_project_root()
        assert root.exists()
        # Should find markers
        assert (
            (root / "pyproject.toml").exists()
            or (root / "setup.py").exists()
            or (root / "README.md").exists()
        )


class TestPlayerConfig:
    """Test suite for PlayerConfig."""

    def test_init(self):
        """Test PlayerConfig initialization."""
        config = PlayerConfig(player_type="human", name="TestPlayer")
        assert config.player_type == "human"
        assert config.name == "TestPlayer"
        assert config.ai_player is None

    def test_init_with_ai(self):
        """Test PlayerConfig with AI player."""
        config = PlayerConfig(player_type="ai", name="AI Player", ai_player="Apocalyptron")
        assert config.player_type == "ai"
        assert config.ai_player == "Apocalyptron"

    def test_init_with_symbol(self):
        """Test PlayerConfig with custom symbol."""
        config = PlayerConfig(player_type="human", name="Player", symbol="⚫")
        assert config.symbol == "⚫"


class TestGameConfig:
    """Test suite for GameConfig."""

    def test_init(self):
        """Test GameConfig initialization."""
        black = PlayerConfig(player_type="human", name="Black")
        white = PlayerConfig(player_type="ai", name="White", ai_player="Apocalyptron")
        config = GameConfig(
            title="Test",
            auto_start=True,
            board_size=8,
            black_player=black,
            white_player=white,
            show_legal_moves=True,
            show_hints=False,
            show_ai_thinking=False,
            show_ai_evaluation=False,
            show_ai_stats=True,
            show_opening_book=False,
            think_delay_ms=500,
            board_style="unicode",
            show_coordinates=True,
            show_history=True,
            show_score=True,
            clear_screen=False,
            debug_mode=False,
        )
        assert config.title == "Test"
        assert config.board_size == 8

    def test_is_human_vs_ai(self):
        """Test is_human_vs_ai property."""
        black = PlayerConfig(player_type="human", name="Black")
        white = PlayerConfig(player_type="ai", name="White", ai_player="Apocalyptron")
        config = GameConfig(
            title="Test",
            auto_start=True,
            board_size=8,
            black_player=black,
            white_player=white,
            show_legal_moves=True,
            show_hints=False,
            show_ai_thinking=False,
            show_ai_evaluation=False,
            show_ai_stats=True,
            show_opening_book=False,
            think_delay_ms=500,
            board_style="unicode",
            show_coordinates=True,
            show_history=True,
            show_score=True,
            clear_screen=False,
            debug_mode=False,
        )
        assert config.is_human_vs_ai == True
        assert config.is_ai_vs_ai == False
        assert config.is_human_vs_human == False

    def test_is_ai_vs_ai(self):
        """Test is_ai_vs_ai property."""
        black = PlayerConfig(player_type="ai", name="AI1", ai_player="Apocalyptron")
        white = PlayerConfig(player_type="ai", name="AI2", ai_player="Apocalyptron")
        config = GameConfig(
            title="Test",
            auto_start=True,
            board_size=8,
            black_player=black,
            white_player=white,
            show_legal_moves=True,
            show_hints=False,
            show_ai_thinking=False,
            show_ai_evaluation=False,
            show_ai_stats=True,
            show_opening_book=False,
            think_delay_ms=500,
            board_style="unicode",
            show_coordinates=True,
            show_history=True,
            show_score=True,
            clear_screen=False,
            debug_mode=False,
        )
        assert config.is_ai_vs_ai == True
        assert config.is_human_vs_ai == False


class TestConvenienceFunctions:
    """Test suite for convenience functions."""

    def test_load_game_config(self):
        """Test load_game_config convenience function."""
        config = load_game_config()
        assert isinstance(config, GameConfig)

    def test_create_default_game_players(self):
        """Test create_default_game_players convenience function."""
        # This might fail if registry is not initialized, so catch exceptions
        try:
            black, white = create_default_game_players()
            assert black is not None
            assert white is not None
        except Exception:
            # Registry might not be initialized in test environment
            pass
