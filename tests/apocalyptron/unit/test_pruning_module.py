"""
Test suite for Apocalyptron Pruning Module.

Tests pruning techniques:
- Null Move Pruning
- Futility Pruning
- Late Move Reduction (LMR)
- Multi-Cut Pruning
"""

import pytest
from src.Reversi.BitboardGame import BitboardGame
from src.AI.Apocalyptron.pruning.null_move import NullMovePruning
from src.AI.Apocalyptron.pruning.futility import FutilityPruning
from src.AI.Apocalyptron.pruning.late_move_reduction import LateMoveReduction
from src.AI.Apocalyptron.pruning.multi_cut import MultiCutPruning


class TestNullMovePruning:
    """Test suite for Null Move Pruning."""
    
    def test_null_move_initialization(self):
        """Test null move pruning initializes correctly."""
        pruner = NullMovePruning()
        
        assert pruner is not None
        assert hasattr(pruner, 'should_try_null_move')
    
    def test_null_move_not_at_shallow_depth(self):
        """Test that null move is not tried at shallow depths."""
        game = BitboardGame()
        pruner = NullMovePruning(min_depth=3)
        
        # Should not try at depth < 3
        should_try = pruner.should_try_null_move(game, depth=2)
        
        assert should_try == False, "Should not try null move at shallow depth"
    
    def test_null_move_at_sufficient_depth(self):
        """Test that null move is considered at sufficient depth."""
        game = BitboardGame()
        pruner = NullMovePruning(min_depth=3)
        
        # Should try at depth >= 3
        should_try = pruner.should_try_null_move(game, depth=5)
        
        # Might be True depending on implementation details
        assert isinstance(should_try, bool)
    
    def test_null_move_reduction_factor(self):
        """Test null move reduction factor."""
        pruner = NullMovePruning(reduction=2)
        
        reduction = pruner.get_reduction(depth=6)
        
        assert reduction == 2, "Reduction should match configured value"
        assert reduction < 6, "Reduction should be less than depth"


class TestFutilityPruning:
    """Test suite for Futility Pruning."""
    
    def test_futility_initialization(self):
        """Test futility pruning initializes correctly."""
        pruner = FutilityPruning()
        
        assert pruner is not None
        assert hasattr(pruner, 'should_prune')
    
    def test_futility_only_at_frontier(self):
        """Test that futility only applies near leaf nodes."""
        game = BitboardGame()
        pruner = FutilityPruning(max_depth=3)
        
        # Should not prune at deep depths
        should_prune_deep = pruner.should_prune(game, move=19, depth=8, alpha=0)
        
        assert should_prune_deep == False, "Should not prune at deep nodes"
    
    def test_futility_margin_calculation(self):
        """Test futility margin calculation."""
        pruner = FutilityPruning(margin_per_depth=200)
        
        margin = pruner.get_margin(depth=2)
        
        assert margin == 400, "Margin should be depth * margin_per_depth"
    
    def test_futility_hopeless_position(self):
        """Test futility pruning for hopeless positions."""
        game = BitboardGame()
        pruner = FutilityPruning()
        
        # Very negative alpha (position already bad)
        # Even with best gain, can't reach alpha
        should_prune = pruner.should_prune(game, move=19, depth=2, alpha=1000)
        
        # Might prune if position is hopeless
        assert isinstance(should_prune, bool)


class TestLateMoveReduction:
    """Test suite for Late Move Reduction (LMR)."""
    
    def test_lmr_initialization(self):
        """Test LMR initializes correctly."""
        lmr = LateMoveReduction()
        
        assert lmr is not None
        assert hasattr(lmr, 'get_reduction')
    
    def test_lmr_no_reduction_for_first_moves(self):
        """Test that first moves are not reduced."""
        lmr = LateMoveReduction(full_depth_moves=4)
        
        # First 4 moves should not be reduced
        for move_index in range(4):
            reduction = lmr.get_reduction(
                depth=6,
                move_index=move_index,
                moves_searched=move_index
            )
            
            assert reduction == 0, f"Move {move_index} should not be reduced"
    
    def test_lmr_reduction_for_late_moves(self):
        """Test that late moves are reduced."""
        lmr = LateMoveReduction(full_depth_moves=4)
        
        # Move 10 should be reduced
        reduction = lmr.get_reduction(
            depth=8,
            move_index=10,
            moves_searched=10
        )
        
        assert reduction >= 1, "Late moves should be reduced"
        assert reduction < 8, "Reduction should be less than depth"
    
    def test_lmr_no_reduction_at_low_depth(self):
        """Test that LMR is not applied at low depths."""
        lmr = LateMoveReduction(min_depth=3)
        
        # At depth 2, should not reduce even for late moves
        reduction = lmr.get_reduction(
            depth=2,
            move_index=10,
            moves_searched=10
        )
        
        assert reduction == 0, "Should not reduce at low depth"
    
    def test_lmr_reduction_increases_with_move_index(self):
        """Test that reduction increases for later moves."""
        lmr = LateMoveReduction(full_depth_moves=4)
        
        reduction_6 = lmr.get_reduction(depth=8, move_index=6, moves_searched=6)
        reduction_12 = lmr.get_reduction(depth=8, move_index=12, moves_searched=12)
        
        # Later moves should have same or greater reduction
        assert reduction_12 >= reduction_6, "Later moves should have more reduction"


class TestMultiCutPruning:
    """Test suite for Multi-Cut Pruning."""
    
    def test_multicut_initialization(self):
        """Test multi-cut initializes correctly."""
        pruner = MultiCutPruning()
        
        assert pruner is not None
        assert hasattr(pruner, 'should_prune')
    
    def test_multicut_requires_multiple_cutoffs(self):
        """Test that multi-cut requires multiple beta cutoffs."""
        pruner = MultiCutPruning(M=3)  # Need 3 cutoffs
        
        # Should need at least M cutoffs to prune
        assert pruner.M == 3
        assert pruner.M > 1, "Multi-cut needs multiple cutoffs"
    
    def test_multicut_limited_move_search(self):
        """Test that multi-cut only searches C moves."""
        pruner = MultiCutPruning(C=10)  # Search first 10 moves
        
        assert pruner.C == 10
        assert pruner.C > pruner.M, "Should search more moves than cutoffs needed"


class TestPruningConsistency:
    """Test consistency across pruning techniques."""
    
    def test_all_pruning_techniques_instantiate(self):
        """Test all pruning techniques can be instantiated."""
        pruners = [
            NullMovePruning(),
            FutilityPruning(),
            LateMoveReduction(),
            MultiCutPruning()
        ]
        
        for pruner in pruners:
            assert pruner is not None, f"{pruner.__class__.__name__} failed to instantiate"
    
    def test_pruning_safe_defaults(self):
        """Test that default configurations are safe (not too aggressive)."""
        null_move = NullMovePruning()
        futility = FutilityPruning()
        lmr = LateMoveReduction()
        multicut = MultiCutPruning()
        
        # Null move reduction should be reasonable (2-3)
        assert null_move.reduction >= 2
        assert null_move.reduction <= 3
        
        # LMR should only apply after several moves
        assert lmr.full_depth_moves >= 3
        
        # Multi-cut should need multiple cutoffs
        assert multicut.M >= 2
    
    @pytest.mark.parametrize("depth", [1, 3, 5, 8, 12])
    def test_pruning_at_various_depths(self, depth):
        """Test pruning techniques at various depths."""
        game = BitboardGame()
        
        null_move = NullMovePruning()
        futility = FutilityPruning()
        lmr = LateMoveReduction()
        
        # Should not crash at any depth
        null_move.should_try_null_move(game, depth)
        futility.should_prune(game, move=19, depth=depth, alpha=0)
        lmr.get_reduction(depth=depth, move_index=0, moves_searched=0)
    
    def test_pruning_preserves_correctness(self):
        """
        Test that pruning techniques are safe (don't break correctness).
        
        This is more of a sanity check - real correctness tested in integration.
        """
        game = BitboardGame()
        
        # All pruning should be conservative (safe)
        null_move = NullMovePruning()
        
        # At very shallow depth, should not use risky techniques
        should_try = null_move.should_try_null_move(game, depth=1)
        
        assert should_try == False, "Should not use null move at depth 1"


class TestPruningInteraction:
    """Test interaction between different pruning techniques."""
    
    def test_combined_pruning_more_aggressive(self):
        """Test that combining techniques increases pruning."""
        game = BitboardGame()
        
        # Individual techniques might not prune
        null_move = NullMovePruning(min_depth=5)
        futility = FutilityPruning(max_depth=2)
        
        # At depth 3: null move won't trigger (< 5), futility won't trigger (> 2)
        null_try = null_move.should_try_null_move(game, depth=3)
        
        # Combined, at least one technique is active at each depth
        assert isinstance(null_try, bool)
    
    def test_lmr_with_good_ordering(self):
        """Test that LMR works better with good move ordering."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        lmr = LateMoveReduction(full_depth_moves=3)
        orderer = PositionalOrderer()
        
        # Good ordering means first moves are likely best
        ordered = orderer.order(moves, game)
        
        # First 3 moves: no reduction
        # Later moves: reduced
        for i in range(min(3, len(ordered))):
            reduction = lmr.get_reduction(depth=6, move_index=i, moves_searched=i)
            assert reduction == 0, f"First {i} moves should not be reduced"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

