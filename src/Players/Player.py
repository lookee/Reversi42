"""
Player - Base class for all players

Clean Architecture: Players are in the domain layer and should NOT
depend on any specific UI frameworks.

Design Pattern: Template Method
"""

from typing import List, Optional

from Reversi.Game import Move


class Player(object):
    """
    Base class for all players.

    This is the domain layer - NO UI dependencies allowed here!
    Players depend on abstractions (InputProvider), not concrete implementations.

    Subclasses can define class-level metadata for automatic menu generation.
    """

    # Class-level metadata for menu generation
    PLAYER_METADATA = {
        "display_name": "Player",
        "description": "Base player class",
        "enabled": False,  # Not selectable by default
        "parameters": [],  # List of configurable parameters
    }

    def __init__(self):
        self.name = "Player"

    def get_name(self) -> str:
        """Get player name."""
        return self.name

    def get_move(self, game, move_list: List[Move], control=None) -> Optional[Move]:
        """
        Get next move from this player.

        Args:
            game: Current game state
            move_list: List of legal moves
            control: (DEPRECATED) BoardControl instance - use InputProvider instead
                     In WebGUI context, this is the SearchObserver for AI insights

        Returns:
            Selected move, or None if exit/pause
        """
        # Default implementation: return first move
        return move_list[0] if move_list else None

    def _call_engine_with_observer(
        self,
        engine,
        bitboard_game,
        depth,
        player_name=None,
        opening_book=None,
        game_history=None,
        observer=None,
    ):
        """
        Helper method to call engine.get_best_move with observer support.

        This centralizes observer handling so all AI players get it automatically.

        Args:
            engine: ApocalyptronEngine instance
            bitboard_game: BitboardGame instance
            depth: Search depth
            player_name: Player name (optional)
            opening_book: Opening book instance (optional)
            game_history: Game history string (optional)
            observer: SearchObserver instance (optional, from control parameter)

        Returns:
            Best move from engine
        """
        return engine.get_best_move(
            bitboard_game,
            depth,
            player_name=player_name,
            opening_book=opening_book,
            game_history=game_history,
            observer=observer,
        )

    @classmethod
    def get_metadata(cls):
        """Get player metadata for menu generation"""
        return cls.PLAYER_METADATA
