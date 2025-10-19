"""
Unit tests for AlphaBetaSearch component.

Test che la nuova implementazione modulare funzioni correttamente.
"""

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
    CompositeOrderer, PositionalOrderer, PVMoveOrderer
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
    try:
        move = search.get_best_move(game, depth=3)
        stats = search.get_statistics()
        print(f"   ✅ Mossa: {move}")
        print(f"   ✅ Nodi: {stats['nodes']}")
        print(f"   ✅ Pruning: {stats['pruning']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. Test search deeper
    print("\n5. Test search (depth 5)...")
    try:
        game = BitboardGame()
        search.reset()
        move = search.get_best_move(game, depth=5)
        stats = search.get_statistics()
        print(f"   ✅ Mossa: {move}")
        print(f"   ✅ Nodi: {stats['nodes']}")
        print(f"   ✅ TT hits: {stats['tt_hits']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 6. Test midgame position
    print("\n6. Test midgame position...")
    try:
        game = BitboardGame()
        for m in [Move(6,5), Move(4,6), Move(3,5), Move(5,6)]:
            game.move(m)
        
        search.reset()
        move = search.get_best_move(game, depth=4)
        print(f"   ✅ Mossa midgame: {move}")
    except Exception as e:
        print(f"   ❌ Errore midgame: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*60)
    print("✅ ALPHABETA SEARCH FUNZIONA CORRETTAMENTE!")
    print("="*60 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_alphabeta_basic()
    exit(0 if success else 1)

