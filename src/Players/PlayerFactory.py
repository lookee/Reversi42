# ------------------------------------------------------------------------
#    Copyright (C) 2011 Luca Amore <luca.amore at gmail.com>
#
#    Reversi42 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Reversi42 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Reversi42.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------

from Players.Player import Player
from Players.PlayerApocalyptron import PlayerApocalyptron
from Players.PlayerHuman import PlayerHuman

# Epic Gladiators - 10 Legendary Fighters (from separate files)
from Players.Gladiators import (
    PlayerDivZero,
    PlayerLightningStrike,
    PlayerTheStrangler,
    PlayerFortressEternal,
    PlayerCornerReaper,
    PlayerTheOracle,
    PlayerBlitzDemon,
    PlayerTheExecutioner,
    PlayerGlitchLord,
    PlayerZenMaster,
)


class PlayerFactory:
    """
    Factory class for creating players with Dependency Injection.

    Clean Architecture: Factory handles dependency injection of InputProviders
    for human players, keeping the Player domain layer UI-agnostic.

    Player types are automatically discovered from their metadata.
    """

    # Registry of all player classes
    # Apocalyptron is the ultimate AI, followed by Epic Gladiators
    ALL_PLAYER_CLASSES = [
        PlayerHuman,  # Human player (disabled in menu, but available for API)
        PlayerApocalyptron,  # Apocalyptron - The ultimate AI (enabled in menu)
        # Epic Gladiators - 10 Legendary Fighters
        PlayerDivZero,  # The Ultimate Singularity (ELO 1880)
        PlayerLightningStrike,  # Lightning Fast (ELO 1400)
        PlayerTheStrangler,  # Mobility Assassin (ELO 1750)
        PlayerFortressEternal,  # Defensive Master (ELO 1800)
        PlayerCornerReaper,  # Corner Specialist (ELO 1720)
        PlayerTheOracle,  # Endgame Prophet (ELO 1850)
        PlayerBlitzDemon,  # Speed Incarnate (ELO 1350)
        PlayerTheExecutioner,  # Ruthless Destroyer (ELO 1770)
        PlayerGlitchLord,  # Chaotic Anomaly (ELO 1500)
        PlayerZenMaster,  # Enlightened One (ELO 1250)
    ]

    # Build registry from metadata
    PLAYER_TYPES = {cls.PLAYER_METADATA["display_name"]: cls for cls in ALL_PLAYER_CLASSES}

    # Store board_control for DI (set externally)
    _board_control = None
    _ui_type = "pygame"  # Default UI type

    @classmethod
    def set_board_control(cls, board_control):
        """
        Set BoardControl for dependency injection.

        Args:
            board_control: BoardControl instance for pygame InputProvider
        """
        cls._board_control = board_control

    @classmethod
    def set_ui_type(cls, ui_type: str):
        """
        Set UI type for InputProvider selection.

        Args:
            ui_type: 'pygame', 'terminal', or 'headless'
        """
        cls._ui_type = ui_type

    @classmethod
    def create_player(cls, player_type, **kwargs):
        """
        Create a player of the specified type with dependency injection.

        For PlayerHuman, automatically injects appropriate InputProvider.
        For AI players, creates normally.

        Args:
            player_type (str): Type of player to create
            **kwargs: Additional arguments for player creation

        Returns:
            Player: The created player instance

        Raises:
            ValueError: If player type is not supported
        """
        if player_type not in cls.PLAYER_TYPES:
            raise ValueError(f"Unsupported player type: {player_type}")

        player_class = cls.PLAYER_TYPES[player_type]

        # Special handling for PlayerHuman - inject InputProvider
        if player_class == PlayerHuman:
            return cls.create_human_player(**kwargs)

        # Other players (AI) don't need InputProvider
        return player_class(**kwargs)

    @classmethod
    def create_human_player(cls, name="Human", board_control=None, **kwargs):
        """
        Create human player with appropriate InputProvider (Dependency Injection!)

        Args:
            name: Player name
            board_control: BoardControl instance (for pygame), if None uses factory's stored one
            **kwargs: Additional arguments

        Returns:
            PlayerHuman instance with injected InputProvider
        """
        # Use provided board_control or factory's stored one
        control = board_control or cls._board_control

        # Create appropriate InputProvider based on UI type
        input_provider = cls._create_input_provider(control)

        # Inject dependency!
        return PlayerHuman(input_provider, name=name)

    @classmethod
    def _create_input_provider(cls, board_control):
        """
        Create appropriate InputProvider based on UI type.

        Design Pattern: Factory Method

        Args:
            board_control: BoardControl instance (for pygame)

        Returns:
            InputProvider implementation
        """
        if cls._ui_type == "pygame" and board_control:
            from ui.implementations.pygame.input_providers import PygameInputProvider

            return PygameInputProvider(board_control)
        elif cls._ui_type == "terminal":
            from ui.implementations.terminal.input_providers import TerminalInputProvider

            return TerminalInputProvider()
        elif cls._ui_type == "headless":
            from Reversi.Game import Move
            from ui.implementations.headless.input_providers import MockInputProvider

            # Default mock moves for testing
            return MockInputProvider([Move(3, 3)], auto_exit=False)
        else:
            # Fallback to pygame if available
            if board_control:
                from ui.implementations.pygame.input_providers import PygameInputProvider

                return PygameInputProvider(board_control)
            else:
                # Last resort: terminal
                from ui.implementations.terminal.input_providers import TerminalInputProvider

                return TerminalInputProvider()

    @classmethod
    def create_apocalyptron(cls, depth=9, weights=None, **kwargs):
        """
        Create an Apocalyptron AI player (recommended).

        Args:
            depth (int): Search depth (7-12 recommended, default 9)
            weights: GrandmasterWeights instance for custom evaluation (None = default)
            **kwargs: Additional arguments for player creation

        Returns:
            PlayerApocalyptron: The created Apocalyptron AI instance
        """
        return PlayerApocalyptron(depth=depth, weights=weights, **kwargs)

    @classmethod
    def create_grandmaster(cls, difficulty=9, weights=None, **kwargs):
        """
        Create a Grandmaster AI player (legacy alias for create_apocalyptron).

        Note: This method is kept for backwards compatibility.
        Grandmaster AI has been replaced by Apocalyptron.

        Args:
            difficulty (int): Search depth (7-12 recommended, default 9)
            weights: GrandmasterWeights instance for custom evaluation (None = default)
            **kwargs: Additional arguments for player creation

        Returns:
            PlayerApocalyptron: The created Apocalyptron AI instance
        """
        return PlayerApocalyptron(depth=difficulty, weights=weights, **kwargs)

    @classmethod
    def get_available_player_types(cls):
        """
        Get list of available (enabled) player types.

        Returns:
            list: List of available player type names
        """
        return [
            player_class.PLAYER_METADATA["display_name"]
            for player_class in cls.ALL_PLAYER_CLASSES
            if player_class.PLAYER_METADATA["enabled"]
        ]

    @classmethod
    def get_all_player_types(cls):
        """
        Get list of all player types (including disabled).

        Returns:
            list: List of all player type names
        """
        return list(cls.PLAYER_TYPES.keys())

    @classmethod
    def get_player_metadata(cls, player_type):
        """
        Get metadata for a specific player type.

        Args:
            player_type: Name of the player type

        Returns:
            dict: Player metadata
        """
        if player_type in cls.PLAYER_TYPES:
            return cls.PLAYER_TYPES[player_type].PLAYER_METADATA
        return None

    @classmethod
    def get_all_player_metadata(cls):
        """
        Get metadata for all player types.

        Returns:
            dict: Dictionary mapping player type names to their metadata
        """
        return {
            player_class.PLAYER_METADATA["display_name"]: player_class.PLAYER_METADATA
            for player_class in cls.ALL_PLAYER_CLASSES
        }

    @classmethod
    def register_player_type(cls, name, player_class):
        """
        Register a new player type.

        Args:
            name (str): Name of the player type
            player_class: Class that implements the player
        """
        cls.PLAYER_TYPES[name] = player_class
