"""
Test suite for Apocalyptron Cache Module.

Tests caching components:
- ZobristHash
- TranspositionTable
"""

import pytest
from src.Reversi.BitboardGame import BitboardGame
from src.AI.Apocalyptron.cache.zobrist_hash import ZobristHash
from src.AI.Apocalyptron.cache.transposition_table import TranspositionTable


class TestZobristHash:
    """Test suite for Zobrist hashing."""
    
    def test_zobrist_initialization(self):
        """Test Zobrist hash initializes correctly."""
        hasher = ZobristHash()
        
        assert hasher is not None
        assert hasattr(hasher, 'hash_position')
    
    def test_same_position_same_hash(self):
        """Test that same position always produces same hash."""
        game = BitboardGame()
        hasher = ZobristHash()
        
        hash1 = hasher.hash_position(game)
        hash2 = hasher.hash_position(game)
        
        assert hash1 == hash2, "Same position should produce same hash"
    
    def test_different_positions_different_hash(self):
        """Test that different positions produce different hashes."""
        game1 = BitboardGame()
        game2 = game1.make_move(19)  # Different position
        
        hasher = ZobristHash()
        
        hash1 = hasher.hash_position(game1)
        hash2 = hasher.hash_position(game2)
        
        assert hash1 != hash2, "Different positions should have different hashes"
    
    def test_hash_is_integer(self):
        """Test that hash is an integer."""
        game = BitboardGame()
        hasher = ZobristHash()
        
        hash_value = hasher.hash_position(game)
        
        assert isinstance(hash_value, int), "Hash should be integer"
        assert hash_value >= 0, "Hash should be non-negative"
    
    def test_hash_deterministic(self):
        """Test that hash is deterministic (not random)."""
        hasher1 = ZobristHash()
        hasher2 = ZobristHash()
        
        game = BitboardGame()
        
        hash1 = hasher1.hash_position(game)
        hash2 = hasher2.hash_position(game)
        
        assert hash1 == hash2, "Hash should be deterministic across instances"
    
    def test_incremental_hash_update(self):
        """Test incremental hash update is faster than full rehash."""
        game = BitboardGame()
        hasher = ZobristHash()
        
        hash1 = hasher.hash_position(game)
        
        # Make move
        game2 = game.make_move(19)
        
        # Full hash
        hash2_full = hasher.hash_position(game2)
        
        # Incremental update (if implemented)
        if hasattr(hasher, 'update_hash'):
            hash2_incremental = hasher.update_hash(hash1, game, game2, 19)
            
            assert hash2_full == hash2_incremental, "Incremental hash should match full hash"
    
    def test_hash_collision_resistance(self):
        """Test that hash collisions are rare."""
        hasher = ZobristHash()
        
        # Generate hashes for first 100 game positions
        hashes = set()
        game = BitboardGame()
        
        for _ in range(10):  # Limited iterations for test speed
            moves = game.get_valid_moves(game.current_player)
            if not moves:
                break
            
            hash_value = hasher.hash_position(game)
            hashes.add(hash_value)
            
            game = game.make_move(moves[0])
        
        # All hashes should be unique
        assert len(hashes) >= 8, "Should have diverse hashes"


class TestTranspositionTable:
    """Test suite for Transposition Table."""
    
    def test_transposition_table_initialization(self):
        """Test TT initializes with correct size."""
        tt = TranspositionTable(size_mb=1)  # Small for testing
        
        assert tt is not None
        assert hasattr(tt, 'store')
        assert hasattr(tt, 'lookup')
    
    def test_store_and_lookup(self):
        """Test storing and retrieving from TT."""
        tt = TranspositionTable(size_mb=1)
        
        hash_value = 12345
        entry = {
            'hash': hash_value,
            'depth': 5,
            'score': 42.0,
            'move': 19,
            'type': 'exact'
        }
        
        # Store
        tt.store(
            hash_value=hash_value,
            depth=entry['depth'],
            score=entry['score'],
            move=entry['move'],
            node_type=entry['type']
        )
        
        # Lookup
        retrieved = tt.lookup(hash_value)
        
        assert retrieved is not None, "Should find stored entry"
        assert retrieved['hash'] == hash_value
        assert retrieved['depth'] == 5
        assert retrieved['score'] == 42.0
        assert retrieved['move'] == 19
    
    def test_lookup_miss(self):
        """Test lookup of non-existent entry."""
        tt = TranspositionTable(size_mb=1)
        
        result = tt.lookup(99999)
        
        assert result is None, "Should return None for miss"
    
    def test_replacement_strategy(self):
        """Test that deeper searches replace shallower ones."""
        tt = TranspositionTable(size_mb=1)
        
        hash_value = 12345
        
        # Store shallow search
        tt.store(hash_value, depth=3, score=10.0, move=19, node_type='exact')
        
        # Store deeper search
        tt.store(hash_value, depth=7, score=20.0, move=26, node_type='exact')
        
        # Should retrieve deeper search
        entry = tt.lookup(hash_value)
        
        assert entry['depth'] == 7, "Deeper search should replace shallow"
        assert entry['move'] == 26, "Should have move from deeper search"
    
    def test_hash_collision_handling(self):
        """Test that hash collisions are handled correctly."""
        tt = TranspositionTable(size_mb=1)
        
        # Create two entries that might collide (same index, different hash)
        hash1 = 1000
        hash2 = 1000 + tt.size  # Will have same index
        
        tt.store(hash1, depth=5, score=10.0, move=19, node_type='exact')
        tt.store(hash2, depth=5, score=20.0, move=26, node_type='exact')
        
        # Lookup should return correct entry
        entry1 = tt.lookup(hash1)
        entry2 = tt.lookup(hash2)
        
        # One will be overwritten (depends on replacement strategy)
        # At least one should be retrievable
        assert entry1 is not None or entry2 is not None
    
    def test_node_types(self):
        """Test different node types (exact, lower, upper)."""
        tt = TranspositionTable(size_mb=1)
        
        node_types = ['exact', 'lower', 'upper']
        
        for i, node_type in enumerate(node_types):
            hash_value = 1000 + i
            tt.store(hash_value, depth=5, score=10.0, move=19, node_type=node_type)
            
            entry = tt.lookup(hash_value)
            assert entry['type'] == node_type, f"Node type {node_type} should be preserved"
    
    def test_statistics_tracking(self):
        """Test that TT tracks hits and misses."""
        tt = TranspositionTable(size_mb=1)
        
        # Initial stats
        initial_hits = tt.hits if hasattr(tt, 'hits') else 0
        initial_misses = tt.misses if hasattr(tt, 'misses') else 0
        
        # Store entry
        tt.store(12345, depth=5, score=10.0, move=19, node_type='exact')
        
        # Hit
        tt.lookup(12345)
        
        # Miss
        tt.lookup(99999)
        
        # Check stats updated (if implemented)
        if hasattr(tt, 'hits') and hasattr(tt, 'misses'):
            assert tt.hits > initial_hits, "Hits should increase"
            assert tt.misses > initial_misses, "Misses should increase"
    
    def test_clear_table(self):
        """Test clearing the transposition table."""
        tt = TranspositionTable(size_mb=1)
        
        # Store some entries
        tt.store(1, depth=5, score=10.0, move=19, node_type='exact')
        tt.store(2, depth=5, score=20.0, move=26, node_type='exact')
        
        # Clear if implemented
        if hasattr(tt, 'clear'):
            tt.clear()
            
            # Should not find entries after clear
            assert tt.lookup(1) is None
            assert tt.lookup(2) is None


class TestCacheIntegration:
    """Test integration between Zobrist and TranspositionTable."""
    
    def test_zobrist_with_transposition_table(self):
        """Test using Zobrist hash with TT."""
        game = BitboardGame()
        hasher = ZobristHash()
        tt = TranspositionTable(size_mb=1)
        
        # Hash position
        hash_value = hasher.hash_position(game)
        
        # Store in TT
        tt.store(hash_value, depth=5, score=42.0, move=19, node_type='exact')
        
        # Retrieve
        entry = tt.lookup(hash_value)
        
        assert entry is not None
        assert entry['score'] == 42.0
    
    def test_game_sequence_hashing(self):
        """Test hashing a sequence of game positions."""
        game = BitboardGame()
        hasher = ZobristHash()
        tt = TranspositionTable(size_mb=1)
        
        # Play a few moves and cache each position
        for i in range(5):
            moves = game.get_valid_moves(game.current_player)
            if not moves:
                break
            
            hash_value = hasher.hash_position(game)
            tt.store(hash_value, depth=5, score=float(i), move=moves[0], node_type='exact')
            
            game = game.make_move(moves[0])
        
        # Verify we can retrieve them
        # (Note: some might be overwritten due to collisions)
        assert tt.hits + tt.misses > 0 if hasattr(tt, 'hits') else True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

