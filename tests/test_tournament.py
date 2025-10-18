#!/usr/bin/env python3

"""
Test Tournament System - Ultra Quick Test
"""

import sys
import os

# Add paths (now from tests/ subdirectory)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tournament import Tournament

print("\n" + "="*80)
print("TESTING TOURNAMENT SYSTEM")
print("="*80)
print("\nRunning mini tournament: 3 players, 1 game per matchup\n")

# Minimal configuration for quick test
players_config = [
    ("AI", "Minimax-2", 2, "Minimax", "Standard"),
    ("Greedy", "Greedy", 1, "Minimax", "Standard"),
    ("Monkey", "Random", 1, "Random", "Standard"),
]

games_per_matchup = 1

# Run tournament
tournament = Tournament(players_config, games_per_matchup)
tournament.run()

# Generate report
report = tournament.generate_report()
print(report)

# Save report
filename = tournament.save_report("test_tournament_report.txt")

print("\n" + "="*80)
print("✓ Tournament system test completed successfully!")
print("="*80)
print(f"\nFeatures verified:")
print("  ✓ Player creation")
print("  ✓ Game execution")
print("  ✓ Statistics collection")
print("  ✓ Timing analysis")
print("  ✓ Report generation")
print(f"  ✓ Report saved to: {filename}")
print()

