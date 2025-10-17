#!/usr/bin/env python3

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

"""
EXAMPLE: How to create a custom player with configurable parameters.

This file demonstrates the metadata system for automatic menu generation.
To add a new player to the game:

1. Create a class inheriting from Player
2. Define PLAYER_METADATA with:
   - display_name: Name shown in menu
   - description: Short description for help
   - enabled: True to show in menu, False to hide
   - parameters: List of configurable parameters

3. Add to PlayerFactory.ALL_PLAYER_CLASSES

The menu system will automatically:
- Show the player in selection menus
- Display the description
- Create configuration screens for parameters
- Pass parameters to __init__
"""

from Players.Player import Player
from Reversi.Game import Move
import random

class CustomPlayerExample(Player):
    """
    Example custom player with configurable parameters.
    
    This player demonstrates:
    - Custom metadata
    - Multiple configurable parameters
    - Automatic menu integration
    - Parameter validation
    """
    
    PLAYER_METADATA = {
        'display_name': 'CustomExample',
        'description': 'Example player with configurable parameters',
        'enabled': False,  # Set to True to enable in menu
        'parameters': [
            {
                'name': 'aggression',
                'display_name': 'Aggression Level',
                'type': 'int',
                'min': 1,
                'max': 10,
                'default': 5,
                'description': 'How aggressive the player is (1=defensive, 10=aggressive)'
            },
            {
                'name': 'randomness',
                'display_name': 'Randomness',
                'type': 'int',
                'min': 0,
                'max': 100,
                'default': 20,
                'description': 'Percentage of random moves (0=deterministic, 100=random)'
            },
            {
                'name': 'strategy',
                'display_name': 'Strategy',
                'type': 'choice',
                'choices': ['Corners', 'Edges', 'Center', 'Mixed'],
                'default': 'Mixed',
                'description': 'Preferred positional strategy'
            }
        ]
    }
    
    def __init__(self, name='CustomExample', aggression=5, randomness=20, strategy='Mixed'):
        """
        Initialize custom player with parameters.
        
        Args:
            name: Player name
            aggression: Aggression level (1-10)
            randomness: Randomness percentage (0-100)
            strategy: Preferred strategy (Corners/Edges/Center/Mixed)
        """
        self.name = name
        self.aggression = aggression
        self.randomness = randomness
        self.strategy = strategy
    
    def get_move(self, game, moves, control):
        """
        Get move based on configured parameters.
        
        This is a simplified example. A real implementation would
        use the parameters to influence move selection.
        """
        if not moves:
            return None
        
        # Apply randomness
        if random.randint(0, 100) < self.randomness:
            return random.choice(moves)
        
        # Apply strategy
        best_move = moves[0]
        best_score = -1000
        
        for move in moves:
            score = 0
            
            # Corners strategy
            if self.strategy in ['Corners', 'Mixed']:
                if (move.x, move.y) in [(1,1), (1,8), (8,1), (8,8)]:
                    score += 100 * self.aggression
            
            # Edges strategy
            if self.strategy in ['Edges', 'Mixed']:
                if move.x == 1 or move.x == 8 or move.y == 1 or move.y == 8:
                    score += 50 * self.aggression
            
            # Center strategy
            if self.strategy in ['Center', 'Mixed']:
                center_dist = abs(move.x - 4.5) + abs(move.y - 4.5)
                score += (10 - center_dist) * self.aggression
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move


# TO USE THIS PLAYER:
# 1. Enable it by setting enabled=True in PLAYER_METADATA
# 2. Add to PlayerFactory.ALL_PLAYER_CLASSES:
#    from Players.CustomPlayerExample import CustomPlayerExample
#    ALL_PLAYER_CLASSES = [
#        HumanPlayer,
#        AIPlayer,
#        CustomPlayerExample,  # Add here
#        ...
#    ]
# 3. The menu will automatically show it with parameter configuration!

