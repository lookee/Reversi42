#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from domain.knowledge import OpeningBook
from Reversi.Game import Game

# Crea game e fai prima mossa
game = Game()
game.move_str('F5')  # Prima mossa standard

print("="*80)
print("TEST: Opening book trova mosse?")
print("="*80)

# Carica opening book
book = OpeningBook(book_path='Books/opening_book.txt')
print(f"✓ Book caricato: {book.lines_loaded} posizioni")

# Esporta stato per il libro
game_state = game.export_str()
print(f"Game state: {game_state}")

# Cerca mossa
book_move = book.get_move(game_state)
print(f"Book move: {book_move}")

if book_move:
    print(f"✓ Opening book HA trovato una mossa: {book_move}")
    print(f"  Opening name: {getattr(book, 'last_opening_name', 'N/A')}")
else:
    print(f"❌ Opening book NON ha trovato mosse per questa posizione")
    print(f"  Posizioni nel book: {book.lines_loaded}")

print("="*80)
