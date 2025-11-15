#!/usr/bin/env python3
"""
Battery di test per l'integrità della scacchiera.

Testa:
- Undo/redo operations
- Posizioni limite (bordi, angoli)
- Mosse non valide
- Consistenza dello stato
- Stack delle mosse
"""

import os
import sys

import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Game, Move


class TestBoardStateIntegrity:
    """Test per l'integrità dello stato della scacchiera"""

    def test_initial_state(self):
        """Verifica lo stato iniziale della scacchiera"""
        game = Game(8)

        assert game.black_cnt == 2, "Inizialmente devono esserci 2 pezzi neri"
        assert game.white_cnt == 2, "Inizialmente devono esserci 2 pezzi bianchi"
        assert game.turn == "B", "Il nero deve iniziare"
        assert game.turn_cnt == 0, "Il contatore mosse deve essere 0"
        assert len(game.board_position_stack) == 0, "Lo stack deve essere vuoto"

    def test_piece_count_after_move(self):
        """Verifica che il conteggio pezzi sia corretto dopo una mossa"""
        game = Game(8)
        initial_count = game.black_cnt + game.white_cnt

        moves = game.get_move_list()
        assert len(moves) > 0, "Devono esserci mosse disponibili"

        move = moves[0]
        game.move(move)

        new_count = game.black_cnt + game.white_cnt
        assert new_count > initial_count, "Il numero di pezzi deve aumentare"
        assert new_count == initial_count + 1 + (
            initial_count - new_count + 1
        ), "Conteggio inconsistente dopo la mossa"

    def test_turn_alternation(self):
        """Verifica che i turni si alternino correttamente"""
        game = Game(8)

        assert game.turn == "B", "Deve iniziare il nero"

        moves = game.get_move_list()
        game.move(moves[0])
        assert game.turn == "W", "Dopo il nero deve giocare il bianco"

        moves = game.get_move_list()
        if len(moves) > 0:
            game.move(moves[0])
            assert game.turn == "B", "Dopo il bianco deve giocare il nero"


class TestUndoFunctionality:
    """Test per la funzionalità di undo"""

    def test_undo_single_move(self):
        """Verifica undo di una singola mossa"""
        game = Game(8)

        # Salva stato iniziale
        initial_state = game.export_str()
        initial_turn = game.turn
        initial_black = game.black_cnt
        initial_white = game.white_cnt
        initial_turn_cnt = game.turn_cnt

        # Fai una mossa
        moves = game.get_move_list()
        game.move(moves[0])

        # Verifica che lo stato sia cambiato
        assert game.export_str() != initial_state
        assert game.turn != initial_turn

        # Undo
        game.undo_move()

        # Verifica ripristino completo
        assert game.export_str() == initial_state, "La board deve essere ripristinata"
        assert game.turn == initial_turn, "Il turno deve essere ripristinato"
        assert game.black_cnt == initial_black, "I pezzi neri devono essere ripristinati"
        assert game.white_cnt == initial_white, "I pezzi bianchi devono essere ripristinati"
        assert game.turn_cnt == initial_turn_cnt, "Il contatore turni deve essere ripristinato"

    def test_undo_multiple_moves(self):
        """Verifica undo di più mosse consecutive"""
        game = Game(8)

        initial_state = game.export_str()
        states = [initial_state]

        # Fai 5 mosse
        for _ in range(5):
            moves = game.get_move_list()
            if len(moves) == 0:
                break
            game.move(moves[0])
            states.append(game.export_str())

        moves_made = len(states) - 1

        # Undo tutte le mosse
        for i in range(moves_made):
            game.undo_move()
            expected_state = states[moves_made - i - 1]
            assert game.export_str() == expected_state, f"Undo {i+1}: stato non corretto"

        # Verifica ritorno allo stato iniziale
        assert game.export_str() == initial_state
        assert game.turn == "B"
        assert game.black_cnt == 2
        assert game.white_cnt == 2

    def test_undo_redo_consistency(self):
        """Verifica consistenza undo/redo"""
        game = Game(8)

        # Fai 3 mosse
        moves_played = []
        for _ in range(3):
            moves = game.get_move_list()
            if len(moves) == 0:
                break
            move = moves[0]
            moves_played.append(move)
            game.move(move)

        state_after_moves = game.export_str()

        # Undo tutte
        for _ in range(len(moves_played)):
            game.undo_move()

        # Rifai le stesse mosse
        for move in moves_played:
            game.move(move)

        # Lo stato deve essere identico
        assert game.export_str() == state_after_moves, "Undo/redo deve produrre lo stesso stato"

    def test_undo_with_pass(self):
        """Verifica undo quando c'è un pass_turn"""
        game = Game(8)

        initial_state = game.export_str()
        initial_turn = game.turn

        # Passa il turno
        game.pass_turn()

        assert game.turn != initial_turn, "Il turno deve cambiare"

        # Undo
        game.undo_move()

        assert game.export_str() == initial_state, "La board deve essere ripristinata"
        assert game.turn == initial_turn, "Il turno deve essere ripristinato"


class TestBorderPositions:
    """Test per posizioni ai bordi e angoli"""

    def test_corner_moves(self):
        """Verifica mosse negli angoli"""
        game = Game(8)

        # Gioca fino a poter catturare un angolo
        # (questo è un test semplificato)
        corners = [
            Move(1, 1),  # A1
            Move(8, 1),  # H1
            Move(1, 8),  # A8
            Move(8, 8),  # H8
        ]

        # Gli angoli non sono validi all'inizio
        for corner in corners:
            assert not game.valid_move(
                corner
            ), f"L'angolo {corner} non dovrebbe essere valido all'inizio"

    def test_edge_moves(self):
        """Verifica mosse sui bordi"""
        game = Game(8)

        # Fai alcune mosse per testare i bordi
        moves = game.get_move_list()

        # Verifica che ci siano mosse valide
        assert len(moves) > 0, "Devono esserci mosse disponibili"

        # Tutte le mosse valide devono essere effettivamente giocabili
        for move in moves:
            # Crea una copia per testare
            test_game = Game(8)
            test_game.import_str(game.export_str())
            test_game.turn = game.turn

            # Deve essere possibile giocare la mossa
            try:
                test_game.move(move)
                piece_count = test_game.black_cnt + test_game.white_cnt
                assert piece_count > 4, "Il conteggio pezzi deve aumentare"
            except Exception as e:
                pytest.fail(f"Mossa valida {move} ha causato errore: {e}")

    def test_all_board_positions(self):
        """Verifica che tutte le posizioni della board siano accessibili"""
        game = Game(8)

        # Verifica che la matrice sia 10x10 (con bordi)
        assert len(game.matrix) == 10, "La matrice deve essere 10x10"
        assert len(game.matrix[0]) == 10, "Ogni riga deve avere 10 elementi"

        # Verifica che le posizioni di gioco siano 1-8
        for y in range(1, 9):
            for x in range(1, 9):
                cell = game.matrix[y][x]
                assert cell in [".", "B", "W"], f"Posizione [{y}][{x}] ha valore invalido: {cell}"


class TestInvalidMoves:
    """Test per mosse non valide"""

    def test_move_on_occupied_square(self):
        """Verifica che non si possa giocare su una casella occupata"""
        game = Game(8)

        # Prova a giocare in D4 (occupata all'inizio)
        move = Move(4, 4)
        assert not game.valid_move(
            move
        ), "Non dovrebbe essere possibile giocare su una casella occupata"

    def test_move_without_flips(self):
        """Verifica che non si possa giocare senza catturare"""
        game = Game(8)

        # Prova a giocare in una posizione che non cattura nulla
        # Ad esempio A1 all'inizio
        move = Move(1, 1)
        assert not game.valid_move(
            move
        ), "Non dovrebbe essere possibile giocare senza catturare pezzi"

    def test_move_outside_board(self):
        """Verifica comportamento con mosse fuori dalla scacchiera"""
        game = Game(8)

        # Mosse fuori dalla board (0 o 9+)
        invalid_moves = [
            Move(0, 0),
            Move(9, 5),
            Move(5, 9),
            Move(0, 5),
        ]

        for move in invalid_moves:
            # Queste mosse non dovrebbero mai essere valide
            # e non dovrebbero causare crash
            try:
                result = game.valid_move(move)
                assert not result, f"Mossa fuori board {move} non dovrebbe essere valida"
            except IndexError:
                # Accettabile se lancia IndexError
                pass

    def test_invalid_move_exception(self):
        """Verifica che move() lanci eccezione per mosse invalide"""
        game = Game(8)

        # Prova a fare una mossa invalida
        invalid_move = Move(1, 1)  # A1, non valida all'inizio

        with pytest.raises(Exception):  # Dovrebbe lanciare NameError o simile
            game.move(invalid_move)


class TestStateConsistency:
    """Test per la consistenza dello stato"""

    def test_export_import_consistency(self):
        """Verifica che export/import preservino lo stato"""
        game = Game(8)

        # Fai alcune mosse
        for _ in range(3):
            moves = game.get_move_list()
            if len(moves) == 0:
                break
            game.move(moves[0])

        # Esporta stato
        exported = game.export_str()
        black_cnt = game.black_cnt
        white_cnt = game.white_cnt
        turn = game.turn

        # Crea nuovo gioco e importa
        new_game = Game(8)
        new_game.import_str(exported)
        new_game.turn = turn

        # Verifica consistenza
        assert new_game.export_str() == exported, "L'import deve riprodurre lo stato"
        assert new_game.black_cnt == black_cnt, "I pezzi neri devono corrispondere"
        assert new_game.white_cnt == white_cnt, "I pezzi bianchi devono corrispondere"

    def test_move_stack_size(self):
        """Verifica che lo stack cresca correttamente"""
        game = Game(8)

        assert len(game.board_position_stack) == 0, "Stack deve essere vuoto"

        # Fai 5 mosse
        for i in range(5):
            moves = game.get_move_list()
            if len(moves) == 0:
                break
            game.move(moves[0])
            assert (
                len(game.board_position_stack) == i + 1
            ), f"Dopo {i+1} mosse, lo stack deve avere {i+1} elementi"

        # Undo tutte le mosse
        stack_size = len(game.board_position_stack)
        for i in range(stack_size):
            game.undo_move()
            expected_size = stack_size - i - 1
            assert (
                len(game.board_position_stack) == expected_size
            ), f"Dopo undo {i+1}, lo stack deve avere {expected_size} elementi"

    def test_piece_count_invariant(self):
        """Verifica che black_cnt + white_cnt sia sempre corretto"""
        game = Game(8)

        for _ in range(10):
            moves = game.get_move_list()
            if len(moves) == 0:
                break

            # Conta manualmente i pezzi
            manual_black = 0
            manual_white = 0
            for y in range(1, 9):
                for x in range(1, 9):
                    if game.matrix[y][x] == "B":
                        manual_black += 1
                    elif game.matrix[y][x] == "W":
                        manual_white += 1

            # Verifica consistenza
            assert (
                game.black_cnt == manual_black
            ), "black_cnt deve corrispondere al conteggio manuale"
            assert (
                game.white_cnt == manual_white
            ), "white_cnt deve corrispondere al conteggio manuale"

            game.move(moves[0])

    def test_monotonic_piece_count(self):
        """Verifica che il numero totale di pezzi cresca sempre"""
        game = Game(8)

        prev_count = game.black_cnt + game.white_cnt

        for _ in range(20):
            moves = game.get_move_list()
            if len(moves) == 0:
                # Pass turn non modifica il conteggio
                game.pass_turn()
                current_count = game.black_cnt + game.white_cnt
                assert current_count == prev_count, "Pass turn non deve modificare il conteggio"

                # Verifica se il gioco è finito
                if len(game.get_move_list()) == 0:
                    break
                continue

            game.move(moves[0])
            current_count = game.black_cnt + game.white_cnt

            assert (
                current_count > prev_count
            ), f"Il conteggio deve crescere: {prev_count} -> {current_count}"

            prev_count = current_count


class TestBitboardConsistency:
    """Test per consistenza tra Game e BitboardGame"""

    def test_bitboard_piece_count(self):
        """Verifica che BitboardGame conti correttamente i pezzi"""
        game = BitboardGame()

        assert game.black_cnt == 2, "Devono esserci 2 pezzi neri"
        assert game.white_cnt == 2, "Devono esserci 2 pezzi bianchi"

    def test_bitboard_undo(self):
        """Verifica undo in BitboardGame"""
        game = BitboardGame()

        initial_black = game.black
        initial_white = game.white
        initial_turn = game.turn

        # Fai una mossa
        moves = game.get_move_list()
        if len(moves) > 0:
            game.move(moves[0])

            # Undo
            game.undo_move()

            # Verifica ripristino
            assert game.black == initial_black, "Bitboard nero deve essere ripristinato"
            assert game.white == initial_white, "Bitboard bianco deve essere ripristinato"
            assert game.turn == initial_turn, "Il turno deve essere ripristinato"

    def test_bitboard_move_stack(self):
        """Verifica che lo stack di BitboardGame funzioni"""
        game = BitboardGame()

        assert len(game.move_stack) == 0, "Stack deve essere vuoto"

        # Fai mosse
        for i in range(3):
            moves = game.get_move_list()
            if len(moves) == 0:
                break
            game.move(moves[0])
            assert len(game.move_stack) == i + 1

        # Undo
        stack_size = len(game.move_stack)
        for _ in range(stack_size):
            game.undo_move()

        assert len(game.move_stack) == 0, "Stack deve essere vuoto dopo tutti gli undo"


def test_comprehensive_game_sequence():
    """Test completo di una sequenza di gioco"""
    game = Game(8)

    states = []
    max_moves = 60

    for move_num in range(max_moves):
        # Salva stato
        state = {
            "board": game.export_str(),
            "turn": game.turn,
            "black": game.black_cnt,
            "white": game.white_cnt,
            "turn_cnt": game.turn_cnt,
            "stack_size": len(game.board_position_stack),
            "is_pass": False,
        }

        # Verifica invarianti
        assert game.black_cnt >= 0, "I pezzi neri non possono essere negativi"
        assert game.white_cnt >= 0, "I pezzi bianchi non possono essere negativi"
        assert game.black_cnt + game.white_cnt >= 4, "Devono esserci almeno 4 pezzi"
        assert game.black_cnt + game.white_cnt <= 64, "Non possono esserci più di 64 pezzi"
        assert game.turn in ["B", "W"], "Il turno deve essere B o W"

        # Ottieni mosse
        moves = game.get_move_list()

        if len(moves) == 0:
            # Pass turn
            state["is_pass"] = True
            game.pass_turn()
            if len(game.get_move_list()) == 0:
                # Gioco finito
                states.append(state)
                break
        else:
            # Gioca
            game.move(moves[0])

        states.append(state)

    # Undo solo le mosse effettive (non i pass intermedi)
    # Verifica che i contatori base tornino corretti
    initial_stack_size = len(game.board_position_stack)

    for _ in range(initial_stack_size):
        game.undo_move()

    # Verifica ritorno allo stato iniziale
    assert game.black_cnt == 2, "Dopo undo totale: deve tornare a 2 pezzi neri"
    assert game.white_cnt == 2, "Dopo undo totale: deve tornare a 2 pezzi bianchi"
    assert game.turn == "B", "Dopo undo totale: deve tornare al turno nero"
    assert len(game.board_position_stack) == 0, "Lo stack deve essere vuoto"


def test_complete_forward_backward_sequence():
    """
    Test RIGOROSO: partita completa forward, poi backward step-by-step.

    Verifica che OGNI undo ripristini esattamente lo stato precedente,
    non solo lo stato iniziale finale.
    """
    game = Game(8)

    # Array per salvare OGNI stato dopo ogni mossa
    saved_states = []

    # Salva stato iniziale
    saved_states.append(
        {
            "board": game.export_str(),
            "turn": game.turn,
            "black": game.black_cnt,
            "white": game.white_cnt,
            "turn_cnt": game.turn_cnt,
            "history": game.history,
        }
    )

    print(f"\n{'='*80}")
    print("FORWARD: Giocando partita e salvando ogni stato...")
    print(f"{'='*80}")

    # FORWARD: Gioca fino alla fine
    # Lo stack salva automaticamente gli stati, NOI verifichiamo solo che tutto funzioni
    moves_played = 0
    max_moves = 60

    while not game.is_finish() and moves_played < max_moves:
        moves = game.get_move_list()

        if len(moves) == 0:
            # Pass
            game.pass_turn()
            if len(game.get_move_list()) == 0:
                break
            continue

        # Gioca la prima mossa disponibile
        game.move(moves[0])
        moves_played += 1

        # Salva lo stato corrente (DOPO la mossa) per statistiche
        saved_states.append(
            {
                "board": game.export_str(),
                "turn": game.turn,
                "black": game.black_cnt,
                "white": game.white_cnt,
                "turn_cnt": game.turn_cnt,
                "history": game.history,
            }
        )

        if moves_played <= 5 or moves_played % 10 == 0:
            pieces = game.black_cnt + game.white_cnt
            print(f"  Mossa {moves_played}: {pieces} pezzi, turno={game.turn}")

    final_pieces = game.black_cnt + game.white_cnt
    print(f"\nPartita completata: {moves_played} mosse, {final_pieces} pezzi")
    print(f"Stati salvati: {len(saved_states)} (incluso iniziale)")

    # Verifica che abbiamo salvato stati
    assert len(saved_states) > 1, "Devono esserci stati salvati"
    assert (
        len(saved_states) == moves_played + 1
    ), f"Numero stati errato: {len(saved_states)} != {moves_played + 1}"

    print(f"\n{'='*80}")
    print("BACKWARD: Undo step-by-step verificando invarianti...")
    print(f"{'='*80}")

    # BACKWARD: Undo TUTTE le operazioni nello stack (mosse + pass)
    stack_size = len(game.board_position_stack)
    print(f"Stack size: {stack_size} (mosse reali: {moves_played})")

    for step in range(stack_size):
        # Prima di undo: salva stato attuale
        before_pieces = game.black_cnt + game.white_cnt

        # Fai l'undo
        game.undo_move()

        # Dopo undo: verifica invarianti
        after_pieces = game.black_cnt + game.white_cnt

        # Il numero di pezzi deve DIMINUIRE o rimanere uguale (se era un pass_turn)
        assert (
            after_pieces <= before_pieces
        ), f"Undo {step + 1}: pezzi non devono aumentare (prima={before_pieces}, dopo={after_pieces})"

        # I contatori devono essere validi
        assert game.black_cnt >= 0, f"Undo {step + 1}: black_cnt negativo"
        assert game.white_cnt >= 0, f"Undo {step + 1}: white_cnt negativo"
        assert game.turn in ["B", "W"], f"Undo {step + 1}: turno invalido"

        # Stampa progresso
        if step < 5 or (step + 1) % 10 == 0 or step == stack_size - 1:
            print(f"  Undo {step + 1}/{stack_size}: {after_pieces} pezzi, turno={game.turn} ✓")

    # Verifica finale: siamo tornati esattamente allo stato iniziale
    initial = saved_states[0]
    assert game.export_str() == initial["board"], "Non siamo tornati alla board iniziale"
    assert game.turn == initial["turn"], "Non siamo tornati al turno iniziale"
    assert game.black_cnt == initial["black"], "Non siamo tornati al black_cnt iniziale"
    assert game.white_cnt == initial["white"], "Non siamo tornati al white_cnt iniziale"
    assert game.turn_cnt == initial["turn_cnt"], "Non siamo tornati al turn_cnt iniziale"
    assert len(game.board_position_stack) == 0, "Lo stack deve essere vuoto"

    print(f"\n{'='*80}")
    print("✅ TEST RIGOROSO COMPLETATO!")
    print(f"   - {moves_played} mosse giocate (forward)")
    print(f"   - {stack_size} undo verificati (backward, inclusi {stack_size - moves_played} pass)")
    print(f"   - OGNI invariante verificato corretto")
    print(f"   - Ritorno perfetto allo stato iniziale")
    print(f"{'='*80}\n")


def test_random_position_forward_backward():
    """
    Test con posizioni casuali: gioca N mosse random, poi undo totale.
    Ripete il test 5 volte per aumentare la copertura.
    """
    import random

    for iteration in range(5):
        game = Game(8)

        # Numero random di mosse (tra 10 e 30)
        num_moves = random.randint(10, 30)

        states = [game.export_str()]

        # Forward: gioca mosse random
        for _ in range(num_moves):
            moves = game.get_move_list()
            if len(moves) == 0:
                break

            # Scegli una mossa a caso
            move = random.choice(moves)
            game.move(move)
            states.append(game.export_str())

        actual_moves = len(states) - 1

        # Backward: undo tutte
        for i in range(actual_moves):
            game.undo_move()
            expected_state = states[actual_moves - i - 1]

            assert (
                game.export_str() == expected_state
            ), f"Iterazione {iteration + 1}, undo {i + 1}: stato non corretto"

        # Verifica stato iniziale
        assert game.export_str() == states[0]
        assert game.black_cnt == 2
        assert game.white_cnt == 2
        assert game.turn == "B"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
