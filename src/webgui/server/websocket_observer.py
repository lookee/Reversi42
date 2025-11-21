"""
WebSocket Observer for real-time search statistics.

Sends search progress updates to frontend during AI thinking.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from AI.Apocalyptron.observers.interfaces import SearchObserver


class MoveEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts Move objects to strings"""

    def default(self, obj):
        # Check if this is a Move object (has x and y attributes)
        if hasattr(obj, "x") and hasattr(obj, "y"):
            return f"{chr(64+obj.x)}{obj.y}"
        # Let the base class handle everything else
        return super().default(obj)


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
        self.current_stats: Dict[str, Any] = {
            "depth": 0,
            "nodes_searched": 0,
            "nodes_pruned": 0,
            "best_move": None,
            "best_value": 0,
            "search_time": 0.0,
        }
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.search_start_time: Optional[datetime] = None
        self.player_name: Optional[str] = None
        self.aspiration_hits = 0
        self.aspiration_fails = 0
        # Track history for sparklines and charts
        self.depth_history: List[Dict[str, Any]] = []  # [(depth, time, nodes, value), ...]
        self.move_evaluations: List[Dict[str, Any]] = []  # [(move, value, nodes), ...]
        # Parallel search tracking
        self.parallel_results_count = 0
        self.parallel_total_moves = 0
        self.parallel_start_time: Optional[datetime] = None
        self.last_parallel_update: Optional[float] = None
        import time as time_module

        self.time_module = time_module

    def _send_async(self, message: dict):
        """Send message via WebSocket in an async-safe way"""
        try:
            # ALWAYS use run_coroutine_threadsafe for thread safety
            # This is crucial for parallel search which runs in worker threads
            if self.loop is not None and self.loop.is_running():
                # Use run_coroutine_threadsafe to schedule from ANY thread
                future = asyncio.run_coroutine_threadsafe(self._send(message), self.loop)
                # Don't wait - let messages queue up and send asynchronously
                # Waiting can cause deadlocks during parallel search
            else:
                # Fallback: try to get the running loop
                try:
                    loop = asyncio.get_running_loop()
                    future = asyncio.run_coroutine_threadsafe(self._send(message), loop)
                except Exception:
                    pass
        except Exception:
            pass

    async def _send(self, message: dict):
        """Send message via WebSocket using custom encoder for Move objects"""
        try:
            # Use custom encoder that handles Move objects automatically
            json_text = json.dumps(message, cls=MoveEncoder)
            await self.websocket.send_text(json_text)
        except Exception:
            pass

    def _send_ai_log(self, log_type: str, message: str, data: Optional[Dict[str, Any]] = None):
        """Send AI reasoning log to frontend"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_message = {
            "type": "ai_log",
            "data": {
                "timestamp": timestamp,
                "log_type": log_type,
                "message": message,
                "details": data or {},
            },
        }
        # Reduce logging noise - commented out
        # print(f"[AI_LOG] Sending: {log_type} - {message}")
        self._send_async(log_message)

    def on_search_start(
        self, depth: int, player_name: Optional[str], game: Any, mode: str = "sequential"
    ):
        """Search started"""
        self.search_start_time = datetime.now()
        self.player_name = player_name  # Store for statistics summary
        self.aspiration_hits = 0  # Reset counters
        self.aspiration_fails = 0
        self.depth_history = []  # Reset for new search
        self.move_evaluations = []
        # Reset stats (ensure no Move objects remain from previous search)
        self.current_stats = {
            "depth": 0,
            "nodes_searched": 0,
            "nodes_pruned": 0,
            "best_move": None,  # Will be string coordinate, never Move object
            "best_value": 0,
            "search_time": 0.0,
        }

        # Send AI log
        self._send_ai_log(
            "search_start",
            f"🎯 Starting search (target depth: {depth}, mode: {mode})",
            {"depth": depth, "player": player_name, "mode": mode},
        )

        message = {
            "type": "ai_thinking",
            "data": {
                "status": "Searching...",
                "depth": f"Starting depth {depth}",
                "nodes_searched": 0,
                "nodes_pruned": 0,
            },
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
                "beta": beta,
            },
        )

        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Searching depth {current_depth}/{target_depth}",
                "depth": current_depth,
                "nodes_searched": self.current_stats.get("nodes_searched", 0),
                "nodes_pruned": self.current_stats.get("nodes_pruned", 0),
            },
        }
        self._send_async(message)

    def on_move_evaluated(
        self, move: Any, value: int, is_best: bool, nodes: int, pruning: int, elapsed_time: float
    ):
        """Move evaluated"""
        # Convert move to coordinate string
        coord = None
        if move and hasattr(move, "x") and hasattr(move, "y"):
            coord = f"{chr(64+move.x)}{move.y}"

        if is_best:
            self.current_stats["best_move"] = coord  # Store as string, not Move object
            self.current_stats["best_value"] = value

        self.current_stats["nodes_searched"] = nodes
        self.current_stats["nodes_pruned"] = pruning

        # Send AI log for evaluated moves (filter trivial moves)

        pruning_ratio = (pruning / nodes * 100) if nodes > 0 else 0

        # Only log significant moves (> 50 nodes OR best move)
        # This filters out trivial book moves or shallow evaluations
        is_significant = is_best or nodes > 50

        if is_significant:
            best_marker = " ⭐ NEW BEST" if is_best else ""
            self._send_ai_log(
                "move_evaluated",
                f"📍 {coord or 'N/A'} → {value:+d} ({nodes:,} nodes, {pruning_ratio:.1f}% pruned, {elapsed_time:.0f}ms){best_marker}",
                {
                    "move": coord,
                    "value": value,
                    "nodes": nodes,
                    "pruning": pruning,
                    "pruning_ratio": pruning_ratio,
                    "elapsed_time": elapsed_time,
                    "is_best": is_best,
                },
            )

        # Send updates for significant moves (throttled by frontend to 1/sec anyway)
        # Update if: nodes changed significantly OR is best move
        if is_best or nodes % 10 == 0:
            message = {
                "type": "ai_thinking",
                "data": {
                    "status": "Evaluating moves...",
                    "depth": self.current_stats["depth"],
                    "depth_reached": self.current_stats["depth"],
                    "nodes_searched": nodes,
                    "nodes": nodes,
                    "nodes_pruned": pruning,
                    "pruning": pruning,
                    "search_time_ms": elapsed_time,
                    "time_ms": elapsed_time,
                    "best_value": value if is_best else self.current_stats.get("best_value", 0),
                },
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

        # Track aspiration window success/failure
        if aspiration_success:
            self.aspiration_hits += 1
        else:
            self.aspiration_fails += 1

        # Track iteration data for charts
        # IMPORTANT: These are CUMULATIVE values across all iterations so far
        nodes = self.current_stats.get("nodes_searched", 0) or 0
        pruned = self.current_stats.get("nodes_pruned", 0) or 0
        nps = (float(nodes) / (iteration_time / 1000.0)) if iteration_time > 0 else 0.0

        self.depth_history.append(
            {
                "depth": depth,
                "time": iteration_time,
                "nodes": nodes,  # CUMULATIVE
                "pruned": pruned,  # CUMULATIVE
                "nps": nps,
                "value": value,
                "aspiration_success": aspiration_success,
            }
        )

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
                "aspiration_success": aspiration_success,
            },
        )

        # Send statistics update after each iteration (frontend throttles to 1/sec)
        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Completed depth {depth}",
                "depth": depth,
                "depth_reached": depth,
                "selected_move": coord or "Analyzing...",
                "evaluation": value,
                "nodes_searched": nodes,
                "nodes": nodes,
                "nodes_pruned": pruned,
                "pruning": pruned,
                "search_time_ms": iteration_time,
                "time_ms": iteration_time,
                "total_time_ms": self.current_stats.get("search_time", 0),
            },
        }
        self._send_async(message)

    def on_search_complete(
        self,
        best_move: Any,
        value: int,
        statistics: Dict,
        total_time: float,
        opening_book: Any = None,
        game_history: Optional[str] = None,
        game: Any = None,
    ):
        """Search completed"""
        coord = None
        if best_move:
            coord = f"{chr(64+best_move.x)}{best_move.y}"

        # Try multiple keys for compatibility with different search engines
        # If depth_history exists, use the last iteration data
        nodes = statistics.get("nodes_searched", statistics.get("nodes", 0))
        pruned = statistics.get("nodes_pruned", statistics.get("pruning", 0))
        final_depth = statistics.get("depth_reached", statistics.get("depth", 0))

        # Fallback to depth_history if main stats are empty
        if nodes == 0 and len(self.depth_history) > 0:
            last_iter = self.depth_history[-1]
            nodes = last_iter.get("nodes", 0)
            pruned = last_iter.get("pruned", 0)
            final_depth = last_iter.get("depth", 0)

        # Final fallback to current_stats
        if nodes == 0:
            nodes = self.current_stats.get("nodes_searched", 0)
            pruned = self.current_stats.get("nodes_pruned", 0)
            final_depth = self.current_stats.get("depth", 0)

        pruning_ratio = (pruned / nodes * 100) if nodes > 0 else 0

        # total_time is already in milliseconds from the search engine
        # Format time intelligently (ms, s, m, h, d)
        time_str = self._format_time_smart(total_time)

        self._send_ai_log(
            "search_complete",
            f"🏁 Search complete! Move: {coord or 'N/A'} ({value:+d}) | Depth: {final_depth} | Nodes: {nodes:,} | Pruned: {pruned:,} ({pruning_ratio:.1f}%) | Time: {time_str}",
            {
                "best_move": coord,
                "value": value,
                "depth": final_depth,
                "nodes_searched": nodes,
                "nodes_pruned": pruned,
                "pruning_ratio": pruning_ratio,
                "total_time": total_time,
                "statistics": statistics,
            },
        )

        # Send comprehensive AI statistics for data science dashboard
        self._send_ai_statistics_summary(
            best_move=coord,
            value=value,
            statistics=statistics,
            total_time=total_time,
            opening_book=opening_book,
            game_history=game_history,
        )

    def _send_ai_statistics_summary(
        self, best_move, value, statistics, total_time, opening_book, game_history
    ):
        """Send comprehensive statistics summary for data science dashboard"""
        # Extract basic stats - TRY BOTH KEYS (parallel uses nodes_searched, sequential uses nodes)
        nodes = statistics.get("nodes_searched", statistics.get("nodes", 0))
        pruned = statistics.get("nodes_pruned", statistics.get("pruning", 0))

        pruning_ratio = (pruned / nodes * 100) if nodes > 0 else 0
        nps = (nodes / (total_time / 1000.0)) if total_time > 0 else 0

        # Extract optimization statistics from nested objects
        null_move_stats = statistics.get("null_move", {})
        futility_stats = statistics.get("futility", {})
        lmr_stats = statistics.get("lmr", {})
        multi_cut_stats = statistics.get("multi_cut", {})

        # Extract counts from nested stats
        null_move_cuts = (
            null_move_stats.get("cutoffs", 0) if isinstance(null_move_stats, dict) else 0
        )
        futility_cuts = (
            futility_stats.get("pruning_count", 0) if isinstance(futility_stats, dict) else 0
        )
        lmr_reductions = lmr_stats.get("reductions", 0) if isinstance(lmr_stats, dict) else 0
        multi_cut_prunes = (
            multi_cut_stats.get("pruning_count", 0) if isinstance(multi_cut_stats, dict) else 0
        )

        # Get depth info
        depth_reached = statistics.get("depth", statistics.get("depth_reached", 0))

        summary = {
            "type": "ai_statistics_summary",
            "data": {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "player_name": self.player_name or "AI",
                "player_description": (
                    f"{self.player_name} - High-performance AI engine with alpha-beta search and advanced pruning"
                    if self.player_name
                    else None
                ),
                # Move info
                "best_move": best_move,
                "evaluation": value,
                # Performance metrics
                "total_time_ms": round(total_time, 2),
                "search_time_ms": round(total_time, 2),  # Add for consistency
                "time_ms": round(total_time, 2),  # Add for consistency
                "total_time_s": round(total_time / 1000.0, 3),
                "nodes_per_second": int(nps),
                # Search depth
                "depth_reached": depth_reached,
                "depth": depth_reached,  # Add for consistency
                "target_depth": statistics.get("target_depth", depth_reached),
                # Node statistics
                "nodes_searched": nodes,
                "nodes": nodes,  # Add for consistency
                "nodes_pruned": pruned,
                "pruning": pruned,  # Add for consistency
                "nodes_evaluated": nodes - pruned,
                "pruning_efficiency": round(pruning_ratio, 2),
                # Optimizations breakdown (extracted from nested objects)
                "null_move_cuts": null_move_cuts,
                "futility_cuts": futility_cuts,
                "lmr_reductions": lmr_reductions,
                "multi_cut_prunes": multi_cut_prunes,
                # Optimization enabled flags (detect from stats presence)
                "null_move_enabled": null_move_cuts > 0 or isinstance(null_move_stats, dict),
                "futility_enabled": futility_cuts > 0 or isinstance(futility_stats, dict),
                "lmr_enabled": lmr_reductions > 0 or isinstance(lmr_stats, dict),
                "multi_cut_enabled": multi_cut_prunes > 0 or isinstance(multi_cut_stats, dict),
                "aspiration_enabled": True,  # Always enabled in Apocalyptron
                "tt_enabled": statistics.get("tt_hits", 0) > 0 or statistics.get("tt_size", 0) > 0,
                "killer_enabled": statistics.get("killer_moves", 0) > 0,
                "history_enabled": statistics.get("history_entries", 0) > 0,
                "parallel_enabled": statistics.get("parallel_workers", 0) > 0
                or statistics.get("parallel_mode") == "active",
                "book_enabled": opening_book is not None,
                # Parallel search info
                "parallel_threads": statistics.get("parallel_workers", 0),
                "parallel_tasks": statistics.get("parallel_tasks", 0),
                # Opening book info
                "book_hits": 1 if opening_book else 0,
                # Aspiration windows (from observer tracking)
                "aspiration_hits": statistics.get("aspiration_hits", self.aspiration_hits),
                "aspiration_fails": statistics.get("aspiration_fails", self.aspiration_fails),
                "aspiration_success_rate": self._calculate_aspiration_rate(),
                # Iterative deepening info
                "iterations_completed": depth_reached,
                "avg_iteration_time": round(total_time / max(1, depth_reached), 2),
                # Move ordering effectiveness
                "pv_move_hits": statistics.get("pv_hits", 0),
                "killer_move_hits": statistics.get("killer_moves", 0),
                "history_entries": statistics.get("history_entries", 0),
                # Transposition table
                "tt_hits": statistics.get("tt_hits", 0),
                "tt_size": statistics.get("tt_size", 0),
                "tt_hit_rate": self._calculate_tt_rate(statistics),
                # Chart data for visualizations
                "depth_history": self.depth_history,  # For iteration timeline
                "move_evaluations": self.move_evaluations,  # For move distribution
                # Full statistics object
                "raw_statistics": statistics,
            },
        }

        # Store for aspiration tracking
        if hasattr(self, "search_stats"):
            self.search_stats = summary["data"]

        self._send_async(summary)

    def _calculate_aspiration_rate(self):
        """Calculate aspiration window success rate"""
        hits = getattr(self, "aspiration_hits", 0)
        fails = getattr(self, "aspiration_fails", 0)
        total = hits + fails
        return round((hits / total * 100), 1) if total > 0 else 0

    def _calculate_tt_rate(self, statistics):
        """Calculate transposition table hit rate"""
        tt_hits = statistics.get("tt_hits", 0)
        nodes = statistics.get("nodes_searched", 1)
        return round((tt_hits / nodes * 100), 2) if nodes > 0 else 0

    def _format_time_smart(self, ms):
        """Format time with appropriate unit (ms, s, m, h, d)"""
        if ms < 1000:
            return f"{ms:.0f}ms"
        s = ms / 1000
        if s < 60:
            return f"{s:.1f}s" if s < 10 else f"{s:.0f}s"
        m = int(s / 60)
        rem_s = int(s % 60)
        if m < 60:
            return f"{m}m {rem_s:02d}s"
        h = int(m / 60)
        rem_m = m % 60
        if h < 24:
            return f"{h}h {rem_m:02d}m"
        d = int(h / 24)
        rem_h = h % 24
        return f"{d}d {rem_h:02d}h"

    def on_parallel_phase_start(self, depth: int, num_workers: int):
        """Parallel phase started"""
        # Store parallel phase start time for accurate NPS calculation
        self.parallel_start_time = datetime.now()
        self.parallel_results_count = 0
        self.last_parallel_update = self.time_module.time()

        # IMPORTANT: Store depth in current_stats so on_parallel_result can access it
        self.current_stats["depth"] = depth

        self._send_ai_log(
            "parallel_start",
            f"🔀 Starting parallel search: {num_workers} workers at depth {depth}",
            {"depth": depth, "workers": num_workers},
        )

        # Calculate current stats from Phase 1
        nodes = self.current_stats.get("nodes_searched", 0)
        pruned = self.current_stats.get("nodes_pruned", 0)
        elapsed_time: float = 0.0
        nps = 0
        if self.search_start_time:
            elapsed_time = (datetime.now() - self.search_start_time).total_seconds() * 1000.0
            nps = int((nodes * 1000) / elapsed_time) if elapsed_time > 0 else 0

        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Parallel search with {num_workers} workers",
                "depth": depth,
                "depth_reached": depth,
                "nodes_searched": nodes,
                "nodes": nodes,
                "nodes_pruned": pruned,
                "pruning": pruned,
                "search_time_ms": elapsed_time,
                "time_ms": elapsed_time,
                "total_time_ms": elapsed_time,
                "nodes_per_second": nps,
                "parallel_mode": True,
                "parallel_workers": num_workers,
            },
        }
        self._send_async(message)

    def on_parallel_result(self, move: Any, value: int, is_best: bool, nodes: int, pruning: int):
        """Parallel result received

        NOTE: nodes and pruning are CUMULATIVE totals for parallel phase only
        They DO NOT include Phase 1 nodes
        """
        # Convert move to coordinate string
        coord = None
        if move and hasattr(move, "x") and hasattr(move, "y"):
            coord = f"{chr(64+move.x)}{move.y}"

        # Update stats - these are cumulative for parallel phase
        self.current_stats["nodes_searched"] = nodes
        self.current_stats["nodes_pruned"] = pruning
        self.parallel_results_count += 1

        if is_best:
            self.current_stats["best_move"] = coord  # Store as string, not Move object
            self.current_stats["best_value"] = value

        # Send AI log for parallel results

        pruning_ratio = (pruning / nodes * 100) if nodes > 0 else 0
        best_marker = " ⭐ BEST" if is_best else ""

        # Calculate elapsed time for PARALLEL PHASE ONLY
        parallel_elapsed: float = 0.0
        if hasattr(self, "parallel_start_time") and self.parallel_start_time:
            parallel_elapsed = (datetime.now() - self.parallel_start_time).total_seconds() * 1000.0

        # Calculate NPS for parallel phase
        nps = int((nodes * 1000) / parallel_elapsed) if parallel_elapsed > 0 else 0

        self._send_ai_log(
            "move_evaluated",
            f"🔀 Parallel: {coord or 'N/A'} → {value:+d} ({nodes:,} nodes, {pruning_ratio:.1f}% pruned){best_marker}",
            {
                "move": coord,
                "value": value,
                "nodes": nodes,
                "pruning": pruning,
                "pruning_ratio": pruning_ratio,
                "is_best": is_best,
                "parallel": True,
            },
        )

        # ALWAYS send updates during parallel (every result is valuable)
        # IMPORTANT: Send ai_thinking message with statistics for LIVE UPDATE
        # Use parallel phase stats only (more accurate for parallel search)
        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Parallel: {self.parallel_results_count} moves evaluated",
                "depth": self.current_stats.get("depth", 0),
                "depth_reached": self.current_stats.get("depth", 0),
                "nodes_searched": nodes,
                "nodes": nodes,
                "nodes_pruned": pruning,
                "pruning": pruning,
                "search_time_ms": parallel_elapsed,
                "time_ms": parallel_elapsed,
                "total_time_ms": parallel_elapsed,
                "nodes_per_second": nps,
                "best_move": coord,
                "best_value": value if is_best else self.current_stats.get("best_value", 0),
                "parallel_mode": True,
                "parallel_progress": self.parallel_results_count,
            },
        }

        # Send message immediately (non-blocking)
        self._send_async(message)

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
                "stats": stats,
            },
        )

        message = {
            "type": "ai_thinking",
            "data": {
                "status": f"Phase 1 complete, moving to Phase 2",
                "depth": final_depth,
                "phase1_time": f"{time_elapsed:.1f}s",
            },
        }
        self._send_async(message)
