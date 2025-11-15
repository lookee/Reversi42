"""
Custom exceptions for the AI Player Configuration System.

Following best practices for exception hierarchy and error handling.
"""


class PlayerConfigError(Exception):
    """Base exception for all player configuration errors."""

    pass


class PlayerNotFoundError(PlayerConfigError):
    """Raised when a requested player cannot be found."""

    def __init__(self, player_name: str, available_players: list = None):
        self.player_name = player_name
        self.available_players = available_players or []

        message = f"Player '{player_name}' not found."
        if self.available_players:
            message += f"\nAvailable players: {', '.join(self.available_players)}"

        super().__init__(message)


class InvalidConfigError(PlayerConfigError):
    """Raised when a configuration file is invalid."""

    def __init__(self, config_path: str, reason: str, details: dict = None):
        self.config_path = config_path
        self.reason = reason
        self.details = details or {}

        message = f"Invalid configuration in '{config_path}': {reason}"
        if self.details:
            message += f"\nDetails: {self.details}"

        super().__init__(message)


class PlayerCreationError(PlayerConfigError):
    """Raised when player instance creation fails."""

    def __init__(self, player_name: str, config_path: str, original_error: Exception):
        self.player_name = player_name
        self.config_path = config_path
        self.original_error = original_error

        message = (
            f"Failed to create player '{player_name}' from config '{config_path}': "
            f"{type(original_error).__name__}: {str(original_error)}"
        )

        super().__init__(message)


class ConfigNotFoundError(PlayerConfigError):
    """Raised when configuration directory or file cannot be found."""

    def __init__(self, path: str):
        self.path = path
        message = f"Configuration path not found: {path}"
        super().__init__(message)
