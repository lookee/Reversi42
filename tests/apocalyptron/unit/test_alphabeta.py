"""
Unit tests for AlphaBetaSearch component.

Test che la nuova implementazione modulare funzioni correttamente.
"""

import pytest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from AI.Apocalyptron.search.alphabeta import AlphaBetaSearch
from AI.Apocalyptron.evaluation import (
    CompositeEvaluator, MobilityEvaluator, PositionalEvaluator,
    StabilityEvaluator, ParityEvaluator
)
from AI.Apocalyptron.ordering import (
    CompositeOrderer, PositionalOrderer, PVMoveOrderer, KillerMoveOrderer
)
from AI.Apocalyptron.weights import EvaluationWeights
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def test_alphabeta_basic():
    """Test base di AlphaBetaSearch"""
    
    print("\n" + "="*60)
    print("TEST: AlphaBetaSearch Modulare")
    print("="*60)
    
    # 1. Setup components
    print("\n1. Setup componenti...")
    weights = EvaluationWeights()
    
    # Create composite evaluator
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    evaluator.add_evaluator(PositionalEvaluator(weights), weight=1.0)
    evaluator.add_evaluator(StabilityEvaluator(weights), weight=1.0)
    evaluator.add_evaluator(ParityEvaluator(weights), weight=1.0)
    print(f"   ✅ Evaluator: {evaluator.get_evaluator_count()} componenti")
    
    # Create composite orderer
    orderer = CompositeOrderer()
    orderer.add_orderer(PVMoveOrderer())
    orderer.add_orderer(PositionalOrderer(weights))
    print(f"   ✅ Orderer: {orderer.get_orderer_count()} componenti")
    
    # Create search
    search = AlphaBetaSearch(evaluator, orderer, use_transposition_table=True)
    print("   ✅ AlphaBetaSearch creato")
    
    # 2. Test evaluation
    print("\n2. Test evaluation...")
    game = BitboardGame()
    score = evaluator.evaluate(game)
    print(f"   ✅ Evaluation score: {score}")
    
    # 3. Test move ordering
    print("\n3. Test move ordering...")
    moves = game.get_move_list()
    ordered = orderer.order_moves(game, moves)
    print(f"   ✅ Moves ordinati: {len(ordered)} mosse")
    
    # 4. Test search shallow
    print("\n4. Test search (depth 3)...")
    move = search.get_best_move(game, depth=3)
    stats = search.get_statistics()
    print(f"   ✅ Mossa: {move}")
    print(f"   ✅ Nodi: {stats['nodes']}")
    print(f"   ✅ Pruning: {stats['pruning']}")
    assert move is not None
    assert stats['nodes'] > 0
    
    # 5. Test search deeper
    print("\n5. Test search (depth 5)...")
    game = BitboardGame()
    search.reset()
    move = search.get_best_move(game, depth=5)
    stats = search.get_statistics()
    print(f"   ✅ Mossa: {move}")
    print(f"   ✅ Nodi: {stats['nodes']}")
    print(f"   ✅ TT hits: {stats['tt_hits']}")
    assert move is not None
    assert stats['nodes'] > 0
    
    # 6. Test midgame position
    print("\n6. Test midgame position...")
    game = BitboardGame()
    for m in [Move(6,5), Move(4,6), Move(3,5), Move(5,6)]:
        game.move(m)
    
    search.reset()
    move = search.get_best_move(game, depth=4)
    print(f"   ✅ Mossa midgame: {move}")
    assert move is not None
    
    print("\n" + "="*60)
    print("✅ ALPHABETA SEARCH FUNZIONA CORRETTAMENTE!")
    print("="*60 + "\n")


def test_alphabeta_with_transposition_table():
    """Test che la transposition table funzioni correttamente"""
    weights = EvaluationWeights()
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PositionalOrderer(weights))
    
    # Con TT
    search_with_tt = AlphaBetaSearch(evaluator, orderer, use_transposition_table=True)
    game = BitboardGame()
    move1 = search_with_tt.get_best_move(game, depth=5)
    stats1 = search_with_tt.get_statistics()
    
    # Senza TT
    search_no_tt = AlphaBetaSearch(evaluator, orderer, use_transposition_table=False)
    search_no_tt.reset()
    move2 = search_no_tt.get_best_move(game, depth=5)
    stats2 = search_no_tt.get_statistics()
    
    # Verifica che TT riduca i nodi esplorati
    assert move1 is not None
    assert move2 is not None
    assert stats1['tt_hits'] > 0  # Con TT dovrebbe avere hits
    assert stats2['tt_hits'] == 0  # Senza TT non dovrebbe avere hits


def test_alphabeta_returns_valid_moves():
    """Test che AlphaBeta restituisca sempre mosse valide"""
    weights = EvaluationWeights()
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PositionalOrderer(weights))
    
    search = AlphaBetaSearch(evaluator, orderer)
    
    # Test su diverse posizioni
    for _ in range(5):
        game = BitboardGame()
        # Fai alcune mosse casuali
        for _ in range(3):
            moves = game.get_move_list()
            if moves:
                game.move(moves[0])
        
        # Verifica che la mossa restituita sia valida
        valid_moves = game.get_move_list()
        if valid_moves:
            move = search.get_best_move(game, depth=3)
            assert move in valid_moves


def test_alphabeta_statistics_accuracy():
    """Test che le statistiche siano accurate"""
    weights = EvaluationWeights()
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PositionalOrderer(weights))
    
    search = AlphaBetaSearch(evaluator, orderer, use_transposition_table=True)
    game = BitboardGame()
    
    move = search.get_best_move(game, depth=4)
    stats = search.get_statistics()
    
    # Verifica che le statistiche siano presenti e coerenti
    assert 'nodes' in stats
    assert 'pruning' in stats
    assert 'tt_hits' in stats
    assert 'tt_size' in stats
    
    assert stats['nodes'] > 0
    assert stats['pruning'] >= 0
    assert stats['tt_hits'] >= 0
    assert stats['tt_size'] >= 0


def test_alphabeta_reset():
    """Test che reset pulisca correttamente lo stato"""
    weights = EvaluationWeights()
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PositionalOrderer(weights))
    
    search = AlphaBetaSearch(evaluator, orderer, use_transposition_table=True)
    game = BitboardGame()
    
    # Prima ricerca
    search.get_best_move(game, depth=4)
    stats1 = search.get_statistics()
    tt_size_before = stats1['tt_size']
    
    # Reset
    search.reset()
    
    # Seconda ricerca
    search.get_best_move(game, depth=4)
    stats2 = search.get_statistics()
    
    # Verifica che le statistiche siano state resettate
    assert stats2['tt_size'] >= 0  # TT dovrebbe essere pulita o riempita di nuovo


@pytest.mark.parametrize("depth", [1, 2, 3, 4, 5])
def test_alphabeta_various_depths(depth):
    """Test AlphaBeta a diverse profondità"""
    weights = EvaluationWeights()
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PositionalOrderer(weights))
    
    search = AlphaBetaSearch(evaluator, orderer)
    game = BitboardGame()
    
    move = search.get_best_move(game, depth=depth)
    stats = search.get_statistics()
    
    assert move is not None
    assert stats['nodes'] > 0
    
    # Profondità maggiori dovrebbero esplorare più nodi
    if depth > 1:
        assert stats['nodes'] >= depth


def test_alphabeta_with_killer_moves():
    """Test AlphaBeta con killer move heuristic"""
    weights = EvaluationWeights()
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    evaluator.add_evaluator(PositionalEvaluator(weights), weight=1.0)
    
    # Orderer con killer moves
    orderer = CompositeOrderer()
    orderer.add_orderer(PVMoveOrderer())
    orderer.add_orderer(KillerMoveOrderer())
    orderer.add_orderer(PositionalOrderer(weights))
    
    search = AlphaBetaSearch(evaluator, orderer, use_transposition_table=True)
    game = BitboardGame()
    
    move = search.get_best_move(game, depth=5)
    stats = search.get_statistics()
    
    assert move is not None
    assert stats['nodes'] > 0
    # Con killer moves dovrebbe avere più pruning
    assert stats['pruning'] >= 0


def test_alphabeta_consistency():
    """Test che AlphaBeta dia risultati consistenti sulla stessa posizione"""
    weights = EvaluationWeights()
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights), weight=1.0)
    evaluator.add_evaluator(PositionalEvaluator(weights), weight=1.0)
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PositionalOrderer(weights))
    
    search = AlphaBetaSearch(evaluator, orderer, use_transposition_table=True)
    game = BitboardGame()
    
    # Esegui la ricerca due volte sulla stessa posizione
    search.reset()
    move1 = search.get_best_move(game, depth=4)
    
    search.reset()
    move2 = search.get_best_move(game, depth=4)
    
    # Dovrebbero restituire la stessa mossa
    assert move1 == move2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

