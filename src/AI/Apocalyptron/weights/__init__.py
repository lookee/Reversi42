"""Weight configuration for evaluation"""

from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights
from AI.Apocalyptron.weights.weight_presets import (
    get_preset_weights,
    list_presets,
    WEIGHT_PRESETS
)

__all__ = [
    'EvaluationWeights',
    'get_preset_weights',
    'list_presets',
    'WEIGHT_PRESETS',
]

