"""
OpeningBook - Efficient opening book management for Reversi42

This module provides an efficient Trie-based structure to store and query
opening sequences from a book file.
"""

import os
from Reversi.Game import Move

class TrieNode:
    """Node in the opening book trie"""
    def __init__(self):
        self.children = {}  # key: move_str, value: TrieNode
        self.is_end = False  # True if this is the end of a book line

class OpeningBook:
    """
    Efficient opening book using a Trie structure.
    
    The Trie allows O(m) lookup where m is the length of the move sequence,
    much faster than comparing against all book lines.
    """
    
    def __init__(self, book_path=None):
        """
        Initialize the opening book.
        
        Args:
            book_path: Path to the opening book file. If None, uses default.
        """
        self.root = TrieNode()
        self.book_path = book_path
        self.lines_loaded = 0
        self.opening_names = {}  # Map: move_sequence -> opening_name
        
        if book_path and os.path.exists(book_path):
            self._load_book(book_path)
    
    def _load_book(self, book_path):
        """Load opening book from file into Trie structure"""
        with open(book_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Check if line has format: NAME | MOVES
                opening_name = None
                if '|' in line:
                    parts = line.split('|', 1)
                    opening_name = parts[0].strip()
                    move_sequence = parts[1].strip()
                else:
                    move_sequence = line
                
                # Parse the move sequence
                moves = self._parse_move_sequence(move_sequence)
                if moves:
                    self._add_sequence(moves)
                    # Store opening name if provided
                    if opening_name:
                        self.opening_names[move_sequence] = opening_name
                    self.lines_loaded += 1
    
    def _parse_move_sequence(self, sequence):
        """
        Parse a move sequence string into a list of Move objects.
        
        Format: F5d6C3 (uppercase=black, lowercase=white)
        Returns: [Move('F5'), Move('d6'), Move('C3'), ...]
        """
        moves = []
        i = 0
        while i < len(sequence):
            if sequence[i].isalpha():
                if i + 1 < len(sequence) and sequence[i + 1].isdigit():
                    move_str = sequence[i:i+2]
                    moves.append(move_str)
                    i += 2
                else:
                    i += 1
            else:
                i += 1
        return moves
    
    def _add_sequence(self, moves):
        """Add a move sequence to the Trie"""
        node = self.root
        for move_str in moves:
            # Normalize to uppercase for storage (we only care about position, not color)
            normalized = move_str.upper()
            if normalized not in node.children:
                node.children[normalized] = TrieNode()
            node = node.children[normalized]
        node.is_end = True
    
    def get_book_moves(self, game_history):
        """
        Get all valid book moves for the current position.
        
        Args:
            game_history: String of moves so far (e.g., "F5d6C3")
        
        Returns:
            List of Move objects that continue any book line, or empty list
        """
        # Parse the game history
        history_moves = self._parse_move_sequence(game_history)
        
        # Navigate the Trie to current position
        node = self.root
        for move_str in history_moves:
            normalized = move_str.upper()
            if normalized not in node.children:
                # Position not in book
                return []
            node = node.children[normalized]
        
        # Get all possible next moves from this position
        book_moves = []
        for move_str in node.children.keys():
            # Convert back to Move object
            try:
                move = self._str_to_move(move_str)
                if move:
                    book_moves.append(move)
            except:
                pass
        
        return book_moves
    
    def _str_to_move(self, move_str):
        """
        Convert move string to Move object.
        
        Args:
            move_str: String like "F5" or "d6"
        
        Returns:
            Move object with x, y coordinates
        """
        if len(move_str) != 2:
            return None
        
        col = move_str[0].upper()
        row = move_str[1]
        
        # Convert column letter to x (A=1, B=2, ..., H=8)
        x = ord(col) - ord('A') + 1
        # Convert row digit to y
        y = int(row)
        
        return Move(x, y)
    
    def is_in_book(self, game_history):
        """
        Check if current position is in the opening book.
        
        Args:
            game_history: String of moves so far
        
        Returns:
            True if position is in book, False otherwise
        """
        history_moves = self._parse_move_sequence(game_history)
        node = self.root
        
        for move_str in history_moves:
            normalized = move_str.upper()
            if normalized not in node.children:
                return False
            node = node.children[normalized]
        
        return True
    
    def get_opening_names(self, game_history):
        """
        Get the names of all openings that match or extend the current position.
        
        Args:
            game_history: String of moves so far (e.g., "F5d6C3")
        
        Returns:
            List of opening names that include this position
        """
        matching_names = []
        history_upper = game_history.upper()
        
        for sequence, name in self.opening_names.items():
            sequence_upper = sequence.upper()
            # Check if this opening matches or extends the current position
            if sequence_upper.startswith(history_upper) or history_upper.startswith(sequence_upper):
                matching_names.append(name)
        
        return matching_names
    
    def get_current_opening_name(self, game_history):
        """
        Get the exact opening name for the current position if it exists.
        
        Args:
            game_history: String of moves so far
        
        Returns:
            Opening name if exact match found, None otherwise
        """
        # Try to find exact match
        if game_history in self.opening_names:
            return self.opening_names[game_history]
        
        # Try uppercase version
        history_upper = game_history.upper()
        for sequence, name in self.opening_names.items():
            if sequence.upper() == history_upper:
                return name
        
        return None
    
    def get_statistics(self):
        """Get statistics about the loaded book"""
        return {
            'lines_loaded': self.lines_loaded,
            'total_positions': self._count_nodes(self.root)
        }
    
    def _count_nodes(self, node):
        """Recursively count all nodes in the Trie"""
        count = 1
        for child in node.children.values():
            count += self._count_nodes(child)
        return count


def get_default_opening_book():
    """
    Get the default opening book instance.
    
    Returns:
        OpeningBook instance with default book loaded, or empty book if not found
    """
    # Try to find the opening book file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    book_path = os.path.join(project_root, 'Books', 'opening_book.txt')
    
    if os.path.exists(book_path):
        return OpeningBook(book_path)
    else:
        print(f"Warning: Opening book not found at {book_path}")
        return OpeningBook()

