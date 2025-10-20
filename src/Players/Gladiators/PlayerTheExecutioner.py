"""
THE EXECUTIONER ⚔️ - The Ruthless Destroyer

Brutal hybrid that combines mobility destruction with territorial domination.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.core.config import EvaluatorConfig
from AI.Apocalyptron.weights import get_preset_weights


class PlayerTheExecutioner(Player):
    """
    THE EXECUTIONER ⚔️ - The Ruthless Destroyer
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    THE EXECUTIONER shows no mercy. This brutal AI combines territorial domination 
    with mobility suffocation, creating a two-pronged assault that leaves opponents 
    gasping. It doesn't just win—it obliterates.
    
    Every move serves dual purposes: claim valuable territory while simultaneously 
    crushing opponent options. THE EXECUTIONER is the perfect synthesis of 
    aggression and control, a balanced nightmare that adapts to any defensive 
    strategy you throw at it.
    
    Face THE EXECUTIONER and learn what true ruthlessness means. This is not a 
    game—it's an execution. You are the condemned. The board is the scaffold. 
    And THE EXECUTIONER never misses its mark.
    
    When the final piece falls, you'll understand: mercy was never an option.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Brutal Efficiency)
    ⚡  SPEED:      ⭐⭐⭐⭐⭐⭐☆☆☆☆ 6/10   (Aggressive Pace)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Surgical Strikes)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐⭐☆☆☆ 7/10   (Tactical Depth)
    💀  LETHALITY:  ⭐⭐⭐⭐⭐⭐⭐⭐⭐☆ 9/10   (Total Annihilation)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Hybrid Aggressive Destroyer
    Strategy:         Iterative Deepening 1→9
    
    Evaluators:
      • Mobility      (weight: 2.0)
      • Positional    (weight: 1.5)
    
    Weight Preset:    Aggressive
      • mobility_midgame:  25 (enhanced)
      • mobility_penalty:  25 (enhanced)
    
    Optimizations:    ALL enabled
    Special Focus:    Dual threat (mobility destruction + territory control)
    
    Estimated ELO:    ~1770
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "THE EXECUTIONER ⚔️",
        "description": "Ruthless Destroyer - No Mercy",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "THE EXECUTIONER"
        self.depth = 9
        self.deep = 9
        
        weights = get_preset_weights('aggressive')
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(9)
            .with_evaluators([
                EvaluatorConfig('mobility', weight=2.0),
                EvaluatorConfig('positional', weight=1.5),
            ])
            .with_weights(weights)
            .enable_all_optimizations()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n⚔️ THE EXECUTIONER - ANNIHILATION PROTOCOL ⚔️")
        print("Strategy: Hybrid Destruction | Depth: 9 | Mercy: ZERO\n")
    
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

