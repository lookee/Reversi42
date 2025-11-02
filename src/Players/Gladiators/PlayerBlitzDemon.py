"""
BLITZ DEMON 🔥 - The Chaos Incarnate

Speed incarnate. Chaos unleashed. Thinks in microseconds.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerBlitzDemon(Player):
    """
    BLITZ DEMON 🔥 - The Chaos Incarnate
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    BLITZ DEMON doesn't think—it ACTS. Born in the crucible of rapid-fire games 
    where hesitation means death, this frenetic AI embodies pure, unfiltered 
    aggression. It moves faster than thought, striking before you can blink.
    
    No deep calculations, no sophisticated strategies—just raw, primal instinct 
    honed through millions of blitz games compressed into nanoseconds. BLITZ DEMON 
    lives in the moment, thrives in chaos, and dominates through sheer overwhelming 
    speed that leaves opponents dizzy and disoriented.
    
    Perfect for speed chess enthusiasts who value action over contemplation. When 
    BLITZ DEMON enters the arena, the clock becomes your enemy. Can you keep up 
    with pure velocity made manifest? Can you match the tempo of digital lightning?
    
    Try. You'll lose. But at least it'll be over quickly.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐☆☆☆☆☆☆☆ 3/10   (Chaotic Aggression)
    ⚡  SPEED:       ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Instantaneous)
    🎯  ACCURACY:   ⭐⭐⭐☆☆☆☆☆☆☆ 3/10   (Reckless)
    🧠  DEPTH:      ⭐⭐☆☆☆☆☆☆☆☆ 2/10   (Pure Instinct)
    💀  LETHALITY:  ⭐⭐⭐⭐☆☆☆☆☆☆ 4/10   (Death by Speed)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Minimal Pure Alpha-Beta
    Strategy:         Fixed Depth 5 (no iterative deepening)
    
    Evaluators:       ALL 4 (but very shallow depth)
      • Mobility
      • Positional
      • Stability
      • Parity
    
    Optimizations:    NONE (pure speed, no pruning)
    Parallel:         Disabled (overhead reduction)
    
    Average Response: <50ms
    Estimated ELO:    ~1350
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "BLITZ DEMON",
        "description": "Speed Incarnate - Chaos Unleashed",
        "headline": "CHAOS MODE ENGAGED",
        "strategy": "Pure Speed | Depth: 5 | Think Time: <50ms",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "BLITZ DEMON"
        self.depth = 5
        self.deep = 5
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)
            .with_fixed_depth_search()
            .disable_all_pruning()
            .enable_parallel(False)
            .quiet_mode()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n🔥 BLITZ DEMON - CHAOS MODE ENGAGED 🔥")
        print("Strategy: Pure Speed | Depth: 5 | Think Time: <50ms\n")
    
    def get_move(self, game, moves, control):
        if len(moves) == 0:
            return None
        try:
            bitboard_game = self._convert_to_bitboard(game)
            move = self._call_engine_with_observer(
                self.bitboard_engine, bitboard_game, self.deep, observer=control
            )
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

