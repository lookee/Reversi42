"""
Pygame Input Handler

Handles all Pygame-specific input (mouse, keyboard, window events).
Converts Pygame events to standard InputEvent format.

Version: 3.1.0
"""

import pygame
from pygame.locals import *
from typing import List, Optional, Tuple

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from ui.abstractions.input_interface import AbstractInputHandler, InputEvent


class PygameInputHandler(AbstractInputHandler):
    """
    Pygame-specific input handling.
    
    Responsibilities:
    - Poll pygame events
    - Convert to standard InputEvent format
    - Provide mouse position
    - Handle window events
    
    Framework: Pygame
    """
    
    def __init__(self):
        """Initialize Pygame input handler"""
        self.last_mouse_pos = (0, 0)
        self.capabilities = {
            'has_mouse': True,
            'has_keyboard': True,
            'has_touch': False,
            'supports_hover': True,
        }
    
    def poll_events(self) -> List[dict]:
        """
        Poll Pygame events and convert to standard format.
        
        Returns:
            List of standardized event dictionaries
        """
        events = []
        
        # Check if pygame is initialized
        if not pygame.get_init():
            return []
        
        try:
            for event in pygame.event.get():
                # Quit event
                if event.type == QUIT:
                    events.append({'type': InputEvent.QUIT})
                
                # Keyboard events
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        events.append({'type': InputEvent.PAUSE})
                    elif event.key == K_q:
                        events.append({'type': InputEvent.QUIT})
                    elif event.key == K_UP:
                        events.append({'type': InputEvent.MOVE_UP})
                    elif event.key == K_DOWN:
                        events.append({'type': InputEvent.MOVE_DOWN})
                    elif event.key == K_LEFT:
                        events.append({'type': InputEvent.MOVE_LEFT})
                    elif event.key == K_RIGHT:
                        events.append({'type': InputEvent.MOVE_RIGHT})
                    elif event.key in [K_RETURN, K_SPACE]:
                        events.append({'type': InputEvent.SELECT})
                    else:
                        # Generic key press
                        events.append({
                            'type': InputEvent.KEY_PRESS,
                            'data': {
                                'key': event.key,
                                'unicode': event.unicode,
                                'mod': event.mod
                            }
                        })
                
                # Mouse events
                elif event.type == MOUSEBUTTONDOWN:
                    self.last_mouse_pos = event.pos
                    events.append({
                        'type': InputEvent.CLICK,
                        'data': {
                            'position': event.pos,
                            'button': event.button
                        }
                    })
                
                elif event.type == MOUSEMOTION:
                    self.last_mouse_pos = event.pos
                    events.append({
                        'type': InputEvent.HOVER,
                        'data': {'position': event.pos}
                    })
                
                # Window events
                elif event.type == VIDEORESIZE:
                    events.append({
                        'type': InputEvent.RESIZE,
                        'data': {
                            'width': event.w,
                            'height': event.h
                        }
                    })
        
        except Exception:
            # Handle any pygame errors gracefully
            pass
        
        return events
    
    def get_pointer_position(self) -> Optional[Tuple[int, int]]:
        """Get current mouse position"""
        if not pygame.get_init():
            return self.last_mouse_pos
        
        try:
            return pygame.mouse.get_pos()
        except:
            return self.last_mouse_pos
    
    def is_available(self) -> bool:
        """Pygame input is always available when initialized"""
        return pygame.get_init()
    
    def get_capabilities(self) -> dict:
        """Get Pygame input capabilities"""
        return self.capabilities.copy()
    
    def cleanup(self):
        """No cleanup needed for Pygame input"""
        pass
