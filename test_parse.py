#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from AI.OpeningBook import OpeningBook

book = OpeningBook(book_path='Books/opening_book.txt')
print(f"✓ Book loaded: {book.lines_loaded} positions\n")

# Test parsing
test_states = ["", "F5", "F5d6", "F5d6C5"]

for state in test_states:
    moves = book.get_book_moves(state)
    print(f"State: '{state}' → Book moves: {[str(m) for m in moves]}")
