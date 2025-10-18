#!/usr/bin/env python3

"""
Quick Tournament - Configuration-Based Runner

This script has been updated to use the new configuration file system.
It now loads tournament settings from ring/quick_tournament.json

For the old inline configuration style, see the JSON file or create a custom one.
"""

import sys
import os

# Add parent directory's src to path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(os.path.join(parent_dir, 'src'))

# Import tournament system
from tournament import Tournament

# Configuration file path
config_file = os.path.join(script_dir, 'ring', 'quick_tournament.json')

print("\n" + "="*80)
print("QUICK TOURNAMENT - CONFIGURATION-BASED")
print("="*80)
print(f"Loading configuration from: ring/quick_tournament.json")
print()

# Check if config file exists
if not os.path.exists(config_file):
    print(f"ERROR: Configuration file not found: {config_file}")
    print()
    print("The quick tournament now uses a configuration file.")
    print("Please ensure ring/quick_tournament.json exists.")
    sys.exit(1)

try:
    # Load tournament from configuration
    tournament = Tournament.from_config_file(config_file)
    
    print(f"Tournament: {tournament.name}")
    if tournament.description:
        print(f"Description: {tournament.description}")
    print()
    
    print("Players:")
    for config in tournament.players_config:
        print(f"  - {config[1]}")
    
    print(f"\nGames per matchup: {tournament.games_per_matchup}")
    n_players = len(tournament.players_config)
    total_games = n_players * (n_players - 1) * tournament.games_per_matchup
    print(f"Total games: {total_games}")
    print(f"Include move history: {'Yes' if tournament.include_move_history else 'No'}")
    print()
    
    input("Press ENTER to start...")
    
    # Run tournament
    tournament.run()
    
    # Generate and display report
    report = tournament.generate_report()
    print(report)
    
    # Save report
    filename = tournament.save_report()
    
    print(f"\n✓ Tournament completed!")
    print(f"✓ Report saved to: {filename}")
    if tournament.include_move_history:
        print(f"✓ Report includes complete move history for all {total_games} games")

except Exception as e:
    print(f"ERROR: Failed to run tournament: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

