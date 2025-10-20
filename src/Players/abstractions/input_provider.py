"""
InputProvider - Abstract interface for user input

This abstraction allows Players to be completely UI-agnostic.
Concrete implementations (Pygame, Terminal, Headless) are provided in the UI layer.

Design Pattern: Strategy + Dependency Inversion Principle
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from Reversi.Game import Move


class InputProvider(ABC):
    """
    Abstract interface for getting user input.
    
    Players depend on this abstraction, NOT on concrete UI frameworks (pygame, etc.)
    This is Dependency Inversion Principle in action!
    
    Different UI implementations (pygame, terminal, web) provide concrete implementations.
    """
    
    @abstractmethod
    def get_move_input(self, game, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get a move from user input.
        
        This method should handle all UI-specific input logic:
        - Mouse clicks (pygame)
        - Keyboard input (terminal)
        - Network requests (web)
        - etc.
        
        Args:
            game: Current game state
            legal_moves: List of legal moves available
            
        Returns:
            Move selected by user, or None if exit/pause requested
        """
        pass
    
    @abstractmethod
    def should_exit(self) -> bool:
        """
        Check if user wants to exit the game.
        
        Returns:
            True if exit requested, False otherwise
        """
        pass
    
    @abstractmethod
    def should_pause(self) -> bool:
        """
        Check if user wants to pause the game.
        
        Returns:
            True if pause requested, False otherwise
        """
        pass
    
    @abstractmethod
    def reset(self):
        """
        Reset the input provider state.
        
        Called before getting a new move to clear any previous state.
        """
        pass

