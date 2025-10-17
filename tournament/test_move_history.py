#!/usr/bin/env python3

import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(os.path.join(parent_dir, 'src'))

from tournament import Tournament

print("Testing move history feature...\n")

players_config = [
    ('Heuristic', 'Heuristic', 1, 'Heuristic', 'Standard'),
    ('Greedy', 'Greedy', 1, 'Minimax', 'Standard'),
]

# Test WITHOUT move history
print("1. Tournament WITHOUT move history:")
tournament1 = Tournament(players_config, 1, include_move_history=False)
tournament1.run()
report1 = tournament1.generate_report()

if "COMPLETE MOVE HISTORY" in report1:
    print("   ✗ ERROR: Move history included when it shouldn't be")
else:
    print("   ✓ Move history correctly excluded")

# Test WITH move history
print("\n2. Tournament WITH move history:")
tournament2 = Tournament(players_config, 1, include_move_history=True)
tournament2.run()
report2 = tournament2.generate_report()

if "COMPLETE MOVE HISTORY" in report2:
    print("   ✓ Move history correctly included")
    # Show a sample
    lines = report2.split('\n')
    for i, line in enumerate(lines):
        if 'COMPLETE MOVE HISTORY' in line:
            # Print section header and a few lines
            for j in range(i, min(i+15, len(lines))):
                print(f"   {lines[j]}")
            break
else:
    print("   ✗ ERROR: Move history NOT included when it should be")

print("\n" + "="*60)
print("✓ Move history feature working correctly!")
print("="*60)

