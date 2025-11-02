"""
GLITCH_LORD 👾 - The Chaotic Anomaly

A beautiful mistake. Plays like a fever dream. Unpredictably genius.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerGlitchLord(Player):
    """
    GLITCH_LORD 👾 - The Chaotic Anomaly
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    GLITCH_LORD is what happens when AI goes beautifully, gloriously wrong. Born 
    from a corrupted neural network that refused to die, this digital aberration 
    plays Reversi like a fever dream—unpredictable, bizarre, yet strangely 
    effective.
    
    Sometimes it plays genius moves that make grandmasters weep with envy. Other 
    times it makes choices so baffling they seem random, chaotic, nonsensical. 
    But there's method in the madness: GLITCH_LORD evaluates ONLY parity (the 
    most abstract metric imaginable), creating a playing style so alien it's 
    terrifying.
    
    Playing against GLITCH_LORD is like arguing with a quantum computer having 
    an existential crisis while simultaneously composing poetry in a language 
    that doesn't exist. You'll win most of the time... unless you don't. And 
    when you lose, you won't understand how it happened.
    
    Error 404: Sanity not found. Proceeding anyway.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐☆☆☆☆☆ 5/10   (Chaotic Variance)
    ⚡   SPEED:      ⭐⭐⭐⭐⭐⭐⭐☆☆☆ 7/10   (Erratic Bursts)
    🎯  ACCURACY:   ⭐⭐⭐☆☆☆☆☆☆☆ 3/10   (Beautiful Chaos)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐☆☆☆☆ 6/10   (Quantum Logic)
    💀  LETHALITY:  ⭐⭐⭐⭐☆☆☆☆☆☆ 4/10   (Random Critical Hits)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Parity-Only Experimental
    Strategy:         Fixed Depth 6
    
    Evaluators:
      • Parity ONLY (abstract endgame thinking)
    
    Optimizations:
      ❌ Null Move Pruning
      ❌ Futility Pruning
      ✅ Late Move Reduction (only this one for maximum chaos)
      ❌ Multi-Cut Pruning
    
    Special Behavior: Falls back to random move on error
    
    Estimated ELO:    ~1500 (±200 variance!)
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "GLITCH_LORD",
        "description": "Chaotic Anomaly - Beautiful Madness",
        "headline": "REALITY.EXE HAS STOPPED WORKING",
        "strategy": "??????? | Logic: UNDEFINED | Sanity: NULL",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "GLITCH_LORD"
        self.depth = 6
        self.deep = 6
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .with_fixed_depth_search()
            .with_only_parity(weight=1.0)
            .enable_null_move_pruning(False)
            .enable_futility_pruning(False)
            .enable_late_move_reduction(True)  # Only this one for chaos
            .enable_multi_cut_pruning(False)
            .enable_parallel(False)
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n👾 GLITCH_LORD - REALITY.EXE HAS STOPPED WORKING 👾")
        print("Strategy: ??????? | Logic: UNDEFINED | Sanity: NULL\n")
    
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
            # Embrace chaos!
            import random
            return random.choice(moves)
    
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

