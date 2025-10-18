"""
Abstract Engine Base Class

Strategy Pattern: Defines the interface for all game engines.
All engines must implement this interface.

Version: 3.2.0
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class Engine(ABC):
    """
    Abstract base class for all game engines.
    
    Strategy Pattern: Allows interchangeable algorithms.
    Dependency Injection: Engines are injected into players.
    
    All concrete engines must implement:
    - get_best_move(): Find optimal move
    - evaluate_position(): Score a position
    
    Example:
        class MyEngine(Engine):
            def get_best_move(self, game, depth, **kwargs):
                # Implementation
                pass
    """
    
    def __init__(self, name: str = "Engine", config: Optional[Dict[str, Any]] = None):
        """
        Initialize engine.
        
        Args:
            name: Engine name for display
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        
        # Statistics tracking
        self._statistics = {
            'nodes_evaluated': 0,
            'pruning_count': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'time_spent_ms': 0
        }
    
    @abstractmethod
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Find the best move for the current position.
        
        Args:
            game: Game state object
            depth: Search depth
            **kwargs: Additional parameters (player_name, etc.)
        
        Returns:
            Move: Best move found
        """
        pass
    
    @abstractmethod
    def evaluate_position(self, game) -> float:
        """
        Evaluate the current board position.
        
        Args:
            game: Game state object
        
        Returns:
            float: Position score (positive = good for current player)
        """
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get engine performance statistics.
        
        Returns:
            dict: Statistics including nodes, pruning, cache hits, etc.
        """
        return self._statistics.copy()
    
    def reset_statistics(self):
        """Reset all statistics counters."""
        self._statistics = {k: 0 for k in self._statistics}
    
    def update_statistics(self, **kwargs):
        """
        Update specific statistics.
        
        Args:
            **kwargs: Statistic name-value pairs
        """
        for key, value in kwargs.items():
            if key in self._statistics:
                self._statistics[key] += value
    
    def get_name(self) -> str:
        """Get engine display name."""
        return self.name
    
    def get_config(self) -> Dict[str, Any]:
        """Get engine configuration."""
        return self.config.copy()
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"

