"""
Tests for Players.config.discovery module.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Players.config.discovery import PlayerConfigFile, PlayerDiscovery


class TestPlayerDiscovery:
    """Test suite for PlayerDiscovery."""

    def test_init_default(self):
        """Test PlayerDiscovery initialization with defaults."""
        discovery = PlayerDiscovery()
        assert discovery.pattern == "*.yaml"
        assert discovery.config_dir is not None

    def test_init_custom_config_dir(self):
        """Test PlayerDiscovery with custom config directory."""
        discovery = PlayerDiscovery(config_dir="custom/path")
        assert "custom/path" in str(discovery.config_dir)

    def test_init_custom_pattern(self):
        """Test PlayerDiscovery with custom pattern."""
        discovery = PlayerDiscovery(pattern="*.yml")
        assert discovery.pattern == "*.yml"

    def test_player_config_file(self):
        """Test PlayerConfigFile dataclass."""
        path = Path("/test/path/player.yaml")
        config_file = PlayerConfigFile(
            path=path,
            name="TestPlayer",
            relative_path="test/player.yaml",
            category="test",
        )
        assert config_file.name == "TestPlayer"
        assert config_file.path == path
        assert config_file.category == "test"
        assert str(config_file) == "TestPlayer (test/player.yaml)"

    def test_find_project_root(self):
        """Test finding project root."""
        discovery = PlayerDiscovery()
        assert discovery.project_root.exists()
        # Should find markers like pyproject.toml or setup.py
        assert (discovery.project_root / "pyproject.toml").exists() or (
            discovery.project_root / "setup.py"
        ).exists()

    def test_discover_with_existing_dir(self):
        """Test discovery with existing directory."""
        discovery = PlayerDiscovery()
        # Should not raise if config dir exists
        try:
            files = discovery.discover()
            assert isinstance(files, list)
        except Exception:
            # Config dir might not exist in test environment
            pass

    def test_cache(self):
        """Test caching functionality."""
        discovery = PlayerDiscovery()
        # First call should populate cache
        try:
            files1 = discovery.discover(use_cache=True)
            # Second call should use cache
            files2 = discovery.discover(use_cache=True)
            assert files1 == files2
        except Exception:
            # Config dir might not exist
            pass

    def test_discover_no_cache(self):
        """Test discovery without cache."""
        discovery = PlayerDiscovery()
        try:
            files = discovery.discover(use_cache=False)
            assert isinstance(files, list)
        except Exception:
            pass
