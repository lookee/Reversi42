#!/usr/bin/env python3
"""
Reversi42 - Unified Test Runner
Run all tests from a single command
"""

import sys
import os
import subprocess

def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n{'='*80}")
    print(f"Running: {description}")
    print('='*80)
    
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    """Run all test suites"""
    print("="*80)
    print("REVERSI42 TEST SUITE v3.1.0")
    print("="*80)
    
    all_passed = True
    
    # Run bitboard tests
    if not run_command('python tests/test_bitboard_book.py', 'Bitboard Implementation Tests'):
        all_passed = False
    
    # Run parallel engine tests
    if not run_command('python tests/test_parallel_engine.py', 'Parallel Engine Tests'):
        all_passed = False
    
    # Run tournament tests
    if not run_command('python tests/test_tournament.py', 'Tournament System Tests'):
        all_passed = False
    
    if not run_command('python tests/test_move_history.py', 'Tournament Move History Tests'):
        all_passed = False
    
    if not run_command('python tests/test_report_save.py', 'Tournament Report Tests'):
        all_passed = False
    
    # Summary
    print(f"\n{'='*80}")
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print('='*80)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

