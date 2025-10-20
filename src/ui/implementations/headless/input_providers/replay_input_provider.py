"""
ReplayInputProvider - Replay moves from game file

Useful for:
- Replaying saved games
- AI training from human games
- Testing with real game sequences

Design Pattern: Iterator + Strategy
"""

from typing import Optional, List
from Reversi.Game import Move
from Players.abstractions import InputProvider


class ReplayInputProvider(InputProvider):
    """
    Replay InputProvider for playing back recorded games.
    
    Reads moves from a game history string or file.
    """
    
    def __init__(self, game_history: str):
        """
        Initialize replay provider.
        
        Args:
            game_history: String with game moves (e.g., "D3c3E3...")
        """
        self.moves = self._parse_history(game_history)
        self.current_index = 0
        self._exit_requested = False
    
    def _parse_history(self, history: str) -> List[Move]:
        """
        Parse game history string into moves.
        
        Format: uppercase = black, lowercase = white
        Example: "D3c3E3" -> [Move(4,3), Move(3,3), Move(5,3)]
        """
        moves = []
        i = 0
        while i < len(history):
            # Skip 'pass' markers if any
            if history[i:i+4].lower() == 'pass':
                i += 4
                continue
            
            # Read column (letter)
            if i < len(history) and history[i].isalpha():
                col = history[i].upper()
                x = ord(col) - ord('A') + 1
                i += 1
                
                # Read row (number)
                row_str = ''
                while i < len(history) and history[i].isdigit():
                    row_str += history[i]
                    i += 1
                
                if row_str:
                    y = int(row_str)
                    moves.append(Move(x, y))
            else:
                i += 1
        
        return moves
    
    def get_move_input(self, game, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get next move from replay.
        
        Args:
            game: Current game state
            legal_moves: List of legal moves
            
        Returns:
            Next move from history, or None if exhausted
        """
        if self.current_index >= len(self.moves):
            self._exit_requested = True
            return None
        
        move = self.moves[self.current_index]
        self.current_index += 1
        
        # Validate move is legal
        if move not in legal_moves:
            print(f"⚠️ Replay move {move} not legal at this position!")
            self._exit_requested = True
            return None
        
        return move
    
    def should_exit(self) -> bool:
        """Check if replay is complete."""
        return self._exit_requested
    
    def should_pause(self) -> bool:
        """Replay doesn't pause."""
        return False
    
    def reset(self):
        """Reset to start of replay."""
        self.current_index = 0
        self._exit_requested = False

