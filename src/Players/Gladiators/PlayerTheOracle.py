"""
THE ORACLE 🔮 - Seer of Fates

Endgame prophet that sees 14 moves into the future. Destiny is revealed.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.core.config import EvaluatorConfig
from AI.Apocalyptron.weights import get_preset_weights


class PlayerTheOracle(Player):
    """
    THE ORACLE 🔮 - Seer of Fates
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    THE ORACLE doesn't just play the present—it inhabits the future. This mystical 
    AI has pierced the veil of time, seeing not just your next move, but the 
    entire branching tree of possibilities that stems from it.
    
    With adaptive depth that grows more profound as the game progresses, THE ORACLE 
    becomes increasingly omniscient. In the opening, it's cautious, probing. In the 
    midgame, it's calculating. But in the endgame? It sees 14 moves ahead, mapping 
    every possible outcome with crystalline clarity.
    
    Playing against THE ORACLE is like playing against destiny itself. It knows 
    your moves before you make them. It has calculated the outcome before the 
    game begins. When it speaks, reality listens.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐⭐⭐⭐⭐☆ 9/10   (Prophetic Dominance)
    ⚡  SPEED:      ⭐⭐⭐⭐☆☆☆☆☆☆ 4/10   (Contemplative Wisdom)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐⭐⭐⭐⭐☆ 9/10   (Prescient Precision)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Sees All Futures)
    💀  LETHALITY:  ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Inevitable Fate)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Adaptive Depth Endgame Specialist
    Strategy:         Adaptive Depth (7 → 9 → 14 by game phase)
    
    Evaluators:
      • Parity        (weight: 2.0)
      • Stability     (weight: 1.5)
      • Positional    (weight: 1.0)
    
    Weight Preset:    Endgame Specialist
      • parity_favorable:    50 (2x boost)
      • piece_count_weight:  35 (1.75x boost)
    
    Optimizations:    ALL enabled
    Special Feature:  Extreme endgame depth (14 ply)
    
    Estimated ELO:    ~1850
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "THE ORACLE",
        "description": "Endgame Prophet - Seer of Fates",
        "headline": "PROPHETIC VISION ACTIVATED",
        "strategy": "Adaptive 7/9/14 | Focus: Endgame Mastery",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "THE ORACLE"
        self.depth = 9
        self.deep = 9
        
        weights = get_preset_weights('endgame_specialist')
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(9)
            .with_adaptive_depth(opening=7, midgame=9, endgame=14)
            .with_evaluators([
                EvaluatorConfig('parity', weight=2.0),
                EvaluatorConfig('stability', weight=1.5),
                EvaluatorConfig('positional', weight=1.0),
            ])
            .with_weights(weights)
            .enable_all_optimizations()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n🔮 THE ORACLE - PROPHETIC VISION ACTIVATED 🔮")
        print("Strategy: Adaptive 7/9/14 | Focus: Endgame Mastery\n")
    
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

