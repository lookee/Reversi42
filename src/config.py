"""
Reversi42 - Centralized Configuration
Version 3.0.0

All constants, defaults, and configuration values in one place.
"""

# ============================================================================
# GAME CONFIGURATION
# ============================================================================

class GameConfig:
    """Core game settings"""
    BOARD_SIZE = 8
    INITIAL_PIECES = 2
    MAX_MOVES = 60
    
    # Players
    DEFAULT_BLACK_PLAYER = "Human"
    DEFAULT_WHITE_PLAYER = "AI Bitboard with Book (Fastest)"
    DEFAULT_DEPTH = 5
    
    # Opening Book
    OPENING_BOOK_ENABLED = True
    OPENING_BOOK_PATH = 'Books/opening_book.txt'


# ============================================================================
# COLOR PALETTE
# ============================================================================

class Colors:
    """Centralized color definitions"""
    
    # Board colors
    BOARD_BG = (0, 95, 75)          # Rich forest green
    BOARD_LINE = (15, 55, 45)       # Dark teal lines
    BOARD_SHADOW = (25, 50, 40)     # Subtle shadow
    
    # Piece colors
    BLACK_PIECE = (15, 15, 20)      # Deep black
    WHITE_PIECE = (248, 248, 250)   # Soft white
    
    # UI Accent colors
    GOLD = (255, 215, 0)            # Gold for accents, cursor, book moves
    MINT = (180, 220, 190)          # Mint for possible moves
    MINT_LIGHT = (200, 230, 210)    # Light mint for white moves
    MINT_DARK = (160, 200, 170)     # Dark mint for black moves
    AMBER = (255, 180, 50)          # Amber for last move
    
    # Hoshi and grid
    HOSHI = (20, 70, 55)            # Subtle dark teal
    
    # Menu colors
    MENU_BG = (20, 50, 30)          # Dark green menu background
    MENU_TITLE = (255, 255, 255)    # White title
    MENU_TEXT = (200, 200, 200)     # Light gray text
    MENU_SELECTED = (255, 255, 0)   # Yellow selection
    MENU_HIGHLIGHT = (100, 150, 100) # Light green highlight
    
    # Header colors (tournament style)
    HEADER_BG = (0, 65, 50)         # Dark forest green
    HEADER_ACCENT = (0, 85, 65)     # Lighter green accent
    HEADER_TEXT = (230, 235, 230)   # Off-white text
    HEADER_LABEL = (160, 180, 170)  # Soft mint labels
    TURN_INDICATOR = (255, 215, 0)  # Gold dot for active player
    
    # Coordinates
    COORD_COLOR = (180, 200, 185)   # Soft mint for coords


# ============================================================================
# UI CONFIGURATION
# ============================================================================

class UIConfig:
    """UI dimensions and settings"""
    
    # Window settings
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    MIN_WIDTH = 400
    MIN_HEIGHT = 300
    
    # Header
    HEADER_HEIGHT = 80
    
    # Font sizes
    TITLE_FONT_SIZE = 64
    MENU_FONT_SIZE = 32
    SMALL_FONT_SIZE = 20
    PLAYER_NAME_FONT_SIZE = 28
    SCORE_FONT_SIZE = 52
    LABEL_FONT_SIZE = 20
    COORD_FONT_SIZE = 22
    OPENING_INFO_FONT_SIZE = 18
    
    # Spacing
    COORD_MARGIN = 25
    MENU_ITEM_SPACING = 50
    SUBMENU_ITEM_SPACING = 45
    
    # Opening Book UI
    OPENING_TOOLTIP_MARGIN = 15
    OPENING_TOOLTIP_PADDING = 12
    OPENING_MAX_DISPLAY = 6
    OPENING_BADGE_RADIUS = 10
    OPENING_BADGE_FONT_SIZE = 16


# ============================================================================
# AI CONFIGURATION  
# ============================================================================

class AIConfig:
    """AI engine settings"""
    
    # Search depth limits
    MIN_DEPTH = 1
    MAX_DEPTH_STANDARD = 10
    MAX_DEPTH_BITBOARD = 12
    DEFAULT_DEPTH = 5
    
    # Alpha-beta constants
    INFINITY = 10000
    NEG_INFINITY = -10000
    
    # Performance
    EXPECTED_BITBOARD_SPEEDUP = "50-100x"
    
    # Difficulty levels (for menu)
    DIFFICULTY_LEVELS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    DIFFICULTY_LEVELS_STANDARD = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# ============================================================================
# OPENING BOOK CONFIGURATION
# ============================================================================

class OpeningBookConfig:
    """Opening book system settings"""
    
    # File paths
    DEFAULT_BOOK_PATH = 'Books/opening_book.txt'
    FALLBACK_BOOK_PATH = 'src/Books/openings_book.txt'
    
    # Display settings
    MAX_TOOLTIPS_SHOWN = 6
    TOOLTIP_POSITION = 'top-right'
    SHOW_OPENING_DEFAULT = True
    
    # Badge settings
    BADGE_MAX_COUNT = 99  # Show "99+" if more
    

# ============================================================================
# TOURNAMENT CONFIGURATION
# ============================================================================

class TournamentConfig:
    """Tournament system settings"""
    
    GAMES_PER_MATCHUP = 10
    INCLUDE_MOVE_HISTORY_DEFAULT = False
    REPORTS_DIR = 'tournament/reports/'
    
    # Statistics
    TRACK_MOVE_TIMES = True
    TRACK_OPENING_USAGE = True


# ============================================================================
# FILE PATHS
# ============================================================================

class Paths:
    """File path constants"""
    
    # Directories
    SAVES_DIR = 'saves/'
    BOOKS_DIR = 'Books/'
    TOURNAMENT_REPORTS_DIR = 'tournament/reports/'
    IMAGES_DIR = 'src/Images/'
    
    # Files
    SPLASH_IMAGE = 'src/Images/reversi42-splash.png'
    DEFAULT_OPENING_BOOK = 'Books/opening_book.txt'
    
    # Save file format
    SAVE_FILE_EXTENSION = '.xot'
    SAVE_FILE_PREFIX = 'reversi42_'


# ============================================================================
# GAME CONSTANTS
# ============================================================================

# Player sides
BLACK = 'B'
WHITE = 'W'

# Cell states
EMPTY = '.'
BLACK_CELL = 'B'
WHITE_CELL = 'W'
BLACK_MOVE = 'b'  # Possible move for black
WHITE_MOVE = 'w'  # Possible move for white

# Board notation
ROWNAME = ' ABCDEFGH'

# Version
VERSION = '3.0.0'
VERSION_NAME = 'Bitboard Revolution'

