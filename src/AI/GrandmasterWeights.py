#------------------------------------------------------------------------
#    GrandmasterWeights - Configuration weights for Grandmaster AI
#    Allows creating different playing styles by adjusting evaluation weights
#------------------------------------------------------------------------

class GrandmasterWeights:
    """
    Configuration class for Grandmaster AI evaluation weights.
    
    All weights can be customized to create different playing styles:
    - Aggressive players that penalize opponent mobility
    - Defensive players that prioritize stability
    - Corner hunters that focus on corners
    - Edge control specialists
    - Custom combinations
    
    Default values are the original Grandmaster weights.
    """
    
    def __init__(self):
        # ============================================================
        # MOBILITY WEIGHTS - Importance of move availability
        # ============================================================
        # Opening phase (0-19 pieces on board)
        self.mobility_opening = 10
        
        # Midgame phase (20-49 pieces)
        self.mobility_midgame = 15
        
        # Endgame phase (50-64 pieces)
        self.mobility_endgame = 5
        
        # ============================================================
        # POSITIONAL WEIGHTS - Strategic square values
        # ============================================================
        # Corner control (critical squares)
        self.corner_weight = 150
        
        # X-square penalty (adjacent to empty corners - dangerous!)
        self.x_square_penalty = 80
        
        # Stability (pieces that cannot be flipped)
        self.stability_weight = 40
        
        # Frontier discs (pieces with empty neighbors - usually bad)
        self.frontier_weight = 8
        
        # Edge control (border squares)
        self.edge_weight = 10
        
        # ============================================================
        # ENDGAME WEIGHTS - Final phase considerations
        # ============================================================
        # Parity advantage (favorable - we make last move)
        self.parity_favorable = 25
        
        # Parity disadvantage (unfavorable - opponent makes last move)
        self.parity_unfavorable = -10
        
        # Piece count differential (only in endgame)
        self.piece_count_weight = 20
        
        # ============================================================
        # MOVE ORDERING WEIGHTS - Search tree optimization
        # ============================================================
        # Corner priority in move ordering
        self.move_order_corner = 1000
        
        # Edge priority in move ordering
        self.move_order_edge = 500
        
        # Center priority in move ordering
        self.move_order_center = 100
        
        # Penalty per opponent move (mobility reduction)
        self.move_order_mobility_penalty = 15
    
    def __repr__(self):
        """String representation for debugging"""
        return (f"GrandmasterWeights("
                f"mobility=[{self.mobility_opening},{self.mobility_midgame},{self.mobility_endgame}], "
                f"corner={self.corner_weight}, "
                f"x_square_penalty={self.x_square_penalty}, "
                f"stability={self.stability_weight})")
    
    def to_dict(self):
        """Export weights as dictionary for serialization"""
        return {
            'mobility_opening': self.mobility_opening,
            'mobility_midgame': self.mobility_midgame,
            'mobility_endgame': self.mobility_endgame,
            'corner_weight': self.corner_weight,
            'x_square_penalty': self.x_square_penalty,
            'stability_weight': self.stability_weight,
            'frontier_weight': self.frontier_weight,
            'edge_weight': self.edge_weight,
            'parity_favorable': self.parity_favorable,
            'parity_unfavorable': self.parity_unfavorable,
            'piece_count_weight': self.piece_count_weight,
            'move_order_corner': self.move_order_corner,
            'move_order_edge': self.move_order_edge,
            'move_order_center': self.move_order_center,
            'move_order_mobility_penalty': self.move_order_mobility_penalty,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create weights from dictionary"""
        weights = cls()
        for key, value in data.items():
            if hasattr(weights, key):
                setattr(weights, key, value)
        return weights
    
    def copy(self):
        """Create a deep copy of these weights"""
        return GrandmasterWeights.from_dict(self.to_dict())


# ============================================================
# PRESET CONFIGURATIONS - Ready-to-use playing styles
# ============================================================

class AggressiveMobilityWeights(GrandmasterWeights):
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
        self.mobility_endgame = 8   # +60% from 5
        self.move_order_mobility_penalty = 25  # +67% from 15
        self.corner_weight = 120  # Slightly reduced to balance


class DefensiveStabilityWeights(GrandmasterWeights):
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
        self.frontier_weight = 15   # ~2x from 8
        self.x_square_penalty = 120  # +50% from 80
        self.mobility_midgame = 10   # Reduced from 15
        self.edge_weight = 20        # 2x from 10


class CornerHunterWeights(GrandmasterWeights):
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


class EdgeControlWeights(GrandmasterWeights):
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


class EndgameSpecialistWeights(GrandmasterWeights):
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


class BalancedWeights(GrandmasterWeights):
    """
    Balanced player with even distribution across all factors.
    
    Strategy:
    - No extreme weights
    - Adaptable to all positions
    - Good general-purpose player
    - This is just the default with minor tweaks
    """
    def __init__(self):
        super().__init__()
        # Uses all defaults - this is the "standard" Grandmaster


# ============================================================
# WEIGHT PRESETS REGISTRY
# ============================================================

WEIGHT_PRESETS = {
    'default': GrandmasterWeights,
    'aggressive': AggressiveMobilityWeights,
    'defensive': DefensiveStabilityWeights,
    'corner_hunter': CornerHunterWeights,
    'edge_control': EdgeControlWeights,
    'endgame_specialist': EndgameSpecialistWeights,
    'balanced': BalancedWeights,
}


def get_preset_weights(preset_name='default'):
    """
    Get a preset weight configuration by name.
    
    Args:
        preset_name: One of 'default', 'aggressive', 'defensive', 
                    'corner_hunter', 'edge_control', 'endgame_specialist', 'balanced'
    
    Returns:
        GrandmasterWeights instance
    
    Raises:
        ValueError: If preset name is unknown
    """
    if preset_name not in WEIGHT_PRESETS:
        available = ', '.join(WEIGHT_PRESETS.keys())
        raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")
    
    return WEIGHT_PRESETS[preset_name]()


def list_presets():
    """List all available weight presets"""
    return list(WEIGHT_PRESETS.keys())

