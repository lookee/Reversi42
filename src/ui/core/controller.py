"""
Board Controller - Framework-Agnostic Orchestrator

Coordinates Model, View, and InputHandler without framework dependencies.
Pure orchestration logic following MVC pattern.

Architecture: Controller in MVC pattern
Version: 3.1.0
"""

from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from ui.core.model import BoardModel
from ui.core.state import GameState
from ui.abstractions.view_interface import AbstractView
from ui.abstractions.input_interface import AbstractInputHandler, InputEvent


class BoardController:
    """
    Framework-agnostic board controller.
    
    Responsibilities:
    - Coordinate Model ↔ View
    - Process input through InputHandler
    - Update game state
    - NO framework-specific code
    
    Design Philosophy:
    - Depend on abstractions (AbstractView, AbstractInputHandler)
    - Not on implementations (Pygame, Terminal, etc.)
    - Easily testable with mocks
    - Zero framework coupling
    """
    
    def __init__(self,
                 model: BoardModel,
                 view: AbstractView,
                 input_handler: AbstractInputHandler,
                 state: Optional[GameState] = None):
        """
        Initialize controller with dependencies.
        
        Args:
            model: Board model (domain logic)
            view: View implementation (rendering)
            input_handler: Input handler (event processing)
            state: Game state (optional, creates new if None)
        """
        self.model = model
        self.view = view
        self.input_handler = input_handler
        self.state = state if state is not None else GameState()
        
        # Initialize view
        self.view.initialize()
    
    def process_input(self) -> None:
        """
        Process input events (framework-agnostic).
        
        Polls input handler and updates state based on events.
        No framework-specific code.
        """
        events = self.input_handler.poll_events()
        
        for event in events:
            event_type = event['type']
            event_data = event.get('data', {})
            
            if event_type == InputEvent.QUIT:
                self.state.should_exit = True
            
            elif event_type == InputEvent.PAUSE:
                self.state.should_pause = True
            
            elif event_type == InputEvent.SELECT:
                # Select current cursor position
                self.state.selected_position = self.state.cursor_position
            
            elif event_type == InputEvent.CLICK:
                # Convert click position to board coordinates
                position = event_data.get('position')
                if position:
                    # This would need coordinate conversion
                    # For now, store raw position
                    self.state.selected_position = position
            
            elif event_type == InputEvent.MOVE_UP:
                x, y = self.state.cursor_position
                self.state.cursor_position = (x, max(0, y - 1))
            
            elif event_type == InputEvent.MOVE_DOWN:
                x, y = self.state.cursor_position
                self.state.cursor_position = (x, min(self.state.size_y - 1, y + 1))
            
            elif event_type == InputEvent.MOVE_LEFT:
                x, y = self.state.cursor_position
                self.state.cursor_position = (max(0, x - 1), y)
            
            elif event_type == InputEvent.MOVE_RIGHT:
                x, y = self.state.cursor_position
                self.state.cursor_position = (min(self.state.size_x - 1, x + 1), y)
            
            elif event_type == InputEvent.RESIZE:
                width = event_data.get('width')
                height = event_data.get('height')
                if width and height:
                    self.view.resize(width, height)
    
    def render(self) -> None:
        """
        Render current state through view (framework-agnostic).
        
        Converts model state to visual output through view interface.
        No framework-specific code.
        """
        # Get board state from model
        board_state = self.model.to_2d_array()
        
        # Render board
        self.view.render_board(board_state)
        
        # Show game info
        self.view.show_game_info(self.state.to_dict())
        
        # Highlight valid moves
        if self.state.valid_moves:
            self.view.highlight_cells(self.state.valid_moves, 'valid_move')
        
        # Highlight last move
        if self.state.last_move:
            self.view.highlight_cells([self.state.last_move], 'last_move')
        
        # Highlight cursor
        if self.state.cursor_mode:
            self.view.highlight_cells([self.state.cursor_position], 'cursor')
        
        # Update display
        self.view.update_display()
    
    def update(self) -> None:
        """
        Single update cycle: input → logic → render.
        
        Main game loop calls this repeatedly.
        """
        self.process_input()
        # Game logic would be called here
        self.render()
    
    def cleanup(self):
        """Cleanup all resources"""
        self.view.cleanup()
        self.input_handler.cleanup()

