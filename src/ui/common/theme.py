"""
Theme System - Centralized Color and Style Management

Provides theme presets for easy styling and theming support.
Makes it easy to switch themes (Professional, Dark Mode, Light Mode, etc.)

Design Pattern: Strategy (swappable themes)
"""

from dataclasses import dataclass
from typing import Tuple

Color = Tuple[int, int, int]


@dataclass
class ColorPalette:
    """
    Color palette for a theme.
    
    Contains all colors used in the UI for consistent styling.
    """
    # Board colors
    board_background: Color
    board_lines: Color
    board_shadow: Color
    board_hoshi: Color
    
    # Piece colors
    white_piece: Color
    black_piece: Color
    
    # UI accent colors
    last_move: Color
    legal_move: Color
    white_legal_move: Color
    black_legal_move: Color
    cursor: Color
    book_move: Color
    
    # UI element colors
    ui_background: Color
    ui_text: Color
    ui_accent: Color
    ui_success: Color
    ui_warning: Color
    ui_error: Color
    
    # Menu colors
    menu_background: Color
    menu_text: Color
    menu_selected: Color
    menu_hover: Color


class Theme:
    """
    Theme manager with predefined themes.
    
    Usage:
        view = BoardView(theme=Theme.PROFESSIONAL)
        # Or switch dynamically:
        view.set_theme(Theme.DARK_MODE)
    """
    
    # Professional tournament theme (current default)
    PROFESSIONAL = ColorPalette(
        # Board
        board_background=(0, 95, 75),       # Rich forest green
        board_lines=(15, 55, 45),            # Dark teal
        board_shadow=(25, 50, 40),           # Subtle shadow
        board_hoshi=(20, 70, 55),            # Subtle dark teal
        
        # Pieces
        white_piece=(248, 248, 250),         # Soft white
        black_piece=(15, 15, 20),            # Deep black
        
        # Accents
        last_move=(255, 180, 50),            # Golden amber
        legal_move=(180, 220, 190),          # Soft mint
        white_legal_move=(200, 230, 210),    # Light mint
        black_legal_move=(160, 200, 170),    # Darker mint
        cursor=(255, 215, 0),                # Pure gold
        book_move=(255, 215, 0),             # Gold
        
        # UI
        ui_background=(40, 40, 45),
        ui_text=(240, 240, 245),
        ui_accent=(0, 120, 100),
        ui_success=(80, 200, 120),
        ui_warning=(255, 180, 50),
        ui_error=(220, 60, 60),
        
        # Menu
        menu_background=(30, 30, 35),
        menu_text=(240, 240, 245),
        menu_selected=(0, 150, 120),
        menu_hover=(0, 120, 100),
    )
    
    # Dark mode theme
    DARK_MODE = ColorPalette(
        # Board
        board_background=(30, 30, 35),
        board_lines=(50, 50, 55),
        board_shadow=(20, 20, 25),
        board_hoshi=(60, 60, 65),
        
        # Pieces
        white_piece=(240, 240, 245),
        black_piece=(40, 40, 45),
        
        # Accents
        last_move=(100, 180, 255),           # Blue accent
        legal_move=(80, 120, 160),
        white_legal_move=(100, 140, 180),
        black_legal_move=(60, 100, 140),
        cursor=(100, 180, 255),
        book_move=(255, 180, 100),
        
        # UI
        ui_background=(25, 25, 30),
        ui_text=(220, 220, 225),
        ui_accent=(100, 180, 255),
        ui_success=(80, 180, 120),
        ui_warning=(255, 180, 80),
        ui_error=(220, 80, 80),
        
        # Menu
        menu_background=(20, 20, 25),
        menu_text=(220, 220, 225),
        menu_selected=(100, 180, 255),
        menu_hover=(80, 150, 220),
    )
    
    # Light mode theme
    LIGHT_MODE = ColorPalette(
        # Board
        board_background=(200, 220, 200),
        board_lines=(100, 120, 100),
        board_shadow=(150, 170, 150),
        board_hoshi=(140, 160, 140),
        
        # Pieces
        white_piece=(250, 250, 252),
        black_piece=(30, 30, 35),
        
        # Accents
        last_move=(255, 140, 0),
        legal_move=(180, 220, 180),
        white_legal_move=(200, 230, 200),
        black_legal_move=(160, 200, 160),
        cursor=(255, 140, 0),
        book_move=(255, 180, 0),
        
        # UI
        ui_background=(245, 245, 248),
        ui_text=(30, 30, 35),
        ui_accent=(0, 120, 200),
        ui_success=(60, 180, 100),
        ui_warning=(255, 140, 0),
        ui_error=(220, 50, 50),
        
        # Menu
        menu_background=(240, 240, 245),
        menu_text=(30, 30, 35),
        menu_selected=(0, 120, 200),
        menu_hover=(100, 160, 220),
    )
    
    # High contrast theme (accessibility)
    HIGH_CONTRAST = ColorPalette(
        # Board
        board_background=(0, 0, 0),
        board_lines=(255, 255, 255),
        board_shadow=(128, 128, 128),
        board_hoshi=(200, 200, 200),
        
        # Pieces
        white_piece=(255, 255, 255),
        black_piece=(0, 0, 0),
        
        # Accents
        last_move=(255, 255, 0),
        legal_move=(0, 255, 0),
        white_legal_move=(200, 255, 200),
        black_legal_move=(0, 200, 0),
        cursor=(255, 0, 255),
        book_move=(255, 255, 0),
        
        # UI
        ui_background=(0, 0, 0),
        ui_text=(255, 255, 255),
        ui_accent=(0, 255, 255),
        ui_success=(0, 255, 0),
        ui_warning=(255, 255, 0),
        ui_error=(255, 0, 0),
        
        # Menu
        menu_background=(0, 0, 0),
        menu_text=(255, 255, 255),
        menu_selected=(0, 255, 255),
        menu_hover=(128, 255, 255),
    )
    
    @classmethod
    def get_theme(cls, name: str) -> ColorPalette:
        """
        Get theme by name.
        
        Args:
            name: Theme name ('professional', 'dark', 'light', 'high_contrast')
            
        Returns:
            ColorPalette for the theme
        """
        themes = {
            'professional': cls.PROFESSIONAL,
            'dark': cls.DARK_MODE,
            'light': cls.LIGHT_MODE,
            'high_contrast': cls.HIGH_CONTRAST,
        }
        return themes.get(name.lower(), cls.PROFESSIONAL)

