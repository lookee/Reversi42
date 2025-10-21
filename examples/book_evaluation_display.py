#!/usr/bin/env python3
"""
Example: Evolved Book Evaluation Display

Demonstrates the new elegant visualization when using book_instant=False.
Shows book moves with scores, priorities, and engine evaluation process.
"""

import sys
import os

# Silence pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from Players.PlayerApocalyptron import PlayerApocalyptron
from Reversi.Game import Game

print("\n" + "="*80)
print("EXAMPLE: Evolved Book Evaluation Display")
print("="*80 + "\n")

print("Creating player with book_instant=False and show_book_options=True...")
print()

# Create player with evaluation mode and verbose output
player = PlayerApocalyptron(
    depth=6,
    show_book_options=True,   # Enable evolved display
    book_instant=False         # Evaluation mode (default)
)

print(f"✓ Player: {player.name}")
print(f"✓ book_instant: {player.book_instant}")
print(f"✓ show_book_options: {player.show_book_options}")
print()

# Create game at initial position
game = Game(8)
moves = game.get_move_list()

print("="*80)
print("SCENARIO: First move of the game")
print("="*80)
print(f"Valid moves: {[str(m) for m in moves]}")
print()

print("What you'll see:")
print("  1. 📚 Opening Book information")
print("  2. 🔍 BOOK EVALUATION MODE display (NEW!)")
print("     • Table with book moves, scores, advantages")
print("     • ★ marks best book move")
print("     • Shows priority threshold")
print("     • Separates ON TOP moves from filtered out")
print("     • Lists non-book moves")
print("  3. Engine evaluation of ALL moves")
print("  4. Final selection by ENGINE SCORE (not just book)")
print()

print("="*80)
print("Press ENTER to get move and see the display...")
input()

# This will show the evolved display
move = player.get_move(game, moves, None)

print("\n" + "="*80)
print(f"✅ Selected move: {move}")
print("="*80 + "\n")

print("Key features of the new display:")
print("  ✓ Shows book moves with calculated scores (advantage + variety)")
print("  ✓ ★ marks the highest-scored book move")
print("  ✓ Threshold based on average score")
print("  ✓ ON TOP moves get priority in engine evaluation")
print("  ✓ Non-book moves listed separately")
print("  ✓ Clear explanation of evaluation process")
print()

print("Benefits:")
print("  • Transparent decision making")
print("  • See why moves are prioritized")
print("  • Understand book scores vs engine scores")
print("  • Debug opening book behavior")
print()

print("="*80)
print("Compare with book_instant=True (legacy):")
print("="*80)
print()

print("Creating legacy player...")
player_legacy = PlayerApocalyptron(
    depth=6,
    show_book_options=True,
    book_instant=True  # Legacy instant mode
)

# Reset game
game2 = Game(8)
moves2 = game2.get_move_list()

print("\nGetting move with instant mode...")
print("(Will select book move instantly, no evolved display)")
print()

move_legacy = player_legacy.get_move(game2, moves2, None)

print(f"\n✅ Selected move (instant): {move_legacy}")
print()

print("="*80)
print("Summary:")
print("="*80)
print()
print("book_instant=False (NEW DEFAULT):")
print("  • Shows evolved book evaluation display")
print("  • Evaluates all moves with engine")
print("  • More transparent and debuggable")
print("  • Stronger play (combines book + engine)")
print()
print("book_instant=True (LEGACY):")
print("  • Shows basic book info")
print("  • Selects instantly from book")
print("  • Faster but less transparent")
print("  • Relies only on book score")
print()

print("="*80 + "\n")

