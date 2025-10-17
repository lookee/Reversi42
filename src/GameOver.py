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

class GameOver:
    """
    Game Over screen that shows the final results and allows
    the player to return to the menu or exit.
    """
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode((width, height))
        
        pygame.display.set_caption("Reversi42 - Game Over")
        
        # Colors
        self.bg_color = (20, 50, 30)
        self.title_color = (255, 255, 255)
        self.winner_color = (255, 215, 0)  # Gold
        self.text_color = (200, 200, 200)
        self.button_color = (100, 150, 100)
        self.button_hover_color = (120, 180, 120)
        self.button_text_color = (255, 255, 255)
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.winner_font = pygame.font.Font(None, 56)
        self.score_font = pygame.font.Font(None, 42)
        self.button_font = pygame.font.Font(None, 36)
        
        # Game results
        self.winner = "Draw"
        self.black_player_name = "Black"
        self.white_player_name = "White"
        self.black_score = 0
        self.white_score = 0
        
        # Buttons
        self.buttons = {
            'menu': pygame.Rect(0, 0, 200, 50),
            'exit': pygame.Rect(0, 0, 200, 50)
        }
        self.selected_button = None
    
    def set_results(self, winner, black_name, white_name, black_score, white_score):
        """Set the game results"""
        self.winner = winner
        self.black_player_name = black_name
        self.white_player_name = white_name
        self.black_score = black_score
        self.white_score = white_score
    
    def draw(self):
        """Draw the game over screen"""
        self.screen.fill(self.bg_color)
        
        center_x = self.width // 2
        y_pos = 80
        
        # Draw "GAME OVER" title
        title_text = "GAME OVER"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(center_x, y_pos))
        self.screen.blit(title_surface, title_rect)
        y_pos += 100
        
        # Draw winner announcement
        if self.winner == "Draw":
            winner_text = "IT'S A DRAW!"
            winner_color = self.text_color
        elif "Black" in self.winner:
            winner_text = f"{self.black_player_name} WINS!"
            winner_color = self.winner_color
        else:
            winner_text = f"{self.white_player_name} WINS!"
            winner_color = self.winner_color
        
        winner_surface = self.winner_font.render(winner_text, True, winner_color)
        winner_rect = winner_surface.get_rect(center=(center_x, y_pos))
        self.screen.blit(winner_surface, winner_rect)
        y_pos += 80
        
        # Draw scores
        # Black score
        black_text = f"{self.black_player_name}: {self.black_score}"
        black_surface = self.score_font.render(black_text, True, self.text_color)
        black_rect = black_surface.get_rect(center=(center_x, y_pos))
        self.screen.blit(black_surface, black_rect)
        
        # Draw black piece
        piece_radius = 18
        pygame.draw.circle(self.screen, (0, 0, 0), 
                         (black_rect.left - 30, y_pos), piece_radius)
        y_pos += 50
        
        # White score
        white_text = f"{self.white_player_name}: {self.white_score}"
        white_surface = self.score_font.render(white_text, True, self.text_color)
        white_rect = white_surface.get_rect(center=(center_x, y_pos))
        self.screen.blit(white_surface, white_rect)
        
        # Draw white piece
        pygame.draw.circle(self.screen, (255, 255, 255), 
                         (white_rect.left - 30, y_pos), piece_radius)
        pygame.draw.circle(self.screen, (0, 0, 0), 
                         (white_rect.left - 30, y_pos), piece_radius, 2)
        y_pos += 100
        
        # Draw buttons
        button_y = y_pos
        
        # Back to Menu button
        menu_button = self.buttons['menu']
        menu_button.center = (center_x - 120, button_y)
        menu_color = self.button_hover_color if self.selected_button == 'menu' else self.button_color
        pygame.draw.rect(self.screen, menu_color, menu_button, border_radius=10)
        pygame.draw.rect(self.screen, self.title_color, menu_button, 2, border_radius=10)
        
        menu_text = self.button_font.render("Menu", True, self.button_text_color)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)
        
        # Exit button
        exit_button = self.buttons['exit']
        exit_button.center = (center_x + 120, button_y)
        exit_color = self.button_hover_color if self.selected_button == 'exit' else self.button_color
        pygame.draw.rect(self.screen, exit_color, exit_button, border_radius=10)
        pygame.draw.rect(self.screen, self.title_color, exit_button, 2, border_radius=10)
        
        exit_text = self.button_font.render("Exit", True, self.button_text_color)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        self.screen.blit(exit_text, exit_text_rect)
        
        pygame.display.flip()
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion for button hover effects"""
        self.selected_button = None
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                self.selected_button = button_name
                break
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks on buttons"""
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                return button_name
        return None
    
    def run(self):
        """Run the game over screen"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "exit"
                elif event.type == MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                    self.draw()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        result = self.handle_mouse_click(event.pos)
                        if result:
                            return result
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "menu"
                    elif event.key == K_q:
                        return "exit"
            
            self.draw()
            clock.tick(60)
        
        return "exit"

