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

from Players.PlayerFactory import PlayerFactory
from Players.HumanPlayer import HumanPlayer
from Board.BoardControl import BoardControl
from Menu import Menu
from GameOver import GameOver

def create_player(player_type, difficulty=6, engine_type='Minimax'):
    """Create a player instance using the PlayerFactory"""
    try:
        if player_type == "AI":
            return PlayerFactory.create_ai_player(engine_type, difficulty)
        else:
            return PlayerFactory.create_player(player_type)
    except ValueError as e:
        print(f"Error creating player: {e}")
        return PlayerFactory.create_player("Human")  # Default fallback

def run_game(menu_result):
    """Run a single game with the given player settings"""
    
    # Extract player settings
    black_player_type = menu_result["black_player"]
    white_player_type = menu_result["white_player"]
    black_difficulty = menu_result["black_difficulty"]
    white_difficulty = menu_result["white_difficulty"]
    
    # Create players
    players = {
        'B': create_player(black_player_type, black_difficulty),
        'W': create_player(white_player_type, white_difficulty)
    }
    
    # Initialize game
    size = 8
    g = Game(size)
    c = BoardControl(size, size)
    
    # Set player names in the board view
    c.setPlayerNames(players['B'].get_name(), players['W'].get_name())
    
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
    
    # Handle game finish
    if g.is_finish():
        # Update final board state
        c.importModel(g.export_str())
        c.renderModel()
        
        # Print results to console
        g.view()
        result = g.get_result()
        g.result()
        print(f"\ngame history:\n{game_history}\n")
        
        # Show game over screen
        game_over = GameOver()
        game_over.set_results(
            winner=result,
            black_name=players['B'].get_name(),
            white_name=players['W'].get_name(),
            black_score=g.black_cnt,
            white_score=g.white_cnt
        )
        return game_over.run()  # Returns "menu" or "exit"
    else:
        print("Game was exited by user.")
        return "menu"  # Default to menu if game exited early

def main():
    """Main game loop - handles menu and multiple games"""
    # Initialize pygame
    pygame.init()
    
    keep_running = True
    
    while keep_running:
        # Show menu
        menu = Menu()
        result = menu.run()
        
        if result == "exit":
            keep_running = False
        else:
            # Run game with selected settings
            game_result = run_game(result)
            
            if game_result == "exit":
                keep_running = False
            # If game_result is "menu", loop continues to show menu again
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
