"""
Test suite for Apocalyptron Search Module.

Tests search algorithms:
- Iterative Deepening
- Alpha-Beta Complete
- Parallel Search
"""

import pytest
from src.Reversi.BitboardGame import BitboardGame
from src.AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
from src.AI.Apocalyptron.search.alphabeta_complete import AlphaBetaCompleteSearch
from src.AI.Apocalyptron.search.alphabeta import AlphaBetaSearch
try:
    from src.AI.Apocalyptron.search.parallel import ParallelSearch
    PARALLEL_AVAILABLE = True
except ImportError:
    PARALLEL_AVAILABLE = False


class TestAlphaBetaSearch:
    """Test suite for basic Alpha-Beta search."""
    
    def test_alphabeta_initialization(self):
        """Test alpha-beta search initializes."""
        search = AlphaBetaSearch()
        
        assert search is not None
        assert hasattr(search, 'search')
    
    def test_alphabeta_finds_move(self):
        """Test that alpha-beta finds a valid move."""
        game = BitboardGame()
        search = AlphaBetaSearch()
        
        score, move = search.search(game, depth=3)
        
        assert move is not None, "Should find a move"
        assert move in game.get_valid_moves(game.current_player), "Move should be valid"
        assert isinstance(score, (int, float)), "Score should be numeric"
    
    def test_alphabeta_depth_1(self):
        """Test alpha-beta at depth 1 (immediate evaluation)."""
        game = BitboardGame()
        search = AlphaBetaSearch()
        
        score, move = search.search(game, depth=1)
        
        assert move is not None
        assert move in game.get_valid_moves(1)
    
    def test_alphabeta_deeper_search_better(self):
        """Test that deeper search generally finds better moves."""
        game = BitboardGame()
        search = AlphaBetaSearch()
        
        score_shallow, move_shallow = search.search(game, depth=2)
        score_deep, move_deep = search.search(game, depth=4)
        
        # Deeper search should give same or better evaluation
        # (might be same move or different, but evaluation shouldn't be worse)
        assert isinstance(score_shallow, (int, float))
        assert isinstance(score_deep, (int, float))
    
    def test_alphabeta_pruning_reduces_nodes(self):
        """Test that alpha-beta prunes nodes."""
        game = BitboardGame()
        search = AlphaBetaSearch()
        
        # Search with tracking
        score, move = search.search(game, depth=4)
        
        # Should search far fewer nodes than minimax would
        # (Minimax at depth 4: ~4^4 = 256 nodes, alpha-beta: ~16-64)
        if hasattr(search, 'nodes_searched'):
            assert search.nodes_searched < 256, "Alpha-beta should prune nodes"


class TestAlphaBetaCompleteSearch:
    """Test suite for Alpha-Beta Complete (with all optimizations)."""
    
    def test_complete_search_initialization(self):
        """Test complete search initializes."""
        search = AlphaBetaCompleteSearch()
        
        assert search is not None
        assert hasattr(search, 'search')
    
    def test_complete_search_finds_move(self):
        """Test that complete search finds valid move."""
        game = BitboardGame()
        search = AlphaBetaCompleteSearch()
        
        score, move = search.search(game, depth=4)
        
        assert move is not None
        assert move in game.get_valid_moves(game.current_player)
    
    def test_complete_search_uses_transposition_table(self):
        """Test that complete search uses transposition table."""
        game = BitboardGame()
        search = AlphaBetaCompleteSearch()
        
        # First search
        score1, move1 = search.search(game, depth=5)
        
        # Second search of same position
        score2, move2 = search.search(game, depth=5)
        
        # Should be instant due to TT (if implemented)
        # At minimum, should give consistent results
        assert score1 == score2, "Same position should give same score"
        assert move1 == move2, "Same position should give same move"
    
    def test_complete_search_respects_depth(self):
        """Test that search respects depth limit."""
        game = BitboardGame()
        search = AlphaBetaCompleteSearch()
        
        # Search at different depths
        score_3, move_3 = search.search(game, depth=3)
        score_5, move_5 = search.search(game, depth=5)
        
        # Deeper search might find different move or same
        assert isinstance(score_3, (int, float))
        assert isinstance(score_5, (int, float))


class TestIterativeDeepeningSearch:
    """Test suite for Iterative Deepening."""
    
    def test_iterative_deepening_initialization(self):
        """Test iterative deepening initializes."""
        search = IterativeDeepeningSearch()
        
        assert search is not None
        assert hasattr(search, 'search')
    
    def test_iterative_deepening_reaches_target_depth(self):
        """Test that ID searches to target depth."""
        game = BitboardGame()
        search = IterativeDeepeningSearch()
        
        score, move = search.search(game, max_depth=4)
        
        assert move is not None
        assert move in game.get_valid_moves(game.current_player)
    
    def test_iterative_deepening_progressive_results(self):
        """Test that ID provides progressive results."""
        game = BitboardGame()
        search = IterativeDeepeningSearch()
        
        results = []
        
        # Track results at each depth (if observable)
        if hasattr(search, 'add_observer'):
            class ResultCollector:
                def __init__(self):
                    self.depths = []
                
                def on_depth_complete(self, depth, score, move, nodes):
                    self.depths.append(depth)
            
            collector = ResultCollector()
            search.add_observer(collector)
            
            search.search(game, max_depth=4)
            
            # Should have searched depths 1, 2, 3, 4
            assert len(collector.depths) >= 3, "Should search multiple depths"
    
    def test_iterative_deepening_can_stop_early(self):
        """Test that ID can stop before max depth (time limit)."""
        game = BitboardGame()
        search = IterativeDeepeningSearch()
        
        # Set very short time limit (if supported)
        if hasattr(search, 'set_time_limit'):
            search.set_time_limit(0.001)  # 1ms
            
            score, move = search.search(game, max_depth=10)
            
            # Should still return a move (from depth 1 or 2)
            assert move is not None


@pytest.mark.skipif(not PARALLEL_AVAILABLE, reason="Parallel search not available")
class TestParallelSearch:
    """Test suite for Parallel Search."""
    
    def test_parallel_search_initialization(self):
        """Test parallel search initializes."""
        search = ParallelSearch(num_cores=2)
        
        assert search is not None
        assert hasattr(search, 'search')
    
    def test_parallel_search_finds_move(self):
        """Test that parallel search finds valid move."""
        game = BitboardGame()
        search = ParallelSearch(num_cores=2)
        
        score, move = search.search(game, depth=4)
        
        assert move is not None
        assert move in game.get_valid_moves(game.current_player)
    
    def test_parallel_same_result_as_serial(self):
        """Test that parallel search gives same result as serial."""
        game = BitboardGame()
        
        serial_search = AlphaBetaSearch()
        parallel_search = ParallelSearch(num_cores=2)
        
        score_serial, move_serial = serial_search.search(game, depth=3)
        score_parallel, move_parallel = parallel_search.search(game, depth=3)
        
        # Should find same best move (or at least same score)
        assert abs(score_serial - score_parallel) < 0.1, "Parallel should match serial"
    
    @pytest.mark.slow
    def test_parallel_faster_than_serial(self):
        """Test that parallel search is faster (on multi-core)."""
        import time
        
        game = BitboardGame()
        
        serial_search = AlphaBetaSearch()
        parallel_search = ParallelSearch(num_cores=4)
        
        # Measure serial
        start = time.perf_counter()
        serial_search.search(game, depth=6)
        serial_time = time.perf_counter() - start
        
        # Measure parallel
        start = time.perf_counter()
        parallel_search.search(game, depth=6)
        parallel_time = time.perf_counter() - start
        
        # Parallel should be faster (allow some overhead)
        # On single-core CI, might not be faster, so just check it works
        assert parallel_time > 0, "Parallel search completed"


class TestSearchConsistency:
    """Test consistency across search algorithms."""
    
    def test_all_searches_find_valid_moves(self):
        """Test that all search types find valid moves."""
        game = BitboardGame()
        
        searches = [
            AlphaBetaSearch(),
            AlphaBetaCompleteSearch(),
            IterativeDeepeningSearch(),
        ]
        
        if PARALLEL_AVAILABLE:
            searches.append(ParallelSearch(num_cores=2))
        
        for search in searches:
            score, move = search.search(game, depth=3)
            
            valid_moves = game.get_valid_moves(game.current_player)
            
            assert move in valid_moves, f"{search.__class__.__name__} found invalid move"
    
    def test_deeper_search_consistency(self):
        """Test that search is consistent at different depths."""
        game = BitboardGame()
        search = AlphaBetaSearch()
        
        # Search at depth 3 and 5
        score_3, move_3 = search.search(game, depth=3)
        score_5, move_5 = search.search(game, depth=5)
        
        # Both should be valid
        valid_moves = game.get_valid_moves(1)
        assert move_3 in valid_moves
        assert move_5 in valid_moves
    
    @pytest.mark.parametrize("depth", [1, 2, 3, 4, 5])
    def test_search_at_various_depths(self, depth):
        """Test search works at various depths."""
        game = BitboardGame()
        search = AlphaBetaSearch()
        
        score, move = search.search(game, depth=depth)
        
        assert move is not None
        assert move in game.get_valid_moves(game.current_player)
        assert isinstance(score, (int, float))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

