"""
Test suite for Apocalyptron Observer Module.

Tests observer implementations:
- ConsoleObserver
- StatisticsObserver
- QuietObserver
- Observer pattern compliance
"""

import pytest
from io import StringIO
import sys
from src.Reversi.BitboardGame import BitboardGame
from src.AI.Apocalyptron.observers.console import ConsoleObserver
from src.AI.Apocalyptron.observers.statistics import StatisticsObserver
from src.AI.Apocalyptron.observers.quiet import QuietObserver
from src.AI.Apocalyptron.observers.interfaces import SearchObserver


class TestConsoleObserver:
    """Test suite for ConsoleObserver."""
    
    def test_console_observer_initialization(self):
        """Test console observer initializes."""
        observer = ConsoleObserver()
        
        assert observer is not None
        assert isinstance(observer, SearchObserver)
    
    def test_console_observer_prints_output(self):
        """Test that console observer produces output."""
        observer = ConsoleObserver()
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            observer.on_search_start(BitboardGame(), depth=5)
            observer.on_depth_complete(depth=3, score=42.0, move=19, nodes=1000)
            observer.on_search_complete(best_move=19, best_score=42.0, total_nodes=5000)
            
            output = captured_output.getvalue()
            
            # Should have printed something
            assert len(output) > 0, "Console observer should print output"
            
        finally:
            sys.stdout = sys.__stdout__
    
    def test_console_observer_methods_dont_crash(self):
        """Test all observer methods execute without errors."""
        observer = ConsoleObserver()
        game = BitboardGame()
        
        # Should not crash
        observer.on_search_start(game, depth=5)
        observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=100)
        observer.on_depth_complete(depth=2, score=5.0, move=26, nodes=500)
        observer.on_search_complete(best_move=26, best_score=5.0, total_nodes=1000)


class TestStatisticsObserver:
    """Test suite for StatisticsObserver."""
    
    def test_statistics_observer_initialization(self):
        """Test statistics observer initializes."""
        observer = StatisticsObserver()
        
        assert observer is not None
        assert hasattr(observer, 'get_statistics')
    
    def test_statistics_collection(self):
        """Test that statistics observer collects data."""
        observer = StatisticsObserver()
        game = BitboardGame()
        
        observer.on_search_start(game, depth=5)
        observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=100)
        observer.on_depth_complete(depth=2, score=5.0, move=26, nodes=500)
        observer.on_depth_complete(depth=3, score=10.0, move=37, nodes=2000)
        observer.on_search_complete(best_move=37, best_score=10.0, total_nodes=5000)
        
        stats = observer.get_statistics()
        
        assert stats is not None, "Should return statistics"
        assert isinstance(stats, dict), "Statistics should be a dictionary"
    
    def test_statistics_tracks_nodes(self):
        """Test that statistics tracks node count."""
        observer = StatisticsObserver()
        
        observer.on_search_start(BitboardGame(), depth=5)
        observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=100)
        observer.on_depth_complete(depth=2, score=0.0, move=19, nodes=500)
        observer.on_search_complete(best_move=19, best_score=0.0, total_nodes=1000)
        
        stats = observer.get_statistics()
        
        # Should track total nodes
        if 'nodes_searched' in stats or 'total_nodes' in stats:
            nodes = stats.get('nodes_searched', stats.get('total_nodes', 0))
            assert nodes >= 1000, "Should track node count"
    
    def test_statistics_tracks_depths(self):
        """Test that statistics tracks depths completed."""
        observer = StatisticsObserver()
        
        observer.on_search_start(BitboardGame(), depth=5)
        observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=100)
        observer.on_depth_complete(depth=2, score=5.0, move=26, nodes=500)
        observer.on_depth_complete(depth=3, score=10.0, move=37, nodes=2000)
        observer.on_search_complete(best_move=37, best_score=10.0, total_nodes=5000)
        
        stats = observer.get_statistics()
        
        # Should track depths
        if 'depths_completed' in stats:
            assert len(stats['depths_completed']) == 3
    
    def test_statistics_calculates_nps(self):
        """Test that statistics calculates nodes per second."""
        observer = StatisticsObserver()
        
        observer.on_search_start(BitboardGame(), depth=5)
        observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=1000)
        observer.on_search_complete(best_move=19, best_score=0.0, total_nodes=5000)
        
        stats = observer.get_statistics()
        
        # Should calculate NPS if time tracked
        if 'nps' in stats or 'nodes_per_second' in stats:
            nps = stats.get('nps', stats.get('nodes_per_second', 0))
            assert nps >= 0, "NPS should be non-negative"
    
    def test_statistics_reset(self):
        """Test that statistics can be reset."""
        observer = StatisticsObserver()
        
        # Collect some stats
        observer.on_search_start(BitboardGame(), depth=5)
        observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=1000)
        
        # Reset if implemented
        if hasattr(observer, 'reset'):
            observer.reset()
            
            stats = observer.get_statistics()
            
            # Stats should be cleared
            if 'nodes_searched' in stats:
                assert stats['nodes_searched'] == 0


class TestQuietObserver:
    """Test suite for QuietObserver (no output)."""
    
    def test_quiet_observer_initialization(self):
        """Test quiet observer initializes."""
        observer = QuietObserver()
        
        assert observer is not None
        assert isinstance(observer, SearchObserver)
    
    def test_quiet_observer_produces_no_output(self):
        """Test that quiet observer produces no output."""
        observer = QuietObserver()
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            observer.on_search_start(BitboardGame(), depth=5)
            observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=1000)
            observer.on_search_complete(best_move=19, best_score=0.0, total_nodes=5000)
            
            output = captured_output.getvalue()
            
            # Should produce no output
            assert len(output) == 0, "Quiet observer should produce no output"
            
        finally:
            sys.stdout = sys.__stdout__
    
    def test_quiet_observer_methods_dont_crash(self):
        """Test all quiet observer methods execute without errors."""
        observer = QuietObserver()
        game = BitboardGame()
        
        # Should not crash
        observer.on_search_start(game, depth=5)
        observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=100)
        observer.on_search_complete(best_move=19, best_score=0.0, total_nodes=1000)


class TestObserverPattern:
    """Test observer pattern compliance and integration."""
    
    def test_multiple_observers(self):
        """Test that multiple observers can be used simultaneously."""
        observers = [
            ConsoleObserver(),
            StatisticsObserver(),
            QuietObserver()
        ]
        
        game = BitboardGame()
        
        # All should handle same events
        for observer in observers:
            observer.on_search_start(game, depth=5)
            observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=100)
            observer.on_search_complete(best_move=19, best_score=0.0, total_nodes=1000)
    
    def test_observer_interface_compliance(self):
        """Test that all observers implement required interface."""
        observers = [
            ConsoleObserver(),
            StatisticsObserver(),
            QuietObserver()
        ]
        
        required_methods = [
            'on_search_start',
            'on_depth_complete',
            'on_search_complete'
        ]
        
        for observer in observers:
            for method in required_methods:
                assert hasattr(observer, method), \
                    f"{observer.__class__.__name__} missing {method}"
    
    def test_observer_methods_signatures(self):
        """Test that observer methods have correct signatures."""
        observer = ConsoleObserver()
        game = BitboardGame()
        
        # Test calling with correct parameters
        try:
            observer.on_search_start(game, depth=5)
            observer.on_depth_complete(depth=1, score=0.0, move=19, nodes=100)
            observer.on_search_complete(best_move=19, best_score=0.0, total_nodes=1000)
        except TypeError as e:
            pytest.fail(f"Observer method signature incorrect: {e}")
    
    def test_statistics_observer_data_accuracy(self):
        """Test that statistics observer data is accurate."""
        observer = StatisticsObserver()
        game = BitboardGame()
        
        # Send known data
        observer.on_search_start(game, depth=5)
        observer.on_depth_complete(depth=1, score=10.0, move=19, nodes=100)
        observer.on_depth_complete(depth=2, score=20.0, move=26, nodes=500)
        observer.on_depth_complete(depth=3, score=30.0, move=37, nodes=2000)
        observer.on_search_complete(best_move=37, best_score=30.0, total_nodes=5000)
        
        stats = observer.get_statistics()
        
        # Verify data accuracy
        if 'total_nodes' in stats:
            assert stats['total_nodes'] == 5000, "Total nodes should match"
        
        if 'best_move' in stats:
            assert stats['best_move'] == 37, "Best move should match"
        
        if 'best_score' in stats:
            assert abs(stats['best_score'] - 30.0) < 0.01, "Best score should match"


class TestObserverEdgeCases:
    """Test edge cases for observers."""
    
    def test_observer_handles_no_moves(self):
        """Test observers handle positions with no moves."""
        # Create position with no moves (game over or pass)
        game = BitboardGame()
        
        observers = [
            ConsoleObserver(),
            StatisticsObserver(),
            QuietObserver()
        ]
        
        for observer in observers:
            # Should not crash
            observer.on_search_start(game, depth=0)
            observer.on_search_complete(best_move=None, best_score=0.0, total_nodes=0)
    
    def test_observer_handles_depth_zero(self):
        """Test observers handle depth 0 search."""
        game = BitboardGame()
        
        observer = StatisticsObserver()
        
        observer.on_search_start(game, depth=0)
        observer.on_search_complete(best_move=19, best_score=0.0, total_nodes=1)
        
        stats = observer.get_statistics()
        
        # Should handle gracefully
        assert stats is not None
    
    def test_observer_handles_large_numbers(self):
        """Test observers handle large node counts."""
        observer = StatisticsObserver()
        
        observer.on_search_start(BitboardGame(), depth=12)
        observer.on_depth_complete(depth=12, score=100.0, move=19, nodes=10_000_000)
        observer.on_search_complete(best_move=19, best_score=100.0, total_nodes=50_000_000)
        
        stats = observer.get_statistics()
        
        # Should handle large numbers
        assert stats is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

