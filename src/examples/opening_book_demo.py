#!/usr/bin/env python3
"""
Demo: Grandmaster with Opening Book

This demonstrates how the Grandmaster AI uses opening theory from the book
and falls back to advanced search when out of book.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Reversi.Game import Game, Move
from Players.AIPlayerGrandmaster import AIPlayerGrandmaster
from AI.OpeningBook import get_default_opening_book

def demo_opening_book():
    """Demo the opening book lookup"""
    print("=" * 70)
    print("OPENING BOOK DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Load opening book
    book = get_default_opening_book()
    stats = book.get_statistics()
    print(f"Opening Book Statistics:")
    print(f"  Lines loaded: {stats['lines_loaded']}")
    print(f"  Total positions: {stats['total_positions']}")
    print()
    
    # Test some positions
    test_positions = [
        "",           # Start position
        "F5",         # After first move
        "F5d6",       # After second move
        "F5d6C3",     # After third move (diagonal opening)
        "F5d6C3d3",   # Fourth move
        "F5f6E6f4",   # Tiger opening
    ]
    
    print("Testing positions:")
    print("-" * 70)
    for pos in test_positions:
        book_moves = book.get_book_moves(pos)
        in_book = "✓" if book_moves else "✗"
        print(f"{in_book} Position '{pos}': {len(book_moves)} book moves")
        if book_moves:
            move_strs = [str(m) for m in book_moves[:5]]  # Show first 5
            print(f"   Options: {', '.join(move_strs)}")
            if len(book_moves) > 5:
                print(f"   ... and {len(book_moves) - 5} more")
    print()

def play_grandmaster_mirror_match():
    """Play a game between two Grandmaster players"""
    print("=" * 70)
    print("GAME: Grandmaster vs Grandmaster (Mirror Match)")
    print("=" * 70)
    print()
    
    game = Game(8)
    
    # Create players - both Grandmaster but different depths
    gm_black = AIPlayerGrandmaster(deep=5, show_book_options=False)
    gm_white = AIPlayerGrandmaster(deep=5, show_book_options=False)
    
    players = {
        'B': gm_black,
        'W': gm_white
    }
    
    move_count = 0
    max_moves = 20  # Just show first 20 moves for demo
    
    print("Playing first 20 moves...")
    print("-" * 70)
    
    while not game.is_finish() and move_count < max_moves:
        turn = game.get_turn()
        player = players[turn]
        
        moves = game.get_move_list()
        
        if len(moves) > 0:
            # Show game state
            move_num = (move_count // 2) + 1
            color = "Black" if turn == 'B' else "White"
            print(f"\nMove {move_num} ({color} - {player.name}):")
            print(f"  History: {game.history}")
            
            # Get move
            move = player.get_move(game, moves, None)
            
            if move:
                game.move(move)
                move_count += 1
            else:
                break
        else:
            game.pass_turn()
            next_moves = game.get_move_list()
            if len(next_moves) == 0:
                break
    
    print()
    print("=" * 70)
    print("Game Statistics:")
    print("=" * 70)
    
    # Show player statistics
    print(f"\n{gm_black.name} (Black):")
    print(f"  Total moves: {gm_black.total_moves}")
    print(f"  Book moves: {gm_black.book_hits}")
    if gm_black.total_moves > 0:
        print(f"  Book usage: {(gm_black.book_hits/gm_black.total_moves)*100:.1f}%")
    
    print(f"\n{gm_white.name} (White):")
    print(f"  Total moves: {gm_white.total_moves}")
    print(f"  Book moves: {gm_white.book_hits}")
    if gm_white.total_moves > 0:
        print(f"  Book usage: {(gm_white.book_hits/gm_white.total_moves)*100:.1f}%")
    
    print(f"\nFinal position:")
    print(f"  Black: {game.black_cnt}")
    print(f"  White: {game.white_cnt}")
    print()

def compare_book_performance():
    """Test Grandmaster with opening book performance"""
    print("=" * 70)
    print("GRANDMASTER PERFORMANCE WITH OPENING BOOK")
    print("=" * 70)
    print()
    
    import time
    
    game = Game(8)
    grandmaster = AIPlayerGrandmaster(deep=5, show_book_options=False)
    
    # Play a few moves and time them
    print("Testing first 10 moves with Grandmaster:")
    print("-" * 70)
    
    for i in range(10):
        moves = game.get_move_list()
        if not moves:
            break
        
        start = time.perf_counter()
        move = grandmaster.get_move(game, moves, None)
        elapsed = time.perf_counter() - start
        
        if move:
            game.move(move)
            is_book = "📚 BOOK" if grandmaster.book_hits > 0 and i < grandmaster.book_hits else "🧠 ENGINE"
            print(f"Move {i+1}: {move} - {elapsed*1000:.2f}ms ({is_book})")
    
    print()
    print("Book moves should be nearly instant (<<10ms)")
    print("Engine moves take longer but are still very fast (10-500ms)")
    print()

if __name__ == "__main__":
    # Run demos
    demo_opening_book()
    print()
    
    play_grandmaster_mirror_match()
    print()
    
    compare_book_performance()
    
    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)

