"""
Tests for BoardModel module.
"""

import os
import sys

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Board.BoardModel import BoardModel


class TestBoardModel:
    """Test suite for BoardModel."""

    def test_init(self):
        """Test BoardModel initialization."""
        model = BoardModel(8, 8)
        assert model.sizex == 8
        assert model.sizey == 8
        assert len(model.matrix) == 8
        assert len(model.matrix[0]) == 8

    def test_init_different_sizes(self):
        """Test BoardModel with different sizes."""
        model = BoardModel(10, 6)
        assert model.sizex == 10
        assert model.sizey == 6
        assert len(model.matrix) == 10
        assert len(model.matrix[0]) == 6

    def test_set_point(self):
        """Test setting a point."""
        model = BoardModel(8, 8)
        model.setPoint(3, 4, "B")
        assert model.getPoint(3, 4) == "B"

    def test_set_point_white(self):
        """Test setting white piece."""
        model = BoardModel(8, 8)
        model.setPoint(5, 5, "W")
        assert model.getPoint(5, 5) == "W"

    def test_get_point_default(self):
        """Test getting unset point returns 0."""
        model = BoardModel(8, 8)
        assert model.getPoint(0, 0) == 0

    def test_unset_point(self):
        """Test unsetting a point."""
        model = BoardModel(8, 8)
        model.setPoint(2, 3, "B")
        assert model.getPoint(2, 3) == "B"
        model.unsetPoint(2, 3)
        assert model.getPoint(2, 3) == 0

    def test_multiple_points(self):
        """Test setting multiple points."""
        model = BoardModel(8, 8)
        model.setPoint(0, 0, "B")
        model.setPoint(7, 7, "W")
        model.setPoint(3, 3, "B")
        assert model.getPoint(0, 0) == "B"
        assert model.getPoint(7, 7) == "W"
        assert model.getPoint(3, 3) == "B"
        assert model.getPoint(1, 1) == 0  # Unset point

    def test_set_point_overwrite(self):
        """Test overwriting a point."""
        model = BoardModel(8, 8)
        model.setPoint(4, 4, "B")
        assert model.getPoint(4, 4) == "B"
        model.setPoint(4, 4, "W")
        assert model.getPoint(4, 4) == "W"

    def test_boundary_points(self):
        """Test setting points at boundaries."""
        model = BoardModel(8, 8)
        model.setPoint(0, 0, "B")
        model.setPoint(7, 7, "W")
        model.setPoint(0, 7, "B")
        model.setPoint(7, 0, "W")
        assert model.getPoint(0, 0) == "B"
        assert model.getPoint(7, 7) == "W"
        assert model.getPoint(0, 7) == "B"
        assert model.getPoint(7, 0) == "W"
