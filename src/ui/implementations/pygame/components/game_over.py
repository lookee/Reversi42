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
GameOver Screen - Refactored using Bootstrap-like Layout System

Super clean with Stack primitive!

Design Pattern: Composite + Bootstrap-like Layout
"""

import pygame

from ui.widgets.base import Stack, HBox, Center
from ui.widgets.primitives import Button, Label, Title


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
        """Build UI using Bootstrap-like Stack - ULTRA CLEAN!"""
        
        # === LAYOUT COMPLETO ===
        # Stack verticale centrato con tutto
        layout = Stack(gap=30, align="center", justify="center")
        layout.set_size(self.width, self.height)
        
        # Title - auto-centered with Title()!
        layout.add(Title("GAME OVER", font_size=72))
        
        # Winner announcement - auto-centered!
        if self.winner == "Draw":
            winner_text = "IT'S A DRAW!"
            winner_color = (200, 220, 210)
        elif "Black" in self.winner:
            winner_text = f"{self.black_player_name} WINS!"
            winner_color = (255, 215, 0)
        else:
            winner_text = f"{self.white_player_name} WINS!"
            winner_color = (255, 215, 0)
        
        winner_label = Label(winner_text, font_size=56, color=winner_color)
        winner_label.center_in_parent = True
        layout.add(winner_label)
        
        # Scores - auto-centered!
        black_label = Label(
            f"{self.black_player_name}: {self.black_score}",
            font_size=42,
            color=(200, 220, 210),
        )
        black_label.center_in_parent = True
        
        white_label = Label(
            f"{self.white_player_name}: {self.white_score}",
            font_size=42,
            color=(200, 220, 210),
        )
        white_label.center_in_parent = True
        
        layout.add(black_label)
        layout.add(white_label)
        
        # Buttons row
        buttons = HBox(spacing=40, align="center")
        
        menu_btn = Button(
            "Menu",
            width=200,
            height=50,
            on_click=lambda: setattr(self, "result", "menu"),
            color=(0, 80, 60),
            text_color=(230, 240, 235),
        )
        exit_btn = Button(
            "Exit",
            width=200,
            height=50,
            on_click=lambda: setattr(self, "result", "exit"),
            color=(0, 80, 60),
            text_color=(230, 240, 235),
        )
        
        buttons.add(menu_btn)
        buttons.add(exit_btn)
        layout.add(buttons)
        
        self.container = layout

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
