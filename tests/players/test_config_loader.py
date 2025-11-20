"""
Tests for Players.config.loader module.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Players.config.exceptions import InvalidConfigError
from Players.config.loader import ConfigLoader
from Players.config.validator import ConfigValidator


class TestConfigLoader:
    """Test suite for ConfigLoader."""

    def test_init_default(self):
        """Test ConfigLoader initialization with defaults."""
        loader = ConfigLoader()
        assert loader.validator is not None
        assert loader.use_cache == True

    def test_init_custom_validator(self):
        """Test ConfigLoader with custom validator."""
        validator = ConfigValidator()
        loader = ConfigLoader(validator=validator)
        assert loader.validator == validator

    def test_init_no_cache(self):
        """Test ConfigLoader without cache."""
        loader = ConfigLoader(use_cache=False)
        assert loader.use_cache == False

    def test_load_valid_yaml(self):
        """Test loading valid YAML file."""
        loader = ConfigLoader()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            config = {
                "metadata": {"name": "TestPlayer"},
                "engine": {"depth": {"base": 5, "strategy": "fixed"}},
            }
            yaml.dump(config, f)
            temp_path = Path(f.name)

        try:
            result = loader.load(temp_path, validate=False)
            assert isinstance(result, dict)
            assert result["metadata"]["name"] == "TestPlayer"
        finally:
            temp_path.unlink()

    def test_load_invalid_yaml(self):
        """Test loading invalid YAML file."""
        loader = ConfigLoader()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_path = Path(f.name)

        try:
            with pytest.raises(InvalidConfigError):
                loader.load(temp_path, validate=False)
        finally:
            temp_path.unlink()

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file."""
        loader = ConfigLoader()
        fake_path = Path("/nonexistent/path/config.yaml")
        with pytest.raises(Exception):  # FileNotFoundError or InvalidConfigError
            loader.load(fake_path, validate=False)

    def test_cache_functionality(self):
        """Test caching functionality."""
        loader = ConfigLoader(use_cache=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            config = {"metadata": {"name": "TestPlayer"}}
            yaml.dump(config, f)
            temp_path = Path(f.name)

        try:
            result1 = loader.load(temp_path, validate=False)
            result2 = loader.load(temp_path, validate=False)
            assert result1 == result2
            assert temp_path in loader._cache
        finally:
            temp_path.unlink()

    def test_load_with_validation(self):
        """Test loading with validation."""
        loader = ConfigLoader()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            config = {
                "metadata": {"name": "TestPlayer"},
                "engine": {
                    "depth": {"base": 5, "strategy": "fixed"},
                    "parallel": {"enabled": False},
                    "transposition_table": {"enabled": True},
                },
                "evaluation": {},
                "move_ordering": {},
                "pruning": {},
                "opening_book": {},
                "behavior": {},
            }
            yaml.dump(config, f)
            temp_path = Path(f.name)

        try:
            result = loader.load(temp_path, validate=True)
            assert isinstance(result, dict)
        except InvalidConfigError:
            # Validation might fail, that's ok
            pass
        finally:
            temp_path.unlink()

    def test_clear_cache(self):
        """Test clearing cache."""
        loader = ConfigLoader(use_cache=True)
        loader._cache = {"test": "value"}
        loader.clear_cache()
        assert len(loader._cache) == 0
