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
from AI.GrandmasterEngine import GrandmasterEngine
from AI.GrandmasterWeights import GrandmasterWeights
import time


class TestGrandmasterBaseline(unittest.TestCase):
    """Characterization tests for Grandmaster AI behavior"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize engine once for all tests"""
        cls.engine = GrandmasterEngine(weights=GrandmasterWeights())
        cls.baseline_file = os.path.join(
            os.path.dirname(__file__),
            'grandmaster_baseline.json'
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
            # Reset engine state
            self.engine.transposition_table.clear()
            self.engine.killer_moves.clear()
            self.engine.history_table.clear()
            
            move = self.engine.get_best_move(game, depth=6, player_name=f"Test{i}")
            results.append(str(move))
        
        # All results should be identical
        self.assertEqual(len(set(results)), 1, 
                        f"Inconsistent results: {results}")
    
    def test_10_move_ordering_effectiveness(self):
        """Test move ordering is working"""
        game = TestPositions.midgame_tactical()
        move_list = game.get_move_list()
        
        # Order moves
        ordered = self.engine.order_moves(game, move_list)
        
        # Should return all moves
        self.assertEqual(len(ordered), len(move_list))
        
        # Should not be empty
        self.assertGreater(len(ordered), 0)
    
    def test_11_evaluation_function(self):
        """Test advanced evaluation on various positions"""
        positions = TestPositions.all_positions()
        
        for name, game in positions.items():
            with self.subTest(position=name):
                score = self.engine.evaluate_advanced(game)
                # Score should be reasonable (not infinite)
                self.assertLess(abs(score), 100000)
                # Store for baseline
                self.baseline_data[f'eval_{name}'] = {
                    'score': score,
                    'pieces': game.black_cnt + game.white_cnt
                }
    
    def _evaluate_position(self, game, depth, test_name):
        """
        Evaluate a position and capture detailed results.
        
        Returns dict with: move, value, nodes, time, statistics
        """
        # Reset engine state for clean test
        self.engine.nodes = 0
        self.engine.pruning = 0
        self.engine.transposition_table.clear()
        self.engine.killer_moves.clear()
        self.engine.history_table.clear()
        self.engine.null_move_cutoffs = 0
        self.engine.null_move_attempts = 0
        self.engine.lmr_reductions = 0
        self.engine.lmr_re_searches = 0
        self.engine.futility_pruning = 0
        self.engine.multi_cut_pruning = 0
        
        # Measure time
        start_time = time.perf_counter()
        
        # Get best move (suppress output)
        move = self.engine.get_best_move(game, depth, player_name=None)
        
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        
        # Evaluate the position to get score
        game_copy = game.copy()
        if move and game_copy.valid_move(move):
            game_copy.move(move)
            # Get value from opponent's perspective
            value = -self.engine.evaluate_advanced(game_copy)
        else:
            value = None
        
        # Capture results
        result = {
            'move': str(move) if move else None,
            'value': value,
            'nodes': self.engine.nodes,
            'pruning': self.engine.pruning,
            'time': elapsed,
            'depth': depth,
            'position': test_name,
            'statistics': {
                'null_move_cutoffs': self.engine.null_move_cutoffs,
                'null_move_attempts': self.engine.null_move_attempts,
                'lmr_reductions': self.engine.lmr_reductions,
                'lmr_re_searches': self.engine.lmr_re_searches,
                'futility_pruning': self.engine.futility_pruning,
                'multi_cut_pruning': self.engine.multi_cut_pruning,
                'history_entries': len(self.engine.history_table),
                'tt_size': len(self.engine.transposition_table),
            },
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
                'engine': 'GrandmasterEngine',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'purpose': 'Baseline for Apocalyptron refactoring',
            },
            'results': cls.baseline_data
        }
        
        # Write to JSON file
        with open(cls.baseline_file, 'w') as f:
            json.dump(baseline_output, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"BASELINE DATA SAVED: {cls.baseline_file}")
        print(f"Total tests: {len(cls.baseline_data)}")
        print(f"Use this file to validate Apocalyptron produces identical results")
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

