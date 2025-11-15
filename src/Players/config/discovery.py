"""
Player Discovery System

Recursively discovers all player configuration files in the enabled directory.
Implements the Strategy pattern for flexible discovery rules.

Architecture:
- Recursive directory scanning
- Configurable file patterns
- Caching for performance
- Logging for transparency
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class PlayerConfigFile:
    """Represents a discovered player configuration file."""

    path: Path
    name: str
    relative_path: str
    category: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.name} ({self.relative_path})"


class PlayerDiscovery:
    """
    Discovers player configuration files recursively.

    Follows the Open/Closed Principle: open for extension (custom patterns),
    closed for modification (core discovery logic).
    """

    DEFAULT_CONFIG_DIR = "config/players/enabled"
    DEFAULT_PATTERN = "*.yaml"
    EXCLUDED_FILES = {"00_AI_CONFIG_TEMPLATE.yaml", "template.yaml", "_example.yaml"}
    EXCLUDED_DIRS = {"__pycache__", ".git", "node_modules", "avatars"}

    def __init__(
        self,
        config_dir: Optional[str] = None,
        pattern: str = DEFAULT_PATTERN,
        project_root: Optional[str] = None,
    ):
        """
        Initialize the discovery system.

        Args:
            config_dir: Directory to scan (relative to project root)
            pattern: Glob pattern for config files (default: *.yaml)
            project_root: Project root directory (auto-detected if None)
        """
        self.project_root = Path(project_root) if project_root else self._find_project_root()
        self.config_dir = self.project_root / (config_dir or self.DEFAULT_CONFIG_DIR)
        self.pattern = pattern
        self._cache: Optional[List[PlayerConfigFile]] = None

        logger.debug(f"PlayerDiscovery initialized:")
        logger.debug(f"  Project root: {self.project_root}")
        logger.debug(f"  Config dir: {self.config_dir}")
        logger.debug(f"  Pattern: {self.pattern}")

    def discover(self, use_cache: bool = True) -> List[PlayerConfigFile]:
        """
        Discover all player configuration files.

        Args:
            use_cache: Use cached results if available

        Returns:
            List of discovered configuration files

        Raises:
            ConfigNotFoundError: If config directory doesn't exist
        """
        if use_cache and self._cache is not None:
            logger.debug(f"Using cached discovery results ({len(self._cache)} players)")
            return self._cache

        if not self.config_dir.exists():
            from .exceptions import ConfigNotFoundError

            raise ConfigNotFoundError(str(self.config_dir))

        logger.info(f"🔍 Discovering players in: {self.config_dir}")

        discovered = []
        for config_file in self._scan_directory(self.config_dir):
            discovered.append(config_file)
            logger.debug(f"  Found: {config_file}")

        # Sort by name for consistent ordering
        discovered.sort(key=lambda x: x.name.lower())

        self._cache = discovered
        logger.info(f"✅ Discovered {len(discovered)} player configuration(s)")

        return discovered

    def _scan_directory(self, directory: Path) -> List[PlayerConfigFile]:
        """
        Recursively scan directory for configuration files.

        Args:
            directory: Directory to scan

        Returns:
            List of discovered configuration files
        """
        discovered = []

        try:
            for item in directory.iterdir():
                # Skip excluded directories
                if item.is_dir():
                    if item.name in self.EXCLUDED_DIRS:
                        logger.debug(f"  Skipping excluded dir: {item.name}")
                        continue
                    # Recurse into subdirectories
                    discovered.extend(self._scan_directory(item))

                # Check files matching pattern
                elif item.is_file() and item.match(self.pattern):
                    if item.name in self.EXCLUDED_FILES:
                        logger.debug(f"  Skipping excluded file: {item.name}")
                        continue

                    config_file = self._create_config_file(item)
                    discovered.append(config_file)

        except PermissionError as e:
            logger.warning(f"⚠️  Permission denied scanning {directory}: {e}")
        except Exception as e:
            logger.error(f"❌ Error scanning {directory}: {e}")

        return discovered

    def _create_config_file(self, path: Path) -> PlayerConfigFile:
        """
        Create PlayerConfigFile from a path.

        Args:
            path: Path to configuration file

        Returns:
            PlayerConfigFile instance
        """
        # Calculate relative path from config dir
        try:
            relative = path.relative_to(self.config_dir)
        except ValueError:
            relative = path

        # Extract category from directory structure (if present)
        category = None
        if len(relative.parts) > 1:
            category = relative.parts[0]  # e.g., "gladiators" from "gladiators/divzero.yaml"

        # Extract player name from filename (without extension)
        name = path.stem

        return PlayerConfigFile(
            path=path, name=name, relative_path=str(relative), category=category
        )

    def _find_project_root(self) -> Path:
        """
        Auto-detect project root by looking for marker files.

        Returns:
            Path to project root
        """
        # Markers that indicate project root
        markers = ["pyproject.toml", "setup.py", "README.md", ".git"]

        # Start from current file's directory
        current = Path(__file__).resolve().parent

        # Walk up directory tree
        for parent in [current] + list(current.parents):
            if any((parent / marker).exists() for marker in markers):
                return parent

        # Fallback to current directory
        return Path.cwd()

    def clear_cache(self):
        """Clear the discovery cache."""
        self._cache = None
        logger.debug("Discovery cache cleared")

    def get_by_name(self, name: str) -> Optional[PlayerConfigFile]:
        """
        Get configuration file by player name.

        Args:
            name: Player name (case-insensitive)

        Returns:
            PlayerConfigFile if found, None otherwise
        """
        discovered = self.discover()
        name_lower = name.lower()

        for config in discovered:
            if config.name.lower() == name_lower:
                return config

        return None

    def get_by_category(self, category: str) -> List[PlayerConfigFile]:
        """
        Get all configuration files in a category.

        Args:
            category: Category name (e.g., "gladiators")

        Returns:
            List of PlayerConfigFile in category
        """
        discovered = self.discover()
        return [c for c in discovered if c.category == category]
