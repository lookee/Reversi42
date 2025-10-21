#!/usr/bin/env python3
"""
Example: book_instant Parameter Comparison

Demonstrates the difference between:
- book_instant=True (LEGACY): Book moves used instantly
- book_instant=False (NEW DEFAULT): Book moves evaluated by engine
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from Players.PlayerApocalyptron import PlayerApocalyptron
from Reversi.Game import Game

print("\n" + "="*80)
print("EXAMPLE: book_instant Parameter Comparison")
print("="*80 + "\n")

print("SCENARIO: First move of a Reversi game")
print("-" * 80)

# Create game
game = Game(8)
moves = game.get_move_list()

print(f"Valid moves: {[str(m) for m in moves]}")
print(f"Opening book has moves for initial position: Yes")
print()

# ==============================================================================
# Test 1: Legacy behavior (book_instant=True)
# ==============================================================================
print("\n" + "="*80)
print("TEST 1: LEGACY BEHAVIOR (book_instant=True)")
print("="*80 + "\n")

print("Creating player with book_instant=True...")
player_legacy = PlayerApocalyptron(
    depth=6,
    show_book_options=True,  # Show what's happening
    book_instant=True        # LEGACY: instant selection
)

print(f"\nPlayer: {player_legacy.name}")
print(f"book_instant: {player_legacy.book_instant}")
print(f"\nBehavior: Will select book move INSTANTLY (no engine evaluation)")
print("-" * 80)

# Note: Uncommenting this would actually make a move
# move_legacy = player_legacy.get_move(game, moves, None)
# print(f"Selected move: {move_legacy}")

print("\n✅ With book_instant=True:")
print("   1. Check opening book")
print("   2. If book has moves → SELECT INSTANTLY")
print("   3. NO engine evaluation")
print("   4. Fast but may miss better tactical moves")

# ==============================================================================
# Test 2: New behavior (book_instant=False)
# ==============================================================================
print("\n" + "="*80)
print("TEST 2: NEW BEHAVIOR (book_instant=False - DEFAULT)")
print("="*80 + "\n")

print("Creating player with book_instant=False...")
player_new = PlayerApocalyptron(
    depth=6,
    show_book_options=True,  # Show what's happening
    book_instant=False       # NEW: evaluate after prioritization
)

print(f"\nPlayer: {player_new.name}")
print(f"book_instant: {player_new.book_instant}")
print(f"\nBehavior: Will PRIORITIZE book moves but EVALUATE with engine")
print("-" * 80)

# Note: Uncommenting this would actually make a move
# move_new = player_new.get_move(game, moves, None)
# print(f"Selected move: {move_new}")

print("\n✅ With book_instant=False:")
print("   1. Check opening book")
print("   2. Filter book moves by score threshold (default: > 0)")
print("   3. Put best book moves at TOP of evaluation list")
print("   4. ENGINE EVALUATES ALL MOVES (book + non-book)")
print("   5. Select move with HIGHEST ENGINE SCORE")
print("   6. More intelligent - combines book + tactical analysis")

# ==============================================================================
# Summary
# ==============================================================================
print("\n" + "="*80)
print("COMPARISON SUMMARY")
print("="*80 + "\n")

print("┌─────────────────────────┬──────────────────────┬──────────────────────┐")
print("│ Feature                 │ book_instant=True    │ book_instant=False   │")
print("│                         │ (LEGACY)             │ (NEW DEFAULT)        │")
print("├─────────────────────────┼──────────────────────┼──────────────────────┤")
print("│ Book lookup             │ ✅ Yes               │ ✅ Yes               │")
print("│ Engine evaluation       │ ❌ No (instant)      │ ✅ Yes (all moves)   │")
print("│ Speed                   │ ⚡ Very fast         │ 🐢 Slower (eval)     │")
print("│ Intelligence            │ 📖 Book only         │ 🧠 Book + Engine     │")
print("│ Tactical awareness      │ ❌ Limited           │ ✅ Full              │")
print("│ Best for                │ Speed, known         │ Strength, unknown    │")
print("│                         │ positions            │ positions            │")
print("└─────────────────────────┴──────────────────────┴──────────────────────┘")

print("\n📚 RECOMMENDATION:")
print("   • Use book_instant=False (default) for STRONGEST play")
print("   • Use book_instant=True for FASTEST play in known openings")
print("\n" + "="*80 + "\n")

print("Example Configuration:")
print("-" * 80)
print("""
# Strong player (evaluates everything)
strong_player = PlayerApocalyptron(
    depth=9,
    book_instant=False  # Default - evaluate book moves
)

# Fast player (instant book selection)
fast_player = PlayerApocalyptron(
    depth=6,
    book_instant=True   # Legacy - instant selection
)
""")
print("="*80 + "\n")

