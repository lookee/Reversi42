"""
Tests for ViewFactory module.
"""

import os
import sys

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Board.ViewFactory import ViewFactory, create_headless_view


class TestViewFactory:
    """Test suite for ViewFactory."""

    def test_create_headless_view(self):
        """Test creating headless view."""
        view = ViewFactory.create_view("headless", 8, 8, 800, 600)
        assert view is not None
        assert view.sizex == 8
        assert view.sizey == 8

    def test_create_view_none(self):
        """Test creating view with 'none' type."""
        view = ViewFactory.create_view("none", 8, 8, 800, 600)
        assert view is not None

    def test_create_view_invalid_type(self):
        """Test creating view with invalid type."""
        with pytest.raises(ValueError):
            ViewFactory.create_view("invalid", 8, 8, 800, 600)

    def test_create_view_case_insensitive(self):
        """Test creating view with different case."""
        view = ViewFactory.create_view("HEADLESS", 8, 8, 800, 600)
        assert view is not None

    def test_get_available_views(self):
        """Test getting available views."""
        views = ViewFactory.get_available_views()
        assert "headless" in views
        assert "none" in views

    def test_create_view_custom_size(self):
        """Test creating view with custom size."""
        view = ViewFactory.create_view("headless", 10, 10, 1000, 1000)
        assert view.sizex == 10
        assert view.sizey == 10

    def test_create_headless_view_function(self):
        """Test convenience function."""
        view = create_headless_view(8, 8)
        assert view is not None
        assert view.sizex == 8
        assert view.sizey == 8
