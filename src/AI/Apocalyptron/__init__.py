"""
Apocalyptron - Ultimate Reversi AI Engine

Clean architecture refactoring of Grandmaster AI with SOLID principles
and design patterns for maximum maintainability and extensibility.

Main exports:
    - ApocalyptronEngine: Main engine
    - ApocalyptronConfig: Configuration
    - ApocalyptronFactory: Factory for creating engines
"""

from AI.Apocalyptron.core.engine import ApocalyptronEngine
from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.Apocalyptron.factory.factory import ApocalyptronFactory
from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder
from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights
from AI.Apocalyptron.weights.weight_presets import get_preset_weights, list_presets

__all__ = [
    'ApocalyptronEngine',
    'ApocalyptronConfig',
    'ApocalyptronFactory',
    'ApocalyptronConfigBuilder',
    'EvaluationWeights',
    'get_preset_weights',
    'list_presets',
]

__version__ = '1.0.0'
__author__ = 'Luca Amore'
__description__ = 'Ultimate Reversi AI with clean architecture'

