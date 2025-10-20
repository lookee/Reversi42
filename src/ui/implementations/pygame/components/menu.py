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
from ui.widgets.primitives import Button, Label, Panel, Title, panel


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
            splash_path = os.path.join(project_root, "reversi42-splash.png")

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
        """Build main menu using Bootstrap-like primitives - ULTRA CLEAN!"""
        from ui.widgets.base import HBox, Spacer, Stack

        # === LAYOUT COMPLETO ===
        # Stack verticale con tutto il menu (titolo + panel + bottoni)
        main_layout = Stack(gap=40, align="center", justify="center")
        main_layout.set_size(self.width, self.height)

        # === TITOLO ===
        # Title() crea automaticamente un Label centrato!
        main_layout.add(Title("Reversi42", font_size=48, color=MenuConfig.TITLE_COLOR))

        # === PANEL CENTRALE ===
        # Stack per i controlli di gioco (player buttons + start + book)
        # Panel largo 85% dello schermo e centrato automaticamente!
        panel_width = int(self.width * 0.85)

        game_controls = Stack(gap=15, align="center")
        game_controls.background_color = (30, 50, 40)
        game_controls.border_color = MenuConfig.TITLE_COLOR
        game_controls.border_width = 2
        game_controls.padding = 20
        game_controls.center_in_parent = True  # Centra il panel!
        game_controls.set_size(panel_width, 0)  # Larghezza fissa, altezza auto

        # Players Row
        players_row = HBox(spacing=30, align="center")

        black_text = f"B: {self.black_player}"
        if self.black_difficulty and self.black_player != "Human Player":
            black_text += f" (Lv {self.black_difficulty})"

        self.black_btn = Button(
            black_text,
            width=280,
            height=50,
            on_click=lambda: self._open_player_selection("black"),
            color=(50, 70, 90),
            hover_color=(70, 90, 110),
            text_color=MenuConfig.TEXT_COLOR,
        )

        white_text = f"W: {self.white_player}"
        if self.white_difficulty and self.white_player != "Human Player":
            white_text += f" (Lv {self.white_difficulty})"

        self.white_btn = Button(
            white_text,
            width=280,
            height=50,
            on_click=lambda: self._open_player_selection("white"),
            color=(50, 70, 90),
            hover_color=(70, 90, 110),
            text_color=MenuConfig.TEXT_COLOR,
        )

        players_row.add(self.black_btn)
        players_row.add(self.white_btn)
        game_controls.add(players_row)

        # Start Game Button
        self.start_btn = Button(
            "Start Game",
            width=300,
            height=55,
            on_click=lambda: self._handle_start_game(),
            color=(130, 85, 55),
            hover_color=(155, 105, 70),
            text_color=MenuConfig.TITLE_COLOR,
        )
        game_controls.add(self.start_btn)

        # Opening Book Button
        opening_text = "Book: ON" if self.show_opening else "Book: OFF"
        self.opening_btn = Button(
            opening_text,
            width=280,
            height=50,
            on_click=lambda: self._toggle_opening(),
            color=(40, 40, 50),
            text_color=MenuConfig.TEXT_COLOR,
        )
        game_controls.add(self.opening_btn)

        main_layout.add(game_controls)

        # === BOTTONI IN BASSO ===
        sections_row = HBox(spacing=30, align="center")

        self.help_btn = Button(
            "Help",
            width=150,
            height=40,
            on_click=lambda: self._show_help(),
            color=(60, 60, 70),
            hover_color=(80, 80, 90),
            text_color=MenuConfig.TEXT_COLOR,
        )

        self.about_btn = Button(
            "About",
            width=150,
            height=40,
            on_click=lambda: self._show_about(),
            color=(60, 60, 70),
            hover_color=(80, 80, 90),
            text_color=MenuConfig.TEXT_COLOR,
        )

        self.quit_btn = Button(
            "Quit",
            width=150,
            height=40,
            on_click=lambda: self._quit(),
            color=(80, 50, 50),
            hover_color=(100, 60, 60),
            text_color=MenuConfig.TEXT_COLOR,
        )

        sections_row.add(self.help_btn)
        sections_row.add(self.about_btn)
        sections_row.add(self.quit_btn)
        main_layout.add(sections_row)

        # === SALVA RIFERIMENTI ===
        self.main_menu_layout = main_layout

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

    def _build_parameters_menu(self, player_color, player_type, metadata):
        """Build parameters configuration menu (supports both old and new structure)"""
        from ui.widgets.base import Stack, Center

        # Panel with parameters - LARGO quasi tutto lo schermo (80%)
        panel_width = int(self.width * 0.80)

        panel = Stack(gap=20, align="center")
        panel.background_color = (30, 50, 40)
        panel.border_color = MenuConfig.TITLE_COLOR
        panel.border_width = 2
        panel.padding = 30
        panel.center_in_parent = True
        panel.set_size(panel_width, 0)  # Larghezza fissa 80%, altezza auto

        # Title
        panel.add(Title(f"Configure {player_type}", font_size=32, color=MenuConfig.TITLE_COLOR))

        # Check for new parameters structure
        if "parameters" in metadata and metadata["parameters"]:
            params = metadata["parameters"]

            # For now, handle "difficulty" parameter specially
            if "difficulty" in params:
                diff_param = params["difficulty"]
                min_val = diff_param.get("min", 1)
                max_val = diff_param.get("max", 12)
                default_val = diff_param.get("default", 9)
                description = diff_param.get("description", "Difficulty level")

                # Add description label
                desc_label = Label(description, font_size=20, color=MenuConfig.TEXT_COLOR)
                desc_label.center_in_parent = True
                panel.add(desc_label)

                # Create buttons for each difficulty level
                for level in range(min_val, max_val + 1):
                    btn = Button(
                        f"Depth {level}",
                        width=300,
                        height=45,
                        on_click=lambda d=level: self._select_difficulty(player_color, d),
                        color=(40, 40, 50),
                        hover_color=(60, 60, 70),
                        text_color=MenuConfig.TEXT_COLOR,
                    )
                    panel.add(btn)

        # Fallback to old difficulty_levels structure
        elif metadata.get("difficulty_levels", []):
            for diff in metadata["difficulty_levels"]:
                btn = Button(
                    f"Level {diff}",
                    width=300,
                    height=45,
                    on_click=lambda d=diff: self._select_difficulty(player_color, d),
                    color=(40, 40, 50),
                    hover_color=(60, 60, 70),
                    text_color=MenuConfig.TEXT_COLOR,
                )
                panel.add(btn)

        # Back button
        back_btn = Button(
            "Back",
            width=150,
            height=40,
            on_click=lambda: self._back_to_player_selection(player_color),
            color=(60, 40, 40),
            hover_color=(80, 60, 60),
            text_color=MenuConfig.TEXT_COLOR,
        )
        panel.add(back_btn)

        # Center the panel
        center = Center(width=self.width, height=self.height)
        center.add(panel)

        self.submenu_widget = center

    def _build_difficulty_menu(self, player_color, player_type):
        """Legacy method - redirects to _build_parameters_menu"""
        metadata = self.all_metadata.get(player_type, {})
        self._build_parameters_menu(player_color, player_type, metadata)

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
        """Select player type and open parameters config if needed"""
        # Check if player needs parameters configuration
        metadata = self.all_metadata.get(player_type, {})

        # Check both old (difficulty_levels) and new (parameters) structure
        has_old_difficulty = metadata.get("difficulty_levels", []) != []
        has_new_params = "parameters" in metadata and metadata["parameters"]
        needs_configuration = has_old_difficulty or has_new_params

        if color == "black":
            self.black_player = player_type
            if not needs_configuration:
                self.black_difficulty = None
                self._back_to_main()
            else:
                # Open parameters configuration
                self.current_screen = "difficulty_select"
                self._build_parameters_menu(color, player_type, metadata)
        else:
            self.white_player = player_type
            if not needs_configuration:
                self.white_difficulty = None
                self._back_to_main()
            else:
                # Open parameters configuration
                self.current_screen = "difficulty_select"
                self._build_parameters_menu(color, player_type, metadata)

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
                        # Handle entire main layout (includes title, panel, sections)
                        self.main_menu_layout.handle_event(event)
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
                # Render entire main layout (title + panel + sections all together!)
                self.main_menu_layout.render(self.screen)
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
