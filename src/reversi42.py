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
from PauseMenu import PauseMenu
from GameIO import GameIO

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

def handle_save_game(game, black_player_name, white_player_name, game_history):
    """Handle game save"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"game_{timestamp}"
    
    print(f"\nSaving game...")
    print(f"Default filename: {default_name}.xot")
    filename = input("Enter filename (or press ENTER for default): ").strip()
    
    if not filename:
        filename = default_name
    
    try:
        filepath = GameIO.save_game(game, filename, black_player_name, white_player_name, game_history)
        print(f"✓ Game saved to: {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error saving game: {e}")
        return False

def handle_load_game():
    """Handle game load - returns game data or None"""
    saved_games = GameIO.list_saved_games()
    
    if not saved_games:
        print("\nNo saved games found.")
        input("Press ENTER to continue...")
        return None
    
    print("\nAvailable saved games:")
    for i, game_file in enumerate(saved_games, 1):
        print(f"  {i}. {game_file}")
    
    print(f"  0. Cancel")
    
    while True:
        try:
            choice = int(input(f"\nSelect game to load (0-{len(saved_games)}): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(saved_games):
                filename = saved_games[choice - 1]
                break
            print(f"Please enter a number between 0 and {len(saved_games)}")
        except ValueError:
            print("Please enter a valid number")
    
    try:
        saves_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'saves')
        filepath = os.path.join(saves_dir, filename)
        game_data = GameIO.load_game(filepath)
        print(f"✓ Game loaded from: {filepath}")
        return game_data
    except Exception as e:
        print(f"✗ Error loading game: {e}")
        input("Press ENTER to continue...")
        return None

def handle_pause_menu_action(action, g, c, game_history, players):
    """
    Handle actions from pause menu.
    
    Returns:
        tuple: (continue_game, action_result, updated_history)
        - continue_game: True to continue, False to exit game loop
        - action_result: "resume", "menu", "exit", or None
        - updated_history: Potentially modified game history
    """
    if action == "resume":
        return (True, "resume", game_history)
    
    elif action == "save":
        handle_save_game(g, players['B'].get_name(), players['W'].get_name(), game_history)
        input("Press ENTER to continue...")
        return (True, None, game_history)
    
    elif action == "load":
        game_data = handle_load_game()
        if game_data:
            # Game will be reloaded - signal to restart
            return (False, "load", game_data)
        return (True, None, game_history)
    
    elif action == "menu":
        return (False, "menu", game_history)
    
    elif action == "exit":
        return (False, "exit", game_history)
    
    return (True, None, game_history)

def run_game(menu_result, loaded_game_data=None):
    """Run a single game with the given player settings or loaded data"""
    
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
    
    if loaded_game_data:
        # Load from saved game
        g = Game(size)
        game_history = loaded_game_data['move_history']
        
        # Replay moves
        for i in range(0, len(game_history), 2):
            move_str = game_history[i:i+2]
            # Parse move (uppercase or lowercase)
            col = ord(move_str[0].upper()) - ord('A') + 1
            row = int(move_str[1])
            move = Move(col, row)
            g.move(move)
        
        print(f"✓ Loaded game with {len(game_history)//2} moves")
    else:
        # New game
        g = Game(size)
        game_history = ""
    
    c = BoardControl(size, size)
    
    # Set player names in the board view
    c.setPlayerNames(players['B'].get_name(), players['W'].get_name())
    
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
            
            # Set current turn for indicator
            c.setCurrentTurn(turn)
            
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
                print("- Arrow keys: Move cursor (in cursor mode)")
                print("- ENTER or SPACE: Select move at cursor")
                print("- ESC: Pause menu (save/load), Q: Quit")
            
            # Get move
            move = player.get_move(g, moves, c)
            
            # Check if player requested pause
            if c.should_pause:
                c.should_pause = False  # Reset flag
                pause_menu = PauseMenu()
                pause_result = pause_menu.run()
                
                # Handle pause menu action
                continue_game, action_result, game_history = handle_pause_menu_action(
                    pause_result, g, c, game_history, players
                )
                
                if not continue_game:
                    if action_result == "load":
                        # Return to main to reload game
                        return ("load", game_history)
                    else:
                        return action_result
                
                # Re-render board after pause menu actions
                c.view.refresh()  # Clear screen and redraw grid
                c.importModel(g.export_str())
                moves = g.get_move_list()  # Refresh moves (may have changed due to undo)
                for m in moves:
                    c.setCanMove(m.get_x(), m.get_y(), g.get_turn())
                c.renderModel()
                continue  # Go back to get move again
            
            # Check if player wants to exit
            if move is None:
                if c.should_exit:
                    print("Game exited by user.")
                    return "exit"
                else:
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
        
        # Check for pause/exit events during AI turns
        c.check_events()
        
        # Handle pause request
        if c.should_pause:
            c.should_pause = False  # Reset flag
            pause_menu = PauseMenu()
            pause_result = pause_menu.run()
            
            # Handle pause menu action
            continue_game, action_result, game_history = handle_pause_menu_action(
                pause_result, g, c, game_history, players
            )
            
            if not continue_game:
                if action_result == "load":
                    return ("load", game_history)
                else:
                    return action_result
            
            # Re-render board after pause menu actions
            c.view.refresh()  # Clear screen and redraw grid
            c.importModel(g.export_str())
            moves = g.get_move_list()
            for move in moves:
                c.setCanMove(move.get_x(), move.get_y(), g.get_turn())
            c.renderModel()
        
        if c.should_exit:
            print("Game exited by user.")
            return "exit"
        
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
    current_menu_result = None
    loaded_data = None
    
    while keep_running:
        # Show menu (unless we're loading a game)
        if loaded_data is None:
            menu = Menu()
            result = menu.run()
            
            if result == "exit":
                keep_running = False
                continue
            
            current_menu_result = result
        
        # Run game with selected settings or loaded data
        game_result = run_game(current_menu_result, loaded_data)
        loaded_data = None  # Reset after use
        
        # Handle game result
        if isinstance(game_result, tuple) and game_result[0] == "load":
            # Game requested load - reload with saved data
            loaded_data = game_result[1]
            # Keep current_menu_result to maintain player settings
        elif game_result == "exit":
            keep_running = False
        else:
            # "menu" or game finished normally
            current_menu_result = None
            # Loop continues to show menu again
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
