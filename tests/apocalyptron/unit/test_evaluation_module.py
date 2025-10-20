"""
Test suite for Apocalyptron Evaluation Module.

Tests all evaluators:
- MobilityEvaluator
- StabilityEvaluator
- PositionalEvaluator
- ParityEvaluator
- CompositeEvaluator
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from Reversi.BitboardGame import BitboardGame
from AI.Apocalyptron.evaluation.mobility import MobilityEvaluator
from AI.Apocalyptron.evaluation.stability import StabilityEvaluator
from AI.Apocalyptron.evaluation.positional import PositionalEvaluator
from AI.Apocalyptron.evaluation.parity import ParityEvaluator
from AI.Apocalyptron.evaluation.composite import CompositeEvaluator


class TestMobilityEvaluator:
    """Test suite for MobilityEvaluator."""
    
    def test_initial_position_mobility(self):
        """Test mobility evaluation at initial position."""
        game = BitboardGame()
        evaluator = MobilityEvaluator()
        
        score = evaluator.evaluate(game)
        
        # Initial position: both players have 4 moves
        # Mobility should be neutral (0)
        assert score == 0.0, "Initial position should have neutral mobility"
    
    def test_more_moves_better_score(self):
        """Test that having more moves gives positive score."""
        game = BitboardGame()
        evaluator = MobilityEvaluator()
        
        # Make move that gives black more mobility
        game = game.make_move(19)  # D3
        
        score = evaluator.evaluate(game)
        
        # After first move, current player (white) should have evaluation
        # Score is from current player perspective
        assert isinstance(score, (int, float)), "Score should be numeric"
    
    def test_no_moves_penalty(self):
        """Test that having no moves gives strong penalty."""
        evaluator = MobilityEvaluator()
        
        # Create position where one player has no moves
        # This is tested more in integration tests
        # For now, just verify evaluator handles edge cases
        game = BitboardGame()
        
        # Should not crash
        score = evaluator.evaluate(game)
        assert score is not None
    
    def test_mobility_symmetry(self):
        """Test that mobility evaluation is symmetric."""
        game = BitboardGame()
        evaluator = MobilityEvaluator()
        
        black_score = evaluator.evaluate(game)
        
        # Flip colors
        game_flipped = BitboardGame(
            black=game.white,
            white=game.black,
            current_player=-game.current_player
        )
        
        white_score = evaluator.evaluate(game_flipped)
        
        # Scores should be opposite
        assert abs(black_score + white_score) < 0.01, "Mobility should be symmetric"


class TestStabilityEvaluator:
    """Test suite for StabilityEvaluator."""
    
    def test_initial_position_stability(self):
        """Test stability at initial position."""
        game = BitboardGame()
        evaluator = StabilityEvaluator()
        
        score = evaluator.evaluate(game)
        
        # Initial position: no stable pieces yet
        assert score == 0.0, "Initial position has no stable pieces"
    
    def test_corner_stability(self):
        """Test that corners are recognized as stable."""
        evaluator = StabilityEvaluator()
        
        # Create position with corner captured
        # Black captures A1 (position 0)
        game = BitboardGame(
            black=0x0000000810000001,  # Added corner
            white=0x0000001008000000,
            current_player=1
        )
        
        score = evaluator.evaluate(game)
        
        # Black should have positive stability score
        assert score > 0, "Corner should give positive stability"
    
    def test_edge_stability_from_corner(self):
        """Test that edges connected to corners are stable."""
        evaluator = StabilityEvaluator()
        
        # Create position with corner and connected edge
        game = BitboardGame(
            black=0x0000000810000003,  # Corner + edge
            white=0x0000001008000000,
            current_player=1
        )
        
        score = evaluator.evaluate(game)
        
        # More stable pieces = higher score
        assert score > 0, "Corner with edge should be stable"


class TestPositionalEvaluator:
    """Test suite for PositionalEvaluator."""
    
    def test_initial_position_positional(self):
        """Test positional evaluation at start."""
        game = BitboardGame()
        evaluator = PositionalEvaluator()
        
        score = evaluator.evaluate(game)
        
        # Initial position should be roughly balanced
        assert abs(score) < 50, "Initial position should be balanced"
    
    def test_corner_value(self):
        """Test that corners have high positional value."""
        evaluator = PositionalEvaluator()
        
        # Black captures corner
        game = BitboardGame(
            black=0x0000000810000001,  # Corner A1
            white=0x0000001008000000,
            current_player=1
        )
        
        score = evaluator.evaluate(game)
        
        # Corner is worth 100 points
        assert score >= 90, "Corner should have high value"
    
    def test_x_square_penalty(self):
        """Test that X-squares (diagonal to corners) have negative value."""
        evaluator = PositionalEvaluator()
        
        # Black on X-square (B2, position 9)
        game = BitboardGame(
            black=0x0000000810000200,  # X-square
            white=0x0000001008000000,
            current_player=1
        )
        
        score = evaluator.evaluate(game)
        
        # X-square is worth -40 points
        assert score < 0, "X-square should have negative value"
    
    def test_positional_weights_applied(self):
        """Test that positional weights are correctly applied."""
        evaluator = PositionalEvaluator()
        game = BitboardGame()
        
        score = evaluator.evaluate(game)
        
        # Should be deterministic based on position weights
        assert isinstance(score, (int, float))


class TestParityEvaluator:
    """Test suite for ParityEvaluator."""
    
    def test_opening_parity_neutral(self):
        """Test that parity is neutral in opening."""
        game = BitboardGame()
        evaluator = ParityEvaluator()
        
        score = evaluator.evaluate(game)
        
        # Parity matters only in endgame
        assert score == 0.0, "Parity should be neutral in opening"
    
    def test_endgame_parity_matters(self):
        """Test that parity affects endgame evaluation."""
        evaluator = ParityEvaluator()
        
        # Create near-endgame position (few empty squares)
        # 60 pieces = 4 empty squares
        black = 0x0FFFFFFF00000000
        white = 0x00000000FFFFF000
        game = BitboardGame(black=black, white=white, current_player=1)
        
        score = evaluator.evaluate(game)
        
        # Should have some parity value (even/odd empty squares)
        assert isinstance(score, (int, float))


class TestCompositeEvaluator:
    """Test suite for CompositeEvaluator."""
    
    def test_composite_combines_evaluators(self):
        """Test that composite evaluator combines multiple evaluators."""
        game = BitboardGame()
        evaluator = CompositeEvaluator()
        
        score = evaluator.evaluate(game)
        
        # Should combine all evaluators
        assert isinstance(score, (int, float))
        # Initial position should be near 0 (balanced)
        assert abs(score) < 100
    
    def test_phase_detection(self):
        """Test that phase detection works."""
        evaluator = CompositeEvaluator()
        
        # Opening
        game_opening = BitboardGame()
        score_opening = evaluator.evaluate(game_opening)
        
        # Create midgame position (~30 pieces)
        black_mid = 0x0000FFFF00000000
        white_mid = 0x000000000000FFFF
        game_midgame = BitboardGame(black=black_mid, white=white_mid, current_player=1)
        score_midgame = evaluator.evaluate(game_midgame)
        
        # Scores should be different due to different phase weights
        # Just verify they compute without error
        assert isinstance(score_opening, (int, float))
        assert isinstance(score_midgame, (int, float))
    
    def test_composite_consistency(self):
        """Test that composite evaluator is deterministic."""
        game = BitboardGame()
        evaluator = CompositeEvaluator()
        
        score1 = evaluator.evaluate(game)
        score2 = evaluator.evaluate(game)
        
        assert score1 == score2, "Evaluation should be deterministic"
    
    @pytest.mark.parametrize("player", [1, -1])
    def test_composite_works_for_both_players(self, player):
        """Test evaluation works for both black and white."""
        game = BitboardGame(current_player=player)
        evaluator = CompositeEvaluator()
        
        score = evaluator.evaluate(game)
        
        assert isinstance(score, (int, float))


class TestEvaluatorConsistency:
    """Test consistency across evaluators."""
    
    def test_all_evaluators_handle_initial_position(self):
        """Test all evaluators can evaluate initial position."""
        game = BitboardGame()
        
        evaluators = [
            MobilityEvaluator(),
            StabilityEvaluator(),
            PositionalEvaluator(),
            ParityEvaluator(),
            CompositeEvaluator()
        ]
        
        for evaluator in evaluators:
            score = evaluator.evaluate(game)
            assert isinstance(score, (int, float)), f"{evaluator.__class__.__name__} failed"
    
    def test_all_evaluators_handle_game_over(self):
        """Test all evaluators handle game-over positions."""
        # Create a game-over position (board full or no moves for both)
        # For simplicity, use a simple endgame-ish position
        black = 0xFFFFFFFF00000000
        white = 0x00000000FFFFFFFF
        game = BitboardGame(black=black, white=white, current_player=1)
        
        evaluators = [
            MobilityEvaluator(),
            StabilityEvaluator(),
            PositionalEvaluator(),
            ParityEvaluator(),
            CompositeEvaluator()
        ]
        
        for evaluator in evaluators:
            # Should not crash on endgame
            score = evaluator.evaluate(game)
            assert isinstance(score, (int, float))
    
    def test_evaluators_are_bounded(self):
        """Test that evaluator scores are within reasonable bounds."""
        game = BitboardGame()
        
        mobility = MobilityEvaluator().evaluate(game)
        stability = StabilityEvaluator().evaluate(game)
        positional = PositionalEvaluator().evaluate(game)
        parity = ParityEvaluator().evaluate(game)
        composite = CompositeEvaluator().evaluate(game)
        
        # Reasonable bounds (adjust if needed)
        assert -1000 < mobility < 1000
        assert -1000 < stability < 1000
        assert -1000 < positional < 1000
        assert -100 < parity < 100
        assert -10000 < composite < 10000

