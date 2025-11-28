"""
Script per giocare contro il giocatore RL.

Usage:
    python experimental/rl_player/play_against.py [--model MODEL_PATH] [--color B|W]
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from experimental.rl_player.player.player_rl_lightweight import PlayerRLLightweight
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def print_board(game: BitboardGame):
    """Stampa il board in formato leggibile."""
    print("\n  " + " ".join([str(i) for i in range(1, 9)]))
    for row in range(1, 9):
        line = f"{row} "
        for col in range(1, 9):
            pos = 1 << ((row - 1) * 8 + (col - 1))
            if game.black & pos:
                line += "B "
            elif game.white & pos:
                line += "W "
            else:
                line += ". "
        print(line)
    print()


def parse_move(move_str: str) -> tuple:
    """Parse move string (es. 'D3' o 'd3') -> (col, row)."""
    move_str = move_str.strip().upper()
    if len(move_str) != 2:
        return None
    
    col_char = move_str[0]
    row_char = move_str[1]
    
    # Convert column (A-H -> 1-8)
    col_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
    if col_char not in col_map:
        return None
    
    col = col_map[col_char]
    
    # Convert row (1-8)
    try:
        row = int(row_char)
        if row < 1 or row > 8:
            return None
    except ValueError:
        return None
    
    return (col, row)


def play_game(model_path: str, human_color: str = 'B'):
    """Gioca una partita contro il giocatore RL."""
    
    print("=" * 70)
    print("Play Against RL Player")
    print("=" * 70)
    print()
    
    # Setup
    rl_color = 'W' if human_color == 'B' else 'B'
    
    print(f"Human plays: {human_color}")
    print(f"RL Player plays: {rl_color}")
    print()
    
    # Load RL player
    print(f"Loading RL player from: {model_path}")
    try:
        rl_player = PlayerRLLightweight(
            model_path=model_path,
            temperature=0.1  # Low temperature for deterministic play
        )
        print("✓ RL Player loaded")
        print()
    except Exception as e:
        print(f"✗ Error loading RL player: {e}")
        return
    
    # Initialize game
    game = BitboardGame()
    move_count = 0
    
    print("Game started!")
    print_board(game)
    
    # Game loop
    while not game.is_finish():
        current_player = game.turn
        legal_moves = game.get_move_list()
        
        if len(legal_moves) == 0:
            print(f"{current_player} has no legal moves. Passing...")
            game.pass_turn()
            continue
        
        print(f"Turn: {current_player} (Move {move_count + 1})")
        print(f"Legal moves: {len(legal_moves)}")
        
        if current_player == human_color:
            # Human turn
            print("\nYour move (format: D3, or 'pass' to pass):")
            while True:
                move_input = input("> ").strip()
                
                if move_input.lower() == 'pass':
                    if len(legal_moves) == 0:
                        game.pass_turn()
                        break
                    else:
                        print("You have legal moves! Please make a move.")
                        continue
                
                move_coords = parse_move(move_input)
                if move_coords is None:
                    print("Invalid format. Use format like 'D3' (column A-H, row 1-8)")
                    continue
                
                col, row = move_coords
                # Find matching move
                move = None
                for m in legal_moves:
                    if m.get_x() == col and m.get_y() == row:
                        move = m
                        break
                
                if move is None:
                    print(f"Move ({col},{row}) is not legal. Try again.")
                    continue
                
                game.move(move)
                print(f"You played: {move_input} ({col},{row})")
                break
        else:
            # RL turn
            print("\nRL Player thinking...")
            move = rl_player.get_move(game, legal_moves)
            
            if move:
                col = move.get_x()
                row = move.get_y()
                col_char = chr(ord('A') + col - 1)
                print(f"RL Player played: {col_char}{row} ({col},{row})")
                game.move(move)
            else:
                print("RL Player passed")
                game.pass_turn()
        
        move_count += 1
        print_board(game)
    
    # Game over
    black_count = bin(game.black).count('1')
    white_count = bin(game.white).count('1')
    
    print("=" * 70)
    print("Game Over!")
    print("=" * 70)
    print(f"Final score:")
    print(f"  Black: {black_count}")
    print(f"  White: {white_count}")
    print()
    
    if black_count > white_count:
        winner = "Black"
    elif white_count > black_count:
        winner = "White"
    else:
        winner = "Draw"
    
    print(f"Winner: {winner}")
    
    if (winner == "Black" and human_color == 'B') or (winner == "White" and human_color == 'W'):
        print("🎉 Congratulations! You won!")
    elif winner == "Draw":
        print("🤝 It's a draw!")
    else:
        print("😔 RL Player won. Better luck next time!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Play against RL player")
    parser.add_argument(
        "--model",
        default="experimental/checkpoints/latest.pth",
        help="Path to model file"
    )
    parser.add_argument(
        "--color",
        choices=['B', 'W'],
        default='B',
        help="Your color (B=Black, W=White)"
    )
    
    args = parser.parse_args()
    
    # Resolve model path
    model_path = Path(args.model)
    if not model_path.is_absolute():
        model_path = project_root / model_path
    
    if not model_path.exists():
        print(f"Error: Model not found: {model_path}")
        print("\nAvailable options:")
        print("  1. Train a model first: python experimental/rl_player/train.py")
        print("  2. Export a model: python experimental/rl_player/utils/export_model.py")
        sys.exit(1)
    
    play_game(str(model_path), args.color)

