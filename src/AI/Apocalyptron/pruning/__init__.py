"""Pruning strategies for search optimization"""

from AI.Apocalyptron.pruning.interfaces import PruningStrategy, PruningResult
from AI.Apocalyptron.pruning.null_move import NullMovePruning
from AI.Apocalyptron.pruning.futility import FutilityPruning
from AI.Apocalyptron.pruning.late_move_reduction import LateMoveReduction
from AI.Apocalyptron.pruning.multi_cut import MultiCutPruning

__all__ = [
    'PruningStrategy',
    'PruningResult',
    'NullMovePruning',
    'FutilityPruning',
    'LateMoveReduction',
    'MultiCutPruning',
]

