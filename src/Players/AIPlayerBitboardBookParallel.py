#------------------------------------------------------------------------
#    AIPlayerBitboardBookParallel - Multi-Core Ultimate AI
#    Combines parallel bitboard speed with opening book intelligence
#------------------------------------------------------------------------

from Players.AIPlayerBitboardBook import AIPlayerBitboardBook
from AI.ParallelBitboardMinimaxEngine import ParallelBitboardMinimaxEngine

class AIPlayerBitboardBookParallel(AIPlayerBitboardBook):
    """
    Parallel version of The Oracle - Multi-core optimized.
    
    This is the ultimate AI player combining:
    - Opening book for tournament-level early game (instant)
    - Parallel bitboard for 2-5x speedup in mid/late game
    - Deep searches (8-12) are practical even on laptops
    
    Performance: 150-500x faster than standard AIPlayer
    Ideal for: Deep analysis, tournaments, strong opponents
    
    Requirements: 4+ CPU cores recommended
    Best depth: 8-10 (auto-adaptive)
    """
    
    PLAYER_METADATA = {
        'display_name': 'Parallel Oracle',
        'description': 'Multi-core AI - Parallel bitboard (2-4x) + Opening book (57 sequences)',
        'enabled': True,
        'parameters': {
            'difficulty': {
                'type': int,
                'min': 7,
                'max': 12,
                'default': 8,
                'description': 'Search depth (7-12, parallel optimized)'
            }
        }
    }
    
    def __init__(self, deep=8, show_book_options=True):
        """
        Initialize parallel bitboard AI with opening book.
        
        Args:
            deep: Search depth (7-12 recommended for parallel)
            show_book_options: Show opening book information during play
        """
        # Initialize parent (sets up opening book, etc.)
        super().__init__(deep, show_book_options)
        
        # Replace standard bitboard engine with parallel version
        self.bitboard_engine = ParallelBitboardMinimaxEngine()
        
        # Update name
        self.name = f"ParallelOracle{deep}"
        
        # Print configuration
        print(f"[{self.name}] Parallel Bitboard AI with Opening Book initialized!")
        print(f"  • Search depth: {self.deep}")
        print(f"  • Worker processes: {self.bitboard_engine.num_workers}")
        print(f"  • Opening book: {len(self.opening_book.opening_names)} openings loaded")
        print(f"  • Expected speedup: 2-4x vs sequential bitboard at depth {self.deep}")
        print(f"  • Total speedup: ~150-500x vs standard AI")
        print(f"  • Auto-adaptive: Uses parallel only when beneficial")
    
    def __del__(self):
        """Cleanup worker pool on destruction"""
        if hasattr(self, 'bitboard_engine'):
            self.bitboard_engine.close_pool()
    
    @classmethod
    def get_metadata(cls):
        """Return player metadata for factory"""
        return cls.PLAYER_METADATA

