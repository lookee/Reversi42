"""
Integration tests for Epic Gladiators.

Tests all 10 legendary fighters to ensure they work correctly.
"""

import os
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from Players.PlayerFactory import PlayerFactory
from Reversi.BitboardGame import BitboardGame


class TestEpicGladiators:
    """Test suite for all 10 Epic Gladiators."""
    
    GLADIATORS = [
        'DIVZERO.EXE',
        'LIGHTNING STRIKE ⚡',
        'THE STRANGLER 🎯',
        'FORTRESS ETERNAL 🛡️',
        'CORNER REAPER 👑',
        'THE ORACLE 🔮',
        'BLITZ DEMON 🔥',
        'THE EXECUTIONER ⚔️',
        'GLITCH_LORD 👾',
        'ZEN MASTER 🧘',
    ]
    
    def test_all_gladiators_can_be_created(self):
        """Test that all gladiators can be instantiated"""
        for name in self.GLADIATORS:
            player = PlayerFactory.create_player(name)
            assert player is not None
            assert hasattr(player, 'get_move')
    
    def test_all_gladiators_make_valid_moves(self):
        """Test that all gladiators make valid moves"""
        game = BitboardGame()
        moves = game.get_move_list()
        
        for name in self.GLADIATORS:
            player = PlayerFactory.create_player(name)
            move = player.get_move(game, moves, control=None)
            
            assert move is not None, f"{name} returned None"
            assert move in moves, f"{name} returned invalid move {move}"
    
    def test_divzero_is_strongest(self):
        """Test that DIVZERO.EXE has the highest depth/strongest config"""
        divzero = PlayerFactory.create_player('DIVZERO.EXE')
        
        # Should have adaptive depth
        config = divzero.bitboard_engine.config
        assert config.search_strategy == 'adaptive'
        assert config.enable_null_move_pruning == True
        assert config.enable_futility_pruning == True
        assert config.use_parallel == True
        
        # Should have all 4 evaluators
        assert len(config.evaluators) == 4
    
    def test_lightning_strike_is_fastest(self):
        """Test that LIGHTNING STRIKE has fastest config"""
        lightning = PlayerFactory.create_player('LIGHTNING STRIKE ⚡')
        
        config = lightning.bitboard_engine.config
        
        # Should be fixed depth
        assert config.search_strategy == 'fixed_depth'
        
        # Should have minimal depth
        assert config.depth <= 5
        
        # Should have no parallel (overhead)
        assert config.use_parallel == False
        
        # Should have no pruning (pure speed)
        assert config.enable_null_move_pruning == False
    
    def test_strangler_focuses_on_mobility(self):
        """Test that THE STRANGLER focuses on mobility"""
        strangler = PlayerFactory.create_player('THE STRANGLER 🎯')
        
        config = strangler.bitboard_engine.config
        
        # Should have only mobility evaluator
        assert len(config.evaluators) == 1
        assert config.evaluators[0].evaluator_type == 'mobility'
        
        # Should have high mobility weight
        assert config.evaluators[0].weight >= 3.0
    
    def test_fortress_focuses_on_stability(self):
        """Test that FORTRESS ETERNAL focuses on stability"""
        fortress = PlayerFactory.create_player('FORTRESS ETERNAL 🛡️')
        
        config = fortress.bitboard_engine.config
        
        # Should have stability evaluator
        has_stability = any(e.evaluator_type == 'stability' for e in config.evaluators)
        assert has_stability
        
        # Should use defensive weights
        assert config.weights.stability_weight >= 80
    
    def test_corner_reaper_focuses_on_corners(self):
        """Test that CORNER REAPER focuses on corners"""
        reaper = PlayerFactory.create_player('CORNER REAPER 👑')
        
        config = reaper.bitboard_engine.config
        
        # Should have only positional evaluator
        assert len(config.evaluators) == 1
        assert config.evaluators[0].evaluator_type == 'positional'
        
        # Should have corner hunter weights
        assert config.weights.corner_weight >= 200
    
    def test_oracle_has_adaptive_depth(self):
        """Test that THE ORACLE uses adaptive depth"""
        oracle = PlayerFactory.create_player('THE ORACLE 🔮')
        
        config = oracle.bitboard_engine.config
        
        # Should be adaptive
        assert config.search_strategy == 'adaptive'
        
        # Should have endgame depth configured
        assert 'endgame' in config.adaptive_depths
        assert config.adaptive_depths['endgame'] >= 12
    
    def test_zen_master_is_minimalist(self):
        """Test that ZEN MASTER is truly minimalist"""
        zen = PlayerFactory.create_player('ZEN MASTER 🧘')
        
        config = zen.bitboard_engine.config
        
        # Should be fixed depth
        assert config.search_strategy == 'fixed_depth'
        
        # Should be very shallow
        assert config.depth <= 3
        
        # Should have NO optimizations
        assert config.enable_null_move_pruning == False
        assert config.enable_futility_pruning == False
        assert config.enable_late_move_reduction == False
        assert config.enable_multi_cut_pruning == False
        assert config.use_parallel == False
    
    def test_glitch_lord_is_chaotic(self):
        """Test that GLITCH_LORD has chaotic config"""
        glitch = PlayerFactory.create_player('GLITCH_LORD 👾')
        
        config = glitch.bitboard_engine.config
        
        # Should have only parity (most abstract)
        assert len(config.evaluators) == 1
        assert config.evaluators[0].evaluator_type == 'parity'
        
        # Should have only LMR enabled (for chaos)
        assert config.enable_late_move_reduction == True
        assert config.enable_null_move_pruning == False
        assert config.enable_futility_pruning == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

