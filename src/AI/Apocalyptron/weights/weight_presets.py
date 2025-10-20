"""
Weight presets for different playing styles.

Provides ready-to-use weight configurations for various strategies.
"""

from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights


class AggressiveWeights(EvaluationWeights):
    """
    Aggressive player that heavily penalizes opponent mobility.

    Strategy:
    - Maximizes opponent move restriction
    - High mobility differential value
    - Good for controlling the game tempo
    """

    def __init__(self):
        super().__init__()
        self.mobility_opening = 15  # +50% from 10
        self.mobility_midgame = 25  # +67% from 15
        self.mobility_endgame = 8  # +60% from 5
        self.move_order_mobility_penalty = 25  # +67% from 15
        self.corner_weight = 120  # Slightly reduced to balance


class DefensiveWeights(EvaluationWeights):
    """
    Defensive player that prioritizes stability and solid positions.

    Strategy:
    - Maximizes stable pieces
    - Minimizes frontier discs
    - Avoids X-squares aggressively
    - Good for positional, safe play
    """

    def __init__(self):
        super().__init__()
        self.stability_weight = 80  # 2x from 40
        self.frontier_weight = 15  # ~2x from 8
        self.x_square_penalty = 120  # +50% from 80
        self.mobility_midgame = 10  # Reduced from 15
        self.edge_weight = 20  # 2x from 10


class CornerHunterWeights(EvaluationWeights):
    """
    Obsessed with corners - will sacrifice a lot to get them.

    Strategy:
    - Extreme corner priority
    - Very high X-square penalty
    - Corners > everything else
    - Good for aggressive corner play
    """

    def __init__(self):
        super().__init__()
        self.corner_weight = 250  # +67% from 150
        self.move_order_corner = 2000  # 2x from 1000
        self.x_square_penalty = 150  # +88% from 80
        self.stability_weight = 60  # Increased (corners build stability)


class EdgeControlWeights(EvaluationWeights):
    """
    Specialist in edge control and border domination.

    Strategy:
    - High edge value
    - Builds stable edge formations
    - Combines with stability
    - Good for methodical, territorial play
    """

    def __init__(self):
        super().__init__()
        self.edge_weight = 25  # +150% from 10
        self.move_order_edge = 800  # +60% from 500
        self.stability_weight = 60  # +50% from 40
        self.corner_weight = 180  # Slight increase (edges lead to corners)


class EndgameSpecialistWeights(EvaluationWeights):
    """
    Focuses on endgame factors: parity and piece count.

    Strategy:
    - High parity value
    - Strong piece count differential
    - Better endgame mobility
    - Good for converting advantages in final phase
    """

    def __init__(self):
        super().__init__()
        self.parity_favorable = 50  # 2x from 25
        self.parity_unfavorable = -20  # 2x from -10
        self.piece_count_weight = 35  # +75% from 20
        self.mobility_endgame = 12  # +140% from 5


class BalancedWeights(EvaluationWeights):
    """
    Balanced player with even distribution across all factors.

    Strategy:
    - No extreme weights
    - Adaptable to all positions
    - Good general-purpose player
    - This is just the default configuration
    """

    def __init__(self):
        super().__init__()
        # Uses all defaults - this is the "standard" configuration


# ============================================================
# WEIGHT PRESETS REGISTRY
# ============================================================

WEIGHT_PRESETS = {
    "default": EvaluationWeights,
    "aggressive": AggressiveWeights,
    "defensive": DefensiveWeights,
    "corner_hunter": CornerHunterWeights,
    "edge_control": EdgeControlWeights,
    "endgame_specialist": EndgameSpecialistWeights,
    "balanced": BalancedWeights,
}


def get_preset_weights(preset_name="default"):
    """
    Get a preset weight configuration by name.

    Args:
        preset_name: One of 'default', 'aggressive', 'defensive',
                    'corner_hunter', 'edge_control', 'endgame_specialist', 'balanced'

    Returns:
        EvaluationWeights instance

    Raises:
        ValueError: If preset name is unknown
    """
    if preset_name not in WEIGHT_PRESETS:
        available = ", ".join(WEIGHT_PRESETS.keys())
        raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")

    return WEIGHT_PRESETS[preset_name]()


def list_presets():
    """List all available weight presets"""
    return list(WEIGHT_PRESETS.keys())
