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
        self._numbered_moves = []  # Store numbered moves for reference
    
    def get_move_input(self, game, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get move from terminal input.
        
        Args:
            game: Current game state
            legal_moves: List of legal moves
            
        Returns:
            Move selected by user, or None if exit/pause
        """
        # Show compact legal moves (max 8, sorted)
        self._print_compact_moves(legal_moves)
        
        while True:
            try:
                # Get input from user
                user_input = input("\n→ Move (number or D3) or ENTER for random, 'q' to quit: ").strip().upper()
                
                # ENTER = random move (default)
                if user_input == '':
                    import random
                    return random.choice(legal_moves)
                
                # Check for exit commands
                if user_input in ('Q', 'QUIT', 'EXIT'):
                    self._exit_requested = True
                    return None
                
                # Check for pause commands
                if user_input in ('P', 'PAUSE'):
                    self._pause_requested = True
                    return None
                
                # Try to parse as number first
                if user_input.isdigit():
                    num = int(user_input)
                    if 1 <= num <= len(legal_moves):
                        return legal_moves[num - 1]
                    else:
                        print(f"❌ Invalid number. Use 1-{len(legal_moves)}")
                        continue
                
                # Parse as move notation (e.g., "D3" -> Move(4, 3))
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
                        print("❌ Invalid column. Use A-H or number 1-{len(legal_moves)}.")
                else:
                    print(f"❌ Invalid format. Use number (1-{len(legal_moves)}) or move like 'D3'.")
                    
            except ValueError:
                print(f"❌ Invalid input. Use number (1-{len(legal_moves)}) or move like 'D3'.")
            except (KeyboardInterrupt, EOFError):
                self._exit_requested = True
                return None
    
    def _print_compact_moves(self, legal_moves: List[Move]):
        """
        Print legal moves numbered and in compact format.
        
        Shows all moves numbered: 1:C3 2:D3 3:E6...
        User can enter number (1, 2, 3) or move (C3, D3)
        """
        if not legal_moves:
            return
        
        # Store for later use
        self._numbered_moves = legal_moves
        
        # Convert to numbered list with chess notation
        move_strs = []
        for i, move in enumerate(legal_moves, 1):
            col = chr(ord('A') + move.x - 1)
            row = move.y
            move_strs.append(f"{i}:{col}{row}")
        
        # Print in rows of 8 for compactness
        print(f"\n▸ Moves:")
        for i in range(0, len(move_strs), 8):
            chunk = move_strs[i:i+8]
            print(f"  {' '.join(chunk)}")
    
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

