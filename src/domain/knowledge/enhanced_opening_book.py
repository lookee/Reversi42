"""
EnhancedOpeningBook - Advanced opening book with sophisticated move evaluation

Retrocompatibile con OpeningBook ma con funzionalità avanzate:
- Filtri parametrici per soglie di valutazione
- Sistema di scoring multi-criterio
- Modalità di selezione configurabili
- Analisi statistica delle varianti

Non utilizzato da giocatori esistenti - disponibile per future implementazioni.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from domain.knowledge.opening_book import OpeningBook


class SelectionMode(Enum):
    """Modalità di selezione della mossa dall'opening book"""

    BEST_SCORE = "best"  # Migliore punteggio assoluto
    WEIGHTED_RANDOM = "weighted"  # Random pesato per punteggio
    VARIETY_FIRST = "variety"  # Preferisce varietà (più continuazioni)
    SAFE_FIRST = "safe"  # Preferisce mosse bilanciate (=)
    AGGRESSIVE = "aggressive"  # Preferisce vantaggi forti (w++, b++)


@dataclass
class MoveEvaluation:
    """Valutazione dettagliata di una mossa dall'opening book"""

    move: str
    score: float  # Punteggio finale (weighted)
    advantage_score: float  # Punteggio da advantage
    variety_score: float  # Punteggio da varietà
    count_continuations: int  # Numero di continuazioni disponibili
    has_evaluation: bool  # Se ha dati di advantage
    advantage_symbol: Optional[str]  # Simbolo advantage (=, w, w+, etc.)
    is_above_threshold: bool  # Se supera la soglia configurata


class EnhancedOpeningBook(OpeningBook):
    """
    Versione avanzata dell'opening book con sistema di scoring sofisticato.

    RETROCOMPATIBILE con OpeningBook - può essere usato come drop-in replacement.

    Novità:
    - Soglia configurabile per filtrare mosse (score_threshold)
    - Filtro basato su media invece che solo valore assoluto
    - Sistema multi-criterio (advantage + variety + safety)
    - Modalità di selezione diverse
    - Analisi statistica avanzata

    Non utilizzato da giocatori esistenti - pronto per future estensioni.
    """

    def __init__(
        self,
        book_path=None,
        advantage_weight=0.2,
        variety_weight=0.1,
        only_evaluated_openings=True,
        score_threshold=0.0,  # NEW: Soglia minima score (default: 0.0)
        use_average_threshold=True,  # NEW: Usa media invece di valore assoluto
        selection_mode=SelectionMode.BEST_SCORE,  # NEW: Modalità selezione
        safety_weight=0.05,  # NEW: Peso per mosse sicure (=)
    ):
        """
        Inizializza enhanced opening book.

        Args:
            book_path: Path al file opening book
            advantage_weight: Peso per advantage evaluation (default: 0.2)
            variety_weight: Peso per varietà (default: 0.1)
            only_evaluated_openings: Solo aperture con advantage data
            score_threshold: Soglia minima per accettare mosse (default: 0.0)
            use_average_threshold: Se True, usa media delle mosse valide come soglia
            selection_mode: Modalità di selezione (BEST_SCORE, WEIGHTED_RANDOM, etc.)
            safety_weight: Peso bonus per mosse bilanciate '=' (default: 0.05)
        """
        # Inizializza la classe base (retrocompatibilità)
        super().__init__(
            book_path=book_path,
            advantage_weight=advantage_weight,
            variety_weight=variety_weight,
            only_evaluated_openings=only_evaluated_openings,
        )

        # Parametri avanzati (NEW!)
        self.score_threshold = score_threshold
        self.use_average_threshold = use_average_threshold
        self.selection_mode = selection_mode
        self.safety_weight = safety_weight

    def evaluate_move_detailed(
        self, move_str: str, game_history: str, available_moves: List
    ) -> MoveEvaluation:
        """
        Valutazione dettagliata di una mossa dall'opening book.

        Args:
            move_str: Mossa da valutare (es: "C4")
            game_history: Storia partita corrente
            available_moves: Tutte le mosse valide

        Returns:
            MoveEvaluation con scoring dettagliato
        """
        # Test se questa mossa è nel book
        test_sequence = game_history + move_str
        book_moves_after = self.get_book_moves(test_sequence)

        # Conta continuazioni disponibili
        count_continuations = len(book_moves_after) if book_moves_after else 0

        # Ottieni advantage per questa sequenza
        advantage = None
        for seq, adv in self.opening_advantages.items():
            if seq.upper().startswith(test_sequence.upper()):
                # Trova il primo advantage che matcha
                advantage = adv
                break

        # Calcola scores
        advantage_score = 0.0
        variety_score = 0.0
        safety_bonus = 0.0
        has_evaluation = advantage is not None

        if advantage:
            # Interpreta advantage
            _, numeric_value = self.interpret_advantage(advantage)
            advantage_score = numeric_value * self.advantage_weight

            # Bonus per mosse sicure (=)
            if advantage == "=":
                safety_bonus = self.safety_weight

        # Variety score (più continuazioni = meglio)
        if count_continuations > 0:
            # Normalizza: log scale per evitare che numeri alti dominino
            import math

            variety_score = math.log(1 + count_continuations) * self.variety_weight

        # Score finale
        total_score = advantage_score + variety_score + safety_bonus

        # Determina se supera soglia
        is_above_threshold = total_score >= self.score_threshold

        return MoveEvaluation(
            move=move_str,
            score=total_score,
            advantage_score=advantage_score,
            variety_score=variety_score,
            count_continuations=count_continuations,
            has_evaluation=has_evaluation,
            advantage_symbol=advantage,
            is_above_threshold=is_above_threshold,
        )

    def get_ranked_moves(self, game_history: str, available_moves: List) -> List[MoveEvaluation]:
        """
        Ottieni tutte le mosse rankkate con valutazioni dettagliate.

        Args:
            game_history: Storia partita corrente
            available_moves: Mosse valide

        Returns:
            Lista di MoveEvaluation ordinate per score (decrescente)
        """
        evaluations = []

        for move in available_moves:
            move_str = str(move).upper()
            eval_result = self.evaluate_move_detailed(move_str, game_history, available_moves)
            evaluations.append(eval_result)

        # Ordina per score (decrescente - migliore prima)
        evaluations.sort(key=lambda e: e.score, reverse=True)

        return evaluations

    def get_filtered_moves(
        self, game_history: str, available_moves: List, apply_threshold=True
    ) -> List[MoveEvaluation]:
        """
        Ottieni mosse filtrate in base ai criteri configurati.

        Args:
            game_history: Storia partita
            available_moves: Mosse valide
            apply_threshold: Se True, applica score_threshold

        Returns:
            Lista di MoveEvaluation filtrate e ordinate
        """
        # Ottieni tutte le valutazioni
        all_evals = self.get_ranked_moves(game_history, available_moves)

        if not apply_threshold:
            return all_evals

        # Determina soglia effettiva
        effective_threshold = self.score_threshold

        if self.use_average_threshold and all_evals:
            # Usa media come soglia se configurato
            scores = [e.score for e in all_evals if e.has_evaluation]
            if scores:
                average_score = sum(scores) / len(scores)
                # Usa il maggiore tra score_threshold e average
                effective_threshold = max(self.score_threshold, average_score)

        # Filtra mosse sopra soglia
        filtered = [e for e in all_evals if e.score >= effective_threshold]

        # Se il filtro elimina tutto, ritorna almeno la migliore
        if not filtered and all_evals:
            filtered = [all_evals[0]]

        return filtered

    def select_best_move(
        self, game_history: str, available_moves: List, mode: Optional[SelectionMode] = None
    ) -> Optional[str]:
        """
        Seleziona la migliore mossa secondo la modalità configurata.

        Args:
            game_history: Storia partita
            available_moves: Mosse valide
            mode: Modalità selezione (None = usa self.selection_mode)

        Returns:
            Stringa mossa selezionata o None
        """
        if mode is None:
            mode = self.selection_mode

        # Ottieni mosse filtrate
        filtered_moves = self.get_filtered_moves(game_history, available_moves)

        if not filtered_moves:
            return None

        # Selezione basata su modalità
        if mode == SelectionMode.BEST_SCORE:
            # Migliore punteggio assoluto
            return filtered_moves[0].move

        elif mode == SelectionMode.WEIGHTED_RANDOM:
            # Random pesato per score
            import random

            weights = [max(0.1, e.score + 1.0) for e in filtered_moves]  # +1 per evitare negativi
            total_weight = sum(weights)
            r = random.random() * total_weight

            cumulative = 0
            for eval_result, weight in zip(filtered_moves, weights):
                cumulative += weight
                if r <= cumulative:
                    return eval_result.move

            return filtered_moves[0].move  # Fallback

        elif mode == SelectionMode.VARIETY_FIRST:
            # Preferisce mosse con più continuazioni
            sorted_by_variety = sorted(
                filtered_moves, key=lambda e: e.count_continuations, reverse=True
            )
            return sorted_by_variety[0].move

        elif mode == SelectionMode.SAFE_FIRST:
            # Preferisce mosse bilanciate (=)
            safe_moves = [e for e in filtered_moves if e.advantage_symbol == "="]
            if safe_moves:
                return safe_moves[0].move
            return filtered_moves[0].move  # Fallback alla migliore

        elif mode == SelectionMode.AGGRESSIVE:
            # Preferisce vantaggi forti (w++, w+)
            aggressive_moves = [
                e for e in filtered_moves if e.advantage_symbol in ["w++", "w+", "b++", "b+"]
            ]
            if aggressive_moves:
                # Ordina per advantage score
                aggressive_moves.sort(key=lambda e: abs(e.advantage_score), reverse=True)
                return aggressive_moves[0].move
            return filtered_moves[0].move  # Fallback

        else:
            # Default: best score
            return filtered_moves[0].move

    def get_move_statistics(self, game_history: str, available_moves: List) -> Dict:
        """
        Ottieni statistiche dettagliate sulle mosse disponibili.

        Returns:
            Dict con statistiche complete per debug/analysis
        """
        all_evals = self.get_ranked_moves(game_history, available_moves)
        filtered_evals = self.get_filtered_moves(game_history, available_moves)

        stats = {
            "total_moves": len(all_evals),
            "filtered_moves": len(filtered_evals),
            "has_book_moves": any(e.has_evaluation for e in all_evals),
            "best_move": filtered_evals[0].move if filtered_evals else None,
            "best_score": filtered_evals[0].score if filtered_evals else 0.0,
            "average_score": sum(e.score for e in all_evals) / len(all_evals) if all_evals else 0.0,
            "threshold_used": self.score_threshold,
            "selection_mode": self.selection_mode.value,
            "evaluations": filtered_evals,
        }

        return stats


def get_enhanced_opening_book(
    score_threshold=0.0, use_average_threshold=True, selection_mode=SelectionMode.BEST_SCORE
):
    """
    Factory per creare EnhancedOpeningBook con configurazione default.

    Args:
        score_threshold: Soglia minima score (default: 0.0 - accetta solo positive)
        use_average_threshold: Usa media come soglia dinamica
        selection_mode: Modalità di selezione

    Returns:
        EnhancedOpeningBook configurato e pronto all'uso
    """
    import os

    # Determina path ai file opening book
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")

    # Cerca file opening book
    book_files = []
    if os.path.exists(data_dir):
        for filename in sorted(os.listdir(data_dir)):
            if filename.endswith(".txt") and "opening" in filename.lower():
                book_files.append(os.path.join(data_dir, filename))

    # Crea enhanced book (usa primo file o None)
    book_path = book_files[0] if book_files else None

    enhanced_book = EnhancedOpeningBook(
        book_path=book_path,
        advantage_weight=0.2,
        variety_weight=0.1,
        only_evaluated_openings=True,
        score_threshold=score_threshold,
        use_average_threshold=use_average_threshold,
        selection_mode=selection_mode,
        safety_weight=0.05,
    )

    # Carica eventuali file addizionali
    for additional_file in book_files[1:]:
        enhanced_book.load_additional_book(additional_file)

    return enhanced_book
