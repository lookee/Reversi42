"""
Abstract Evaluator Base Class

Strategy Pattern: Defines interface for position evaluation.

Version: 3.2.0
"""

from abc import ABC, abstractmethod


class Evaluator(ABC):
    """
    Abstract base class for position evaluators.
    
    Strategy Pattern: Different evaluation strategies.
    
    Evaluators score board positions to guide engine search.
    
    Example:
        class MyEvaluator(Evaluator):
            def evaluate(self, game):
                # Return score for current position
                return score
    """
    
    def __init__(self, name: str = "Evaluator"):
        """
        Initialize evaluator.
        
        Args:
            name: Evaluator name for display
        """
        self.name = name
    
    @abstractmethod
    def evaluate(self, game) -> float:
        """
        Evaluate the current board position.
        
        Args:
            game: Game state object
        
        Returns:
            float: Position score
                  Positive = good for current player
                  Negative = bad for current player
                  0 = neutral
        """
        pass
    
    def get_name(self) -> str:
        """Get evaluator display name."""
        return self.name
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"

