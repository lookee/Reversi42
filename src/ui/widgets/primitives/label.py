"""
Label Widget - Text display component

Simple text label with customizable font, size, and color.

Design Pattern: Component
"""

from typing import Tuple, Optional
import pygame
from ui.widgets.base import Widget


class Label(Widget):
    """
    Text label widget.
    
    Features:
    - Customizable font and size
    - Text alignment
    - Color support
    - Auto-sizing
    
    Usage:
        label = Label("Score: 34")
        label.render(surface)
    """
    
    def __init__(self, text: str, x: int = 0, y: int = 0, 
                 font_size: int = 24, color: Tuple[int, int, int] = (240, 240, 245)):
        """
        Initialize label.
        
        Args:
            text: Label text
            x, y: Position
            font_size: Font size in pixels
            color: Text color (RGB)
        """
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.bold = False
        self.italic = False
        
        # Calculate size from text
        text_surface = self.font.render(text, True, color)
        width, height = text_surface.get_size()
        
        super().__init__(x, y, width, height)
    
    def render(self, surface: pygame.Surface):
        """Render label."""
        if not self.visible:
            return
        
        # Render text
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, (self.rect.x, self.rect.y))
    
    def set_text(self, text: str):
        """
        Update label text and resize.
        
        Args:
            text: New text
        """
        self.text = text
        text_surface = self.font.render(text, True, self.color)
        self.rect.width, self.rect.height = text_surface.get_size()
    
    def set_color(self, color: Tuple[int, int, int]):
        """
        Set text color.
        
        Args:
            color: RGB color tuple
        """
        self.color = color
    
    def set_font_size(self, size: int):
        """
        Set font size.
        
        Args:
            size: Font size in pixels
        """
        self.font_size = size
        self.font = pygame.font.Font(None, size)
        # Recalculate size
        self.set_text(self.text)

