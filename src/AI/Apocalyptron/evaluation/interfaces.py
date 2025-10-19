"""
Interfaces for position evaluation.

Defines the contract that all evaluators must implement.
"""

from abc import ABC, abstractmethod
from enum import Enum


class GamePhase(Enum):
    """Game phase classification"""
    OPENING = 'opening'    # 0-19 pieces
    MIDGAME = 'midgame'    # 20-49 pieces
    ENDGAME = 'endgame'    # 50-64 pieces


class PositionEvaluator(ABC):
    """
    Abstract base class for position evaluation strategies.
    
    All evaluators must implement the evaluate() method which returns
    a score from the current player's perspective (positive = good).
    """
    
    @abstractmethod
    def evaluate(self, game) -> int:
        """
        Evaluate a game position from current player's perspective.
        
        Args:
            game: BitboardGame instance to evaluate
            
        Returns:
            int: Evaluation score (positive = good for current player)
        """
        pass
    
    def get_name(self) -> str:
        """Get evaluator name for debugging"""
        return self.__class__.__name__

