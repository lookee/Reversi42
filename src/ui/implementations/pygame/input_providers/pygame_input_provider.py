"""
PygameInputProvider - Pygame-specific implementation of InputProvider

Adapts pygame input mechanism to the InputProvider interface.
This keeps pygame dependencies OUT of the Players domain layer.

Design Pattern: Adapter
"""

from typing import List, Optional

import pygame

from Players.abstractions import InputProvider
from Reversi.Game import Move


class PygameInputProvider(InputProvider):
    """
    Pygame-specific implementation of InputProvider.

    Handles:
    - Mouse clicks for move selection
    - Keyboard input (cursor navigation, ENTER/SPACE for selection)
    - Opening book tooltips
    - ESC for pause, Q for quit

    This adapter isolates pygame dependencies from the Player domain layer.
    """

    def __init__(self, board_control):
        """
        Initialize pygame input provider.

        Args:
            board_control: BoardControl instance for pygame-specific operations
        """
        self.control = board_control
        self.clock = pygame.time.Clock()
        self._exit_requested = False
        self._pause_requested = False

    def get_move_input(self, game, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get move from pygame input (mouse or keyboard).

        Args:
            game: Current game state
            legal_moves: List of legal moves

        Returns:
            Move selected by user, or None if exit/pause
        """
        self.control.cursorHand()
        self.control.waitInput = True
        self.control.resetSelection()

        while self.control.waitInput:
            # Process pygame events
            self.control.action()

            # Check for exit/pause
            if self.control.should_exit:
                self._exit_requested = True
                return None

            if self.control.should_pause:
                self._pause_requested = True
                return None

            # Check if a move has been selected (via click or keyboard)
            if self.control.bx is not None and self.control.by is not None:
                move = Move(self.control.bx + 1, self.control.by + 1)

                # Validate move
                if move in legal_moves:
                    self.control.waitInput = False
                    return move
                else:
                    # Invalid move - reset and continue
                    print(f"Move {move} is not valid!")
                    self.control.bx = self.control.by = None

            # Handle opening book tooltip display
            self._handle_opening_book_tooltip(game, legal_moves)

            # Limit to 60 FPS
            self.clock.tick(60)

        return None

    def _handle_opening_book_tooltip(self, game, legal_moves):
        """
        Handle opening book information tooltip.

        Shows opening information when hovering over legal moves.
        """
        if not self.control.show_opening or not self.control.opening_book:
            return

        current_opening_info = None

        # Determine hovered move (mouse or cursor)
        if self.control.cursor_mode:
            # Cursor navigation mode
            cursor_x, cursor_y = self.control.view.cursorX, self.control.view.cursorY
            if cursor_x is not None and cursor_y is not None:
                cursor_move = Move(cursor_x + 1, cursor_y + 1)
                if cursor_move in legal_moves:
                    current_opening_info = self.control.opening_book.get_openings_for_move(
                        game.history, cursor_move
                    )
        else:
            # Mouse mode
            mouse_pos = pygame.mouse.get_pos()
            bx, by = self.control.view.point2Box(mouse_pos[0], mouse_pos[1])
            if bx is not None and by is not None:
                if bx in range(self.control.sizex) and by in range(self.control.sizey):
                    hover_move = Move(bx + 1, by + 1)
                    if hover_move in legal_moves:
                        current_opening_info = self.control.opening_book.get_openings_for_move(
                            game.history, hover_move
                        )

        # Initialize last_opening_info if not exists
        if not hasattr(self.control, "last_opening_info"):
            self.control.last_opening_info = None

        # Check if tooltip changed
        if current_opening_info != self.control.last_opening_info:
            # Clear old tooltip
            self.control.view.clear_tooltip_area()

            # Redraw board
            self.control.renderModel()

            # Draw new tooltip if exists
            if current_opening_info:
                self.control.view.set_opening_info(current_opening_info)
                self.control.view.draw_opening_info_fixed()
            else:
                self.control.view.set_opening_info(None)

            # Update display
            pygame.display.flip()
            self.control.last_opening_info = current_opening_info
        else:
            # Normal update
            self.control.view.update(self.control.cursor_mode)

    def should_exit(self) -> bool:
        """Check if exit was requested."""
        return self._exit_requested or self.control.should_exit

    def should_pause(self) -> bool:
        """Check if pause was requested."""
        return self._pause_requested or self.control.should_pause

    def reset(self):
        """Reset input provider state."""
        self._exit_requested = False
        self._pause_requested = False
        self.control.waitInput = False
        self.control.bx = self.control.by = None
