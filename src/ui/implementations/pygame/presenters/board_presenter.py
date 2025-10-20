"""
BoardPresenter - MVP Presenter for Board

Mediates between BoardModel (domain) and BoardView (UI).
Contains presentation logic - 100% testable without pygame!

Design Pattern: MVP (Model-View-Presenter)
"""

from typing import Optional, Tuple, List
from ui.common import EventBus


class BoardPresenter:
    """
    Board presenter - presentation logic (testable!)
    
    Responsibilities:
    - Coordinate Model ↔ View communication
    - Handle user interactions
    - Update view based on model changes
    - NO pygame code here! (testable)
    
    This is the key to MVP pattern - all logic is here, not in View.
    """
    
    def __init__(self, model, view, event_bus: Optional[EventBus] = None):
        """
        Initialize presenter.
        
        Args:
            model: BoardModel instance
            view: BoardView instance  
            event_bus: EventBus for decoupled events
        """
        self.model = model
        self.view = view
        self.event_bus = event_bus or EventBus()
        
        # Subscribe to model events
        self.event_bus.on('model_changed', self.on_model_changed)
        self.event_bus.on('move_made', self.on_move_made)
    
    def on_model_changed(self, data=None):
        """
        React to model changes (Observer pattern).
        
        This is where presentation logic lives!
        """
        # Get data from model
        board_state = self.model.get_board_state()
        legal_moves = self.model.get_legal_moves()
        last_move = self.model.get_last_move()
        
        # Tell view what to render (not HOW!)
        self.view.set_board_state(board_state)
        self.view.set_legal_moves(legal_moves)
        self.view.set_last_move(last_move)
        
        # Request re-render
        self.view.render()
    
    def on_move_made(self, move_data):
        """React to move being made."""
        self.on_model_changed()
        
        # Could add animation here
        # self.event_bus.emit('play_sound', 'piece_placed')
    
    def handle_cell_click(self, board_x: int, board_y: int):
        """
        Handle cell click (presentation logic).
        
        Args:
            board_x: Board X coordinate
            board_y: Board Y coordinate
        """
        # Validate and execute move
        if self.model.is_legal_move(board_x, board_y):
            self.model.make_move(board_x, board_y)
            self.event_bus.emit('move_made', {'x': board_x, 'y': board_y})
            return True
        return False
    
    def handle_hover(self, board_x: int, board_y: int):
        """
        Handle cell hover.
        
        Args:
            board_x: Board X coordinate  
            board_y: Board Y coordinate
        """
        # Show opening book info if hovering over legal move
        if (board_x, board_y) in self.model.get_legal_moves():
            # Could trigger opening book tooltip
            self.event_bus.emit('cell_hovered', {'x': board_x, 'y': board_y})

