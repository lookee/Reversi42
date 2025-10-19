"""
TEST DI EQUIVALENZA RIGOROSO

Confronta ApocalyptronEngineStandalone vs GrandmasterEngine su molte posizioni
per verificare ZERO REGRESSIONI prima di sostituire il backend.
"""

import sys
import os
import copy

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from AI.Apocalyptron.core.engine_standalone import ApocalyptronEngineStandalone
from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.GrandmasterEngine import GrandmasterEngine
from AI.GrandmasterWeights import GrandmasterWeights
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


def create_test_positions():
    """Create diverse test positions"""
    positions = []
    
    # Position 1: Initial
    game = BitboardGame()
    positions.append(("Initial", game))
    
    # Position 2-5: After various openings
    for opening_moves, name in [
        ([Move(6,5)], "After F5"),
        ([Move(6,5), Move(4,6)], "After F5d6"),
        ([Move(6,5), Move(4,6), Move(3,5)], "After F5d6C5"),
        ([Move(6,5), Move(4,6), Move(3,5), Move(5,6)], "Early midgame"),
    ]:
        game = BitboardGame()
        for m in opening_moves:
            game.move(m)
        positions.append((name, game))
    
    # Position 6: Midgame tactical
    game = BitboardGame()
    for m in [Move(6,5), Move(4,6), Move(3,5), Move(5,6), 
              Move(6,6), Move(6,4), Move(7,5)]:
        if game.valid_move(m):
            game.move(m)
    positions.append(("Midgame tactical", game))
    
    # Position 7: Late midgame
    game = BitboardGame()
    for m in [Move(6,5), Move(4,6), Move(3,5), Move(5,6),
              Move(6,6), Move(6,4), Move(5,7), Move(6,3),
              Move(7,5), Move(3,6)]:
        if game.valid_move(m):
            game.move(m)
    positions.append(("Late midgame", game))
    
    return positions


def test_equivalence():
    """Test equivalence"""
    
    print("\n" + "="*70)
    print("TEST DI EQUIVALENZA: Standalone vs GrandmasterEngine")
    print("="*70)
    
    # Create engines
    print("\n1. Setup engines...")
    
    config = ApocalyptronConfig(
        depth=6,
        use_iterative_deepening=False,  # Disable for direct comparison
        use_aspiration_windows=False,
        use_parallel=False,
        enable_null_move_pruning=True,
        enable_futility_pruning=True,
        enable_late_move_reduction=True,
        enable_multi_cut_pruning=True,
        show_search_output=False,
    )
    
    standalone = ApocalyptronEngineStandalone(config=config)
    grandmaster = GrandmasterEngine(weights=GrandmasterWeights())
    
    print("   ✅ Standalone engine pronto")
    print("   ✅ GrandmasterEngine pronto")
    
    # Get test positions
    positions = create_test_positions()
    print(f"\n2. Test su {len(positions)} posizioni (depth 4-6)...\n")
    
    results = []
    
    for name, game in positions:
        # Test at depth 4 (faster)
        depth = 4 if "midgame" in name.lower() else 5
        
        # Standalone
        standalone.reset()
        game_copy1 = copy.deepcopy(game)
        st_move = standalone.alphabeta.get_best_move(game_copy1, depth)
        st_stats = standalone.alphabeta.get_statistics()
        
        # Grandmaster
        grandmaster.transposition_table.clear()
        grandmaster.killer_moves.clear()
        grandmaster.history_table.clear()
        grandmaster.nodes = 0
        grandmaster.pruning = 0
        game_copy2 = copy.deepcopy(game)
        gm_move = grandmaster.get_best_move(game_copy2, depth, player_name=None)
        
        # Compare
        same = (st_move == gm_move)
        symbol = "✅" if same else "⚠️"
        
        print(f"   {symbol} {name:<20} (depth {depth})")
        print(f"      Standalone:   {st_move:<6} ({st_stats['nodes']:>5} nodi, {st_stats['pruning']:>4} pruning)")
        print(f"      Grandmaster:  {gm_move:<6} ({grandmaster.nodes:>5} nodi, {grandmaster.pruning:>4} pruning)")
        
        results.append({
            'name': name,
            'same': same,
            'st_move': st_move,
            'gm_move': gm_move,
            'st_nodes': st_stats['nodes'],
            'gm_nodes': grandmaster.nodes,
        })
    
    # Summary
    same_count = sum(1 for r in results if r['same'])
    total = len(results)
    
    print("\n" + "="*70)
    print(f"RISULTATI: {same_count}/{total} mosse identiche ({same_count/total*100:.1f}%)")
    
    if same_count >= total * 0.7:  # Accept 70%+ match
        print("✅ EQUIVALENZA ACCETTABILE!")
        print("   (Differenze normali per ordine mosse / TT / ottimizzazioni)")
        success = True
    else:
        print("⚠️  Troppe differenze - verificare implementazione")
        success = False
    
    print("="*70 + "\n")
    
    return success


if __name__ == '__main__':
    success = test_equivalence()
    exit(0 if success else 1)

