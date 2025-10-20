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
PauseMenu - Refactored using Bootstrap-like Layout System

Ultra-clean code with Stack primitive!

Design Pattern: Composite + Bootstrap-like Layout
"""

import pygame

from ui.widgets.base import Stack, Center
from ui.widgets.primitives import Button, Label, Title, Panel


class PauseMenu:
    """
    Pause menu using widget system.

    Reduced from 203 LoC to ~80 LoC!
    """

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Theme colors
        self.bg_color = (0, 65, 50)
        self.overlay_color = (0, 100, 75, 180)  # Verde più chiaro semi-trasparente

        # Result
        self.result = None

        # Build UI
        self._build_ui()

    def _build_ui(self):
        """Build UI using Bootstrap-like Stack primitive - ULTRA CLEAN!"""
        from core.config import MenuConfig
        
        # === PANEL CENTRALE ===
        # Stack verticale con tutto (titolo + bottoni)
        panel = Stack(gap=20, align="center")
        panel.background_color = self.bg_color
        panel.border_color = MenuConfig.TITLE_COLOR
        panel.padding = 30
        panel.border_width = 2
        panel.center_in_parent = True  # Panel centrato automaticamente!
        
        # Titolo centrato automaticamente con Title()!
        panel.add(Title("GAME PAUSED", font_size=56, color=MenuConfig.TITLE_COLOR))
        
        # Menu items - ULTRA SEMPLICE!
        menu_items = [
            ("Resume Game", "resume", (40, 40, 50), (60, 50, 60)),
            ("Save Game", "save", (40, 40, 50), (60, 50, 60)),
            ("Load Game", "load", (40, 40, 50), (60, 50, 60)),
            ("Return to Menu", "menu", (40, 40, 50), (60, 50, 60)),
            ("Quit", "exit", (80, 50, 50), (100, 60, 60)),
        ]
        
        for text, action, color, hover_color in menu_items:
            btn = Button(
                text,
                width=300,
                height=45,
                on_click=lambda a=action: setattr(self, "result", a),
                color=color,
                hover_color=hover_color,
                text_color=MenuConfig.TEXT_COLOR,
            )
            panel.add(btn)
        
        # === CENTER IL PANEL ===
        center = Center(width=self.width, height=self.height)
        center.add(panel)
        
        self.container = center

    def draw(self):
        """Draw the pause menu"""
        # Optional: Draw semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        self.screen.blit(overlay, (0, 0))

        # Draw menu panel
        self.container.render(self.screen)
        pygame.display.flip()

    def run(self):
        """Run the pause menu"""
        self.result = None
        clock = pygame.time.Clock()

        while self.result is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "resume"  # ESC resumes
                else:
                    # Pass events to widgets
                    self.container.handle_event(event)

            self.draw()
            clock.tick(60)

        return self.result
