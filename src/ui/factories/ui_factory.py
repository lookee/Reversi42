"""
UI Factory

Creates complete UI stacks (Controller + View + InputHandler).
High-level factory for easy UI creation.

Version: 3.1.0
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from ui.core.model import BoardModel
from ui.core.state import GameState
from ui.core.controller import BoardController
from ui.implementations.pygame.input_handler import PygameInputHandler
from ui.implementations.terminal.input_handler import TerminalInputHandler
from ui.implementations.headless.input_handler import HeadlessInputHandler
from ui.factories.view_factory import ViewFactory


class UIFactory:
    """
    High-level factory for creating complete UI stacks.
    
    Creates Model + View + InputHandler + Controller in one call.
    """
    
    @staticmethod
    def create_ui(view_type: str, width: int = 8, height: int = 8,
                  window_width: int = 800, window_height: int = 600):
        """
        Create complete UI stack for specified view type.
        
        Args:
            view_type: 'pygame', 'terminal', or 'headless'
            width: Board width
            height: Board height
            window_width: Display width
            window_height: Display height
            
        Returns:
            Tuple of (controller, model, view, input_handler, state)
        """
        # Create components
        model = BoardModel(width, height)
        state = GameState()
        state.size_x = width
        state.size_y = height
        
        # Create view
        view = ViewFactory.create_view(view_type, width, height, 
                                      window_width, window_height)
        
        # Create input handler
        view_type = view_type.lower()
        if view_type in ['pygame', 'gui']:
            input_handler = PygameInputHandler()
        elif view_type in ['terminal', 'console', 'ascii']:
            input_handler = TerminalInputHandler()
        elif view_type in ['headless', 'none', 'null']:
            input_handler = HeadlessInputHandler()
        else:
            input_handler = HeadlessInputHandler()  # Default
        
        # Create controller
        controller = BoardController(model, view, input_handler, state)
        
        return controller, model, view, input_handler, state
    
    @staticmethod
    def create_pygame_ui(width: int = 8, height: int = 8):
        """Create Pygame UI stack"""
        return UIFactory.create_ui('pygame', width, height)
    
    @staticmethod
    def create_terminal_ui(width: int = 8, height: int = 8):
        """Create Terminal UI stack"""
        return UIFactory.create_ui('terminal', width, height, 80, 24)
    
    @staticmethod
    def create_headless_ui(width: int = 8, height: int = 8):
        """Create Headless UI stack"""
        return UIFactory.create_ui('headless', width, height, 0, 0)

