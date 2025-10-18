"""
Opening Book Decorator

Decorator Pattern: Adds opening book to any engine.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from engines.base.engine import Engine
from typing import Optional


class OpeningBookDecorator(Engine):
    """
    Decorator Pattern: Wraps any engine with opening book.
    
    Checks opening book first, falls back to wrapped engine.
    
    Example:
        base_engine = MinimaxEngine()
        engine = OpeningBookDecorator(base_engine, book_path="master.book")
    """
    
    def __init__(self, wrapped_engine: Engine, book_path: Optional[str] = None):
        """
        Wrap engine with opening book.
        
        Args:
            wrapped_engine: Base engine to wrap
            book_path: Path to opening book file
        """
        super().__init__(name=f"{wrapped_engine.name}+Book")
        self.engine = wrapped_engine  # Wrapped engine
        self.book = None
        self.book_path = book_path
        
        # Load opening book
        if book_path:
            self._load_book(book_path)
    
    def _load_book(self, path: str):
        """Load opening book from file."""
        try:
            from AI.OpeningBook import OpeningBook
            self.book = OpeningBook()
            self.book.load(path)
        except Exception as e:
            print(f"Warning: Could not load opening book from {path}: {e}")
            self.book = None
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Get best move: Check book first, fallback to engine.
        
        Args:
            game: Game state
            depth: Search depth
            **kwargs: Additional parameters
        
        Returns:
            Move: Best move
        """
        # Try opening book first
        if self.book:
            try:
                book_move = self.book.get_move(game.export_str())
                if book_move:
                    if kwargs.get('verbose', False):
                        print(f"📖 Opening book move")
                    return book_move
            except:
                pass  # Book lookup failed, use engine
        
        # Fallback to wrapped engine
        return self.engine.get_best_move(game, depth, **kwargs)
    
    def evaluate_position(self, game) -> float:
        """Delegate evaluation to wrapped engine."""
        return self.engine.evaluate_position(game)
    
    def get_statistics(self):
        """Get combined statistics from wrapper and wrapped engine."""
        stats = super().get_statistics()
        engine_stats = self.engine.get_statistics()
        
        # Merge statistics
        stats['wrapped_engine'] = self.engine.name
        stats['wrapped_stats'] = engine_stats
        
        return stats

