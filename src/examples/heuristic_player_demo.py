#!/usr/bin/env python3

#------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Reversi42 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Reversi42.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

"""
Demonstration of the Heuristic Player.

The Heuristic Player uses simple heuristics without full minimax search:
- Prioritizes corners and edges
- Uses position weight matrix
- Considers mobility (moves after placement)
- Evaluates piece count

Much faster than Minimax but less sophisticated. Good balance of speed and quality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Players.PlayerFactory import PlayerFactory
from Reversi.Game import Game
import time

def run_game_headless(black_player, white_player, game_name="Game"):
    """Run a game without GUI and track timing"""
    
    print(f"\n{'='*80}")
    print(f"Starting {game_name}")
    print(f"Black: {black_player.get_name()}")
    print(f"White: {white_player.get_name()}")
    print(f"{'='*80}\n")
    
    size = 8
    g = Game(size)
    
    moves_count = 0
    black_times = []
    white_times = []
    game_start = time.perf_counter()
    
    while not g.is_finish():
        turn = g.get_turn()
        player = black_player if turn == 'B' else white_player
        
        moves = g.get_move_list()
        
        if len(moves) > 0:
            # Time the move
            move_start = time.perf_counter()
            move = player.get_move(g, moves, None)
            move_time = time.perf_counter() - move_start
            
            if turn == 'B':
                black_times.append(move_time)
            else:
                white_times.append(move_time)
            
            if move is None:
                break
            
            g.move(move)
            moves_count += 1
            
            if moves_count % 10 == 0:
                print(f"Move {moves_count}: {player.get_name()} (took {move_time*1000:.2f}ms)")
        else:
            g.pass_turn()
            next_moves = g.get_move_list()
            if len(next_moves) == 0:
                break
    
    game_duration = time.perf_counter() - game_start
    result = g.get_result()
    
    print(f"\n{'='*80}")
    print(f"Game Finished: {game_name}")
    print(f"Winner: {result}")
    print(f"Score: Black {g.black_cnt} - {g.white_cnt} White")
    print(f"Total moves: {moves_count}")
    print(f"Game duration: {game_duration:.3f}s")
    
    # Timing analysis
    if black_times:
        print(f"\n{black_player.get_name()} (Black):")
        print(f"  Average move time: {sum(black_times)/len(black_times)*1000:.2f}ms")
        print(f"  Total thinking time: {sum(black_times):.3f}s")
    
    if white_times:
        print(f"\n{white_player.get_name()} (White):")
        print(f"  Average move time: {sum(white_times)/len(white_times)*1000:.2f}ms")
        print(f"  Total thinking time: {sum(white_times):.3f}s")
    
    print(f"{'='*80}\n")
    
    return result, g.black_cnt, g.white_cnt, moves_count, game_duration


def main():
    """
    Demonstrate the Heuristic Player and compare its speed with Minimax.
    """
    
    print("\n" + "="*80)
    print("HEURISTIC PLAYER DEMONSTRATION")
    print("="*80)
    print("""
The Heuristic Player uses simple evaluation without deep search:
- No minimax tree search
- Direct move evaluation
- Priority-based selection
- Fast execution

Advantages:
+ Much faster than Minimax
+ Consistent move times
+ Good for fast games

Disadvantages:
- Less strategic depth
- Misses long-term tactics
- Weaker than deep Minimax

Let's compare Heuristic vs other players!
""")
    
    # Create players
    heuristic = PlayerFactory.create_player('Heuristic', name='HeuristicPlayer')
    greedy = PlayerFactory.create_player('Greedy', name='GreedyPlayer')
    minimax_shallow = PlayerFactory.create_ai_player('Minimax', difficulty=3, evaluator_type='Standard')
    minimax_shallow.name = "Minimax-3"
    
    results = []
    
    # Game 1: Heuristic vs Greedy (should win - better strategy)
    print("\n[1/3] Heuristic vs Greedy")
    print("Expected: Heuristic should win with better move evaluation")
    result1 = run_game_headless(heuristic, greedy, "Heuristic vs Greedy")
    results.append(("Heuristic vs Greedy", result1))
    
    # Game 2: Heuristic vs Minimax-3 (competitive)
    print("\n[2/3] Heuristic vs Minimax (Depth 3)")
    print("Expected: Close game, Minimax may have edge")
    result2 = run_game_headless(heuristic, minimax_shallow, "Heuristic vs Minimax-3")
    results.append(("Heuristic vs Minimax-3", result2))
    
    # Game 3: Minimax-3 vs Heuristic (reversed)
    print("\n[3/3] Minimax-3 vs Heuristic (Reversed colors)")
    result3 = run_game_headless(minimax_shallow, heuristic, "Minimax-3 vs Heuristic")
    results.append(("Minimax-3 vs Heuristic", result3))
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY OF RESULTS")
    print("="*80)
    for game_name, (winner, black_score, white_score, moves, duration) in results:
        print(f"\n{game_name}:")
        print(f"  Winner: {winner}")
        print(f"  Score: Black {black_score} - {white_score} White")
        print(f"  Duration: {duration:.3f}s")
    
    print("\n" + "="*80)
    print("CONCLUSIONS:")
    print("="*80)
    print("""
The Heuristic Player offers an excellent balance:

✓ Faster than Minimax (no deep tree search)
✓ Smarter than Greedy (considers position, not just immediate gains)
✓ Consistent performance (predictable move times)
✓ Good for medium difficulty

Use cases:
- Fast games where deep search isn't needed
- Mobile or resource-constrained environments
- Teaching intermediate strategy
- Baseline for testing stronger AIs

The Heuristic Player is perfect when you want decent play without
the computational cost of deep minimax search!
""")


if __name__ == "__main__":
    main()

