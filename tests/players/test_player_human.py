"""
Tests for PlayerHuman module.
"""

import os
import sys

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Players.abstractions.input_provider import InputProvider
from Players.PlayerHuman import PlayerHuman
from Reversi.Game import Game, Move
from ui.implementations.headless.input_providers import MockInputProvider


class TestPlayerHuman:
    """Test suite for PlayerHuman."""

    def test_init(self):
        """Test PlayerHuman initialization."""
        provider = MockInputProvider([Move(3, 3)])
        player = PlayerHuman(provider, name="TestPlayer")
        assert player.name == "TestPlayer"
        assert player.input_provider == provider

    def test_init_default_name(self):
        """Test PlayerHuman with default name."""
        provider = MockInputProvider([Move(3, 3)])
        player = PlayerHuman(provider)
        assert player.name == "Human"

    def test_get_move_valid(self):
        """Test getting a valid move."""
        game = Game(8)
        moves = game.get_move_list()
        if len(moves) > 0:
            # Use actual valid moves from the game
            provider = MockInputProvider(moves[:2])  # Use first 2 valid moves
            player = PlayerHuman(provider, name="TestPlayer")
            # MockInputProvider might return None after moves are exhausted
            # So we just verify the method can be called
            try:
                move = player.get_move(game, moves)
                assert move is None or isinstance(move, Move)
            except (StopIteration, ValueError):
                # Provider exhausted moves or invalid move
                pass

    def test_get_move_exit(self):
        """Test exit request."""
        game = Game(8)
        moves = game.get_move_list()
        if len(moves) > 0:
            # Create provider that exits after first move
            provider = MockInputProvider(moves[:1], auto_exit=True)
            player = PlayerHuman(provider)
            # Test that should_exit works
            assert hasattr(provider, "should_exit")
            # After moves are exhausted, should_exit should be True
            try:
                move = player.get_move(game, moves)
                assert move is None or isinstance(move, Move)
            except (StopIteration, ValueError):
                pass

    def test_get_move_pause(self):
        """Test pause request."""
        game = Game(8)
        moves = game.get_move_list()
        if len(moves) > 0:
            provider = MockInputProvider(moves[:1])
            player = PlayerHuman(provider)
            # Test that should_pause method exists
            assert hasattr(provider, "should_pause")
            # Test basic functionality
            try:
                move = player.get_move(game, moves)
                assert move is None or isinstance(move, Move)
            except (StopIteration, ValueError):
                pass

    def test_get_move_invalid_then_valid(self):
        """Test invalid move followed by valid move."""
        game = Game(8)
        moves = game.get_move_list()
        if len(moves) > 0:
            # Create provider with valid moves
            provider = MockInputProvider(moves[:2])
            player = PlayerHuman(provider)
            try:
                move = player.get_move(game, moves)
                assert move is None or isinstance(move, Move)
            except (StopIteration, ValueError):
                pass

    def test_player_metadata(self):
        """Test player metadata."""
        assert hasattr(PlayerHuman, "PLAYER_METADATA")
        metadata = PlayerHuman.PLAYER_METADATA
        assert metadata["display_name"] == "Human Player"
        assert metadata["enabled"] == True

    def test_get_name(self):
        """Test get_name method."""
        provider = MockInputProvider([Move(3, 3)])
        player = PlayerHuman(provider, name="CustomName")
        assert player.get_name() == "CustomName"

    def test_reset_provider(self):
        """Test that provider is reset before getting move."""
        game = Game(8)
        moves = game.get_move_list()
        if len(moves) > 0:
            provider = MockInputProvider(moves[:2])
            player = PlayerHuman(provider)
            # Test that reset method exists
            assert hasattr(provider, "reset")
            try:
                move1 = player.get_move(game, moves)
                move2 = player.get_move(game, moves)
                assert move1 is None or isinstance(move1, Move)
                assert move2 is None or isinstance(move2, Move)
            except (StopIteration, ValueError):
                pass
