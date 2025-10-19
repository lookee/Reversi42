"""
Evaluation weights configuration.

Defines all weight parameters for position evaluation and move ordering.
Identical to GrandmasterWeights but renamed for Apocalyptron.
"""


class EvaluationWeights:
    """
    Configuration class for Apocalyptron evaluation weights.
    
    All weights can be customized to create different playing styles:
    - Aggressive players that penalize opponent mobility
    - Defensive players that prioritize stability
    - Corner hunters that focus on corners
    - Edge control specialists
    - Custom combinations
    
    Default values are identical to original Grandmaster weights.
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
        return (f"EvaluationWeights("
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
        return EvaluationWeights.from_dict(self.to_dict())

