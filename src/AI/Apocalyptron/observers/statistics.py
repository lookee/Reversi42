"""
Statistics Observer - Collects search statistics.

Observes search without printing, just collecting data.
"""

from AI.Apocalyptron.observers.interfaces import SearchObserver
from typing import Any, Dict, Optional, List


class StatisticsObserver(SearchObserver):
    """
    Statistics collector observer.
    
    Collects search statistics without printing.
    Useful for analysis, benchmarking, or post-processing.
    """
    
    def __init__(self):
        """Initialize statistics collector"""
        self.reset()
    
    def reset(self):
        """Reset all statistics"""
        self.search_data = {}
        self.iterations = []
        self.moves_evaluated = []
        self.parallel_results = []
    
    def on_search_start(self, depth: int, player_name: Optional[str], game: Any,
                       mode: str = "sequential"):
        """Record search start"""
        self.search_data['target_depth'] = depth
        self.search_data['player_name'] = player_name
        self.search_data['mode'] = mode
        self.search_data['pieces'] = game.black_cnt + game.white_cnt if hasattr(game, 'black_cnt') else 0
    
    def on_iteration_start(self, current_depth: int, target_depth: int,
                          use_aspiration: bool = False,
                          alpha: int = 0, beta: int = 0):
        """Record iteration start"""
        self.current_iteration = {
            'depth': current_depth,
            'use_aspiration': use_aspiration,
            'alpha': alpha,
            'beta': beta,
            'moves': [],
        }
    
    def on_move_evaluated(self, move: Any, value: int, is_best: bool,
                         nodes: int, pruning: int, elapsed_time: float):
        """Record move evaluation"""
        self.moves_evaluated.append({
            'move': str(move),
            'value': value,
            'is_best': is_best,
            'nodes': nodes,
            'pruning': pruning,
            'time': elapsed_time,
        })
        
        if hasattr(self, 'current_iteration'):
            self.current_iteration['moves'].append({
                'move': str(move),
                'value': value,
                'is_best': is_best,
            })
    
    def on_iteration_complete(self, depth: int, best_move: Any, value: int,
                            iteration_time: float, aspiration_success: bool = True):
        """Record iteration completion"""
        if hasattr(self, 'current_iteration'):
            self.current_iteration['best_move'] = str(best_move)
            self.current_iteration['value'] = value
            self.current_iteration['time'] = iteration_time
            self.current_iteration['aspiration_success'] = aspiration_success
            self.iterations.append(self.current_iteration)
    
    def on_search_complete(self, best_move: Any, value: int, 
                          statistics: Dict, total_time: float,
                          opening_book: Any = None, game_history: str = None,
                          game: Any = None):
        """Record search completion"""
        self.search_data['best_move'] = str(best_move) if best_move else None
        self.search_data['value'] = value
        self.search_data['total_time'] = total_time
        self.search_data['statistics'] = statistics
        self.search_data['iterations_count'] = len(self.iterations)
    
    def on_parallel_phase_start(self, depth: int, num_workers: int):
        """Record parallel phase start"""
        self.search_data['parallel_depth'] = depth
        self.search_data['num_workers'] = num_workers
    
    def on_parallel_result(self, move: Any, value: int, is_best: bool,
                          nodes: int, pruning: int):
        """Record parallel result"""
        self.parallel_results.append({
            'move': str(move),
            'value': value,
            'is_best': is_best,
            'nodes': nodes,
            'pruning': pruning,
        })
    
    def get_summary(self) -> Dict:
        """Get complete statistics summary"""
        return {
            'search': self.search_data,
            'iterations': self.iterations,
            'moves_evaluated': self.moves_evaluated,
            'parallel_results': self.parallel_results,
        }
    
    def get_total_nodes(self) -> int:
        """Get total nodes evaluated"""
        if 'statistics' in self.search_data:
            return self.search_data['statistics'].get('nodes', 0)
        return sum(m['nodes'] for m in self.moves_evaluated)
    
    def get_best_move(self) -> Optional[str]:
        """Get best move found"""
        return self.search_data.get('best_move')

