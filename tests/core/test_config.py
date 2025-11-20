"""
Tests for core.config module.
"""

import os
import sys

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from core.config import (
    BLACK,
    BLACK_CELL,
    BLACK_MOVE,
    EMPTY,
    ROWNAME,
    VERSION,
    VERSION_NAME,
    WHITE,
    WHITE_CELL,
    WHITE_MOVE,
    AIConfig,
    Colors,
    GameConfig,
    MenuConfig,
    OpeningBookConfig,
    Paths,
    TournamentConfig,
    UIConfig,
)


class TestGameConfig:
    """Test suite for GameConfig."""

    def test_board_size(self):
        """Test board size constant."""
        assert GameConfig.BOARD_SIZE == 8

    def test_initial_pieces(self):
        """Test initial pieces constant."""
        assert GameConfig.INITIAL_PIECES == 2

    def test_max_moves(self):
        """Test max moves constant."""
        assert GameConfig.MAX_MOVES == 60

    def test_default_players(self):
        """Test default player names."""
        assert GameConfig.DEFAULT_BLACK_PLAYER == "Human Player"
        assert GameConfig.DEFAULT_WHITE_PLAYER == "Apocalyptron"

    def test_default_depths(self):
        """Test default depths."""
        assert GameConfig.DEFAULT_BLACK_DEPTH == 5
        assert GameConfig.DEFAULT_WHITE_DEPTH == 9

    def test_opening_book_enabled(self):
        """Test opening book enabled flag."""
        assert GameConfig.OPENING_BOOK_ENABLED == True


class TestMenuConfig:
    """Test suite for MenuConfig."""

    def test_window_dimensions(self):
        """Test window dimensions."""
        assert MenuConfig.DEFAULT_WIDTH == 800
        assert MenuConfig.DEFAULT_HEIGHT == 600

    def test_colors(self):
        """Test color constants."""
        assert isinstance(MenuConfig.BG_COLOR, tuple)
        assert len(MenuConfig.BG_COLOR) == 3

    def test_font_sizes(self):
        """Test font size constants."""
        assert MenuConfig.TITLE_FONT_SIZE > 0
        assert MenuConfig.MENU_FONT_SIZE > 0

    def test_menu_items(self):
        """Test menu items list."""
        assert isinstance(MenuConfig.MENU_ITEMS, list)
        assert len(MenuConfig.MENU_ITEMS) > 0

    def test_difficulty_levels(self):
        """Test difficulty levels."""
        assert isinstance(MenuConfig.DIFFICULTY_LEVELS, list)
        assert len(MenuConfig.DIFFICULTY_LEVELS) > 0


class TestColors:
    """Test suite for Colors."""

    def test_board_colors(self):
        """Test board color constants."""
        assert isinstance(Colors.BOARD_BG, tuple)
        assert isinstance(Colors.BOARD_LINE, tuple)

    def test_piece_colors(self):
        """Test piece color constants."""
        assert isinstance(Colors.BLACK_PIECE, tuple)
        assert isinstance(Colors.WHITE_PIECE, tuple)

    def test_ui_colors(self):
        """Test UI color constants."""
        assert isinstance(Colors.GOLD, tuple)
        assert isinstance(Colors.MINT, tuple)


class TestUIConfig:
    """Test suite for UIConfig."""

    def test_window_settings(self):
        """Test window settings."""
        assert UIConfig.DEFAULT_WIDTH == 800
        assert UIConfig.DEFAULT_HEIGHT == 600
        assert UIConfig.MIN_WIDTH > 0
        assert UIConfig.MIN_HEIGHT > 0

    def test_header_height(self):
        """Test header height."""
        assert UIConfig.HEADER_HEIGHT > 0

    def test_font_sizes(self):
        """Test font size constants."""
        assert UIConfig.TITLE_FONT_SIZE > 0
        assert UIConfig.MENU_FONT_SIZE > 0


class TestAIConfig:
    """Test suite for AIConfig."""

    def test_depth_limits(self):
        """Test depth limits."""
        assert AIConfig.MIN_DEPTH >= 1
        assert AIConfig.MAX_DEPTH_STANDARD > AIConfig.MIN_DEPTH
        assert AIConfig.MAX_DEPTH_BITBOARD >= AIConfig.MAX_DEPTH_STANDARD

    def test_infinity_constants(self):
        """Test infinity constants."""
        assert AIConfig.INFINITY > 0
        assert AIConfig.NEG_INFINITY < 0

    def test_difficulty_levels(self):
        """Test difficulty levels."""
        assert isinstance(AIConfig.DIFFICULTY_LEVELS, list)
        assert len(AIConfig.DIFFICULTY_LEVELS) > 0


class TestOpeningBookConfig:
    """Test suite for OpeningBookConfig."""

    def test_default_book_path(self):
        """Test default book path."""
        assert isinstance(OpeningBookConfig.DEFAULT_BOOK_PATH, str)

    def test_display_settings(self):
        """Test display settings."""
        assert OpeningBookConfig.MAX_TOOLTIPS_SHOWN > 0
        assert isinstance(OpeningBookConfig.SHOW_OPENING_DEFAULT, bool)


class TestTournamentConfig:
    """Test suite for TournamentConfig."""

    def test_games_per_matchup(self):
        """Test games per matchup."""
        assert TournamentConfig.GAMES_PER_MATCHUP > 0

    def test_reports_dir(self):
        """Test reports directory."""
        assert isinstance(TournamentConfig.REPORTS_DIR, str)


class TestPaths:
    """Test suite for Paths."""

    def test_directories(self):
        """Test directory paths."""
        assert isinstance(Paths.SAVES_DIR, str)
        assert isinstance(Paths.BOOKS_DIR, str)

    def test_file_extension(self):
        """Test file extension."""
        assert Paths.SAVE_FILE_EXTENSION == ".xot"


class TestGameConstants:
    """Test suite for game constants."""

    def test_player_sides(self):
        """Test player side constants."""
        assert BLACK == "B"
        assert WHITE == "W"

    def test_cell_states(self):
        """Test cell state constants."""
        assert EMPTY == "."
        assert BLACK_CELL == "B"
        assert WHITE_CELL == "W"
        assert BLACK_MOVE == "b"
        assert WHITE_MOVE == "w"

    def test_row_name(self):
        """Test row name constant."""
        assert isinstance(ROWNAME, str)
        assert len(ROWNAME) > 0

    def test_version(self):
        """Test version constant."""
        assert isinstance(VERSION, str)
        assert len(VERSION) > 0

    def test_version_name(self):
        """Test version name constant."""
        assert isinstance(VERSION_NAME, str)
        assert len(VERSION_NAME) > 0
