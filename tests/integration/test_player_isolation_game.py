#!/usr/bin/env python3
"""
Test script to verify player isolation during an actual game.

This script simulates a complete game between DIVZERO.EXE and LIGHTNING STRIKE
and verifies that each player maintains its correct configuration throughout
the game, especially at critical points like the 4th move.
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

def simulate_game_and_verify():
    """Simulate a game and verify player isolation at each move."""
    
    print("=" * 80)
    print("🧪 TEST: Player Isolation During Game Simulation")
    print("=" * 80)
    print()
    
    # Clear registry cache first
    print("🧹 Clearing registry cache...")
    registry = PlayerFactory._get_registry()
    registry.clear_instance_cache()
    print("✅ Cache cleared")
    print()
    
    # Create players
    print("─" * 80)
    print("Creating AI Players")
    print("─" * 80)
    
    player_black_name = "DIVZERO.EXE"
    player_white_name = "LIGHTNING STRIKE"
    
    print(f"Creating ⚫ Black: {player_black_name}")
    player_black = PlayerFactory.create_player(player_black_name)
    black_id = id(player_black)
    print(f"✅ Created: {type(player_black).__name__} @ {black_id}")
    
    print(f"Creating ⚪ White: {player_white_name}")
    player_white = PlayerFactory.create_player(player_white_name)
    white_id = id(player_white)
    print(f"✅ Created: {type(player_white).__name__} @ {white_id}")
    
    # Verify instances are different
    if black_id == white_id:
        print(f"❌ CRITICAL: Both players share the same instance!")
        return False
    
    print()
    print("─" * 80)
    print("Initial Configuration Verification")
    print("─" * 80)
    
    # Verify initial configurations
    black_cfg = player_black.bitboard_engine.config
    white_cfg = player_white.bitboard_engine.config
    
    print(f"⚫ {player_black_name}:")
    print(f"   Depth: {black_cfg.depth} (expected: 12)")
    print(f"   Strategy: {black_cfg.search_strategy} (expected: adaptive)")
    print(f"   TT: {black_cfg.use_transposition_table} (expected: True)")
    print(f"   Config ID: {id(black_cfg)}")
    
    print(f"⚪ {player_white_name}:")
    print(f"   Depth: {white_cfg.depth} (expected: 4)")
    print(f"   Strategy: {white_cfg.search_strategy} (expected: fixed_depth)")
    print(f"   TT: {white_cfg.use_transposition_table} (expected: False)")
    print(f"   Config ID: {id(white_cfg)}")
    
    # Verify configs are different
    if id(black_cfg) == id(white_cfg):
        print(f"❌ CRITICAL: Both players share the same config object!")
        return False
    
    # Store initial config IDs
    initial_black_cfg_id = id(black_cfg)
    initial_white_cfg_id = id(white_cfg)
    
    print()
    print("─" * 80)
    print("Starting Game Simulation")
    print("─" * 80)
    
    # Create game
    game = Game(8)
    
    # Track moves
    move_count = 0
    errors = []
    
    # Play up to 10 moves (enough to catch the 4th move issue)
    max_moves = 10
    
    while move_count < max_moves:
        move_count += 1
        current_turn = game.turn
        current_player = player_black if current_turn == 'B' else player_white
        current_player_name = player_black_name if current_turn == 'B' else player_white_name
        expected_depth = 12 if current_turn == 'B' else 4
        expected_strategy = 'adaptive' if current_turn == 'B' else 'fixed_depth'
        
        print()
        print(f"Move {move_count}: {current_turn} ({current_player_name})")
        print(f"   Player instance ID: {id(current_player)}")
        
        # Get available moves
        move_list = game.get_move_list()
        if not move_list:
            print("   No moves available, passing...")
            game.pass_turn()
            continue
        
        # CRITICAL: Verify configuration BEFORE move
        current_cfg = current_player.bitboard_engine.config
        current_cfg_id = id(current_cfg)
        
        # Also check self.deep and self.depth attributes
        player_depth = getattr(current_player, 'depth', None)
        player_deep = getattr(current_player, 'deep', None)
        
        print(f"   Config ID: {current_cfg_id}")
        print(f"   Config depth: {current_cfg.depth} (expected: {expected_depth})")
        print(f"   Strategy: {current_cfg.search_strategy} (expected: {expected_strategy})")
        print(f"   Player.depth: {player_depth}")
        print(f"   Player.deep: {player_deep}")
        
        # Verify config matches expected
        # Note: For adaptive strategy, depth may vary by phase, so we check the base depth
        if current_cfg.search_strategy == 'adaptive':
            # For adaptive, check that adaptive_depths are set correctly
            adaptive_depths = getattr(current_cfg, 'adaptive_depths', {})
            if current_turn == 'B':
                # DIVZERO.EXE should have adaptive depths: opening=6, midgame=12, endgame=12
                if adaptive_depths.get('midgame', 0) != 12:
                    error_msg = f"Move {move_count}: {current_player_name} has wrong adaptive midgame depth! Expected 12, got {adaptive_depths.get('midgame', 0)}"
                    print(f"   ❌ {error_msg}")
                    errors.append(error_msg)
        else:
            # For fixed_depth, depth must match exactly
            if current_cfg.depth != expected_depth:
                error_msg = f"Move {move_count}: {current_player_name} has wrong depth! Expected {expected_depth}, got {current_cfg.depth}"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
        
        if current_cfg.search_strategy != expected_strategy:
            error_msg = f"Move {move_count}: {current_player_name} has wrong strategy! Expected {expected_strategy}, got {current_cfg.search_strategy}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
        
        # CRITICAL: Verify config object hasn't changed
        if current_turn == 'B':
            if current_cfg_id != initial_black_cfg_id:
                error_msg = f"Move {move_count}: Black config object changed! Initial: {initial_black_cfg_id}, Current: {current_cfg_id}"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
        else:
            if current_cfg_id != initial_white_cfg_id:
                error_msg = f"Move {move_count}: White config object changed! Initial: {initial_white_cfg_id}, Current: {current_cfg_id}"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
        
        # CRITICAL: Verify instances haven't swapped
        if current_turn == 'B':
            if id(current_player) != black_id:
                error_msg = f"Move {move_count}: Black player instance changed! Initial: {black_id}, Current: {id(current_player)}"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
        else:
            if id(current_player) != white_id:
                error_msg = f"Move {move_count}: White player instance changed! Initial: {white_id}, Current: {id(current_player)}"
                print(f"   ❌ {error_msg}")
                errors.append(error_msg)
        
        # CRITICAL: Verify configs are still different
        if id(black_cfg) == id(white_cfg):
            error_msg = f"Move {move_count}: Configs became shared!"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
        
        # Get move from AI
        try:
            ai_move = current_player.get_move(game, move_list)
            if ai_move:
                coord = f"{chr(64+ai_move.x)}{ai_move.y}"
                print(f"   ✅ Selected move: {coord}")
                game.move(ai_move)
            else:
                print("   No move returned, passing...")
                game.pass_turn()
        except Exception as e:
            error_msg = f"Move {move_count}: Error getting move: {e}"
            print(f"   ❌ {error_msg}")
            errors.append(error_msg)
            import traceback
            traceback.print_exc()
            break
        
        # Special check at move 4
        if move_count == 4:
            print()
            print("   🔍 SPECIAL CHECK AT MOVE 4:")
            print(f"      Black instance ID: {id(player_black)}")
            print(f"      White instance ID: {id(player_white)}")
            print(f"      Black config ID: {id(player_black.bitboard_engine.config)}")
            print(f"      White config ID: {id(player_white.bitboard_engine.config)}")
            print(f"      Black depth: {player_black.bitboard_engine.config.depth}")
            print(f"      White depth: {player_white.bitboard_engine.config.depth}")
            
            if player_black.bitboard_engine.config.depth != 12:
                error_msg = "Move 4: Black lost its configuration!"
                print(f"      ❌ {error_msg}")
                errors.append(error_msg)
            
            if player_white.bitboard_engine.config.depth != 4:
                error_msg = "Move 4: White lost its configuration!"
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
        success = simulate_game_and_verify()
        sys.exit(0 if success else 1)
    except Exception as e:
        import traceback
        print(f"❌ TEST FAILED with exception:")
        print(traceback.format_exc())
        sys.exit(1)

