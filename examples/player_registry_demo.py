#!/usr/bin/env python3
"""
AI Player Registry Demo

Demonstrates the elegant, centralized player management system.

This script shows how to:
1. Initialize the player registry
2. Discover and load all players automatically
3. List available players
4. Create player instances
5. Use players in games

Architecture showcased:
- Auto-discovery from config/players/enabled/
- Centralized registry pattern
- Factory pattern for player creation
- Comprehensive logging
"""

import logging
import sys
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logger = logging.getLogger(__name__)


def main():
    """Demonstrate the player registry system."""

    print("\n" + "=" * 80)
    print("🎮 Reversi42 AI Player Registry Demo")
    print("=" * 80 + "\n")

    # ========================================================================
    # 1. Initialize Registry (Auto-discovers all players)
    # ========================================================================
    print("Step 1: Initialize Player Registry")
    print("-" * 80)

    from Players.config import PlayerRegistry

    # Create registry (auto-discovers players on init)
    registry = PlayerRegistry(auto_discover=True)

    # ========================================================================
    # 2. List Available Players
    # ========================================================================
    print("\n\nStep 2: List Available Players")
    print("-" * 80)

    players = registry.list_players()
    print(f"\nFound {len(players)} player(s):")
    for i, name in enumerate(players, 1):
        info = registry.get_player_info(name)
        metadata = info["metadata"]
        icon = metadata.get("icon", "🤖")
        elo = metadata.get("estimated_elo", "???")
        category = metadata.get("category", "unknown")
        print(f"  {i:2d}. {icon} {name:<25} ELO: {elo:<4} ({category})")

    # ========================================================================
    # 3. Get Players by Category
    # ========================================================================
    print("\n\nStep 3: List Players by Category")
    print("-" * 80)

    categories = registry.get_categories()
    for category in categories:
        category_players = registry.list_players(category=category)
        print(f"\n{category.upper()}: {len(category_players)} player(s)")
        for name in category_players:
            info = registry.get_player_info(name)
            icon = info["metadata"].get("icon", "🤖")
            print(f"  • {icon} {name}")

    # ========================================================================
    # 4. Get Players by ELO Range
    # ========================================================================
    print("\n\nStep 4: Get Players by ELO Range")
    print("-" * 80)

    # Beginner players (ELO < 1400)
    beginners = registry.get_by_elo_range(0, 1399)
    print(f"\nBeginner players (ELO 1000-1399): {len(beginners)}")
    for name in beginners:
        info = registry.get_player_info(name)
        elo = info["metadata"].get("estimated_elo", "???")
        print(f"  • {name}: {elo}")

    # Champion players (ELO >= 1800)
    champions = registry.get_by_elo_range(1800, 3000)
    print(f"\nChampion players (ELO 1800+): {len(champions)}")
    for name in champions:
        info = registry.get_player_info(name)
        elo = info["metadata"].get("estimated_elo", "???")
        print(f"  • {name}: {elo}")

    # ========================================================================
    # 5. Create Player Instances
    # ========================================================================
    print("\n\nStep 5: Create Player Instances")
    print("-" * 80)

    if players:
        # Create first two players for a demo game
        player1_name = players[0]
        player2_name = players[1] if len(players) > 1 else players[0]

        print(f"\nCreating player instances:")
        print(f"  Player 1: {player1_name}")
        player1 = registry.create_player(player1_name)
        print(f"    ✅ Created: {player1.name}")

        print(f"  Player 2: {player2_name}")
        player2 = registry.create_player(player2_name)
        print(f"    ✅ Created: {player2.name}")

        print(f"\n  Both players ready for game!")

    # ========================================================================
    # 6. Registry Statistics
    # ========================================================================
    print("\n\nStep 6: Registry Statistics")
    print("-" * 80)

    stats = registry.get_stats()
    print(f"\nRegistry Statistics:")
    print(f"  • Total players loaded: {stats['total_players']}")
    print(f"  • Cached instances: {stats['cached_instances']}")
    print(f"  • Categories: {', '.join(stats['categories'])}")

    factory_stats = stats["factory_stats"]
    print(f"\nFactory Statistics:")
    print(f"  • Total created: {factory_stats['total_created']}")
    print(f"  • Failed: {factory_stats['failed']}")
    if factory_stats["by_category"]:
        print(f"  • By category:")
        for cat, count in factory_stats["by_category"].items():
            print(f"      {cat}: {count}")

    # ========================================================================
    # 7. Print Summary
    # ========================================================================
    print("\n\nStep 7: Complete Player Summary")
    print("-" * 80)

    registry.print_summary()

    # ========================================================================
    # Done
    # ========================================================================
    print("\n" + "=" * 80)
    print("✅ Demo completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Demo failed: {e}", exc_info=True)
        sys.exit(1)
