"""
Configuration Loader

Loads and parses YAML configuration files.
Implements caching and error handling following best practices.

Architecture:
- YAML parsing with error handling
- Configuration caching for performance
- Validation integration
- Comprehensive logging
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .validator import ConfigValidator
from .exceptions import InvalidConfigError


logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Loads player configurations from YAML files.
    
    Follows the Single Responsibility Principle: focuses on loading and parsing.
    Uses dependency injection for validation.
    """
    
    def __init__(self, validator: Optional[ConfigValidator] = None, use_cache: bool = True):
        """
        Initialize the config loader.
        
        Args:
            validator: ConfigValidator instance (creates default if None)
            use_cache: Whether to cache loaded configurations
        """
        self.validator = validator or ConfigValidator()
        self.use_cache = use_cache
        self._cache: Dict[Path, Dict[str, Any]] = {}
    
    def load(self, config_path: Path, validate: bool = True) -> Dict[str, Any]:
        """
        Load a configuration file.
        
        Args:
            config_path: Path to YAML configuration file
            validate: Whether to validate the configuration
            
        Returns:
            Configuration dictionary
            
        Raises:
            InvalidConfigError: If configuration is invalid
            FileNotFoundError: If file doesn't exist
        """
        # Check cache
        if self.use_cache and config_path in self._cache:
            logger.debug(f"Using cached configuration for {config_path.name}")
            return self._cache[config_path]
        
        # Load file
        try:
            logger.debug(f"Loading configuration from {config_path}")
            config = self._load_yaml(config_path)
        except Exception as e:
            raise InvalidConfigError(
                config_path=str(config_path),
                reason=f"Failed to parse YAML: {type(e).__name__}",
                details={'error': str(e)}
            )
        
        # Validate
        if validate:
            is_valid = self.validator.validate(config, config_path)
            if not is_valid:
                raise InvalidConfigError(
                    config_path=str(config_path),
                    reason="Configuration validation failed",
                    details={
                        'errors': self.validator.errors,
                        'warnings': self.validator.warnings
                    }
                )
        
        # Cache and return
        if self.use_cache:
            self._cache[config_path] = config
        
        return config
    
    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """
        Load and parse a YAML file.
        
        Args:
            path: Path to YAML file
            
        Returns:
            Parsed YAML as dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML is malformed
        """
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error in {path}: {e}")
                raise
        
        if not isinstance(config, dict):
            raise ValueError(f"Configuration must be a dictionary, got {type(config)}")
        
        return config
    
    def load_multiple(self, config_paths: list[Path], validate: bool = True) -> Dict[Path, Dict[str, Any]]:
        """
        Load multiple configuration files.
        
        Args:
            config_paths: List of paths to configuration files
            validate: Whether to validate configurations
            
        Returns:
            Dictionary mapping paths to loaded configurations
            
        Note:
            Invalid configurations are logged but not included in results
        """
        results = {}
        
        for path in config_paths:
            try:
                config = self.load(path, validate=validate)
                results[path] = config
            except Exception as e:
                logger.error(f"Failed to load {path}: {e}")
        
        return results
    
    def clear_cache(self):
        """Clear the configuration cache."""
        self._cache.clear()
        logger.debug("Configuration cache cleared")
    
    def get_metadata(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract metadata from configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Metadata dictionary
        """
        return config.get('metadata', {})
    
    def get_player_name(self, config: Dict[str, Any]) -> str:
        """
        Extract player name from configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Player name
            
        Raises:
            KeyError: If name not found in metadata
        """
        metadata = self.get_metadata(config)
        if 'name' not in metadata:
            raise KeyError("Player name not found in configuration metadata")
        return metadata['name']

