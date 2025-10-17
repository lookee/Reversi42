#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Reversi42 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Reversi42.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

from Players.Player import Player
from Reversi.Game import Game
from Reversi.Game import Move

class NetworkPlayer(Player):
    """
    Example of a network player that could connect to remote players.
    This demonstrates how easy it is to add new player types.
    """
    
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
    
    def __init__(self, name='NetworkPlayer', server_url=None):
        self.name = name
        self.server_url = server_url
        self.connected = False
    
    def get_move(self, game, moves, control):
        """
        Get move from network connection.
        For now, this is just a placeholder that returns a random move.
        In a real implementation, this would communicate with a remote server.
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
    
    def connect(self, server_url):
        """Connect to a network server."""
        self.server_url = server_url
        self.connected = True
        print(f"NetworkPlayer {self.name}: Connected to {server_url}")
    
    def disconnect(self):
        """Disconnect from network server."""
        self.connected = False
        print(f"NetworkPlayer {self.name}: Disconnected from server")
