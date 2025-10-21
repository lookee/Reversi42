"""
Knowledge Package - Game Knowledge Bases

This package contains knowledge bases for Reversi:
- Opening theory (professional sequences)
- Endgame databases (future)
- Pattern libraries (future)

The knowledge is stored as:
- Code: opening_book.py, etc.
- Data: data/ directory with .txt files

This organization keeps related code and data together (Cohesion principle).
"""

from .opening_book import OpeningBook, get_default_opening_book
from .enhanced_opening_book import EnhancedOpeningBook, get_enhanced_opening_book, SelectionMode, MoveEvaluation

__all__ = [
    "OpeningBook", 
    "get_default_opening_book",
    "EnhancedOpeningBook",
    "get_enhanced_opening_book", 
    "SelectionMode",
    "MoveEvaluation"
]
