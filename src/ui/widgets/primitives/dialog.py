"""
Dialog Widget - Modal dialog component

Modal dialog box for user interaction (messages, confirmations, input).

Design Pattern: Template Method (base dialog with customizable content)

Includes:
- Dialog: Basic message/confirmation dialog
- InputDialog: Text input dialog  
- ListDialog: List selection dialog
"""

from typing import Callable, List, Optional

import pygame

from ui.widgets.base import Container

from .button import Button
from .input_box import InputBox
from .label import Label
from .panel import Panel


class Dialog(Panel):
    """
    Modal dialog widget.

    Features:
    - Modal overlay (blocks interaction behind)
    - Title and message
    - Buttons (OK, Cancel, Yes/No, etc.)
    - Auto-centering
    - ESC to close

    Usage:
        dialog = Dialog(title="Confirm", message="Are you sure?",
                       buttons=["Yes", "No"], on_button=handle_choice)
        dialog.show_modal(screen)
    """

    def __init__(
        self,
        title: str,
        message: str,
        buttons: Optional[List[str]] = None,
        on_button: Optional[Callable] = None,
        width: int = 400,
        height: int = 200,
    ):
        """
        Initialize dialog.

        Args:
            title: Dialog title
            message: Dialog message
            buttons: List of button labels
            on_button: Callback(button_text) when button clicked
            width, height: Dialog size
        """
        super().__init__(0, 0, width, height)

        self.title = title
        self.message = message
        self.on_button = on_button
        self.result = None
        self.modal_active = False

        # Styling
        self.background_color = (40, 40, 50)
        self.border_color = (100, 100, 120)
        self.overlay_color = (0, 0, 0, 180)  # Semi-transparent black

        # Build dialog content
        self._build_content(buttons or ["OK"])

    def _build_content(self, button_labels: List[str]):
        """
        Build dialog content (title, message, buttons).

        Args:
            button_labels: List of button labels
        """
        self.clear()

        current_y = 20

        # Title
        title_label = Label(self.title, x=20, y=current_y, font_size=28, color=(240, 240, 245))
        self.add(title_label)
        current_y += 40

        # Message (can be multi-line)
        message_lines = self.message.split("\n")
        for line in message_lines:
            msg_label = Label(line, x=20, y=current_y, font_size=20, color=(200, 200, 210))
            self.add(msg_label)
            current_y += 30

        # Buttons
        button_y = self.rect.height - 60
        button_width = 100
        button_spacing = 20
        total_button_width = (
            len(button_labels) * button_width + (len(button_labels) - 1) * button_spacing
        )
        button_x = (self.rect.width - total_button_width) // 2

        for btn_label in button_labels:
            btn = Button(
                btn_label,
                x=button_x,
                y=button_y,
                width=button_width,
                height=35,
                on_click=lambda text=btn_label: self._handle_button_click(text),
            )
            self.add(btn)
            button_x += button_width + button_spacing

    def _handle_button_click(self, button_text: str):
        """
        Handle button click.

        Args:
            button_text: Text of clicked button
        """
        self.result = button_text
        self.modal_active = False

        if self.on_button:
            self.on_button(button_text)

    def show_modal(self, screen: pygame.Surface) -> str:
        """
        Show dialog modally (blocking).

        Args:
            screen: Pygame screen surface

        Returns:
            Button text that was clicked
        """
        self.modal_active = True
        self.result = None

        # Center dialog
        self.rect.center = screen.get_rect().center

        clock = pygame.time.Clock()

        while self.modal_active:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.result = "Cancel"
                    self.modal_active = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.result = "Cancel"
                    self.modal_active = False
                else:
                    self.handle_event(event)

            # Render overlay
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill(self.overlay_color)
            screen.blit(overlay, (0, 0))

            # Render dialog
            self.render(screen)

            pygame.display.flip()
            clock.tick(60)

        return self.result or "Cancel"


class InputDialog(Dialog):
    """
    Text input dialog widget.

    Usage:
        dialog = InputDialog(title="Save Game", prompt="Enter filename:",
                            default_text="game_001")
        result = dialog.show_modal(screen)  # Returns text or None if cancelled
    """

    def __init__(
        self,
        title: str = "Input",
        prompt: str = "Enter text:",
        default_text: str = "",
        width: int = 500,
        height: int = 200,
    ):
        """
        Initialize input dialog.

        Args:
            title: Dialog title
            prompt: Prompt message
            default_text: Default input text
            width, height: Dialog size
        """
        self.prompt = prompt
        self.default_text = default_text
        self.input_box = None

        # Call parent with dummy message (will rebuild)
        super().__init__(
            title=title, message="", buttons=["OK", "Cancel"], width=width, height=height
        )

    def _build_content(self, button_labels: List[str]):
        """Build input dialog content with InputBox."""
        self.clear()

        current_y = 20

        # Title
        title_label = Label(self.title, x=20, y=current_y, font_size=28, color=(240, 240, 245))
        self.add(title_label)
        current_y += 40

        # Prompt
        prompt_label = Label(self.prompt, x=20, y=current_y, font_size=20, color=(200, 200, 210))
        self.add(prompt_label)
        current_y += 35

        # Input box
        self.input_box = InputBox(
            x=20, y=current_y, width=self.rect.width - 40, height=40, default_text=self.default_text
        )
        self.add(self.input_box)
        current_y += 50

        # Instructions
        inst_label = Label(
            "ENTER: OK | ESC: Cancel | Backspace: Delete",
            x=20,
            y=current_y,
            font_size=14,
            color=(150, 150, 160),
        )
        self.add(inst_label)

        # Buttons
        button_y = self.rect.height - 60
        button_width = 100
        button_spacing = 20
        total_button_width = (
            len(button_labels) * button_width + (len(button_labels) - 1) * button_spacing
        )
        button_x = (self.rect.width - total_button_width) // 2

        for btn_label in button_labels:
            btn = Button(
                btn_label,
                x=button_x,
                y=button_y,
                width=button_width,
                height=35,
                on_click=lambda text=btn_label: self._handle_button_click(text),
            )
            self.add(btn)
            button_x += button_width + button_spacing

    def _handle_button_click(self, button_text: str):
        """Handle button click - get input text."""
        if button_text == "OK":
            self.result = self.input_box.text if self.input_box else ""
        else:
            self.result = None
        self.modal_active = False

    def handle_event(self, event: pygame.event.Event):
        """Handle keyboard events (ENTER submits)."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.result = self.input_box.text if self.input_box else ""
                self.modal_active = False
                return

        # Pass to children (InputBox handles typing)
        super().handle_event(event)


class ListDialog(Dialog):
    """
    List selection dialog widget.

    Usage:
        dialog = ListDialog(title="Load Game",
                           items=["game1.xot", "game2.xot"],
                           allow_cancel=True)
        result = dialog.show_modal(screen)  # Returns selected index or None
    """

    def __init__(
        self,
        title: str = "Select",
        items: Optional[List[str]] = None,
        allow_cancel: bool = True,
        width: int = 600,
        height: int = 500,
    ):
        """
        Initialize list dialog.

        Args:
            title: Dialog title
            items: List of items to display
            allow_cancel: Add Cancel option
            width, height: Dialog size
        """
        self.items = items or []
        self.allow_cancel = allow_cancel
        self.selected_index = 0
        self.item_buttons = []

        # Call parent with dummy message (will rebuild)
        super().__init__(title=title, message="", buttons=[], width=width, height=height)

    def _build_content(self, button_labels: List[str]):
        """Build list dialog content with selectable items."""
        self.clear()
        self.item_buttons = []

        current_y = 20

        # Title
        title_label = Label(self.title, x=20, y=current_y, font_size=28, color=(240, 240, 245))
        self.add(title_label)
        current_y += 50

        # Items (scrollable if too many)
        max_visible = 8
        item_height = 40
        item_spacing = 5

        display_items = self.items[:]
        if self.allow_cancel:
            display_items.append("Cancel")

        visible_items = display_items[:max_visible]

        for idx, item in enumerate(visible_items):
            # Truncate long items
            display_item = item if len(item) <= 50 else item[:47] + "..."

            is_selected = idx == self.selected_index
            btn_color = (255, 215, 0) if is_selected else (100, 100, 120)
            text_color = (20, 20, 30) if is_selected else (200, 200, 210)

            btn = Button(
                display_item,
                x=20,
                y=current_y,
                width=self.rect.width - 40,
                height=item_height,
                on_click=lambda i=idx: self._handle_item_click(i),
                color=btn_color,
                text_color=text_color,
            )
            self.add(btn)
            self.item_buttons.append(btn)
            current_y += item_height + item_spacing

        # Show scroll indicator if needed
        if len(display_items) > max_visible:
            scroll_label = Label(
                f"Showing {max_visible} of {len(display_items)} items",
                x=20,
                y=current_y,
                font_size=14,
                color=(150, 150, 160),
            )
            self.add(scroll_label)
            current_y += 25

        # Instructions
        inst_label = Label(
            "Arrows: Navigate | ENTER: Select | ESC: Cancel",
            x=20,
            y=self.rect.height - 50,
            font_size=14,
            color=(150, 150, 160),
        )
        self.add(inst_label)

    def _handle_item_click(self, index: int):
        """Handle item click."""
        display_items = self.items[:]
        if self.allow_cancel:
            display_items.append("Cancel")

        if self.allow_cancel and index == len(self.items):
            self.result = None  # Cancel
        else:
            self.result = index

        self.modal_active = False

    def handle_event(self, event: pygame.event.Event):
        """Handle keyboard navigation."""
        if event.type == pygame.KEYDOWN:
            display_items = self.items[:]
            if self.allow_cancel:
                display_items.append("Cancel")

            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(display_items)
                self._rebuild_list()
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(display_items)
                self._rebuild_list()
            elif event.key == pygame.K_RETURN:
                self._handle_item_click(self.selected_index)
                return

        # Pass to children
        super().handle_event(event)

    def _rebuild_list(self):
        """Rebuild list to update selection highlighting."""
        self._build_content([])
