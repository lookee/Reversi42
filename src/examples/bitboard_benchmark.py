#!/usr/bin/env python3
"""
Bitboard Performance Benchmark

Compares performance between standard array-based AI and bitboard AI.
Expected speedup: 50-100x
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Reversi.Game import Game, Move
from Reversi.BitboardGame import BitboardGame
from Players.AIPlayer import AIPlayer
from Players.AIPlayerBitboard import AIPlayerBitboard
import time

def benchmark_standard_ai(depth=4, num_moves=5):
    """Benchmark standard array-based AI"""
    print("="*80)
    print(f"BENCHMARK: Standard AI (depth {depth})")
    print("="*80)
    print()
    
    game = Game(8)
    player = AIPlayer(deep=depth)
    player.name = f"StandardAI-{depth}"
    
    total_time = 0
    total_nodes = 0
    
    for move_num in range(num_moves):
        moves = game.get_move_list()
        if not moves:
            break
        
        print(f"\n--- Move {move_num + 1}/{num_moves} ---")
        start = time.perf_counter()
        
        move = player.get_move(game, moves, None)
        
        elapsed = time.perf_counter() - start
        total_time += elapsed
        
        if move:
            game.move(move)
        else:
            break
    
    print(f"\nStandard AI Summary:")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Average per move: {total_time/num_moves:.3f}s")
    print()
    
    return total_time

def benchmark_bitboard_ai(depth=4, num_moves=5):
    """Benchmark bitboard-based AI"""
    print("="*80)
    print(f"BENCHMARK: Bitboard AI (depth {depth})")
    print("="*80)
    print()
    
    # Use BitboardGame directly
    game = BitboardGame()
    player = AIPlayerBitboard(deep=depth)
    player.name = f"BitboardAI-{depth}"
    
    total_time = 0
    total_nodes = 0
    
    for move_num in range(num_moves):
        moves = game.get_move_list()
        if not moves:
            break
        
        print(f"\n--- Move {move_num + 1}/{num_moves} ---")
        start = time.perf_counter()
        
        move = player.engine.get_best_move(game, depth, player_name=player.name)
        
        elapsed = time.perf_counter() - start
        total_time += elapsed
        
        if move:
            game.move(move)
        else:
            break
    
    print(f"\nBitboard AI Summary:")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Average per move: {total_time/num_moves:.3f}s")
    print()
    
    return total_time

def compare_performance():
    """Run comprehensive performance comparison"""
    print("\n" + "="*80)
    print("BITBOARD PERFORMANCE COMPARISON")
    print("="*80)
    print()
    
    depths = [4, 6, 8]
    num_moves = 5
    
    results = []
    
    for depth in depths:
        print(f"\n{'='*80}")
        print(f"TESTING DEPTH {depth}")
        print(f"{'='*80}\n")
        
        # Standard AI
        standard_time = benchmark_standard_ai(depth, num_moves)
        
        print("\n" + "-"*80 + "\n")
        
        # Bitboard AI
        bitboard_time = benchmark_bitboard_ai(depth, num_moves)
        
        # Calculate speedup
        speedup = standard_time / bitboard_time if bitboard_time > 0 else 0
        
        results.append({
            'depth': depth,
            'standard': standard_time,
            'bitboard': bitboard_time,
            'speedup': speedup
        })
        
        print("\n" + "="*80)
        print(f"DEPTH {depth} COMPARISON")
        print("="*80)
        print(f"Standard AI: {standard_time:.3f}s")
        print(f"Bitboard AI: {bitboard_time:.3f}s")
        print(f"SPEEDUP: {speedup:.1f}x faster! 🚀")
        print("="*80)
    
    # Final summary
    print("\n\n" + "="*80)
    print("FINAL PERFORMANCE SUMMARY")
    print("="*80)
    print()
    print(f"{'Depth':<10} {'Standard':<15} {'Bitboard':<15} {'Speedup':<15}")
    print("-"*80)
    
    for r in results:
        print(f"{r['depth']:<10} {r['standard']:>10.3f}s    {r['bitboard']:>10.3f}s    "
              f"{r['speedup']:>10.1f}x 🚀")
    
    avg_speedup = sum(r['speedup'] for r in results) / len(results)
    print("-"*80)
    print(f"Average Speedup: {avg_speedup:.1f}x")
    print()
    
    if avg_speedup > 50:
        print("🏆 EXCELLENT! Bitboard achieves >50x speedup!")
    elif avg_speedup > 20:
        print("✅ GREAT! Bitboard achieves >20x speedup!")
    elif avg_speedup > 10:
        print("✓ GOOD! Bitboard achieves >10x speedup!")
    else:
        print("⚠️  Speedup lower than expected, may need optimization")
    
    print("="*80)

if __name__ == "__main__":
    try:
        compare_performance()
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted.")

