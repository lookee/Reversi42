#!/usr/bin/env python3

#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Reversi42 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Reversi42.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

import pygame
from pygame.locals import *

class PauseMenu:
    """
    Pause menu that appears when ESC is pressed during the game.
    Allows player to resume, return to main menu, or exit.
    """
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Colors
        self.overlay_color = (0, 0, 0, 180)  # Semi-transparent black
        self.bg_color = (20, 50, 30)
        self.title_color = (255, 255, 255)
        self.text_color = (200, 200, 200)
        self.selected_color = (255, 255, 0)
        self.button_color = (100, 150, 100)
        self.button_hover_color = (120, 180, 120)
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 56)
        self.menu_font = pygame.font.Font(None, 36)
        
        # Menu items
        self.menu_items = [
            "Resume Game",
            "Save Game",
            "Load Game",
            "Return to Menu",
            "Exit Game"
        ]
        self.current_selection = 0
    
    def draw(self):
        """Draw the pause menu overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause menu box
        menu_width = 450
        menu_height = 400
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        # Draw menu background
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, self.bg_color, menu_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.title_color, menu_rect, 3, border_radius=15)
        
        # Draw title
        title_text = self.title_font.render("GAME PAUSED", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, menu_y + 70))
        self.screen.blit(title_text, title_rect)
        
        # Draw menu items
        start_y = menu_y + 140
        item_spacing = 45  # Spacing for menu items
        
        for i, item in enumerate(self.menu_items):
            color = self.selected_color if i == self.current_selection else self.text_color
            
            # Draw menu item without indicator
            item_text = self.menu_font.render(item, True, color)
            item_rect = item_text.get_rect(center=(self.width // 2, start_y + i * item_spacing))
            self.screen.blit(item_text, item_rect)
        
        pygame.display.flip()
    
    def handle_key(self, event):
        """Handle keyboard input"""
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.menu_items)
                return None
            elif event.key == K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.menu_items)
                return None
            elif event.key == K_RETURN:
                item = self.menu_items[self.current_selection]
                if item == "Resume Game":
                    return "resume"
                elif item == "Save Game":
                    return "save"
                elif item == "Load Game":
                    return "load"
                elif item == "Return to Menu":
                    return "menu"
                elif item == "Exit Game":
                    return "exit"
            elif event.key == K_ESCAPE:
                return "resume"  # ESC again resumes the game
        return None
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks on menu items"""
        menu_width = 450
        menu_height = 450
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        start_y = menu_y + 140
        item_spacing = 45
        
        mouse_x, mouse_y = pos
        
        for i, item in enumerate(self.menu_items):
            item_y = start_y + i * item_spacing
            # Check if click is within the item area
            if abs(mouse_y - item_y) < 22 and menu_x < mouse_x < menu_x + menu_width:
                if item == "Resume Game":
                    return "resume"
                elif item == "Save Game":
                    return "save"
                elif item == "Load Game":
                    return "load"
                elif item == "Return to Menu":
                    return "menu"
                elif item == "Exit Game":
                    return "exit"
        return None
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion for hover effects"""
        menu_width = 450
        menu_height = 400
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        start_y = menu_y + 140
        item_spacing = 45
        
        mouse_x, mouse_y = pos
        
        for i, item in enumerate(self.menu_items):
            item_y = start_y + i * item_spacing
            if abs(mouse_y - item_y) < 22 and menu_x < mouse_x < menu_x + menu_width:
                self.current_selection = i
                return
    
    def run(self):
        """Run the pause menu"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "exit"
                elif event.type == KEYDOWN:
                    result = self.handle_key(event)
                    if result:
                        return result
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        result = self.handle_mouse_click(event.pos)
                        if result:
                            return result
                elif event.type == MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
            
            self.draw()
            clock.tick(60)
        
        return "resume"

