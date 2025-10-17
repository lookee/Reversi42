#!/usr/bin/env python3
"""
Demo: AIPlayerBook with Opening Book

This demonstrates how the AIPlayerBook uses opening theory from the book
and falls back to minimax when out of book.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Reversi.Game import Game, Move
from Players.AIPlayerBook import AIPlayerBook
from Players.AIPlayer import AIPlayer
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

def play_book_vs_standard():
    """Play a game between AIPlayerBook and standard AIPlayer"""
    print("=" * 70)
    print("GAME: AIPlayerBook vs Standard AI")
    print("=" * 70)
    print()
    
    game = Game(8)
    
    # Create players
    book_player = AIPlayerBook(deep=4)
    standard_player = AIPlayer(deep=4)
    
    players = {
        'B': book_player,
        'W': standard_player
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
    
    # Show book player statistics
    if hasattr(book_player, 'get_statistics'):
        stats = book_player.get_statistics()
        print(f"\n{book_player.name}:")
        print(f"  Moves from book: {stats['moves_from_book']}")
        print(f"  Moves from engine: {stats['moves_from_engine']}")
        print(f"  Book usage: {stats['book_percentage']:.1f}%")
        if stats['left_book_at_move']:
            print(f"  Left book at move: {stats['left_book_at_move']}")
    
    print(f"\nFinal position:")
    print(f"  Black: {game.black_cnt}")
    print(f"  White: {game.white_cnt}")
    print()

def compare_book_performance():
    """Compare AIPlayerBook vs standard AI performance"""
    print("=" * 70)
    print("PERFORMANCE COMPARISON")
    print("=" * 70)
    print()
    
    import time
    
    game = Game(8)
    book_player = AIPlayerBook(deep=4)
    
    # Play a few moves and time them
    print("Testing first 5 moves with AIPlayerBook:")
    print("-" * 70)
    
    for i in range(5):
        moves = game.get_move_list()
        if not moves:
            break
        
        start = time.perf_counter()
        move = book_player.get_move(game, moves, None)
        elapsed = time.perf_counter() - start
        
        if move:
            game.move(move)
            print(f"Move {i+1}: {move} ({elapsed*1000:.2f}ms)")
    
    print()
    print("Book moves should be nearly instant (<<1ms)")
    print("Engine moves typically take longer (>100ms)")
    print()

if __name__ == "__main__":
    # Run demos
    demo_opening_book()
    print()
    
    play_book_vs_standard()
    print()
    
    compare_book_performance()
    
    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)

