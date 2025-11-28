#!/usr/bin/env python3
"""
Test script per verificare che il giocatore RL funzioni correttamente.

Usage:
    python experimental/test_rl_player.py
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from Players.PlayerFactory import PlayerFactory
from Reversi.BitboardGame import BitboardGame


def test_rl_player():
    """Test che il giocatore RL funzioni."""
    
    print("=" * 70)
    print("Test RL Player")
    print("=" * 70)
    print()
    
    # Verifica che il player sia disponibile
    print("1. Verifica disponibilità player...")
    metadata = PlayerFactory.get_all_player_metadata()
    if "RL Player" not in metadata:
        print("✗ RL Player non trovato!")
        return False
    
    print(f"✓ RL Player trovato: {metadata['RL Player']['display_name']}")
    print()
    
    # Verifica che il modello esista
    print("2. Verifica modello...")
    model_path = Path("experimental/checkpoints/latest.pth")
    if not model_path.exists():
        print(f"⚠ Modello non trovato: {model_path}")
        print("  Il giocatore funzionerà solo se il modello viene addestrato.")
        print("  Per ora continuiamo il test...")
    else:
        print(f"✓ Modello trovato: {model_path}")
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"  Dimensione: {size_mb:.1f} MB")
    print()
    
    # Crea giocatore
    print("3. Creazione giocatore...")
    try:
        rl_player = PlayerFactory.create_player("RL Player")
        print(f"✓ Giocatore creato: {rl_player.get_name()}")
    except Exception as e:
        print(f"✗ Errore creazione giocatore: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # Test mossa
    print("4. Test generazione mossa...")
    try:
        game = BitboardGame()
        legal_moves = game.get_move_list()
        
        if not legal_moves:
            print("⚠ Nessuna mossa legale nella posizione iniziale")
            return False
        
        print(f"  Posizione iniziale: {len(legal_moves)} mosse legali")
        print("  Generando mossa...")
        
        move = rl_player.get_move(game, legal_moves)
        
        if move:
            print(f"✓ Mossa generata: ({move.get_x()}, {move.get_y()})")
            print(f"  Mossa valida: {move in legal_moves}")
        else:
            print("✗ Nessuna mossa generata")
            return False
            
    except Exception as e:
        print(f"✗ Errore generazione mossa: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # Test partita breve
    print("5. Test partita breve (3 mosse)...")
    try:
        game = BitboardGame()
        moves_played = 0
        
        for _ in range(3):
            if game.is_finish():
                break
            
            legal_moves = game.get_move_list()
            if not legal_moves:
                game.pass_turn()
                continue
            
            move = rl_player.get_move(game, legal_moves)
            if move:
                game.move(move)
                moves_played += 1
                print(f"  Mossa {moves_played}: ({move.get_x()}, {move.get_y()})")
            else:
                break
        
        print(f"✓ Partita test completata: {moves_played} mosse giocate")
        
    except Exception as e:
        print(f"✗ Errore durante partita test: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    print("=" * 70)
    print("✓ Tutti i test passati!")
    print("=" * 70)
    print()
    print("Il giocatore RL è pronto per essere utilizzato!")
    print()
    print("Prossimi passi:")
    print("  1. Avvia web GUI: python -m src.ui.web")
    print("  2. Seleziona 'RL Player' come avversario")
    print("  3. Gioca!")
    
    return True


if __name__ == "__main__":
    success = test_rl_player()
    sys.exit(0 if success else 1)

