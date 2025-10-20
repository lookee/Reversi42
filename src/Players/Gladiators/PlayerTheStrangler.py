"""
THE STRANGLER 🎯 - The Suffocator

Mobility assassin that crushes your options. Watch your moves disappear.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.core.config import EvaluatorConfig
from AI.Apocalyptron.weights import get_preset_weights


class PlayerTheStrangler(Player):
    """
    THE STRANGLER 🎯 - The Suffocator
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    Breathe while you can. THE STRANGLER doesn't win by brute force—it wins by 
    making you wish you'd never started playing. This sadistic AI has mastered 
    the art of suffocation, slowly tightening its grip around your possibilities 
    until you're gasping for valid moves.
    
    Every move is calculated to reduce your options. Watch helplessly as your 
    mobility score plummets while THE STRANGLER expands its own freedom. By the 
    time you realize what's happening, it's already too late. The noose has 
    tightened, and there's no escape.
    
    This is psychological warfare disguised as a board game. THE STRANGLER doesn't 
    just defeat you—it makes you feel the slow, inevitable crush of mathematical 
    inevitability. Your moves dwindle from 10 to 5, from 5 to 2, from 2 to zero. 
    And then... checkmate.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐⭐⭐☆☆☆ 7/10   (Methodical Dominance)
    ⚡  SPEED:      ⭐⭐⭐⭐⭐☆☆☆☆☆ 5/10   (Patient Suffocation)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Surgical Precision)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Deep Calculation)
    💀  LETHALITY:  ⭐⭐⭐⭐⭐⭐⭐⭐⭐☆ 9/10   (Merciless Restriction)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Mobility-Focused Aggressive
    Strategy:         Iterative Deepening 1→10
    
    Evaluators:
      • Mobility ONLY (weight: 3.0 - TRIPLED!)
    
    Weight Preset:    Aggressive (custom enhanced)
      • mobility_opening:  30 (3x boost from 10)
      • mobility_midgame:  45 (3x boost from 15)
      • mobility_endgame:  15 (3x boost from 5)
      • mobility_penalty:  45 (3x boost from 15)
    
    Optimizations:    ALL enabled
    Special Focus:    Opponent mobility destruction
    
    Estimated ELO:    ~1750
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "THE STRANGLER",
        "description": "Mobility Assassin - Suffocates Your Options",
        "headline": "SUFFOCATION MODE ENGAGED",
        "strategy": "Mobility Destruction | Depth: 10 | Mercy: NONE",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "THE STRANGLER"
        self.depth = 10
        self.deep = 10
        
        # Create ultra-aggressive mobility weights
        weights = get_preset_weights('aggressive')
        weights.mobility_opening = 30  # x3 from default
        weights.mobility_midgame = 45  # x3 from default
        weights.mobility_endgame = 15  # x3 from default
        weights.move_order_mobility_penalty = 45  # x3 from default
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(10)
            .with_only_mobility(weight=3.0)
            .with_weights(weights)
            .enable_all_optimizations()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n🎯 THE STRANGLER - SUFFOCATION MODE ENGAGED 🎯")
        print("Strategy: Mobility Destruction | Depth: 10 | Mercy: NONE\n")
    
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

