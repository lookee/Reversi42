#!/usr/bin/env python3

import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(os.path.join(parent_dir, 'src'))

from tournament import Tournament

print("Testing report save location...\n")

players_config = [
    ('AI', 'Test-AI', 2, 'Minimax', 'Standard'),
    ('Greedy', 'Test-Greedy', 1, 'Minimax', 'Standard'),
]

tournament = Tournament(players_config, 1)
tournament.run()

# Save report
filepath = tournament.save_report("test_save.txt")

print(f"\n✓ Report saved to: {filepath}")

# Verify it's in reports directory
if '/reports/' in filepath:
    print("✓ Report correctly saved in reports/ directory")
else:
    print("✗ Report NOT in reports/ directory")

# Check if file exists
if os.path.exists(filepath):
    print("✓ File exists and is accessible")
    print(f"✓ File size: {os.path.getsize(filepath)} bytes")
else:
    print("✗ File NOT found")

# List reports directory
reports_dir = os.path.join(script_dir, 'reports')
if os.path.exists(reports_dir):
    files = [f for f in os.listdir(reports_dir) if f.endswith('.txt')]
    print(f"\n✓ Reports directory contains {len(files)} report(s)")

