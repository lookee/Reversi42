"""
Game Configuration Loader

Loads and manages game configuration from YAML files.
Provides default game setup including player selection.

Architecture:
- YAML-based configuration
- Default configuration with overrides
- Validation and error handling
- Integration with Player Registry
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class PlayerConfig:
    """Configuration for a single player."""
    player_type: str  # "human" or "ai"
    name: str
    ai_player: Optional[str] = None
    symbol: str = "⚫"
    input_method: str = "console"


@dataclass
class GameConfig:
    """Complete game configuration."""
    title: str
    auto_start: bool
    board_size: int
    black_player: PlayerConfig
    white_player: PlayerConfig
    show_legal_moves: bool
    show_hints: bool
    show_ai_thinking: bool
    show_ai_evaluation: bool
    show_ai_stats: bool
    show_opening_book: bool
    think_delay_ms: int
    board_style: str
    show_coordinates: bool
    show_history: bool
    show_score: bool
    clear_screen: bool
    debug_mode: bool
    
    @property
    def is_human_vs_ai(self) -> bool:
        """Check if game is human vs AI."""
        return (self.black_player.player_type == "human" and 
                self.white_player.player_type == "ai") or \
               (self.black_player.player_type == "ai" and 
                self.white_player.player_type == "human")
    
    @property
    def is_ai_vs_ai(self) -> bool:
        """Check if game is AI vs AI."""
        return (self.black_player.player_type == "ai" and 
                self.white_player.player_type == "ai")
    
    @property
    def is_human_vs_human(self) -> bool:
        """Check if game is human vs human."""
        return (self.black_player.player_type == "human" and 
                self.white_player.player_type == "human")


class GameConfigLoader:
    """
    Loads game configuration from YAML file.
    
    Follows Single Responsibility Principle: manages game config only.
    """
    
    DEFAULT_CONFIG_PATH = "config/game.yaml"
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize config loader.
        
        Args:
            project_root: Project root directory (auto-detected if None)
        """
        self.project_root = project_root or self._find_project_root()
        self._config: Optional[GameConfig] = None
    
    def load(self, config_path: Optional[str] = None) -> GameConfig:
        """
        Load game configuration.
        
        Args:
            config_path: Path to config file (uses default if None)
            
        Returns:
            GameConfig instance
            
        Raises:
            FileNotFoundError: If config file not found
            ValueError: If configuration is invalid
        """
        # Determine config file path
        if config_path:
            path = Path(config_path)
        else:
            path = self.project_root / self.DEFAULT_CONFIG_PATH
        
        logger.info(f"📄 Loading game configuration from: {path}")
        
        # Load YAML
        if not path.exists():
            logger.warning(f"⚠️  Config file not found: {path}, using defaults")
            return self._get_default_config()
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"❌ Failed to load config: {e}")
            logger.info("📄 Using default configuration")
            return self._get_default_config()
        
        # Parse configuration
        try:
            game_config = self._parse_config(config_dict)
            self._config = game_config
            self._log_config(game_config)
            return game_config
        except Exception as e:
            logger.error(f"❌ Invalid configuration: {e}")
            logger.info("📄 Using default configuration")
            return self._get_default_config()
    
    def _parse_config(self, config_dict: Dict[str, Any]) -> GameConfig:
        """Parse configuration dictionary into GameConfig."""
        # Extract sections with defaults
        game_settings = config_dict.get('game', {})
        players_config = config_dict.get('players', {})
        display_config = config_dict.get('display', {})
        ai_behavior = config_dict.get('ai_behavior', {})
        rules_config = config_dict.get('rules', {})
        advanced_config = config_dict.get('advanced', {})
        
        # Parse player configurations
        black_config = players_config.get('black', {})
        white_config = players_config.get('white', {})
        
        black_player = PlayerConfig(
            player_type=black_config.get('type', 'human'),
            name=black_config.get('name', 'Black Player'),
            ai_player=black_config.get('ai_player'),
            symbol=black_config.get('symbol', '⚫'),
            input_method=black_config.get('input_method', 'console')
        )
        
        white_player = PlayerConfig(
            player_type=white_config.get('type', 'ai'),
            name=white_config.get('name', 'White Player'),
            ai_player=white_config.get('ai_player', 'LIGHTNING STRIKE'),
            symbol=white_config.get('symbol', '⚪'),
            input_method=white_config.get('input_method', 'console')
        )
        
        # Build complete GameConfig
        return GameConfig(
            # Game settings
            title=game_settings.get('title', 'Reversi42'),
            auto_start=game_settings.get('auto_start', True),
            board_size=game_settings.get('board_size', 8),
            
            # Players
            black_player=black_player,
            white_player=white_player,
            
            # Rules
            show_legal_moves=rules_config.get('show_legal_moves', True),
            show_hints=rules_config.get('show_hints', False),
            
            # AI Behavior
            show_ai_thinking=ai_behavior.get('show_thinking', False),
            show_ai_evaluation=ai_behavior.get('show_evaluation', False),
            show_ai_stats=ai_behavior.get('show_statistics', True),
            show_opening_book=ai_behavior.get('show_opening_book', False),
            think_delay_ms=ai_behavior.get('think_delay_ms', 500),
            
            # Display
            board_style=display_config.get('board_style', 'unicode'),
            show_coordinates=display_config.get('show_coordinates', True),
            show_history=display_config.get('show_history', True),
            show_score=display_config.get('show_score', True),
            clear_screen=display_config.get('clear_screen', False),
            
            # Advanced
            debug_mode=advanced_config.get('debug_mode', False)
        )
    
    def _get_default_config(self) -> GameConfig:
        """Get default game configuration (fallback)."""
        return GameConfig(
            # Game settings
            title="Reversi42 - Default Game",
            auto_start=True,
            board_size=8,
            
            # Players
            black_player=PlayerConfig(
                player_type="human",
                name="Human Player",
                symbol="⚫"
            ),
            white_player=PlayerConfig(
                player_type="ai",
                name="Lightning Strike",
                ai_player="LIGHTNING STRIKE",
                symbol="⚪"
            ),
            
            # Rules
            show_legal_moves=True,
            show_hints=False,
            
            # AI Behavior
            show_ai_thinking=False,
            show_ai_evaluation=False,
            show_ai_stats=True,
            show_opening_book=False,
            think_delay_ms=500,
            
            # Display
            board_style="unicode",
            show_coordinates=True,
            show_history=True,
            show_score=True,
            clear_screen=False,
            
            # Advanced
            debug_mode=False
        )
    
    def _log_config(self, config: GameConfig):
        """Log configuration details."""
        logger.info("\n" + "=" * 80)
        logger.info(f"🎮 {config.title}")
        logger.info("=" * 80)
        
        # Players
        logger.info(f"\n👥 Players:")
        logger.info(f"   ⚫ Black: {config.black_player.name} ({config.black_player.player_type.upper()})")
        if config.black_player.ai_player:
            logger.info(f"      AI: {config.black_player.ai_player}")
        
        logger.info(f"   ⚪ White: {config.white_player.name} ({config.white_player.player_type.upper()})")
        if config.white_player.ai_player:
            logger.info(f"      AI: {config.white_player.ai_player}")
        
        # Settings
        logger.info(f"\n⚙️  Settings:")
        logger.info(f"   • Auto-start: {config.auto_start}")
        logger.info(f"   • Board size: {config.board_size}×{config.board_size}")
        logger.info(f"   • Board style: {config.board_style}")
        logger.info(f"   • Show legal moves: {config.show_legal_moves}")
        logger.info(f"   • Show coordinates: {config.show_coordinates}")
        
        # AI Behavior (if AI player present)
        if config.is_human_vs_ai or config.is_ai_vs_ai:
            logger.info(f"\n🤖 AI Behavior:")
            logger.info(f"   • Think delay: {config.think_delay_ms}ms")
            logger.info(f"   • Show thinking: {config.show_ai_thinking}")
            logger.info(f"   • Show statistics: {config.show_ai_stats}")
            logger.info(f"   • Show evaluation: {config.show_ai_evaluation}")
        
        logger.info("=" * 80 + "\n")
    
    def _find_project_root(self) -> Path:
        """Find project root directory."""
        markers = ['pyproject.toml', 'setup.py', 'README.md', '.git']
        current = Path(__file__).resolve().parent
        
        for parent in [current] + list(current.parents):
            if any((parent / marker).exists() for marker in markers):
                return parent
        
        return Path.cwd()
    
    def create_players(self, config: Optional[GameConfig] = None) -> Tuple[Any, Any]:
        """
        Create player instances from configuration.
        
        Args:
            config: GameConfig instance (uses loaded config if None)
            
        Returns:
            Tuple of (black_player, white_player)
        """
        if config is None:
            config = self._config
            if config is None:
                config = self.load()
        
        from Players.config import PlayerRegistry
        from Players.PlayerHuman import PlayerHuman
        from ui.implementations.headless.input_providers import MockInputProvider
        from Reversi.Game import Move
        
        registry = PlayerRegistry()
        
        # Create black player
        if config.black_player.player_type == "human":
            logger.info(f"🎮 Creating human player: {config.black_player.name}")
            # For now, using mock input provider
            # TODO: Replace with actual input based on input_method
            input_provider = MockInputProvider([Move(3, 3)], auto_exit=False)
            black_player = PlayerHuman(input_provider, name=config.black_player.name)
        else:
            logger.info(f"🤖 Creating AI player: {config.black_player.ai_player}")
            black_player = registry.create_player(config.black_player.ai_player)
        
        # Create white player
        if config.white_player.player_type == "human":
            logger.info(f"🎮 Creating human player: {config.white_player.name}")
            input_provider = MockInputProvider([Move(3, 3)], auto_exit=False)
            white_player = PlayerHuman(input_provider, name=config.white_player.name)
        else:
            logger.info(f"🤖 Creating AI player: {config.white_player.ai_player}")
            white_player = registry.create_player(config.white_player.ai_player)
        
        logger.info(f"✅ Players created successfully\n")
        
        return black_player, white_player


# Convenience function
def load_game_config(config_path: Optional[str] = None) -> GameConfig:
    """
    Load game configuration.
    
    Args:
        config_path: Path to config file (uses default if None)
        
    Returns:
        GameConfig instance
    """
    loader = GameConfigLoader()
    return loader.load(config_path)


def create_default_game_players() -> Tuple[Any, Any]:
    """
    Create players for default game configuration.
    
    Returns:
        Tuple of (black_player, white_player)
    """
    loader = GameConfigLoader()
    config = loader.load()
    return loader.create_players(config)

