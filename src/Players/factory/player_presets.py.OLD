"""
Player Presets

Pre-configured player/engine combinations for easy creation.

Version: 3.2.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from AI.factory.engine_builder import EngineBuilder
from Players.ai.ai_player import AIPlayer


class PlayerPresets:
    """
    Pre-configured player presets.
    
    Provides easy creation of common player configurations.
    
    Example:
        player = PlayerPresets.create_grandmaster(depth=9)
        player = PlayerPresets.create_beginner(depth=3)
    """
    
    @staticmethod
    def create_beginner(depth: int = 3) -> AIPlayer:
        """
        Create beginner-level AI.
        
        Args:
            depth: Search depth (default 3)
        
        Returns:
            AIPlayer: Beginner-level player
        """
        engine = (EngineBuilder()
            .use_minimax()
            .with_standard_evaluator()
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Beginner-{depth}")
    
    @staticmethod
    def create_intermediate(depth: int = 6) -> AIPlayer:
        """
        Create intermediate-level AI.
        
        Args:
            depth: Search depth (default 6)
        
        Returns:
            AIPlayer: Intermediate player
        """
        engine = (EngineBuilder()
            .use_bitboard()
            .with_advanced_evaluator()
            .with_opening_book()
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Intermediate-{depth}")
    
    @staticmethod
    def create_advanced(depth: int = 8) -> AIPlayer:
        """
        Create advanced-level AI.
        
        Args:
            depth: Search depth (default 8)
        
        Returns:
            AIPlayer: Advanced player
        """
        engine = (EngineBuilder()
            .use_bitboard()
            .with_advanced_evaluator()
            .with_opening_book()
            .with_transposition_table(size_mb=128)
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Advanced-{depth}")
    
    @staticmethod
    def create_grandmaster(depth: int = 9) -> AIPlayer:
        """
        Create grandmaster-level AI.
        
        Args:
            depth: Search depth (default 9)
        
        Returns:
            AIPlayer: Grandmaster player
        """
        engine = (EngineBuilder()
            .use_grandmaster()
            .with_advanced_evaluator()
            .with_opening_book()
            .with_transposition_table(size_mb=256)
            .with_endgame_solver(depth_trigger=14)
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Grandmaster-{depth}")
    
    @staticmethod
    def create_alpha_beta(depth: int = 6) -> AIPlayer:
        """
        Create standard alpha-beta AI.
        
        Args:
            depth: Search depth (default 6)
        
        Returns:
            AIPlayer: Alpha-beta player
        """
        engine = (EngineBuilder()
            .use_minimax()
            .with_standard_evaluator()
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"AlphaBeta-{depth}")
    
    @staticmethod
    def create_opening_scholar(depth: int = 6) -> AIPlayer:
        """
        Create AI with opening book.
        
        Args:
            depth: Search depth (default 6)
        
        Returns:
            AIPlayer: Opening scholar
        """
        engine = (EngineBuilder()
            .use_minimax()
            .with_standard_evaluator()
            .with_opening_book()
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Scholar-{depth}")
    
    @staticmethod
    def create_bitboard_blitz(depth: int = 6) -> AIPlayer:
        """
        Create fast bitboard AI.
        
        Args:
            depth: Search depth (default 6)
        
        Returns:
            AIPlayer: Bitboard player
        """
        engine = (EngineBuilder()
            .use_bitboard()
            .with_standard_evaluator()
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Bitboard-{depth}")
    
    @staticmethod
    def create_oracle(depth: int = 7) -> AIPlayer:
        """
        Create bitboard AI with opening book.
        
        Args:
            depth: Search depth (default 7)
        
        Returns:
            AIPlayer: Oracle player
        """
        engine = (EngineBuilder()
            .use_bitboard()
            .with_advanced_evaluator()
            .with_opening_book()
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Oracle-{depth}")
    
    @staticmethod
    def create_parallel_oracle(depth: int = 7, threads: int = 4) -> AIPlayer:
        """
        Create parallel bitboard AI with opening book.
        
        Args:
            depth: Search depth (default 7)
            threads: Number of threads (default 4)
        
        Returns:
            AIPlayer: Parallel oracle
        """
        engine = (EngineBuilder()
            .use_bitboard()
            .with_advanced_evaluator()
            .with_opening_book()
            .with_parallel_search(threads=threads)
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"ParallelOracle-{depth}")
    
    @staticmethod
    def create_random() -> 'Player':
        """
        Create random player.
        
        Returns:
            Player: Random player (from legacy)
        """
        # Use legacy Monkey player for compatibility
        from Players.Monkey import Monkey
        return Monkey()
    
    @staticmethod
    def create_greedy() -> AIPlayer:
        """
        Create greedy player.
        
        Returns:
            AIPlayer: Greedy player
        """
        engine = (EngineBuilder()
            .use_greedy()
            .with_greedy_evaluator()
            .build())
        
        return AIPlayer(engine=engine, depth=1, name="Greedy")
    
    @staticmethod
    def create_heuristic(depth: int = 4) -> AIPlayer:
        """
        Create heuristic player.
        
        Args:
            depth: Search depth (default 4)
        
        Returns:
            AIPlayer: Heuristic player
        """
        engine = (EngineBuilder()
            .use_heuristic()
            .build())
        
        return AIPlayer(engine=engine, depth=depth, name=f"Heuristic-{depth}")

