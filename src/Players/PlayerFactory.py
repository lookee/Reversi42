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


class PlayerFactory:
    """
    Factory class for creating players with Dependency Injection.
    
    MIGRATION NOTE: This factory now wraps the new PlayerRegistry system.
    All Gladiator players are now created from YAML configurations.
    
    Clean Architecture: Factory handles dependency injection of InputProviders
    for human players, keeping the Player domain layer UI-agnostic.
    
    Legacy Support: Maintains backward compatibility with old API.
    New code should use Players.config.PlayerRegistry directly.
    """

    # Legacy player classes (kept for backward compatibility)
    LEGACY_PLAYER_CLASSES = [
        PlayerHuman,         # Human player
        PlayerApocalyptron,  # Apocalyptron AI
    ]

    # Build legacy registry
    PLAYER_TYPES = {cls.PLAYER_METADATA["display_name"]: cls for cls in LEGACY_PLAYER_CLASSES}
    
    # NEW: PlayerRegistry integration
    _registry = None

    # Store board_control for DI (set externally)
    _board_control = None
    _ui_type = "headless"  # Default UI type

    @classmethod
    def set_board_control(cls, board_control):
        """
        Set BoardControl for dependency injection.

        Args:
            board_control: BoardControl instance
        """
        cls._board_control = board_control

    @classmethod
    def set_ui_type(cls, ui_type: str):
        """
        Set UI type for InputProvider selection.

        Args:
            ui_type: 'headless'
        """
        cls._ui_type = ui_type

    @classmethod
    def _get_registry(cls):
        """Get or create PlayerRegistry instance (lazy initialization)."""
        if cls._registry is None:
            from Players.config import PlayerRegistry
            cls._registry = PlayerRegistry(auto_discover=True)
        return cls._registry
    
    @classmethod
    def create_player(cls, player_type, **kwargs):
        """
        Create a player of the specified type with dependency injection.
        
        MIGRATION: Now uses PlayerRegistry for AI players.
        
        For PlayerHuman, automatically injects appropriate InputProvider.
        For AI players, delegates to PlayerRegistry (config-based).

        Args:
            player_type (str): Type of player to create
            **kwargs: Additional arguments for player creation

        Returns:
            Player: The created player instance

        Raises:
            ValueError: If player type is not supported
        """
        # Check legacy players first (Human, Apocalyptron)
        if player_type in cls.PLAYER_TYPES:
            player_class = cls.PLAYER_TYPES[player_type]
            
            # Special handling for PlayerHuman - inject InputProvider
            if player_class == PlayerHuman:
                return cls.create_human_player(**kwargs)
            
            # Apocalyptron uses legacy class
            return player_class(**kwargs)
        
        # Try PlayerRegistry for config-based players (Gladiators)
        try:
            registry = cls._get_registry()
            
            # Check if player exists in registry
            if player_type in registry.list_players():
                return registry.create_player(player_type, cached=False)
            
            # Also check by display name variations
            for registered_name in registry.list_players():
                if registered_name.upper() == player_type.upper():
                    return registry.create_player(registered_name, cached=False)
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"Registry lookup failed for {player_type}: {e}")
        
        # Player not found
        available = list(cls.PLAYER_TYPES.keys())
        try:
            available.extend(cls._get_registry().list_players())
        except:
            pass
        
        raise ValueError(
            f"Unsupported player type: '{player_type}'\n"
            f"Available players: {', '.join(sorted(set(available)))}"
        )

    @classmethod
    def create_human_player(cls, name="Human", board_control=None, **kwargs):
        """
        Create human player with appropriate InputProvider (Dependency Injection!)

        Args:
            name: Player name
            board_control: BoardControl instance, if None uses factory's stored one
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
            board_control: BoardControl instance

        Returns:
            InputProvider implementation
        """
        # Only headless is supported now
        from Reversi.Game import Move
        from ui.implementations.headless.input_providers import MockInputProvider

        # Default mock moves for testing
        return MockInputProvider([Move(3, 3)], auto_exit=False)

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
        
        MIGRATION: Now includes both legacy and config-based players.

        Returns:
            list: List of available player type names
        """
        available = []
        
        # Legacy players
        for player_class in cls.LEGACY_PLAYER_CLASSES:
            if player_class.PLAYER_METADATA.get("enabled", False):
                available.append(player_class.PLAYER_METADATA["display_name"])
        
        # Config-based players from registry
        try:
            registry = cls._get_registry()
            available.extend(registry.list_players())
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Could not load registry players: {e}")
        
        return sorted(set(available))

    @classmethod
    def get_all_player_types(cls):
        """
        Get list of all player types (including disabled).
        
        MIGRATION: Now includes both legacy and config-based players.

        Returns:
            list: List of all player type names
        """
        all_types = list(cls.PLAYER_TYPES.keys())
        
        # Add config-based players
        try:
            registry = cls._get_registry()
            all_types.extend(registry.list_players())
        except Exception:
            pass
        
        return sorted(set(all_types))

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
