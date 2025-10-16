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

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from pygame.locals import *

from Reversi.Game import Game
from Reversi.Game import Move

from Players.HumanPlayer import HumanPlayer
from Players.AIPlayer import AIPlayer
from Players.Monkey import Monkey

from Board.BoardControl import BoardControl
from Menu import Menu

def create_player(player_type, difficulty=6):
    """Create a player instance based on type and difficulty"""
    if player_type == "Human":
        return HumanPlayer()
    elif player_type == "AI":
        return AIPlayer(difficulty)
    elif player_type == "Monkey":
        return Monkey()
    else:
        return HumanPlayer()  # Default fallback

def main():
    # Initialize pygame
    pygame.init()
    
    # Show menu and get player selections
    menu = Menu()
    result = menu.run()
    
    if result == "exit":
        pygame.quit()
        sys.exit()
    
    # Extract player settings
    black_player_type = result["black_player"]
    white_player_type = result["white_player"]
    black_difficulty = result["black_difficulty"]
    white_difficulty = result["white_difficulty"]
    
    # Create players
    players = {
        'B': create_player(black_player_type, black_difficulty),
        'W': create_player(white_player_type, white_difficulty)
    }
    
    # Initialize game
    size = 8
    g = Game(size)
    c = BoardControl(size, size)
    
    game_history = ""
    last_move = None
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Check if game is finished
        if g.is_finish():
            break
            
        turn = g.get_turn()
        player = players[turn]
        
        print(f"{player.get_name()} is moving...")
        
        moves = g.get_move_list()
        
        if len(moves) > 0:
            # Import board position
            c.importModel(g.export_str())
            
            # Show all available moves
            for move in moves:
                # print(f"move: {move}")
                c.setCanMove(move.get_x(), move.get_y(), turn)
            
            # Render board
            c.renderModel()
            c.cursorWait()
            
            # Render ascii board
            # g.view()
            
            # History and last move
            print(f"\ngame history:\n{game_history}\n")
            print(f"last move: {last_move}")
            
            # Instructions for cursor navigation
            if isinstance(player, HumanPlayer):
                print("\nControls:")
                print("- Click to select a move")
                print("- Press 'C' to toggle cursor navigation mode")
                print("- Use arrow keys to move cursor")
                print("- Press ENTER or SPACE to select move at cursor")
                print("- Press ESC or Q to quit")
            
            # Get move
            move = player.get_move(g, moves, c)
            
            # Check if player wants to exit
            if move is None:
                print("Game exited by user.")
                running = False
                break
            
            # Move
            g.move(move)
            
            # Set last move indicator for visual display
            c.setLastMove(move.get_x(), move.get_y())
            
            # Update game history
            if turn == 'B':
                # is a black move
                last_move = str(move).upper()
            else:
                # is a white move
                last_move = str(move).lower()
            
            game_history += last_move
            
            print(f"move: {move}")
        
        else:
            g.pass_turn()
            print(f"{player.get_name()} is passing")
            
            # Check if both players have no moves (game over)
            next_moves = g.get_move_list()
            if len(next_moves) == 0:
                print("No moves available for either player. Game over!")
                break
        
        # Check for exit events during AI turns
        c.check_events()
        if c.should_exit:
            print("Game exited by user.")
            running = False
            break
        
        clock.tick(60)  # Limit to 60 FPS
    
    # Print results
    if not g.is_finish():
        print("Game was exited by user.")
    else:
        c.importModel(g.export_str())
        c.renderModel()
        
        g.view()
        g.result()
        
        print(f"\ngame history:\n{game_history}\n")
        
        # Wait for user to close the window
        print("Game finished! Close the window to exit.")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    break
            else:
                clock.tick(60)
                continue
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
