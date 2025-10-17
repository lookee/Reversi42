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
Example demonstrating different evaluators with the same engine.

This shows how the evaluation function affects AI behavior by running
games with the same Minimax engine but different evaluators.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Players.PlayerFactory import PlayerFactory
from Reversi.Game import Game
import pygame

def run_game_headless(black_player, white_player, game_name="Game"):
    """
    Run a game without GUI (headless mode for testing).
    
    Args:
        black_player: Player instance for Black
        white_player: Player instance for White
        game_name: Name of the game for display
        
    Returns:
        tuple: (winner, black_score, white_score, moves_count)
    """
    print(f"\n{'='*80}")
    print(f"Starting {game_name}")
    print(f"Black: {black_player.get_name()}")
    print(f"White: {white_player.get_name()}")
    print(f"{'='*80}\n")
    
    size = 8
    g = Game(size)
    
    moves_count = 0
    
    while not g.is_finish():
        turn = g.get_turn()
        player = black_player if turn == 'B' else white_player
        
        moves = g.get_move_list()
        
        if len(moves) > 0:
            # Get move from player (no control needed for headless)
            move = player.get_move(g, moves, None)
            
            if move is None:
                print("Player returned None move. Ending game.")
                break
            
            g.move(move)
            moves_count += 1
            
            # Print progress
            if moves_count % 5 == 0:
                print(f"Move {moves_count}: {move} by {player.get_name()}")
                print(f"  Score - Black: {g.black_cnt}, White: {g.white_cnt}")
        else:
            g.pass_turn()
            next_moves = g.get_move_list()
            if len(next_moves) == 0:
                break
    
    # Get final results
    result = g.get_result()
    
    print(f"\n{'='*80}")
    print(f"Game Finished: {game_name}")
    print(f"Final Score - Black: {g.black_cnt}, White: {g.white_cnt}")
    print(f"Winner: {result}")
    print(f"Total moves: {moves_count}")
    print(f"{'='*80}\n")
    
    return result, g.black_cnt, g.white_cnt, moves_count


def main():
    """
    Compare different evaluators by running games between AIs
    using the same engine (Minimax) but different evaluation functions.
    """
    
    print("\n" + "="*80)
    print("EVALUATOR COMPARISON DEMO")
    print("="*80)
    print("\nThis demo compares different evaluation functions:")
    print("- Standard: Original evaluation with mobility and corners")
    print("- Simple: Basic piece count only")
    print("- Advanced: Weighted positions with dynamic phase evaluation")
    print("\n")
    
    # Create players with different evaluators
    # All use Minimax with depth 4 for fair comparison
    difficulty = 4
    
    standard_ai = PlayerFactory.create_ai_player(
        engine_type='Minimax',
        difficulty=difficulty,
        evaluator_type='Standard'
    )
    standard_ai.name = "Minimax-Standard"
    
    simple_ai = PlayerFactory.create_ai_player(
        engine_type='Minimax',
        difficulty=difficulty,
        evaluator_type='Simple'
    )
    simple_ai.name = "Minimax-Simple"
    
    advanced_ai = PlayerFactory.create_ai_player(
        engine_type='Minimax',
        difficulty=difficulty,
        evaluator_type='Advanced'
    )
    advanced_ai.name = "Minimax-Advanced"
    
    # Run comparison games
    results = []
    
    # Game 1: Standard vs Simple
    print("\n[1/3] Standard Evaluator vs Simple Evaluator")
    result1 = run_game_headless(standard_ai, simple_ai, "Standard vs Simple")
    results.append(("Standard vs Simple", result1))
    
    # Game 2: Standard vs Advanced
    print("\n[2/3] Standard Evaluator vs Advanced Evaluator")
    result2 = run_game_headless(standard_ai, advanced_ai, "Standard vs Advanced")
    results.append(("Standard vs Advanced", result2))
    
    # Game 3: Advanced vs Simple
    print("\n[3/3] Advanced Evaluator vs Simple Evaluator")
    result3 = run_game_headless(advanced_ai, simple_ai, "Advanced vs Simple")
    results.append(("Advanced vs Simple", result3))
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY OF RESULTS")
    print("="*80)
    for game_name, (winner, black_score, white_score, moves) in results:
        print(f"\n{game_name}:")
        print(f"  Winner: {winner}")
        print(f"  Score: Black {black_score} - {white_score} White")
        print(f"  Total moves: {moves}")
    
    print("\n" + "="*80)
    print("CONCLUSIONS:")
    print("="*80)
    print("""
The results show how different evaluation functions lead to different playing styles:

- Standard Evaluator: Balances mobility and positional play
- Simple Evaluator: Greedy approach focusing only on piece count
- Advanced Evaluator: Sophisticated position weighting with game phase awareness

Each evaluator has strengths and weaknesses depending on the opponent and game phase.
This modularity allows easy experimentation and development of custom evaluators!
""")


if __name__ == "__main__":
    # Note: We don't initialize pygame for headless mode
    # The AI players don't need pygame to function
    main()

