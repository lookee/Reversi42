#!/usr/bin/env python3
"""
WebGUI Backend Server - WebSocket Bridge for Reversi42
Enables real-time gameplay between web frontend and game engine

Usage:
    python -m src.webgui.backend_server --port 8000 --player DIVZERO.EXE
"""

import sys
import os
import logging
import traceback
import signal
import atexit
from datetime import datetime
from typing import Dict, Optional, Tuple

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(src_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, project_root)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, Response
import asyncio
import json
import argparse
from typing import Dict, Set, Optional
from dataclasses import dataclass, asdict

# Import game engine
from Reversi.Game import Game, Move
from Players.PlayerFactory import PlayerFactory
from Players.Gladiators.PlayerDivZero import PlayerDivZero

# Import WebSocket observer for AI insights
from webgui.server.websocket_observer import WebSocketSearchObserver

# Import version
try:
    from __version__ import __version__
except ImportError:
    __version__ = "3.2.0"  # Fallback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/backend_detailed.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global variables for graceful shutdown
app_instance = None
active_connections = set()
shutdown_event = asyncio.Event()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    logger.info(f"Active connections: {len(active_connections)}, Active sessions: {len(sessions)}")
    shutdown_event.set()

def cleanup_on_exit():
    """Cleanup function called on exit"""
    logger.info("Backend server shutting down...")
    # Close all active WebSocket connections
    for websocket in active_connections.copy():
        try:
            asyncio.create_task(websocket.close())
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

# Register signal handlers and cleanup
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(cleanup_on_exit)


@dataclass
class GameState:
    """Represents the current game state"""
    game: Game
    ai_player: any  # Player instance
    player_name: str
    ai_name: str
    current_turn: str  # 'B' or 'W'
    game_over: bool = False
    winner: str = None
    

class GameSession:
    """Manages a single game session"""
    
    def __init__(self, session_id: str, ai_player_name: str = "DIVZERO.EXE"):
        try:
            self.session_id = session_id
            # Default: AI plays White; Black is Human
            self.ai_white_name = ai_player_name
            self.ai_black_name = None
            # Backwards-compat shadow (used in some logs)
            self.ai_player_name = ai_player_name
            self.game = Game(8)
            self.last_ai_stats = {}  # Store last AI analysis
            self.error_count = 0  # Track consecutive errors
            self.max_errors = 5  # Max errors before session reset
            self.last_error_time = None
            
            # Create AI players (only for configured sides)
            self.ai_white = None
            self.ai_black = None
            if self.ai_white_name:
                if self.ai_white_name == "DIVZERO.EXE":
                    self.ai_white = PlayerDivZero(depth=6)
                else:
                    self.ai_white = PlayerFactory.create_player(self.ai_white_name)
            if self.ai_black_name:
                if self.ai_black_name == "DIVZERO.EXE":
                    self.ai_black = PlayerDivZero(depth=6)
                else:
                    self.ai_black = PlayerFactory.create_player(self.ai_black_name)
            
            logger.info(f"Created game session {session_id} with AI {ai_player_name}")
            
        except Exception as e:
            logger.error(f"Failed to create game session {session_id}: {e}")
            logger.error(traceback.format_exc())
            raise
        
        # Player instances do not need explicit color; we check side before moving
    
    def handle_error(self, error: Exception, context: str = ""):
        """Handle errors and potentially reset session if too many occur"""
        self.error_count += 1
        self.last_error_time = datetime.now()
        
        logger.error(f"Error in session {self.session_id} ({context}): {error}")
        logger.error(traceback.format_exc())
        
        # If too many errors, reset the session
        if self.error_count >= self.max_errors:
            logger.warning(f"Too many errors ({self.error_count}) in session {self.session_id}, resetting...")
            try:
                self.reset_session()
                self.error_count = 0
                logger.info(f"Session {self.session_id} reset successfully")
            except Exception as reset_error:
                logger.error(f"Failed to reset session {self.session_id}: {reset_error}")
                raise
    
    def reset_session(self):
        """Reset the game session to initial state"""
        try:
            self.game = Game(8)
            # Recreate AI instances based on current config
            self.ai_white = None
            self.ai_black = None
            if self.ai_white_name:
                if self.ai_white_name == "DIVZERO.EXE":
                    self.ai_white = PlayerDivZero(depth=6)
                else:
                    self.ai_white = PlayerFactory.create_player(self.ai_white_name)
            if self.ai_black_name:
                if self.ai_black_name == "DIVZERO.EXE":
                    self.ai_black = PlayerDivZero(depth=6)
                else:
                    self.ai_black = PlayerFactory.create_player(self.ai_black_name)
            self.last_ai_stats = {}
            logger.info(f"Session {self.session_id} reset to initial state")
        except Exception as e:
            logger.error(f"Failed to reset session {self.session_id}: {e}")
            raise
    
    def _count_opening_sequences(self, opening_book, sequence):
        """Count how many opening sequences contain the given sequence"""
        count = 0
        sequence_upper = sequence.upper()
        
        # Check all opening names
        for full_sequence, name in opening_book.opening_names.items():
            full_sequence_upper = full_sequence.upper()
            # If this opening's sequence starts with our sequence
            if full_sequence_upper.startswith(sequence_upper):
                count += 1
        
        return count
    
    def _get_opening_book(self):
        """Return opening_book from active AI (prefer current turn), if any."""
        try:
            ai = None
            if self.game.turn == 'W' and self.ai_white and hasattr(self.ai_white, 'opening_book'):
                ai = self.ai_white
            elif self.game.turn == 'B' and self.ai_black and hasattr(self.ai_black, 'opening_book'):
                ai = self.ai_black
            elif self.ai_white and hasattr(self.ai_white, 'opening_book'):
                ai = self.ai_white
            elif self.ai_black and hasattr(self.ai_black, 'opening_book'):
                ai = self.ai_black
            return ai.opening_book if ai else None
        except Exception:
            return None

    def _build_opening_tree(self, max_depth: int = 3, max_children: int = 6) -> Optional[dict]:
        """Build a compact opening tree from current position using the AI opening book.

        The structure returned is tailored for UI rendering and limited in depth/width.
        """
        try:
            book = self._get_opening_book()
            if not book:
                return None

            history = self.game.history or ""

            # Build PATH-ONLY opening tree: show only the moves actually played, no alternative variants
            history_moves = book._parse_move_sequence(history)

            # Helper: collect compact info (variants count + top names) for a given sequence
            def collect_info_for_sequence(seq_upper: str):
                variants = self._count_opening_sequences(book, seq_upper)
                names = []
                openings_info = []
                for full_seq, nm in book.opening_names.items():
                    if full_seq.upper().startswith(seq_upper):
                        names.append(nm)
                        openings_info.append({"name": nm})
                        if len(names) >= 3 and len(openings_info) >= 8:
                            break
                return variants, names, openings_info

            # Next VALID book moves from current position (compact list with names)
            # Compute valid moves for current player as coordinates
            valid_coords = set(f"{chr(64+m.x)}{m.y}" for m in self.game.get_move_list())

            # Navigate the trie to current history
            node = book.root
            for mv in history_moves:
                up = mv.upper()
                if up not in node.children:
                    node = None
                    break
                node = node.children[up]

            children: list = []
            if node is not None:
                book_next = book.get_book_moves(history)
                for mv in book_next or []:
                    coord = f"{chr(64+mv.x)}{mv.y}"
                    if coord not in valid_coords:
                        continue
                    # Extend sequence respecting turn
                    move_with_turn = coord if self.game.turn == 'B' else coord.lower()
                    ext_seq = (history or "") + move_with_turn
                    variants, names, opens = collect_info_for_sequence(ext_seq.upper())
                    children.append({
                        "move": coord,
                        "variants": variants,
                        "names": names,
                        "openings": opens,
                        "children": []
                    })

            # Compute current opening (flexible): prefer the longest line whose sequence is a prefix of history (token-aware)
            current_opening = None
            try:
                # Exact match first
                current_opening = book.get_current_opening_name(history)
                if not current_opening and history:
                    # Compare by token (two-char moves), not raw string length
                    hist_tokens = book._parse_move_sequence(history)
                    best_len = -1
                    for seq, name in book.opening_names.items():
                        seq_tokens = book._parse_move_sequence(seq)
                        # seq_tokens must be a prefix of hist_tokens
                        if len(seq_tokens) == 0 or len(seq_tokens) > len(hist_tokens):
                            continue
                        is_prefix = True
                        for i in range(len(seq_tokens)):
                            if seq_tokens[i].upper() != hist_tokens[i].upper():
                                is_prefix = False
                                break
                        if is_prefix and len(seq_tokens) > best_len:
                            current_opening = name
                            best_len = len(seq_tokens)
                # Fallback: if we left the book, show the closest earlier opening (max common prefix)
                if not current_opening and history:
                    hist_tokens = book._parse_move_sequence(history)
                    best_score = -1
                    best_name = None
                    for seq, name in book.opening_names.items():
                        seq_tokens = book._parse_move_sequence(seq)
                        k = 0  # common prefix length in tokens
                        for a, b in zip(hist_tokens, seq_tokens):
                            if a.upper() == b.upper():
                                k += 1
                            else:
                                break
                        if k > best_score:
                            best_score = k
                            best_name = name
                    current_opening = best_name if best_score > 0 else None
            except Exception:
                current_opening = None

            # Names reachable from here
            names_at_position = []
            try:
                names_at_position = book.get_remaining_openings(history) or []
            except Exception:
                names_at_position = []

            tree = {
                "path": [m.upper() for m in history_moves],
                "children": children,
                "current_opening": current_opening,
                "names_at_position": names_at_position
            }
            return tree
        except Exception as e:
            logger.warning(f"Could not build opening tree: {e}")
            return None
        
    def get_state(self) -> dict:
        """Get current game state as dictionary in the format expected by the frontend"""
        game = self.game
        
        # Convert board to coordinate format
        positions = {}
        for y in range(1, 9):  # 1-8 (Game uses 1-indexed with border)
            for x in range(1, 9):
                coord = f"{chr(64+x)}{y}"  # A1-H8
                pos = game.matrix[y][x]
                positions[coord] = pos
        
        # Get move history from game.history (string format)
        moves = []
        # game.history is a string with moves like "C4e3D3" (uppercase=black, lowercase=white)
        history = game.history or ""
        if history:
            # Convert string to individual moves
            import re
            # Extract all moves in order (both uppercase and lowercase)
            all_moves = re.findall(r'[A-Za-z][0-9]', history)
            for move in all_moves:
                moves.append(move.upper())  # Always uppercase for display
        
        # Get valid moves for current player from the engine
        valid_moves = []
        move_list = game.get_move_list()
        for move in move_list:
            coord = f"{chr(64+move.x)}{move.y}"
            valid_moves.append(coord)
        
        # Get opening book moves with variant count (filtered to VALID moves)
        opening_moves = []
        book = self._get_opening_book()
        if book:
            try:
                book_moves = book.get_book_moves(history)
                if book_moves:
                    # Navigate to current position in the book
                    history_moves = book._parse_move_sequence(history)
                    node = book.root
                    for move_str in history_moves:
                        normalized = move_str.upper()
                        if normalized not in node.children:
                            break
                        node = node.children[normalized]
                    
                    # Precompute valid move coordinates based on the list we already exposed to frontend
                    # This guarantees perfect alignment with 'valid_by_ply'
                    valid_coords = set(valid_moves)

                    # For each book move that is currently VALID, count how many opening sequences continue
                    for move_obj in book_moves:
                        # Only include if move is valid now (coordinate-based to avoid equality issues)
                        coord = f"{chr(64+move_obj.x)}{move_obj.y}"
                        if coord not in valid_coords:
                            logger.info(f"Skipping book move not valid now: {coord}; valid={sorted(valid_coords)}")
                            continue
                        # Extra safety: confirm with engine validator
                        try:
                            if not self.game.valid_move(Move(move_obj.x, move_obj.y)):
                                continue
                        except Exception:
                            continue
                        move_str = coord
                        
                        # Check if this move exists in the book
                        if move_str in node.children:
                            next_node = node.children[move_str]
                            # Build the sequence after this move: history + move
                            # Turns alternate: B plays uppercase, W plays lowercase
                            move_with_turn = move_str if game.turn == 'B' else move_str.lower()
                            extended_sequence = history + move_with_turn
                            
                            # Count how many opening names contain this extended sequence
                            variant_count = self._count_opening_sequences(book, extended_sequence)
                        else:
                            variant_count = 0
                        
                        opening_moves.append({
                            "move": coord,
                            "variants": variant_count
                        })
            except Exception as e:
                logger.warning(f"Could not get opening book moves: {e}")
        
        # Use last AI stats for notes if available
        notes = self.last_ai_stats if self.last_ai_stats else {"title": "Notes"}
        
        # Opening tree (limited, UI-friendly)
        opening_tree = None
        try:
            opening_tree = self._build_opening_tree(max_depth=3, max_children=6)
        except Exception as e:
            logger.warning(f"Opening tree error: {e}")
        
        return {
            "meta": {
                "variant": "Reversi/Othello",
                "size": 8
            },
            "players": {
                "black": {
                    "name": (self.ai_black_name or "Human"),
                    "avatar": (self.ai_black_name[:2].upper() if self.ai_black_name else "HM")
                },
                "white": {
                    "name": (self.ai_white_name or "Human"),
                    "avatar": (self.ai_white_name[:2].upper() if self.ai_white_name else "HM")
                }
            },
            "status": {
                "turn_by_ply": [game.turn],
                "can_undo": len(game.board_position_stack) > 0,
                "can_redo": len(getattr(game, 'redo_stack', [])) > 0
            },
            "positions": [positions],
            "moves": moves,
            "history_compact": history,
            "valid_by_ply": [valid_moves],
            "opening_by_ply": opening_moves,
            "opening_tree": opening_tree,
            "notes": notes
        }
    
    def make_move(self, move_coord: str) -> Tuple[bool, str]:
        """Make a move and return (success, error_message)"""
        try:
            # Convert algebraic notation (A1-H8) to Move object
            if len(move_coord) != 2:
                return False, "Invalid move format"
            
            col = ord(move_coord[0]) - ord('A') + 1  # A=1, B=2, etc.
            row = int(move_coord[1])  # 1-8
            
            logger.info(f"Converting move {move_coord} to col={col}, row={row}")
            
            if not (1 <= col <= 8 and 1 <= row <= 8):
                return False, "Move out of bounds"
            
            # Move constructor is Move(y, x) where y is row and x is col
            # But in algebraic notation, A1 means col=A, row=1
            # So for C4: col=C(3), row=4 -> Move(row=4, col=3) which is D3!
            # We need to swap them: Move(col=3, row=4) = Move(3, 4)
            move = Move(col, row)
            
            # Check if move is valid
            valid_moves = self.game.get_move_list()
            logger.info(f"Valid moves (y,x): {[(m.y, m.x) for m in valid_moves]}")
            logger.info(f"Attempted move {move_coord}: Move(col={col}, row={row}) = Move(y={col}, x={row})")
            
            if move not in valid_moves:
                return False, "Invalid move"
            
            # Make the move
            self.game.move(move)
            logger.info(f"Move {move_coord} executed successfully")
            return True, None
            
        except Exception as e:
            logger.error(f"Error making move {move_coord}: {e}")
            logger.error(traceback.format_exc())
            return False, str(e)
    
    def get_ai_move(self, side: str, websocket: WebSocket = None) -> Move:
        """Get AI move for side 'B' or 'W'"""
        try:
            move_list = self.game.get_move_list()
            if not move_list:
                return None
            
            # Select AI by side
            ai = self.ai_white if side == 'W' else self.ai_black
            if ai is None:
                return None
            
            # Create observer for AI insights if websocket is provided
            observer = None
            if websocket:
                logger.info("[AI_INSIGHT] Creating WebSocketSearchObserver for AI insights")
                observer = WebSocketSearchObserver(websocket, self.session_id)
                # Set the event loop for async operations
                try:
                    observer.loop = asyncio.get_running_loop()
                    logger.info(f"[AI_INSIGHT] Observer loop set: {observer.loop}")
                except RuntimeError:
                    observer.loop = None
                    logger.warning("[AI_INSIGHT] No running event loop found for observer")
            else:
                logger.info("[AI_INSIGHT] No websocket provided, observer not created")
            
            logger.info(f"[AI_INSIGHT] Calling AI.get_move with observer={observer}")
            ai_move = ai.get_move(self.game, move_list, observer)
            logger.info(f"[AI_INSIGHT] AI.get_move completed, move={ai_move}")
            return ai_move
            
        except Exception as e:
            logger.error(f"Error getting AI move: {e}")
            logger.error(traceback.format_exc())
            raise


# Global session storage
sessions: Dict[str, GameSession] = {}
active_connections: Dict[str, WebSocket] = {}

# FastAPI app
app = FastAPI(
    title="Reversi42 WebSocket Backend",
    version=__version__,
    description="Ultra-Fast Reversi (Othello) with Bitboard AI and Opening Book Learning",
    contact={
        "name": "Luca Amore",
        "url": "https://www.lucaamore.com",
        "email": "luca.amore@gmail.com"
    },
    license_info={
        "name": "GPL-3.0-or-later",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html"
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_index():
    """Serve the main game page"""
    try:
        html_file = os.path.join(current_dir, "game_websocket.html")
        if os.path.exists(html_file):
            return FileResponse(html_file)
        else:
            return HTMLResponse("<h1>Game file not found</h1>", status_code=404)
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return HTMLResponse("<h1>Server Error</h1>", status_code=500)

@app.get("/stats")
async def get_stats():
    """Get server statistics"""
    return {
        "version": __version__,
        "active_sessions": len(sessions),
        "active_connections": len(active_connections),
        "uptime": "N/A"  # Could implement uptime tracking
    }

@app.get("/version")
async def get_version():
    """Get server version"""
    return {
        "version": __version__,
        "name": "Reversi42",
        "description": "Ultra-Fast Reversi (Othello) with Bitboard AI"
    }

@app.get("/logs")
async def get_logs():
    """Get server logs"""
    try:
        log_file = '/tmp/backend_detailed.log'
        if os.path.exists(log_file):
            # Return last 500 lines
            with open(log_file, 'r') as f:
                lines = f.readlines()
                content = '\n'.join(lines[-500:]) if len(lines) > 500 else '\n'.join(lines)
                return Response(content=content, media_type="text/plain")
        else:
            return Response(content="No logs available yet", media_type="text/plain")
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return Response(content=f"Error reading logs: {str(e)}", media_type="text/plain")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    session_id = "default"  # For now, use single session
    
    logger.info(f"WebSocket connection accepted for session {session_id}")
    active_connections[session_id] = websocket
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            logger.info(f"Received WebSocket message: {data}")
            message = json.loads(data)
            logger.info(f"Parsed message: {message}")
            
            # Handle message
            await handle_message(websocket, session_id, message)
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected from session {session_id} (client closed connection)")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        logger.error(traceback.format_exc())
    finally:
        # Cleanup
        if session_id in active_connections:
            del active_connections[session_id]
            logger.info(f"Removed WebSocket connection for session {session_id}")
        # DON'T delete the session - keep it alive for reconnection
        # Only cleanup session if it's been idle for too long
        logger.info(f"Session {session_id} kept alive for potential reconnection")


async def handle_message(websocket: WebSocket, session_id: str, data: dict):
    """Handle incoming WebSocket message with robust error handling"""
    try:
        msg_type = data.get("type")
        session = sessions.get(session_id)
        
        if not session and msg_type != "init":
            await send_to_connection(websocket, {
                "type": "error",
                "message": "Session not found"
            })
            return
        
        logger.info(f"Handling message type '{msg_type}' for session {session_id}")
        
        # Process message based on type
        await process_message_by_type(websocket, session, msg_type, data)
        logger.info(f"Message type '{msg_type}' processed successfully")
        
    except Exception as e:
        logger.error(f"Error handling message for session {session_id}: {e}")
        logger.error(traceback.format_exc())
        
        # Try to handle the error gracefully
        try:
            session = sessions.get(session_id)
            if session:
                session.handle_error(e, f"handle_message({msg_type})")
            
            await send_to_connection(websocket, {
                "type": "error",
                "message": f"Internal server error: {str(e)}"
            })
        except Exception as cleanup_error:
            logger.error(f"Error during error handling: {cleanup_error}")

async def process_message_by_type(websocket: WebSocket, session: GameSession, msg_type: str, data: dict):
    """Process message based on type with individual error handling"""
    try:
        logger.info(f"Processing message type: {msg_type}")
        if msg_type == "human_move":
            await handle_human_move(websocket, session, data)
        elif msg_type == "ai_move_request":
            # Optional: side parameter for explicit requests
            await handle_ai_move_request(websocket, session, data.get('side'))
        elif msg_type == "init":
            logger.info("Calling handle_init_message")
            await handle_init_message(websocket, session, data)
            logger.info("handle_init_message completed")
        elif msg_type == "set_players":
            await handle_set_players(websocket, session, data)
        elif msg_type == "reset_game":
            await handle_reset_game(websocket, session)
        elif msg_type == "get_state":
            await handle_get_state(websocket, session)
        elif msg_type == "undo":
            await handle_undo(websocket, session)
        elif msg_type == "redo":
            await handle_redo(websocket, session)
        elif msg_type == "load_history":
            await handle_load_history(websocket, session, data)
        else:
            await send_to_connection(websocket, {
                "type": "error",
                "message": f"Unknown message type: {msg_type}"
            })
    except Exception as e:
        session.handle_error(e, f"process_message_by_type({msg_type})")
        raise

async def handle_game_over(websocket: WebSocket, session: GameSession, reason: str):
    """Handle game over condition"""
    try:
        # Calculate winner
        winner = None
        if session.game.white_cnt > session.game.black_cnt:
            winner = "White (AI)"
        elif session.game.black_cnt > session.game.white_cnt:
            winner = "Black (Human)"
        else:
            winner = "Draw"
        
        logger.info(f"Game over: {reason}. Winner: {winner}")
        
        await broadcast(session.session_id, {
            "type": "board_update",
            "data": session.get_state()
        })
        
        await send_to_connection(websocket, {
            "type": "game_over",
            "data": {
                "winner": winner,
                "black_count": session.game.black_cnt,
                "white_count": session.game.white_cnt,
                "reason": reason
            }
        })
    except Exception as e:
        logger.error(f"Error handling game over: {e}")
        session.handle_error(e, "handle_game_over")

async def handle_human_move(websocket: WebSocket, session: GameSession, data: dict):
    """Handle human move with robust error handling"""
    try:
        # Handle human move
        move_coord = data.get("move")
        if not move_coord:
            await send_to_connection(websocket, {
                "type": "error",
                "message": "No move provided"
            })
            return
        
        # Make move
        logger.info(f"Making human move: {move_coord}")
        success, error = session.make_move(move_coord)
        
        if not success:
            logger.warning(f"Move failed: {error}")
            await send_to_connection(websocket, {
                "type": "error",
                "message": error or "Invalid move"
            })
            return
        
        logger.info(f"Human move successful. Current turn: {session.game.turn}")
        
        # Check for game over
        if session.game.white_cnt + session.game.black_cnt == 64:
            await handle_game_over(websocket, session, "Board full")
            return
        
        # Broadcast update
        await broadcast(session.session_id, {
            "type": "board_update",
            "data": session.get_state()
        })
        
        # Check if current player has moves
        move_list = session.game.get_move_list()
        
        # If no moves available for current player, pass
        if not move_list:
            logger.info(f"No moves available for {session.game.turn}, passing...")
            session.game.pass_turn()
            
            await broadcast(session.session_id, {
                "type": "board_update",
                "data": session.get_state()
            })
            
            # Check again after pass - if still no moves, game over
            move_list = session.game.get_move_list()
            if not move_list:
                await handle_game_over(websocket, session, "Both players passed")
                return
        
        # DON'T auto-trigger AI move here!
        # Frontend will request AI move via checkAndRequestAIMove() after receiving board_update
        logger.info(f"Human move complete. Next turn: {session.game.turn}. Frontend will request AI move if needed.")
            
    except Exception as e:
        logger.error(f"Error in handle_human_move: {e}")
        session.handle_error(e, "handle_human_move")
        await send_to_connection(websocket, {
            "type": "error",
            "message": f"Error processing human move: {str(e)}"
        })

async def handle_undo(websocket: WebSocket, session: GameSession):
    """Undo back to previous move of the current player (same side)."""
    try:
        desired_turn = session.game.turn
        steps = 0
        # If no history, nothing to undo
        while session.game.board_position_stack:
            try:
                session.game.undo_move()
                steps += 1
            except Exception as e:
                logger.warning(f"Undo failed on step {steps}: {e}")
                break
            # Stop when it's again the same side to move as before
            if session.game.turn == desired_turn:
                break

        logger.info(f"Undo performed: {steps} step(s). Current turn: {session.game.turn}")

        # Send updated state back on this socket and broadcast
        state_payload = {"type": "board_update", "data": session.get_state()}
        await send_to_connection(websocket, state_payload)
        await broadcast(session.session_id, state_payload)
    except Exception as e:
        logger.error(f"Error in handle_undo: {e}")
        session.handle_error(e, "handle_undo")
        await send_to_connection(websocket, {
            "type": "error",
            "message": f"Error processing undo: {str(e)}"
        })

async def handle_redo(websocket: WebSocket, session: GameSession):
    """Redo forward to the next move of the same player (if available)."""
    try:
        desired_turn = session.game.turn
        steps = 0
        while getattr(session.game, 'redo_stack', None):
            try:
                session.game.redo_move()
                steps += 1
            except Exception as e:
                logger.warning(f"Redo failed on step {steps}: {e}")
                break
            if session.game.turn == desired_turn:
                break

        logger.info(f"Redo performed: {steps} step(s). Current turn: {session.game.turn}")

        await broadcast(session.session_id, {
            "type": "board_update",
            "data": session.get_state()
        })
    except Exception as e:
        logger.error(f"Error in handle_redo: {e}")
        session.handle_error(e, "handle_redo")
        await send_to_connection(websocket, {
            "type": "error",
            "message": f"Error processing redo: {str(e)}"
        })

async def handle_load_history(websocket: WebSocket, session: GameSession, data: dict):
    """Reset game and load compact history string like 'F5f6E6f4'."""
    try:
        hist = (data.get("history") or "").strip()
        if not isinstance(hist, str):
            await send_to_connection(websocket, {"type": "error", "message": "Invalid history format"})
            return
        # Reset session/game
        session.reset_session()
        import re
        tokens = re.findall(r"[A-Ha-h][1-8]", hist)
        if len("".join(tokens)) != len(hist):
            logger.warning("History contains non-move characters; ignoring extraneous chars")
        # Apply moves sequentially
        for tok in tokens:
            coord = tok.upper()
            ok, err = session.make_move(coord)
            if not ok:
                await send_to_connection(websocket, {"type": "error", "message": f"Invalid move in history: {tok}"})
                return
        # Broadcast updated state
        await broadcast(session.session_id, {
            "type": "board_update",
            "data": session.get_state()
        })
        # After load: if current player has no moves, pass once; if AI to move, proceed
        move_list = session.game.get_move_list()
        if not move_list:
            session.game.pass_turn()
            state_payload = {"type": "board_update", "data": session.get_state()}
            await send_to_connection(websocket, state_payload)
            await broadcast(session.session_id, state_payload)
            # If still none, game over
            if not session.game.get_move_list():
                await handle_game_over(websocket, session, "Both players passed")
                return
        side = session.game.turn
        ai_present = (session.ai_white is not None and side == 'W') or (session.ai_black is not None and side == 'B')
        if ai_present:
            ai_ml = session.game.get_move_list()
            if not ai_ml:
                session.game.pass_turn()
                state_payload = {"type": "board_update", "data": session.get_state()}
                await send_to_connection(websocket, state_payload)
                await broadcast(session.session_id, state_payload)
            else:
                await handle_ai_move_request(websocket, session, side)
    except Exception as e:
        logger.error(f"Error in handle_load_history: {e}")
        session.handle_error(e, "handle_load_history")
        await send_to_connection(websocket, {"type": "error", "message": f"Error loading history: {str(e)}"})
async def handle_ai_move_request(websocket: WebSocket, session: GameSession, side: str = None):
    """Handle AI move request with robust error handling"""
    try:
        logger.info("AI turn - requesting move...")
        
        # Check if game is already over (board full)
        if session.game.white_cnt + session.game.black_cnt == 64:
            logger.info("Game already over (board full), ignoring AI move request")
            await handle_game_over(websocket, session, "Board full")
            return
        
        side = side or session.game.turn
        ai_name = session.ai_white_name if side == 'W' else session.ai_black_name
        ai_instance = session.ai_white if side == 'W' else session.ai_black
        
        # Verify AI exists for this side
        if ai_instance is None:
            logger.warning(f"No AI configured for side {side} (name: {ai_name})")
            return
        
        # Check if there are any moves available
        move_list = session.game.get_move_list()
        if not move_list:
            logger.info(f"No moves available for AI ({side}), passing...")
            session.game.pass_turn()
            
            await broadcast(session.session_id, {
                "type": "board_update",
                "data": session.get_state()
            })
            
            # Check if opponent has moves
            next_moves = session.game.get_move_list()
            if not next_moves:
                logger.info("Both players have no moves - game over")
                await handle_game_over(websocket, session, "Both players passed")
                return
            
            # Opponent has moves, frontend will continue
            return
        
        # Send ai_thinking with initial stats
        initial_stats = {
            "title": ai_name or "AI",
            "selected_move": "Analyzing...",
            "evaluation": "Calculating...",
            "depth": "Searching...",
            "nodes_searched": 0,
            "nodes_pruned": 0,
            "pruning_ratio": 0,
            "avg_search_time": "0ms",
            "total_searches": 0
        }
        
        await send_to_connection(websocket, {
            "type": "ai_thinking",
            "message": f"{(ai_name or 'AI')} is thinking...",
            "data": initial_stats
        })
        
        try:
            import time
            start_ts = time.perf_counter()
            # Get AI move (with websocket observer for AI insights)
            ai_move = session.get_ai_move(side, websocket)
            end_ts = time.perf_counter()
            last_search_time_ms = max(0.0, (end_ts - start_ts) * 1000.0)
            logger.info(f"AI move received: {ai_move}")
            
            if ai_move:
                # Convert Move coordinates to algebraic notation (A1-H8)
                coord = f"{chr(64+ai_move.x)}{ai_move.y}"
                logger.info(f"Playing AI move: {coord} (x={ai_move.x}, y={ai_move.y})")
                
                try:
                    session.game.move(ai_move)
                    logger.info(f"AI move {coord} executed successfully")
                except Exception as e:
                    logger.error(f"Error executing AI move: {e}")
                    logger.error(traceback.format_exc())
                    raise
                
                # Get AI analysis data
                ai_eval = getattr(ai_move, 'evaluation', None)
                ai_obj = session.ai_white if side == 'W' else session.ai_black
                ai_depth = getattr(ai_obj, 'last_depth', None)
                
                # Get detailed statistics from engine
                engine_stats = {}
                try:
                    if hasattr(ai_obj, 'bitboard_engine'):
                        stats = ai_obj.bitboard_engine.get_statistics()
                        if stats:
                            engine_stats['total_searches'] = stats.get('searches_performed', 0)
                            avg_time = stats.get('avg_time', 0)
                            engine_stats['avg_search_time'] = f"{avg_time*1000:.1f}ms" if avg_time > 0 else "0ms"
                            
                            search_stats = stats.get('search_stats', {})
                            if isinstance(search_stats, dict):
                                nodes = search_stats.get('nodes', 0)
                                pruning = search_stats.get('pruning', 0)
                                engine_stats['nodes_searched'] = nodes
                                engine_stats['nodes_pruned'] = pruning
                                engine_stats['pruning_ratio'] = round(pruning / nodes, 3) if nodes > 0 else 0
                except Exception as e:
                    logger.warning(f"Could not get engine stats: {e}")
                # Always include last search time measured for this move (integer ms)
                engine_stats['last_search_time_ms'] = int(round(last_search_time_ms))
                
                # Store AI stats for notes
                session.last_ai_stats = {
                    "title": ai_name or "AI",
                    "selected_move": coord,
                    "selected_value": str(ai_eval) if ai_eval is not None else "N/A",
                    "final_depth": str(ai_depth) if ai_depth is not None else "N/A",
                    **engine_stats
                }
                
                # Send ai_move message
                await send_to_connection(websocket, {
                    "type": "ai_move",
                    "data": {
                        "move": coord,
                        "evaluation": ai_eval,
                        "depth": ai_depth,
                        **engine_stats
                    }
                })
                
                # Check for game over after AI move
                if session.game.white_cnt + session.game.black_cnt == 64:
                    await handle_game_over(websocket, session, "Board full")
                    return
                
                # Broadcast board update
                await broadcast(session.session_id, {
                    "type": "board_update",
                    "data": session.get_state()
                })
                
                # Check if current player has moves
                move_list = session.game.get_move_list()
                if not move_list:
                    logger.info(f"No moves available for {session.game.turn}, passing...")
                    session.game.pass_turn()
                    
                    await broadcast(session.session_id, {
                        "type": "board_update",
                        "data": session.get_state()
                    })
                    
                    # Check again after pass - if still no moves, game over
                    next_moves = session.game.get_move_list()
                    if not next_moves:
                        logger.info("Both players have no moves - game over")
                        await handle_game_over(websocket, session, "Both players passed")
                        return
                    
                    # Next player has moves - frontend will request if AI and not paused
                    return
                
                # Don't auto-trigger next AI move - let frontend control via pause/play
                # Frontend will send ai_move_request when ready
            else:
                # AI has no moves, pass
                logger.info("AI has no valid moves, passing...")
                session.game.pass_turn()
                
                await broadcast(session.session_id, {
                    "type": "board_update",
                    "data": session.get_state()
                })
                
                # Check if game is over after pass
                next_moves = session.game.get_move_list()
                if not next_moves:
                    logger.info("Both players have no moves after AI pass - game over")
                    await handle_game_over(websocket, session, "Both players passed")
                    return
                
                # After pass, frontend will request AI move if needed and not paused
                    
        except Exception as e:
            logger.error(f"Error in AI move request: {e}")
            session.handle_error(e, "handle_ai_move_request")
            await send_to_connection(websocket, {
                "type": "error",
                "message": f"Error processing AI move: {str(e)}"
            })
            
    except Exception as e:
        logger.error(f"Critical error in handle_ai_move_request: {e}")
        session.handle_error(e, "handle_ai_move_request_critical")
        await send_to_connection(websocket, {
            "type": "error",
            "message": f"Critical error: {str(e)}"
        })

async def handle_init_message(websocket: WebSocket, session: GameSession, data: dict):
    """Handle init message - create new session"""
    try:
        ai_player_name = data.get("ai_player", "DIVZERO.EXE")
        
        # Always create a new session on init (white AI by default)
        new_session = GameSession("default", ai_player_name)
        sessions["default"] = new_session
        
        logger.info(f"Created new session with AI: {ai_player_name}")
        
        # Send initial state
        await send_to_connection(websocket, {
            "type": "board_update",
            "data": new_session.get_state()
        })
        
    except Exception as e:
        logger.error(f"Error in handle_init_message: {e}")
        await send_to_connection(websocket, {
            "type": "error",
            "message": f"Error initializing game: {str(e)}"
        })

async def handle_set_players(websocket: WebSocket, session: GameSession, data: dict):
    """Set players for both sides. Payload: {"white": "Human"|AI_NAME|None, "black": "Human"|AI_NAME|None} """
    try:
        white = data.get("white")
        black = data.get("black")
        
        logger.info(f"Setting players - White: {white}, Black: {black}")
        
        # Normalize: None or 'Human' or 'Human Player' => human
        session.ai_white_name = None if (white is None or str(white).lower()=="human" or str(white)=="Human Player") else str(white)
        session.ai_black_name = None if (black is None or str(black).lower()=="human" or str(black)=="Human Player") else str(black)
        
        logger.info(f"Configured - ai_white_name: {session.ai_white_name}, ai_black_name: {session.ai_black_name}")
        
        # Recreate AI instances
        session.reset_session()
        
        logger.info(f"Session reset - ai_white: {session.ai_white is not None}, ai_black: {session.ai_black is not None}")
        logger.info(f"Current turn after reset: {session.game.turn}")
        
        # Send updated state
        state_data = session.get_state()
        logger.info(f"Sending state - Black: {state_data['players']['black']['name']}, White: {state_data['players']['white']['name']}, Turn: {state_data['status']['turn_by_ply'][0]}")
        
        await send_to_connection(websocket, {"type": "board_update", "data": state_data})
        
        # Check if AI should make first move (if it's AI's turn to start)
        current_turn = session.game.turn
        ai_present = (session.ai_white is not None and current_turn == 'W') or (session.ai_black is not None and current_turn == 'B')
        
        if ai_present:
            logger.info(f"AI should move immediately (turn: {current_turn})")
            # Small delay to ensure frontend receives board_update first
            await asyncio.sleep(0.1)
            await handle_ai_move_request(websocket, session, current_turn)
        else:
            logger.info(f"Human to move (turn: {current_turn})")
        
    except Exception as e:
        logger.error(f"Error in handle_set_players: {e}")
        session.handle_error(e, "handle_set_players")
        await send_to_connection(websocket, {"type": "error", "message": f"Error setting players: {str(e)}"})

async def handle_reset_game(websocket: WebSocket, session: GameSession):
    """Handle reset game message"""
    try:
        session.reset_session()
        await send_to_connection(websocket, {
            "type": "board_update",
            "data": session.get_state()
        })
    except Exception as e:
        logger.error(f"Error in handle_reset_game: {e}")
        session.handle_error(e, "handle_reset_game")

async def handle_get_state(websocket: WebSocket, session: GameSession):
    """Handle get state message"""
    try:
        await send_to_connection(websocket, {
            "type": "board_update",
            "data": session.get_state()
        })
    except Exception as e:
        logger.error(f"Error in handle_get_state: {e}")
        session.handle_error(e, "handle_get_state")

async def send_to_connection(websocket: WebSocket, message: dict):
    """Send message to WebSocket connection"""
    try:
        message_str = json.dumps(message)
        logger.info(f"Sending message: {message_str[:100]}...")
        await websocket.send_text(message_str)
        logger.info("Message sent successfully")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

async def broadcast(session_id: str, message: dict):
    """Broadcast message to all connections in session"""
    try:
        if session_id in active_connections:
            await send_to_connection(active_connections[session_id], message)
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Reversi42 WebSocket Backend')
    parser.add_argument('--port', type=int, default=8000, help='Port to run on')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--player', default='DIVZERO.EXE', help='AI player to use')
    
    args = parser.parse_args()
    
    logger.info(f"Starting Reversi42 WebSocket Backend on {args.host}:{args.port}")
    logger.info(f"AI Player: {args.player}")
    
    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()