"""
Player Registry

Central registry for managing all AI players.
Implements the Registry pattern and Facade pattern for simplified access.

Architecture:
- Orchestrates discovery, loading, validation, and creation
- Provides unified API for player management
- Comprehensive logging and error handling
- Singleton pattern for global access
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from .discovery import PlayerDiscovery, PlayerConfigFile
from .loader import ConfigLoader
from .factory import PlayerFactory
from .validator import ConfigValidator
from .exceptions import PlayerNotFoundError


logger = logging.getLogger(__name__)


class PlayerRegistry:
    """
    Central registry for all AI players.
    
    Follows the Facade pattern: provides a simple interface to complex subsystem.
    Implements the Registry pattern for centralized player management.
    
    Thread-safe singleton pattern for global access.
    """
    
    _instance: Optional['PlayerRegistry'] = None
    _initialized: bool = False
    
    def __new__(cls, *args, **kwargs):
        """Singleton implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, 
                 config_dir: Optional[str] = None,
                 auto_discover: bool = True,
                 strict_validation: bool = False):
        """
        Initialize the player registry.
        
        Args:
            config_dir: Configuration directory (default: config/players/enabled)
            auto_discover: Automatically discover players on init
            strict_validation: Treat warnings as errors
        
        Note:
            Only initialized once (singleton pattern)
        """
        # Prevent re-initialization
        if PlayerRegistry._initialized:
            logger.debug("PlayerRegistry already initialized (singleton)")
            return
        
        logger.info("=" * 80)
        logger.info("🎮 Initializing Reversi42 AI Player Registry")
        logger.info("=" * 80)
        
        # Initialize components (Dependency Injection)
        self.discovery = PlayerDiscovery(config_dir=config_dir)
        self.validator = ConfigValidator(strict=strict_validation)
        self.loader = ConfigLoader(validator=self.validator)
        self.factory = PlayerFactory()
        
        # Internal state
        self._players: Dict[str, Dict[str, Any]] = {}  # name -> player_info
        self._instances: Dict[str, Any] = {}  # name -> player_instance
        
        # Auto-discover if requested
        if auto_discover:
            self.discover_and_load_all()
        
        PlayerRegistry._initialized = True
        
        logger.info("✅ Player Registry initialized successfully")
        logger.info("=" * 80)
    
    def discover_and_load_all(self) -> int:
        """
        Discover and load all available players.
        
        Returns:
            Number of successfully loaded players
        """
        logger.info("\n📂 Discovering AI players...")
        
        try:
            # Discover configuration files
            config_files = self.discovery.discover()
            
            if not config_files:
                logger.warning("⚠️  No player configurations found!")
                return 0
            
            # Load and validate each configuration
            loaded_count = 0
            for config_file in config_files:
                try:
                    if self._load_player_config(config_file):
                        loaded_count += 1
                except Exception as e:
                    logger.error(f"❌ Failed to load {config_file.name}: {e}")
            
            # Print summary
            self._print_load_summary(loaded_count, len(config_files))
            
            return loaded_count
            
        except Exception as e:
            logger.error(f"❌ Discovery failed: {e}")
            return 0
    
    def _load_player_config(self, config_file: PlayerConfigFile) -> bool:
        """
        Load a single player configuration.
        
        Args:
            config_file: PlayerConfigFile instance
            
        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            # Load configuration
            config = self.loader.load(config_file.path, validate=True)
            
            # Extract player info
            metadata = config.get('metadata', {})
            player_name = metadata.get('name', config_file.name)
            
            # Store player info (include directory category from discovery)
            self._players[player_name] = {
                'config': config,
                'config_file': config_file,
                'metadata': metadata,
                'directory_category': config_file.category,  # NEW: Directory tag (e.g., "gladiators")
                'loaded_at': self._get_timestamp()
            }
            
            # Log success
            category = metadata.get('category', 'unknown')
            elo = metadata.get('estimated_elo', '???')
            icon = metadata.get('icon', '🤖')
            
            logger.info(f"  ✅ {icon} {player_name:<20} (ELO: {elo}, Category: {category})")
            
            return True
            
        except Exception as e:
            logger.error(f"  ❌ {config_file.name}: {type(e).__name__}: {str(e)}")
            return False
    
    def _print_load_summary(self, loaded: int, total: int):
        """Print loading summary."""
        logger.info("\n" + "=" * 80)
        logger.info(f"📊 Loading Summary:")
        logger.info(f"  • Total configurations found: {total}")
        logger.info(f"  • Successfully loaded: {loaded}")
        logger.info(f"  • Failed to load: {total - loaded}")
        
        if loaded > 0:
            # Group by category
            by_category: Dict[str, int] = {}
            for player_info in self._players.values():
                category = player_info['metadata'].get('category', 'unknown')
                by_category[category] = by_category.get(category, 0) + 1
            
            if by_category:
                logger.info(f"\n  Players by category:")
                for category, count in sorted(by_category.items()):
                    logger.info(f"    • {category.capitalize()}: {count}")
        
        logger.info("=" * 80 + "\n")
    
    def list_players(self, category: Optional[str] = None) -> List[str]:
        """
        List all available player names.
        
        Args:
            category: Filter by category (None = all)
            
        Returns:
            List of player names
        """
        if category is None:
            return sorted(self._players.keys())
        
        return sorted([
            name for name, info in self._players.items()
            if info['metadata'].get('category') == category
        ])
    
    def get_player_info(self, player_name: str) -> Dict[str, Any]:
        """
        Get information about a player.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Player information dictionary
            
        Raises:
            PlayerNotFoundError: If player not found
        """
        if player_name not in self._players:
            raise PlayerNotFoundError(player_name, self.list_players())
        
        return self._players[player_name].copy()
    
    def create_player(self, player_name: str, cached: bool = True) -> Any:
        """
        Create a player instance.
        
        Args:
            player_name: Name of the player to create
            cached: Use cached instance if available
            
        Returns:
            Player instance
            
        Raises:
            PlayerNotFoundError: If player not found
        """
        # Check if player exists
        if player_name not in self._players:
            raise PlayerNotFoundError(player_name, self.list_players())
        
        # Log cache status
        logger.info(f"")
        logger.info(f"╔═══════════════════════════════════════════════════════════╗")
        logger.info(f"║ 🎮 PlayerRegistry.create_player                          ║")
        logger.info(f"╠═══════════════════════════════════════════════════════════╣")
        logger.info(f"   REQUESTED Player Name: {player_name}")
        logger.info(f"   Cached parameter: {cached}")
        logger.info(f"   Instance already in cache: {player_name in self._instances}")
        if player_name in self._instances:
            logger.info(f"   ⚠️  CACHED INSTANCE ID: {id(self._instances[player_name])}")
        logger.info(f"╚═══════════════════════════════════════════════════════════╝")
        logger.info(f"")
        
        # Return cached instance if available and requested
        if cached and player_name in self._instances:
            logger.warning(f"⚠️  RETURNING CACHED INSTANCE of {player_name} @ {id(self._instances[player_name])}")
            logger.warning(f"   THIS MAY CAUSE ISSUES WITH MULTIPLE AI PLAYERS!")
            return self._instances[player_name]
        
        # Create new instance
        player_info = self._players[player_name]
        config = player_info['config']
        config_file = player_info['config_file']
        
        logger.info(f"")
        logger.info(f"🏭 Creating NEW instance (cached={cached})")
        logger.info(f"   Config for: {player_name}")
        logger.info(f"   Config file path: {config_file.path}")
        logger.info(f"   Config metadata.name: {config.get('metadata', {}).get('name', 'UNKNOWN')}")
        logger.info(f"")
        
        player = self.factory.create_player(config, config_file.path)
        
        # VALIDATION: Verify the created player has the correct name
        # This catches bugs where wrong config is loaded
        if hasattr(player, 'name'):
            player_display_name = player.name
        elif hasattr(player, 'bitboard_engine'):
            # Try to get name from config metadata
            try:
                player_info = self.get_player_info(player_name)
                player_display_name = player_info['metadata'].get('name', 'UNKNOWN')
            except:
                player_display_name = 'UNKNOWN'
        else:
            player_display_name = 'UNKNOWN'
        
        logger.info(f"   ✅ Player instance created:")
        logger.info(f"      Requested name: {player_name}")
        logger.info(f"      Player name: {player_display_name}")
        logger.info(f"      Instance ID: {id(player)}")
        
        if player_display_name != player_name and player_display_name != 'UNKNOWN':
            logger.error(f"   ❌ CRITICAL: Player name mismatch in instance!")
            logger.error(f"      Expected: {player_name}")
            logger.error(f"      Got: {player_display_name}")
            logger.error(f"      This indicates wrong config was loaded!")
        
        # NEVER cache instances for game sessions (always create fresh)
        # Cache only for non-game uses (like API lookups)
        if cached:
            logger.info(f"   💾 Caching instance @ {id(player)} (WARNING: may cause issues in multi-player games)")
            self._instances[player_name] = player
        else:
            logger.info(f"   🚫 NOT caching instance (cached=False) - FRESH INSTANCE CREATED")
        
        return player
    
    def get_categories(self) -> List[str]:
        """
        Get all available player categories.
        
        Returns:
            List of unique categories
        """
        categories = set()
        for player_info in self._players.values():
            category = player_info['metadata'].get('category')
            if category:
                categories.add(category)
        return sorted(categories)
    
    def get_by_elo_range(self, min_elo: int = 0, max_elo: int = 3000) -> List[str]:
        """
        Get players within ELO range.
        
        Args:
            min_elo: Minimum ELO
            max_elo: Maximum ELO
            
        Returns:
            List of player names in range
        """
        players = []
        for name, info in self._players.items():
            elo = info['metadata'].get('estimated_elo', 0)
            if isinstance(elo, int) and min_elo <= elo <= max_elo:
                players.append(name)
        return sorted(players)
    
    def clear_instance_cache(self, player_name: str = None):
        """
        Clear cached player instances.
        
        Args:
            player_name: Specific player to clear (None = clear all)
        """
        if player_name:
            if player_name in self._instances:
                logger.info(f"🗑️  Clearing cached instance: {player_name} @ {id(self._instances[player_name])}")
                del self._instances[player_name]
        else:
            logger.info(f"🗑️  Clearing ALL cached instances ({len(self._instances)} total)")
            self._instances.clear()
    
    def reload(self):
        """Reload all player configurations from disk."""
        logger.info("🔄 Reloading player configurations...")
        
        # Clear caches
        self._players.clear()
        self._instances.clear()
        self.loader.clear_cache()
        self.discovery.clear_cache()
        
        # Rediscover and reload
        count = self.discover_and_load_all()
        
        logger.info(f"✅ Reloaded {count} player(s)")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_players': len(self._players),
            'cached_instances': len(self._instances),
            'categories': self.get_categories(),
            'factory_stats': self.factory.get_stats(),
            'players': list(self._players.keys())
        }
    
    def print_summary(self):
        """Print a formatted summary of all players."""
        if not self._players:
            logger.info("No players loaded.")
            return
        
        logger.info("\n" + "=" * 80)
        logger.info("🎮 Registered AI Players")
        logger.info("=" * 80)
        
        # Group by category
        by_category: Dict[str, List[str]] = {}
        for name, info in sorted(self._players.items()):
            category = info['metadata'].get('category', 'unknown')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(name)
        
        # Print by category
        for category in sorted(by_category.keys()):
            logger.info(f"\n📁 {category.upper()}:")
            for name in sorted(by_category[category]):
                info = self._players[name]
                metadata = info['metadata']
                icon = metadata.get('icon', '🤖')
                elo = metadata.get('estimated_elo', '???')
                description = metadata.get('description', 'No description')
                logger.info(f"  {icon} {name:<20} ELO: {elo:<4} - {description}")
        
        logger.info("\n" + "=" * 80)
        logger.info(f"Total: {len(self._players)} player(s)")
        logger.info("=" * 80 + "\n")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    # Context manager support
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        # Cleanup if needed
        pass


# Convenience function for quick access
def get_registry(**kwargs) -> PlayerRegistry:
    """
    Get the global PlayerRegistry instance.
    
    Args:
        **kwargs: Arguments passed to PlayerRegistry constructor (only on first call)
        
    Returns:
        PlayerRegistry singleton instance
    """
    return PlayerRegistry(**kwargs)

