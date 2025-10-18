# Network Player

## Overview

The `NetworkPlayer` is a placeholder implementation demonstrating how to create a player that could connect to remote opponents over a network. Currently, it's not fully implemented but serves as a template for adding network play functionality to Reversi42.

## Class Definition

```python
class NetworkPlayer(Player):
    """Example of a network player that could connect to remote players.
    This demonstrates how easy it is to add new player types."""
```

## Location
`src/Players/NetworkPlayer.py`

## Current Status

**⚠️ NOT FULLY IMPLEMENTED**

This player is currently disabled in the menu system and serves as:
1. **Template** for implementing network play
2. **Example** of extending the Player class
3. **Demonstration** of the modular player system

## Key Features (Planned)

### 1. Remote Connection
- Connect to game server
- Send/receive game state
- Synchronize moves
- Handle disconnections

### 2. Protocol Support
- JSON-based message format (planned)
- HTTP/WebSocket communication (planned)
- Move validation on both sides
- Turn synchronization

### 3. Flexible Configuration
- Configurable server URL
- Connection timeout settings
- Reconnection logic
- Fallback behavior

## How It Would Work

### Connection Flow (Planned)

```
1. Initialize NetworkPlayer
    ↓
2. Connect to server URL
    ↓
3. Wait for game assignment
    ↓
4. For each move:
   - Send current game state
   - Wait for opponent's move
   - Validate received move
   - Return move to game
    ↓
5. Disconnect on game end
```

### Message Format (Example)

```json
// Request: Send game state
{
  "type": "get_move",
  "game_id": "12345",
  "player_id": "black",
  "board_state": "...",
  "valid_moves": ["D3", "C4", "E6"],
  "history": "F5d6C3"
}

// Response: Receive move
{
  "type": "move_response",
  "move": "D3",
  "timestamp": 1634567890
}
```

## Configuration

### Metadata

```python
PLAYER_METADATA = {
    'display_name': 'Network',
    'description': 'Play against remote opponent (not implemented)',
    'enabled': False,  # Disabled - not fully implemented
    'parameters': [
        {
            'name': 'server_url',
            'display_name': 'Server URL',
            'type': 'str',
            'default': 'localhost:8080',
            'description': 'URL of the game server'
        }
    ]
}
```

**Note**: `enabled: False` prevents selection in menu

### Initialization

```python
# Create network player (placeholder)
net_player = NetworkPlayer(name='NetworkPlayer', server_url='localhost:8080')

# Connect (not implemented)
net_player.connect('game.example.com:8080')
```

## Current Implementation

### Placeholder get_move()

```python
def get_move(self, game, moves, control):
    """
    Get move from network connection.
    For now, this is just a placeholder that returns a random move.
    """
    if not self.connected:
        print(f"NetworkPlayer {self.name}: Not connected to server")
        # Fallback to random move for demonstration
        if moves:
            import random
            return random.choice(moves)
        return None
    
    # In a real implementation, this would:
    # 1. Send game state to server
    # 2. Wait for response
    # 3. Parse and return the move
    
    print(f"NetworkPlayer {self.name}: Getting move from server...")
    
    # Placeholder: return first available move
    if moves:
        return moves[0]
    return None
```

### Connection Methods

```python
def connect(self, server_url):
    """Connect to a network server."""
    self.server_url = server_url
    self.connected = True
    print(f"NetworkPlayer {self.name}: Connected to {server_url}")

def disconnect(self):
    """Disconnect from network server."""
    self.connected = False
    print(f"NetworkPlayer {self.name}: Disconnected from server")
```

**Note**: These methods don't actually create network connections yet

## Implementation Ideas

### WebSocket Implementation

```python
import websocket
import json

class WebSocketNetworkPlayer(NetworkPlayer):
    """Network player using WebSocket protocol"""
    
    def __init__(self, name='WebSocketPlayer', server_url='ws://localhost:8080'):
        super().__init__(name, server_url)
        self.ws = None
    
    def connect(self, server_url):
        """Establish WebSocket connection"""
        try:
            self.ws = websocket.create_connection(server_url)
            self.connected = True
            print(f"Connected to {server_url}")
            
            # Send join message
            self.ws.send(json.dumps({
                'type': 'join',
                'player_name': self.name
            }))
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False
    
    def get_move(self, game, moves, control):
        """Get move from remote player via WebSocket"""
        if not self.connected or not self.ws:
            return random.choice(moves) if moves else None
        
        try:
            # Send game state
            message = {
                'type': 'get_move',
                'board': game.to_dict(),
                'valid_moves': [str(m) for m in moves],
                'history': game.history
            }
            self.ws.send(json.dumps(message))
            
            # Wait for response
            response = json.loads(self.ws.recv())
            move_str = response['move']
            
            # Parse move (e.g., "D3" → Move(4, 3))
            move = Move.from_string(move_str)
            
            if move in moves:
                return move
            else:
                print(f"Invalid move from server: {move_str}")
                return moves[0]
                
        except Exception as e:
            print(f"Network error: {e}")
            self.connected = False
            return random.choice(moves) if moves else None
    
    def disconnect(self):
        """Close WebSocket connection"""
        if self.ws:
            self.ws.close()
        self.connected = False
```

### HTTP REST API Implementation

```python
import requests
import json

class RESTNetworkPlayer(NetworkPlayer):
    """Network player using REST API"""
    
    def __init__(self, name='RESTPlayer', server_url='http://localhost:8080'):
        super().__init__(name, server_url)
        self.session_id = None
    
    def connect(self, server_url):
        """Create game session"""
        try:
            response = requests.post(
                f"{server_url}/api/session/create",
                json={'player_name': self.name},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_id = data['session_id']
                self.connected = True
                print(f"Session created: {self.session_id}")
            else:
                print(f"Failed to create session: {response.status_code}")
                self.connected = False
        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False
    
    def get_move(self, game, moves, control):
        """Get move via HTTP request"""
        if not self.connected or not self.session_id:
            return random.choice(moves) if moves else None
        
        try:
            # POST game state, get move
            response = requests.post(
                f"{self.server_url}/api/game/move",
                json={
                    'session_id': self.session_id,
                    'board_state': game.to_dict(),
                    'valid_moves': [str(m) for m in moves]
                },
                timeout=30  # 30 seconds timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                move = Move.from_string(data['move'])
                return move if move in moves else moves[0]
            else:
                print(f"Server error: {response.status_code}")
                return moves[0]
                
        except requests.Timeout:
            print("Request timeout - using fallback")
            return moves[0]
        except Exception as e:
            print(f"Error: {e}")
            self.connected = False
            return moves[0]
```

### Peer-to-Peer Implementation

```python
import socket
import pickle

class P2PNetworkPlayer(NetworkPlayer):
    """Peer-to-peer network player"""
    
    def __init__(self, name='P2PPlayer', host='0.0.0.0', port=9999):
        super().__init__(name)
        self.host = host
        self.port = port
        self.socket = None
        self.conn = None
    
    def host_game(self):
        """Host a game (server mode)"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        
        print(f"Waiting for connection on {self.host}:{self.port}...")
        self.conn, addr = self.socket.accept()
        print(f"Connected to {addr}")
        self.connected = True
    
    def join_game(self, host, port):
        """Join a game (client mode)"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
            self.conn = self.socket
            self.connected = True
            print(f"Connected to {host}:{port}")
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False
    
    def send_move(self, move):
        """Send move to opponent"""
        if self.conn:
            data = pickle.dumps(move)
            self.conn.sendall(data)
    
    def receive_move(self):
        """Receive move from opponent"""
        if self.conn:
            data = self.conn.recv(1024)
            return pickle.loads(data)
        return None
```

## Use Cases (When Implemented)

### 1. Online Multiplayer
```python
# Player 1 (host)
player1 = HumanPlayer()
net_opponent = P2PNetworkPlayer()
net_opponent.host_game()  # Wait for connection

game.play(player1, net_opponent)

# Player 2 (client)
player2 = HumanPlayer()
net_player = P2PNetworkPlayer()
net_player.join_game('192.168.1.100', 9999)

game.play(net_player, player2)
```

### 2. Remote AI Battle
```python
# Server hosts powerful AI
server_ai = AIPlayerGrandmaster(deep=10)
net_server = NetworkServer(server_ai, port=8080)
net_server.start()

# Client connects to challenge it
client = AIPlayer(deep=6)
net_opponent = RESTNetworkPlayer(server_url='http://server.com:8080')
net_opponent.connect()

game.play(client, net_opponent)
```

### 3. Tournament Server
```python
# Central server coordinates tournament
class TournamentServer:
    def __init__(self, port=8080):
        self.players = []
        self.matches = []
    
    def register_player(self, player_connection):
        """Add player to tournament"""
        self.players.append(player_connection)
    
    def run_tournament(self):
        """Run round-robin tournament"""
        for p1, p2 in combinations(self.players, 2):
            match = Match(p1, p2)
            self.matches.append(match)
            match.play()
```

## Security Considerations (When Implementing)

### 1. Input Validation
- Validate all received moves
- Check move is in valid_moves list
- Sanitize board state data
- Prevent injection attacks

### 2. Authentication
- Player authentication
- Session tokens
- Rate limiting
- Anti-cheat measures

### 3. Network Security
- Use HTTPS/WSS for encryption
- Validate server certificates
- Prevent man-in-the-middle attacks
- Secure credential storage

### 4. Error Handling
- Timeout handling
- Disconnection recovery
- Invalid move handling
- Network errors

## Development Roadmap

### Phase 1: Basic Implementation
- [ ] Simple HTTP-based protocol
- [ ] JSON message format
- [ ] Basic server implementation
- [ ] Client-server communication

### Phase 2: Enhanced Features
- [ ] WebSocket support
- [ ] Game spectating
- [ ] Chat functionality
- [ ] Reconnection logic

### Phase 3: Advanced Features
- [ ] Matchmaking system
- [ ] Player rankings/ELO
- [ ] Tournament support
- [ ] Game replay/analysis

### Phase 4: Security & Polish
- [ ] Authentication system
- [ ] Encryption
- [ ] Anti-cheat
- [ ] Performance optimization

## Contributing

If you're interested in implementing network play:

1. Fork the repository
2. Implement `NetworkPlayer.get_move()`
3. Create server implementation
4. Add protocol documentation
5. Submit pull request

See [ADDING_PLAYERS.md](../ADDING_PLAYERS.md) for player development guidelines.

## Example Server (Conceptual)

```python
# reversi_server.py
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
sessions = {}

@app.route('/api/session/create', methods=['POST'])
def create_session():
    """Create new game session"""
    data = request.json
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        'player': data['player_name'],
        'game': Game()
    }
    return jsonify({'session_id': session_id})

@app.route('/api/game/move', methods=['POST'])
def get_move():
    """Get AI move for position"""
    data = request.json
    session_id = data['session_id']
    
    if session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 404
    
    # Get AI to calculate move
    game = sessions[session_id]['game']
    ai = AIPlayerGrandmaster(deep=8)
    move = ai.get_move(game, data['valid_moves'], None)
    
    return jsonify({'move': str(move)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## See Also

- [Base Player Class](Player.md)
- [Human Player](HumanPlayer.md) - Local input
- [Adding Custom Players](../ADDING_PLAYERS.md)
- [Player Factory](../../src/Players/PlayerFactory.py)

## Summary

The `NetworkPlayer` is currently a placeholder demonstrating the extensibility of Reversi42's player system. While not yet functional, it provides a template for implementing network play and showcases how easy it is to add new player types to the game.

**Status**: 🚧 Not Implemented (Template Only)

**Potential**: High - Could enable online multiplayer, remote AI challenges, and tournament play

**Difficulty**: Medium-High - Requires network programming and protocol design

