"""
Composite evaluator.

Combines multiple evaluation strategies using weighted sum.
Implements Composite Pattern for flexible evaluation composition.
"""

from typing import List, Tuple
from AI.Apocalyptron.evaluation.interfaces import PositionEvaluator


class CompositeEvaluator(PositionEvaluator):
    """
    Composite evaluator that combines multiple evaluation strategies.
    
    Uses weighted sum to combine different evaluation aspects:
    - Mobility
    - Positional (corners, edges, x-squares)
    - Stability
    - Parity
    - Piece count (endgame)
    
    Example:
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
        evaluator.add_evaluator(PositionalEvaluator(weights), weight=1.0)
        evaluator.add_evaluator(StabilityEvaluator(weights), weight=1.0)
        evaluator.add_evaluator(ParityEvaluator(weights), weight=1.0)
        
        score = evaluator.evaluate(game)
    """
    
    def __init__(self):
        """Initialize empty composite evaluator"""
        self.evaluators: List[Tuple[PositionEvaluator, float]] = []
    
    def add_evaluator(self, evaluator: PositionEvaluator, weight: float = 1.0):
        """
        Add an evaluator to the composite.
        
        Args:
            evaluator: PositionEvaluator instance
            weight: Weight multiplier for this evaluator (default: 1.0)
        """
        self.evaluators.append((evaluator, weight))
    
    def evaluate(self, game) -> int:
        """
        Evaluate position using all registered evaluators.
        
        Args:
            game: BitboardGame instance
            
        Returns:
            int: Weighted sum of all evaluator scores
        """
        total = 0
        
        for evaluator, weight in self.evaluators:
            score = evaluator.evaluate(game)
            total += int(score * weight)
        
        return total
    
    def get_detailed_evaluation(self, game) -> dict:
        """
        Get detailed breakdown of evaluation by component.
        
        Useful for debugging and understanding position assessment.
        
        Args:
            game: BitboardGame instance
            
        Returns:
            dict: {evaluator_name: score} for each evaluator
        """
        breakdown = {}
        
        for evaluator, weight in self.evaluators:
            score = evaluator.evaluate(game)
            weighted_score = int(score * weight)
            breakdown[evaluator.get_name()] = {
                'raw_score': score,
                'weight': weight,
                'weighted_score': weighted_score,
            }
        
        breakdown['total'] = sum(e['weighted_score'] for e in breakdown.values() if isinstance(e, dict))
        
        return breakdown
    
    def get_evaluator_count(self) -> int:
        """Get number of registered evaluators"""
        return len(self.evaluators)

