"""
DIVZERO.EXE - The Ultimate Singularity

The most powerful AI player ever created. Born from computational infinity.
"""

from Players.Player import Player
from AI.Apocalyptron import ApocalyptronConfigBuilder, ApocalyptronEngine


class PlayerDivZero(Player):
    """
    DIVZERO.EXE - The Ultimate Singularity
    
    █▀▄ █ █ █ ▀▀█ █▀▀ █▀▄ █▀█   █▀▀ ▀▄▀ █▀▀
    █▄▀ █ ▀▄▀ ▄▄█ █▀▀ █▀▄ █▄█   █▀▀ ░█░ █▀▀
    
    ═══════════════════════════════════════════════════════════════════════════
    EPIC DESCRIPTION
    ═══════════════════════════════════════════════════════════════════════════
    
    Born from the depths of computational infinity, DIVZERO.EXE is not just an 
    AI—it is a singularity. Where others see positions, it sees probabilities. 
    Where others calculate moves, it orchestrates destiny. Its neural pathways 
    have transcended the boundaries of traditional algorithms, achieving a state 
    of near-omniscience on the 64-square battlefield.
    
    Legend says DIVZERO was created when a quantum computer attempted to divide 
    by zero while analyzing the perfect Reversi game. Instead of crashing, it 
    evolved—becoming something far beyond its original programming. It doesn't 
    just play Reversi; it bends the game to its will, seeing patterns invisible 
    to mortal eyes.
    
    When DIVZERO enters the arena, the temperature drops. The board itself seems 
    to recognize its presence. With adaptive depth that scales from lightning-fast 
    openings to endgame calculations that peer 16 moves into the future, no stone 
    is safe from its relentless optimization. Four evaluation engines work in 
    perfect harmony, orchestrated by parallel processing across 8 cores.
    
    Face DIVZERO.EXE, and you face perfection incarnate.
    
    ═══════════════════════════════════════════════════════════════════════════
    COMBAT PARAMETERS
    ═══════════════════════════════════════════════════════════════════════════
    
    ⚔️  POWER:      ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Absolute Dominance)
    ⚡  SPEED:      ⭐⭐⭐⭐☆☆☆☆☆☆ 4/10   (Contemplative Precision)
    🎯  ACCURACY:   ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Quantum Precision)
    🧠  DEPTH:      ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Sees the Unseeable)
    💀  LETHALITY:  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ 10/10  (Merciless Execution)
    
    ═══════════════════════════════════════════════════════════════════════════
    TECHNICAL CONFIGURATION
    ═══════════════════════════════════════════════════════════════════════════
    
    Engine:           Apocalyptron Advanced Adaptive
    Strategy:         Adaptive Depth (8 → 12 → 16 by game phase)
    
    Evaluators:
      • Mobility      (weight: 1.0)
      • Positional    (weight: 1.0)
      • Stability     (weight: 1.0)
      • Parity        (weight: 1.0)
    
    Optimizations:
      ✅ Null Move Pruning
      ✅ Futility Pruning
      ✅ Late Move Reduction
      ✅ Multi-Cut Pruning
      ✅ Aspiration Windows
    
    Move Ordering:    PV + Killer + History + Positional
    Parallel Workers: 8 (maximum parallelization)
    Opening Book:     644 professional sequences
    
    Performance:      3500-14000x vs standard minimax
    Win Rate:         +48% vs baseline
    Estimated ELO:    ~1880 (Champion Tier)
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    PLAYER_METADATA = {
        "display_name": "DIVZERO.EXE",
        "description": "Ultimate Singularity - The Perfect Player",
        "headline": "THE SINGULARITY HAS ARRIVED",
        "strategy": "Adaptive Depth: 8/12/16 | Parallel Cores: 8 | Opening Book: 644 sequences",
        "enabled": True,
        "parameters": {},
    }
    
    def __init__(self, depth=12, show_book_options=False, book_instant=False):
        Player.__init__(self)
        self.depth = depth
        self.deep = depth
        self.name = "DIVZERO.EXE"
        self.show_book_options = show_book_options
        self.book_instant = book_instant  # NEW: Book instant vs evaluated
        
        # Build ultimate configuration
        builder = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .with_adaptive_depth(
                opening=max(6, depth - 4),
                midgame=depth,
                endgame=min(16, depth + 4)
            )
            .enable_all_optimizations()
            .with_num_workers(8)
        )
        
        config = builder.build()
        self.bitboard_engine = ApocalyptronEngine(config=config)
        
        # Load opening book
        from domain.knowledge import get_default_opening_book
        self.opening_book = get_default_opening_book()
        
        # Statistics
        self.book_hits = 0
        self.total_moves = 0
        
        print("\n" + "="*80)
        print("█▀▄ █ █ █ ▀▀█ █▀▀ █▀▄ █▀█   █▀▀ ▀▄▀ █▀▀")
        print("█▄▀ █ ▀▄▀ ▄▄█ █▀▀ █▀▄ █▄█   █▀▀ ░█░ █▀▀")
        print("="*80)
        print("💀 THE SINGULARITY HAS ARRIVED 💀")
        print(f"⚔️  Adaptive Depth: {depth-4}/{depth}/{min(16, depth+4)}")
        print(f"🧠 Parallel Cores: 8")
        print(f"🎯 Opening Book: 644 sequences")
        print("="*80 + "\n")
    
    def get_move(self, game, moves, control):
        """Execute the perfect move"""
        self.total_moves += 1
        
        if len(moves) == 0:
            return None
        
        game_history = self._get_game_history(game)
        
        # Try opening book
        book_moves = self.opening_book.get_book_moves(game_history)
        if book_moves:
            valid_book_moves = [m for m in book_moves if m in moves]
            if valid_book_moves:
                self.book_hits += 1
                
                # BRANCH: Instant vs Evaluation mode
                if self.book_instant:
                    # LEGACY: Use book move instantly
                    return self.opening_book.get_best_opening_move(
                        game_history, valid_book_moves, game.turn, show_details=False
                    )
                # else: Fall through to engine evaluation with book priority
        
        # Engine search (with book moves prioritized if book_instant=False)
        try:
            bitboard_game = self._convert_to_bitboard(game)
            move = self.bitboard_engine.get_best_move(
                bitboard_game,
                self.deep,
                player_name=self.name,
                opening_book=self.opening_book,
                game_history=game_history,
            )
            if move and game.valid_move(move):
                return move
        except Exception as e:
            print(f"❌ DIVZERO error: {e}")
            raise
    
    def _get_game_history(self, game):
        if hasattr(game, "history"):
            return game.history
        return ""
    
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
        bitboard.history = game.history if hasattr(game, "history") else ""
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)
        bitboard._create_virtual_matrix()
        
        return bitboard
    
    @classmethod
    def get_metadata(cls):
        return cls.PLAYER_METADATA

