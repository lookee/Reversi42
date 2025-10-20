"""
FORTRESS ETERNAL 🛡️ - The Immovable Object

Defensive master that builds unbreakable positions. Walls never fall.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.core.config import EvaluatorConfig
from AI.Apocalyptron.weights import get_preset_weights


class PlayerFortressEternal(Player):
    """
    FORTRESS ETERNAL 🛡️ - The Immovable Object
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    Some say FORTRESS ETERNAL was forged in the heart of an ancient mountain, 
    where time moves slower and patience is infinite. This defensive juggernaut 
    doesn't rush to victory—it builds an empire so solid that opponents crumble 
    against its walls.
    
    Every piece placed is a brick in an indestructible fortress. Stability is 
    its creed, permanence its goal. Watch as your aggressive attacks bounce off 
    its impenetrable defenses, each flip revealing another layer of strategic 
    depth you hadn't anticipated.
    
    FORTRESS ETERNAL doesn't play to win quickly. It plays to make losing 
    impossible. Like a castle that withstands centuries of siege, this AI builds 
    positions so stable that time itself cannot erode them. Your attacks break 
    like waves against stone. Your strategies crumble to dust.
    
    In the end, fortresses outlast all aggression.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Immovable Strength)
    ⚡  SPEED:      ⭐⭐⭐⭐☆☆☆☆☆☆ 4/10   (Methodical Building)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Calculated Defense)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Patient Planning)
    💀  LETHALITY:  ⭐⭐⭐⭐⭐⭐⭐☆☆☆ 7/10   (Inevitable Victory)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Stability-Focused Defensive
    Strategy:         Iterative Deepening 1→10
    
    Evaluators:
      • Stability     (weight: 2.0)
      • Positional    (weight: 1.5)
    
    Weight Preset:    Defensive
      • stability_weight:   80 (2x boost)
      • frontier_weight:    15 (2x boost)
      • x_square_penalty:  120 (1.5x boost)
    
    Optimizations:    ALL enabled
    Special Focus:    Unflippable piece maximization
    
    Estimated ELO:    ~1800
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "FORTRESS ETERNAL",
        "description": "Defensive Master - The Immovable Object",
        "headline": "DEFENSE PROTOCOL ACTIVE",
        "strategy": "Impenetrable Stability | Depth: 10",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "FORTRESS ETERNAL"
        self.depth = 10
        self.deep = 10
        
        weights = get_preset_weights('defensive')
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(10)
            .with_evaluators([
                EvaluatorConfig('stability', weight=2.0),
                EvaluatorConfig('positional', weight=1.5),
            ])
            .with_weights(weights)
            .enable_all_optimizations()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n🛡️ FORTRESS ETERNAL - DEFENSE PROTOCOL ACTIVE 🛡️")
        print("Strategy: Impenetrable Stability | Depth: 10\n")
    
    def get_move(self, game, moves, control):
        if len(moves) == 0:
            return None
        try:
            bitboard_game = self._convert_to_bitboard(game)
            move = self.bitboard_engine.get_best_move(bitboard_game, self.deep)
            if move and game.valid_move(move):
                return move
        except:
            return moves[0]
    
    def _convert_to_bitboard(self, game):
        from Reversi.BitboardGame import BitboardGame
        bitboard = BitboardGame.create_empty()
        for y in range(1, 9):
            for x in range(1, 9):
                cell = game.matrix[y][x]
                bit = (y - 1) * 8 + (x - 1)
                if cell == "B":
                    bitboard.black |= 1 << bit
                elif cell == "W":
                    bitboard.white |= 1 << bit
        bitboard.turn = game.turn
        bitboard.turn_cnt = game.turn_cnt
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)
        bitboard._create_virtual_matrix()
        return bitboard
    
    @classmethod
    def get_metadata(cls):
        return cls.PLAYER_METADATA

