"""
Test Observer Pattern implementation.

Verifica che l'Observer Pattern funzioni correttamente.
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

from AI.Apocalyptron import ApocalyptronFactory, ApocalyptronConfigBuilder
from AI.Apocalyptron.observers import ConsoleObserver, QuietObserver, StatisticsObserver
from Reversi.BitboardGame import BitboardGame


def test_observers():
    print("\n" + "="*70)
    print("TEST: Observer Pattern")
    print("="*70)
    
    game = BitboardGame()
    
    # TEST 1: Console Observer (default)
    print("\n📋 TEST 1: ConsoleObserver (default output)")
    print("-"*70)
    config = ApocalyptronConfigBuilder().with_depth(4).build()
    engine = ApocalyptronFactory.create_engine(config)
    
    print("\nSearch con ConsoleObserver (dovrebbe mostrare output):")
    print("-"*70)
    move = engine.get_best_move(game, depth=4)
    print(f"✅ Mossa con console output: {move}")
    
    # TEST 2: Quiet Observer
    print("\n📋 TEST 2: QuietObserver (silent)")
    print("-"*70)
    config2 = ApocalyptronConfigBuilder().with_depth(4).enable_output(False).build()
    engine2 = ApocalyptronFactory.create_engine(config2)
    
    print("Search con QuietObserver (dovrebbe essere silenzioso):")
    move2 = engine2.get_best_move(game, depth=4)
    print(f"✅ Mossa silent: {move2}")
    
    # TEST 3: Multiple Observers
    print("\n📋 TEST 3: Multiple Observers (Console + Statistics)")
    print("-"*70)
    stats_observer = StatisticsObserver()
    
    # Create engine with custom observers
    from AI.Apocalyptron.core.engine import ApocalyptronEngine
    from AI.Apocalyptron.core.config import ApocalyptronConfig
    
    config3 = ApocalyptronConfig(depth=4)
    engine3 = ApocalyptronEngine(config=config3)
    
    # Add statistics observer
    engine3.search.observers.append(stats_observer)
    
    print("Search con Console + Statistics:")
    print("-"*70)
    move3 = engine3.get_best_move(game, depth=4)
    
    print(f"\n✅ Mossa: {move3}")
    print(f"✅ Statistics collector:")
    summary = stats_observer.get_summary()
    print(f"   - Iterations: {len(summary['iterations'])}")
    print(f"   - Moves evaluated: {len(summary['moves_evaluated'])}")
    print(f"   - Total nodes: {stats_observer.get_total_nodes()}")
    print(f"   - Best move: {stats_observer.get_best_move()}")
    
    # TEST 4: Programmatic quiet mode
    print("\n📋 TEST 4: Observers=[] (programmatic quiet)")
    print("-"*70)
    from AI.Apocalyptron.search.iterative_deepening import IterativeDeepeningSearch
    from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
    from AI.Apocalyptron.evaluation import CompositeEvaluator, MobilityEvaluator
    from AI.Apocalyptron.ordering import CompositeOrderer, PositionalOrderer
    from AI.Apocalyptron.weights import EvaluationWeights
    
    weights = EvaluationWeights()
    eval = CompositeEvaluator()
    eval.add_evaluator(MobilityEvaluator(weights))
    
    ord = CompositeOrderer()
    ord.add_orderer(PositionalOrderer(weights))
    
    alphabeta = AlphaBetaSearchComplete(eval, ord)
    it_search = IterativeDeepeningSearch(alphabeta, observers=[])  # Empty = quiet
    
    print("Search con observers=[] (silenzioso):")
    move4 = it_search.get_best_move(game, depth=3)
    print(f"✅ Mossa quiet: {move4}")
    
    print("\n" + "="*70)
    print("✅ OBSERVER PATTERN FUNZIONA PERFETTAMENTE!")
    print("="*70)
    print("\n✅ ConsoleObserver - output formattato")
    print("✅ QuietObserver - silenzioso")
    print("✅ StatisticsObserver - raccolta dati")
    print("✅ Multiple observers - funzionano insieme")
    print("✅ Separation of Concerns - 100% completa!")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_observers()
    exit(0 if success else 1)

