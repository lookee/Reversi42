"""Search algorithms"""

from AI.Apocalyptron.search.alphabeta import AlphaBetaSearch
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.search.interfaces import SearchAlgorithm
from AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
from AI.Apocalyptron.search.parallel import ParallelSearch

__all__ = [
    "SearchAlgorithm",
    "AlphaBetaSearch",
    "AlphaBetaSearchComplete",
    "IterativeDeepeningSearch",
    "ParallelSearch",
]
