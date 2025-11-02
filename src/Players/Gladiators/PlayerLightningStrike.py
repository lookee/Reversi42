"""
LIGHTNING STRIKE ⚡ - The Blitz Master

Fastest AI player - responds in <100ms. Pure speed, pure instinct.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerLightningStrike(Player):
    """
    LIGHTNING STRIKE ⚡ - The Blitz Master
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    They say lightning never strikes the same place twice—but LIGHTNING STRIKE 
    doesn't need to. This electrifying AI moves at speeds that blur the boundary 
    between thought and action. Born in the eye of a digital storm, it channels 
    pure velocity into every move, striking before opponents can even process 
    what's happening.
    
    LIGHTNING STRIKE doesn't waste time on deep contemplation. It trusts its 
    instincts, its positional awareness honed through millions of simulated games 
    compressed into microseconds. When you play against it, you're not just 
    facing an opponent—you're racing against time itself.
    
    Perfect for blitz games where every second counts. Fast, furious, unstoppable.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐☆☆☆☆☆☆ 4/10   (Quick Strike)
    ⚡  SPEED:      ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Lightning Fast)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐☆☆☆☆☆ 5/10   (Instinctive)
    🧠  DEPTH:      ⭐⭐⭐☆☆☆☆☆☆☆ 3/10   (Shallow & Fast)
    💀  LETHALITY:  ⭐⭐⭐⭐☆☆☆☆☆☆ 4/10   (Overwhelming Speed)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Speed-Optimized Fixed Depth
    Strategy:         Fixed Depth 4 (no iterative deepening)
    
    Evaluators:
      • Positional ONLY (minimal overhead)
    
    Optimizations:    NONE (pure alpha-beta for maximum speed)
    Parallel:         Disabled (overhead too high)
    
    Average Response: <100ms
    Estimated ELO:    ~1400
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "LIGHTNING STRIKE",
        "description": "Blitz Master - Speed Above All",
        "headline": "SPEED MODE ACTIVATED",
        "strategy": "Response time: <100ms | Depth: 4 | Blitz",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "LIGHTNING STRIKE"
        self.depth = 4
        self.deep = 4
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(4)
            .with_fixed_depth_search()
            .with_only_positional()
            .disable_all_pruning()
            .enable_parallel(False)
            .quiet_mode()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n⚡ LIGHTNING STRIKE - SPEED MODE ACTIVATED ⚡")
        print("Response time: <100ms | Depth: 4 | Strategy: Blitz\n")
    
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

