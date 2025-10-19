"""
Test AlphaBetaSearchComplete isolato.

Verifica che l'implementazione completa funzioni correttamente.
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.evaluation import (
    CompositeEvaluator, MobilityEvaluator, PositionalEvaluator
)
from AI.Apocalyptron.ordering import (
    CompositeOrderer, PositionalOrderer, PVMoveOrderer,
    KillerMoveOrderer, HistoryHeuristicOrderer
)
from AI.Apocalyptron.weights import EvaluationWeights
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def test():
    print("\n" + "="*60)
    print("TEST: AlphaBetaSearchComplete")
    print("="*60)
    
    # Setup
    print("\n1. Setup componenti...")
    weights = EvaluationWeights()
    
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights))
    evaluator.add_evaluator(PositionalEvaluator(weights))
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PVMoveOrderer())
    orderer.add_orderer(KillerMoveOrderer())
    orderer.add_orderer(HistoryHeuristicOrderer())
    orderer.add_orderer(PositionalOrderer(weights))
    
    search = AlphaBetaSearchComplete(evaluator, orderer)
    print(f"   ✅ AlphaBetaSearchComplete creato")
    
    # Test shallow
    print("\n2. Test depth 2 (veloce)...")
    try:
        game = BitboardGame()
        move = search.get_best_move(game, depth=2)
        print(f"   ✅ Mossa depth 2: {move}")
        print(f"   ✅ Nodi: {search.nodes}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test depth 3
    print("\n3. Test depth 3...")
    try:
        game = BitboardGame()
        search.reset()
        move = search.get_best_move(game, depth=3)
        stats = search.get_statistics()
        print(f"   ✅ Mossa depth 3: {move}")
        print(f"   ✅ Nodi: {stats['nodes']}, Pruning: {stats['pruning']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test depth 4
    print("\n4. Test depth 4...")
    try:
        game = BitboardGame()
        search.reset()
        move = search.get_best_move(game, depth=4)
        stats = search.get_statistics()
        print(f"   ✅ Mossa depth 4: {move}")
        print(f"   ✅ Nodi: {stats['nodes']}, Pruning: {stats['pruning']}")
        
        if 'null_move' in stats:
            print(f"   ✅ Null move: {stats['null_move']}")
        if 'futility' in stats:
            print(f"   ✅ Futility: {stats['futility']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*60)
    print("✅ AlphaBetaSearchComplete FUNZIONA!")
    print("="*60 + "\n")
    
    return True


if __name__ == '__main__':
    success = test()
    exit(0 if success else 1)

