"""Search algorithms"""

from AI.Apocalyptron.search.alphabeta import AlphaBetaSearch
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.search.interfaces import SearchAlgorithm
from AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
from AI.Apocalyptron.search.parallel import ParallelSearch

# Search strategies (new)
from AI.Apocalyptron.search.strategy_interface import SearchStrategy
from AI.Apocalyptron.search.fixed_depth import FixedDepthStrategy
from AI.Apocalyptron.search.iterative_deepening_strategy import IterativeDeepeningStrategy
from AI.Apocalyptron.search.adaptive_depth import AdaptiveDepthStrategy

__all__ = [
    "SearchAlgorithm",
    "AlphaBetaSearch",
    "AlphaBetaSearchComplete",
    "IterativeDeepeningSearch",
    "ParallelSearch",
    # Strategies
    "SearchStrategy",
    "FixedDepthStrategy",
    "IterativeDeepeningStrategy",
    "AdaptiveDepthStrategy",
]
