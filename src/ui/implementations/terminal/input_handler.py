"""
Terminal Input Handler

Handles keyboard input for terminal/console mode.
Non-blocking keyboard reading with fallback options.

Version: 3.1.0
"""

import sys
import os
import select
from typing import List, Optional, Tuple

# Try to import readchar for better cross-platform support
try:
    from readchar import readkey, key as readchar_keys
    HAS_READCHAR = True
except ImportError:
    HAS_READCHAR = False
    # Fallback to termios (Unix only)
    try:
        import termios
        import tty
        HAS_TERMIOS = True
    except ImportError:
        HAS_TERMIOS = False

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
from ui.abstractions.input_interface import AbstractInputHandler, InputEvent


class TerminalInputHandler(AbstractInputHandler):
    """
    Terminal keyboard input handling.
    
    Features:
    - Non-blocking keyboard reading
    - Arrow key support
    - Cross-platform (with readchar) or Unix (with termios)
    - No mouse support
    
    Framework: None (terminal stdin)
    """
    
    def __init__(self):
        """Initialize terminal input handler"""
        self.has_readchar = HAS_READCHAR
        self.has_termios = HAS_TERMIOS
        self.pending_events = []
        self.capabilities = {
            'has_mouse': False,
            'has_keyboard': True,
            'has_touch': False,
            'supports_hover': False,
        }
    
    def poll_events(self) -> List[dict]:
        """
        Poll for keyboard events (non-blocking).
        
        Returns:
            List of input events
        """
        if not self.is_available():
            return []
        
        events = []
        
        try:
            key = self._read_key_non_blocking()
            if key:
                event = self._key_to_event(key)
                if event:
                    events.append(event)
        except:
            pass  # Ignore read errors
        
        return events
    
    def _read_key_non_blocking(self) -> Optional[str]:
        """Read single key without blocking"""
        if self.has_readchar:
            # Use readchar (cross-platform)
            try:
                return readkey()
            except:
                return None
        
        elif self.has_termios:
            # Use termios (Unix only)
            if not self._key_available():
                return None
            return self._read_key_termios()
        
        else:
            # No input method available
            return None
    
    def _key_available(self) -> bool:
        """Check if key is available (Unix only)"""
        if not self.has_termios:
            return False
        return select.select([sys.stdin], [], [], 0)[0] != []
    
    def _read_key_termios(self) -> Optional[str]:
        """Read key using termios (Unix only)"""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setcbreak(fd)
            key = sys.stdin.read(1)
            
            # Handle arrow keys (escape sequences)
            if key == '\x1b':  # ESC
                # Try to read next chars for arrow keys
                if self._key_available():
                    next1 = sys.stdin.read(1)
                    if next1 == '[' and self._key_available():
                        next2 = sys.stdin.read(1)
                        return {'A': 'UP', 'B': 'DOWN', 
                               'C': 'RIGHT', 'D': 'LEFT'}.get(next2, '\x1b')
                return '\x1b'  # Just ESC
            
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _key_to_event(self, key: str) -> Optional[dict]:
        """Convert key to InputEvent"""
        # With readchar
        if self.has_readchar:
            if key == readchar_keys.UP or key == 'UP':
                return {'type': InputEvent.MOVE_UP}
            elif key == readchar_keys.DOWN or key == 'DOWN':
                return {'type': InputEvent.MOVE_DOWN}
            elif key == readchar_keys.LEFT or key == 'LEFT':
                return {'type': InputEvent.MOVE_LEFT}
            elif key == readchar_keys.RIGHT or key == 'RIGHT':
                return {'type': InputEvent.MOVE_RIGHT}
            elif key == readchar_keys.ENTER or key in ['\n', '\r']:
                return {'type': InputEvent.SELECT}
            elif key in ['q', 'Q']:
                return {'type': InputEvent.QUIT}
            elif key == '\x1b':  # ESC
                return {'type': InputEvent.PAUSE}
            else:
                return {
                    'type': InputEvent.KEY_PRESS,
                    'data': {'key': key}
                }
        
        # Without readchar (termios)
        else:
            if key == 'UP':
                return {'type': InputEvent.MOVE_UP}
            elif key == 'DOWN':
                return {'type': InputEvent.MOVE_DOWN}
            elif key == 'LEFT':
                return {'type': InputEvent.MOVE_LEFT}
            elif key == 'RIGHT':
                return {'type': InputEvent.MOVE_RIGHT}
            elif key in ['\n', '\r', ' ']:
                return {'type': InputEvent.SELECT}
            elif key in ['q', 'Q']:
                return {'type': InputEvent.QUIT}
            elif key == '\x1b':
                return {'type': InputEvent.PAUSE}
            else:
                return {
                    'type': InputEvent.KEY_PRESS,
                    'data': {'key': key}
                }
    
    def get_pointer_position(self) -> Optional[Tuple[int, int]]:
        """Terminal has no pointer/mouse"""
        return None
    
    def is_available(self) -> bool:
        """Check if terminal input is available"""
        if self.has_readchar:
            return True  # readchar handles this
        elif self.has_termios:
            return self._key_available()
        else:
            return False  # No input method available
    
    def get_capabilities(self) -> dict:
        """Get terminal input capabilities"""
        return self.capabilities.copy()
    
    def cleanup(self):
        """No cleanup needed for terminal input"""
        pass

