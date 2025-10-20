"""
LayoutManager - Smart Layout Calculations

Handles layout calculations for responsive UI design.
No hardcoded positions - all calculated based on screen size.

Design Pattern: Strategy
"""

from typing import Tuple

import pygame


class LayoutManager:
    """
    Layout manager for calculating widget positions and sizes.

    Provides smart layout calculations based on screen size and constraints.
    No more hardcoded magic numbers!
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize layout manager.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

    def calculate_board_rect(self, board_size: int = 8) -> pygame.Rect:
        """
        Calculate board rectangle based on screen size.

        Centers the board and sizes it appropriately.

        Args:
            board_size: Number of cells (default 8x8)

        Returns:
            pygame.Rect for the board
        """
        # Use 70% of smaller dimension for board
        available_size = min(self.screen_width, self.screen_height)
        board_pixel_size = int(available_size * 0.7)

        # Center on screen
        x = (self.screen_width - board_pixel_size) // 2
        y = (self.screen_height - board_pixel_size) // 2

        return pygame.Rect(x, y, board_pixel_size, board_pixel_size)

    def calculate_cell_size(self, board_rect: pygame.Rect, board_size: int = 8) -> int:
        """
        Calculate size of each cell.

        Args:
            board_rect: Board rectangle
            board_size: Number of cells

        Returns:
            Size of each cell in pixels
        """
        return board_rect.width // board_size

    def board_to_screen(
        self, board_x: int, board_y: int, board_rect: pygame.Rect, cell_size: int
    ) -> Tuple[int, int]:
        """
        Convert board coordinates to screen coordinates.

        Args:
            board_x: Board X (0-7)
            board_y: Board Y (0-7)
            board_rect: Board rectangle
            cell_size: Size of each cell

        Returns:
            (screen_x, screen_y) tuple
        """
        screen_x = board_rect.x + board_x * cell_size
        screen_y = board_rect.y + board_y * cell_size
        return (screen_x, screen_y)

    def screen_to_board(
        self, screen_x: int, screen_y: int, board_rect: pygame.Rect, cell_size: int
    ) -> Tuple[int, int]:
        """
        Convert screen coordinates to board coordinates.

        Args:
            screen_x: Screen X
            screen_y: Screen Y
            board_rect: Board rectangle
            cell_size: Size of each cell

        Returns:
            (board_x, board_y) tuple or (-1, -1) if outside board
        """
        if not board_rect.collidepoint(screen_x, screen_y):
            return (-1, -1)

        rel_x = screen_x - board_rect.x
        rel_y = screen_y - board_rect.y

        board_x = rel_x // cell_size
        board_y = rel_y // cell_size

        return (board_x, board_y)

    def calculate_centered_rect(self, width: int, height: int) -> pygame.Rect:
        """
        Calculate centered rectangle.

        Args:
            width: Rectangle width
            height: Rectangle height

        Returns:
            Centered pygame.Rect
        """
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        return pygame.Rect(x, y, width, height)

    def calculate_header_rect(self, height: int = 60) -> pygame.Rect:
        """
        Calculate header rectangle (top of screen).

        Args:
            height: Header height

        Returns:
            Header rect
        """
        return pygame.Rect(0, 0, self.screen_width, height)

    def calculate_footer_rect(self, height: int = 40) -> pygame.Rect:
        """
        Calculate footer rectangle (bottom of screen).

        Args:
            height: Footer height

        Returns:
            Footer rect
        """
        return pygame.Rect(0, self.screen_height - height, self.screen_width, height)

    def resize(self, new_width: int, new_height: int):
        """
        Update screen size (for window resize).

        Args:
            new_width: New screen width
            new_height: New screen height
        """
        self.screen_width = new_width
        self.screen_height = new_height
