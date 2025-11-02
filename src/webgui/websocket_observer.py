"""
WebSocket Observer for real-time search statistics.

Sends search progress updates to frontend during AI thinking.
"""

from typing import Any, Dict, Optional
import asyncio
from datetime import datetime

from AI.Apocalyptron.observers.interfaces import SearchObserver


class WebSocketSearchObserver(SearchObserver):
    """
    WebSocket observer that sends real-time search statistics to frontend.
    
    Notifies frontend about:
    - Search progress
    - Depth changes
    - Node counts
    - Pruning statistics
    - Move evaluations
    """

    def __init__(self, websocket, session_id: str):
        """
        Initialize WebSocket observer.
        
        Args:
            websocket: WebSocket connection to send updates
            session_id: Session ID for this connection
        """
        self.websocket = websocket
        self.session_id = session_id
        self.current_stats = {
            "depth": 0,
            "nodes_searched": 0,
            "nodes_pruned": 0,
            "best_move": None,
            "best_value": 0,
            "search_time": 0.0
        }
        self.loop = None
        self.search_start_time = None

    def _send_async(self, message: dict):
        """Send message via WebSocket in an async-safe way"""
        try:
            if self.loop and self.loop.is_running():
                asyncio.create_task(self._send(message))
            else:
                # Fallback for non-async contexts
                self.loop = asyncio.new_event_loop()
                self.loop.run_until_complete(self._send(message))
        except Exception as e:
            print(f"Error sending WebSocket update: {e}")

    async def _send(self, message: dict):
        """Send message via WebSocket"""
        try:
            await self.websocket.send_json(message)
        except Exception as e:
            print(f"Error in WebSocket send: {e}")
    
    def _send_ai_log(self, log_type: str, message: str, data: dict = None):
        """Send AI reasoning log to frontend"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_message = {
            "type": "ai_log",
            "data": {
                "timestamp": timestamp,
                "log_type": log_type,
                "message": message,
                "details": data or {}
            }
        }
        self._send_async(log_message)

    def on_search_start(
        self, depth: int, player_name: Optional[str], game: Any, mode: str = "sequential"
    ):
        """Search started"""
        self.search_start_time = datetime.now()
        self.current_stats = {
            "depth": 0,
            "nodes_searched": 0,
            "nodes_pruned": 0,
            "best_move": None,
            "best_value": 0,
            "search_time": 0.0
        }
        
        # Send AI log
        self._send_ai_log(
            "search_start",
            f"🎯 Starting search (target depth: {depth}, mode: {mode})",
            {"depth": depth, "player": player_name, "mode": mode}
        )
        
        message = {
            "type": "ai_thinking",
            "data": {
                "status": "Searching...",
                "depth": f"Starting depth {depth}",
                "nodes_searched": 0,
                "nodes_pruned": 0
            }
        }
        self._send_async(message)

    def on_iteration_start(
        self,
        current_depth: int,
        target_depth: int,
        use_aspiration: bool = False,
        alpha: int = 0,
        beta: int = 0,
    ):
        """Iteration started"""
        self.current_stats["depth"] = current_depth
        
        # Send AI log
        aspiration_info = f" [Aspiration: α={alpha}, β={beta}]" if use_aspiration else ""
        self._send_ai_log(
            "iteration_start",
            f"⚡ Depth {current_depth}/{target_depth}{aspiration_info}",
            {
                "depth": current_depth,
                "target_depth": target_depth,
                "aspiration": use_aspiration,
                "alpha": alpha,
                "beta": beta
            }
        )
        
        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Searching depth {current_depth}/{target_depth}",
                "depth": current_depth,
                "nodes_searched": self.current_stats.get("nodes_searched", 0),
                "nodes_pruned": self.current_stats.get("nodes_pruned", 0)
            }
        }
        self._send_async(message)

    def on_move_evaluated(
        self, move: Any, value: int, is_best: bool, nodes: int, pruning: int, elapsed_time: float
    ):
        """Move evaluated"""
        if is_best:
            self.current_stats["best_move"] = move
            self.current_stats["best_value"] = value
        
        self.current_stats["nodes_searched"] = nodes
        self.current_stats["nodes_pruned"] = pruning
        
        # Send detailed AI log for best moves
        if is_best:
            coord = None
            if move and hasattr(move, 'x') and hasattr(move, 'y'):
                coord = f"{chr(64+move.x)}{move.y}"
            
            pruning_ratio = (pruning / nodes * 100) if nodes > 0 else 0
            self._send_ai_log(
                "move_evaluated",
                f"📍 Move {coord or 'N/A'} → {value:+d} (nodes: {nodes:,}, pruned: {pruning:,}, {pruning_ratio:.1f}%, {elapsed_time:.1f}ms)",
                {
                    "move": coord,
                    "value": value,
                    "nodes": nodes,
                    "pruning": pruning,
                    "pruning_ratio": pruning_ratio,
                    "elapsed_time": elapsed_time,
                    "is_best": True
                }
            )
        
        # Send update every 100 nodes to avoid flooding
        if nodes % 100 == 0:
            message = {
                "type": "ai_thinking",
                "data": {
                    "status": "Evaluating moves...",
                    "depth": self.current_stats["depth"],
                    "nodes_searched": nodes,
                    "nodes_pruned": pruning,
                    "best_value": value if is_best else self.current_stats.get("best_value", 0)
                }
            }
            self._send_async(message)

    def on_iteration_complete(
        self,
        depth: int,
        best_move: Any,
        value: int,
        iteration_time: float,
        aspiration_success: bool = True,
    ):
        """Iteration completed"""
        self.current_stats["search_time"] += iteration_time
        
        coord = None
        if best_move:
            coord = f"{chr(64+best_move.x)}{best_move.y}"
        
        # Send AI log
        nodes = self.current_stats.get("nodes_searched", 0)
        pruned = self.current_stats.get("nodes_pruned", 0)
        aspiration_msg = " ✓" if aspiration_success else " ✗ (re-search)"
        
        self._send_ai_log(
            "iteration_complete",
            f"✓ Depth {depth} complete: {coord or 'N/A'} ({value:+d}) - {nodes:,} nodes, {pruned:,} pruned, {iteration_time:.1f}ms{aspiration_msg}",
            {
                "depth": depth,
                "best_move": coord,
                "value": value,
                "nodes": nodes,
                "pruned": pruned,
                "iteration_time": iteration_time,
                "aspiration_success": aspiration_success
            }
        )
        
        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Completed depth {depth}",
                "depth": depth,
                "selected_move": coord or "Analyzing...",
                "evaluation": value,
                "nodes_searched": self.current_stats.get("nodes_searched", 0),
                "nodes_pruned": self.current_stats.get("nodes_pruned", 0),
                "iteration_time": f"{iteration_time:.1f}ms"
            }
        }
        self._send_async(message)

    def on_search_complete(
        self,
        best_move: Any,
        value: int,
        statistics: Dict,
        total_time: float,
        opening_book: Any = None,
        game_history: str = None,
        game: Any = None,
    ):
        """Search completed"""
        coord = None
        if best_move:
            coord = f"{chr(64+best_move.x)}{best_move.y}"
        
        # Send final AI log with complete statistics
        nodes = statistics.get("nodes_searched", 0)
        pruned = statistics.get("nodes_pruned", 0)
        pruning_ratio = (pruned / nodes * 100) if nodes > 0 else 0
        final_depth = statistics.get("depth_reached", 0)
        
        self._send_ai_log(
            "search_complete",
            f"🏁 Search complete! Move: {coord or 'N/A'} ({value:+d}) | Depth: {final_depth} | Nodes: {nodes:,} | Pruned: {pruned:,} ({pruning_ratio:.1f}%) | Time: {total_time:.0f}ms",
            {
                "best_move": coord,
                "value": value,
                "depth": final_depth,
                "nodes_searched": nodes,
                "nodes_pruned": pruned,
                "pruning_ratio": pruning_ratio,
                "total_time": total_time,
                "statistics": statistics
            }
        )

    def on_parallel_phase_start(self, depth: int, num_workers: int):
        """Parallel phase started"""
        self._send_ai_log(
            "parallel_start",
            f"🔀 Starting parallel search: {num_workers} workers at depth {depth}",
            {"depth": depth, "workers": num_workers}
        )
        
        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Parallel search with {num_workers} workers",
                "depth": depth,
                "nodes_searched": self.current_stats.get("nodes_searched", 0)
            }
        }
        self._send_async(message)

    def on_parallel_result(self, move: Any, value: int, is_best: bool, nodes: int, pruning: int):
        """Parallel result received"""
        # Update stats but don't send every result
        pass

    def on_phase1_complete(
        self,
        stats: Dict,
        time_elapsed: float,
        final_depth: int,
        target_depth: int,
        best_move: Any = None,
        best_value: int = 0,
    ):
        """Phase 1 complete"""
        coord = None
        if best_move:
            coord = f"{chr(64+best_move.x)}{best_move.y}"
        
        self._send_ai_log(
            "phase_transition",
            f"🔄 Phase 1 → Phase 2: Depth {final_depth}/{target_depth}, Best: {coord or 'N/A'} ({best_value:+d}), Time: {time_elapsed:.2f}s",
            {
                "final_depth": final_depth,
                "target_depth": target_depth,
                "best_move": coord,
                "best_value": best_value,
                "time_elapsed": time_elapsed,
                "stats": stats
            }
        )
        
        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Phase 1 complete, moving to Phase 2",
                "depth": final_depth,
                "phase1_time": f"{time_elapsed:.1f}s"
            }
        }
        self._send_async(message)
