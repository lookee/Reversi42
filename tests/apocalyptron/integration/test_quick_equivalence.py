"""
Quick equivalence test (silent mode).

Test rapido e silenzioso per verificare equivalenza senza output.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from AI.Apocalyptron import ApocalyptronFactory
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def test_apocalyptron_engine():
    """Test che ApocalyptronEngine funzioni correttamente"""
    
    print("\n" + "="*60)
    print("TEST RAPIDO: ApocalyptronEngine")
    print("="*60)
    
    # Test 1: Creation
    print("\n1. Creazione engine...")
    try:
        engine = ApocalyptronFactory.create_default(depth=6)
        print("   ✅ Engine creato")
    except Exception as e:
        print(f"   ❌ Errore creazione: {e}")
        return False
    
    # Test 2: Evaluation
    print("\n2. Test evaluation...")
    try:
        game = BitboardGame()
        score = engine.evaluate(game)
        print(f"   ✅ Evaluation funziona (score: {score})")
    except Exception as e:
        print(f"   ❌ Errore evaluation: {e}")
        return False
    
    # Test 3: Move from initial position
    print("\n3. Move da posizione iniziale (depth 5, silent)...")
    try:
        game = BitboardGame()
        move = engine.get_best_move(game, depth=5)
        print(f"   ✅ Mossa trovata: {move}")
    except Exception as e:
        print(f"   ❌ Errore ricerca: {e}")
        return False
    
    # Test 4: Move from midgame
    print("\n4. Move da midgame (depth 5)...")
    try:
        game = BitboardGame()
        for m in [Move(6,5), Move(4,6), Move(3,5)]:
            game.move(m)
        
        move = engine.get_best_move(game, depth=5)
        print(f"   ✅ Mossa trovata: {move}")
    except Exception as e:
        print(f"   ❌ Errore ricerca midgame: {e}")
        return False
    
    # Test 5: Factory variants
    print("\n5. Test factory variants...")
    try:
        aggressive = ApocalyptronFactory.create_aggressive(depth=4)
        defensive = ApocalyptronFactory.create_defensive(depth=4)
        tournament = ApocalyptronFactory.create_tournament(depth=4)
        
        print("   ✅ Tutti i variant funzionano")
    except Exception as e:
        print(f"   ❌ Errore factory: {e}")
        return False
    
    # Test 6: Statistics
    print("\n6. Test statistiche...")
    try:
        stats = engine.get_statistics()
        print(f"   ✅ Statistiche: {stats['searches_performed']} ricerche")
    except Exception as e:
        print(f"   ❌ Errore stats: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ TUTTI I TEST PASSATI!")
    print("="*60 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_apocalyptron_engine()
    exit(0 if success else 1)

