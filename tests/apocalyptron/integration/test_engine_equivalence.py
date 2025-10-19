"""
Test equivalenza ApocalyptronEngine vs GrandmasterEngine.

Verifica che ApocalyptronEngine produca ESATTAMENTE gli stessi risultati
di GrandmasterEngine (zero regressioni).
"""

import unittest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from AI.Apocalyptron import ApocalyptronEngine, ApocalyptronFactory, ApocalyptronConfigBuilder
from AI.GrandmasterEngine import GrandmasterEngine
from AI.GrandmasterWeights import GrandmasterWeights
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


class TestEngineEquivalence(unittest.TestCase):
    """
    Test che ApocalyptronEngine produca risultati identici a GrandmasterEngine.
    
    Questo garantisce zero regressioni.
    """
    
    def setUp(self):
        """Setup engines for each test"""
        # Create GrandmasterEngine
        self.grandmaster = GrandmasterEngine(weights=GrandmasterWeights())
        
        # Create ApocalyptronEngine
        self.apocalyptron = ApocalyptronFactory.create_default(depth=6)
    
    def test_01_engine_creation(self):
        """Test that engine can be created"""
        self.assertIsNotNone(self.apocalyptron)
        self.assertIsNotNone(self.grandmaster)
    
    def test_02_evaluation_equivalence(self):
        """Test that evaluation gives same results"""
        game = BitboardGame()
        
        # Evaluate with both engines
        gm_eval = self.grandmaster.evaluate_advanced(game)
        ap_eval = self.apocalyptron.evaluate(game)
        
        # Should be identical
        self.assertEqual(gm_eval, ap_eval, 
                        f"Evaluation mismatch: GM={gm_eval}, AP={ap_eval}")
    
    def test_03_initial_position_move(self):
        """Test move selection from initial position"""
        game = BitboardGame()
        
        # Get moves from both engines (suppress output)
        gm_move = self.grandmaster.get_best_move(game, depth=6, player_name=None)
        ap_move = self.apocalyptron.get_best_move(game, depth=6, player_name=None)
        
        # Should be identical
        self.assertEqual(gm_move, ap_move,
                        f"Move mismatch: GM={gm_move}, AP={ap_move}")
    
    def test_04_midgame_position_move(self):
        """Test move selection from midgame"""
        game = BitboardGame()
        
        # Play some moves
        sequence = [
            Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6),
            Move(6, 6), Move(6, 4), Move(7, 5),
        ]
        for move in sequence:
            if game.valid_move(move):
                game.move(move)
        
        # Get moves from both engines
        gm_move = self.grandmaster.get_best_move(game.copy(), depth=6, player_name=None)
        ap_move = self.apocalyptron.get_best_move(game.copy(), depth=6, player_name=None)
        
        # Should be identical
        self.assertEqual(gm_move, ap_move,
                        f"Midgame move mismatch: GM={gm_move}, AP={ap_move}")
    
    def test_05_multiple_depths(self):
        """Test equivalence at different depths"""
        game = BitboardGame()
        
        for depth in [4, 6, 8]:
            with self.subTest(depth=depth):
                # Reset engines
                self.grandmaster.transposition_table.clear()
                self.apocalyptron.reset()
                
                gm_move = self.grandmaster.get_best_move(game.copy(), depth=depth, player_name=None)
                ap_move = self.apocalyptron.get_best_move(game.copy(), depth=depth, player_name=None)
                
                self.assertEqual(gm_move, ap_move,
                                f"Depth {depth} mismatch: GM={gm_move}, AP={ap_move}")
    
    def test_06_factory_variants(self):
        """Test that factory variants work correctly"""
        game = BitboardGame()
        
        # Test different factory methods
        engines = {
            'default': ApocalyptronFactory.create_default(depth=6),
            'aggressive': ApocalyptronFactory.create_aggressive(depth=6),
            'defensive': ApocalyptronFactory.create_defensive(depth=6),
        }
        
        for name, engine in engines.items():
            with self.subTest(variant=name):
                move = engine.get_best_move(game.copy(), depth=6, player_name=None)
                self.assertIsNotNone(move, f"{name} variant failed to return move")
    
    def test_07_config_builder(self):
        """Test that config builder works"""
        config = (ApocalyptronConfigBuilder()
            .with_depth(6)
            .enable_all_optimizations()
            .quiet_mode()
            .build())
        
        self.assertEqual(config.depth, 6)
        self.assertTrue(config.enable_null_move_pruning)
        self.assertFalse(config.show_search_output)
        
        # Create engine with config
        engine = ApocalyptronFactory.create_engine(config)
        self.assertIsNotNone(engine)
        
        # Test it can find moves
        game = BitboardGame()
        move = engine.get_best_move(game, depth=6)
        self.assertIsNotNone(move)
    
    def test_08_statistics(self):
        """Test that statistics are collected"""
        game = BitboardGame()
        
        move = self.apocalyptron.get_best_move(game, depth=6)
        stats = self.apocalyptron.get_statistics()
        
        self.assertIn('engine', stats)
        self.assertIn('searches_performed', stats)
        self.assertGreater(stats['searches_performed'], 0)


def run_tests():
    """Run equivalence tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEngineEquivalence)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    print("\n" + "="*80)
    print("TEST DI EQUIVALENZA: ApocalyptronEngine vs GrandmasterEngine")
    print("="*80)
    print("Verifica ZERO REGRESSIONI - i risultati devono essere identici\n")
    
    success = run_tests()
    
    print("\n" + "="*80)
    if success:
        print("✅ TUTTI I TEST PASSATI - ZERO REGRESSIONI!")
    else:
        print("❌ ALCUNI TEST FALLITI - VERIFICARE!")
    print("="*80 + "\n")
    
    exit(0 if success else 1)

