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

# Quick tournament configuration
players_config = [
    # (type, name, difficulty, engine, evaluator)
    ("AI", "Minimax-Std-4", 4, "Minimax", "Standard"),
    ("AI", "Minimax-Adv-4", 4, "Minimax", "Advanced"),
    ("AI", "Minimax-Greedy-4", 4, "Minimax", "Greedy"),
    ("Greedy", "GreedyPlayer", 1, "Minimax", "Standard"),
]

games_per_matchup = 2  # 2 games per matchup (quick test)

print("\n" + "="*80)
print("QUICK TOURNAMENT - PRE-CONFIGURED")
print("="*80)
print("\nPlayers:")
for config in players_config:
    print(f"  - {config[1]}")
print(f"\nGames per matchup: {games_per_matchup}")
print(f"Total games: {len(players_config) * (len(players_config) - 1) * games_per_matchup}")
print()

input("Press ENTER to start...")

# Run tournament
tournament = Tournament(players_config, games_per_matchup)
tournament.run()

# Generate and display report
report = tournament.generate_report()
print(report)

# Save report
filename = tournament.save_report()

print(f"\n✓ Tournament completed!")
print(f"✓ Report saved to: {filename}")

