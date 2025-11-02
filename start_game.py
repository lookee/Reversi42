#!/usr/bin/env python3
"""
Reversi42 Game Launcher

Starts a game using the default configuration from config/game.yaml.

This script:
1. Loads game configuration (players, rules, display)
2. Initializes the Player Registry
3. Creates configured player instances  
4. Starts the game automatically

Usage:
    python start_game.py                    # Use default config
    python start_game.py --config custom.yaml  # Use custom config
    python start_game.py --help             # Show help
"""

import sys
import argparse
import logging
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Reversi42 - AI-powered Reversi/Othello game',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_game.py                        Start with default configuration
  python start_game.py --config custom.yaml  Use custom game configuration
  python start_game.py --list-players        List all available AI players
  python start_game.py --verbose             Show detailed logging

Configuration:
  Edit config/game.yaml to customize:
    - Player selection (Human, AI)
    - AI difficulty level
    - Display settings
    - Game rules
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        metavar='FILE',
        help='Path to game configuration file (default: config/game.yaml)'
    )
    
    parser.add_argument(
        '--list-players',
        action='store_true',
        help='List all available AI players and exit'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    return parser.parse_args()


def list_available_players():
    """List all available AI players."""
    from Players.config import PlayerRegistry
    
    logger.info("\n" + "=" * 80)
    logger.info("🎮 Available AI Players")
    logger.info("=" * 80 + "\n")
    
    try:
        registry = PlayerRegistry()
        registry.print_summary()
        return 0
    except Exception as e:
        logger.error(f"❌ Failed to load players: {e}")
        return 1


def start_game(config_path: str = None):
    """
    Start the game with configuration.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Exit code (0 = success, 1 = error)
    """
    try:
        # Print header
        print("\n" + "=" * 80)
        print("🎮 REVERSI42 - AI-Powered Reversi/Othello")
        print("=" * 80 + "\n")
        
        # Load game configuration
        logger.info("📋 Loading game configuration...")
        from core.game_config import GameConfigLoader
        
        config_loader = GameConfigLoader()
        game_config = config_loader.load(config_path)
        
        # Create players
        logger.info("🎭 Creating players...")
        black_player, white_player = config_loader.create_players(game_config)
        
        # Start game
        logger.info("🎲 Starting game...")
        logger.info("\n" + "=" * 80)
        logger.info(f"⚫ Black: {black_player.get_name()}")
        logger.info(f"⚪ White: {white_player.get_name()}")
        logger.info("=" * 80 + "\n")
        
        # TODO: Start actual game loop
        # For now, just show that players are ready
        logger.info("✅ Game initialized successfully!")
        logger.info("\n⚠️  Note: Full game integration pending")
        logger.info("   Players are configured and ready:")
        logger.info(f"   - Black: {black_player.get_name()} ({type(black_player).__name__})")
        logger.info(f"   - White: {white_player.get_name()} ({type(white_player).__name__})")
        
        print("\n" + "=" * 80)
        print("✨ GAME READY")
        print("=" * 80)
        print("\nConfiguration Summary:")
        print(f"  • Black Player: {game_config.black_player.name} ({game_config.black_player.player_type})")
        print(f"  • White Player: {game_config.white_player.name} ({game_config.white_player.player_type})")
        if game_config.white_player.ai_player:
            print(f"  • AI Opponent: {game_config.white_player.ai_player}")
        print(f"  • Board Size: {game_config.board_size}x{game_config.board_size}")
        print(f"  • Show Legal Moves: {game_config.show_legal_moves}")
        print("\nTo modify game settings, edit: config/game.yaml")
        print("=" * 80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Game interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"\n❌ Game failed to start: {e}", exc_info=True)
        return 1


def main():
    """Main entry point."""
    args = parse_args()
    
    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    
    # Handle list-players command
    if args.list_players:
        return list_available_players()
    
    # Start game
    return start_game(args.config)


if __name__ == "__main__":
    sys.exit(main())

