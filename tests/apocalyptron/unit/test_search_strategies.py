"""
Test suite for Search Strategies (new refactoring).

Tests FixedDepthStrategy, IterativeDeepeningStrategy, and AdaptiveDepthStrategy.
"""

import os
import sys
import time

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from AI.Apocalyptron.evaluation import CompositeEvaluator, MobilityEvaluator
from AI.Apocalyptron.ordering import CompositeOrderer, PositionalOrderer
from AI.Apocalyptron.search import (
    AdaptiveDepthStrategy,
    AlphaBetaSearchComplete,
    FixedDepthStrategy,
    IterativeDeepeningStrategy,
)
from AI.Apocalyptron.weights import EvaluationWeights
from Reversi.BitboardGame import BitboardGame


class TestFixedDepthStrategy:
    """Test suite for FixedDepthStrategy."""

    def test_fixed_depth_initialization(self):
        """Test that FixedDepthStrategy initializes correctly"""
        game = BitboardGame()

        # Create components
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)

        # Create strategy
        strategy = FixedDepthStrategy(alphabeta)

        assert strategy is not None
        assert strategy.alphabeta == alphabeta

    def test_fixed_depth_returns_valid_move(self):
        """Test that FixedDepthStrategy returns valid move"""
        game = BitboardGame()

        # Create components
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        strategy = FixedDepthStrategy(alphabeta)

        # Get move
        moves = game.get_move_list()
        move = strategy.get_best_move(game, depth=4)

        assert move is not None
        assert move in moves

    def test_fixed_depth_reset(self):
        """Test that FixedDepthStrategy reset works"""
        game = BitboardGame()

        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        strategy = FixedDepthStrategy(alphabeta)

        # Search once
        strategy.get_best_move(game, depth=4)

        # Reset
        strategy.reset()

        # Should work fine after reset
        move = strategy.get_best_move(game, depth=4)
        assert move is not None


class TestIterativeDeepeningStrategy:
    """Test suite for IterativeDeepeningStrategy."""

    def test_iterative_deepening_initialization(self):
        """Test that IterativeDeepeningStrategy initializes correctly"""
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)

        # Create strategy
        strategy = IterativeDeepeningStrategy(alphabeta, use_aspiration=True)

        assert strategy is not None
        assert strategy.alphabeta == alphabeta

    def test_iterative_deepening_returns_valid_move(self):
        """Test that IterativeDeepeningStrategy returns valid move"""
        game = BitboardGame()

        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        strategy = IterativeDeepeningStrategy(alphabeta, use_aspiration=True)

        # Get move
        moves = game.get_move_list()
        move = strategy.get_best_move(game, depth=4)

        assert move is not None
        assert move in moves

    def test_iterative_deepening_aspiration_windows(self):
        """Test that IterativeDeepeningStrategy tracks aspiration windows"""
        game = BitboardGame()

        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        strategy = IterativeDeepeningStrategy(alphabeta, use_aspiration=True)

        # Search
        strategy.get_best_move(game, depth=5)

        # Should have aspiration statistics
        assert hasattr(strategy, "aspiration_hits")
        assert hasattr(strategy, "aspiration_fails")


class TestAdaptiveDepthStrategy:
    """Test suite for AdaptiveDepthStrategy."""

    def test_adaptive_depth_initialization(self):
        """Test that AdaptiveDepthStrategy initializes correctly"""
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)

        # Create strategy
        depth_config = {"opening": 6, "midgame": 8, "endgame": 10}
        strategy = AdaptiveDepthStrategy(alphabeta, depth_config)

        assert strategy is not None
        assert strategy.alphabeta == alphabeta
        assert strategy.depth_config == depth_config

    def test_adaptive_depth_phase_detection(self):
        """Test that AdaptiveDepthStrategy detects game phases correctly"""
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        depth_config = {"opening": 6, "midgame": 8, "endgame": 10}
        strategy = AdaptiveDepthStrategy(alphabeta, depth_config)

        # Opening position (4 pieces)
        opening_game = BitboardGame()
        phase = strategy.get_current_phase(opening_game)
        assert phase == "opening"

        # Midgame position (create with ~30 pieces)
        midgame = BitboardGame.create_empty()
        midgame.black = 0x0000FFFF00000000
        midgame.white = 0x000000000000FFFF
        midgame.current_player = 1
        midgame.black_cnt = midgame._count_bits(midgame.black)
        midgame.white_cnt = midgame._count_bits(midgame.white)
        phase = strategy.get_current_phase(midgame)
        assert phase == "midgame"

        # Endgame position (create with ~56 pieces)
        endgame = BitboardGame.create_empty()
        endgame.black = 0xFFFFFFFF00000000
        endgame.white = 0x00000000FFFFFFF0
        endgame.current_player = 1
        endgame.black_cnt = endgame._count_bits(endgame.black)
        endgame.white_cnt = endgame._count_bits(endgame.white)
        phase = strategy.get_current_phase(endgame)
        assert phase == "endgame"

    def test_adaptive_depth_returns_valid_move(self):
        """Test that AdaptiveDepthStrategy returns valid move"""
        game = BitboardGame()

        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        depth_config = {"opening": 4, "midgame": 6, "endgame": 8}
        strategy = AdaptiveDepthStrategy(alphabeta, depth_config)

        # Get move
        moves = game.get_move_list()
        move = strategy.get_best_move(game, depth=6)  # Base depth (ignored)

        assert move is not None
        assert move in moves

    def test_adaptive_depth_requires_all_phases(self):
        """Test that AdaptiveDepthStrategy requires all phase configurations"""
        evaluator = CompositeEvaluator()
        evaluator.add_evaluator(MobilityEvaluator(EvaluationWeights()), weight=1.0)

        orderer = CompositeOrderer()
        orderer.add_orderer(PositionalOrderer(EvaluationWeights()))

        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)

        # Missing 'endgame'
        incomplete_config = {"opening": 6, "midgame": 8}

        with pytest.raises(ValueError):
            AdaptiveDepthStrategy(alphabeta, incomplete_config)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
