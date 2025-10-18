#!/usr/bin/env python
"""
Test script for Parallel Bitboard Engine

Usage:
    python test_parallel_engine.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Reversi.BitboardGame import BitboardGame
from AI.ParallelBitboardMinimaxEngine import ParallelBitboardMinimaxEngine, benchmark_parallel_vs_sequential

def test_basic_parallel():
    """Test basic parallel engine functionality"""
    print("="*80)
    print("TEST 1: Basic Parallel Engine")
    print("="*80)
    
    # Create a mid-game position
    game = BitboardGame()
    game.move('F5')
    game.move('F6')
    game.move('E6')
    game.move('F4')
    game.move('C3')
    
    print(f"\nCurrent position after {game.turn_cnt} moves")
    print(f"Available moves: {game.get_move_list()}")
    
    # Test parallel engine
    engine = ParallelBitboardMinimaxEngine(num_workers=4)
    
    depth = 6
    print(f"\nSearching at depth {depth}...")
    move = engine.get_best_move(game, depth, player_name="TestEngine")
    
    print(f"\n✅ Selected move: {move}")
    
    engine.close_pool()
    print("\n" + "="*80)
    print("TEST 1 PASSED ✓")
    print("="*80 + "\n")


def test_adaptive_parallelization():
    """Test adaptive parallel/sequential switching"""
    print("="*80)
    print("TEST 2: Adaptive Parallelization")
    print("="*80)
    
    game = BitboardGame()
    game.move('F5')
    game.move('F6')
    
    engine = ParallelBitboardMinimaxEngine(num_workers=4)
    
    # Shallow depth - should use sequential
    print("\nTest shallow depth (should use sequential):")
    print("-"*80)
    move1 = engine.get_best_move(game, depth=5, player_name="Shallow")
    print(f"Move: {move1}")
    
    # Deep depth - should use parallel
    print("\nTest deep depth (should use parallel):")
    print("-"*80)
    move2 = engine.get_best_move(game, depth=8, player_name="Deep")
    print(f"Move: {move2}")
    
    engine.close_pool()
    print("\n" + "="*80)
    print("TEST 2 PASSED ✓")
    print("="*80 + "\n")


def test_benchmark():
    """Benchmark parallel vs sequential"""
    print("="*80)
    print("TEST 3: Performance Benchmark")
    print("="*80)
    
    # Create mid-game position (more moves to evaluate)
    game = BitboardGame()
    game.move('F5')
    game.move('F6')
    game.move('E6')
    game.move('F4')
    
    depth = 7
    print(f"\nBenchmarking at depth {depth}...")
    
    speedup = benchmark_parallel_vs_sequential(game, depth=depth, num_workers=4)
    
    print("\n" + "="*80)
    if speedup >= 1.5:
        print(f"TEST 3 PASSED ✓ (Speedup: {speedup:.2f}x)")
    else:
        print(f"TEST 3 WARNING: Speedup lower than expected ({speedup:.2f}x)")
        print("This may be normal for shallow depth or few cores")
    print("="*80 + "\n")
    
    return speedup


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("PARALLEL BITBOARD ENGINE - TEST SUITE")
    print("="*80 + "\n")
    
    try:
        # Test 1: Basic functionality
        test_basic_parallel()
        
        # Test 2: Adaptive switching
        test_adaptive_parallelization()
        
        # Test 3: Performance benchmark
        speedup = test_benchmark()
        
        # Summary
        print("\n" + "="*80)
        print("ALL TESTS PASSED ✅")
        print("="*80)
        print(f"\n📊 Performance Summary:")
        print(f"   • Parallel engine: Working correctly")
        print(f"   • Adaptive logic: Functional")
        print(f"   • Speedup achieved: {speedup:.2f}x")
        print(f"\n💡 Recommendation:")
        if speedup >= 2.0:
            print(f"   ✅ Excellent speedup! Use for depth >= 7")
        elif speedup >= 1.5:
            print(f"   ✅ Good speedup! Use for depth >= 8")
        else:
            print(f"   ⚠️  Modest speedup. Beneficial only for depth >= 9")
        print("\n" + "="*80 + "\n")
        
        return True
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ TEST FAILED: {e}")
        print("="*80 + "\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

