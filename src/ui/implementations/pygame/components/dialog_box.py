#!/usr/bin/env python3

#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#------------------------------------------------------------------------

import pygame
from pygame.locals import *

class TextInputDialog:
    """
    Simple text input dialog for Pygame.
    Used for save game filename input.
    """
    
    def __init__(self, prompt="Enter text:", default_text=""):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.prompt = prompt
        self.text = default_text
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # Colors
        self.overlay_color = (0, 0, 0, 200)
        self.bg_color = (20, 50, 30)
        self.title_color = (255, 255, 255)
        self.text_color = (200, 200, 200)
        self.input_bg_color = (40, 70, 50)
        self.cursor_color = (255, 255, 0)
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
    
    def draw(self):
        """Draw the text input dialog"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 500
        dialog_height = 200
        dialog_x = (self.width - dialog_width) // 2
        dialog_y = (self.height - dialog_height) // 2
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, self.bg_color, dialog_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.title_color, dialog_rect, 3, border_radius=10)
        
        # Prompt text
        prompt_text = self.title_font.render(self.prompt, True, self.title_color)
        prompt_rect = prompt_text.get_rect(center=(self.width // 2, dialog_y + 50))
        self.screen.blit(prompt_text, prompt_rect)
        
        # Input box
        input_width = 400
        input_height = 40
        input_x = (self.width - input_width) // 2
        input_y = dialog_y + 90
        
        input_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        pygame.draw.rect(self.screen, self.input_bg_color, input_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.text_color, input_rect, 2, border_radius=5)
        
        # Input text with cursor
        display_text = self.text
        if self.cursor_visible:
            display_text += "|"
        
        text_surface = self.text_font.render(display_text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(input_x + 10, input_y + input_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Instructions
        instructions = "ENTER: Confirm | ESC: Cancel | Backspace: Delete"
        inst_text = self.small_font.render(instructions, True, self.text_color)
        inst_rect = inst_text.get_rect(center=(self.width // 2, dialog_y + dialog_height - 30))
        self.screen.blit(inst_text, inst_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Run the dialog and return the input text or None if cancelled"""
        clock = pygame.time.Clock()
        
        while True:
            # Cursor blinking
            self.cursor_timer += 1
            if self.cursor_timer >= 30:  # Blink every 30 frames (~0.5s at 60fps)
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return self.text
                    elif event.key == K_ESCAPE:
                        return None
                    elif event.key == K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == K_TAB:
                        pass  # Ignore tab
                    else:
                        # Add character (limit to 30 chars)
                        if len(self.text) < 30 and event.unicode.isprintable():
                            self.text += event.unicode
            
            self.draw()
            clock.tick(60)


class ListSelectDialog:
    """
    List selection dialog for Pygame.
    Used for load game file selection.
    """
    
    def __init__(self, title="Select an option", items=None, allow_cancel=True):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.title = title
        self.items = items or []
        self.allow_cancel = allow_cancel
        self.current_selection = 0
        
        # Colors
        self.overlay_color = (0, 0, 0, 200)
        self.bg_color = (20, 50, 30)
        self.title_color = (255, 255, 255)
        self.text_color = (200, 200, 200)
        self.selected_color = (255, 255, 0)
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 18)
    
    def draw(self):
        """Draw the selection dialog"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 600
        dialog_height = min(500, self.height - 100)
        dialog_x = (self.width - dialog_width) // 2
        dialog_y = (self.height - dialog_height) // 2
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, self.bg_color, dialog_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.title_color, dialog_rect, 3, border_radius=10)
        
        # Title
        title_text = self.title_font.render(self.title, True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, dialog_y + 40))
        self.screen.blit(title_text, title_rect)
        
        # Items list with scrolling
        start_y = dialog_y + 90
        item_spacing = 35
        available_height = dialog_height - 140
        max_visible = available_height // item_spacing
        
        # Calculate visible range
        display_items = self.items[:]
        if self.allow_cancel:
            display_items.append("Cancel")
        
        if len(display_items) > max_visible:
            # Scrolling
            start_idx = max(0, min(self.current_selection - max_visible // 2, 
                                   len(display_items) - max_visible))
            end_idx = start_idx + max_visible
            visible_items = list(enumerate(display_items))[start_idx:end_idx]
            
            # Scroll indicators
            if start_idx > 0:
                arrow = self.small_font.render("^ More above", True, self.selected_color)
                self.screen.blit(arrow, (dialog_x + 20, start_y - 25))
            if end_idx < len(display_items):
                arrow = self.small_font.render("v More below", True, self.selected_color)
                self.screen.blit(arrow, (dialog_x + 20, dialog_y + dialog_height - 50))
        else:
            visible_items = list(enumerate(display_items))
        
        # Draw items
        for display_idx, (actual_idx, item) in enumerate(visible_items):
            is_selected = actual_idx == self.current_selection
            color = self.selected_color if is_selected else self.text_color
            
            # Truncate long filenames
            display_item = item
            if len(display_item) > 50:
                display_item = display_item[:47] + "..."
            
            item_text = self.text_font.render(display_item, True, color)
            item_rect = item_text.get_rect(center=(self.width // 2, start_y + display_idx * item_spacing))
            self.screen.blit(item_text, item_rect)
        
        # Instructions
        instructions = "Arrows: Navigate | ENTER: Select | ESC: Cancel"
        inst_text = self.small_font.render(instructions, True, self.text_color)
        inst_rect = inst_text.get_rect(center=(self.width // 2, dialog_y + dialog_height - 20))
        self.screen.blit(inst_text, inst_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Run the dialog and return selected index or None if cancelled"""
        clock = pygame.time.Clock()
        
        display_items = self.items[:]
        if self.allow_cancel:
            display_items.append("Cancel")
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.current_selection = (self.current_selection - 1) % len(display_items)
                    elif event.key == K_DOWN:
                        self.current_selection = (self.current_selection + 1) % len(display_items)
                    elif event.key == K_RETURN:
                        if self.allow_cancel and self.current_selection == len(self.items):
                            return None  # Cancel selected
                        return self.current_selection
                    elif event.key == K_ESCAPE:
                        return None
            
            self.draw()
            clock.tick(60)


class MessageDialog:
    """
    Simple message dialog for Pygame.
    Used for displaying messages and errors.
    """
    
    def __init__(self, title="Message", message="", message_type="info"):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.title = title
        self.message = message
        self.message_type = message_type  # "info", "success", "error"
        
        # Colors
        self.overlay_color = (0, 0, 0, 200)
        self.bg_color = (20, 50, 30)
        self.title_color = (255, 255, 255)
        self.text_color = (200, 200, 200)
        
        if message_type == "success":
            self.border_color = (0, 255, 0)
        elif message_type == "error":
            self.border_color = (255, 0, 0)
        else:
            self.border_color = (255, 255, 255)
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
    
    def draw(self):
        """Draw the message dialog"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 500
        dialog_height = 250
        dialog_x = (self.width - dialog_width) // 2
        dialog_y = (self.height - dialog_height) // 2
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, self.bg_color, dialog_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.border_color, dialog_rect, 3, border_radius=10)
        
        # Title
        title_text = self.title_font.render(self.title, True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, dialog_y + 50))
        self.screen.blit(title_text, title_rect)
        
        # Message (can be multiline)
        message_lines = self.message.split('\n')
        y_offset = dialog_y + 110
        
        for line in message_lines[:5]:  # Max 5 lines
            if len(line) > 60:
                line = line[:57] + "..."
            text_surface = self.text_font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30
        
        # Instructions
        instructions = "Press ENTER or ESC to close"
        inst_text = self.small_font.render(instructions, True, self.text_color)
        inst_rect = inst_text.get_rect(center=(self.width // 2, dialog_y + dialog_height - 30))
        self.screen.blit(inst_text, inst_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Show the dialog and wait for user to close it"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key in (K_RETURN, K_ESCAPE, K_SPACE):
                        return
                elif event.type == MOUSEBUTTONDOWN:
                    return  # Click anywhere to close
            
            self.draw()
            clock.tick(60)

