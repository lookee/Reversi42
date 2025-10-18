#!/usr/bin/env python3

"""
Terminal Mode Demo - ASCII Art Reversi

Demonstrates the TerminalBoardView for playing in terminal/console.
Perfect for SSH sessions or terminal purists!

Usage:
    python3 src/examples/terminal_mode_demo.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Reversi.Game import Game
from Board.BoardControl import BoardControl
from ui.implementations.terminal import TerminalBoardView
from Players.HumanPlayer import HumanPlayer
from Players.AIPlayer import AIPlayer

print("\n╔═══════════════════════════════════════════════════════════════╗")
print("║          REVERSI42 - TERMINAL MODE DEMONSTRATION              ║")
print("╚═══════════════════════════════════════════════════════════════╝\n")

print("This demo uses ASCII art rendering in the terminal!")
print("No Pygame window will open - everything runs in this terminal.\n")

input("Press ENTER to start...")

# Create game with terminal view
print("\nInitializing terminal view...")
control = BoardControl(8, 8, view_class=TerminalBoardView)

# Note: For terminal view, you'd need to adapt input handling
# This is a demonstration of the view itself

# Create game
game = Game(8)

# Create players
human = HumanPlayer("You")
ai = AIPlayer(deep=3)  # Easy AI for demo

print(f"\nPlayers: {human.name} (Black) vs {ai.name} (White)")
print("\nNote: Full terminal gameplay requires input adaptation.")
print("This demo shows the ASCII rendering capability.\n")

# Render initial board
control.view.set_player_info(
    black_name=human.name,
    white_name=ai.name,
    black_count=game.black_cnt,
    white_count=game.white_cnt,
    current_turn=game.turn
)

control.view.render_board(control.model)

# Show valid moves
moves = game.get_move_list()
control.view.highlight_valid_moves(moves)
control.view.update_display()

print("\nBeautiful ASCII art rendering! ✨")
print("\nThe terminal view supports:")
print("  • Unicode box drawing characters")
print("  • ANSI color codes")
print("  • Valid move highlighting")
print("  • Cursor position tracking")
print("  • Last move indicator")
print("  • Player stats display")

print("\nFor full terminal gameplay, run:")
print("  python3 src/terminal_reversi.py")
print("  (Terminal game loop - coming soon!)")

print("\n" + "="*65)
print("Terminal view demonstration complete!")
print("="*65 + "\n")

