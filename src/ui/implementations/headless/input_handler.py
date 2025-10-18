"""
Headless Input Handler

No-op input handler for headless mode.
All methods return empty/None.

Version: 3.1.0
"""

from typing import List, Optional, Tuple
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
from ui.abstractions.input_interface import AbstractInputHandler


class HeadlessInputHandler(AbstractInputHandler):
    """
    Headless input handler - all no-ops.
    
    Used for automated tournaments and testing where no user input exists.
    
    Framework: None
    """
    
    def __init__(self):
        """Initialize headless input handler"""
        self.capabilities = {
            'has_mouse': False,
            'has_keyboard': False,
            'has_touch': False,
            'supports_hover': False,
        }
    
    def poll_events(self) -> List[dict]:
        """No events in headless mode"""
        return []
    
    def get_pointer_position(self) -> Optional[Tuple[int, int]]:
        """No pointer in headless mode"""
        return None
    
    def is_available(self) -> bool:
        """No input available in headless mode"""
        return False
    
    def get_capabilities(self) -> dict:
        """Get headless input capabilities"""
        return self.capabilities.copy()
    
    def cleanup(self):
        """No cleanup needed"""
        pass

