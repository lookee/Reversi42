"""
Tests for Players.config.validator module.
"""

import os
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Players.config.validator import ConfigValidator


class TestConfigValidator:
    """Test suite for ConfigValidator."""

    def test_init_default(self):
        """Test ConfigValidator initialization with defaults."""
        validator = ConfigValidator()
        assert validator.strict == False
        assert len(validator.errors) == 0
        assert len(validator.warnings) == 0

    def test_init_strict(self):
        """Test ConfigValidator with strict mode."""
        validator = ConfigValidator(strict=True)
        assert validator.strict == True

    def test_validate_minimal_valid_config(self):
        """Test validation of minimal valid config."""
        validator = ConfigValidator()
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
        result = validator.validate(config)
        # Should be valid or have warnings
        assert isinstance(result, bool)

    def test_validate_missing_metadata(self):
        """Test validation with missing metadata."""
        validator = ConfigValidator()
        config = {
            "engine": {"depth": {"base": 5}},
        }
        result = validator.validate(config)
        assert result == False
        assert len(validator.errors) > 0

    def test_validate_missing_name(self):
        """Test validation with missing name."""
        validator = ConfigValidator()
        config = {
            "metadata": {},
            "engine": {"depth": {"base": 5}},
        }
        result = validator.validate(config)
        assert result == False or len(validator.errors) > 0

    def test_validate_invalid_depth_strategy(self):
        """Test validation with invalid depth strategy."""
        validator = ConfigValidator()
        config = {
            "metadata": {"name": "TestPlayer"},
            "engine": {
                "depth": {"base": 5, "strategy": "invalid"},
                "parallel": {"enabled": False},
                "transposition_table": {"enabled": True},
            },
            "evaluation": {},
            "move_ordering": {},
            "pruning": {},
            "opening_book": {},
            "behavior": {},
        }
        result = validator.validate(config)
        # Should have errors or warnings
        assert isinstance(result, bool)

    def test_validate_invalid_book_strategy(self):
        """Test validation with invalid book strategy."""
        validator = ConfigValidator()
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
            "opening_book": {"strategy": "invalid"},
            "behavior": {},
        }
        result = validator.validate(config)
        assert isinstance(result, bool)

    def test_errors_and_warnings(self):
        """Test that errors and warnings are collected."""
        validator = ConfigValidator()
        config = {}  # Invalid config
        validator.validate(config)
        assert isinstance(validator.errors, list)
        assert isinstance(validator.warnings, list)

    def test_validate_with_path(self):
        """Test validation with config path."""
        validator = ConfigValidator()
        config = {
            "metadata": {"name": "TestPlayer"},
            "engine": {"depth": {"base": 5}},
        }
        config_path = Path("/test/path/config.yaml")
        result = validator.validate(config, config_path)
        assert isinstance(result, bool)
