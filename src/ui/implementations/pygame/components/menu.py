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
Menu - Refactored using Widget System

Reduces from 713 LoC → ~250 LoC by using reusable widgets!

Design Pattern: Composite (VBox + Buttons + Panels) + State Machine
"""

import os

import pygame
from pygame.locals import *

from core.config import MenuConfig
from Players.PlayerFactory import PlayerFactory
from ui.widgets.base import HBox, VBox
from ui.widgets.primitives import Button, Label, Panel, panel


class Menu:
    """
    Main menu using widget system.

    Reduced from 713 LoC to ~250 LoC!

    Maintains backward compatible API:
    - Same __init__(width, height)
    - Same run() → returns dict with player selections
    """

    def __init__(self, width=None, height=None):
        # Use config defaults
        self.width = width or MenuConfig.DEFAULT_WIDTH
        self.height = height or MenuConfig.DEFAULT_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(MenuConfig.WINDOW_TITLE)

        # Theme from config
        self.bg_color = MenuConfig.BG_COLOR

        # State
        self.current_screen = "main"  # "main", "player_select", "help", "about"
        self.submenu_type = None  # For player selection
        self.result = None

        # Player selections
        self.black_player = MenuConfig.DEFAULT_BLACK_PLAYER
        self.white_player = MenuConfig.DEFAULT_WHITE_PLAYER
        self.black_difficulty = MenuConfig.DEFAULT_BLACK_DIFFICULTY
        self.white_difficulty = MenuConfig.DEFAULT_WHITE_DIFFICULTY
        self.show_opening = MenuConfig.DEFAULT_SHOW_OPENING

        # Player metadata
        self.player_types = PlayerFactory.get_available_player_types()
        self.all_metadata = PlayerFactory.get_all_player_metadata()
        self.difficulties = MenuConfig.DIFFICULTY_LEVELS

        # Widgets (built on demand)
        self.main_menu_widget = None
        self.submenu_widget = None
        self.help_widget = None
        self.about_widget = None

        # Splash
        self.splash_image = None
        self._load_splash()

    def _load_splash(self):
        """Load splash screen image"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
            )
            splash_path = os.path.join(project_root, "Images", "reversi42-splash.png")

            if os.path.exists(splash_path):
                original = pygame.image.load(splash_path)
                img_w, img_h = original.get_size()
                aspect = img_w / img_h

                if self.width / self.height > aspect:
                    new_h = self.height
                    new_w = int(new_h * aspect)
                else:
                    new_w = self.width
                    new_h = int(new_w / aspect)

                self.splash_image = pygame.transform.scale(original, (new_w, new_h))
        except Exception as e:
            print(f"Splash load error: {e}")

    def show_splash_screen(self):
        """Show splash for 3 seconds"""
        self.screen.fill(self.bg_color)

        if self.splash_image:
            img_w, img_h = self.splash_image.get_size()
            x = (self.width - img_w) // 2
            y = (self.height - img_h) // 2
            self.screen.blit(self.splash_image, (x, y))
        else:
            # Fallback
            font = pygame.font.Font(None, 72)
            text = font.render("Reversi42", True, MenuConfig.TITLE_COLOR)
            rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, rect)

        pygame.display.flip()
        pygame.time.wait(3000)

    def _build_main_menu(self):
        """Build main menu widget with custom layout"""
        # Create LARGER main panel (wider and taller)
        panel_width = self.width - 100  # Much wider (was -200)
        panel_height = self.height - 200  # Taller (was -300)
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height - 80) // 2 + 10  # Leave space for title above and buttons below
        
        self.main_menu_panel = Panel(x=panel_x, y=panel_y, width=panel_width, height=panel_height)
        self.main_menu_panel.background_color = (30, 50, 40)
        self.main_menu_panel.border_color = MenuConfig.TITLE_COLOR
        
        # Title - ABOVE the panel, aligned with panel's left edge
        title_x = panel_x + 20  # Align with panel's left border
        title_y = panel_y - 60  # Above the panel
        self.title_label = Label("Reversi42", x=title_x, y=title_y, font_size=40, color=MenuConfig.TITLE_COLOR)
        
        # Calculate relative positions within panel
        content_start_y = 60  # More space from top
        
        # LARGER buttons positioned more to the right
        button_width = 250  # Much wider (was 250)
        button_y = content_start_y + 120  # Below title
        spacing = 40  # More spacing between buttons
        
        # Calculate position for player buttons (shifted more to the right)
        total_width = button_width * 2 + spacing
        start_x = (panel_width - total_width) // 2 + 100  # Shift 100px to the right (was 80)
        
        # Black Player (centered left) - using B for Black
        black_piece = "⚫"  # Black circle
        black_text = f"B: {self.black_player}"
        # Only show level for AI players, not for Human Player
        if self.black_difficulty and self.black_player != "Human Player":
            black_text += f" (Lv {self.black_difficulty})"
        self.black_btn = Button(
            black_text,
            x=start_x,
            y=button_y,
            width=button_width,
            height=60,  # Taller button
            on_click=lambda: self._open_player_selection("black"),
            color=(50, 70, 90),  # Blu tendente al grigio
            hover_color=(70, 90, 110),  # Blu più chiaro per hover
            text_color=MenuConfig.TEXT_COLOR,
        )
        self.main_menu_panel.add(self.black_btn)
        
        # White Player (centered right) - using W for White
        white_piece = "⚪"  # White circle
        white_text = f"W: {self.white_player}"
        # Only show level for AI players, not for Human Player
        if self.white_difficulty and self.white_player != "Human Player":
            white_text += f" (Lv {self.white_difficulty})"
        self.white_btn = Button(
            white_text,
            x=start_x + button_width + spacing,
            y=button_y,
            width=button_width,
            height=60,  # Taller button
            on_click=lambda: self._open_player_selection("white"),
            color=(50, 70, 90),  # Blu tendente al grigio
            hover_color=(70, 90, 110),  # Blu più chiaro per hover
            text_color=MenuConfig.TEXT_COLOR,
        )
        self.main_menu_panel.add(self.white_btn)
        
        # Start Game button (larger, more to the right, lower)
        start_btn_width = 400  # Much wider (was 300)
        self.start_btn = Button(
            "Start Game",
            x=(panel_width - start_btn_width) // 2 + 100,  # Shift 100px to the right (was 80)
            y=button_y + 140,  # Lower position
            width=start_btn_width,
            height=60,  # Taller (was 55)
            on_click=lambda: self._handle_start_game(),
            color=(130, 85, 55),  # Arancione tendente al grigio
            hover_color=(155, 105, 70),  # Arancione più chiaro per hover
            text_color=MenuConfig.TITLE_COLOR,
        )
        self.main_menu_panel.add(self.start_btn)
        
        # Opening Book toggle (larger, more to the right, lower)
        opening_text = "Book: ON" if self.show_opening else "Book: OFF"
        opening_btn_width = 380  # Wider (was 280)
        self.opening_btn = Button(
            opening_text,
            x=(panel_width - opening_btn_width) // 2 + 100,  # Shift 100px to the right (was 80)
            y=button_y + 240,  # Lower position
            width=opening_btn_width,
            height=60,  # Taller (was 45)
            on_click=lambda: self._toggle_opening(),
            color=(40, 40, 50),
            text_color=MenuConfig.TEXT_COLOR,
        )
        self.main_menu_panel.add(self.opening_btn)
        
        # Bottom buttons (Help, About, Quit) - centered at bottom of screen
        button_y = self.height - 80
        button_width = 150
        spacing = 30
        total_button_width = button_width * 3 + spacing * 2
        start_x = (self.width - total_button_width) // 2
        
        self.help_btn = Button(
            "Help",
            x=start_x,
            y=button_y,
            width=button_width,
            height=40,
            on_click=lambda: self._show_help(),
            color=(40, 40, 50),
            text_color=MenuConfig.TEXT_COLOR,
        )
        
        self.about_btn = Button(
            "About",
            x=start_x + button_width + spacing,
            y=button_y,
            width=button_width,
            height=40,
            on_click=lambda: self._show_about(),
            color=(40, 40, 50),
            text_color=MenuConfig.TEXT_COLOR,
        )
        
        self.quit_btn = Button(
            "Quit",
            x=start_x + (button_width + spacing) * 2,
            y=button_y,
            width=button_width,
            height=40,
            on_click=lambda: self._quit(),
            color=(60, 40, 40),
            text_color=MenuConfig.TEXT_COLOR,
        )

    def _build_player_selection_menu(self, player_color):
        """Build player selection submenu"""
        panel_width = 500
        panel_height = 500
        self.submenu_widget = Panel(x=150, y=100, width=panel_width, height=panel_height)
        self.submenu_widget.background_color = (30, 50, 40)
        self.submenu_widget.border_color = MenuConfig.TITLE_COLOR

        # Title (centered)
        title = Label(
            f"Select {player_color.capitalize()} Player",
            x=0,
            y=20,
            font_size=36,
            color=MenuConfig.TITLE_COLOR,
        )
        title.x = (panel_width - 350) // 2  # Center title
        self.submenu_widget.add(title)

        # Player type buttons (centered)
        button_width = 400
        button_x = (panel_width - button_width) // 2  # Center buttons
        y_pos = 80
        
        for player_type in self.player_types:
            btn = Button(
                player_type,
                x=button_x,
                y=y_pos,
                width=button_width,
                height=45,
                on_click=lambda pt=player_type: self._select_player_type(player_color, pt),
                color=(40, 40, 50),
                text_color=MenuConfig.TEXT_COLOR,
            )
            self.submenu_widget.add(btn)
            y_pos += 55

        # Back button (centered)
        back_btn = Button(
            "Back",
            x=(panel_width - 150) // 2,
            y=panel_height - 70,
            width=150,
            height=40,
            on_click=lambda: self._back_to_main(),
            color=(60, 40, 40),
            text_color=MenuConfig.TEXT_COLOR,
        )
        self.submenu_widget.add(back_btn)

    def _build_difficulty_menu(self, player_color, player_type):
        """Build difficulty selection submenu"""
        panel_width = 400
        panel_height = 400
        self.submenu_widget = Panel(x=200, y=150, width=panel_width, height=panel_height)
        self.submenu_widget.background_color = (30, 50, 40)
        self.submenu_widget.border_color = MenuConfig.TITLE_COLOR

        # Title (centered)
        title = Label(
            f"Select Difficulty for {player_type}",
            x=0,
            y=20,
            font_size=28,
            color=MenuConfig.TITLE_COLOR,
        )
        title.x = (panel_width - 300) // 2  # Center title
        self.submenu_widget.add(title)

        # Difficulty buttons (centered)
        button_width = 300
        button_x = (panel_width - button_width) // 2  # Center buttons
        y_pos = 80
        
        for diff in self.difficulties:
            btn = Button(
                f"Level {diff}",
                x=button_x,
                y=y_pos,
                width=button_width,
                height=45,
                on_click=lambda d=diff: self._select_difficulty(player_color, d),
                color=(40, 40, 50),
                text_color=MenuConfig.TEXT_COLOR,
            )
            self.submenu_widget.add(btn)
            y_pos += 55

        # Back button (centered)
        back_btn = Button(
            "Back",
            x=(panel_width - 150) // 2,
            y=panel_height - 70,
            width=150,
            height=40,
            on_click=lambda: self._back_to_player_selection(player_color),
            color=(60, 40, 40),
            text_color=MenuConfig.TEXT_COLOR,
        )
        self.submenu_widget.add(back_btn)

    def _build_help_screen(self):
        """Build help screen"""
        self.help_widget = Panel(x=50, y=50, width=self.width - 100, height=self.height - 100)
        self.help_widget.background_color = (30, 50, 40)
        self.help_widget.border_color = MenuConfig.TITLE_COLOR

        # Title
        title = Label("Help", x=60, y=20, font_size=48, color=MenuConfig.TITLE_COLOR)
        self.help_widget.add(title)

        # Help text (multiline)
        help_lines = [
            "Game Rules:",
            "• Place discs to capture opponent's pieces",
            "• Must flip at least one opponent disc per move",
            "• Player with most discs wins",
            "",
            "Controls:",
            "• Mouse: Click to place disc",
            "• ESC: Pause game",
            "• Arrow keys: Navigate menus",
        ]

        y_pos = 80
        for line in help_lines:
            label = Label(line, x=80, y=y_pos, font_size=24, color=MenuConfig.TEXT_COLOR)
            self.help_widget.add(label)
            y_pos += 35

        # Back button
        back_btn = Button(
            "Back",
            x=80,
            y=self.height - 150,
            width=150,
            height=40,
            on_click=lambda: self._back_to_main(),
            color=(60, 40, 40),
            text_color=MenuConfig.TEXT_COLOR,
        )
        self.help_widget.add(back_btn)

    def _build_about_screen(self):
        """Build about screen"""
        self.about_widget = Panel(x=50, y=50, width=self.width - 100, height=self.height - 100)
        self.about_widget.background_color = (30, 50, 40)
        self.about_widget.border_color = MenuConfig.TITLE_COLOR

        # Title
        title = Label("About Reversi42", x=60, y=20, font_size=48, color=MenuConfig.TITLE_COLOR)
        self.about_widget.add(title)

        # About text
        about_lines = [
            "Reversi42 - Professional Reversi/Othello Game",
            "",
            "Features:",
            "• Advanced AI (Apocalyptron Engine)",
            "• Opening book with 644 positions",
            "• Multiple difficulty levels",
            "• Professional tournament interface",
            "",
            "© 2011-2025 Luca Amore",
            "Licensed under GPLv3",
        ]

        y_pos = 90
        for line in about_lines:
            label = Label(line, x=80, y=y_pos, font_size=24, color=MenuConfig.TEXT_COLOR)
            self.about_widget.add(label)
            y_pos += 35

        # Back button
        back_btn = Button(
            "Back",
            x=80,
            y=self.height - 150,
            width=150,
            height=40,
            on_click=lambda: self._back_to_main(),
            color=(60, 40, 40),
            text_color=MenuConfig.TEXT_COLOR,
        )
        self.about_widget.add(back_btn)

    # Action handlers
    def _handle_start_game(self):
        """Start game with current selections"""
        self.result = {
            "action": "start",
            "black_player": self.black_player,
            "white_player": self.white_player,
            "black_difficulty": self.black_difficulty,
            "white_difficulty": self.white_difficulty,
            "show_opening": self.show_opening,
        }

    def _open_player_selection(self, color):
        """Open player selection submenu"""
        self.current_screen = "player_select"
        self.submenu_type = color
        self._build_player_selection_menu(color)

    def _select_player_type(self, color, player_type):
        """Select player type and open difficulty if needed"""
        # Check if player needs difficulty
        metadata = self.all_metadata.get(player_type, {})
        needs_difficulty = metadata.get("difficulty_levels", []) != []

        if color == "black":
            self.black_player = player_type
            if not needs_difficulty:
                self.black_difficulty = None
                self._back_to_main()
            else:
                # Open difficulty selection
                self.current_screen = "difficulty_select"
                self._build_difficulty_menu(color, player_type)
        else:
            self.white_player = player_type
            if not needs_difficulty:
                self.white_difficulty = None
                self._back_to_main()
            else:
                # Open difficulty selection
                self.current_screen = "difficulty_select"
                self._build_difficulty_menu(color, player_type)

    def _select_difficulty(self, color, difficulty):
        """Select difficulty and return to main"""
        if color == "black":
            self.black_difficulty = difficulty
        else:
            self.white_difficulty = difficulty
        self._back_to_main()

    def _back_to_player_selection(self, color):
        """Back to player selection from difficulty"""
        self.current_screen = "player_select"
        self._build_player_selection_menu(color)

    def _toggle_opening(self):
        """Toggle opening book display"""
        self.show_opening = not self.show_opening
        self._build_main_menu()  # Rebuild to update text

    def _show_help(self):
        """Show help screen"""
        self.current_screen = "help"
        self._build_help_screen()

    def _show_about(self):
        """Show about screen"""
        self.current_screen = "about"
        self._build_about_screen()

    def _back_to_main(self):
        """Return to main menu"""
        self.current_screen = "main"
        self._build_main_menu()

    def _quit(self):
        """Quit application"""
        self.result = {"action": "quit"}

    def run(self):
        """
        Run the menu (backward compatible API).

        Returns:
            dict with player selections or None if quit
        """
        # Show splash (disabled for faster startup)
        # self.show_splash_screen()

        # Build initial menu
        self._build_main_menu()

        # Main loop
        clock = pygame.time.Clock()
        self.result = None

        while self.result is None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                elif event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                    self.screen = pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE
                    )
                    # Rebuild current screen
                    if self.current_screen == "main":
                        self._build_main_menu()
                    # TODO: rebuild other screens on resize
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.current_screen != "main":
                            self._back_to_main()
                else:
                    # Pass event to current widget
                    if self.current_screen == "main":
                        # Handle title (above panel)
                        self.title_label.handle_event(event)
                        # Handle panel (contains all main menu widgets)
                        self.main_menu_panel.handle_event(event)
                        # Also handle bottom buttons (outside panel)
                        self.help_btn.handle_event(event)
                        self.about_btn.handle_event(event)
                        self.quit_btn.handle_event(event)
                    elif (
                        self.current_screen in ["player_select", "difficulty_select"]
                        and self.submenu_widget
                    ):
                        self.submenu_widget.handle_event(event)
                    elif self.current_screen == "help" and self.help_widget:
                        self.help_widget.handle_event(event)
                    elif self.current_screen == "about" and self.about_widget:
                        self.about_widget.handle_event(event)

            # Render
            self.screen.fill(self.bg_color)

            if self.current_screen == "main":
                # Render title (above panel)
                self.title_label.render(self.screen)
                # Render main menu panel
                self.main_menu_panel.render(self.screen)
                # Render bottom buttons (outside panel)
                self.help_btn.render(self.screen)
                self.about_btn.render(self.screen)
                self.quit_btn.render(self.screen)
            elif (
                self.current_screen in ["player_select", "difficulty_select"]
                and self.submenu_widget
            ):
                self.submenu_widget.render(self.screen)
            elif self.current_screen == "help" and self.help_widget:
                self.help_widget.render(self.screen)
            elif self.current_screen == "about" and self.about_widget:
                self.about_widget.render(self.screen)

            pygame.display.flip()
            clock.tick(60)

        # Return result (backward compatible)
        if self.result["action"] == "quit":
            return None

        return self.result
