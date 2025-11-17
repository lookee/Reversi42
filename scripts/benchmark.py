#!/usr/bin/env python3
"""
Performance benchmarks for Reversi42
"""
import sys
import os
import time
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move
from Players.PlayerApocalyptron import PlayerApocalyptron
from copy import deepcopy

# Set headless mode
os.environ['REVERSI42_VIEW'] = 'headless'

def benchmark_bitboard_operations():
    """Benchmark bitboard operations"""
    print("\n→ Bitboard Operations")
    
    game = BitboardGame()
    iterations = 10000
    
    # Move generation benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        moves = game.get_valid_moves()
    elapsed = (time.perf_counter() - start) / iterations * 1e9
    print(f"  Move generation: {elapsed:.1f} ns/op")
    
    # Make move benchmark (using D3 = Move(4, 3))
    test_move = Move(4, 3)  # D3
    start = time.perf_counter()
    for _ in range(iterations):
        test_game = deepcopy(game)
        if test_game.valid_move(test_move):
            test_game.move(test_move)
    elapsed = (time.perf_counter() - start) / iterations * 1e9
    print(f"  Make move: {elapsed:.1f} ns/op")
    
    # Score calculation
    start = time.perf_counter()
    for _ in range(iterations):
        score = (game.black_cnt, game.white_cnt)
    elapsed = (time.perf_counter() - start) / iterations * 1e9
    print(f"  Get score: {elapsed:.1f} ns/op")

def benchmark_ai_performance():
    """Benchmark AI performance at different depths"""
    print("\n→ AI Performance")
    
    game = BitboardGame()
    
    # Import config builder to disable parallel search
    from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder
    
    for depth in [6, 9]:
        # Disable parallel search for benchmark to avoid multiprocessing issues
        config_builder = (
            ApocalyptronConfigBuilder()
            .with_depth(depth)
            .enable_iterative_deepening()
            .enable_all_optimizations()
            .enable_parallel(False)  # Disable parallel to avoid multiprocessing issues
            .quiet_mode()  # Disable output for cleaner benchmark output
        )
        player = PlayerApocalyptron(depth=depth, config_builder=config_builder)
        
        moves = game.get_move_list()
        
        start = time.perf_counter()
        move = player.get_move(game, moves, None)
        elapsed = time.perf_counter() - start
        
        print(f"  Depth {depth}: {elapsed:.3f} seconds")
        
        if depth == 6 and elapsed > 0.5:
            print(f"    ⚠️  Slower than expected (target: <0.5s)")
        elif depth == 9 and elapsed > 2.0:
            print(f"    ⚠️  Slower than expected (target: <2.0s)")
        else:
            print(f"    ✅ Within performance targets")

def benchmark_memory_usage():
    """Benchmark memory usage"""
    print("\n→ Memory Usage")
    
    game = BitboardGame()
    game_size = sys.getsizeof(game)
    print(f"  BitboardGame: {game_size} bytes")
    
    if game_size < 1024:
        print(f"    ✅ Optimal size (<1KB)")
    else:
        print(f"    ⚠️  Larger than expected")
    
    # Disable parallel search for memory benchmark
    from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder
    config_builder = (
        ApocalyptronConfigBuilder()
        .with_depth(9)
        .enable_parallel(False)
        .quiet_mode()
    )
    player = PlayerApocalyptron(depth=9, config_builder=config_builder)
    player_size = sys.getsizeof(player)
    print(f"  PlayerApocalyptron: {player_size} bytes")

def benchmark_full_game():
    """Benchmark full game completion"""
    print("\n→ Full Game Completion")
    
    game = BitboardGame()
    
    # Import config builder to disable parallel search
    from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder
    
    # Use depth 6 for faster benchmark, disable parallel search
    config_builder = (
        ApocalyptronConfigBuilder()
        .with_depth(6)
        .enable_iterative_deepening()
        .enable_all_optimizations()
        .enable_parallel(False)  # Disable parallel to avoid multiprocessing issues
        .quiet_mode()  # Disable output for cleaner benchmark output
    )
    black = PlayerApocalyptron(depth=6, config_builder=config_builder)
    white = PlayerApocalyptron(depth=6, config_builder=config_builder)
    
    start = time.perf_counter()
    move_count = 0
    
    while not game.is_finish() and move_count < 60:
        moves = game.get_move_list()
        
        if not moves:
            game = game.pass_turn()
            continue
        
        player = black if game.turn == "B" else white
        move = player.get_move(game, moves, None)
        if move:
            game.move(move)
            move_count += 1
    
    elapsed = time.perf_counter() - start
    black_score = game.black_cnt
    white_score = game.white_cnt
    
    print(f"  Game completed in {elapsed:.2f} seconds")
    print(f"  Moves: {move_count}")
    print(f"  Final score: Black {black_score} - White {white_score}")
    if move_count > 0:
        print(f"  Time per move: {elapsed/move_count:.3f} seconds")
    
    if elapsed < 60:
        print(f"    ✅ Excellent performance (<60s)")
    else:
        print(f"    ⚠️  Slower than target")

if __name__ == '__main__':
    print("⚡ Performance Benchmarks")
    print("======================================")
    
    benchmark_bitboard_operations()
    benchmark_ai_performance()
    benchmark_memory_usage()
    benchmark_full_game()
    
    print("\n======================================")
    print("✅ Benchmark suite completed")

