#!/usr/bin/env python3
"""
Test script to verify player isolation and configuration correctness.

This script creates two different AI players (DIVZERO.EXE and LIGHTNING STRIKE)
and verifies that:
1. Each player has a different instance (different ID)
2. Each player has the correct configuration (depth, strategy, TT, etc.)
3. Each player has the correct name
4. Configurations are not shared between players
"""

import os
import sys

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(
    os.path.dirname(current_dir)
)  # Go up from tests/integration to project root
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from Players.PlayerFactory import PlayerFactory


def test_player_creation():
    """Test that players are created correctly with isolated configurations."""

    print("=" * 80)
    print("🧪 TEST: Player Isolation and Configuration Correctness")
    print("=" * 80)
    print()

    # Clear registry cache first
    print("🧹 Clearing registry cache...")
    registry = PlayerFactory._get_registry()
    registry.clear_instance_cache()
    print("✅ Cache cleared")
    print()

    # Test 1: Create LIGHTNING STRIKE
    print("─" * 80)
    print("TEST 1: Creating LIGHTNING STRIKE")
    print("─" * 80)
    player1_name = "LIGHTNING STRIKE"
    print(f"Creating player: {player1_name}")

    player1 = PlayerFactory.create_player(player1_name)
    player1_id = id(player1)
    print(f"✅ Player created: {type(player1).__name__} @ {player1_id}")
    print(f"   Player.name: {player1.name}")

    # Verify player1 configuration
    if hasattr(player1, "bitboard_engine") and hasattr(player1.bitboard_engine, "config"):
        cfg1 = player1.bitboard_engine.config
        print(f"   Engine config:")
        print(f"      Depth: {cfg1.depth}")
        print(f"      Strategy: {cfg1.search_strategy}")
        print(f"      Transposition Table: {cfg1.use_transposition_table}")
        print(f"      Parallel: {cfg1.use_parallel}")
        print(f"      Aspiration: {cfg1.use_aspiration_windows}")

        # Verify LIGHTNING STRIKE config
        expected_depth = 4
        expected_strategy = "fixed_depth"
        expected_tt = False
        expected_parallel = False
        expected_aspiration = False

        errors = []
        if cfg1.depth != expected_depth:
            errors.append(f"   ❌ Depth mismatch: expected {expected_depth}, got {cfg1.depth}")
        if cfg1.search_strategy != expected_strategy:
            errors.append(
                f"   ❌ Strategy mismatch: expected {expected_strategy}, got {cfg1.search_strategy}"
            )
        if cfg1.use_transposition_table != expected_tt:
            errors.append(
                f"   ❌ TT mismatch: expected {expected_tt}, got {cfg1.use_transposition_table}"
            )
        if cfg1.use_parallel != expected_parallel:
            errors.append(
                f"   ❌ Parallel mismatch: expected {expected_parallel}, got {cfg1.use_parallel}"
            )
        if cfg1.use_aspiration_windows != expected_aspiration:
            errors.append(
                f"   ❌ Aspiration mismatch: expected {expected_aspiration}, got {cfg1.use_aspiration_windows}"
            )

        if errors:
            print("   ⚠️  CONFIGURATION ERRORS:")
            for error in errors:
                print(error)
            return False
        else:
            print("   ✅ Configuration correct!")
    else:
        print("   ❌ Cannot verify config (no bitboard_engine)")
        return False

    print()

    # Test 2: Create DIVZERO.EXE
    print("─" * 80)
    print("TEST 2: Creating DIVZERO.EXE")
    print("─" * 80)
    player2_name = "DIVZERO.EXE"
    print(f"Creating player: {player2_name}")

    # Clear cache again to ensure fresh instance
    registry.clear_instance_cache()

    player2 = PlayerFactory.create_player(player2_name)
    player2_id = id(player2)
    print(f"✅ Player created: {type(player2).__name__} @ {player2_id}")
    print(f"   Player.name: {player2.name}")

    # Verify player2 configuration
    if hasattr(player2, "bitboard_engine") and hasattr(player2.bitboard_engine, "config"):
        cfg2 = player2.bitboard_engine.config
        print(f"   Engine config:")
        print(f"      Depth: {cfg2.depth}")
        print(f"      Strategy: {cfg2.search_strategy}")
        print(f"      Transposition Table: {cfg2.use_transposition_table}")
        print(f"      Parallel: {cfg2.use_parallel}")
        print(f"      Aspiration: {cfg2.use_aspiration_windows}")

        # Verify DIVZERO.EXE config
        expected_depth = 12
        expected_strategy = "adaptive"
        expected_tt = True
        expected_parallel = True
        expected_aspiration = True

        errors = []
        if cfg2.depth != expected_depth:
            errors.append(f"   ❌ Depth mismatch: expected {expected_depth}, got {cfg2.depth}")
        if cfg2.search_strategy != expected_strategy:
            errors.append(
                f"   ❌ Strategy mismatch: expected {expected_strategy}, got {cfg2.search_strategy}"
            )
        if cfg2.use_transposition_table != expected_tt:
            errors.append(
                f"   ❌ TT mismatch: expected {expected_tt}, got {cfg2.use_transposition_table}"
            )
        if cfg2.use_parallel != expected_parallel:
            errors.append(
                f"   ❌ Parallel mismatch: expected {expected_parallel}, got {cfg2.use_parallel}"
            )
        if cfg2.use_aspiration_windows != expected_aspiration:
            errors.append(
                f"   ❌ Aspiration mismatch: expected {expected_aspiration}, got {cfg2.use_aspiration_windows}"
            )

        if errors:
            print("   ⚠️  CONFIGURATION ERRORS:")
            for error in errors:
                print(error)
            return False
        else:
            print("   ✅ Configuration correct!")
    else:
        print("   ❌ Cannot verify config (no bitboard_engine)")
        return False

    print()

    # Test 3: Verify instances are different
    print("─" * 80)
    print("TEST 3: Verify Instance Isolation")
    print("─" * 80)
    if player1_id == player2_id:
        print(f"   ❌ CRITICAL: Both players share the same instance!")
        print(f"      Player1 ID: {player1_id}")
        print(f"      Player2 ID: {player2_id}")
        return False
    else:
        print(f"   ✅ Instances are different:")
        print(f"      Player1 ID: {player1_id}")
        print(f"      Player2 ID: {player2_id}")

    # Test 4: Verify configurations are different
    print()
    print("─" * 80)
    print("TEST 4: Verify Configuration Isolation")
    print("─" * 80)
    cfg1 = player1.bitboard_engine.config
    cfg2 = player2.bitboard_engine.config

    if cfg1.depth == cfg2.depth:
        print(f"   ❌ CRITICAL: Both players have the same depth!")
        print(f"      Player1 depth: {cfg1.depth}")
        print(f"      Player2 depth: {cfg2.depth}")
        return False
    else:
        print(f"   ✅ Configurations are different:")
        print(f"      Player1 depth: {cfg1.depth}")
        print(f"      Player2 depth: {cfg2.depth}")

    if cfg1.search_strategy == cfg2.search_strategy:
        print(f"   ❌ CRITICAL: Both players have the same strategy!")
        print(f"      Player1 strategy: {cfg1.search_strategy}")
        print(f"      Player2 strategy: {cfg2.search_strategy}")
        return False
    else:
        print(f"   ✅ Strategies are different:")
        print(f"      Player1 strategy: {cfg1.search_strategy}")
        print(f"      Player2 strategy: {cfg2.search_strategy}")

    # Test 5: Verify config objects are different
    cfg1_id = id(cfg1)
    cfg2_id = id(cfg2)
    if cfg1_id == cfg2_id:
        print(f"   ❌ CRITICAL: Both players share the same config object!")
        print(f"      Config1 ID: {cfg1_id}")
        print(f"      Config2 ID: {cfg2_id}")
        return False
    else:
        print(f"   ✅ Config objects are different:")
        print(f"      Config1 ID: {cfg1_id}")
        print(f"      Config2 ID: {cfg2_id}")

    print()
    print("=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    return True


if __name__ == "__main__":
    try:
        success = test_player_creation()
        sys.exit(0 if success else 1)
    except Exception as e:
        import traceback

        print(f"❌ TEST FAILED with exception:")
        print(traceback.format_exc())
        sys.exit(1)
