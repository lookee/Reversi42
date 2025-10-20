"""
Integration tests for diverse Apocalyptron configurations (new refactoring).

Tests different player configurations to ensure they all work correctly.
"""

import os
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from AI.Apocalyptron.factory import ApocalyptronFactory, ApocalyptronConfigBuilder
from AI.Apocalyptron.core.config import EvaluatorConfig
from Players.PlayerApocalyptron import PlayerApocalyptron
from Reversi.BitboardGame import BitboardGame


class TestDiversePlayerConfigurations:
    """Test players with radically different configurations."""
    
    def test_default_player_still_works(self):
        """Test that default player configuration still works (backward compatibility)"""
        player = PlayerApocalyptron(depth=6)
        game = BitboardGame()
        moves = game.get_move_list()
        
        move = player.get_move(game, moves, control=None)
        
        assert move is not None
        assert move in moves
    
    def test_fixed_depth_player(self):
        """Test player with fixed depth strategy"""
        player = PlayerApocalyptron(depth=6, search_strategy='fixed_depth')
        game = BitboardGame()
        moves = game.get_move_list()
        
        move = player.get_move(game, moves, control=None)
        
        assert move is not None
        assert move in moves
    
    def test_adaptive_depth_player(self):
        """Test player with adaptive depth strategy"""
        player = PlayerApocalyptron(depth=8, search_strategy='adaptive')
        game = BitboardGame()
        moves = game.get_move_list()
        
        move = player.get_move(game, moves, control=None)
        
        assert move is not None
        assert move in moves
    
    def test_mobility_only_player(self):
        """Test player with only mobility evaluator"""
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .with_only_mobility()
            .enable_all_optimizations()
            .build()
        )
        
        from AI.Apocalyptron import ApocalyptronEngine
        engine = ApocalyptronEngine(config=config)
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=6)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_positional_only_player(self):
        """Test player with only positional evaluator"""
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .with_only_positional()
            .enable_all_optimizations()
            .build()
        )
        
        from AI.Apocalyptron import ApocalyptronEngine
        engine = ApocalyptronEngine(config=config)
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=6)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_pure_alphabeta_player(self):
        """Test player with no pruning techniques"""
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)  # Lower depth since no pruning
            .with_fixed_depth_search()
            .disable_all_pruning()
            .enable_parallel(False)
            .build()
        )
        
        from AI.Apocalyptron import ApocalyptronEngine
        engine = ApocalyptronEngine(config=config)
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=5)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_speed_demon_preset(self):
        """Test speed_demon factory preset"""
        engine = ApocalyptronFactory.create_speed_demon(depth=5)
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=5)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_mobility_obsessed_preset(self):
        """Test mobility_obsessed factory preset"""
        engine = ApocalyptronFactory.create_mobility_obsessed(depth=6)
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=6)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_corner_hunter_preset(self):
        """Test corner_hunter factory preset"""
        engine = ApocalyptronFactory.create_corner_hunter(depth=6)
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=6)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_adaptive_player_preset(self):
        """Test adaptive_player factory preset"""
        engine = ApocalyptronFactory.create_adaptive_player(
            opening_depth=5,
            mid_depth=7,
            end_depth=9
        )
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=7)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_custom_evaluator_mix(self):
        """Test custom evaluator combination"""
        config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .with_evaluators([
                EvaluatorConfig('mobility', weight=2.0),
                EvaluatorConfig('stability', weight=0.5),
            ])
            .enable_all_optimizations()
            .build()
        )
        
        from AI.Apocalyptron import ApocalyptronEngine
        engine = ApocalyptronEngine(config=config)
        
        game = BitboardGame()
        move = engine.get_best_move(game, depth=6)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_player_with_custom_builder(self):
        """Test PlayerApocalyptron with custom config builder"""
        builder = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .with_fixed_depth_search()
            .with_only_mobility()
            .enable_all_optimizations()
        )
        
        player = PlayerApocalyptron(
            depth=6,  # This will be overridden by builder
            config_builder=builder
        )
        
        game = BitboardGame()
        moves = game.get_move_list()
        move = player.get_move(game, moves, control=None)
        
        assert move is not None
        assert move in moves


class TestBackwardCompatibility:
    """Test that old code still works (backward compatibility)."""
    
    def test_old_style_player_creation(self):
        """Test that old-style player creation still works"""
        # This is how it was done before refactoring
        player = PlayerApocalyptron(depth=8)
        
        game = BitboardGame()
        moves = game.get_move_list()
        move = player.get_move(game, moves, control=None)
        
        assert move is not None
        assert move in moves
    
    def test_old_style_with_weights(self):
        """Test old-style with custom weights"""
        from AI.Apocalyptron.weights import EvaluationWeights
        
        weights = EvaluationWeights()
        weights.mobility_opening = 20  # Custom value
        
        player = PlayerApocalyptron(depth=6, weights=weights)
        
        game = BitboardGame()
        moves = game.get_move_list()
        move = player.get_move(game, moves, control=None)
        
        assert move is not None
        assert move in moves
    
    def test_factory_old_presets_still_work(self):
        """Test that old factory presets still work"""
        # These existed before refactoring
        default_engine = ApocalyptronFactory.create_default(depth=6)
        aggressive_engine = ApocalyptronFactory.create_aggressive(depth=6)
        defensive_engine = ApocalyptronFactory.create_defensive(depth=6)
        
        game = BitboardGame()
        
        # All should work
        move1 = default_engine.get_best_move(game, depth=6)
        move2 = aggressive_engine.get_best_move(game, depth=6)
        move3 = defensive_engine.get_best_move(game, depth=6)
        
        assert move1 in game.get_move_list()
        assert move2 in game.get_move_list()
        assert move3 in game.get_move_list()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

