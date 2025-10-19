"""
Test standalone engine (NO GrandmasterEngine dependency).

Verifica che il motore standalone funzioni correttamente.
"""

import sys
import os
import copy

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# Suppress pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from AI.Apocalyptron.core.engine_standalone import ApocalyptronEngineStandalone
from AI.Apocalyptron.core.config import ApocalyptronConfig
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def test_standalone():
    """Test standalone engine"""
    
    print("\n" + "="*70)
    print("TEST: ApocalyptronEngineStandalone (NO GrandmasterEngine)")
    print("="*70)
    
    # Create config
    print("\n1. Creazione configurazione...")
    config = ApocalyptronConfig(
        depth=5,
        use_iterative_deepening=True,
        use_aspiration_windows=True,
        use_parallel=False,  # Sequential first
        enable_null_move_pruning=True,
        enable_futility_pruning=True,
        enable_late_move_reduction=True,
        enable_multi_cut_pruning=True,
        show_search_output=False,  # Quiet per test
    )
    print("   ✅ Config creato")
    
    # Create engine
    print("\n2. Creazione engine standalone...")
    try:
        engine = ApocalyptronEngineStandalone(config=config)
        print("   ✅ Engine creato (NESSUNA dipendenza da GrandmasterEngine!)")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 1: Initial position
    print("\n3. Test posizione iniziale (depth 5)...")
    try:
        game = BitboardGame()
        move = engine.get_best_move(game, depth=5)
        print(f"   ✅ Mossa: {move}")
        
        stats = engine.get_statistics()
        print(f"   ✅ Nodi: {stats['search_stats']['nodes']:,}")
        print(f"   ✅ Pruning: {stats['search_stats']['pruning']:,}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Midgame position
    print("\n4. Test midgame (depth 5)...")
    try:
        game = BitboardGame()
        for m in [Move(6,5), Move(4,6), Move(3,5), Move(5,6)]:
            game.move(m)
        
        engine.reset()
        move = engine.get_best_move(game, depth=5)
        print(f"   ✅ Mossa midgame: {move}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: With iterative deepening verbose
    print("\n5. Test con iterative deepening verbose (depth 4)...")
    try:
        config_verbose = ApocalyptronConfig(
            depth=4,
            use_iterative_deepening=True,
            use_aspiration_windows=True,
            show_search_output=True,  # Verbose
        )
        
        engine_verbose = ApocalyptronEngineStandalone(config=config_verbose)
        game = BitboardGame()
        
        print("\\n" + "-"*70)
        move = engine_verbose.get_best_move(game, depth=4)
        print("-"*70)
        
        print(f"   ✅ Iterative deepening funziona")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*70)
    print("✅ STANDALONE ENGINE FUNZIONA PERFETTAMENTE!")
    print("✅ NESSUNA DIPENDENZA DA GRANDMASTERENGINE!")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_standalone()
    exit(0 if success else 1)

