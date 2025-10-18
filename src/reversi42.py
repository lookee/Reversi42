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
import argparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from pygame.locals import *

from Reversi.Game import Game
from Reversi.Game import Move

from Players.PlayerFactory import PlayerFactory
from Players.HumanPlayer import HumanPlayer
from Board.BoardControl import BoardControl
from Board.ViewFactory import ViewFactory
from Board.PygameBoardView import PygameBoardView
from ui.implementations.terminal import TerminalBoardView  # New location
from ui.implementations.headless import HeadlessBoardView  # New location
from Menu import Menu
from GameOver import GameOver
from PauseMenu import PauseMenu
from GameIO import GameIO
from AI.OpeningBook import get_default_opening_book

def create_player(player_type, difficulty=6, engine_type='Minimax'):
    """Create a player instance using the PlayerFactory"""
    try:
        if player_type == "Alpha-Beta AI":
            return PlayerFactory.create_ai_player(engine_type, difficulty)
        elif player_type == "Opening Scholar":
            # Create AIPlayerBook with specified difficulty
            return PlayerFactory.create_player(player_type, deep=difficulty)
        elif player_type == "Bitboard Blitz":
            # Create AIPlayerBitboard with specified difficulty
            return PlayerFactory.create_player(player_type, deep=difficulty)
        elif player_type == "The Oracle":
            # Create AIPlayerBitboardBook with specified difficulty
            return PlayerFactory.create_player(player_type, deep=difficulty, show_book_options=True)
        elif player_type == "Parallel Oracle":
            # Create AIPlayerBitboardBookParallel with specified difficulty
            return PlayerFactory.create_player(player_type, deep=difficulty, show_book_options=True)
        elif player_type == "Grandmaster":
            # Create AIPlayerGrandmaster with specified difficulty
            return PlayerFactory.create_player(player_type, deep=difficulty, show_book_options=True)
        else:
            return PlayerFactory.create_player(player_type)
    except ValueError as e:
        print(f"Error creating player: {e}")
        return PlayerFactory.create_player("Human Player")  # Default fallback

def handle_save_game(game, black_player_name, white_player_name, game_history):
    """Handle game save with graphical dialog"""
    from datetime import datetime
    from DialogBox import TextInputDialog, MessageDialog
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"game_{timestamp}"
    
    # Show text input dialog
    dialog = TextInputDialog(
        prompt="Enter filename to save:",
        default_text=default_name
    )
    
    filename = dialog.run()
    
    if filename is None or filename.strip() == "":
        # User cancelled or empty
        return False
    
    filename = filename.strip()
    
    try:
        filepath = GameIO.save_game(game, filename, black_player_name, white_player_name, game_history)
        
        # Show success message
        msg_dialog = MessageDialog(
            title="Save Successful",
            message=f"Game saved to:\n{os.path.basename(filepath)}",
            message_type="success"
        )
        msg_dialog.run()
        
        return True
    except Exception as e:
        # Show error message
        msg_dialog = MessageDialog(
            title="Save Error",
            message=f"Error saving game:\n{str(e)}",
            message_type="error"
        )
        msg_dialog.run()
        
        return False

def handle_load_game():
    """Handle game load with graphical dialog - returns game data or None"""
    from DialogBox import ListSelectDialog, MessageDialog
    
    saved_games = GameIO.list_saved_games()
    
    if not saved_games:
        # Show "no games" message
        msg_dialog = MessageDialog(
            title="No Saved Games",
            message="No saved games found.\nPlay a game and save it first!",
            message_type="info"
        )
        msg_dialog.run()
        return None
    
    # Show selection dialog
    dialog = ListSelectDialog(
        title="Select game to load:",
        items=saved_games,
        allow_cancel=True
    )
    
    choice = dialog.run()
    
    if choice is None:
        # User cancelled
        return None
    
    filename = saved_games[choice]
    
    try:
        # GameIO.load_game handles path construction
        game_data = GameIO.load_game(filename)
        
        # Show success message
        msg_dialog = MessageDialog(
            title="Load Successful",
            message=f"Game loaded from:\n{filename}",
            message_type="success"
        )
        msg_dialog.run()
        
        return game_data
    except Exception as e:
        # Show error message
        msg_dialog = MessageDialog(
            title="Load Error",
            message=f"Error loading game:\n{str(e)}",
            message_type="error"
        )
        msg_dialog.run()
        
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
        # No need for input() - dialog handles user interaction
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

def run_game(menu_result, loaded_game_data=None, view_class=None):
    """Run a single game with the given player settings or loaded data"""
    
    # Get view class from parameter or global
    if view_class is None:
        view_class = globals().get('SELECTED_VIEW_CLASS', PygameBoardView)
    
    # Check if players are already created (terminal mode) or need creation (menu mode)
    if isinstance(menu_result.get("black_player"), str):
        # Menu mode - players are type strings, need to create them
        black_player_type = menu_result["black_player"]
        white_player_type = menu_result["white_player"]
        black_difficulty = menu_result["black_difficulty"]
        white_difficulty = menu_result["white_difficulty"]
        
        # Create players
        players = {
            'B': create_player(black_player_type, black_difficulty),
            'W': create_player(white_player_type, white_difficulty)
        }
    else:
        # Terminal mode - players are already created objects
        players = {
            'B': menu_result["black_player"],
            'W': menu_result["white_player"]
        }
    
    show_opening = menu_result.get("show_opening", True)  # Default True
    
    # Load opening book if show_opening is enabled
    opening_book = None
    if show_opening:
        opening_book = get_default_opening_book()
    
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
    
    # Create BoardControl with selected view class
    print(f"[INFO] Creating BoardControl with view: {view_class.__name__}")
    c = BoardControl(size, size, view_class=view_class)
    
    # Set opening book in BoardControl if enabled
    if opening_book:
        c.opening_book = opening_book
        c.show_opening = True
    else:
        c.opening_book = None
        c.show_opening = False
    
    # Set player names in the board view
    c.setPlayerNames(players['B'].get_name(), players['W'].get_name())
    
    last_move = None
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    game_ended = False  # Track if game ended naturally
    
    while running:
        # Check if game is finished
        if g.is_finish():
            game_ended = True
            break
            
        turn = g.get_turn()
        player = players[turn]
        
        print(f"{player.get_name()} is moving...")
        
        moves = g.get_move_list()
        
        if len(moves) > 0:
            # Import board position
            c.importModel(g.export_str())
            
            # Show all available moves (unified method - no duplication)
            c.display_available_moves(g, moves, turn)
            
            # Set current turn for indicator
            c.setCurrentTurn(turn)
            
            # Render board
            c.renderModel()
            c.cursorWait()
            
            # Compact game info on single line
            from ui.implementations.terminal import TerminalBoardView
            if isinstance(c.view, TerminalBoardView):
                # For terminal mode: compact single-line info
                if last_move:
                    print(f"Last: {last_move}  |  History: {game_history if game_history else '(start)'}")
                else:
                    print(f"History: {game_history if game_history else '(start)'}")
            else:
                # For pygame mode: original verbose output
                print(f"\ngame history:\n{game_history}\n")
                print(f"last move: {last_move}")
                
                # Instructions for cursor navigation (pygame only)
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
                
                # Show moves (unified method)
                c.display_available_moves(g, moves, g.get_turn())
                
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
                game_ended = True  # Mark as naturally ended
                break
        
        # Check for pause/exit events during AI turns
        c.check_events()
        
        # Don't exit if game just finished naturally
        if c.should_exit and not g.is_finish():
            print("Game exited by user during play.")
            return "exit"
        
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
            
            # Show moves (unified method)
            c.display_available_moves(g, moves, g.get_turn())
            
            c.renderModel()
        
        # Removed duplicate check - already handled above
        
        clock.tick(60)  # Limit to 60 FPS
    
    # Handle game finish
    if game_ended or g.is_finish():
        print("\n🏁 Game finished! Showing results...")
        
        # Clear event queue to avoid immediate exit from GameOver screen
        pygame.event.clear()
        
        # Wait a moment for any pending events to settle
        pygame.time.wait(100)
        
        # Update final board state
        c.importModel(g.export_str())
        c.renderModel()
        
        # Print results to console
        g.view()
        result = g.get_result()
        g.result()
        
        # Compact history display for terminal mode
        from ui.implementations.terminal import TerminalBoardView
        if isinstance(c.view, TerminalBoardView):
            print(f"Final History: {game_history}")
        else:
            print(f"\ngame history:\n{game_history}\n")
        
        # Show game over screen
        print("Creating GameOver screen...")
        try:
            # Clear events again right before showing GameOver
            pygame.event.clear()
            
            game_over = GameOver()
            game_over.set_results(
                winner=result,
                black_name=players['B'].get_name(),
                white_name=players['W'].get_name(),
                black_score=g.black_cnt,
                white_score=g.white_cnt
            )
            print("Showing GameOver screen...")
            return game_over.run()  # Returns "menu" or "exit"
        except Exception as e:
            print(f"Error showing game over screen: {e}")
            import traceback
            traceback.print_exc()
            return "menu"
    else:
        print("Game was exited by user.")
        return "menu"  # Default to menu if game exited early

def main():
    """Main game loop - handles menu and multiple games"""
    # Get selected view class (from command line args)
    view_class = globals().get('SELECTED_VIEW_CLASS', PygameBoardView)
    
    # Initialize pygame
    pygame.init()
    
    # Check if using non-Pygame view
    using_terminal = view_class == TerminalBoardView
    
    keep_running = True
    current_menu_result = None
    loaded_data = None
    
    while keep_running:
        # For terminal mode, skip Pygame menu and use CLI config
        if using_terminal and loaded_data is None:
            print("\n" + "="*70)
            print("TERMINAL MODE - GAME CONFIGURATION")
            print("="*70)
            
            # Get all available players from metadata (same as Pygame menu)
            # But replace Human Player with Terminal Human
            all_metadata = PlayerFactory.get_all_player_metadata()
            
            # Import TerminalHumanPlayer from new location
            from ui.implementations.terminal import TerminalHumanPlayer
            terminal_human_meta = TerminalHumanPlayer.PLAYER_METADATA.copy()
            
            enabled_players = {}
            for name, meta in all_metadata.items():
                if meta['enabled']:
                    if name == 'Human Player':
                        # Replace with Terminal Human
                        enabled_players['Terminal Human'] = terminal_human_meta
                    else:
                        enabled_players[name] = meta
            
            # Build player options list
            player_options = []
            for name, meta in enabled_players.items():
                player_options.append({
                    'name': name,
                    'description': meta['description'],
                    'has_difficulty': len(meta.get('parameters', [])) > 0
                })
            
            # Display all available players
            print("\nAvailable Players:")
            for i, player in enumerate(player_options, 1):
                print(f"  {i}. {player['name']:<25} - {player['description']}")
            
            # Get player selections
            def select_player(color):
                while True:
                    try:
                        choice = input(f"\n{color} player (1-{len(player_options)}): ").strip()
                        if not choice:
                            # Default: AI for terminal
                            return create_player("Alpha-Beta AI", 6)
                        
                        idx = int(choice) - 1
                        if 0 <= idx < len(player_options):
                            player_info = player_options[idx]
                            player_name = player_info['name']
                            
                            # Special case: Terminal Human
                            if player_name == 'Terminal Human':
                                from ui.implementations.terminal import TerminalHumanPlayer
                                return TerminalHumanPlayer(name=f"{color}")
                            
                            # If player has difficulty parameter, ask for it
                            if player_info['has_difficulty']:
                                diff = input(f"  Difficulty level (1-10, default 6): ").strip()
                                difficulty = int(diff) if diff else 6
                                difficulty = max(1, min(12, difficulty))
                            else:
                                difficulty = 6
                            
                            return create_player(player_name, difficulty)
                        else:
                            print(f"  Invalid choice. Enter 1-{len(player_options)}")
                    except ValueError:
                        print("  Invalid input. Enter a number.")
                    except Exception as e:
                        print(f"  Error: {e}")
            
            # Select players
            black_p = select_player("Black")
            white_p = select_player("White")
            
            # Ask about opening book
            show_book = input("\nShow opening book? (y/N): ").strip().lower()
            show_opening = show_book in ['y', 'yes']
            
            print(f"\n✓ Black: {black_p.name}")
            print(f"✓ White: {white_p.name}")
            print(f"✓ Opening book: {'Enabled' if show_opening else 'Disabled'}")
            print()
            
            # Create result matching menu structure
            result = {
                'action': 'start',
                'black_player': black_p,
                'white_player': white_p,
                'black_difficulty': 6,
                'white_difficulty': 6,
                'show_opening': show_opening
            }
            
            current_menu_result = result
            
        # Show Pygame menu for GUI mode
        elif loaded_data is None:
            menu = Menu()
            result = menu.run()
            
            if result == "exit":
                keep_running = False
                continue
            
            current_menu_result = result
        
        # Run game with selected settings or loaded data (pass view_class)
        game_result = run_game(current_menu_result, loaded_data, view_class=view_class)
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

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Reversi42 - Ultra-Fast Reversi with Modular View System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
View Types:
  pygame   - Graphical interface with Pygame (default)
  terminal - ASCII art in terminal (SSH-friendly)
  headless - No rendering (maximum speed)

Examples:
  %(prog)s                    # Start with default Pygame view
  %(prog)s --view terminal    # Use ASCII art terminal view
  %(prog)s --view headless    # Headless mode (no graphics)
  %(prog)s --list-views       # Show available view types

Version 3.1.0 - Modular View Architecture
        """
    )
    
    parser.add_argument(
        '--view', '-v',
        type=str,
        default='pygame',
        choices=['pygame', 'terminal', 'headless', 'gui', 'console', 'none'],
        help='View type to use (default: pygame)'
    )
    
    parser.add_argument(
        '--list-views',
        action='store_true',
        help='List available view types and exit'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Reversi42 v3.1.0 - Modular View Architecture'
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Handle --list-views
    if args.list_views:
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║          REVERSI42 - AVAILABLE VIEW TYPES                     ║")
        print("╚═══════════════════════════════════════════════════════════════╝\n")
        
        views_info = [
            ("pygame (gui)", "Graphical interface with Pygame", "Interactive play, learning", "Default"),
            ("terminal (console)", "ASCII art in terminal", "SSH sessions, terminal purists", ""),
            ("headless (none)", "No rendering", "Tournaments, testing, maximum speed", ""),
        ]
        
        for view, desc, use_case, note in views_info:
            print(f"  {view:20} - {desc}")
            print(f"  {'':20}   Use for: {use_case}")
            if note:
                print(f"  {'':20}   {note}")
            print()
        
        print("Usage:")
        print("  reversi42 --view pygame     # Default graphical mode")
        print("  reversi42 --view terminal   # ASCII art mode")
        print("  reversi42 --view headless   # No graphics (testing)")
        print()
        sys.exit(0)
    
    # Map view argument to view class
    view_mapping = {
        'pygame': PygameBoardView,
        'gui': PygameBoardView,
        'terminal': TerminalBoardView,
        'console': TerminalBoardView,
        'headless': HeadlessBoardView,
        'none': HeadlessBoardView,
    }
    
    selected_view = view_mapping.get(args.view, PygameBoardView)
    
    # Display startup message for non-pygame views
    if args.view in ['terminal', 'console']:
        print("\n" + "="*70)
        print("REVERSI42 - TERMINAL MODE")
        print("="*70)
        print("\nASCII Art Terminal View - Keyboard Controls")
        print("Note: Terminal mode is functional but experimental.")
        print("For full GUI experience, use: reversi42 --view pygame")
        print("="*70 + "\n")
    
    elif args.view in ['headless', 'none']:
        print("\n" + "="*70)
        print("REVERSI42 - HEADLESS MODE")
        print("="*70)
        print("\nHeadless mode is for automated testing/tournaments.")
        print("No interactive play is available in this mode.")
        print("For interactive play, use: reversi42 --view pygame")
        print("="*70 + "\n")
        sys.exit(0)
    
    # Store view class in a global for access in main()
    global SELECTED_VIEW_CLASS
    SELECTED_VIEW_CLASS = selected_view
    
    main()
