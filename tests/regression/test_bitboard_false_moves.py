#!/usr/bin/env python3
"""
Regression test: BitboardGame generates false positive moves.

Bug discovered: After specific game sequence, BitboardGame.get_valid_moves()
returns moves (A5, A3) that are NOT valid according to Game.get_move_list().

This causes AI to select invalid moves leading to game errors.
"""

import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Game, Move


def parse_move(move_str):
    """Parse move from string notation (e.g., 'C4', 'e3')"""
    col = move_str[0].upper()
    row = int(move_str[1])
    col_num = ord(col) - ord("A") + 1
    return Move(col_num, row)


def convert_to_bitboard(game):
    """Convert Game to BitboardGame (exact copy from Gladiators)"""
    bitboard = BitboardGame.create_empty()
    for y in range(1, 9):
        for x in range(1, 9):
            cell = game.matrix[y][x]
            bit = (y - 1) * 8 + (x - 1)
            if cell == "B":
                bitboard.black |= 1 << bit
            elif cell == "W":
                bitboard.white |= 1 << bit
    bitboard.turn = game.turn
    bitboard.turn_cnt = game.turn_cnt
    bitboard.black_cnt = bitboard._count_bits(bitboard.black)
    bitboard.white_cnt = bitboard._count_bits(bitboard.white)
    bitboard._create_virtual_matrix()
    return bitboard


def test_bitboard_false_positive_a5():
    """
    Test the specific bug: BitboardGame generates A5 as valid move when it's not.

    Sequence: C4e3F6e6F5c5F4g6F7d3F3g5G4e7D6h3F8e2H6h5
    After move 20 (h5), BitboardGame says A5 is valid but Game says it's not.
    """
    history = "C4e3F6e6F5c5F4g6F7d3F3g5G4e7D6h3F8e2H6h5"

    # Play game up to move 20
    game = Game(8)
    for i in range(0, len(history), 2):
        move = parse_move(history[i : i + 2])
        game.move(move)

    # Convert to bitboard
    bitboard = convert_to_bitboard(game)

    # Get moves from both
    moves_game = set(str(m) for m in game.get_move_list())
    moves_bitboard = set(str(m) for m in bitboard.get_move_list())

    # They MUST be identical
    assert moves_game == moves_bitboard, (
        f"BitboardGame generates different moves!\n"
        f"  Only in Game: {moves_game - moves_bitboard}\n"
        f"  Only in BitboardGame: {moves_bitboard - moves_game}\n"
        f"  This is a CRITICAL BUG!"
    )

    # Specifically check A5
    move_a5 = Move(1, 5)
    assert not bitboard.valid_move(
        move_a5
    ), "A5 should NOT be valid in BitboardGame (no pieces to capture)"

    assert not game.valid_move(move_a5), "A5 should NOT be valid in Game (no pieces to capture)"


def test_bitboard_game_move_parity():
    """
    Test that Game and BitboardGame always generate the same valid moves.

    This is a CRITICAL invariant: both implementations must agree on valid moves!
    """
    import random

    for iteration in range(10):
        game = Game(8)

        for move_num in range(20):  # Play 20 moves
            # Get moves from both
            moves_game = set(str(m) for m in game.get_move_list())

            # Convert and get bitboard moves
            bitboard = convert_to_bitboard(game)
            moves_bitboard = set(str(m) for m in bitboard.get_move_list())

            # CRITICAL: They MUST match
            if moves_game != moves_bitboard:
                print(f"\n{'='*80}")
                print(f"MISMATCH at move {move_num + 1}, iteration {iteration + 1}!")
                print(f"{'='*80}")
                print(f"Only in Game: {moves_game - moves_bitboard}")
                print(f"Only in BitboardGame: {moves_bitboard - moves_game}")
                print(f"\nBoard:")
                print(game.get_view())
                print(f"{'='*80}\n")

                assert False, f"Move list mismatch at move {move_num + 1}"

            # Play a random move
            if len(moves_game) == 0:
                break

            move_str = random.choice(list(moves_game))
            move = parse_move(move_str)
            game.move(move)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
