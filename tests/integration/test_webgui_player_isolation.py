#!/usr/bin/env python3
"""
Test script to verify player isolation in WebGUI-like scenario.

This simulates exactly what the WebGUI server does:
1. Creates a GameSession-like structure
2. Creates players
3. Calls get_ai_move multiple times
4. Verifies configurations remain correct
"""

import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)

from Players.PlayerFactory import PlayerFactory
from Reversi.Game import Game, Move

class MockGameSession:
    """Simulates GameSession from webgui server"""
    
    def __init__(self, ai_white_name, ai_black_name):
        self.ai_white_name = ai_white_name
        self.ai_black_name = ai_black_name
        self.game = Game(8)
        
        # Clear cache first
        registry = PlayerFactory._get_registry()
        registry.clear_instance_cache()
        
        # Create AI players (exactly like webgui server does)
        self.ai_white = None
        self.ai_black = None
        
        if self.ai_white_name:
            self.ai_white = PlayerFactory.create_player(self.ai_white_name)
        
        if self.ai_black_name:
            self.ai_black = PlayerFactory.create_player(self.ai_black_name)
    
    def get_ai_move(self, side):
        """Simulates get_ai_move from webgui server"""
        move_list = self.game.get_move_list()
        if not move_list:
            return None
        
        # Select AI by side (exactly like webgui server)
        ai = self.ai_white if side == 'W' else self.ai_black
        ai_name = self.ai_white_name if side == 'W' else self.ai_black_name
        
        if ai is None:
            return None
        
        # CRITICAL: Verify configuration BEFORE getting move
        if hasattr(ai, 'bitboard_engine') and hasattr(ai.bitboard_engine, 'config'):
            cfg = ai.bitboard_engine.config
            
            # Verify for known players
            if ai_name == "LIGHTNING STRIKE":
                if cfg.depth != 4:
                    raise ValueError(f"LIGHTNING STRIKE has wrong depth! Expected 4, got {cfg.depth}")
                if cfg.search_strategy != 'fixed_depth':
                    raise ValueError(f"LIGHTNING STRIKE has wrong strategy! Expected fixed_depth, got {cfg.search_strategy}")
            elif ai_name == "DIVZERO.EXE":
                if cfg.depth != 12:
                    raise ValueError(f"DIVZERO.EXE has wrong depth! Expected 12, got {cfg.depth}")
                if cfg.search_strategy != 'adaptive':
                    raise ValueError(f"DIVZERO.EXE has wrong strategy! Expected adaptive, got {cfg.search_strategy}")
        
        # Get move (exactly like webgui server)
        ai_move = ai.get_move(self.game, move_list)
        return ai_move

def test_webgui_simulation():
    """Test player isolation in WebGUI-like scenario"""
    
    print("=" * 80)
    print("🧪 TEST: WebGUI Server Player Isolation Simulation")
    print("=" * 80)
    print()
    
    # Create session (exactly like webgui server)
    session = MockGameSession("LIGHTNING STRIKE", "DIVZERO.EXE")
    
    print("─" * 80)
    print("Initial Configuration Verification")
    print("─" * 80)
    
    # Verify initial configurations
    white_cfg = session.ai_white.bitboard_engine.config
    black_cfg = session.ai_black.bitboard_engine.config
    
    print(f"⚪ White (LIGHTNING STRIKE):")
    print(f"   Instance ID: {id(session.ai_white)}")
    print(f"   Config ID: {id(white_cfg)}")
    print(f"   Depth: {white_cfg.depth} (expected: 4)")
    print(f"   Strategy: {white_cfg.search_strategy} (expected: fixed_depth)")
    
    print(f"⚫ Black (DIVZERO.EXE):")
    print(f"   Instance ID: {id(session.ai_black)}")
    print(f"   Config ID: {id(black_cfg)}")
    print(f"   Depth: {black_cfg.depth} (expected: 12)")
    print(f"   Strategy: {black_cfg.search_strategy} (expected: adaptive)")
    
    # Store initial IDs
    initial_white_id = id(session.ai_white)
    initial_black_id = id(session.ai_black)
    initial_white_cfg_id = id(white_cfg)
    initial_black_cfg_id = id(black_cfg)
    
    print()
    print("─" * 80)
    print("Playing Game (up to 10 moves)")
    print("─" * 80)
    
    errors = []
    move_count = 0
    max_moves = 10
    
    while move_count < max_moves:
        move_count += 1
        current_turn = session.game.turn
        current_side = 'W' if current_turn == 'W' else 'B'
        
        print()
        print(f"Move {move_count}: {current_side} ({session.game.turn})")
        
        # CRITICAL: Verify instances haven't changed
        if id(session.ai_white) != initial_white_id:
            error_msg = f"Move {move_count}: White instance changed! Initial: {initial_white_id}, Current: {id(session.ai_white)}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
        
        if id(session.ai_black) != initial_black_id:
            error_msg = f"Move {move_count}: Black instance changed! Initial: {initial_black_id}, Current: {id(session.ai_black)}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
        
        # CRITICAL: Verify configs haven't changed
        current_white_cfg = session.ai_white.bitboard_engine.config
        current_black_cfg = session.ai_black.bitboard_engine.config
        
        if id(current_white_cfg) != initial_white_cfg_id:
            error_msg = f"Move {move_count}: White config changed! Initial: {initial_white_cfg_id}, Current: {id(current_white_cfg)}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
        
        if id(current_black_cfg) != initial_black_cfg_id:
            error_msg = f"Move {move_count}: Black config changed! Initial: {initial_black_cfg_id}, Current: {id(current_black_cfg)}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
        
        # Get AI move (this will verify config internally)
        try:
            ai_move = session.get_ai_move(current_side)
            if ai_move:
                coord = f"{chr(64+ai_move.x)}{ai_move.y}"
                print(f"   ✅ Move: {coord}")
                session.game.move(ai_move)
            else:
                print("   No move, passing...")
                session.game.pass_turn()
        except ValueError as e:
            error_msg = f"Move {move_count}: Configuration error: {e}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
            break
        except Exception as e:
            error_msg = f"Move {move_count}: Error: {e}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
            import traceback
            traceback.print_exc()
            break
        
        # Special check at move 4
        if move_count == 4:
            print()
            print("   🔍 SPECIAL CHECK AT MOVE 4:")
            print(f"      White instance ID: {id(session.ai_white)}")
            print(f"      Black instance ID: {id(session.ai_black)}")
            print(f"      White config ID: {id(session.ai_white.bitboard_engine.config)}")
            print(f"      Black config ID: {id(session.ai_black.bitboard_engine.config)}")
            print(f"      White depth: {session.ai_white.bitboard_engine.config.depth}")
            print(f"      Black depth: {session.ai_black.bitboard_engine.config.depth}")
            print(f"      White strategy: {session.ai_white.bitboard_engine.config.search_strategy}")
            print(f"      Black strategy: {session.ai_black.bitboard_engine.config.search_strategy}")
            
            if session.ai_white.bitboard_engine.config.depth != 4:
                error_msg = "Move 4: White lost its configuration!"
                print(f"      ❌ {error_msg}")
                errors.append(error_msg)
            
            if session.ai_black.bitboard_engine.config.depth != 12:
                error_msg = "Move 4: Black lost its configuration!"
                print(f"      ❌ {error_msg}")
                errors.append(error_msg)
    
    print()
    print("=" * 80)
    if errors:
        print("❌ TEST FAILED!")
        print(f"   Found {len(errors)} error(s):")
        for error in errors:
            print(f"   - {error}")
        print("=" * 80)
        return False
    else:
        print("✅ ALL TESTS PASSED!")
        print("   Players maintained correct configurations throughout the game")
        print("=" * 80)
        return True

if __name__ == "__main__":
    try:
        success = test_webgui_simulation()
        sys.exit(0 if success else 1)
    except Exception as e:
        import traceback
        print(f"❌ TEST FAILED with exception:")
        print(traceback.format_exc())
        sys.exit(1)

