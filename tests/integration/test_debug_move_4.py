#!/usr/bin/env python3
"""
Test di debug per identificare il problema alla quarta mossa.
Verifica ogni dettaglio possibile per capire cosa va storto.
"""

import os
import sys

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from Players.PlayerFactory import PlayerFactory
from Reversi.Game import Game, Move


def deep_inspect_player(player, label):
    """Ispeziona profondamente un player"""
    print(f"\n{'='*80}")
    print(f"DEEP INSPECTION: {label}")
    print(f"{'='*80}")
    print(f"Player instance ID: {id(player)}")
    print(f"Player type: {type(player).__name__}")
    print(f"Player name: {getattr(player, 'name', 'NO NAME')}")

    if hasattr(player, "bitboard_engine"):
        engine = player.bitboard_engine
        print(f"Engine ID: {id(engine)}")

        if hasattr(engine, "config"):
            cfg = engine.config
            print(f"Config ID: {id(cfg)}")
            print(f"Config depth: {cfg.depth}")
            print(f"Config strategy: {cfg.search_strategy}")
            print(f"Config TT: {cfg.use_transposition_table}")
            print(f"Config parallel: {cfg.use_parallel}")
            print(f"Config aspiration: {cfg.use_aspiration_windows}")

            # Check adaptive depths if adaptive
            if cfg.search_strategy == "adaptive":
                adaptive_depths = getattr(cfg, "adaptive_depths", {})
                print(f"Adaptive depths: {adaptive_depths}")

        # Check search strategy
        if hasattr(engine, "search_strategy"):
            strategy = engine.search_strategy
            print(f"Search strategy ID: {id(strategy)}")
            print(f"Search strategy type: {type(strategy).__name__}")

            # If adaptive, check depth config
            if hasattr(strategy, "depth_config"):
                print(f"Strategy depth_config: {strategy.depth_config}")

    # Check player attributes
    print(f"Player.depth: {getattr(player, 'depth', 'NO ATTR')}")
    print(f"Player.deep: {getattr(player, 'deep', 'NO ATTR')}")

    # Check opening book
    if hasattr(player, "opening_book"):
        book = player.opening_book
        print(f"Opening book ID: {id(book)}")
        print(f"Opening book type: {type(book).__name__}")


def test_move_4_debug():
    """Test approfondito per la mossa 4"""

    print("=" * 80)
    print("🔍 DEBUG TEST: Move 4 Problem Investigation")
    print("=" * 80)

    # Clear cache
    registry = PlayerFactory._get_registry()
    registry.clear_instance_cache()

    # Create players
    print("\n" + "─" * 80)
    print("STEP 1: Creating Players")
    print("─" * 80)

    white = PlayerFactory.create_player("LIGHTNING STRIKE")
    black = PlayerFactory.create_player("DIVZERO.EXE")

    # Initial inspection
    deep_inspect_player(white, "WHITE (LIGHTNING STRIKE) - INITIAL")
    deep_inspect_player(black, "BLACK (DIVZERO.EXE) - INITIAL")

    # Store initial config IDs
    white_cfg_id_initial = id(white.bitboard_engine.config)
    black_cfg_id_initial = id(black.bitboard_engine.config)
    white_id_initial = id(white)
    black_id_initial = id(black)

    print(f"\n📌 INITIAL STATE:")
    print(f"   White instance ID: {white_id_initial}")
    print(f"   Black instance ID: {black_id_initial}")
    print(f"   White config ID: {white_cfg_id_initial}")
    print(f"   Black config ID: {black_cfg_id_initial}")

    # Create game
    game = Game(8)

    # Play moves
    print("\n" + "─" * 80)
    print("STEP 2: Playing Moves")
    print("─" * 80)

    for move_num in range(1, 5):
        turn = game.turn
        player = white if turn == "W" else black
        player_name = "LIGHTNING STRIKE" if turn == "W" else "DIVZERO.EXE"

        print(f"\n{'='*80}")
        print(f"MOVE {move_num}: {turn} ({player_name})")
        print(f"{'='*80}")

        # CRITICAL: Check if instances changed
        current_white_id = id(white)
        current_black_id = id(black)
        current_white_cfg_id = id(white.bitboard_engine.config)
        current_black_cfg_id = id(black.bitboard_engine.config)

        print(f"\n🔍 INSTANCE CHECK:")
        print(
            f"   White instance: {current_white_id} (initial: {white_id_initial}) {'✅' if current_white_id == white_id_initial else '❌ CHANGED!'}"
        )
        print(
            f"   Black instance: {current_black_id} (initial: {black_id_initial}) {'✅' if current_black_id == black_id_initial else '❌ CHANGED!'}"
        )
        print(
            f"   White config: {current_white_cfg_id} (initial: {white_cfg_id_initial}) {'✅' if current_white_cfg_id == white_cfg_id_initial else '❌ CHANGED!'}"
        )
        print(
            f"   Black config: {current_black_cfg_id} (initial: {black_cfg_id_initial}) {'✅' if current_black_cfg_id == black_cfg_id_initial else '❌ CHANGED!'}"
        )

        # Check configurations
        white_cfg = white.bitboard_engine.config
        black_cfg = black.bitboard_engine.config

        print(f"\n🔍 CONFIGURATION CHECK:")
        print(
            f"   White depth: {white_cfg.depth} (expected: 4) {'✅' if white_cfg.depth == 4 else '❌ WRONG!'}"
        )
        print(
            f"   White strategy: {white_cfg.search_strategy} (expected: fixed_depth) {'✅' if white_cfg.search_strategy == 'fixed_depth' else '❌ WRONG!'}"
        )
        print(
            f"   Black depth: {black_cfg.depth} (expected: 12) {'✅' if black_cfg.depth == 12 else '❌ WRONG!'}"
        )
        print(
            f"   Black strategy: {black_cfg.search_strategy} (expected: adaptive) {'✅' if black_cfg.search_strategy == 'adaptive' else '❌ WRONG!'}"
        )

        # Check if configs are shared
        if id(white_cfg) == id(black_cfg):
            print(f"\n❌ CRITICAL: Configs are SHARED!")
        else:
            print(f"\n✅ Configs are separate")

        # Deep inspection at move 4
        if move_num == 4:
            print(f"\n{'='*80}")
            print(f"🔍 DEEP INSPECTION AT MOVE 4")
            print(f"{'='*80}")
            deep_inspect_player(white, "WHITE AT MOVE 4")
            deep_inspect_player(black, "BLACK AT MOVE 4")

        # Get move
        moves = game.get_move_list()
        if not moves:
            print("No moves available")
            break

        # Get move from player (suppress output)
        import contextlib
        import io

        f = io.StringIO()
        try:
            with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                ai_move = player.get_move(game, moves)
            if ai_move:
                coord = f"{chr(64+ai_move.x)}{ai_move.y}"
                print(f"\n✅ Move selected: {coord}")
                game.move(ai_move)
            else:
                print("No move returned")
                game.pass_turn()
        except Exception as e:
            print(f"\n❌ Error getting move: {e}")
            import traceback

            traceback.print_exc()
            break

        # Check again AFTER move
        print(f"\n🔍 POST-MOVE CHECK:")
        white_cfg_after = white.bitboard_engine.config
        black_cfg_after = black.bitboard_engine.config
        print(f"   White config ID after: {id(white_cfg_after)}")
        print(f"   Black config ID after: {id(black_cfg_after)}")
        print(f"   White depth after: {white_cfg_after.depth}")
        print(f"   Black depth after: {black_cfg_after.depth}")

        if id(white_cfg_after) != white_cfg_id_initial:
            print(f"   ⚠️  White config ID changed!")
        if id(black_cfg_after) != black_cfg_id_initial:
            print(f"   ⚠️  Black config ID changed!")
        if white_cfg_after.depth != 4:
            print(f"   ❌ White depth changed from 4 to {white_cfg_after.depth}!")
        if black_cfg_after.depth != 12:
            print(f"   ❌ Black depth changed from 12 to {black_cfg_after.depth}!")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_move_4_debug()
