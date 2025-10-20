"""
Dialog Widget - Modal dialog component

Modal dialog box for user interaction (messages, confirmations, input).

Design Pattern: Template Method (base dialog with customizable content)
"""

from typing import Optional, List, Callable
import pygame
from ui.widgets.base import Container
from .panel import Panel
from .label import Label
from .button import Button


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
    
    def __init__(self, title: str, message: str,
                 buttons: Optional[List[str]] = None,
                 on_button: Optional[Callable] = None,
                 width: int = 400, height: int = 200):
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
        title_label = Label(self.title, x=20, y=current_y, font_size=28, 
                           color=(240, 240, 245))
        self.add(title_label)
        current_y += 40
        
        # Message (can be multi-line)
        message_lines = self.message.split('\n')
        for line in message_lines:
            msg_label = Label(line, x=20, y=current_y, font_size=20, 
                            color=(200, 200, 210))
            self.add(msg_label)
            current_y += 30
        
        # Buttons
        button_y = self.rect.height - 60
        button_width = 100
        button_spacing = 20
        total_button_width = len(button_labels) * button_width + (len(button_labels) - 1) * button_spacing
        button_x = (self.rect.width - total_button_width) // 2
        
        for btn_label in button_labels:
            btn = Button(btn_label, x=button_x, y=button_y, width=button_width, height=35,
                        on_click=lambda text=btn_label: self._handle_button_click(text))
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

