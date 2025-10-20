"""
Terminal View Implementation

Text-based ASCII UI with keyboard-only input.
All terminal-specific code is isolated here.

Version: 3.1.0
"""

from .input_handler import TerminalInputHandler
from .view import TerminalBoardView


class TerminalHumanPlayer:
    """
    Backward compatibility wrapper for PlayerHuman with TerminalInputProvider.

    This is now a factory class that creates PlayerHuman instances
    configured for terminal input, maintaining backward compatibility.
    """

    PLAYER_METADATA = {
        "display_name": "Terminal Human",
        "description": "Human player for terminal/console mode (text input)",
        "enabled": True,
        "parameters": [],
    }

    def __new__(cls, name="Terminal Human"):
        """
        Create PlayerHuman with TerminalInputProvider.

        Args:
            name: Player name

        Returns:
            PlayerHuman instance configured for terminal input
        """
        from Players.PlayerHuman import PlayerHuman

        from .input_providers import TerminalInputProvider

        provider = TerminalInputProvider()
        player = PlayerHuman(provider, name=name)

        # Add PLAYER_METADATA for compatibility
        player.PLAYER_METADATA = cls.PLAYER_METADATA

        return player

    @classmethod
    def get_metadata(cls):
        """Get player metadata for menu generation"""
        return cls.PLAYER_METADATA


__all__ = [
    "TerminalBoardView",
    "TerminalHumanPlayer",
    "TerminalInputHandler",
]
