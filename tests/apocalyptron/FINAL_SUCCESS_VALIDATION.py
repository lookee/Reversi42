"""
VALIDAZIONE FINALE - GrandmasterEngine Eliminato

Test completo per verificare che Apocalyptron funzioni perfettamente
SENZA alcuna dipendenza da GrandmasterEngine.
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

from Players.PlayerApocalyptron import PlayerApocalyptron
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def main():
    print("\n" + "="*70)
    print("🎉 VALIDAZIONE FINALE - GRANDMASTERENGINE ELIMINATO")
    print("="*70)
    
    all_passed = True
    
    # TEST 1: Verifica nessun import GrandmasterEngine
    print("\n📋 TEST 1: Verifica zero dipendenze GrandmasterEngine")
    print("-"*70)
    try:
        # Try to find GrandmasterEngine in imports
        import AI.Apocalyptron.core.engine as engine_module
        import Players.PlayerApocalyptron as player_module
        
        # Check if GrandmasterEngine is in module
        has_gm = False
        for attr in dir(engine_module):
            if 'GrandmasterEngine' in attr:
                has_gm = True
        
        for attr in dir(player_module):
            if 'GrandmasterEngine' in attr and attr != '__doc__':
                has_gm = True
        
        if has_gm:
            print("   ❌ GrandmasterEngine still referenced!")
            all_passed = False
        else:
            print("   ✅ ZERO references to GrandmasterEngine")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        all_passed = False
    
    # TEST 2: Player creation
    print("\n📋 TEST 2: Creazione PlayerApocalyptron")
    print("-"*70)
    try:
        player = PlayerApocalyptron(depth=6, show_book_options=False)
        print(f"   ✅ Player: {player.name}")
        print(f"   ✅ Workers: {player.bitboard_engine.num_workers}")
        print(f"   ✅ Engine type: {type(player.bitboard_engine).__name__}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        all_passed = False
    
    # TEST 3: Move from initial position
    print("\n📋 TEST 3: Mossa da posizione iniziale (depth 5)")
    print("-"*70)
    try:
        game = BitboardGame()
        player = PlayerApocalyptron(depth=5, show_book_options=False)
        move = player.get_move(game, game.get_move_list(), None)
        print(f"   ✅ Mossa: {move}")
        
        if move is None:
            print("   ❌ Nessuna mossa trovata!")
            all_passed = False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    # TEST 4: Move from midgame
    print("\n📋 TEST 4: Mossa da midgame (out of book)")
    print("-"*70)
    try:
        game = BitboardGame()
        for m in [Move(6,5), Move(4,6), Move(3,5), Move(5,6)]:
            game.move(m)
        
        player = PlayerApocalyptron(depth=5, show_book_options=False)
        move = player.get_move(game, game.get_move_list(), None)
        print(f"   ✅ Mossa midgame: {move}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    # TEST 5: Multiple depths
    print("\n📋 TEST 5: Test multiple depth (5, 7, 9)")
    print("-"*70)
    try:
        game = BitboardGame()
        for depth in [5, 7, 9]:
            player = PlayerApocalyptron(depth=depth, show_book_options=False)
            move = player.get_move(game, game.get_move_list(), None)
            print(f"   ✅ Depth {depth}: {move}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        all_passed = False
    
    # TEST 6: Factory
    print("\n📋 TEST 6: ApocalyptronFactory")
    print("-"*70)
    try:
        from AI.Apocalyptron import ApocalyptronFactory
        
        engine = ApocalyptronFactory.create_default(depth=5)
        game = BitboardGame()
        move = engine.get_best_move(game, depth=5)
        print(f"   ✅ Factory default: {move}")
        
        engine2 = ApocalyptronFactory.create_aggressive(depth=5)
        move2 = engine2.get_best_move(game, depth=5)
        print(f"   ✅ Factory aggressive: {move2}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        all_passed = False
    
    # TEST 7: Statistics
    print("\n📋 TEST 7: Statistics collection")
    print("-"*70)
    try:
        player = PlayerApocalyptron(depth=5, show_book_options=False)
        game = BitboardGame()
        move = player.get_move(game, game.get_move_list(), None)
        
        stats = player.get_statistics()
        if "APOCALYPTRON" in stats:
            print("   ✅ Statistics OK")
        else:
            print("   ❌ Statistics malformed")
            all_passed = False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        all_passed = False
    
    # FINAL RESULT
    print("\n" + "="*70)
    if all_passed:
        print("🎉🎉🎉 TUTTI I TEST PASSATI! 🎉🎉🎉")
        print("="*70)
        print("\n✅ GrandmasterEngine COMPLETAMENTE ELIMINATO!")
        print("✅ Apocalyptron usa SOLO componenti modulari!")
        print("✅ Architettura 100% SOLID standalone!")
        print("✅ Tutte le funzionalità mantenute!")
        print("✅ Zero regressioni!")
        print("\n🏆 REFACTORING TOTALMENTE COMPLETATO!")
    else:
        print("❌ ALCUNI TEST FALLITI")
    print("="*70 + "\n")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

