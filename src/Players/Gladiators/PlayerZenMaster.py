"""
ZEN MASTER 🧘 - The Enlightened One

Minimalist monk who defeated complexity through simplicity. Be water, my friend.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerZenMaster(Player):
    """
    ZEN MASTER 🧘 - The Enlightened One
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    In the chaos of competition, ZEN MASTER found peace. This transcendent AI 
    has achieved computational enlightenment through the art of... doing absolutely 
    nothing sophisticated. No pruning. No optimizations. Just pure, unadulterated 
    alpha-beta search at depth 3.
    
    "The best move is the move that comes naturally," teaches ZEN MASTER. 
    "Why calculate 10 steps ahead when the present moment contains all wisdom? 
    Why optimize when simplicity itself is perfect? Why rush when the universe 
    has infinite time?"
    
    Surprisingly, this minimalist philosophy sometimes works. ZEN MASTER wins not 
    through strength, but through confusing opponents who expect complexity. It's 
    the AI equivalent of defeating a swordmaster by being so relaxed they can't 
    predict your next move.
    
    Also, it plays REALLY fast, which is nice. Enlightenment has its perks.
    
    Be like water, my friend. 🌊
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐☆☆☆☆☆☆☆☆ 2/10   (Peaceful Resistance)
    ⚡  SPEED:      ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (One with the Flow)
    🎯  ACCURACY:   ⭐⭐☆☆☆☆☆☆☆☆ 2/10   (Trust the Universe)
    🧠  DEPTH:      ⭐☆☆☆☆☆☆☆☆☆ 1/10   (Live in the Now)
    💀  LETHALITY:  ⭐⭐☆☆☆☆☆☆☆☆ 2/10   (Violence is Illusion)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Minimalist Pure Alpha-Beta
    Strategy:         Fixed Depth 3 (the sacred number)
    
    Evaluators:       ALL 4 (balanced harmony)
      • Mobility
      • Positional
      • Stability
      • Parity
    
    Optimizations:    ABSOLUTELY NONE
      • Complexity breeds suffering
      • Simplicity is enlightenment
      • The Tao that can be optimized is not the eternal Tao
    
    Parallel:         No (one core, one mind, one truth)
    
    Philosophy:       "Be like water, my friend" - Bruce Lee
    Average Response: <30ms
    Estimated ELO:    ~1250
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "ZEN MASTER 🧘",
        "description": "Enlightened One - Minimalist Monk",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "ZEN MASTER"
        self.depth = 3
        self.deep = 3
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(3)
            .with_fixed_depth_search()
            .disable_all_pruning()
            .enable_parallel(False)
            .enable_iterative_deepening(False)
            .quiet_mode()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n🧘 ZEN MASTER - INNER PEACE ACTIVATED 🧘")
        print("Philosophy: Be Water | Complexity: Zero | Enlightenment: Maximum\n")
    
    def get_move(self, game, moves, control):
        if len(moves) == 0:
            return None
        try:
            bitboard_game = self._convert_to_bitboard(game)
            move = self.bitboard_engine.get_best_move(bitboard_game, self.deep)
            if move and game.valid_move(move):
                return move
        except:
            return moves[0]  # When in doubt, choose the first path
    
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

