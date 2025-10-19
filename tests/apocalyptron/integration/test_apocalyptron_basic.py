"""
Basic integration tests for Apocalyptron.

Verifies that Apocalyptron works correctly and produces moves.
"""

import unittest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from Players.PlayerApocalyptron import PlayerApocalyptron
from Players.AIPlayerGrandmaster import AIPlayerGrandmaster
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


class TestApocalyptronBasic(unittest.TestCase):
    """Basic tests for Apocalyptron AI"""
    
    def test_01_creation(self):
        """Test that Apocalyptron can be created"""
        player = PlayerApocalyptron(depth=6)
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Apocalyptron6")
    
    def test_02_initial_move(self):
        """Test that Apocalyptron can make a move from initial position"""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=6, show_book_options=False)
        
        moves = game.get_move_list()
        move = player.get_move(game, moves, None)
        
        self.assertIsNotNone(move)
        self.assertIn(move, moves)
    
    def test_03_midgame_move(self):
        """Test move selection in midgame"""
        game = BitboardGame()
        
        # Play some moves to reach midgame
        sequence = [
            Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6),
            Move(6, 6), Move(6, 4), Move(7, 5),
        ]
        for move in sequence:
            if game.valid_move(move):
                game.move(move)
        
        player = PlayerApocalyptron(depth=6, show_book_options=False)
        moves = game.get_move_list()
        move = player.get_move(game, moves, None)
        
        self.assertIsNotNone(move)
        self.assertIn(move, moves)
    
    def test_04_equivalence_to_grandmaster(self):
        """
        Test that Apocalyptron produces same moves as Grandmaster.
        
        Since Apocalyptron currently wraps Grandmaster, they should
        produce identical results.
        """
        game = BitboardGame()
        
        # Create both players with same depth
        apocalyptron = PlayerApocalyptron(depth=6, show_book_options=False)
        grandmaster = AIPlayerGrandmaster(deep=6, show_book_options=False)
        
        moves = game.get_move_list()
        
        # Get moves from both
        apoc_move = apocalyptron.get_move(game.copy(), moves, None)
        grand_move = grandmaster.get_move(game.copy(), moves, None)
        
        # Should be identical
        self.assertEqual(apoc_move, grand_move, 
                        f"Apocalyptron and Grandmaster should produce same move")
    
    def test_05_factory_creation(self):
        """Test that Apocalyptron can be created via factory"""
        from Players.PlayerFactory import PlayerFactory
        
        player = PlayerFactory.create_apocalyptron(depth=6)
        self.assertIsNotNone(player)
        self.assertIsInstance(player, PlayerApocalyptron)
    
    def test_06_metadata(self):
        """Test that metadata is correctly defined"""
        metadata = PlayerApocalyptron.get_metadata()
        
        self.assertEqual(metadata['display_name'], 'Apocalyptron')
        self.assertTrue(metadata['enabled'])
        self.assertIn('difficulty', metadata['parameters'])
    
    def test_07_statistics(self):
        """Test that statistics are collected"""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=6, show_book_options=False)
        
        moves = game.get_move_list()
        move = player.get_move(game, moves, None)
        
        stats = player.get_statistics()
        self.assertIsNotNone(stats)
        self.assertIn("APOCALYPTRON", stats)


def run_tests():
    """Run all Apocalyptron tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApocalyptronBasic)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)

