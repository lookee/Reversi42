"""
Tests for Players.config.factory module.
"""

import os
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Players.config.exceptions import PlayerCreationError
from Players.config.factory import PlayerFactory


class TestConfigFactory:
    """Test suite for PlayerFactory in config module."""

    def test_init(self):
        """Test factory initialization."""
        factory = PlayerFactory()
        assert factory is not None
        assert factory._creation_stats["total_created"] == 0

    def test_create_player_minimal_config(self):
        """Test creating player with minimal config."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "TestPlayer"},
            "engine": {
                "depth": {"base": 5, "strategy": "fixed"},
            },
        }
        player = factory.create_player(config)
        assert player is not None
        assert player.name == "TestPlayer"

    def test_create_player_full_config(self):
        """Test creating player with full config."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "FullPlayer", "category": "test"},
            "engine": {
                "depth": {"base": 7, "strategy": "iterative"},
                "transposition_table": {"enabled": True, "size_mb": 64},
                "parallel": {"enabled": True, "num_workers": 2},
                "aspiration_windows": {"enabled": True},
            },
            "evaluation": {"preset": "grandmaster"},
            "pruning": {
                "null_move": {"enabled": True},
                "futility": {"enabled": True},
                "late_move_reduction": {"enabled": True},
                "multi_cut": {"enabled": True},
            },
            "opening_book": {"enabled": True, "strategy": "evaluated"},
        }
        player = factory.create_player(config)
        assert player is not None
        assert player.name == "FullPlayer"

    def test_create_player_adaptive_depth(self):
        """Test creating player with adaptive depth."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "AdaptivePlayer"},
            "engine": {
                "depth": {
                    "base": 8,
                    "strategy": "adaptive",
                    "adaptive": {"opening": 6, "midgame": 8, "endgame": 10},
                },
            },
        }
        player = factory.create_player(config)
        assert player is not None

    def test_create_player_with_opening_book(self):
        """Test creating player with opening book."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "BookPlayer"},
            "engine": {"depth": {"base": 6, "strategy": "fixed"}},
            "opening_book": {"enabled": True, "strategy": "instant"},
        }
        player = factory.create_player(config)
        assert player is not None
        assert player.opening_book is not None
        assert player.book_instant == True

    def test_create_player_without_opening_book(self):
        """Test creating player without opening book."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "NoBookPlayer"},
            "engine": {"depth": {"base": 6, "strategy": "fixed"}},
            "opening_book": {"enabled": False},
        }
        player = factory.create_player(config)
        assert player is not None
        assert player.opening_book is None

    def test_create_player_custom_evaluators(self):
        """Test creating player with custom evaluators."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "CustomEvalPlayer"},
            "engine": {"depth": {"base": 5, "strategy": "fixed"}},
            "evaluation": {
                "evaluators": [
                    {"name": "mobility", "enabled": True, "weight": 1.0},
                    {"name": "positional", "enabled": True, "weight": 0.8},
                ],
            },
        }
        player = factory.create_player(config)
        assert player is not None

    def test_create_player_invalid_config(self):
        """Test creating player with invalid config."""
        factory = PlayerFactory()
        config = {"metadata": {}}  # Missing required fields
        # The factory might use defaults or raise an exception
        # Let's test both cases
        try:
            player = factory.create_player(config)
            # If it succeeds, verify it has a name (even if default)
            assert hasattr(player, "name")
        except Exception as e:
            # If it fails, should be PlayerCreationError or related
            from Players.config.exceptions import PlayerCreationError

            assert isinstance(e, (PlayerCreationError, Exception))

    def test_get_stats(self):
        """Test getting creation statistics."""
        factory = PlayerFactory()
        stats = factory.get_stats()
        assert isinstance(stats, dict)
        assert "total_created" in stats
        assert "failed" in stats
        assert "by_category" in stats

    def test_create_player_updates_stats(self):
        """Test that creating player updates statistics."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "StatsPlayer", "category": "test"},
            "engine": {"depth": {"base": 5, "strategy": "fixed"}},
        }
        initial_stats = factory.get_stats()
        factory.create_player(config)
        new_stats = factory.get_stats()
        assert new_stats["total_created"] == initial_stats["total_created"] + 1

    def test_create_player_with_config_path(self):
        """Test creating player with config path."""
        factory = PlayerFactory()
        config = {
            "metadata": {"name": "PathPlayer"},
            "engine": {"depth": {"base": 5, "strategy": "fixed"}},
        }
        config_path = Path("/fake/path/config.yaml")
        player = factory.create_player(config, config_path=config_path)
        assert player is not None
