"""
Abstract Input Handler Interface

Defines the contract for all input handling implementations.
Completely independent of any UI framework.

Architecture: Following Dependency Inversion Principle
Version: 3.1.0
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from enum import Enum


class InputEvent(Enum):
    """
    Standard input events across all view implementations.
    
    Framework-agnostic event types that any input handler can emit.
    """
    QUIT = "quit"              # User wants to quit
    PAUSE = "pause"            # User wants to pause (ESC key)
    SELECT = "select"          # Select current cursor position (ENTER/SPACE)
    CLICK = "click"            # Click at position
    HOVER = "hover"            # Hover over position
    MOVE_UP = "move_up"        # Move cursor up
    MOVE_DOWN = "move_down"    # Move cursor down
    MOVE_LEFT = "move_left"    # Move cursor left
    MOVE_RIGHT = "move_right"  # Move cursor right
    RESIZE = "resize"          # Window/terminal resized
    KEY_PRESS = "key_press"    # Generic key press
    TOGGLE_CURSOR = "toggle_cursor"  # Toggle cursor mode (C key)
    QUIT_DIRECT = "quit_direct"      # Direct quit (Q key)


class AbstractInputHandler(ABC):
    """
    Abstract input handler interface.
    
    Responsibilities:
    - Poll for input events
    - Convert framework-specific events to standard InputEvent
    - Provide pointer/cursor position
    - Non-blocking operation
    
    NOT responsible for:
    - Rendering (that's View's job)
    - Game logic (that's Model's job)
    - Event handling logic (that's Controller's job)
    """
    
    @abstractmethod
    def poll_events(self) -> List[dict]:
        """
        Poll for input events (non-blocking).
        
        Returns:
            List of event dictionaries with structure:
            {
                'type': InputEvent,
                'data': dict  # Event-specific data
            }
            
        Example events:
            {'type': InputEvent.QUIT}
            {'type': InputEvent.CLICK, 'data': {'position': (100, 200)}}
            {'type': InputEvent.KEY_PRESS, 'data': {'key': 'a'}}
        """
        pass
    
    @abstractmethod
    def get_pointer_position(self) -> Optional[Tuple[int, int]]:
        """
        Get current pointer/cursor position in screen coordinates.
        
        Returns:
            (x, y) tuple in screen/pixel coordinates
            None if not applicable (e.g., terminal without cursor)
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if input is available (non-blocking).
        
        Returns:
            True if input can be polled, False otherwise
        """
        pass
    
    def set_blocking(self, blocking: bool):
        """
        Set blocking/non-blocking mode (optional).
        
        Args:
            blocking: True for blocking input, False for non-blocking
        
        Default: non-blocking
        """
        pass
    
    def cleanup(self):
        """
        Cleanup input handler resources (optional).
        
        Called when input handler is no longer needed.
        Should restore terminal state, close connections, etc.
        """
        pass
    
    def get_capabilities(self) -> dict:
        """
        Get input handler capabilities (optional).
        
        Returns:
            Dict with capabilities:
            {
                'has_mouse': bool,
                'has_keyboard': bool,
                'has_touch': bool,
                'supports_hover': bool,
            }
        """
        return {
            'has_mouse': False,
            'has_keyboard': True,
            'has_touch': False,
            'supports_hover': False,
        }

