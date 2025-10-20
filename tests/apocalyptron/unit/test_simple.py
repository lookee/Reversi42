"""
Simple test to verify the test infrastructure works.
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from Reversi.BitboardGame import BitboardGame
from Players.PlayerApocalyptron import PlayerApocalyptron


def test_bitboard_game_creation():
    """Test that BitboardGame can be created."""
    game = BitboardGame()
    assert game is not None
    assert hasattr(game, 'get_valid_moves')


def test_apocalyptron_player_creation():
    """Test that PlayerApocalyptron can be created."""
    player = PlayerApocalyptron(depth=4)
    assert player is not None
    assert hasattr(player, 'get_move')


def test_apocalyptron_makes_move():
    """Test that Apocalyptron can make a move."""
    game = BitboardGame()
    player = PlayerApocalyptron(depth=4)
    
    moves = game.get_move_list()
    assert len(moves) > 0
    
    move = player.get_move(game, moves, None)
    assert move is not None
    assert move in moves


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
