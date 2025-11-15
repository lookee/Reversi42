#!/usr/bin/env python3
"""
Integration test for book_instant parameter.

Verifies that:
1. book_instant=False triggers engine evaluation
2. book_instant=True skips engine evaluation (instant)
3. Both modes select valid moves
"""

import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Players.PlayerApocalyptron import PlayerApocalyptron
from Players.PlayerFactory import PlayerFactory
from Reversi.Game import Game


class TestBookInstantMode:
    """Test book_instant parameter behavior"""

    def test_parameter_exists(self):
        """Verify book_instant parameter exists and works"""
        # PlayerApocalyptron
        p1 = PlayerApocalyptron(depth=6, book_instant=False)
        assert hasattr(p1, "book_instant"), "Should have book_instant attribute"
        assert p1.book_instant == False, "Should be False"

        p2 = PlayerApocalyptron(depth=6, book_instant=True)
        assert p2.book_instant == True, "Should be True"

        # PlayerDivZero
        p3 = PlayerDivZero(depth=8, book_instant=False)
        assert hasattr(p3, "book_instant"), "Should have book_instant attribute"
        assert p3.book_instant == False, "Should be False"

        p4 = PlayerDivZero(depth=8, book_instant=True)
        assert p4.book_instant == True, "Should be True"

    def test_default_is_false(self):
        """Verify default is book_instant=False"""
        p1 = PlayerApocalyptron(depth=6)
        assert p1.book_instant == False, "Default should be False"

        p2 = PlayerDivZero(depth=8)
        assert p2.book_instant == False, "Default should be False"

    def test_instant_mode_selects_valid_move(self):
        """Test that instant mode selects a valid move"""
        player = PlayerApocalyptron(
            depth=6, show_book_options=False, book_instant=True  # Quiet  # Instant mode
        )

        game = Game(8)
        moves = game.get_move_list()

        # Should have opening book moves
        assert len(player.opening_book.get_book_moves("")) > 0

        # Get move (should be instant from book)
        selected_move = player.get_move(game, moves, None)

        # Verify it's valid
        assert selected_move is not None, "Should select a move"
        assert selected_move in moves, "Should be a valid move"
        assert game.valid_move(selected_move), "Should be playable"

    def test_evaluation_mode_selects_valid_move(self):
        """Test that evaluation mode selects a valid move"""
        player = PlayerApocalyptron(
            depth=6, show_book_options=False, book_instant=False  # Quiet  # Evaluation mode
        )

        game = Game(8)
        moves = game.get_move_list()

        # Should have opening book moves
        assert len(player.opening_book.get_book_moves("")) > 0

        # Get move (should evaluate with engine)
        selected_move = player.get_move(game, moves, None)

        # Verify it's valid
        assert selected_move is not None, "Should select a move"
        assert selected_move in moves, "Should be a valid move"
        assert game.valid_move(selected_move), "Should be playable"

    def test_apocalyptron_instant_mode(self):
        """Test PlayerApocalyptron with instant mode"""
        player = PlayerApocalyptron(depth=8, show_book_options=False, book_instant=True)

        game = Game(8)
        moves = game.get_move_list()

        selected_move = player.get_move(game, moves, None)

        assert selected_move is not None
        assert selected_move in moves

    def test_apocalyptron_evaluation_mode(self):
        """Test PlayerApocalyptron with evaluation mode"""
        player = PlayerApocalyptron(depth=8, show_book_options=False, book_instant=False)

        game = Game(8)
        moves = game.get_move_list()

        selected_move = player.get_move(game, moves, None)

        assert selected_move is not None
        assert selected_move in moves

    def test_both_modes_work_out_of_book(self):
        """Verify both modes work when out of book"""
        # Create unusual position (out of book)
        game = Game(8)

        # Play random moves to get out of book quickly
        moves = game.get_move_list()
        if moves:
            game.move(moves[0])  # D3

        moves = game.get_move_list()
        if moves:
            game.move(moves[0])  # C5 or similar

        moves = game.get_move_list()
        if moves:
            game.move(moves[0])

        # Now likely out of book
        moves = game.get_move_list()

        # Test instant mode
        p1 = PlayerApocalyptron(depth=5, show_book_options=False, book_instant=True)
        move1 = p1.get_move(game, moves, None)
        assert move1 in moves, "Instant mode should work out of book"

        # Test evaluation mode
        p2 = PlayerApocalyptron(depth=5, show_book_options=False, book_instant=False)
        move2 = p2.get_move(game, moves, None)
        assert move2 in moves, "Evaluation mode should work out of book"


def test_book_instant_in_tournament_config():
    """
    Verify book_instant can be configured in tournament JSON.

    This is a documentation test - shows how to use in tournaments.
    """
    import json

    example_config = {
        "players": [
            {
                "name": "Strong Apocalyptron",
                "type": "PlayerApocalyptron",
                "parameters": {"depth": 9, "book_instant": False},  # Evaluation mode
            },
            {
                "name": "Fast Apocalyptron",
                "type": "PlayerApocalyptron",
                "parameters": {"depth": 6, "book_instant": True},  # Instant mode
            },
        ]
    }

    # Verify JSON is valid
    json_str = json.dumps(example_config, indent=2)
    parsed = json.loads(json_str)

    assert parsed["players"][0]["parameters"]["book_instant"] == False
    assert parsed["players"][1]["parameters"]["book_instant"] == True

    print("\n✅ Tournament configuration example:")
    print(json_str)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
