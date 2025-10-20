"""
TerminalInputProvider - Terminal/Console implementation of InputProvider

Provides text-based input for terminal mode.
Input format: Column + Row (e.g., "D3", "E4")

Design Pattern: Adapter
"""

from typing import Optional, List
from Reversi.Game import Move
from Players.abstractions import InputProvider


class TerminalInputProvider(InputProvider):
    """
    Terminal/console-specific implementation of InputProvider.
    
    Handles:
    - Text input in format "D3", "E4", etc.
    - Commands: 'quit', 'exit', 'q' for exit
    - Commands: 'pause', 'p' for pause
    
    No pygame dependencies!
    """
    
    def __init__(self):
        """Initialize terminal input provider."""
        self._exit_requested = False
        self._pause_requested = False
    
    def get_move_input(self, game, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get move from terminal input.
        
        Args:
            game: Current game state
            legal_moves: List of legal moves
            
        Returns:
            Move selected by user, or None if exit/pause
        """
        while True:
            try:
                # Get input from user
                user_input = input("Enter move (e.g., D3) or 'q' to quit: ").strip().upper()
                
                # Check for exit commands
                if user_input in ('Q', 'QUIT', 'EXIT'):
                    self._exit_requested = True
                    return None
                
                # Check for pause commands
                if user_input in ('P', 'PAUSE'):
                    self._pause_requested = True
                    return None
                
                # Parse move input (e.g., "D3" -> Move(4, 3))
                if len(user_input) >= 2:
                    col = user_input[0]
                    row = user_input[1:]
                    
                    # Convert column letter to number (A=1, B=2, ...)
                    if 'A' <= col <= 'H':
                        x = ord(col) - ord('A') + 1
                        y = int(row)
                        
                        move = Move(x, y)
                        
                        # Validate move
                        if move in legal_moves:
                            return move
                        else:
                            print(f"❌ Move {move} is not legal. Try again.")
                    else:
                        print("❌ Invalid column. Use A-H.")
                else:
                    print("❌ Invalid format. Use format like 'D3'.")
                    
            except ValueError:
                print("❌ Invalid input. Use format like 'D3'.")
            except (KeyboardInterrupt, EOFError):
                self._exit_requested = True
                return None
    
    def should_exit(self) -> bool:
        """Check if exit was requested."""
        return self._exit_requested
    
    def should_pause(self) -> bool:
        """Check if pause was requested."""
        return self._pause_requested
    
    def reset(self):
        """Reset input provider state."""
        self._exit_requested = False
        self._pause_requested = False

