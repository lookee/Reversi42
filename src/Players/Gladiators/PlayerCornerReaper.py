"""
CORNER REAPER 👑 - Lord of the Corners

Corner specialist obsessed with the eight sacred thrones of the board.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine
from AI.Apocalyptron.weights import get_preset_weights


class PlayerCornerReaper(Player):
    """
    CORNER REAPER 👑 - Lord of the Corners
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    In the kingdom of Reversi, corners are thrones, and CORNER REAPER is the 
    king-maker. This relentless AI has studied the sacred geometry of the board 
    and knows one truth: control the corners, control destiny.
    
    Every move is calculated with singular obsession—the pursuit of those eight 
    precious squares. CORNER REAPER will sacrifice material, abandon mobility, 
    even appear to lose—all to claim its rightful throne. And once a corner is 
    taken, it becomes an anchor point for an empire that spreads inexorably 
    across the board.
    
    Bow before the Lord of Corners, or be consumed by its territorial ambition.
    The throne awaits, and CORNER REAPER will stop at nothing to claim it.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐⭐⭐☆☆☆ 7/10   (Territorial Dominance)
    ⚡  SPEED:      ⭐⭐⭐⭐⭐☆☆☆☆☆ 5/10   (Methodical Conquest)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐⭐⭐⭐☆☆ 8/10   (Geometric Precision)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐⭐☆☆☆ 7/10   (Strategic Vision)
    💀  LETHALITY:  ⭐⭐⭐⭐⭐⭐⭐☆☆☆ 7/10   (Throne or Death)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Positional-Focused Corner Hunter
    Strategy:         Iterative Deepening 1→9
    
    Evaluators:
      • Positional ONLY
    
    Weight Preset:    Corner Hunter
      • corner_weight:        250 (2.5x boost!)
      • x_square_penalty:     150 (1.9x boost)
      • move_order_corner:   2000 (2x boost)
    
    Optimizations:    ALL enabled
    Special Focus:    Corner acquisition at any cost
    
    Estimated ELO:    ~1720
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "CORNER REAPER",
        "description": "Corner Specialist - Throne Seeker",
        "headline": "TERRITORIAL CONQUEST MODE",
        "strategy": "Corner Domination | Depth: 9",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self):
        Player.__init__(self)
        self.name = "CORNER REAPER"
        self.depth = 9
        self.deep = 9
        
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(9)
            .with_only_positional()
            .with_preset_weights('corner_hunter')
            .enable_all_optimizations()
            .build()
        )
        
        self.bitboard_engine = ApocalyptronEngine(config=config)
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        print("\n👑 CORNER REAPER - TERRITORIAL CONQUEST MODE 👑")
        print("Strategy: Corner Domination | Depth: 9\n")
    
    def get_move(self, game, moves, control):
        if len(moves) == 0:
            return None
        try:
            bitboard_game = self._convert_to_bitboard(game)
            game_history = self._get_game_history(game)
            move = self._call_engine_with_observer(
                self.bitboard_engine,
                bitboard_game,
                self.deep,
                player_name=self.name,
                opening_book=self.opening_book,
                game_history=game_history,
                observer=control
            )
            if move and game.valid_move(move):
                return move
        except:
            return moves[0]
    
    def _get_game_history(self, game):
        """Generate game history string from move history"""
        if not hasattr(game, 'history') or not game.history:
            return ""
        
        # Convert move history to notation
        history_moves = []
        for move in game.history:
            if hasattr(move, 'x') and hasattr(move, 'y'):
                coord = f"{chr(64+move.x)}{move.y}"
                history_moves.append(coord)
        
        return " ".join(history_moves)
    
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

