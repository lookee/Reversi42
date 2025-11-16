#!/usr/bin/env python3
"""
Quick Tournament Launcher for Reversi42

Quickly run pre-configured tournaments from the ring/ directory.
"""

import os
import sys

# Add parent directory's src to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, "..", "src"))

import argparse
import subprocess

# Available tournament configurations
TOURNAMENTS = {
    "quick": {
        "file": "ring/quick_battle.json",
        "description": "⚡ Quick Battle - 4 top gladiators (fast)",
    },
    "all": {
        "file": "ring/ultimate_arena.json",
        "description": "👑 Ultimate Arena - ALL 10 gladiators",
    },
    "speed": {
        "file": "ring/speed_demons.json",
        "description": "⚡⚡⚡ Speed Demons - Lightning fast (<200ms)",
    },
    "titans": {
        "file": "ring/titans_clash.json",
        "description": "💀 Titans Clash - Top 5 strongest (ELO 1750+)",
    },
    "chaos": {
        "file": "ring/chaos_realm.json",
        "description": "👾 Chaos Realm - Unpredictable madness",
    },
    "endgame": {
        "file": "ring/endgame_masters.json",
        "description": "🔮 Endgame Masters - Strategic prophets",
    },
    "mobility": {
        "file": "ring/mobility_assassins.json",
        "description": "🎯 Mobility Assassins - Suffocation league",
    },
    "corners": {
        "file": "ring/corner_wars.json",
        "description": "👑 Corner Wars - Territorial conquest",
    },
    "zen": {"file": "ring/zen_vs_chaos.json", "description": "🧘 Zen vs Chaos - Philosophy wars"},
    "boss": {
        "file": "ring/final_boss_challenge.json",
        "description": "💀 Final Boss - Can anyone beat DIVZERO?",
    },
    "training": {
        "file": "ring/training_ground.json",
        "description": "🎓 Training Ground - Beginners arena",
    },
    "apocalypse": {
        "file": "ring/apocalypse_now.json",
        "description": "💥 Apocalypse Now - Maximum carnage",
    },
    "blitz": {
        "file": "ring/blitz_madness.json",
        "description": "🔥 Blitz Madness - Rapid fire (20 games!)",
    },
    "david": {
        "file": "ring/david_vs_goliath.json",
        "description": "⚔️ David vs Goliath - Underdogs challenge",
    },
}


def list_tournaments():
    """Display available tournaments"""
    print("\n" + "=" * 80)
    print("🏆 AVAILABLE TOURNAMENTS")
    print("=" * 80 + "\n")

    for key, info in sorted(TOURNAMENTS.items()):
        print(f"  {key:12} - {info['description']}")

    print("\n" + "=" * 80)
    print("\nUsage: python quick_tournament.py <tournament_name>")
    print("Example: python quick_tournament.py quick\n")


def run_tournament(tournament_key):
    """Run specified tournament"""
    if tournament_key not in TOURNAMENTS:
        print(f"\n❌ ERROR: Tournament '{tournament_key}' not found!")
        print("\nAvailable tournaments:")
        list_tournaments()
        return 1

    config_file = os.path.join(script_dir, TOURNAMENTS[tournament_key]["file"])

    if not os.path.exists(config_file):
        print(f"\n❌ ERROR: Configuration file not found: {config_file}")
        return 1

    print("\n" + "=" * 80)
    print(f"🏆 LAUNCHING: {TOURNAMENTS[tournament_key]['description']}")
    print("=" * 80 + "\n")
    print(f"Configuration: {config_file}\n")

    # Run tournament
    tournament_script = os.path.join(script_dir, "tournament.py")
    cmd = [sys.executable, tournament_script, "--config", config_file]

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        print("\n\n⚠️  Tournament interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ ERROR running tournament: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Quick Tournament Launcher for Reversi42",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quick_tournament.py quick       # Quick 4-player battle
  python quick_tournament.py all         # All 10 gladiators
  python quick_tournament.py speed       # Ultra-fast tournament
  python quick_tournament.py boss        # Final boss challenge
  python quick_tournament.py --list      # Show all tournaments
        """,
    )

    parser.add_argument("tournament", nargs="?", help="Tournament to run (use --list to see all)")
    parser.add_argument("--list", "-l", action="store_true", help="List all available tournaments")

    args = parser.parse_args()

    # List tournaments if requested
    if args.list or not args.tournament:
        list_tournaments()
        return 0

    # Run tournament
    return run_tournament(args.tournament)


if __name__ == "__main__":
    sys.exit(main())
