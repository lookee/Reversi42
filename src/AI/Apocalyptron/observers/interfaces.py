"""
Search Observer interfaces.

Defines the contract for observing search progress and results.
Implements Observer Pattern for complete separation of concerns.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class SearchObserver(ABC):
    """
    Abstract base class for search observers.
    
    Observers are notified of search events:
    - Search start/end
    - Iteration start/end
    - Move evaluation
    - Statistics updates
    
    This allows complete separation of search logic from output/UI.
    """
    
    @abstractmethod
    def on_search_start(self, depth: int, player_name: Optional[str], game: Any,
                       mode: str = "sequential"):
        """
        Called when search starts.
        
        Args:
            depth: Target search depth
            player_name: Player name (optional)
            game: Game instance
            mode: "sequential", "parallel", or "hybrid"
        """
        pass
    
    @abstractmethod
    def on_iteration_start(self, current_depth: int, target_depth: int,
                          use_aspiration: bool = False,
                          alpha: int = 0, beta: int = 0):
        """
        Called when an iteration starts (iterative deepening).
        
        Args:
            current_depth: Current iteration depth
            target_depth: Target final depth
            use_aspiration: Whether aspiration windows are used
            alpha, beta: Aspiration window bounds
        """
        pass
    
    @abstractmethod
    def on_move_evaluated(self, move: Any, value: int, is_best: bool,
                         nodes: int, pruning: int, elapsed_time: float):
        """
        Called after each move is evaluated.
        
        Args:
            move: Move that was evaluated
            value: Evaluation score
            is_best: Whether this is the new best move
            nodes: Nodes searched
            pruning: Nodes pruned
            elapsed_time: Time elapsed for this move
        """
        pass
    
    @abstractmethod
    def on_iteration_complete(self, depth: int, best_move: Any, value: int,
                            iteration_time: float, aspiration_success: bool = True):
        """
        Called when an iteration completes.
        
        Args:
            depth: Depth that was completed
            best_move: Best move found at this depth
            value: Evaluation value
            iteration_time: Time for this iteration
            aspiration_success: Whether aspiration window succeeded
        """
        pass
    
    @abstractmethod
    def on_search_complete(self, best_move: Any, value: int, 
                          statistics: Dict, total_time: float,
                          opening_book: Any = None, game_history: str = None,
                          game: Any = None):
        """
        Called when search completes.
        
        Args:
            best_move: Best move found
            value: Final evaluation
            statistics: Complete search statistics
            total_time: Total search time
            opening_book: Opening book instance (optional, for display)
            game_history: Game history (optional, for display)
            game: Game instance (optional, for display)
        """
        pass
    
    @abstractmethod
    def on_parallel_phase_start(self, depth: int, num_workers: int):
        """
        Called when parallel search phase starts.
        
        Args:
            depth: Depth for parallel search
            num_workers: Number of worker processes
        """
        pass
    
    @abstractmethod
    def on_parallel_result(self, move: Any, value: int, is_best: bool,
                          nodes: int, pruning: int):
        """
        Called for each parallel search result.
        
        Args:
            move: Move evaluated
            value: Evaluation score
            is_best: Whether this is the new best
            nodes: Nodes searched
            pruning: Nodes pruned
        """
        pass

