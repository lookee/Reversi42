#!/usr/bin/env python3

#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#------------------------------------------------------------------------

"""
PauseMenu - Refactored using Widget System

Reduces from 203 LoC → ~80 LoC by using reusable widgets!

Design Pattern: Composite (Panel + Label + Buttons)
"""

import pygame
from ui.widgets.primitives import Panel, Label, Button
from ui.widgets.base import VBox


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
        self.overlay_color = (0, 0, 0, 180)
        
        # Result
        self.result = None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build UI using widgets"""
        # Menu container (centered panel)
        menu_width = 450
        menu_height = 400
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        self.container = Panel(menu_x, menu_y, menu_width, menu_height)
        self.container.background_color = self.bg_color
        self.container.border_color = (230, 240, 235)
        
        # Title
        title = Label("GAME PAUSED", x=20, y=30, font_size=56, color=(230, 240, 235))
        self.container.add(title)
        
        # Menu items (buttons)
        menu_items = [
            ("Resume Game", "resume"),
            ("Save Game", "save"),
            ("Load Game", "load"),
            ("Return to Menu", "menu"),
            ("Exit Game", "exit")
        ]
        
        y_pos = 120
        for text, action in menu_items:
            btn = Button(text, x=75, y=y_pos, width=300, height=40,
                        on_click=lambda a=action: setattr(self, 'result', a),
                        color=(0, 80, 60), text_color=(200, 220, 210),
                        hover_color=(255, 215, 0))
            self.container.add(btn)
            y_pos += 50
    
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

