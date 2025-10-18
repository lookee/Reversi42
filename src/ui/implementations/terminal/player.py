"""
TerminalHumanPlayer - Human player for terminal/console mode

Simple text-based input for playing in terminal without Pygame.
Enter moves as coordinates (e.g., "D3", "E4") or numbers (1-N).

Version: 3.1.0
Architecture: Isolated in ui/implementations/terminal/
"""

import sys
import os

# Add path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from Reversi.Game import Move
from Players.Player import Player


class TerminalHumanPlayer(Player):
    """
    Human player for terminal/console mode.
    
    Input format: Column + Row (e.g., "D3", "E4")
    - Columns: A-H (case insensitive)
    - Rows: 1-8
    
    Examples:
        D3 -> column D (4), row 3
        e6 -> column E (5), row 6
        A1 -> column A (1), row 1
    """
    
    PLAYER_METADATA = {
        'display_name': 'Terminal Human',
        'description': 'You! Play by typing coordinates (e.g., D3)',
        'enabled': True,
        'parameters': []
    }
    
    def __init__(self, name='Human'):
        """Initialize terminal human player"""
        self.name = name
    
    def get_name(self):
        """Get player name"""
        return self.name
    
    def get_move(self, game, moves, control):
        """
        Get move from terminal input.
        
        Args:
            game: Current game state
            moves: List of valid moves
            control: Board control (for rendering)
            
        Returns:
            Move object or None if quit
        """
        # Display valid moves with numbers (compact, on one line)
        if moves:
            move_strs = []
            for i, m in enumerate(moves, 1):
                col_letter = chr(ord('A') + m.x - 1)
                move_str = f"{i}.{col_letter}{m.y}"
                move_strs.append(move_str)
            
            # Print all moves on one line
            print(f"Valid moves: {' '.join(move_strs)}")
            
            # First move as default
            first_move = moves[0]
            first_col_letter = chr(ord('A') + first_move.x - 1)
            default_move_str = f"{first_col_letter}{first_move.y}"
        else:
            print("\nNo valid moves available")
            return None
        
        # Get input
        while True:
            try:
                move_input = input(f"\nEnter move [{default_move_str}], 1-{len(moves)}, 0=Exit, M=Menu: ").strip()
                
                # If empty, use default (first move)
                if not move_input:
                    print(f"✓ Playing default: {default_move_str}")
                    return first_move
                
                move_input_upper = move_input.upper()
                
                # Check for menu
                if move_input_upper in ['M', 'MENU']:
                    print("\n✓ Returning to main menu...")
                    control.should_return_to_menu = True
                    return None
                
                if move_input_upper in ['H', 'HELP', '?']:
                    self._show_help()
                    continue
                
                # Try to parse as number first
                if move_input.isdigit():
                    move_num = int(move_input)
                    
                    # Check for "0" - exit game
                    if move_num == 0:
                        print("\n✓ Exiting game...")
                        import sys
                        sys.exit(0)
                    
                    if 1 <= move_num <= len(moves):
                        selected_move = moves[move_num - 1]
                        col_letter = chr(ord('A') + selected_move.x - 1)
                        print(f"✓ Playing {move_num}.{col_letter}{selected_move.y}")
                        return selected_move
                    else:
                        print(f"✗ Invalid number. Choose 1-{len(moves)}")
                        continue
                
                # Parse as coordinates (e.g., "D3" -> column 4, row 3)
                if len(move_input) < 2:
                    print(f"Invalid format. Use coordinate (D3) or number (1-{len(moves)})")
                    continue
                
                # Extract column and row
                col_letter = move_input_upper[0]
                row_str = move_input_upper[1:]
                
                # Validate column (A-H)
                if col_letter not in 'ABCDEFGH':
                    print(f"Invalid column '{col_letter}'. Use A-H or number 1-{len(moves)}")
                    continue
                
                # Validate row (1-8)
                try:
                    row = int(row_str)
                    if row < 1 or row > 8:
                        print(f"Invalid row {row}. Use 1-8")
                        continue
                except ValueError:
                    print(f"Invalid row '{row_str}'. Use 1-8")
                    continue
                
                # Convert to Move
                col = ord(col_letter) - ord('A') + 1  # A=1, B=2, ..., H=8
                move = Move(col, row)
                
                # Check if move is valid
                if move in moves:
                    print(f"✓ Playing {col_letter}{row}")
                    return move
                else:
                    print(f"✗ {col_letter}{row} is not a valid move")
                    # Show numbered moves
                    numbered_moves = [f"{i}.{chr(ord('A')+m.x-1)}{m.y}" for i, m in enumerate(moves, 1)]
                    print(f"Valid: {' '.join(numbered_moves)}")
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted")
                control.should_exit = True
                return None
            except Exception as e:
                print(f"Error: {e}")
                print("Please try again")
    
    def _show_help(self):
        """Show help message"""
        print("\n" + "="*70)
        print("HOW TO PLAY - TERMINAL MODE")
        print("="*70)
        print("\nMove Format: COLUMN + ROW")
        print("  Columns: A, B, C, D, E, F, G, H")
        print("  Rows:    1, 2, 3, 4, 5, 6, 7, 8")
        print("\nExamples:")
        print("  D3 - Place piece at column D, row 3")
        print("  E6 - Place piece at column E, row 6")
        print("  a1 - Place piece at column A, row 1 (case insensitive)")
        print("\nCommands:")
        print("  q, quit, exit - Quit game")
        print("  h, help, ?    - Show this help")
        print("="*70 + "\n")

