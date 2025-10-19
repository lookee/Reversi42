"""
Search algorithm interfaces.
"""

from abc import ABC, abstractmethod
from AI.Apocalyptron.core.search_context import SearchContext
from AI.Apocalyptron.core.search_result import SearchResult


class SearchAlgorithm(ABC):
    """
    Abstract base class for search algorithms.
    
    All search algorithms must implement the search() method.
    """
    
    @abstractmethod
    def search(self, context: SearchContext) -> SearchResult:
        """
        Perform search from given context.
        
        Args:
            context: SearchContext with position and parameters
            
        Returns:
            SearchResult with best move and statistics
        """
        pass
    
    @abstractmethod
    def get_best_move(self, game, depth: int, **kwargs):
        """
        High-level interface for getting best move.
        
        Args:
            game: Game instance
            depth: Search depth
            **kwargs: Additional parameters
            
        Returns:
            Best move found
        """
        pass

