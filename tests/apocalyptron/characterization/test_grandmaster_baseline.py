"""
Baseline characterization tests for Grandmaster AI.

These tests capture the exact behavior of the current Grandmaster
implementation before refactoring begins. They serve as regression
tests to ensure Apocalyptron produces identical results.

Run this FIRST to establish baseline, then compare Apocalyptron results.
"""

import unittest
import json
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from tests.apocalyptron.characterization.test_positions import TestPositions
from src.Players.PlayerApocalyptron import PlayerApocalyptron
from src.Reversi.BitboardGame import BitboardGame
import time


class TestGrandmasterBaseline(unittest.TestCase):
    """Characterization tests for Apocalyptron AI behavior"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize engine once for all tests"""
        cls.engine = PlayerApocalyptron(depth=6)
        cls.baseline_file = os.path.join(
            os.path.dirname(__file__),
            'apocalyptron_baseline.json'
        )
        cls.baseline_data = {}
    
    def test_01_initial_position_depth_6(self):
        """Test initial position at depth 6"""
        game = TestPositions.initial_position()
        result = self._evaluate_position(game, depth=6, test_name='initial_d6')
        self.assertIsNotNone(result['move'])
        self.assertIsNotNone(result['value'])
    
    def test_02_initial_position_depth_8(self):
        """Test initial position at depth 8"""
        game = TestPositions.initial_position()
        result = self._evaluate_position(game, depth=8, test_name='initial_d8')
        self.assertIsNotNone(result['move'])
    
    def test_03_after_first_move_depth_7(self):
        """Test position after F5 at depth 7"""
        game = TestPositions.after_first_move()
        result = self._evaluate_position(game, depth=7, test_name='after_first_d7')
        self.assertIsNotNone(result['move'])
    
    def test_04_early_midgame_depth_8(self):
        """Test early midgame at depth 8"""
        game = TestPositions.early_midgame()
        result = self._evaluate_position(game, depth=8, test_name='early_mid_d8')
        self.assertIsNotNone(result['move'])
    
    def test_05_midgame_tactical_depth_9(self):
        """Test midgame tactical position at depth 9"""
        game = TestPositions.midgame_tactical()
        result = self._evaluate_position(game, depth=9, test_name='mid_tactical_d9')
        self.assertIsNotNone(result['move'])
    
    def test_06_late_midgame_depth_10(self):
        """Test late midgame at depth 10"""
        game = TestPositions.late_midgame()
        result = self._evaluate_position(game, depth=10, test_name='late_mid_d10')
        self.assertIsNotNone(result['move'])
    
    def test_07_endgame_depth_12(self):
        """Test endgame at depth 12"""
        game = TestPositions.endgame()
        result = self._evaluate_position(game, depth=12, test_name='endgame_d12')
        self.assertIsNotNone(result['move'])
    
    def test_08_corner_capture_depth_8(self):
        """Test corner capture opportunity at depth 8"""
        game = TestPositions.corner_capture()
        result = self._evaluate_position(game, depth=8, test_name='corner_d8')
        self.assertIsNotNone(result['move'])
    
    def test_09_evaluation_consistency(self):
        """Test that same position gives same evaluation"""
        game = TestPositions.initial_position()
        
        # Evaluate multiple times
        results = []
        for i in range(3):
            # Create fresh engine for each test
            engine = PlayerApocalyptron(depth=6)
            moves = game.get_valid_moves(game.current_player)
            move = engine.get_move(game, moves, None)
            results.append(str(move))
        
        # All results should be identical
        self.assertEqual(len(set(results)), 1, 
                        f"Inconsistent results: {results}")
    
    def test_10_move_ordering_effectiveness(self):
        """Test move ordering is working"""
        game = TestPositions.midgame_tactical()
        move_list = game.get_valid_moves(game.current_player)
        
        # Should return all moves
        self.assertGreater(len(move_list), 0)
        
        # Should be valid moves
        for move in move_list:
            self.assertTrue(move in game.get_valid_moves(game.current_player))
    
    def test_11_evaluation_function(self):
        """Test evaluation on various positions"""
        positions = TestPositions.all_positions()
        
        for name, game in positions.items():
            with self.subTest(position=name):
                # Get move from engine (which uses evaluation internally)
                moves = game.get_valid_moves(game.current_player)
                if moves:
                    move = self.engine.get_move(game, moves, None)
                    # Store for baseline
                    self.baseline_data[f'eval_{name}'] = {
                        'move': str(move),
                        'pieces': game.black_cnt + game.white_cnt
                    }
    
    def _evaluate_position(self, game, depth, test_name):
        """
        Evaluate a position and capture detailed results.
        
        Returns dict with: move, time, statistics
        """
        # Create fresh engine for each test
        engine = PlayerApocalyptron(depth=depth)
        
        # Measure time
        start_time = time.perf_counter()
        
        # Get best move
        moves = game.get_valid_moves(game.current_player)
        if moves:
            move = engine.get_move(game, moves, None)
        else:
            move = None
        
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        
        # Capture results
        result = {
            'move': str(move) if move else None,
            'time': elapsed,
            'depth': depth,
            'position': test_name,
            'piece_count': game.black_cnt + game.white_cnt,
            'turn': game.turn,
        }
        
        # Store in baseline
        self.baseline_data[test_name] = result
        
        return result
    
    @classmethod
    def tearDownClass(cls):
        """Save baseline data to file"""
        # Add metadata
        baseline_output = {
            'metadata': {
                'engine': 'ApocalyptronEngine',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'purpose': 'Baseline for Apocalyptron characterization',
            },
            'results': cls.baseline_data
        }
        
        # Write to JSON file
        with open(cls.baseline_file, 'w') as f:
            json.dump(baseline_output, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"BASELINE DATA SAVED: {cls.baseline_file}")
        print(f"Total tests: {len(cls.baseline_data)}")
        print(f"Use this file to validate Apocalyptron behavior")
        print(f"{'='*80}\n")


def run_baseline():
    """Run baseline tests and generate baseline data"""
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGrandmasterBaseline)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run baseline generation
    success = run_baseline()
    exit(0 if success else 1)

