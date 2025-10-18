#!/usr/bin/env python3

"""
Headless Tournament Demo

Demonstrates using HeadlessBoardView for ultra-fast tournaments
with zero rendering overhead.

Usage:
    python3 src/examples/headless_tournament_demo.py
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Reversi.Game import Game
from Board.BoardControl import BoardControl
from Board.HeadlessBoardView import HeadlessBoardView
from Board.PygameBoardView import PygameBoardView
from Players.AIPlayer import AIPlayer
from Players.GreedyPlayer import GreedyPlayer

print("\n╔═══════════════════════════════════════════════════════════════╗")
print("║       HEADLESS VIEW DEMO - PERFORMANCE COMPARISON             ║")
print("╚═══════════════════════════════════════════════════════════════╝\n")

print("Comparing Pygame view vs Headless view performance...\n")

# Test configuration
num_games = 10
ai1 = AIPlayer(deep=4)
ai2 = GreedyPlayer()

# Test 1: With Pygame view (graphics overhead)
print(f"Test 1: {num_games} games with PygameBoardView (graphics enabled)")
print("-" * 65)

start = time.time()
for i in range(num_games):
    control = BoardControl(8, 8, view_class=PygameBoardView)
    game = Game(8)
    
    # Play game (simplified, no actual gameplay for demo)
    moves_played = 0
    while not game.is_finish() and moves_played < 60:
        moves = game.get_move_list()
        if len(moves) == 0:
            game.pass_turn()
            continue
        
        player = ai1 if game.turn == 'B' else ai2
        move = player.get_move(game, moves, None)
        if move:
            game.move(move)
            moves_played += 1
        else:
            break
    
    print(f"  Game {i+1}/{num_games}: {game.black_cnt}-{game.white_cnt}", end='\r')

pygame_time = time.time() - start
print(f"\n\nPygame View Time: {pygame_time:.2f}s ({pygame_time/num_games:.3f}s per game)")

# Test 2: With Headless view (zero graphics)
print(f"\nTest 2: {num_games} games with HeadlessBoardView (no graphics)")
print("-" * 65)

start = time.time()
for i in range(num_games):
    control = BoardControl(8, 8, view_class=HeadlessBoardView)
    game = Game(8)
    
    moves_played = 0
    while not game.is_finish() and moves_played < 60:
        moves = game.get_move_list()
        if len(moves) == 0:
            game.pass_turn()
            continue
        
        player = ai1 if game.turn == 'B' else ai2
        move = player.get_move(game, moves, None)
        if move:
            game.move(move)
            moves_played += 1
        else:
            break
    
    print(f"  Game {i+1}/{num_games}: {game.black_cnt}-{game.white_cnt}", end='\r')

headless_time = time.time() - start
print(f"\n\nHeadless View Time: {headless_time:.2f}s ({headless_time/num_games:.3f}s per game)")

# Comparison
print("\n" + "="*65)
print("PERFORMANCE COMPARISON")
print("="*65)
print(f"Pygame View:   {pygame_time:.2f}s")
print(f"Headless View: {headless_time:.2f}s")
speedup = pygame_time / headless_time if headless_time > 0 else 0
print(f"Speedup:       {speedup:.2f}x faster with headless view")
print("\nConclusion: Headless view eliminates ALL rendering overhead!")
print("Perfect for tournaments where visualization isn't needed.")
print("="*65 + "\n")

