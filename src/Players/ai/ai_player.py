"""
Generic AI Player

Dependency Injection: Engine is injected, not hardcoded.
This ONE class replaces 6+ duplicate AIPlayer variants.

Version: 3.2.0
Architecture: Strategy Pattern + Dependency Injection
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from Players.base.player import Player
from AI.base.engine import Engine
from typing import Optional


class AIPlayer(Player):
    """
    Generic AI player using Dependency Injection.
    
    ✨ THIS ONE CLASS REPLACES:
    - AIPlayer
    - AIPlayerBook
    - AIPlayerBitboard
    - AIPlayerBitboardBook
    - AIPlayerBitboardBookParallel
    - AIPlayerGrandmaster
    
    The engine is INJECTED from outside, allowing ANY engine/configuration!
    
    Example:
        # Simple minimax
        engine = MinimaxEngine()
        player = AIPlayer(engine, depth=6)
        
        # Complex configuration
        engine = (EngineBuilder()
            .use_bitboard()
            .with_advanced_evaluator()
            .with_opening_book("master.book")
            .with_parallel_search(threads=8)
            .build())
        player = AIPlayer(engine, depth=9, name="Grandmaster")
    """
    
    PLAYER_METADATA = {
        'display_name': 'AI Player',
        'description': 'Configurable AI with any engine',
        'enabled': True,
        'category': 'ai',
        'parameters': [
            {
                'name': 'depth',
                'display_name': 'Search Depth',
                'type': 'int',
                'min': 1,
                'max': 12,
                'default': 6,
                'description': 'Search depth (higher = stronger but slower)'
            }
        ]
    }
    
    def __init__(self, engine: Engine, depth: int = 6, name: Optional[str] = None):
        """
        Create AI player with injected engine.
        
        Dependency Injection: Engine is passed from outside!
        
        Args:
            engine: Game engine (ANY Engine implementation)
            depth: Search depth
            name: Optional custom name (defaults to engine name + depth)
        """
        # Use custom name or generate from engine
        if name is None:
            name = f"{engine.get_name()}-{depth}"
        
        super().__init__(name)
        
        # DEPENDENCY INJECTION: Engine is injected!
        self.engine = engine
        self.depth = depth
        self.deep = depth  # Backward compatibility
    
    def get_move(self, game, move_list, control):
        """
        Get best move from injected engine.
        
        Args:
            game: Game state
            move_list: Valid moves
            control: Board control
        
        Returns:
            Move: Best move from engine
        """
        if not move_list:
            return None
        
        # Delegate to injected engine
        move = self.engine.get_best_move(
            game,
            depth=self.depth,
            player_name=self.name
        )
        
        return move
    
    def get_engine(self) -> Engine:
        """
        Get the injected engine.
        
        Returns:
            Engine: Current engine instance
        """
        return self.engine
    
    def set_engine(self, engine: Engine):
        """
        Replace engine at runtime.
        
        Args:
            engine: New engine to use
        """
        self.engine = engine
    
    def get_engine_stats(self):
        """
        Get engine statistics.
        
        Returns:
            dict: Engine performance stats
        """
        return self.engine.get_statistics()
    
    def set_depth(self, depth: int):
        """
        Change search depth.
        
        Args:
            depth: New search depth
        """
        self.depth = depth
        self.deep = depth
    
    def __repr__(self):
        return f"AIPlayer(engine={self.engine}, depth={self.depth}, name='{self.name}')"

