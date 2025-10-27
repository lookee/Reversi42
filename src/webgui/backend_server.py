#!/usr/bin/env python3
"""
WebGUI Backend Server - WebSocket Bridge for Reversi42
Enables real-time gameplay between web frontend and game engine

Usage:
    python -m src.webgui.backend_server --port 8000 --player DIVZERO.EXE
"""

import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(src_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, project_root)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import asyncio
import json
import argparse
from typing import Dict, Set
from dataclasses import dataclass, asdict

# Import game engine
from Reversi.Game import Game, Move
from Players.PlayerFactory import PlayerFactory
from Players.Gladiators.PlayerDivZero import PlayerDivZero


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
        self.session_id = session_id
        self.ai_player_name = ai_player_name
        self.game = Game(8)
        
        # Create AI player
        if ai_player_name == "DIVZERO.EXE":
            self.ai_player = PlayerDivZero()
        else:
            self.ai_player = PlayerFactory.create_player(ai_player_name)
        
        # PlayerDivZero doesn't have set_color method, it uses the game's turn
        # AI will play white automatically based on game.turn
        
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
        
        # Return full state matching frontend JSON structure
        state = {
            "meta": {"variant": "Reversi/Othello", "size": 8},
            "players": {
                "black": {"name": "Human", "avatar": "HM"},
                "white": {"name": self.ai_player_name, "avatar": self.ai_player_name[:2].upper()}
            },
            "status": {
                "turn_by_ply": [game.turn]
            },
            "positions": [positions],
            "moves": moves,
            "valid_by_ply": [valid_moves],
            "opening_by_ply": [[]],
            "notes": {
                "title": "Notes",
                "final_depth": 8,
                "total_nodes": "9,234",
                "alpha_beta_pruned": {
                    "value": "1,729",
                    "value2": "(25.3%)"
                },
                "selected_move": "E3",
                "selected_value": "-10"
            }
        }
        print(f"get_state returning: {state}")
        return state
    
    def make_move(self, move_coord: str) -> tuple[bool, str]:
        """Make a move from coordinate notation (e.g., 'C4')
        Returns (success, error_message)
        """
        if len(move_coord) != 2:
            return False, "Invalid move format"
        
        col = ord(move_coord[0].upper()) - 64  # A=1, B=2, etc. (Game uses 1-indexed)
        row = int(move_coord[1])  # Game uses 1-8 indexing
        
        if col < 1 or col > 8 or row < 1 or row > 8:
            return False, "Move out of bounds"
        
        move = Move(col, row)
        
        if not self.game.valid_move(move):
            return False, "Invalid move"
        
        self.game.move(move)
        return True, None
    
    def get_ai_move(self):
        """Get AI move"""
        move_list = self.game.get_move_list()
        return self.ai_player.get_move(self.game, move_list, None)


# FastAPI app
app = FastAPI(title="Reversi42 WebSocket Server")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
sessions: Dict[str, GameSession] = {}
active_connections: Dict[str, Set[WebSocket]] = {}  # session_id -> set of websockets


@app.get("/")
async def get_index():
    """Serve the game HTML file"""
    import os
    html_path = os.path.join(os.path.dirname(__file__), 'game_websocket.html')
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return HTMLResponse("""
    <html>
        <head><title>Reversi42 WebSocket Server</title></head>
        <body>
            <h1>Reversi42 WebSocket Bridge</h1>
            <p>WebSocket server is running</p>
            <p>Connect to: <code>ws://localhost:8000/ws</code></p>
            <p>Active sessions: <span id="sessions">0</span></p>
            <script>
                fetch('/api/stats').then(r => r.json()).then(data => {
                    document.getElementById('sessions').textContent = data.active_sessions;
                });
            </script>
        </body>
    </html>
    """)


@app.get("/api/stats")
async def get_stats():
    """Get server statistics"""
    return {
        "active_sessions": len(sessions),
        "total_connections": sum(len(conns) for conns in active_connections.values())
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for game communication"""
    print("WebSocket connection attempt received")
    try:
        await websocket.accept()
        print("WebSocket accepted")
    except Exception as e:
        print(f"Error accepting WebSocket: {e}")
        return
    
    session_id = None
    try:
        # Wait for initial message to identify session
        print("Waiting for initial message...")
        initial_msg = await websocket.receive_json()
        print(f"Received initial message: {initial_msg}")
        
        if initial_msg.get("type") != "init":
            await websocket.send_json({
                "type": "error",
                "message": "First message must be init"
            })
            return
        
        session_id = initial_msg.get("session_id", "default")
        
        # Always create a new session (reset game)
        ai_player = initial_msg.get("ai_player", "DIVZERO.EXE")
        sessions[session_id] = GameSession(session_id, ai_player)
        active_connections[session_id] = set()
        print(f"Created new session: {session_id} vs {ai_player}")
        
        # Add this connection
        active_connections[session_id].add(websocket)
        
        # Send initial state
        state = sessions[session_id].get_state()
        print(f"Sending initial state to client: {state}")
        await send_to_connection(websocket, {
            "type": "board_update",
            "data": state
        })
        
        # Handle messages
        while True:
            data = await websocket.receive_json()
            await handle_message(websocket, session_id, data)
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected from session {session_id}")
    except Exception as e:
        print(f"Error in websocket handler: {e}")
    finally:
        # Clean up
        if session_id and websocket in active_connections.get(session_id, set()):
            active_connections[session_id].remove(websocket)
        
        # Remove session if no connections
        if session_id and session_id in active_connections and not active_connections[session_id]:
            del active_connections[session_id]
            if session_id in sessions:
                del sessions[session_id]
                print(f"Removed session: {session_id}")


async def handle_message(websocket: WebSocket, session_id: str, data: dict):
    """Handle incoming WebSocket message"""
    msg_type = data.get("type")
    session = sessions.get(session_id)
    
    if not session:
        await send_to_connection(websocket, {
            "type": "error",
            "message": "Session not found"
        })
        return
    
    if msg_type == "human_move":
        # Handle human move
        move_coord = data.get("move")
        if not move_coord:
            await send_to_connection(websocket, {
                "type": "error",
                "message": "No move provided"
            })
            return
        
        # Make move
        print(f"Making human move: {move_coord}")
        success, error = session.make_move(move_coord)
        
        if not success:
            print(f"Move failed: {error}")
            await send_to_connection(websocket, {
                "type": "error",
                "message": error or "Invalid move"
            })
            return
        
        print(f"Human move successful. Current turn: {session.game.turn}")
        
        # Broadcast update
        await broadcast(session_id, {
            "type": "board_update",
            "data": session.get_state()
        })
        
        # Check if AI should move
        print(f"Checking if AI should move. Turn: {session.game.turn}")
        if session.game.turn == 'W':
            print("AI turn - requesting move...")
            await send_to_connection(websocket, {
                "type": "ai_thinking",
                "message": f"{session.ai_player_name} is thinking..."
            })
            
            try:
                # Get AI move
                ai_move = session.get_ai_move()
                print(f"AI move received: {ai_move}")
                
                if ai_move:
                    # Convert Move coordinates to algebraic notation (A1-H8)
                    coord = f"{chr(64+ai_move.x)}{ai_move.y}"
                    print(f"Playing AI move: {coord} (x={ai_move.x}, y={ai_move.y})")
                    session.game.move(ai_move)
                    
                    # Get AI analysis data
                    ai_eval = getattr(ai_move, 'evaluation', None)
                    ai_depth = getattr(session.ai_player, 'last_depth', None)
                    
                    # Get detailed statistics from engine (with error handling)
                    engine_stats = {}
                    try:
                        if hasattr(session.ai_player, 'bitboard_engine'):
                            stats = session.ai_player.bitboard_engine.get_statistics()
                            if stats:
                                engine_stats['total_searches'] = stats.get('searches_performed', 0)
                                engine_stats['avg_search_time'] = f"{stats.get('avg_time', 0)*1000:.1f}ms"
                                
                                # Extract search stats if available
                                search_stats = stats.get('search_stats', {})
                                if isinstance(search_stats, dict):
                                    engine_stats['nodes_searched'] = search_stats.get('nodes_searched', 0)
                                    engine_stats['nodes_pruned'] = search_stats.get('nodes_pruned', 0)
                                    engine_stats['pruning_ratio'] = search_stats.get('pruning_ratio', 0)
                    except Exception as e:
                        print(f"Error getting engine stats: {e}")
                        import traceback
                        traceback.print_exc()
                        # Continue without stats if there's an error
                    
                    await send_to_connection(websocket, {
                        "type": "ai_move",
                        "data": {
                            "move": coord,
                            "evaluation": ai_eval,
                            "depth": ai_depth,
                            **engine_stats  # Add engine statistics
                        }
                    })
                else:
                    print("AI passed")
                    # AI passed
                    if hasattr(session.game, 'pass_turn'):
                        session.game.pass_turn()
                    else:
                        session.game.turn = 'B'
                
                # Broadcast updated state
                await broadcast(session_id, {
                    "type": "board_update",
                    "data": session.get_state()
                })
            except Exception as e:
                print(f"Error during AI move: {e}")
                import traceback
                traceback.print_exc()
    
    elif msg_type == "reset_game":
        # Reset game
        session.game = Game(8, 8)
        await broadcast(session_id, {
            "type": "board_update",
            "data": session.get_state()
        })
    
    elif msg_type == "get_state":
        # Send current state
        await send_to_connection(websocket, {
            "type": "board_update",
            "data": session.get_state()
        })


async def send_to_connection(websocket: WebSocket, message: dict):
    """Send message to a single connection"""
    try:
        await websocket.send_json(message)
    except Exception as e:
        print(f"Error sending message: {e}")


async def broadcast(session_id: str, message: dict):
    """Broadcast message to all connections in a session"""
    if session_id not in active_connections:
        return
    
    # Get a copy of the set to avoid modification during iteration
    connections = active_connections[session_id].copy()
    
    for connection in connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Error broadcasting to connection: {e}")
            # Remove dead connection
            active_connections[session_id].discard(connection)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Reversi42 WebSocket Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--player", default="DIVZERO.EXE", help="AI player to use")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print(f"""
╔════════════════════════════════════════════╗
║   Reversi42 WebSocket Server              ║
╠════════════════════════════════════════════╣
║  Server:  ws://localhost:{args.port}/ws     ║
║  AI Player: {args.player:<25} ║
╚════════════════════════════════════════════╝
    """)
    
    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
