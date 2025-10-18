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
import os
import sys

# Add src to path if needed
if 'src' not in sys.path:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from Players.PlayerFactory import PlayerFactory

class Menu:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Reversi42 - Menu")
        
        # Colors
        self.bg_color = (20, 50, 30)  # Dark green background
        self.title_color = (255, 255, 255)  # White title
        self.text_color = (200, 200, 200)  # Light gray text
        self.selected_color = (255, 255, 0)  # Yellow for selection
        self.highlight_color = (100, 150, 100)  # Light green for highlight
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 64)  # Reduced from 72
        self.menu_font = pygame.font.Font(None, 32)   # Reduced from 36
        self.small_font = pygame.font.Font(None, 20)  # Reduced from 24
        
        # Menu state
        self.current_selection = 0
        self.menu_items = [
            "Black Player",
            "White Player",
            "Show Opening",
            "Start Game",
            "Help",
            "About",
            "Exit"
        ]
        
        # Player selections - defaults
        self.black_player = "Human"
        self.white_player = "AI Bitboard with Book (Fastest)"
        self.black_difficulty = 5
        self.white_difficulty = 5
        
        # Opening book display option
        self.show_opening = True  # Default: show opening book info
        
        # Get player types and descriptions from PlayerFactory metadata
        self.player_types = PlayerFactory.get_available_player_types()
        self.all_metadata = PlayerFactory.get_all_player_metadata()
        
        # Build descriptions from metadata
        self.player_descriptions = {
            name: meta['description']
            for name, meta in self.all_metadata.items()
            if meta['enabled']
        }
        
        # Difficulties for AI players (can be extended by player metadata)
        self.difficulties = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Submenu state
        self.in_submenu = False
        self.submenu_type = None  # "black_player", "white_player", "black_difficulty", "white_difficulty"
        self.submenu_selection = 0
        
        # Help screen state
        self.in_help = False
        
        # About screen state
        self.in_about = False
        
        # Load splash screen
        self.splash_image = None
        self.load_splash_screen()
        
    def load_splash_screen(self):
        """Load the splash screen image"""
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            splash_path = os.path.join(script_dir, "Images", "reversi42-splash.png")
            
            if os.path.exists(splash_path):
                self.splash_image = pygame.image.load(splash_path)
                # Scale the image to fit the screen
                self.splash_image = pygame.transform.scale(self.splash_image, (self.width, self.height))
            else:
                print(f"Splash image not found at: {splash_path}")
        except Exception as e:
            print(f"Error loading splash screen: {e}")
    
    def show_splash_screen(self):
        """Display splash screen for 3 seconds"""
        if self.splash_image:
            self.screen.blit(self.splash_image, (0, 0))
        else:
            # Fallback splash screen
            self.screen.fill(self.bg_color)
            title_text = self.title_font.render("Reversi42", True, self.title_color)
            title_rect = title_text.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(title_text, title_rect)
            
            subtitle_text = self.menu_font.render("Loading...", True, self.text_color)
            subtitle_rect = subtitle_text.get_rect(center=(self.width//2, self.height//2 + 60))
            self.screen.blit(subtitle_text, subtitle_rect)
        
        pygame.display.flip()
        pygame.time.wait(3000)  # Show for 3 seconds
    
    def draw_menu(self):
        """Draw the main menu"""
        self.screen.fill(self.bg_color)
        
        # Title
        title_text = self.title_font.render("Reversi42", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width//2, 60))
        self.screen.blit(title_text, title_rect)
        
        # Menu items with better spacing
        start_y = 160
        item_spacing = 50  # Reduced from 60
        for i, item in enumerate(self.menu_items):
            color = self.selected_color if i == self.current_selection else self.text_color
            
            if item == "Black Player":
                text = f"Black Player: {self.black_player}"
                if self.black_player in ["AI", "AI with Opening Book", "AI Bitboard (Ultra-Fast)", "AI Bitboard with Book (Fastest)"]:
                    text += f" (Level {self.black_difficulty})"
            elif item == "White Player":
                text = f"White Player: {self.white_player}"
                if self.white_player in ["AI", "AI with Opening Book", "AI Bitboard (Ultra-Fast)", "AI Bitboard with Book (Fastest)"]:
                    text += f" (Level {self.white_difficulty})"
            elif item == "Show Opening":
                text = "Show Opening" if self.show_opening else "Hide Opening"
            else:
                text = item
            
            # Truncate text if too long to prevent going off screen
            max_width = self.width - 100  # Leave 50px margin on each side
            if len(text) > 30:  # Approximate character limit
                text = text[:27] + "..."
            
            menu_text = self.menu_font.render(text, True, color)
            menu_rect = menu_text.get_rect(center=(self.width//2, start_y + i * item_spacing))
            self.screen.blit(menu_text, menu_rect)
        
        # Instructions with better positioning
        instructions = [
            "Use arrow keys to navigate",
            "Press ENTER to select",
            "Press ESC to exit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, self.text_color)
            inst_rect = inst_text.get_rect(center=(self.width//2, self.height - 80 + i * 20))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_submenu(self):
        """Draw submenu for player/difficulty selection"""
        self.screen.fill(self.bg_color)
        
        # Title with better positioning
        if self.submenu_type == "black_player":
            title = "Select Black Player"
        elif self.submenu_type == "white_player":
            title = "Select White Player"
        elif self.submenu_type == "black_difficulty":
            title = "Select Black AI Difficulty"
        elif self.submenu_type == "white_difficulty":
            title = "Select White AI Difficulty"
        else:
            title = "Select Option"
        
        # Use smaller font for longer titles to prevent overflow
        title_font = self.title_font if len(title) <= 20 else self.menu_font
        title_text = title_font.render(title, True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width//2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Options with better spacing
        if "player" in self.submenu_type:
            options = self.player_types
        else:
            options = [f"Level {d}" for d in self.difficulties]
        
        start_y = 200
        option_spacing = 45  # Reduced spacing
        max_options_visible = (self.height - start_y - 100) // option_spacing
        
        # If too many options, show only a subset with scrolling
        if len(options) > max_options_visible:
            # Simple scrolling - show options around current selection
            start_idx = max(0, self.submenu_selection - max_options_visible // 2)
            end_idx = min(len(options), start_idx + max_options_visible)
            visible_options = options[start_idx:end_idx]
            visible_selection = self.submenu_selection - start_idx
        else:
            visible_options = options
            visible_selection = self.submenu_selection
        
        for i, option in enumerate(visible_options):
            color = self.selected_color if i == visible_selection else self.text_color
            option_text = self.menu_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.width//2, start_y + i * option_spacing))
            self.screen.blit(option_text, option_rect)
            
            # Show description for player types
            if "player" in self.submenu_type and option in self.player_descriptions:
                desc_text = self.small_font.render(self.player_descriptions[option], True, self.text_color)
                desc_rect = desc_text.get_rect(center=(self.width//2, start_y + i * option_spacing + 20))
                self.screen.blit(desc_text, desc_rect)
        
        # Instructions with better positioning
        instructions = [
            "Use arrow keys to navigate",
            "Press ENTER to select",
            "Press ESC to go back"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, self.text_color)
            inst_rect = inst_text.get_rect(center=(self.width//2, self.height - 60 + i * 18))
            self.screen.blit(inst_text, inst_rect)
    
    def draw_help(self):
        """Draw the help screen"""
        self.screen.fill(self.bg_color)
        
        # Title
        title_text = self.title_font.render("Help", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width//2, 60))
        self.screen.blit(title_text, title_rect)
        
        # Build player types list from metadata (only enabled players)
        player_descriptions_list = []
        for name in self.player_types:
            if name in self.player_descriptions:
                player_descriptions_list.append(f"{name}: {self.player_descriptions[name]}")
        
        # Help content
        help_sections = [
            ("PLAYER TYPES", player_descriptions_list),
            ("GAME CONTROLS", [
                "Mouse: Click on valid moves to place your piece",
                "C key: Toggle cursor navigation mode",
                "Arrow keys: Move cursor (when in cursor mode)",
                "ENTER/SPACE: Select move at cursor position",
                "ESC or Q: Quit the game"
            ])
        ]
        
        y_pos = 130
        section_spacing = 15
        line_spacing = 22
        
        for section_title, section_lines in help_sections:
            # Draw section title
            section_surface = self.menu_font.render(section_title, True, self.selected_color)
            section_rect = section_surface.get_rect(center=(self.width//2, y_pos))
            self.screen.blit(section_surface, section_rect)
            y_pos += 35
            
            # Draw section content
            for line in section_lines:
                line_surface = self.small_font.render(line, True, self.text_color)
                line_rect = line_surface.get_rect(center=(self.width//2, y_pos))
                self.screen.blit(line_surface, line_rect)
                y_pos += line_spacing
            
            y_pos += section_spacing
        
        # Back instruction
        back_text = self.small_font.render("Press ESC or ENTER to go back", True, self.selected_color)
        back_rect = back_text.get_rect(center=(self.width//2, self.height - 30))
        self.screen.blit(back_text, back_rect)
    
    def draw_about(self):
        """Draw the about screen"""
        self.screen.fill(self.bg_color)
        
        # Title
        title_text = self.title_font.render("About Reversi42", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width//2, 60))
        self.screen.blit(title_text, title_rect)
        
        # About content
        about_sections = [
            ("GAME RULES", [
                "Goal: Have the most pieces when the board fills",
                "Players alternate placing pieces - must flip at least one",
                "Flipped pieces are sandwiched between your pieces",
                "Game ends when board is full or no moves available"
            ]),
            ("VERSION INFO", [
                "Reversi42 v2.0 - Advanced Reversi/Othello with Bitboard Engine",
                "Ultra-fast AI (50-100x faster) | 57 Opening Book moves",
                "AI Difficulty levels 1-12 available"
            ]),
            ("COPYRIGHT", [
                "Copyright (C) 2011-2025 Luca Amore | GNU GPL v3",
                "Free software - you can redistribute it",
                "Visit: github.com/reversi42"
            ])
        ]
        
        y_pos = 140
        section_spacing = 15
        line_spacing = 22
        
        for section_title, section_lines in about_sections:
            # Draw section title
            section_surface = self.menu_font.render(section_title, True, self.selected_color)
            section_rect = section_surface.get_rect(center=(self.width//2, y_pos))
            self.screen.blit(section_surface, section_rect)
            y_pos += 35
            
            # Draw section content
            for line in section_lines:
                line_surface = self.small_font.render(line, True, self.text_color)
                line_rect = line_surface.get_rect(center=(self.width//2, y_pos))
                self.screen.blit(line_surface, line_rect)
                y_pos += line_spacing
            
            y_pos += section_spacing
        
        # Back instruction
        back_text = self.small_font.render("Press ESC or ENTER to go back", True, self.selected_color)
        back_rect = back_text.get_rect(center=(self.width//2, self.height - 30))
        self.screen.blit(back_text, back_rect)
    
    def handle_mouse_click(self, event):
        """Handle mouse click events"""
        if event.button == 1:  # Left click
            mouse_x, mouse_y = event.pos
            
            if not self.in_submenu:
                # Calculate which menu item was clicked
                start_y = 160
                item_spacing = 50
                
                for i, item in enumerate(self.menu_items):
                    item_y = start_y + i * item_spacing
                    if abs(mouse_y - item_y) < 25:  # Within clickable area
                        self.current_selection = i
                        if item == "Start Game":
                            return "start_game"
                        elif item == "Show Opening":
                            self.show_opening = not self.show_opening
                        elif item == "Help":
                            self.in_help = True
                        elif item == "About":
                            self.in_about = True
                        elif item == "Exit":
                            return "exit"
                        elif item == "Black Player":
                            self.in_submenu = True
                            self.submenu_type = "black_player"
                            self.submenu_selection = self.player_types.index(self.black_player)
                        elif item == "White Player":
                            self.in_submenu = True
                            self.submenu_type = "white_player"
                            self.submenu_selection = self.player_types.index(self.white_player)
                        break
            else:
                # Handle submenu clicks
                start_y = 200
                option_spacing = 45
                
                if "player" in self.submenu_type:
                    options = self.player_types
                else:
                    options = [f"Level {d}" for d in self.difficulties]
                
                for i, option in enumerate(options):
                    option_y = start_y + i * option_spacing
                    if abs(mouse_y - option_y) < 22:  # Within clickable area
                        self.submenu_selection = i
                        if "player" in self.submenu_type:
                            if self.submenu_type == "black_player":
                                self.black_player = self.player_types[self.submenu_selection]
                                # Ask for difficulty for AI players
                                if self.black_player in ["AI", "AI with Opening Book", "AI Bitboard (Ultra-Fast)", "AI Bitboard with Book (Fastest)"]:
                                    self.in_submenu = True
                                    self.submenu_type = "black_difficulty"
                                    self.submenu_selection = self.difficulties.index(self.black_difficulty)
                                else:
                                    self.in_submenu = False
                            elif self.submenu_type == "white_player":
                                self.white_player = self.player_types[self.submenu_selection]
                                # Ask for difficulty for AI players
                                if self.white_player in ["AI", "AI with Opening Book", "AI Bitboard (Ultra-Fast)", "AI Bitboard with Book (Fastest)"]:
                                    self.in_submenu = True
                                    self.submenu_type = "white_difficulty"
                                    self.submenu_selection = self.difficulties.index(self.white_difficulty)
                                else:
                                    self.in_submenu = False
                        else:
                            if self.submenu_type == "black_difficulty":
                                self.black_difficulty = self.difficulties[self.submenu_selection]
                            elif self.submenu_type == "white_difficulty":
                                self.white_difficulty = self.difficulties[self.submenu_selection]
                            self.in_submenu = False
                        break
        
        return None

    def handle_key_event(self, event):
        """Handle keyboard events"""
        if event.type == KEYDOWN:
            if self.in_help:
                # Handle help screen keys
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    self.in_help = False
                return None
            elif self.in_about:
                # Handle about screen keys
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    self.in_about = False
                return None
            elif not self.in_submenu:
                return self.handle_main_menu_key(event)
            else:
                return self.handle_submenu_key(event)
        
        return None
    
    def handle_main_menu_key(self, event):
        """Handle keys in main menu"""
        if event.key == K_UP:
            self.current_selection = (self.current_selection - 1) % len(self.menu_items)
        elif event.key == K_DOWN:
            self.current_selection = (self.current_selection + 1) % len(self.menu_items)
        elif event.key == K_RETURN:
            if self.menu_items[self.current_selection] == "Black Player":
                self.in_submenu = True
                self.submenu_type = "black_player"
                self.submenu_selection = self.player_types.index(self.black_player)
            elif self.menu_items[self.current_selection] == "White Player":
                self.in_submenu = True
                self.submenu_type = "white_player"
                self.submenu_selection = self.player_types.index(self.white_player)
            elif self.menu_items[self.current_selection] == "Show Opening":
                self.show_opening = not self.show_opening
            elif self.menu_items[self.current_selection] == "Start Game":
                return "start_game"
            elif self.menu_items[self.current_selection] == "Help":
                self.in_help = True
            elif self.menu_items[self.current_selection] == "About":
                self.in_about = True
            elif self.menu_items[self.current_selection] == "Exit":
                return "exit"
        elif event.key == K_ESCAPE:
            return "exit"
        
        return None
    
    def handle_submenu_key(self, event):
        """Handle keys in submenu"""
        if event.key == K_UP:
            if "player" in self.submenu_type:
                self.submenu_selection = (self.submenu_selection - 1) % len(self.player_types)
            else:
                self.submenu_selection = (self.submenu_selection - 1) % len(self.difficulties)
        elif event.key == K_DOWN:
            if "player" in self.submenu_type:
                self.submenu_selection = (self.submenu_selection + 1) % len(self.player_types)
            else:
                self.submenu_selection = (self.submenu_selection + 1) % len(self.difficulties)
        elif event.key == K_RETURN:
            if "player" in self.submenu_type:
                if self.submenu_type == "black_player":
                    self.black_player = self.player_types[self.submenu_selection]
                    # Ask for difficulty for AI players
                    if self.black_player in ["AI", "AI with Opening Book", "AI Bitboard (Ultra-Fast)", "AI Bitboard with Book (Fastest)"]:
                        self.in_submenu = True
                        self.submenu_type = "black_difficulty"
                        self.submenu_selection = self.difficulties.index(self.black_difficulty)
                    else:
                        self.in_submenu = False
                elif self.submenu_type == "white_player":
                    self.white_player = self.player_types[self.submenu_selection]
                    # Ask for difficulty for AI players
                    if self.white_player in ["AI", "AI with Opening Book", "AI Bitboard (Ultra-Fast)", "AI Bitboard with Book (Fastest)"]:
                        self.in_submenu = True
                        self.submenu_type = "white_difficulty"
                        self.submenu_selection = self.difficulties.index(self.white_difficulty)
                    else:
                        self.in_submenu = False
            else:
                if self.submenu_type == "black_difficulty":
                    self.black_difficulty = self.difficulties[self.submenu_selection]
                elif self.submenu_type == "white_difficulty":
                    self.white_difficulty = self.difficulties[self.submenu_selection]
                self.in_submenu = False
        elif event.key == K_ESCAPE:
            self.in_submenu = False
        
        return None
    
    def run(self):
        """Run the menu system"""
        # Show splash screen first
        #self.show_splash_screen()
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "exit"
                elif event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                elif event.type == MOUSEBUTTONDOWN:
                    result = self.handle_mouse_click(event)
                    if result == "start_game":
                        return {
                            "black_player": self.black_player,
                            "white_player": self.white_player,
                            "black_difficulty": self.black_difficulty,
                            "white_difficulty": self.white_difficulty,
                            "show_opening": self.show_opening
                        }
                    elif result == "exit":
                        return "exit"
                else:
                    result = self.handle_key_event(event)
                    if result == "start_game":
                        return {
                            "black_player": self.black_player,
                            "white_player": self.white_player,
                            "black_difficulty": self.black_difficulty,
                            "white_difficulty": self.white_difficulty,
                            "show_opening": self.show_opening
                        }
                    elif result == "exit":
                        return "exit"
            
            # Draw current screen
            if self.in_help:
                self.draw_help()
            elif self.in_about:
                self.draw_about()
            elif self.in_submenu:
                self.draw_submenu()
            else:
                self.draw_menu()
            
            pygame.display.flip()
            clock.tick(60)
        
        return "exit"
