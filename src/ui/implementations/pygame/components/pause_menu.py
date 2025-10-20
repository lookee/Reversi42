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
PauseMenu - Refactored using Widget System

Reduces from 203 LoC → ~80 LoC by using reusable widgets!

Design Pattern: Composite (Panel + Label + Buttons)
"""

import pygame

from ui.widgets.base import VBox
from ui.widgets.primitives import Button, Label, Panel


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
        """Build UI using widgets"""
        # Import MenuConfig for consistent colors
        from core.config import MenuConfig
        
        # Menu container (centered panel)
        menu_width = 450
        menu_height = 450
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2

        self.container = Panel(menu_x, menu_y, menu_width, menu_height)
        self.container.background_color = self.bg_color
        self.container.border_color = MenuConfig.TITLE_COLOR

        # Title (centered in panel)
        title = Label("GAME PAUSED", font_size=56, color=MenuConfig.TITLE_COLOR)
        # Center title horizontally using actual width
        title_x = (menu_width - title.rect.width) // 2
        title.set_position(title_x, 30)
        self.container.add(title)

        # Menu items (buttons) - centered in panel
        menu_items = [
            ("Resume Game", "resume", (40, 40, 50)),
            ("Save Game", "save", (40, 40, 50)),
            ("Load Game", "load", (40, 40, 50)),
            ("Return to Menu", "menu", (40, 40, 50)),
            ("Quit", "exit", (80, 50, 50)),  # Rosso scuro tendente al grigio
        ]
        
        button_width = 300
        button_x = (menu_width - button_width) // 2  # Center buttons horizontally
        y_pos = 130
        
        for text, action, color in menu_items:
            btn = Button(
                text,
                x=button_x,
                y=y_pos,
                width=button_width,
                height=45,
                on_click=lambda a=action: setattr(self, "result", a),
                color=color,
                hover_color=(color[0] + 20, color[1] + 10, color[2] + 10) if action != "exit" else (100, 60, 60),
                text_color=MenuConfig.TEXT_COLOR,
            )
            self.container.add(btn)
            y_pos += 55

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
