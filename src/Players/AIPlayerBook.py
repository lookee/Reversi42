"""
AIPlayerBook - AI Player with Opening Book support

This player uses an opening book for the early game and falls back to
standard minimax search when out of book.
"""

from Reversi.Game import Game, Move
from AI.MinimaxEngine import MinimaxEngine
from AI.OpeningBook import get_default_opening_book
from Players.Player import Player
import random


class AIPlayerBook(Player):
    """
    AI Player that uses opening book for early game.
    
    Features:
    - Consults opening book first (O(m) lookup via Trie)
    - If multiple book moves available, chooses randomly among them
    - Falls back to minimax engine when out of book
    - Tracks when it leaves the book for statistics
    """
    
    PLAYER_METADATA = {
        'display_name': 'AI with Opening Book',
        'description': 'AI that uses opening theory from book, then minimax search. Very strong in early game.',
        'enabled': True,
        'parameters': {
            'difficulty': {
                'type': int,
                'min': 1,
                'max': 10,
                'default': 6,
                'description': 'Search depth when out of book (higher = stronger but slower)'
            }
        }
    }
    
    def __init__(self, deep=6, show_book_options=True):
        """
        Initialize AIPlayerBook.
        
        Args:
            deep: Search depth for minimax when out of book
            show_book_options: If True, show all available book moves when consulting book
        """
        self.name = f'AIPlayerBook{deep}'
        self.deep = deep
        self.engine = MinimaxEngine()
        self.opening_book = get_default_opening_book()
        self.show_book_options = show_book_options  # Show all available openings
        
        # Statistics
        self.moves_from_book = 0
        self.moves_from_engine = 0
        self.left_book_at_move = None
        
        # Load book statistics
        stats = self.opening_book.get_statistics()
        if stats['lines_loaded'] > 0:
            print(f"[{self.name}] Opening book loaded: {stats['lines_loaded']} lines, "
                  f"{stats['total_positions']} positions")
    
    def get_move(self, game, moves, control):
        """
        Get next move using opening book or engine.
        
        Priority:
        1. Check opening book for current position
        2. If book moves found, choose randomly among them
        3. Otherwise, use minimax engine
        
        Args:
            game: Current game state
            moves: List of valid moves
            control: Board control (for UI updates)
        
        Returns:
            Move object
        """
        # Get game history (needed for book lookup)
        game_history = self._get_game_history(game)
        
        # Check opening book first
        book_moves = self.opening_book.get_book_moves(game_history)
        
        # Filter book moves to only include valid moves for current position
        valid_book_moves = [m for m in book_moves if m in moves]
        
        if valid_book_moves:
            # In book! Choose randomly among valid book moves
            move = random.choice(valid_book_moves)
            self.moves_from_book += 1
            
            # Show book options if enabled
            if self.show_book_options:
                # Get opening names
                current_opening = self.opening_book.get_current_opening_name(game_history)
                available_openings = self.opening_book.get_opening_names(game_history)
                
                print("\n" + "="*80)
                print(f"📚 OPENING BOOK - {self.name}")
                print(f"Position: {game_history if game_history else '(start)'}")
                
                # Show current opening if matched
                if current_opening:
                    print(f"Current Opening: {current_opening}")
                
                # Show available openings (extensions of current position)
                if available_openings:
                    print(f"Available Openings ({len(available_openings)}): {', '.join(available_openings[:5])}")
                    if len(available_openings) > 5:
                        print(f"  ... and {len(available_openings) - 5} more")
                
                print("="*80)
                print(f"Available book moves ({len(valid_book_moves)}):")
                for i, book_move in enumerate(valid_book_moves, 1):
                    selected_indicator = "⭐" if book_move == move else "  "
                    # Try to find which opening this move leads to
                    next_history = game_history + str(book_move).upper()
                    next_opening = self.opening_book.get_current_opening_name(next_history)
                    opening_info = f" → {next_opening}" if next_opening else ""
                    print(f"  {selected_indicator} {i}. {book_move}{opening_info}")
                print("-"*80)
                print(f"Selected: {move} (random choice from {len(valid_book_moves)} options)")
                print("="*80 + "\n")
            else:
                # Simple message
                print(f"[{self.name}] Book move: {move} "
                      f"(from {len(valid_book_moves)} book options)")
            
            return move
        else:
            # Out of book, use engine
            if self.left_book_at_move is None:
                self.left_book_at_move = len(game_history) // 2  # Approximate move number
                print(f"[{self.name}] Left book at move ~{self.left_book_at_move}, "
                      f"switching to engine (depth {self.deep})")
            
            move = self.engine.get_best_move(game, self.deep, player_name=self.name)
            self.moves_from_engine += 1
            return move
    
    def _get_game_history(self, game):
        """
        Extract game history as a move string.
        
        This is a bit hacky - we rely on the game object having a history
        or we reconstruct it. For efficiency, game should store this.
        
        Returns:
            String like "F5d6C3d3" representing the game so far
        """
        # Check if game has history attribute (it should after our changes)
        if hasattr(game, 'history'):
            return game.history
        
        # Fallback: empty history (will work but won't use book effectively)
        return ""
    
    def get_statistics(self):
        """
        Get player statistics.
        
        Returns:
            Dict with book usage stats
        """
        total_moves = self.moves_from_book + self.moves_from_engine
        book_percentage = (self.moves_from_book / total_moves * 100) if total_moves > 0 else 0
        
        return {
            'moves_from_book': self.moves_from_book,
            'moves_from_engine': self.moves_from_engine,
            'book_percentage': book_percentage,
            'left_book_at_move': self.left_book_at_move
        }
    
    @classmethod
    def get_metadata(cls):
        """Return player metadata for factory"""
        return cls.PLAYER_METADATA

