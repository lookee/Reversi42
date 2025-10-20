"""Weight configuration for evaluation"""

from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights
from AI.Apocalyptron.weights.weight_presets import WEIGHT_PRESETS, get_preset_weights, list_presets

__all__ = [
    "EvaluationWeights",
    "get_preset_weights",
    "list_presets",
    "WEIGHT_PRESETS",
]
