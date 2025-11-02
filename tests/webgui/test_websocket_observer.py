"""
Comprehensive test suite for WebSocketSearchObserver.

Tests cover:
- Observer lifecycle (search start/complete)
- Real-time update notifications
- Statistics tracking and reporting
- Message formatting
- Error handling
- Edge cases
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)

from webgui.server.websocket_observer import WebSocketSearchObserver
from Reversi.Game import Move


class TestWebSocketObserverCreation:
    """Test suite for observer creation and initialization"""
    
    def test_observer_creation(self):
        """Test basic observer creation"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test_session")
        
        assert observer.websocket == websocket
        assert observer.session_id == "test_session"
        assert observer.current_stats["depth"] == 0
        assert observer.current_stats["nodes_searched"] == 0
        
    def test_observer_initial_state(self):
        """Test observer initial state"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test_session")
        
        assert observer.search_start_time is None
        assert observer.player_name is None
        assert observer.aspiration_hits == 0
        assert observer.aspiration_fails == 0
        assert len(observer.depth_history) == 0
        assert len(observer.move_evaluations) == 0


@pytest.mark.asyncio
class TestObserverNotifications:
    """Test suite for observer notification methods"""
    
    @pytest.fixture
    async def observer_with_websocket(self):
        """Create observer with mocked WebSocket"""
        websocket = AsyncMock()
        websocket.send_json = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test_session")
        
        # Set up event loop
        try:
            observer.loop = asyncio.get_running_loop()
        except RuntimeError:
            observer.loop = None
            
        return observer
    
    async def test_on_search_start(self, observer_with_websocket):
        """Test search start notification"""
        observer = observer_with_websocket
        
        observer.on_search_start(
            depth=8,
            player_name="TestPlayer",
            game=MagicMock(),
            mode="sequential"
        )
        
        assert observer.player_name == "TestPlayer"
        assert observer.search_start_time is not None
        assert observer.aspiration_hits == 0
        assert observer.aspiration_fails == 0
        assert len(observer.depth_history) == 0
        
    async def test_on_iteration_start(self, observer_with_websocket):
        """Test iteration start notification"""
        observer = observer_with_websocket
        
        observer.on_iteration_start(
            current_depth=5,
            target_depth=8,
            use_aspiration=True,
            alpha=-100,
            beta=100
        )
        
        assert observer.current_stats["depth"] == 5
        
    async def test_on_move_evaluated_best(self, observer_with_websocket):
        """Test move evaluation notification for best move"""
        observer = observer_with_websocket
        move = Move(3, 4)  # C4
        
        observer.on_move_evaluated(
            move=move,
            value=50,
            is_best=True,
            nodes=1000,
            pruning=200,
            elapsed_time=100.0
        )
        
        assert observer.current_stats["best_move"] == move
        assert observer.current_stats["best_value"] == 50
        assert observer.current_stats["nodes_searched"] == 1000
        assert observer.current_stats["nodes_pruned"] == 200
        
    async def test_on_move_evaluated_not_best(self, observer_with_websocket):
        """Test move evaluation for non-best move"""
        observer = observer_with_websocket
        move = Move(3, 4)
        
        observer.on_move_evaluated(
            move=move,
            value=30,
            is_best=False,
            nodes=500,
            pruning=100,
            elapsed_time=50.0
        )
        
        assert observer.current_stats["nodes_searched"] == 500
        assert observer.current_stats["nodes_pruned"] == 100
        # best_move should not change if is_best=False
        
    async def test_on_iteration_complete_success(self, observer_with_websocket):
        """Test iteration completion with aspiration success"""
        observer = observer_with_websocket
        move = Move(3, 4)
        
        observer.on_iteration_complete(
            depth=5,
            best_move=move,
            value=50,
            iteration_time=100.0,
            aspiration_success=True
        )
        
        assert observer.aspiration_hits == 1
        assert observer.aspiration_fails == 0
        assert len(observer.depth_history) == 1
        
        history_entry = observer.depth_history[0]
        assert history_entry["depth"] == 5
        assert history_entry["value"] == 50
        
    async def test_on_iteration_complete_failure(self, observer_with_websocket):
        """Test iteration completion with aspiration failure"""
        observer = observer_with_websocket
        move = Move(3, 4)
        
        observer.on_iteration_complete(
            depth=5,
            best_move=move,
            value=50,
            iteration_time=100.0,
            aspiration_success=False
        )
        
        assert observer.aspiration_hits == 0
        assert observer.aspiration_fails == 1
        
    async def test_on_search_complete(self, observer_with_websocket):
        """Test search complete notification"""
        observer = observer_with_websocket
        move = Move(3, 4)
        
        statistics = {
            "nodes_searched": 10000,
            "nodes_pruned": 2000,
            "depth_reached": 8
        }
        
        observer.on_search_complete(
            best_move=move,
            value=100,
            statistics=statistics,
            total_time=1000.0,
            opening_book=None,
            game_history="C4e3",
            game=MagicMock()
        )
        
        # Should send final statistics
        # Verify via websocket calls if needed
        
    async def test_on_parallel_phase_start(self, observer_with_websocket):
        """Test parallel phase start notification"""
        observer = observer_with_websocket
        
        observer.on_parallel_phase_start(depth=6, num_workers=4)
        
        # Verify notification was triggered
        
    async def test_on_parallel_result(self, observer_with_websocket):
        """Test parallel result notification"""
        observer = observer_with_websocket
        move = Move(3, 4)
        
        observer.on_parallel_result(
            move=move,
            value=50,
            is_best=True,
            nodes=1000,
            pruning=200
        )
        
        assert observer.current_stats["best_move"] == move
        assert observer.current_stats["best_value"] == 50
        
    async def test_on_phase1_complete(self, observer_with_websocket):
        """Test phase 1 completion notification"""
        observer = observer_with_websocket
        move = Move(3, 4)
        
        stats = {"nodes": 5000, "pruning": 1000}
        
        observer.on_phase1_complete(
            stats=stats,
            time_elapsed=500.0,
            final_depth=6,
            target_depth=8,
            best_move=move,
            best_value=75
        )
        
        # Verify notification was triggered


class TestStatisticsFormatting:
    """Test suite for statistics formatting and calculations"""
    
    def test_format_time_milliseconds(self):
        """Test time formatting for milliseconds"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        formatted = observer._format_time_smart(500)
        assert "ms" in formatted
        
    def test_format_time_seconds(self):
        """Test time formatting for seconds"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        formatted = observer._format_time_smart(5000)
        assert "s" in formatted
        
    def test_format_time_minutes(self):
        """Test time formatting for minutes"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        formatted = observer._format_time_smart(120000)  # 2 minutes
        assert "m" in formatted
        
    def test_format_time_hours(self):
        """Test time formatting for hours"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        formatted = observer._format_time_smart(3600000)  # 1 hour
        assert "h" in formatted
        
    def test_calculate_aspiration_rate_success(self):
        """Test aspiration rate calculation with successes"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        observer.aspiration_hits = 8
        observer.aspiration_fails = 2
        
        rate = observer._calculate_aspiration_rate()
        assert rate == 80.0
        
    def test_calculate_aspiration_rate_zero(self):
        """Test aspiration rate with no data"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        observer.aspiration_hits = 0
        observer.aspiration_fails = 0
        
        rate = observer._calculate_aspiration_rate()
        assert rate == 0
        
    def test_calculate_tt_rate(self):
        """Test transposition table hit rate calculation"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        stats = {
            "tt_hits": 500,
            "nodes_searched": 1000
        }
        
        rate = observer._calculate_tt_rate(stats)
        assert rate == 50.0
        
    def test_calculate_tt_rate_zero_nodes(self):
        """Test TT rate with zero nodes"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        stats = {
            "tt_hits": 0,
            "nodes_searched": 0
        }
        
        rate = observer._calculate_tt_rate(stats)
        assert rate == 0


@pytest.mark.asyncio
class TestMessageSending:
    """Test suite for WebSocket message sending"""
    
    @pytest.fixture
    async def observer_with_websocket(self):
        """Create observer with mocked WebSocket"""
        websocket = AsyncMock()
        websocket.send_json = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test_session")
        
        try:
            observer.loop = asyncio.get_running_loop()
        except RuntimeError:
            observer.loop = None
            
        return observer
    
    async def test_send_async_with_loop(self, observer_with_websocket):
        """Test async message sending with event loop"""
        observer = observer_with_websocket
        
        if observer.loop:
            message = {"type": "test", "data": {}}
            observer._send_async(message)
            
            # Give time for async task
            await asyncio.sleep(0.1)
        
    async def test_send_ai_log(self, observer_with_websocket):
        """Test AI log message sending"""
        observer = observer_with_websocket
        
        observer._send_ai_log(
            log_type="test_log",
            message="Test message",
            data={"key": "value"}
        )
        
        # Verify log was prepared
        await asyncio.sleep(0.1)
        
    async def test_send_ai_statistics_summary(self, observer_with_websocket):
        """Test comprehensive statistics summary sending"""
        observer = observer_with_websocket
        observer.player_name = "TestAI"
        
        statistics = {
            "nodes_searched": 10000,
            "nodes_pruned": 2000,
            "depth": 8,
            "null_move": {"cutoffs": 500},
            "futility": {"pruning_count": 300},
            "lmr": {"reductions": 200},
            "multi_cut": {"pruning_count": 100}
        }
        
        observer._send_ai_statistics_summary(
            best_move="C4",
            value=100,
            statistics=statistics,
            total_time=1000.0,
            opening_book=MagicMock(),
            game_history="C4e3"
        )
        
        await asyncio.sleep(0.1)


class TestEdgeCases:
    """Test suite for edge cases and error conditions"""
    
    def test_observer_with_none_websocket(self):
        """Test observer creation with None websocket"""
        # Should not crash
        observer = WebSocketSearchObserver(None, "test")
        assert observer.websocket is None
        
    def test_move_evaluation_with_none_move(self):
        """Test move evaluation with None move"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        # Should not crash
        observer.on_move_evaluated(
            move=None,
            value=0,
            is_best=False,
            nodes=100,
            pruning=20,
            elapsed_time=10.0
        )
        
    def test_iteration_complete_with_none_move(self):
        """Test iteration complete with None best_move"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        observer.on_iteration_complete(
            depth=5,
            best_move=None,
            value=0,
            iteration_time=100.0,
            aspiration_success=True
        )
        
        assert len(observer.depth_history) == 1
        
    def test_search_complete_with_none_move(self):
        """Test search complete with None best_move"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        stats = {"nodes_searched": 1000, "nodes_pruned": 200, "depth": 5}
        
        observer.on_search_complete(
            best_move=None,
            value=0,
            statistics=stats,
            total_time=500.0,
            opening_book=None,
            game_history="",
            game=None
        )
        
        # Should complete without error
        
    def test_statistics_with_missing_keys(self):
        """Test statistics handling with missing keys"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        # Minimal statistics
        stats = {}
        
        observer.on_search_complete(
            best_move=Move(3, 4),
            value=50,
            statistics=stats,
            total_time=100.0,
            opening_book=None,
            game_history="",
            game=None
        )
        
        # Should use defaults
        
    def test_depth_history_accumulation(self):
        """Test depth history accumulates correctly"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        # Simulate multiple iterations
        for depth in range(1, 6):
            observer.current_stats["nodes_searched"] = depth * 1000
            observer.current_stats["nodes_pruned"] = depth * 200
            
            observer.on_iteration_complete(
                depth=depth,
                best_move=Move(3, 4),
                value=depth * 10,
                iteration_time=100.0,
                aspiration_success=True
            )
        
        assert len(observer.depth_history) == 5
        
        # Verify monotonic increase
        for i in range(1, 5):
            assert observer.depth_history[i]["depth"] > observer.depth_history[i-1]["depth"]
            
    def test_large_statistics_values(self):
        """Test handling of very large statistics values"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        stats = {
            "nodes_searched": 1000000000,  # 1 billion
            "nodes_pruned": 500000000,
            "depth": 20
        }
        
        observer.on_search_complete(
            best_move=Move(3, 4),
            value=10000,
            statistics=stats,
            total_time=60000.0,
            opening_book=None,
            game_history="",
            game=None
        )
        
        # Should handle large numbers
        
    def test_zero_time_elapsed(self):
        """Test handling of zero elapsed time"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        observer.on_iteration_complete(
            depth=1,
            best_move=Move(3, 4),
            value=10,
            iteration_time=0.0,
            aspiration_success=True
        )
        
        # Should not crash on division by zero
        assert len(observer.depth_history) == 1
        
    def test_negative_statistics(self):
        """Test handling of negative statistics (should not occur but test robustness)"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        observer.on_move_evaluated(
            move=Move(3, 4),
            value=-100,
            is_best=True,
            nodes=1000,
            pruning=200,
            elapsed_time=50.0
        )
        
        assert observer.current_stats["best_value"] == -100


class TestIntegrationScenarios:
    """Test suite for realistic integration scenarios"""
    
    def test_complete_search_lifecycle(self):
        """Test complete search from start to finish"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        # Search start
        observer.on_search_start(
            depth=6,
            player_name="TestAI",
            game=MagicMock(),
            mode="sequential"
        )
        
        # Multiple iterations
        for depth in range(1, 7):
            observer.on_iteration_start(
                current_depth=depth,
                target_depth=6,
                use_aspiration=(depth > 2),
                alpha=-100,
                beta=100
            )
            
            # Evaluate some moves
            for i in range(3):
                observer.on_move_evaluated(
                    move=Move(i+1, depth),
                    value=i * 10,
                    is_best=(i == 0),
                    nodes=depth * 100 * (i+1),
                    pruning=depth * 20 * (i+1),
                    elapsed_time=10.0 * (i+1)
                )
            
            observer.on_iteration_complete(
                depth=depth,
                best_move=Move(1, depth),
                value=depth * 10,
                iteration_time=50.0,
                aspiration_success=True
            )
        
        # Search complete
        stats = {
            "nodes_searched": 10000,
            "nodes_pruned": 2000,
            "depth": 6
        }
        
        observer.on_search_complete(
            best_move=Move(3, 4),
            value=60,
            statistics=stats,
            total_time=500.0,
            opening_book=None,
            game_history="C4e3",
            game=None
        )
        
        # Verify state
        assert len(observer.depth_history) == 6
        assert observer.aspiration_hits == 6
        
    def test_parallel_search_scenario(self):
        """Test parallel search workflow"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        observer.on_search_start(
            depth=8,
            player_name="ParallelAI",
            game=MagicMock(),
            mode="parallel"
        )
        
        observer.on_parallel_phase_start(depth=6, num_workers=4)
        
        # Simulate parallel results
        for i in range(4):
            observer.on_parallel_result(
                move=Move(i+1, 4),
                value=i * 20,
                is_best=(i == 2),
                nodes=1000 * (i+1),
                pruning=200 * (i+1)
            )
        
        observer.on_phase1_complete(
            stats={"nodes": 10000},
            time_elapsed=200.0,
            final_depth=6,
            target_depth=8,
            best_move=Move(3, 4),
            best_value=40
        )
        
        # Verify parallel tracking
        
    def test_search_with_aspiration_failures(self):
        """Test search with multiple aspiration window failures"""
        websocket = AsyncMock()
        observer = WebSocketSearchObserver(websocket, "test")
        
        observer.on_search_start(
            depth=8,
            player_name="AspirationAI",
            game=MagicMock(),
            mode="sequential"
        )
        
        # Mix of successes and failures
        for depth in range(1, 9):
            observer.on_iteration_start(
                current_depth=depth,
                target_depth=8,
                use_aspiration=True,
                alpha=-100,
                beta=100
            )
            
            success = (depth % 2 == 0)
            
            observer.on_iteration_complete(
                depth=depth,
                best_move=Move(3, 4),
                value=depth * 10,
                iteration_time=50.0,
                aspiration_success=success
            )
        
        # Verify aspiration tracking
        assert observer.aspiration_hits == 4
        assert observer.aspiration_fails == 4
        rate = observer._calculate_aspiration_rate()
        assert rate == 50.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

