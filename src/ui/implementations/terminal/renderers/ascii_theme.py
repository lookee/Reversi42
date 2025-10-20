"""
ASCII Theme System for Terminal

ANSI color configurations for terminal UI.
Similar to Pygame Theme but for terminal/console.

Design Pattern: Strategy (swappable color schemes)
"""

from dataclasses import dataclass
from typing import Optional


class ANSIColors:
    """ANSI escape codes for terminal colors"""

    # Reset
    RESET = "\033[0m"

    # Text attributes
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Bright background colors
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"


@dataclass
class ASCIIColorScheme:
    """Color scheme for terminal UI"""

    # Pieces
    black_piece: str
    white_piece: str
    empty_cell: str

    # Board elements
    board_border: str
    board_grid: str
    coordinates: str

    # Highlights
    valid_move: str
    last_move: str
    book_move: str

    # UI elements
    header_bg: str
    header_text: str
    score_text: str
    turn_indicator: str

    # Status messages
    info_text: str
    warning_text: str
    error_text: str

    # Use colors flag
    use_colors: bool = True


class ASCIITheme:
    """
    Theme presets for terminal UI.

    Similar to Pygame Theme but for terminal/console.
    """

    # Classic colored theme (default)
    CLASSIC = ASCIIColorScheme(
        # Pieces
        black_piece=f"{ANSIColors.BOLD}{ANSIColors.WHITE}●{ANSIColors.RESET}",
        white_piece=f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_BLACK}○{ANSIColors.RESET}",
        empty_cell=f"{ANSIColors.DIM}{ANSIColors.WHITE}·{ANSIColors.RESET}",
        # Board
        board_border=f"{ANSIColors.GREEN}",
        board_grid=f"{ANSIColors.GREEN}",
        coordinates=f"{ANSIColors.CYAN}",
        # Highlights
        valid_move=f"{ANSIColors.YELLOW}",
        last_move=f"{ANSIColors.BG_YELLOW}{ANSIColors.BLACK}",
        book_move=f"{ANSIColors.BRIGHT_YELLOW}",
        # UI
        header_bg=f"{ANSIColors.BG_GREEN}",
        header_text=f"{ANSIColors.BOLD}{ANSIColors.WHITE}",
        score_text=f"{ANSIColors.WHITE}",
        turn_indicator=f"{ANSIColors.BOLD}{ANSIColors.YELLOW}",
        # Messages
        info_text=f"{ANSIColors.CYAN}",
        warning_text=f"{ANSIColors.YELLOW}",
        error_text=f"{ANSIColors.RED}",
        use_colors=True,
    )

    # No-color theme (pure ASCII, works on any terminal)
    NO_COLOR = ASCIIColorScheme(
        # Pieces (pure symbols)
        black_piece="●",
        white_piece="○",
        empty_cell="·",
        # Board (no colors)
        board_border="",
        board_grid="",
        coordinates="",
        # Highlights (no colors)
        valid_move="",
        last_move="",
        book_move="",
        # UI (no colors)
        header_bg="",
        header_text="",
        score_text="",
        turn_indicator="",
        # Messages (no colors)
        info_text="",
        warning_text="",
        error_text="",
        use_colors=False,
    )

    # High contrast theme (accessibility)
    HIGH_CONTRAST = ASCIIColorScheme(
        # Pieces
        black_piece=f"{ANSIColors.BG_BLACK}{ANSIColors.BRIGHT_WHITE}●{ANSIColors.RESET}",
        white_piece=f"{ANSIColors.BG_WHITE}{ANSIColors.BLACK}○{ANSIColors.RESET}",
        empty_cell=f"{ANSIColors.DIM}{ANSIColors.WHITE}·{ANSIColors.RESET}",
        # Board
        board_border=f"{ANSIColors.BRIGHT_WHITE}",
        board_grid=f"{ANSIColors.BRIGHT_WHITE}",
        coordinates=f"{ANSIColors.BRIGHT_CYAN}",
        # Highlights
        valid_move=f"{ANSIColors.BG_BRIGHT_YELLOW}{ANSIColors.BLACK}",
        last_move=f"{ANSIColors.BG_BRIGHT_RED}{ANSIColors.WHITE}",
        book_move=f"{ANSIColors.BRIGHT_GREEN}",
        # UI
        header_bg=f"{ANSIColors.BG_BRIGHT_BLUE}",
        header_text=f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_WHITE}",
        score_text=f"{ANSIColors.BRIGHT_WHITE}",
        turn_indicator=f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_YELLOW}",
        # Messages
        info_text=f"{ANSIColors.BRIGHT_CYAN}",
        warning_text=f"{ANSIColors.BRIGHT_YELLOW}",
        error_text=f"{ANSIColors.BRIGHT_RED}",
        use_colors=True,
    )

    # Dark mode theme
    DARK_MODE = ASCIIColorScheme(
        # Pieces
        black_piece=f"{ANSIColors.BRIGHT_WHITE}●{ANSIColors.RESET}",
        white_piece=f"{ANSIColors.BRIGHT_BLACK}○{ANSIColors.RESET}",
        empty_cell=f"{ANSIColors.DIM}·{ANSIColors.RESET}",
        # Board
        board_border=f"{ANSIColors.BLUE}",
        board_grid=f"{ANSIColors.BLUE}",
        coordinates=f"{ANSIColors.BRIGHT_BLUE}",
        # Highlights
        valid_move=f"{ANSIColors.BRIGHT_CYAN}",
        last_move=f"{ANSIColors.BG_BLUE}{ANSIColors.BRIGHT_WHITE}",
        book_move=f"{ANSIColors.BRIGHT_YELLOW}",
        # UI
        header_bg=f"{ANSIColors.BG_BLUE}",
        header_text=f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_WHITE}",
        score_text=f"{ANSIColors.BRIGHT_WHITE}",
        turn_indicator=f"{ANSIColors.BOLD}{ANSIColors.BRIGHT_CYAN}",
        # Messages
        info_text=f"{ANSIColors.BRIGHT_BLUE}",
        warning_text=f"{ANSIColors.BRIGHT_YELLOW}",
        error_text=f"{ANSIColors.BRIGHT_RED}",
        use_colors=True,
    )
