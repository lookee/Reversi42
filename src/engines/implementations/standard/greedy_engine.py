"""
Greedy Engine

Immediate gain maximization.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engines.base.engine import Engine
from engines.base.engine_metadata import EngineMetadata
from engines.factory.engine_registry import EngineRegistry


@EngineRegistry.register('greedy', EngineMetadata(
    name='greedy',
    display_name='Greedy Gobbler',
    description='Maximizes immediate piece gain - simple but effective',
    complexity='low',
    speed='fast',
    strength='weak',
    features=['greedy']
))
class GreedyEngine(Engine):
    """
    Greedy strategy: maximize immediate piece capture.
    
    No lookahead - just picks move that flips most pieces.
    """
    
    def __init__(self, config=None):
        """Initialize greedy engine."""
        super().__init__("Greedy", config)
        
        # Use legacy greedy evaluator
        from AI.GreedyEvaluator import GreedyEvaluator
        self.evaluator = GreedyEvaluator()
    
    def get_best_move(self, game, depth: int, **kwargs):
        """
        Find move that captures most pieces immediately.
        
        Args:
            game: Game state
            depth: Ignored (greedy is depth-1)
            **kwargs: Ignored
        
        Returns:
            Move: Greediest move
        """
        moves = game.get_move_list()
        
        if not moves:
            return None
        
        # Evaluate each move greedily
        best_move = None
        best_score = float('-inf')
        
        for move in moves:
            # Make move and evaluate
            game_copy = game.copy() if hasattr(game, 'copy') else self._copy_game(game)
            game_copy.move(move)
            
            score = self.evaluator.evaluate(game_copy)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        self.update_statistics(nodes_evaluated=len(moves))
        
        return best_move
    
    def evaluate_position(self, game) -> float:
        """Evaluate position (piece count)."""
        return self.evaluator.evaluate(game)
    
    def _copy_game(self, game):
        """Manual game copy if copy() not available."""
        from Reversi.Game import Game
        g = Game(game.size)
        g.import_str(game.export_str())
        g.turn = game.turn
        return g

