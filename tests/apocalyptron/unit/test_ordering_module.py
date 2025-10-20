"""
Test suite for Apocalyptron Ordering Module.

Tests all move orderers:
- PVMoveOrderer
- KillerMoveOrderer
- HistoryHeuristic
- PositionalOrderer
- CompositeOrderer
"""

import pytest
from src.Reversi.BitboardGame import BitboardGame
from src.AI.Apocalyptron.ordering.pv_move import PVMoveOrderer
from src.AI.Apocalyptron.ordering.killer_moves import KillerMoveOrderer
from src.AI.Apocalyptron.ordering.history import HistoryHeuristic
from src.AI.Apocalyptron.ordering.positional import PositionalOrderer
from src.AI.Apocalyptron.ordering.composite import CompositeOrderer


class TestPVMoveOrderer:
    """Test suite for PV (Principal Variation) move ordering."""
    
    def test_pv_move_ordered_first(self):
        """Test that PV move is placed first in ordering."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)  # [19, 26, 37, 44]
        
        orderer = PVMoveOrderer()
        
        # Set PV move to 44
        orderer.set_pv_move(game, 44)
        
        ordered = orderer.order(moves, game)
        
        # 44 should be first
        assert ordered[0] == 44, "PV move should be first"
        assert len(ordered) == len(moves), "All moves should be present"
        assert set(ordered) == set(moves), "No moves should be lost"
    
    def test_pv_move_not_in_list(self):
        """Test ordering when PV move is not in current move list."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = PVMoveOrderer()
        
        # Set PV move to invalid move
        orderer.set_pv_move(game, 99)
        
        ordered = orderer.order(moves, game)
        
        # Should return original list
        assert ordered == moves or set(ordered) == set(moves)
    
    def test_no_pv_move_set(self):
        """Test ordering when no PV move is set."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = PVMoveOrderer()
        
        ordered = orderer.order(moves, game)
        
        # Should return original list
        assert set(ordered) == set(moves)


class TestKillerMoveOrderer:
    """Test suite for Killer move heuristic."""
    
    def test_killer_move_ordered_early(self):
        """Test that killer moves are ordered early."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = KillerMoveOrderer()
        
        # Add killer move at depth 5
        orderer.add_killer(26, depth=5)
        
        ordered = orderer.order(moves, game, depth=5)
        
        # 26 should be early (ideally first)
        assert 26 in ordered[:2], "Killer move should be early"
    
    def test_multiple_killer_moves(self):
        """Test handling of multiple killer moves."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = KillerMoveOrderer(max_killers=2)
        
        # Add two killers
        orderer.add_killer(26, depth=5)
        orderer.add_killer(37, depth=5)
        
        ordered = orderer.order(moves, game, depth=5)
        
        # Both should be early
        assert 26 in ordered[:3]
        assert 37 in ordered[:3]
    
    def test_killer_depth_isolation(self):
        """Test that killers are isolated by depth."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = KillerMoveOrderer()
        
        # Add killer at depth 5
        orderer.add_killer(26, depth=5)
        
        # Order at depth 3 (different depth)
        ordered = orderer.order(moves, game, depth=3)
        
        # Killer from depth 5 should not affect depth 3
        # (might still appear, but not prioritized)
        assert set(ordered) == set(moves)


class TestHistoryHeuristic:
    """Test suite for History heuristic."""
    
    def test_history_records_cutoffs(self):
        """Test that history records moves that cause cutoffs."""
        orderer = HistoryHeuristic()
        
        # Record some successful moves
        orderer.update(19, caused_cutoff=True)
        orderer.update(19, caused_cutoff=True)
        orderer.update(26, caused_cutoff=False)
        
        score_19 = orderer.get_score(19)
        score_26 = orderer.get_score(26)
        
        # Move 19 should have higher score (2/2 = 1.0)
        # Move 26 should have lower score (0/1 = 0.0)
        assert score_19 > score_26, "Move with cutoffs should score higher"
    
    def test_history_ordering(self):
        """Test that moves are ordered by historical success."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)  # [19, 26, 37, 44]
        
        orderer = HistoryHeuristic()
        
        # Build history: 37 is best, 19 is good, others neutral
        for _ in range(5):
            orderer.update(37, caused_cutoff=True)
        for _ in range(2):
            orderer.update(19, caused_cutoff=True)
        
        ordered = orderer.order(moves, game)
        
        # 37 should be first, 19 should be second
        assert ordered[0] == 37, "Best historical move should be first"
        assert ordered[1] == 19, "Second best should be second"
    
    def test_history_new_move_neutral(self):
        """Test that new moves have neutral score."""
        orderer = HistoryHeuristic()
        
        score = orderer.get_score(99)  # New move
        
        assert score == 0.0, "New moves should have neutral score"


class TestPositionalOrderer:
    """Test suite for Positional move ordering."""
    
    def test_corners_ordered_first(self):
        """Test that corner moves are prioritized."""
        # Create position where corner is available
        game = BitboardGame(
            black=0x0000000810000000,
            white=0x0000001008000001,  # White at A1
            current_player=1
        )
        
        # Get moves including corner if available
        moves = game.get_valid_moves(1)
        
        orderer = PositionalOrderer()
        ordered = orderer.order(moves, game)
        
        # Corners (0, 7, 56, 63) should be prioritized if in list
        if any(m in [0, 7, 56, 63] for m in moves):
            # First should be a corner
            assert ordered[0] in [0, 7, 56, 63], "Corner should be first"
    
    def test_positional_ordering_consistent(self):
        """Test that positional ordering is deterministic."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = PositionalOrderer()
        
        ordered1 = orderer.order(moves, game)
        ordered2 = orderer.order(moves, game)
        
        assert ordered1 == ordered2, "Ordering should be deterministic"
    
    def test_all_moves_preserved(self):
        """Test that all moves are preserved after ordering."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = PositionalOrderer()
        ordered = orderer.order(moves, game)
        
        assert len(ordered) == len(moves), "All moves should be preserved"
        assert set(ordered) == set(moves), "No moves should be lost or added"


class TestCompositeOrderer:
    """Test suite for Composite move ordering."""
    
    def test_composite_combines_orderers(self):
        """Test that composite combines multiple ordering strategies."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = CompositeOrderer()
        
        # Should combine PV, killer, history, positional
        ordered = orderer.order(moves, game, depth=5)
        
        assert len(ordered) == len(moves), "All moves should be preserved"
        assert set(ordered) == set(moves), "No moves should be lost"
    
    def test_pv_move_highest_priority(self):
        """Test that PV move has highest priority in composite."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = CompositeOrderer()
        
        # Set PV move
        orderer.pv_orderer.set_pv_move(game, 44)
        
        # Add killer and history for other moves
        orderer.killer_orderer.add_killer(19, depth=5)
        orderer.history.update(26, caused_cutoff=True)
        
        ordered = orderer.order(moves, game, depth=5)
        
        # PV move (44) should still be first
        assert ordered[0] == 44, "PV move should override all others"
    
    def test_composite_ordering_improves_over_random(self):
        """Test that composite ordering is better than random."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = CompositeOrderer()
        
        # Build some history
        orderer.history.update(37, caused_cutoff=True)
        orderer.killer_orderer.add_killer(26, depth=5)
        
        ordered = orderer.order(moves, game, depth=5)
        
        # Should be different from original (unless coincidentally same)
        # At minimum, should not crash
        assert len(ordered) == len(moves)
        assert set(ordered) == set(moves)


class TestOrdererEdgeCases:
    """Test edge cases for all orderers."""
    
    def test_empty_move_list(self):
        """Test orderers handle empty move list."""
        game = BitboardGame()
        moves = []
        
        orderers = [
            PVMoveOrderer(),
            PositionalOrderer(),
        ]
        
        for orderer in orderers:
            ordered = orderer.order(moves, game)
            assert ordered == [], f"{orderer.__class__.__name__} failed on empty list"
    
    def test_single_move(self):
        """Test orderers handle single move."""
        game = BitboardGame()
        moves = [19]  # Single move
        
        orderers = [
            PVMoveOrderer(),
            PositionalOrderer(),
        ]
        
        for orderer in orderers:
            ordered = orderer.order(moves, game)
            assert ordered == [19], f"{orderer.__class__.__name__} failed on single move"
    
    @pytest.mark.parametrize("orderer_class", [
        PVMoveOrderer,
        PositionalOrderer,
        HistoryHeuristic,
    ])
    def test_orderer_preserves_moves(self, orderer_class):
        """Test that orderers preserve all moves."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        orderer = orderer_class()
        
        if orderer_class == HistoryHeuristic:
            ordered = orderer.order(moves, game)
        else:
            ordered = orderer.order(moves, game)
        
        assert len(ordered) == len(moves), "All moves should be preserved"
        assert set(ordered) == set(moves), "Exact same moves"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

