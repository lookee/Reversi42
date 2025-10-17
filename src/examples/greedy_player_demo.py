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
Demonstration of the Greedy Player strategy.

The Greedy Player always chooses the move that immediately captures
the most pieces. This demo shows why this strategy is often poor
in Reversi, as it doesn't consider long-term positional advantages.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Players.PlayerFactory import PlayerFactory
from Reversi.Game import Game

def run_game_headless(black_player, white_player, game_name="Game", verbose=True):
    """
    Run a game without GUI (headless mode).
    
    Args:
        black_player: Player instance for Black
        white_player: Player instance for White
        game_name: Name of the game for display
        verbose: If True, print detailed move information
        
    Returns:
        tuple: (winner, black_score, white_score, moves_count)
    """
    if verbose:
        print(f"\n{'='*80}")
        print(f"Starting {game_name}")
        print(f"Black: {black_player.get_name()}")
        print(f"White: {white_player.get_name()}")
        print(f"{'='*80}\n")
    
    size = 8
    g = Game(size)
    
    moves_count = 0
    move_history = []
    
    while not g.is_finish():
        turn = g.get_turn()
        player = black_player if turn == 'B' else white_player
        
        moves = g.get_move_list()
        
        if len(moves) > 0:
            # Save state before move
            black_before = g.black_cnt
            white_before = g.white_cnt
            
            # Get move from player
            move = player.get_move(g, moves, None)
            
            if move is None:
                if verbose:
                    print("Player returned None move. Ending game.")
                break
            
            g.move(move)
            moves_count += 1
            
            # Calculate pieces captured
            if turn == 'B':
                captured = g.black_cnt - black_before
            else:
                captured = g.white_cnt - white_before
            
            move_history.append({
                'move': move,
                'player': player.get_name(),
                'turn': turn,
                'captured': captured,
                'black_cnt': g.black_cnt,
                'white_cnt': g.white_cnt
            })
            
            # Print progress
            if verbose and moves_count % 5 == 0:
                print(f"Move {moves_count}: {move} by {player.get_name()} (captured {captured} pieces)")
                print(f"  Score - Black: {g.black_cnt}, White: {g.white_cnt}")
        else:
            g.pass_turn()
            next_moves = g.get_move_list()
            if len(next_moves) == 0:
                break
    
    # Get final results
    result = g.get_result()
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"Game Finished: {game_name}")
        print(f"Final Score - Black: {g.black_cnt}, White: {g.white_cnt}")
        print(f"Winner: {result}")
        print(f"Total moves: {moves_count}")
        print(f"{'='*80}\n")
    
    return result, g.black_cnt, g.white_cnt, moves_count, move_history


def main():
    """
    Demonstrate the Greedy Player against various opponents.
    """
    
    print("\n" + "="*80)
    print("GREEDY PLAYER DEMONSTRATION")
    print("="*80)
    print("""
The Greedy Player always chooses the move that captures the most pieces immediately.
While this seems intuitive, it's often a poor strategy in Reversi because:

1. It ignores positional advantages (corners, edges)
2. It doesn't consider mobility (number of available moves)
3. It can give the opponent better positions
4. Early piece count doesn't predict the final outcome

Let's see how the Greedy Player performs against different opponents!
""")
    
    # Create players
    greedy = PlayerFactory.create_player('Greedy', name='Greedy')
    monkey = PlayerFactory.create_player('Monkey', name='Monkey')
    minimax_ai = PlayerFactory.create_ai_player('Minimax', difficulty=4, evaluator_type='Standard')
    minimax_ai.name = "Minimax-Standard-4"
    
    results = []
    
    # Game 1: Greedy vs Monkey (should win - Greedy is better than random)
    print("\n[1/3] Greedy vs Monkey (Random)")
    print("Expected: Greedy should win against random play")
    result1 = run_game_headless(greedy, monkey, "Greedy vs Monkey", verbose=True)
    results.append(("Greedy vs Monkey", result1))
    
    # Game 2: Greedy vs Minimax AI (should lose - Minimax considers strategy)
    print("\n[2/3] Greedy vs Minimax AI (Depth 4)")
    print("Expected: Minimax should win with better strategic play")
    result2 = run_game_headless(greedy, minimax_ai, "Greedy vs Minimax", verbose=True)
    results.append(("Greedy vs Minimax", result2))
    
    # Game 3: Minimax vs Greedy (reversed colors)
    print("\n[3/3] Minimax AI vs Greedy (Reversed colors)")
    print("Expected: Minimax should still win regardless of color")
    result3 = run_game_headless(minimax_ai, greedy, "Minimax vs Greedy", verbose=True)
    results.append(("Minimax vs Greedy", result3))
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY OF RESULTS")
    print("="*80)
    for game_name, (winner, black_score, white_score, moves, history) in results:
        print(f"\n{game_name}:")
        print(f"  Winner: {winner}")
        print(f"  Score: Black {black_score} - {white_score} White")
        print(f"  Total moves: {moves}")
    
    print("\n" + "="*80)
    print("CONCLUSIONS:")
    print("="*80)
    print("""
The results demonstrate that the Greedy strategy:

✓ Beats random play (Monkey) - having any strategy is better than none
✗ Loses to strategic play (Minimax) - short-term gains lead to long-term losses

The Greedy Player is useful as:
- A teaching tool to show why immediate gains aren't always best
- A baseline opponent for testing
- An example of a simple, understandable strategy

In Reversi, the player with fewer pieces in the midgame often has more
mobility and better positions, leading to victory in the endgame!
""")


if __name__ == "__main__":
    main()

