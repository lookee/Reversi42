#!/usr/bin/env python3

"""
Quick Tournament Example
Run a fast tournament with pre-configured players
"""

import sys
import os

# Add parent directory's src to path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(os.path.join(parent_dir, 'src'))

# Import tournament system
from tournament import Tournament

# Quick tournament configuration - All available AI players with defaults
players_config = [
    # Standard AI with different evaluators
    ("AI", "AIPlayer-Std-6", 6, "Minimax", "Standard"),
    ("AI", "AIPlayer-Adv-6", 6, "Minimax", "Advanced"),
    ("AI", "AIPlayer-Simple-6", 6, "Minimax", "Simple"),
    ("AI", "AIPlayer-Greedy-6", 6, "Minimax", "Greedy"),
    
    # AI with Opening Book (NEW!)
    ("AIBook", "AIPlayerBook-6", 6, "Minimax", "Standard"),
    
    # Specialized players
    ("Heuristic", "HeuristicPlayer", 1, "Heuristic", "Standard"),
    ("Greedy", "GreedyPlayer", 1, "Minimax", "Greedy"),
    ("Monkey", "MonkeyPlayer", 1, "Random", "Standard"),
]

games_per_matchup = 2  # 2 games per matchup (quick test)
include_move_history = True  # Include move history in report

print("\n" + "="*80)
print("QUICK TOURNAMENT - PRE-CONFIGURED")
print("="*80)
print("\nPlayers:")
for config in players_config:
    print(f"  - {config[1]}")
print(f"\nGames per matchup: {games_per_matchup}")
print(f"Total games: {len(players_config) * (len(players_config) - 1) * games_per_matchup}")
print(f"Include move history: {'Yes' if include_move_history else 'No'}")
print()

input("Press ENTER to start...")

# Run tournament with move history
tournament = Tournament(players_config, games_per_matchup, include_move_history)
tournament.run()

# Generate and display report
report = tournament.generate_report()
print(report)

# Save report
filename = tournament.save_report()

print(f"\n✓ Tournament completed!")
print(f"✓ Report saved to: {filename}")
if include_move_history:
    print(f"✓ Report includes complete move history for all {len(players_config) * (len(players_config) - 1) * games_per_matchup} games")

