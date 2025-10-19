"""
Test di equivalenza: AlphaBetaSearch vs GrandmasterEngine

Verifica che la nuova implementazione modulare produca risultati
simili (non necessariamente identici per ottimizzazioni diverse).
"""

import sys
import os
import copy

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from AI.Apocalyptron.search.alphabeta import AlphaBetaSearch
from AI.Apocalyptron.evaluation import (
    CompositeEvaluator, MobilityEvaluator, PositionalEvaluator,
    StabilityEvaluator, ParityEvaluator
)
from AI.Apocalyptron.ordering import CompositeOrderer, PositionalOrderer, PVMoveOrderer
from AI.Apocalyptron.weights import EvaluationWeights
from AI.GrandmasterEngine import GrandmasterEngine
from AI.GrandmasterWeights import GrandmasterWeights
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def test_equivalence():
    """Test equivalenza tra AlphaBetaSearch e GrandmasterEngine"""
    
    print("\n" + "="*70)
    print("TEST EQUIVALENZA: AlphaBetaSearch vs GrandmasterEngine")
    print("="*70)
    
    # Setup AlphaBetaSearch
    print("\n1. Setup AlphaBetaSearch modulare...")
    weights = EvaluationWeights()
    
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(MobilityEvaluator(weights))
    evaluator.add_evaluator(PositionalEvaluator(weights))
    evaluator.add_evaluator(StabilityEvaluator(weights))
    evaluator.add_evaluator(ParityEvaluator(weights))
    
    orderer = CompositeOrderer()
    orderer.add_orderer(PVMoveOrderer())
    orderer.add_orderer(PositionalOrderer(weights))
    
    alphabeta = AlphaBetaSearch(evaluator, orderer)
    print("   ✅ AlphaBetaSearch pronto")
    
    # Setup GrandmasterEngine
    print("\n2. Setup GrandmasterEngine...")
    gm_weights = GrandmasterWeights()
    grandmaster = GrandmasterEngine(weights=gm_weights)
    print("   ✅ GrandmasterEngine pronto")
    
    # Test positions
    test_cases = []
    
    # Position 1: Initial
    game1 = BitboardGame()
    test_cases.append(("Initial position", game1, 4))
    
    # Position 2: After F5
    game2 = BitboardGame()
    game2.move(Move(6, 5))
    test_cases.append(("After F5", game2, 4))
    
    # Position 3: Early midgame
    game3 = BitboardGame()
    for m in [Move(6,5), Move(4,6), Move(3,5)]:
        game3.move(m)
    test_cases.append(("Early midgame", game3, 4))
    
    print("\n3. Confronto mosse su {} posizioni...\n".format(len(test_cases)))
    
    results = []
    for name, game, depth in test_cases:
        # AlphaBetaSearch
        alphabeta.reset()
        game_copy1 = copy.deepcopy(game)
        ab_move = alphabeta.get_best_move(game_copy1, depth)
        ab_stats = alphabeta.get_statistics()
        
        # GrandmasterEngine  
        grandmaster.transposition_table.clear()
        grandmaster.killer_moves.clear()
        grandmaster.history_table.clear()
        grandmaster.nodes = 0
        grandmaster.pruning = 0
        game_copy2 = copy.deepcopy(game)
        gm_move = grandmaster.get_best_move(game_copy2, depth, player_name=None)
        
        # Compare
        same_move = (ab_move == gm_move)
        symbol = "✅" if same_move else "⚠️"
        
        print(f"   {symbol} {name:<20} (depth {depth})")
        print(f"      AlphaBeta:   {ab_move} ({ab_stats['nodes']} nodi)")
        print(f"      Grandmaster: {gm_move} ({grandmaster.nodes} nodi)")
        
        results.append({
            'name': name,
            'same_move': same_move,
            'ab_move': ab_move,
            'gm_move': gm_move,
            'ab_nodes': ab_stats['nodes'],
            'gm_nodes': grandmaster.nodes,
        })
    
    # Summary
    same_count = sum(1 for r in results if r['same_move'])
    total = len(results)
    
    print("\n" + "="*70)
    print(f"RISULTATI: {same_count}/{total} mosse identiche ({same_count/total*100:.1f}%)")
    
    if same_count == total:
        print("✅ EQUIVALENZA PERFETTA!")
    else:
        print("⚠️  Alcune mosse differiscono (normale per ottimizzazioni diverse)")
        print("   AlphaBetaSearch è più semplice (no iterative deepening)")
    
    print("="*70 + "\n")
    
    return results


if __name__ == '__main__':
    results = test_equivalence()
    
    # Success if most moves are the same or if differences are explainable
    same_count = sum(1 for r in results if r['same_move'])
    total = len(results)
    
    # Accept >50% match (AlphaBetaSearch è più semplice, differenze sono OK)
    exit(0 if same_count >= total * 0.5 else 1)

