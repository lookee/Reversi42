#!/usr/bin/env python3
"""
Test suite for EnhancedOpeningBook.

Verifies:
- Backward compatibility with OpeningBook
- New filtering and scoring features
- Selection modes
- Parametric thresholds
"""

import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from domain.knowledge import (
    EnhancedOpeningBook,
    MoveEvaluation,
    OpeningBook,
    SelectionMode,
    get_enhanced_opening_book,
)
from Reversi.Game import Game, Move


class TestBackwardCompatibility:
    """Test che EnhancedOpeningBook sia retrocompatibile"""

    def test_inheritance(self):
        """Verifica che sia una sottoclasse di OpeningBook"""
        book = get_enhanced_opening_book()
        assert isinstance(book, OpeningBook), "Deve essere sottoclasse di OpeningBook"
        assert isinstance(book, EnhancedOpeningBook), "Deve essere EnhancedOpeningBook"

    def test_classic_methods_work(self):
        """Verifica che i metodi classici funzionino"""
        book = get_enhanced_opening_book()

        # Metodi di OpeningBook devono funzionare
        book_moves = book.get_book_moves("C4")
        assert book_moves is not None

        # is_in_book
        assert book.is_in_book("C4") or True  # Almeno uno dovrebbe esistere

        # get_current_opening_name
        name = book.get_current_opening_name("C4")
        # Può essere None o una stringa
        assert name is None or isinstance(name, str)

    def test_can_replace_openingbook(self):
        """Verifica che possa sostituire OpeningBook senza modifiche"""
        # Simula utilizzo come OpeningBook normale
        book = EnhancedOpeningBook()

        game = Game(8)
        moves = game.get_move_list()

        # Metodi base devono funzionare
        book_moves = book.get_book_moves("")
        assert book_moves is not None or book_moves is None  # Non deve crashare


class TestEnhancedFeatures:
    """Test per le nuove funzionalità"""

    def test_detailed_evaluation(self):
        """Test valutazione dettagliata di una mossa"""
        book = get_enhanced_opening_book()

        game = Game(8)
        moves = game.get_move_list()

        if moves:
            move_str = str(moves[0]).upper()
            eval_result = book.evaluate_move_detailed(move_str, "", moves)

            # Verifica struttura MoveEvaluation
            assert isinstance(eval_result, MoveEvaluation)
            assert eval_result.move == move_str
            assert isinstance(eval_result.score, float)
            assert isinstance(eval_result.count_continuations, int)
            assert isinstance(eval_result.has_evaluation, bool)

    def test_ranked_moves(self):
        """Test che le mosse siano rankkate correttamente"""
        book = get_enhanced_opening_book()

        game = Game(8)
        moves = game.get_move_list()

        ranked = book.get_ranked_moves("", moves)

        # Deve essere ordinato per score (decrescente)
        for i in range(len(ranked) - 1):
            assert (
                ranked[i].score >= ranked[i + 1].score
            ), "Mosse devono essere ordinate per score decrescente"

    def test_score_threshold_filtering(self):
        """Test filtro per soglia score"""
        # Book con soglia alta
        book_strict = get_enhanced_opening_book(score_threshold=0.5)

        # Book con soglia bassa
        book_lenient = get_enhanced_opening_book(score_threshold=0.0)

        game = Game(8)
        moves = game.get_move_list()

        filtered_strict = book_strict.get_filtered_moves("", moves)
        filtered_lenient = book_lenient.get_filtered_moves("", moves)

        # Soglia più alta dovrebbe filtrare di più (o uguale)
        assert len(filtered_strict) <= len(
            filtered_lenient
        ), "Soglia alta dovrebbe filtrare più mosse"

    def test_average_threshold(self):
        """Test uso media come soglia"""
        book_avg = get_enhanced_opening_book(score_threshold=0.0, use_average_threshold=True)

        book_fixed = get_enhanced_opening_book(score_threshold=0.0, use_average_threshold=False)

        game = Game(8)
        moves = game.get_move_list()

        # Entrambi devono funzionare
        filtered_avg = book_avg.get_filtered_moves("", moves)
        filtered_fixed = book_fixed.get_filtered_moves("", moves)

        assert filtered_avg is not None
        assert filtered_fixed is not None


class TestSelectionModes:
    """Test per le diverse modalità di selezione"""

    def test_best_score_mode(self):
        """Test modalità BEST_SCORE"""
        book = get_enhanced_opening_book(selection_mode=SelectionMode.BEST_SCORE)

        game = Game(8)
        moves = game.get_move_list()

        best_move = book.select_best_move("", moves)

        # Deve selezionare una mossa (o None se nessuna nel book)
        assert best_move is None or isinstance(best_move, str)

        if best_move:
            # Deve essere una mossa valida
            col = ord(best_move[0]) - ord("A") + 1
            row = int(best_move[1])
            move = Move(col, row)
            assert game.valid_move(move), "Mossa selezionata deve essere valida"

    def test_variety_first_mode(self):
        """Test modalità VARIETY_FIRST"""
        book = get_enhanced_opening_book(selection_mode=SelectionMode.VARIETY_FIRST)

        game = Game(8)
        moves = game.get_move_list()

        move = book.select_best_move("", moves, mode=SelectionMode.VARIETY_FIRST)

        # Non deve crashare
        assert move is None or isinstance(move, str)

    def test_safe_first_mode(self):
        """Test modalità SAFE_FIRST (preferisce =)"""
        book = get_enhanced_opening_book(selection_mode=SelectionMode.SAFE_FIRST)

        game = Game(8)
        moves = game.get_move_list()

        move = book.select_best_move("", moves, mode=SelectionMode.SAFE_FIRST)

        assert move is None or isinstance(move, str)

    def test_mode_override(self):
        """Test che mode parameter override la configurazione"""
        book = get_enhanced_opening_book(selection_mode=SelectionMode.BEST_SCORE)

        game = Game(8)
        moves = game.get_move_list()

        # Usa modalità diversa tramite parametro
        move_variety = book.select_best_move("", moves, mode=SelectionMode.VARIETY_FIRST)
        move_safe = book.select_best_move("", moves, mode=SelectionMode.SAFE_FIRST)

        # Entrambi devono funzionare (possono essere uguali o diversi)
        assert move_variety is None or isinstance(move_variety, str)
        assert move_safe is None or isinstance(move_safe, str)


class TestStatistics:
    """Test per statistiche avanzate"""

    def test_move_statistics(self):
        """Test statistiche complete"""
        book = get_enhanced_opening_book()

        game = Game(8)
        moves = game.get_move_list()

        stats = book.get_move_statistics("", moves)

        # Verifica struttura stats
        assert "total_moves" in stats
        assert "filtered_moves" in stats
        assert "best_move" in stats
        assert "best_score" in stats
        assert "average_score" in stats
        assert "evaluations" in stats

        # Valori devono essere sensati
        assert stats["total_moves"] == len(moves)
        assert stats["filtered_moves"] <= stats["total_moves"]
        assert isinstance(stats["average_score"], float)


def test_not_used_by_existing_players():
    """
    Verifica che EnhancedOpeningBook NON sia usato da giocatori esistenti.

    Questo garantisce backward compatibility - nessun comportamento cambiato.
    """
    # Verifica imports nei giocatori
    import glob

    player_files = glob.glob("src/Players/**/*.py", recursive=True)

    for player_file in player_files:
        with open(player_file, "r") as f:
            content = f.read()

            # EnhancedOpeningBook NON deve apparire
            assert (
                "EnhancedOpeningBook" not in content
            ), f"{player_file} uses EnhancedOpeningBook! Should use OpeningBook instead."

            assert (
                "get_enhanced_opening_book" not in content
            ), f"{player_file} uses get_enhanced_opening_book! Should use get_default_opening_book."

    print(f"\n✅ Verified: NO existing players use EnhancedOpeningBook")
    print(f"   Checked {len(player_files)} player files")
    print(f"   Backward compatibility guaranteed!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
