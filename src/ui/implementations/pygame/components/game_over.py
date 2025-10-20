#!/usr/bin/env python3

# ------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
# ------------------------------------------------------------------------

"""
GameOver Screen - Refactored using Widget System

Reduces from 221 LoC → ~50 LoC by using reusable widgets!

Design Pattern: Composite (Panel + Labels + Buttons)
"""

import pygame

from ui.widgets.base import HBox, VBox
from ui.widgets.primitives import Button, Label, Panel


class GameOver:
    """
    Game Over screen using widget system.

    Reduced from 221 LoC to ~50 LoC!
    """

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.get_surface() or pygame.display.set_mode(
            (width, height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Reversi42 - Game Over")

        # Theme colors
        self.bg_color = (0, 65, 50)

        # Game results
        self.winner = "Draw"
        self.black_player_name = "Black"
        self.white_player_name = "White"
        self.black_score = 0
        self.white_score = 0
        self.result = None

        # Build UI
        self._build_ui()

    def set_results(self, winner, black_name, white_name, black_score, white_score):
        """Set game results and rebuild UI"""
        self.winner = winner
        self.black_player_name = black_name
        self.white_player_name = white_name
        self.black_score = black_score
        self.white_score = white_score
        self._build_ui()

    def _build_ui(self):
        """Build UI using widgets"""
        center_x = self.width // 2

        # Main container
        self.container = VBox([], x=0, y=80, width=self.width, height=self.height - 80, spacing=30)

        # Title
        title = Label("GAME OVER", x=0, y=0, font_size=72, color=(230, 240, 235))
        self.container.add(title)

        # Winner announcement
        if self.winner == "Draw":
            winner_text = "IT'S A DRAW!"
            winner_color = (200, 220, 210)
        elif "Black" in self.winner:
            winner_text = f"{self.black_player_name} WINS!"
            winner_color = (255, 215, 0)
        else:
            winner_text = f"{self.white_player_name} WINS!"
            winner_color = (255, 215, 0)

        winner = Label(winner_text, x=0, y=0, font_size=56, color=winner_color)
        self.container.add(winner)

        # Scores
        black_label = Label(
            f"{self.black_player_name}: {self.black_score}",
            x=0,
            y=0,
            font_size=42,
            color=(200, 220, 210),
        )
        white_label = Label(
            f"{self.white_player_name}: {self.white_score}",
            x=0,
            y=0,
            font_size=42,
            color=(200, 220, 210),
        )
        self.container.add(black_label)
        self.container.add(white_label)

        # Buttons
        button_container = HBox([], x=0, y=0, spacing=40)

        menu_btn = Button(
            "Menu",
            x=0,
            y=0,
            width=200,
            height=50,
            on_click=lambda: setattr(self, "result", "menu"),
            color=(0, 80, 60),
            text_color=(230, 240, 235),
        )
        exit_btn = Button(
            "Exit",
            x=0,
            y=0,
            width=200,
            height=50,
            on_click=lambda: setattr(self, "result", "exit"),
            color=(0, 80, 60),
            text_color=(230, 240, 235),
        )

        button_container.add(menu_btn)
        button_container.add(exit_btn)
        self.container.add(button_container)

        # Center container
        self.container.rect.centerx = center_x

    def draw(self):
        """Draw the screen"""
        self.screen.fill(self.bg_color)
        self.container.render(self.screen)
        pygame.display.flip()

    def run(self):
        """Run the game over screen"""
        print("[GameOver] Starting game over screen...")

        self.result = None
        self.draw()

        clock = pygame.time.Clock()

        while self.result is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                    self.screen = pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE
                    )
                    self._build_ui()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    elif event.key == pygame.K_q:
                        return "exit"
                else:
                    # Pass event to widgets
                    self.container.handle_event(event)

            self.draw()
            clock.tick(60)

        return self.result
