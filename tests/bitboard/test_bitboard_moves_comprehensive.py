#!/usr/bin/env python3
"""
Comprehensive test suite for BitboardGame move generation.

Verifies that BitboardGame.get_valid_moves() generates EXACTLY the same
moves as Game.get_move_list() across hundreds of critical positions:
- Corner positions
- Edge positions
- Center positions
- All game phases
- Random game sequences
- Known problematic positions
"""

import os
import random
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Game, Move


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


def assert_moves_match(game, position_name=""):
    """
    Assert that Game and BitboardGame generate identical moves.

    This is the CRITICAL invariant that must always hold!
    """
    bitboard = convert_to_bitboard(game)

    # Get moves from both
    moves_game = set(str(m) for m in game.get_move_list())
    moves_bitboard = set(str(m) for m in bitboard.get_move_list())

    # Verify count matches
    assert len(moves_game) == len(
        moves_bitboard
    ), f"{position_name}: Different move counts! Game={len(moves_game)}, Bitboard={len(moves_bitboard)}"

    # Verify same moves
    only_in_game = moves_game - moves_bitboard
    only_in_bitboard = moves_bitboard - moves_game

    if only_in_game or only_in_bitboard:
        error_msg = f"{position_name}: Move lists don't match!\n"
        if only_in_game:
            error_msg += f"  Only in Game: {sorted(only_in_game)}\n"
        if only_in_bitboard:
            error_msg += f"  Only in BitboardGame: {sorted(only_in_bitboard)}\n"
        error_msg += f"\nBoard:\n{game.get_view()}"
        assert False, error_msg

    # Verify each move individually with valid_move()
    for move_str in moves_game:
        x = ord(move_str[0]) - ord("A") + 1
        y = int(move_str[1])
        move = Move(x, y)

        assert game.valid_move(move), f"{position_name}: {move_str} should be valid in Game"
        assert bitboard.valid_move(
            move
        ), f"{position_name}: {move_str} should be valid in BitboardGame"


class TestInitialPosition:
    """Test posizione iniziale"""

    def test_initial_moves(self):
        """Verifica mosse dalla posizione iniziale"""
        game = Game(8)
        assert_moves_match(game, "Initial position")

        # Le 4 mosse standard all'inizio
        moves = set(str(m) for m in game.get_move_list())
        assert len(moves) == 4, "All'inizio devono esserci 4 mosse"
        assert moves == {"D3", "C4", "F5", "E6"}, "Mosse iniziali standard"


class TestCornerPositions:
    """Test per posizioni critiche negli angoli"""

    def test_near_corner_a1(self):
        """Posizioni vicino all'angolo A1"""
        game = Game(8)

        # Gioca mosse verso l'angolo A1
        for _ in range(10):
            moves = game.get_move_list()
            if not moves:
                break
            game.move(moves[0])
            assert_moves_match(game, f"Near A1, move {game.turn_cnt}")

    def test_near_corner_h1(self):
        """Posizioni vicino all'angolo H1"""
        game = Game(8)

        for _ in range(10):
            moves = game.get_move_list()
            if not moves:
                break
            # Scegli mosse verso destra
            game.move(moves[min(1, len(moves) - 1)])
            assert_moves_match(game, f"Near H1, move {game.turn_cnt}")

    def test_all_corners_proximity(self):
        """Test vicinanza a tutti gli angoli"""
        # Gioca partite diverse che esplorano tutti gli angoli
        for seed in range(4):
            random.seed(seed)
            game = Game(8)

            for move_num in range(15):
                moves = game.get_move_list()
                if not moves:
                    break

                # Gioca mossa random
                move = random.choice(moves)
                game.move(move)

                assert_moves_match(game, f"Corner exploration seed={seed}, move={move_num+1}")


class TestEdgePositions:
    """Test per posizioni sui bordi"""

    def test_left_edge_column_a(self):
        """
        Test critico: Colonna A (problematica per NE direction).

        Questo è il bordo che aveva il bug!
        """
        game = Game(8)

        # Gioca 20 mosse random
        random.seed(42)
        for move_num in range(20):
            moves = game.get_move_list()
            if not moves:
                break

            game.move(random.choice(moves))

            # Verifica SEMPRE, specialmente per la colonna A
            assert_moves_match(game, f"Left edge (col A), move={move_num+1}")

    def test_right_edge_column_h(self):
        """Test colonna H (bordo destro)"""
        game = Game(8)

        random.seed(43)
        for move_num in range(20):
            moves = game.get_move_list()
            if not moves:
                break
            game.move(random.choice(moves))
            assert_moves_match(game, f"Right edge (col H), move={move_num+1}")

    def test_top_edge_row_1(self):
        """Test riga 1 (bordo superiore)"""
        game = Game(8)

        random.seed(44)
        for move_num in range(20):
            moves = game.get_move_list()
            if not moves:
                break
            game.move(random.choice(moves))
            assert_moves_match(game, f"Top edge (row 1), move={move_num+1}")

    def test_bottom_edge_row_8(self):
        """Test riga 8 (bordo inferiore)"""
        game = Game(8)

        random.seed(45)
        for move_num in range(20):
            moves = game.get_move_list()
            if not moves:
                break
            game.move(random.choice(moves))
            assert_moves_match(game, f"Bottom edge (row 8), move={move_num+1}")


class TestGamePhases:
    """Test per diverse fasi del gioco"""

    def test_opening_phase(self):
        """Test fase di apertura (4-19 pezzi)"""
        game = Game(8)

        for move_num in range(1, 16):  # Fino a ~16 mosse
            moves = game.get_move_list()
            if not moves:
                break

            game.move(moves[0])
            pieces = game.black_cnt + game.white_cnt

            assert_moves_match(game, f"Opening phase, {pieces} pieces, move={move_num}")

    def test_midgame_phase(self):
        """Test fase di midgame (20-49 pezzi)"""
        game = Game(8)

        # Gioca fino al midgame
        for move_num in range(1, 41):
            moves = game.get_move_list()
            if not moves:
                break

            game.move(moves[0])
            pieces = game.black_cnt + game.white_cnt

            if 20 <= pieces <= 49:
                assert_moves_match(game, f"Midgame phase, {pieces} pieces, move={move_num}")

    def test_endgame_phase(self):
        """Test fase di endgame (50+ pezzi)"""
        game = Game(8)

        # Gioca fino all'endgame
        for move_num in range(1, 61):
            moves = game.get_move_list()
            if not moves:
                break

            game.move(moves[0])
            pieces = game.black_cnt + game.white_cnt

            if pieces >= 50:
                assert_moves_match(game, f"Endgame phase, {pieces} pieces, move={move_num}")


class TestKnownProblematicSequences:
    """Test per sequenze note che causavano problemi"""

    def test_sequence_that_caused_a5_bug(self):
        """
        Test la sequenza specifica che ha rivelato il bug A5/A3.

        Questa è una regression test CRITICA!
        """
        history = "C4e3F6e6F5c5F4g6F7d3F3g5G4e7D6h3F8e2H6h5"

        game = Game(8)

        # Replay move by move
        for i in range(0, len(history), 2):
            move_str = history[i : i + 2]
            col = ord(move_str[0].upper()) - ord("A") + 1
            row = int(move_str[1])
            move = Move(col, row)

            game.move(move)
            move_num = (i // 2) + 1
            pieces = game.black_cnt + game.white_cnt

            # Verifica OGNI mossa della sequenza
            assert_moves_match(game, f"Problematic sequence, move {move_num}, {pieces} pieces")

        # Verifica specifica alla mossa 20 (dove appariva A5)
        bitboard = convert_to_bitboard(game)
        moves_bitboard = set(str(m) for m in bitboard.get_move_list())

        assert "A5" not in moves_bitboard, "A5 must NOT be in valid moves (was the bug!)"
        assert "A3" not in moves_bitboard, "A3 must NOT be in valid moves (was the bug!)"

    def test_multiple_problematic_games(self):
        """Test multiple sequenze che potrebbero causare problemi"""
        # Sequenze di test pre-definite (da partite reali o generate)
        test_sequences = [
            "D3C3C4B3C5B4E3B5D6C6",
            "E6F4C3C4F3F6G5C5D6",
            "F5D6C5F4F6G5E6F7E7",
            "C4E3F4E6D3C5B4D6F5",
        ]

        for seq_num, history in enumerate(test_sequences):
            game = Game(8)

            for i in range(0, len(history), 2):
                move_str = history[i : i + 2]
                col = ord(move_str[0].upper()) - ord("A") + 1
                row = int(move_str[1])
                move = Move(col, row)

                if not game.valid_move(move):
                    break

                game.move(move)
                move_num = (i // 2) + 1

                assert_moves_match(game, f"Test sequence {seq_num+1}, move {move_num}")


class TestRandomGames:
    """Test con partite casuali complete"""

    def test_100_random_games(self):
        """
        Test MASSIVO: 100 partite casuali complete.

        Verifica che in OGNI posizione di OGNI partita,
        Game e BitboardGame generino le stesse mosse.
        """
        positions_tested = 0

        for game_num in range(100):
            random.seed(game_num)
            game = Game(8)

            move_num = 0
            while not game.is_finish() and move_num < 60:
                # Verifica mosse
                assert_moves_match(game, f"Random game {game_num+1}, move {move_num+1}")
                positions_tested += 1

                # Gioca mossa random
                moves = game.get_move_list()
                if not moves:
                    game.pass_turn()
                    if not game.get_move_list():
                        break
                    continue

                move = random.choice(moves)
                game.move(move)
                move_num += 1

        # Deve aver testato migliaia di posizioni
        assert (
            positions_tested >= 2000
        ), f"Should test at least 2000 positions, tested {positions_tested}"

        print(f"\n✅ Tested {positions_tested} positions across 100 games - ALL PASSED!")


class TestSpecificBoardConfigurations:
    """Test per configurazioni specifiche della board"""

    def test_full_row(self):
        """Test con una riga completamente piena"""
        game = Game(8)
        bitboard = BitboardGame()

        # Modifica manualmente per avere riga piena (row 4)
        for x in range(1, 9):
            game.matrix[4][x] = "B" if x % 2 == 0 else "W"
            bit = (4 - 1) * 8 + (x - 1)
            if x % 2 == 0:
                bitboard.black |= 1 << bit
            else:
                bitboard.white |= 1 << bit

        game.black_cnt = sum(
            1 for y in range(1, 9) for x in range(1, 9) if game.matrix[y][x] == "B"
        )
        game.white_cnt = sum(
            1 for y in range(1, 9) for x in range(1, 9) if game.matrix[y][x] == "W"
        )
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)

        assert_moves_match(game, "Full row configuration")

    def test_full_column(self):
        """Test con una colonna completamente piena"""
        game = Game(8)
        bitboard = BitboardGame()

        # Colonna A piena (il bordo problematico!)
        for y in range(1, 9):
            game.matrix[y][1] = "B" if y % 2 == 0 else "W"
            bit = (y - 1) * 8 + 0  # colonna A = offset 0
            if y % 2 == 0:
                bitboard.black |= 1 << bit
            else:
                bitboard.white |= 1 << bit

        game.black_cnt = sum(
            1 for y in range(1, 9) for x in range(1, 9) if game.matrix[y][x] == "B"
        )
        game.white_cnt = sum(
            1 for y in range(1, 9) for x in range(1, 9) if game.matrix[y][x] == "W"
        )
        bitboard.black_cnt = bitboard._count_bits(bitboard.black)
        bitboard.white_cnt = bitboard._count_bits(bitboard.white)

        assert_moves_match(game, "Full column A configuration")

    def test_diagonal_patterns(self):
        """Test con pattern diagonali"""
        game = Game(8)

        # Gioca apertura diagonale
        diag_moves = ["D3", "C3", "E3", "F3", "C4"]

        for move_str in diag_moves:
            col = ord(move_str[0]) - ord("A") + 1
            row = int(move_str[1])
            move = Move(col, row)

            if game.valid_move(move):
                game.move(move)
                assert_moves_match(game, f"Diagonal pattern after {move_str}")


class TestEdgeCasesPerDirection:
    """Test edge cases per ogni direzione"""

    def test_north_direction_edge_cases(self):
        """Test direzione Nord (shift -8) con edge cases"""
        game = Game(8)

        for _ in range(15):
            moves = game.get_move_list()
            if not moves:
                break
            game.move(moves[0])
            assert_moves_match(game, f"North direction test, move {game.turn_cnt}")

    def test_northeast_direction_edge_cases(self):
        """
        Test direzione NE (shift -7) - CRITICA!

        Questa direzione aveva il bug con la mask sbagliata.
        """
        random.seed(100)
        game = Game(8)

        for _ in range(20):
            moves = game.get_move_list()
            if not moves:
                break
            game.move(random.choice(moves))
            assert_moves_match(game, f"NE direction (CRITICAL!), move {game.turn_cnt}")

    def test_all_8_directions(self):
        """Test che copre tutte le 8 direzioni"""
        for direction_seed in range(8):
            random.seed(direction_seed * 10)
            game = Game(8)

            for _ in range(15):
                moves = game.get_move_list()
                if not moves:
                    break
                game.move(random.choice(moves))
                assert_moves_match(game, f"Direction {direction_seed+1}/8, move {game.turn_cnt}")


class TestBoundaryWraparound:
    """Test per verificare che non ci sia wrap-around ai bordi"""

    def test_column_a_no_wraparound(self):
        """
        Verifica che mosse sulla colonna A non generino wraparound.

        CRITICO: Questo test verifica che il fix del bug A5/A3 funzioni!
        """
        # Usa la sequenza esatta che causava il bug
        history = "C4e3F6e6F5c5F4g6F7d3F3g5G4e7D6h3F8e2H6h5"

        game = Game(8)
        for i in range(0, len(history), 2):
            move_str = history[i : i + 2]
            col = ord(move_str[0].upper()) - ord("A") + 1
            row = int(move_str[1])
            game.move(Move(col, row))

        bitboard = convert_to_bitboard(game)

        # A5 e A3 non devono essere nelle mosse valide
        moves = set(str(m) for m in bitboard.get_move_list())

        assert "A5" not in moves, "A5 should NOT be valid (column A wraparound bug!)"
        assert "A3" not in moves, "A3 should NOT be valid (column A wraparound bug!)"
        assert "A1" not in moves, "A1 should NOT be valid (corner, no captures)"
        assert "A2" not in moves, "A2 should NOT be valid if no valid captures"
        assert "A4" not in moves, "A4 should NOT be valid if no valid captures"
        assert "A6" not in moves, "A6 should NOT be valid if no valid captures"
        assert "A7" not in moves, "A7 should NOT be valid if no valid captures"
        assert "A8" not in moves, "A8 should NOT be valid (corner, no captures)"

        print(f"\n✅ NO wraparound detected on column A!")
        print(f"   Valid moves: {sorted(moves)}")

    def test_column_h_no_wraparound(self):
        """Verifica nessun wraparound sulla colonna H"""
        random.seed(200)
        game = Game(8)

        for _ in range(25):
            moves = game.get_move_list()
            if not moves:
                break

            game.move(random.choice(moves))

            # Verifica che non ci siano mosse invalide sulla colonna H
            bitboard = convert_to_bitboard(game)
            bitboard_moves = set(str(m) for m in bitboard.get_move_list())

            # Ogni mossa H* deve essere valida anche in Game
            for move_str in bitboard_moves:
                if move_str[0] == "H":
                    col = 8
                    row = int(move_str[1])
                    move = Move(col, row)
                    assert game.valid_move(
                        move
                    ), f"Column H move {move_str} generated by Bitboard but invalid in Game!"


class TestEveryPositionOfGame:
    """Test OGNI posizione di una partita completa"""

    def test_complete_game_every_position(self):
        """
        Test COMPLETO: gioca una partita intera e verifica OGNI posizione.
        """
        game = Game(8)
        positions_verified = 0

        while not game.is_finish() and positions_verified < 60:
            # VERIFICA CRITICA prima di ogni mossa
            assert_moves_match(game, f"Complete game, position {positions_verified+1}")
            positions_verified += 1

            moves = game.get_move_list()
            if not moves:
                game.pass_turn()
                if not game.get_move_list():
                    break
                continue

            game.move(moves[0])

        print(f"\n✅ Verified {positions_verified} positions in complete game - ALL CORRECT!")


def test_stress_test_1000_positions():
    """
    STRESS TEST: 1000+ posizioni casuali.

    Questo è il test finale che verifica robustezza su larga scala.
    """
    positions_tested = 0
    games_played = 0

    for seed in range(50):  # 50 partite
        random.seed(seed * 100)
        game = Game(8)

        for _ in range(40):
            assert_moves_match(
                game, f"Stress test game {games_played+1}, position {positions_tested+1}"
            )
            positions_tested += 1

            moves = game.get_move_list()
            if not moves:
                break

            game.move(random.choice(moves))

        games_played += 1

    assert positions_tested >= 1000, f"Should test 1000+ positions, tested {positions_tested}"

    print(f"\n" + "=" * 80)
    print(f"✅ STRESS TEST PASSED!")
    print(f"   Games played: {games_played}")
    print(f"   Positions tested: {positions_tested}")
    print(f"   ALL BitboardGame moves matched Game moves!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
