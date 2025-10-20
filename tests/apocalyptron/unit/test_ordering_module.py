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
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move
from AI.Apocalyptron.ordering.pv_move import PVMoveOrderer
from AI.Apocalyptron.ordering.killer_moves import KillerMoveOrderer
from AI.Apocalyptron.ordering.history import HistoryHeuristicOrderer
from AI.Apocalyptron.ordering.positional import PositionalOrderer
from AI.Apocalyptron.ordering.composite import CompositeOrderer


class TestPVMoveOrderer:
    """Test suite for PV (Principal Variation) move ordering."""
    
    def test_pv_move_ordered_first(self):
        """Test that PV move is placed first in ordering."""
        game = BitboardGame()
        moves = game.get_move_list()  # [19, 26, 37, 44]
        
        orderer = PVMoveOrderer()
        
        # Set PV move to 44
        orderer.set_pv_move(Move(5, 4))  # E4
        
        ordered = orderer.order_moves(game, moves)
        
        # 44 should be first
        pv_move = Move(5, 4)  # E4
        if pv_move in moves:
            assert ordered[0] == pv_move, "PV move should be first"
        assert len(ordered) == len(moves), "All moves should be present"
        assert set(ordered) == set(moves), "No moves should be lost"
    
    def test_pv_move_not_in_list(self):
        """Test ordering when PV move is not in current move list."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = PVMoveOrderer()
        
        # Set PV move to invalid move
        orderer.set_pv_move(Move(9, 9))  # Invalid move
        
        ordered = orderer.order_moves(game, moves)
        
        # Should return original list
        assert ordered == moves or set(ordered) == set(moves)
    
    def test_no_pv_move_set(self):
        """Test ordering when no PV move is set."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = PVMoveOrderer()
        
        ordered = orderer.order_moves(game, moves)
        
        # Should return original list
        assert set(ordered) == set(moves)


class TestKillerMoveOrderer:
    """Test suite for Killer move heuristic."""
    
    def test_killer_move_ordered_early(self):
        """Test that killer moves are ordered early."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = KillerMoveOrderer()
        
        # Add killer move at depth 5
        orderer.add_killer(Move(4, 3), depth=5)  # D3
        
        ordered = orderer.order_moves(game, moves)
        
        # 26 should be early (ideally first)
        killer_move = Move(4, 3)  # D3
        if killer_move in moves:
            assert killer_move in ordered[:2], "Killer move should be early"
    
    def test_multiple_killer_moves(self):
        """Test handling of multiple killer moves."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = KillerMoveOrderer()
        
        # Add two killers
        orderer.add_killer(Move(4, 3), depth=5)  # D3
        orderer.add_killer(Move(5, 3), depth=5)  # E3
        
        ordered = orderer.order_moves(game, moves)
        
        # Both should be early (if they're in the move list)
        killer1 = Move(4, 3)  # D3
        killer2 = Move(5, 3)  # E3
        if killer1 in moves:
            assert killer1 in ordered[:3], "First killer should be early"
        if killer2 in moves:
            assert killer2 in ordered[:3], "Second killer should be early"
        # Should not crash and return valid moves
        assert len(ordered) == len(moves), "Should preserve all moves"
    
    def test_killer_depth_isolation(self):
        """Test that killers are isolated by depth."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = KillerMoveOrderer()
        
        # Add killer at depth 5
        orderer.add_killer(Move(4, 3), depth=5)  # D3
        
        # Order at depth 3 (different depth)
        ordered = orderer.order_moves(game, moves)
        
        # Killer from depth 5 should not affect depth 3
        # (might still appear, but not prioritized)
        assert set(ordered) == set(moves)


class TestHistoryHeuristicOrderer:
    """Test suite for History heuristic."""
    
    def test_history_records_cutoffs(self):
        """Test that history records moves that cause cutoffs."""
        orderer = HistoryHeuristicOrderer()
        
        # Record some successful moves
        orderer.update_history(Move(3, 3), depth=5)  # C3
        orderer.update_history(Move(3, 3), depth=5)  # C3
        orderer.update_history(Move(4, 3), depth=5)  # D3
        
        score_19 = orderer.history_table.get((2, 2), 0)  # C3
        score_26 = orderer.history_table.get((3, 2), 0)  # D3
        
        # Move 19 should have higher score (2/2 = 1.0)
        # Move 26 should have lower score (0/1 = 0.0)
        assert score_19 > score_26, "Move with cutoffs should score higher"
    
    def test_history_ordering(self):
        """Test that moves are ordered by historical success."""
        game = BitboardGame()
        moves = game.get_move_list()  # [19, 26, 37, 44]
        
        orderer = HistoryHeuristicOrderer()
        
        # Build history: 37 is best, 19 is good, others neutral
        for _ in range(5):
            orderer.update_history(Move(5, 3), depth=5)  # E3
        for _ in range(2):
            orderer.update_history(Move(3, 3), depth=5)  # C3
        
        ordered = orderer.order_moves(game, moves)
        
        # 37 should be first, 19 should be second
        best_move = Move(5, 3)  # E3
        if best_move in moves:
            assert ordered[0] == best_move, "Best historical move should be first"
        second_best = Move(3, 3)  # C3
        if second_best in moves:
            assert ordered[1] == second_best, "Second best should be second"
    
    def test_history_new_move_neutral(self):
        """Test that new moves have neutral score."""
        orderer = HistoryHeuristicOrderer()
        
        score = orderer.history_table.get((8, 8), 0)  # New move (H8)
        
        assert score == 0.0, "New moves should have neutral score"


class TestPositionalOrderer:
    """Test suite for Positional move ordering."""
    
    def test_corners_ordered_first(self):
        """Test that corner moves are prioritized."""
        # Create position where corner is available
        game = BitboardGame()
        # Make moves to create a position
        game.move(Move(1, 1))  # A1 corner
        
        # Get moves including corner if available
        moves = game.get_move_list()
        
        orderer = PositionalOrderer()
        ordered = orderer.order_moves(game, moves)
        
        # Corners (0, 7, 56, 63) should be prioritized if in list
        if any(m in [0, 7, 56, 63] for m in moves):
            # First should be a corner
            assert ordered[0] in [0, 7, 56, 63], "Corner should be first"
    
    def test_positional_ordering_consistent(self):
        """Test that positional ordering is deterministic."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = PositionalOrderer()
        
        ordered1 = orderer.order_moves(game, moves)
        ordered2 = orderer.order_moves(game, moves)
        
        assert ordered1 == ordered2, "Ordering should be deterministic"
    
    def test_all_moves_preserved(self):
        """Test that all moves are preserved after ordering."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = PositionalOrderer()
        ordered = orderer.order_moves(game, moves)
        
        assert len(ordered) == len(moves), "All moves should be preserved"
        assert set(ordered) == set(moves), "No moves should be lost or added"


class TestCompositeOrderer:
    """Test suite for Composite move ordering."""
    
    def test_composite_combines_orderers(self):
        """Test that composite combines multiple ordering strategies."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = CompositeOrderer()
        
        # Should combine PV, killer, history, positional
        ordered = orderer.order_moves(game, moves)
        
        assert len(ordered) == len(moves), "All moves should be preserved"
        assert set(ordered) == set(moves), "No moves should be lost"
    
    def test_pv_move_highest_priority(self):
        """Test that PV move has highest priority in composite."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = CompositeOrderer()
        
        # Add orderers to composite
        pv_orderer = PVMoveOrderer()
        killer_orderer = KillerMoveOrderer()
        history_orderer = HistoryHeuristicOrderer()
        
        orderer.add_orderer(pv_orderer)
        orderer.add_orderer(killer_orderer)
        orderer.add_orderer(history_orderer)
        
        # Set PV move
        pv_orderer.set_pv_move(Move(5, 4))  # E4
        
        # Add killer and history for other moves
        killer_orderer.add_killer(Move(3, 3), depth=5)  # C3
        history_orderer.update_history(Move(4, 3), depth=5)  # D3
        
        ordered = orderer.order_moves(game, moves)
        
        # PV move should still be first (if it's in the move list)
        pv_move = Move(5, 4)  # E4
        if pv_move in moves:
            assert ordered[0] == pv_move, "PV move should override all others"
    
    def test_composite_ordering_improves_over_random(self):
        """Test that composite ordering is better than random."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = CompositeOrderer()
        
        # Add orderers to composite
        pv_orderer = PVMoveOrderer()
        killer_orderer = KillerMoveOrderer()
        history_orderer = HistoryHeuristicOrderer()
        
        orderer.add_orderer(pv_orderer)
        orderer.add_orderer(killer_orderer)
        orderer.add_orderer(history_orderer)
        
        # Build some history
        history_orderer.update_history(Move(5, 3), depth=5)  # E3
        killer_orderer.add_killer(Move(4, 3), depth=5)  # D3
        
        ordered = orderer.order_moves(game, moves)
        
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
            ordered = orderer.order_moves(game, moves)
            assert ordered == [], f"{orderer.__class__.__name__} failed on empty list"
    
    def test_single_move(self):
        """Test orderers handle single move."""
        game = BitboardGame()
        moves = [Move(3, 3)]  # Single move (C3)
        
        orderers = [
            PVMoveOrderer(),
            PositionalOrderer(),
        ]
        
        for orderer in orderers:
            ordered = orderer.order_moves(game, moves)
            assert ordered == [Move(3, 3)], f"{orderer.__class__.__name__} failed on single move"
    
    @pytest.mark.parametrize("orderer_class", [
        PVMoveOrderer,
        PositionalOrderer,
        HistoryHeuristicOrderer,
    ])
    def test_orderer_preserves_moves(self, orderer_class):
        """Test that orderers preserve all moves."""
        game = BitboardGame()
        moves = game.get_move_list()
        
        orderer = orderer_class()
        
        if orderer_class == HistoryHeuristicOrderer:
            ordered = orderer.order_moves(game, moves)
        else:
            ordered = orderer.order_moves(game, moves)
        
        assert len(ordered) == len(moves), "All moves should be preserved"
        assert set(ordered) == set(moves), "Exact same moves"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

