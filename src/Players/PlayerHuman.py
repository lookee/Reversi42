
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
PlayerHuman - Human player (UI-agnostic!)

Clean Architecture Implementation:
- NO pygame dependencies
- Depends on InputProvider abstraction (Dependency Inversion)
- UI-specific logic delegated to InputProvider implementations
- Fully testable with MockInputProvider

Design Pattern: Strategy + Dependency Injection
"""

from typing import List, Optional
from Reversi.Game import Move
from Players.Player import Player
from Players.abstractions import InputProvider


class PlayerHuman(Player):
    """
    Human player - completely UI-agnostic!
    
    This class contains ONLY domain logic for a human player.
    All UI-specific input handling is delegated to the InputProvider.
    
    Benefits:
    - No pygame/UI dependencies
    - Fully testable with mock InputProvider
    - Works with ANY UI (pygame, terminal, web, network)
    - Follows Dependency Inversion Principle
    
    Example:
        # Pygame UI
        provider = PygameInputProvider(board_control)
        player = PlayerHuman(provider, name="Alice")
        
        # Terminal UI
        provider = TerminalInputProvider()
        player = PlayerHuman(provider, name="Bob")
        
        # Testing
        provider = MockInputProvider([Move(3,3), Move(4,4)])
        player = PlayerHuman(provider, name="TestPlayer")
    """
    
    PLAYER_METADATA = {
        'display_name': 'Human Player',
        'description': 'You! Play with mouse or keyboard controls',
        'enabled': True,
        'parameters': []
    }

    def __init__(self, input_provider: InputProvider, name='Human'):
        """
        Initialize human player with InputProvider (Dependency Injection!)
        
        Args:
            input_provider: Implementation of InputProvider for getting user input
            name: Player name
        """
        super().__init__()
        self.name = name
        self.input_provider = input_provider
    
    def get_move(self, game, move_list: List[Move], control=None) -> Optional[Move]:
        """
        Get move from human player.
        
        Pure domain logic - delegates input to provider.
        
        Args:
            game: Current game state
            move_list: List of legal moves
            control: (DEPRECATED) Kept for backward compatibility, not used
            
        Returns:
            Move selected by user, or None if exit/pause requested
        """
        # Reset input provider state before getting new move
        self.input_provider.reset()
        
        while True:
            # Delegate input to provider (Strategy pattern!)
            move = self.input_provider.get_move_input(game, move_list)
            
            # Check for exit/pause requests
            if self.input_provider.should_exit() or self.input_provider.should_pause():
                return None
            
            # Validate move
            if move and game.valid_move(move):
                return move
            elif move:
                print(f"Move {move} is not valid!")
                # Continue loop to get another move
        
        return None
