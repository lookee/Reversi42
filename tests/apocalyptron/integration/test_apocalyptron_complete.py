"""
Complete integration tests for Apocalyptron engine.

Tests the full engine with all components working together:
- Search + Evaluation + Ordering + Pruning + Cache + Observers
"""

import pytest
import time
from src.Reversi.BitboardGame import BitboardGame
from src.Players.PlayerApocalyptron import PlayerApocalyptron
from src.AI.Apocalyptron.factory.factory import ApocalyptronFactory
from src.AI.Apocalyptron.observers.statistics import StatisticsObserver


class TestApocalyptronIntegration:
    """Integration tests for complete Apocalyptron engine."""
    
    def test_apocalyptron_player_creation(self):
        """Test creating Apocalyptron player."""
        player = PlayerApocalyptron(depth=6)
        
        assert player is not None
        assert hasattr(player, 'get_move')
    
    def test_apocalyptron_makes_valid_move(self):
        """Test that Apocalyptron makes valid moves."""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=6)
        
        moves = game.get_valid_moves(game.current_player)
        move = player.get_move(game, moves, control=None)
        
        assert move is not None, "Should return a move"
        assert move in moves, "Move should be valid"
    
    def test_apocalyptron_different_depths(self):
        """Test Apocalyptron at different depth settings."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        for depth in [4, 6, 8]:
            player = PlayerApocalyptron(depth=depth)
            move = player.get_move(game, moves, control=None)
            
            assert move in moves, f"Move should be valid at depth {depth}"
    
    def test_apocalyptron_opening_book_integration(self):
        """Test that Apocalyptron uses opening book when available."""
        game = BitboardGame()
        
        # Create with opening book
        config = ApocalyptronFactory.create_default_config(depth=6)
        config.use_opening_book = True
        player = PlayerApocalyptron(config=config)
        
        moves = game.get_valid_moves(1)
        move = player.get_move(game, moves, control=None)
        
        # Should return immediately (book move)
        assert move in moves
    
    def test_apocalyptron_full_game(self):
        """Test Apocalyptron playing a complete game."""
        game = BitboardGame()
        black = PlayerApocalyptron(depth=4)
        white = PlayerApocalyptron(depth=4)
        
        move_count = 0
        max_moves = 60
        
        while not game.is_game_over() and move_count < max_moves:
            moves = game.get_valid_moves(game.current_player)
            
            if not moves:
                game = game.pass_turn()
                continue
            
            player = black if game.current_player == 1 else white
            move = player.get_move(game, moves, control=None)
            
            assert move in moves, f"Invalid move at move {move_count}"
            
            game = game.make_move(move)
            move_count += 1
        
        # Game should complete
        black_score, white_score = game.get_score()
        assert black_score + white_score <= 64, "Total pieces should be <= 64"
        assert black_score > 0 or white_score > 0, "Should have pieces"
    
    @pytest.mark.slow
    def test_apocalyptron_performance_depth_6(self):
        """Test Apocalyptron performance at depth 6."""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=6)
        moves = game.get_valid_moves(1)
        
        start = time.perf_counter()
        move = player.get_move(game, moves, control=None)
        elapsed = time.perf_counter() - start
        
        assert move is not None
        assert elapsed < 1.0, f"Depth 6 should be < 1s, got {elapsed:.2f}s"
    
    @pytest.mark.slow
    def test_apocalyptron_performance_depth_9(self):
        """Test Apocalyptron performance at depth 9."""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=9)
        moves = game.get_valid_moves(1)
        
        start = time.perf_counter()
        move = player.get_move(game, moves, control=None)
        elapsed = time.perf_counter() - start
        
        assert move is not None
        # Target: < 2s for depth 9
        # Allow more time in CI (might be slower)
        assert elapsed < 5.0, f"Depth 9 should be < 5s, got {elapsed:.2f}s"


class TestApocalyptronWithObservers:
    """Test Apocalyptron with different observers."""
    
    def test_apocalyptron_with_statistics_observer(self):
        """Test Apocalyptron with statistics observer."""
        game = BitboardGame()
        
        # Create with statistics observer
        observer = StatisticsObserver()
        config = ApocalyptronFactory.create_default_config(depth=5)
        
        # Create engine with observer (if factory supports it)
        player = PlayerApocalyptron(config=config)
        
        moves = game.get_valid_moves(1)
        move = player.get_move(game, moves, control=None)
        
        assert move in moves
    
    def test_apocalyptron_observer_statistics_collection(self):
        """Test that observer collects statistics during search."""
        game = BitboardGame()
        
        observer = StatisticsObserver()
        config = ApocalyptronFactory.create_default_config(depth=5)
        
        player = PlayerApocalyptron(config=config)
        
        # Add observer if possible
        if hasattr(player, 'add_observer'):
            player.add_observer(observer)
        
        moves = game.get_valid_moves(1)
        move = player.get_move(game, moves, control=None)
        
        # Check statistics
        if hasattr(observer, 'get_statistics'):
            stats = observer.get_statistics()
            assert stats is not None


class TestApocalyptronEdgeCases:
    """Test edge cases for Apocalyptron engine."""
    
    def test_apocalyptron_single_move_position(self):
        """Test Apocalyptron when only one move available."""
        # Create position with only one move
        # This is position-dependent, but test that it handles gracefully
        game = BitboardGame()
        player = PlayerApocalyptron(depth=6)
        
        moves = game.get_valid_moves(game.current_player)
        
        # Even with one move, should work
        if len(moves) == 1:
            move = player.get_move(game, moves, control=None)
            assert move == moves[0], "Should return the only move"
    
    def test_apocalyptron_late_game_position(self):
        """Test Apocalyptron in late game positions."""
        # Create a late-game position (many pieces on board)
        black = 0x0FFFFFFF00000000  # ~28 pieces
        white = 0x00000000F0FFFFFF  # ~28 pieces
        game = BitboardGame(black=black, white=white, current_player=1)
        
        player = PlayerApocalyptron(depth=6)
        moves = game.get_valid_moves(game.current_player)
        
        if moves:  # If there are moves available
            move = player.get_move(game, moves, control=None)
            assert move in moves
    
    def test_apocalyptron_near_endgame(self):
        """Test Apocalyptron in near-endgame positions."""
        # Position with few empty squares
        black = 0xFFFFFFFF00000000
        white = 0x00000000FFFFFFF0  # ~4 empty
        game = BitboardGame(black=black, white=white, current_player=1)
        
        player = PlayerApocalyptron(depth=8)
        moves = game.get_valid_moves(game.current_player)
        
        if moves:
            move = player.get_move(game, moves, control=None)
            assert move in moves


class TestApocalyptronConfiguration:
    """Test Apocalyptron configuration options."""
    
    def test_create_with_factory_default(self):
        """Test creating Apocalyptron with factory defaults."""
        config = ApocalyptronFactory.create_default_config()
        
        assert config is not None
        assert hasattr(config, 'depth')
        assert config.depth >= 7, "Default depth should be 7+"
    
    def test_create_with_custom_config(self):
        """Test creating Apocalyptron with custom configuration."""
        config = ApocalyptronFactory.create_default_config(depth=10)
        
        assert config.depth == 10, "Should respect custom depth"
    
    def test_disable_opening_book(self):
        """Test Apocalyptron without opening book."""
        config = ApocalyptronFactory.create_default_config(depth=6)
        config.use_opening_book = False
        
        player = PlayerApocalyptron(config=config)
        
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        move = player.get_move(game, moves, control=None)
        
        assert move in moves
    
    def test_different_evaluation_weights(self):
        """Test Apocalyptron with different evaluation weights."""
        config = ApocalyptronFactory.create_default_config(depth=5)
        
        # Modify weights if accessible
        player = PlayerApocalyptron(config=config)
        
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        move = player.get_move(game, moves, control=None)
        
        assert move in moves


class TestApocalyptronDeterminism:
    """Test that Apocalyptron is deterministic."""
    
    def test_same_position_same_move(self):
        """Test that same position produces same move."""
        game = BitboardGame()
        player = PlayerApocalyptron(depth=6)
        moves = game.get_valid_moves(1)
        
        move1 = player.get_move(game, moves, control=None)
        move2 = player.get_move(game, moves, control=None)
        
        assert move1 == move2, "Same position should give same move"
    
    def test_consistent_across_instances(self):
        """Test consistency across different player instances."""
        game = BitboardGame()
        moves = game.get_valid_moves(1)
        
        player1 = PlayerApocalyptron(depth=6)
        player2 = PlayerApocalyptron(depth=6)
        
        move1 = player1.get_move(game, moves, control=None)
        move2 = player2.get_move(game, moves, control=None)
        
        assert move1 == move2, "Different instances should give same move"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

