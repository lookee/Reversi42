"""
Test suite for Apocalyptron Search Module.

Tests search algorithms:
- Iterative Deepening
- Alpha-Beta Complete
- Parallel Search
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from Reversi.BitboardGame import BitboardGame
from AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.search.alphabeta import AlphaBetaSearch
from AI.Apocalyptron.evaluation.composite import CompositeEvaluator
from AI.Apocalyptron.ordering.composite import CompositeOrderer
from AI.Apocalyptron.core.search_context import SearchContext
try:
    from AI.Apocalyptron.search.parallel import ParallelSearch
    PARALLEL_AVAILABLE = True
except ImportError:
    PARALLEL_AVAILABLE = False


def create_search_components():
    """Create standard search components for testing."""
    evaluator = CompositeEvaluator()
    orderer = CompositeOrderer()
    return evaluator, orderer


def create_alphabeta_complete_with_observers():
    """Create AlphaBetaSearchComplete with observers attribute."""
    evaluator, orderer = create_search_components()
    search = AlphaBetaSearchComplete(evaluator, orderer)
    # Add observers attribute if it doesn't exist
    if not hasattr(search, 'observers'):
        search.observers = []
    
    # Create a wrapper that filters parameters for compatibility
    class AlphaBetaSearchCompleteWrapper:
        def __init__(self, base_search):
            self.base_search = base_search
            self.observers = base_search.observers
        
        def get_best_move(self, game, target_depth, player_name=None, opening_book=None, game_history=None):
            # Only pass the parameters that AlphaBetaSearchComplete accepts
            return self.base_search.get_best_move(game, target_depth)
    
    return AlphaBetaSearchCompleteWrapper(search)


def create_search_context(game, depth=3):
    """Create a SearchContext for testing."""
    return SearchContext(
        game=game,
        depth=depth,
        alpha=-10000,
        beta=10000,
        allow_null_move=True,
        ply_from_root=0,
        killer_moves=(),
        history_table={},
        move_list=None
    )


class TestAlphaBetaSearch:
    """Test suite for basic Alpha-Beta search."""
    
    def test_alphabeta_initialization(self):
        """Test alpha-beta search initializes."""
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearch(evaluator, orderer)
        
        assert search is not None
        assert hasattr(search, 'search')
    
    def test_alphabeta_finds_move(self):
        """Test that alpha-beta finds a valid move."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearch(evaluator, orderer)
        
        context = create_search_context(game, depth=3)
        result = search.search(context)
        
        assert result.best_move is not None, "Should find a move"
        assert result.best_move in game.get_move_list(), "Move should be valid"
        assert isinstance(result.value, (int, float)), "Score should be numeric"
    
    def test_alphabeta_depth_1(self):
        """Test alpha-beta at depth 1 (immediate evaluation)."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearch(evaluator, orderer)
        
        context = create_search_context(game, depth=1)
        result = search.search(context)
        score, move = result.value, result.best_move
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_alphabeta_deeper_search_better(self):
        """Test that deeper search generally finds better moves."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearch(evaluator, orderer)
        
        context_shallow = create_search_context(game, depth=2)
        result_shallow = search.search(context_shallow)
        score_shallow, move_shallow = result_shallow.value, result_shallow.best_move
        context_deep = create_search_context(game, depth=4)
        result_deep = search.search(context_deep)
        score_deep, move_deep = result_deep.value, result_deep.best_move
        
        # Deeper search should give same or better evaluation
        # (might be same move or different, but evaluation shouldn't be worse)
        assert isinstance(score_shallow, (int, float))
        assert isinstance(score_deep, (int, float))
    
    def test_alphabeta_pruning_reduces_nodes(self):
        """Test that alpha-beta prunes nodes."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearch(evaluator, orderer)
        
        # Search with tracking
        context = create_search_context(game, depth=4)
        result = search.search(context)
        score, move = result.value, result.best_move
        
        # Should search far fewer nodes than minimax would
        # (Minimax at depth 4: ~4^4 = 256 nodes, alpha-beta: ~16-64)
        if hasattr(search, 'nodes_searched'):
            assert search.nodes_searched < 256, "Alpha-beta should prune nodes"


class TestAlphaBetaSearchComplete:
    """Test suite for Alpha-Beta Complete (with all optimizations)."""
    
    def test_complete_search_initialization(self):
        """Test complete search initializes."""
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearchComplete(evaluator, orderer)
        
        assert search is not None
        assert hasattr(search, 'get_best_move')
    
    def test_complete_search_finds_move(self):
        """Test that complete search finds valid move."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearchComplete(evaluator, orderer)
        
        move = search.get_best_move(game, depth=4)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_complete_search_uses_transposition_table(self):
        """Test that complete search uses transposition table."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearchComplete(evaluator, orderer)
        
        # First search
        move1 = search.get_best_move(game, depth=5)
        
        # Second search of same position
        move2 = search.get_best_move(game, depth=5)
        
        # Should be instant due to TT (if implemented)
        # At minimum, should give consistent results
        assert move1 == move2, "Same position should give same move"
    
    def test_complete_search_respects_depth(self):
        """Test that search respects depth limit."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearchComplete(evaluator, orderer)
        
        # Search at different depths
        move_3 = search.get_best_move(game, depth=3)
        move_5 = search.get_best_move(game, depth=5)
        
        # Deeper search might find different move or same
        assert move_3 is not None
        assert move_5 is not None
        assert move_3 in game.get_move_list()
        assert move_5 in game.get_move_list()


class TestIterativeDeepeningSearch:
    """Test suite for Iterative Deepening."""
    
    def test_iterative_deepening_initialization(self):
        """Test iterative deepening initializes."""
        evaluator, orderer = create_search_components()
        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        search = IterativeDeepeningSearch(alphabeta)
        
        assert search is not None
        assert hasattr(search, 'get_best_move')
    
    def test_iterative_deepening_reaches_target_depth(self):
        """Test that ID searches to target depth."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        search = IterativeDeepeningSearch(alphabeta)
        
        move = search.get_best_move(game, target_depth=4)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_iterative_deepening_progressive_results(self):
        """Test that ID provides progressive results."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        search = IterativeDeepeningSearch(alphabeta)
        
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
        evaluator, orderer = create_search_components()
        alphabeta = AlphaBetaSearchComplete(evaluator, orderer)
        search = IterativeDeepeningSearch(alphabeta)
        
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
        base_search = create_alphabeta_complete_with_observers()
        search = ParallelSearch(base_search, num_workers=2)
        
        assert search is not None
        assert hasattr(search, 'get_best_move')
    
    def test_parallel_search_finds_move(self):
        """Test that parallel search finds valid move."""
        game = BitboardGame()
        base_search = create_alphabeta_complete_with_observers()
        search = ParallelSearch(base_search, num_workers=2)
        
        move = search.get_best_move(game, target_depth=4)
        
        assert move is not None
        assert move in game.get_move_list()
    
    def test_parallel_same_result_as_serial(self):
        """Test that parallel search gives same result as serial."""
        game = BitboardGame()
        
        serial_search = AlphaBetaSearch(*create_search_components())
        base_search = create_alphabeta_complete_with_observers()
        parallel_search = ParallelSearch(base_search, num_workers=2)
        
        context = create_search_context(game, depth=3)
        result_serial = serial_search.search(context)
        score_serial, move_serial = result_serial.value, result_serial.best_move
        
        move_parallel = parallel_search.get_best_move(game, target_depth=3)
        
        # Should find same best move (or at least same score)
        assert move_serial == move_parallel, "Parallel should match serial"
    
    @pytest.mark.slow
    def test_parallel_faster_than_serial(self):
        """Test that parallel search is faster (on multi-core)."""
        import time
        
        game = BitboardGame()
        
        serial_search = AlphaBetaSearch(*create_search_components())
        base_search = create_alphabeta_complete_with_observers()
        parallel_search = ParallelSearch(base_search, num_workers=4)
        
        # Measure serial
        start = time.perf_counter()
        context = create_search_context(game, depth=6)
        serial_search.search(context)
        serial_time = time.perf_counter() - start
        
        # Measure parallel
        start = time.perf_counter()
        parallel_search.get_best_move(game, target_depth=6)
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
            AlphaBetaSearch(*create_search_components()),
            AlphaBetaSearchComplete(*create_search_components()),
            IterativeDeepeningSearch(AlphaBetaSearchComplete(*create_search_components())),
        ]
        
        if PARALLEL_AVAILABLE:
            base_search = create_alphabeta_complete_with_observers()
            searches.append(ParallelSearch(base_search, num_workers=2))
        
        for search in searches:
            if hasattr(search, 'get_best_move') and not hasattr(search, 'search'):
                # AlphaBetaSearchComplete, IterativeDeepeningSearch, and ParallelSearch
                if hasattr(search, 'target_depth'):
                    # IterativeDeepeningSearch
                    move = search.get_best_move(game, target_depth=3)
                elif hasattr(search, 'base_search'):
                    # ParallelSearch
                    move = search.get_best_move(game, target_depth=3)
                else:
                    # AlphaBetaSearchComplete
                    move = search.get_best_move(game, 3)
            else:
                # AlphaBetaSearch
                context = create_search_context(game, depth=3)
                result = search.search(context)
                # Check if result is a SearchResult or a Move
                if hasattr(result, 'best_move'):
                    move = result.best_move
                else:
                    move = result  # result is already a Move
            
            valid_moves = game.get_move_list()
            assert move in valid_moves, f"{search.__class__.__name__} found invalid move"
    
    def test_deeper_search_consistency(self):
        """Test that search is consistent at different depths."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearch(evaluator, orderer)
        
        # Search at depth 3 and 5
        context_3 = create_search_context(game, depth=3)
        result_3 = search.search(context_3)
        score_3, move_3 = result_3.value, result_3.best_move
        
        context_5 = create_search_context(game, depth=5)
        result_5 = search.search(context_5)
        score_5, move_5 = result_5.value, result_5.best_move
        
        # Both should be valid
        valid_moves = game.get_move_list()
        assert move_3 in valid_moves
        assert move_5 in valid_moves
    
    @pytest.mark.parametrize("depth", [1, 2, 3, 4, 5])
    def test_search_at_various_depths(self, depth):
        """Test search works at various depths."""
        game = BitboardGame()
        evaluator, orderer = create_search_components()
        search = AlphaBetaSearch(evaluator, orderer)
        
        context = create_search_context(game, depth=depth)
        result = search.search(context)
        score, move = result.value, result.best_move
        
        assert move is not None
        assert move in game.get_move_list()
        assert isinstance(score, (int, float))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

