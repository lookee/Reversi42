"""
Player Factory

Creates player instances from configuration dictionaries.
Implements the Abstract Factory pattern for flexible player creation.

Architecture:
- Configuration to player instance mapping
- Engine configuration building
- Dependency injection for extensibility
- Comprehensive error handling
"""

import copy
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .exceptions import PlayerCreationError

logger = logging.getLogger(__name__)


class PlayerFactory:
    """
    Creates AI player instances from configurations.

    Follows the Factory pattern and Dependency Inversion Principle.
    Extensible for different player types.
    """

    def __init__(self):
        """Initialize the player factory."""
        self._creation_stats: Dict[str, Any] = {
            "total_created": 0,
            "failed": 0,
            "by_category": {},
        }

    def create_player(self, config: Dict[str, Any], config_path: Optional[Path] = None) -> Any:
        """
        Create a player instance from configuration.

        Args:
            config: Configuration dictionary
            config_path: Path to config file (for error messages)

        Returns:
            Player instance

        Raises:
            PlayerCreationError: If player creation fails
        """
        player_name = config.get("metadata", {}).get("name", "Unknown")

        try:
            logger.info(f"")
            logger.info(f"╔══════════════════════════════════════════════════════════════╗")
            logger.info(f"║ 🏗️  FACTORY: Creating player from config                    ║")
            logger.info(f"╠══════════════════════════════════════════════════════════════╣")
            logger.info(f"   Player name from metadata: {player_name}")
            logger.info(f"   Config file path: {config_path}")

            # Check player type from metadata FIRST (before building engine config)
            metadata = config.get("metadata", {})
            player_type = metadata.get("type", "apocalyptron")  # Default to apocalyptron
            
            if player_type == "rl":
                # Create RL player (skip engine config)
                player = self._create_rl_player(config)
                self._update_stats(config, success=True)
                logger.info(f"✅ Successfully created RL player: {player_name} @ {id(player)}")
                logger.info(f"╚══════════════════════════════════════════════════════════════╝")
                logger.info(f"")
                return player

            # Log key configuration details FROM YAML
            engine_config_dict = config.get("engine", {})
            depth_config = engine_config_dict.get("depth", {})
            logger.info(f"")
            logger.info(f"   📄 YAML Configuration:")
            logger.info(f"      Depth base: {depth_config.get('base')} (LIGHTNING=4, DIVZERO=12)")
            logger.info(f"      Strategy: {depth_config.get('strategy')}")
            logger.info(
                f"      Transposition table: {engine_config_dict.get('transposition_table', {}).get('enabled', True)}"
            )
            logger.info(
                f"      Parallel: {engine_config_dict.get('parallel', {}).get('enabled', True)}"
            )
            logger.info(
                f"      Aspiration windows: {engine_config_dict.get('aspiration_windows', {}).get('enabled', True)}"
            )
            logger.info(f"╚══════════════════════════════════════════════════════════════╝")
            logger.info(f"")

            # Build engine configuration
            engine_config = self._build_engine_config(config)

            logger.info(f"")
            logger.info(f"   ⚙️  Engine Config Built:")
            logger.info(f"      Config ID: {id(engine_config)}")
            logger.info(
                f"      Depth: {engine_config.depth} (YAML said: {depth_config.get('base')})"
            )
            logger.info(
                f"      Strategy: {engine_config.search_strategy} (YAML said: {depth_config.get('strategy')})"
            )
            logger.info(f"      Transposition Table: {engine_config.use_transposition_table}")
            logger.info(f"      Parallel: {engine_config.use_parallel}")
            logger.info(f"      Aspiration: {engine_config.use_aspiration_windows}")

            # VALIDATION: Verify config matches YAML
            expected_depth = depth_config.get("base", 9)
            if engine_config.depth != expected_depth:
                logger.error(f"   ❌ CRITICAL: Depth mismatch!")
                logger.error(f"      YAML: {expected_depth}")
                logger.error(f"      Config: {engine_config.depth}")

            expected_strategy = depth_config.get("strategy", "iterative")
            if expected_strategy == "fixed" and engine_config.search_strategy != "fixed_depth":
                logger.error(f"   ❌ CRITICAL: Strategy mismatch!")
                logger.error(f"      YAML: fixed")
                logger.error(f"      Config: {engine_config.search_strategy}")

            logger.info(f"")

            # CRITICAL: Create a deep copy of the config to ensure it's independent
            # This prevents any accidental sharing between players
            engine_config_copy = copy.deepcopy(engine_config)
            logger.info(f"   🔄 Created DEEP COPY of engine config:")
            logger.info(f"      Original ID: {id(engine_config)}")
            logger.info(f"      Copy ID: {id(engine_config_copy)}")
            logger.info(f"      Copy Depth: {engine_config_copy.depth}")
            logger.info(f"")

            # Create player instance using ApocalyptronEngine with COPY
            player = self._create_apocalyptron_player(config, engine_config_copy)

            # FINAL VALIDATION: Verify player has correct config
            if hasattr(player, "bitboard_engine") and hasattr(player.bitboard_engine, "config"):
                actual_config = player.bitboard_engine.config
                logger.info(f"   ✅ FINAL VALIDATION - Player Engine Config:")
                logger.info(f"      Depth: {actual_config.depth}")
                logger.info(f"      Strategy: {actual_config.search_strategy}")
                logger.info(f"      Transposition Table: {actual_config.use_transposition_table}")
                logger.info(f"      Parallel: {actual_config.use_parallel}")
                logger.info(f"      Aspiration: {actual_config.use_aspiration_windows}")

                # Verify it matches what we built
                if actual_config.depth != engine_config.depth:
                    logger.error(f"   ❌ CRITICAL: Player config doesn't match built config!")
                    logger.error(
                        f"      Built: {engine_config.depth}, Player: {actual_config.depth}"
                    )

            # Update statistics
            self._update_stats(config, success=True)

            logger.info(f"✅ Successfully created player: {player_name} @ {id(player)}")
            logger.info(f"╚══════════════════════════════════════════════════════════════╝")
            logger.info(f"")
            return player

        except Exception as e:
            self._update_stats(config, success=False)
            raise PlayerCreationError(
                player_name=player_name,
                config_path=str(config_path) if config_path else "unknown",
                original_error=e,
            )

    def _build_engine_config(self, config: Dict[str, Any]) -> Any:
        """
        Build ApocalyptronEngine configuration from config dict.

        Args:
            config: Configuration dictionary

        Returns:
            ApocalyptronConfig instance
        """
        from AI.Apocalyptron import ApocalyptronConfigBuilder

        engine_config = config.get("engine", {})
        depth_config = engine_config.get("depth", {})

        # Start building configuration
        builder = ApocalyptronConfigBuilder()

        # Configure depth
        base_depth = depth_config.get("base", 9)
        builder.with_depth(base_depth)

        # Configure depth strategy
        strategy = depth_config.get("strategy", "iterative")

        if strategy == "fixed":
            builder.with_fixed_depth_search()
        elif strategy == "adaptive":
            adaptive_config = depth_config.get("adaptive", {})
            builder.with_adaptive_depth(
                opening=adaptive_config.get("opening", base_depth - 2),
                midgame=adaptive_config.get("midgame", base_depth),
                endgame=adaptive_config.get("endgame", base_depth + 2),
            )
        else:  # iterative (default)
            builder.enable_iterative_deepening()

        # Configure evaluation
        self._configure_evaluation(builder, config.get("evaluation", {}))

        # Configure parallelization
        parallel_config = engine_config.get("parallel", {})
        if parallel_config.get("enabled", True):
            num_workers = parallel_config.get("num_workers")
            builder.with_num_workers(num_workers)
        else:
            builder.enable_parallel(False)

        # Configure transposition table
        tt_config = engine_config.get("transposition_table", {})
        tt_enabled = tt_config.get("enabled", True)  # Default True
        logger.info(f"   TT config from YAML: enabled={tt_enabled}")
        # Set directly in config (no builder method exists)
        builder._config.use_transposition_table = tt_enabled
        if tt_enabled:
            size_mb = tt_config.get("size_mb", 128)
            logger.info(f"   ✅ Transposition Table ENABLED (size: {size_mb}MB)")
        else:
            logger.info(f"   ❌ Transposition Table DISABLED")

        # Configure pruning optimizations
        self._configure_pruning(builder, config.get("pruning", {}))

        # Configure aspiration windows
        aw_config = engine_config.get("aspiration_windows", {})
        aw_enabled = aw_config.get("enabled", True)  # Default True
        logger.info(f"   Aspiration config from YAML: enabled={aw_enabled}")
        builder.enable_aspiration_windows(aw_enabled)  # Pass False to disable
        if aw_enabled:
            logger.info(f"   ✅ Aspiration Windows ENABLED")
        else:
            logger.info(f"   ❌ Aspiration Windows DISABLED")

        # Configure temperature/randomization
        behavior_config = config.get("behavior", {})
        randomization_config = behavior_config.get("randomization", {})
        if randomization_config.get("enabled", False):
            temperature = randomization_config.get("temperature", 0.0)
            builder.with_temperature(temperature)
            logger.info(f"   🌡️  Temperature: {temperature} (randomization enabled)")
        else:
            # Auto-calculate temperature from depth if not explicitly set
            from AI.Apocalyptron.core.config import calculate_default_temperature

            auto_temperature = calculate_default_temperature(base_depth)
            builder.with_temperature(auto_temperature)
            logger.info(
                f"   🌡️  Temperature: {auto_temperature} (auto-calculated from depth {base_depth})"
            )

        return builder.build()

    def _configure_evaluation(self, builder, eval_config: Dict[str, Any]):
        """Configure evaluation settings."""
        preset = eval_config.get("preset")

        if preset:
            # Use preset
            from AI.Apocalyptron.weights import get_preset_weights

            try:
                weights = get_preset_weights(preset)
                builder.with_weights(weights)
            except Exception as e:
                logger.warning(f"Failed to load preset '{preset}': {e}, using default")

        elif "evaluators" in eval_config:
            # Use custom evaluators
            from AI.Apocalyptron.core.config import EvaluatorConfig

            evaluators = []
            for ev_config in eval_config["evaluators"]:
                if ev_config.get("enabled", True):
                    evaluators.append(
                        EvaluatorConfig(ev_config["name"], weight=ev_config.get("weight", 1.0))
                    )

            if evaluators:
                builder.with_evaluators(evaluators)

    def _configure_pruning(self, builder, pruning_config: Dict[str, Any]):
        """Configure pruning optimizations."""
        # Null move pruning
        null_move_config = pruning_config.get("null_move", {})
        builder.enable_null_move_pruning(null_move_config.get("enabled", True))

        # Futility pruning
        futility_config = pruning_config.get("futility", {})
        builder.enable_futility_pruning(futility_config.get("enabled", True))

        # Late move reduction
        lmr_config = pruning_config.get("late_move_reduction", {})
        builder.enable_late_move_reduction(lmr_config.get("enabled", True))

        # Multi-cut pruning (note: method name is enable_multi_cut_pruning)
        multi_cut_config = pruning_config.get("multi_cut", {})
        builder.enable_multi_cut_pruning(multi_cut_config.get("enabled", True))

    def _create_apocalyptron_player(self, config: Dict[str, Any], engine_config: Any) -> Any:
        """
        Create a configurable AI player instance.

        Args:
            config: Full configuration dictionary
            engine_config: Built engine configuration

        Returns:
            Player instance
        """
        from AI.Apocalyptron import ApocalyptronEngine
        from domain.knowledge import get_default_opening_book

        # Create a dynamic player class
        class ConfiguredPlayer:
            def __init__(self):
                metadata = config.get("metadata", {})
                self.name: str = str(metadata.get("name", "ConfiguredAI"))
                self.metadata = metadata
                self.config = config

                # Create engine
                self.bitboard_engine = ApocalyptronEngine(config=engine_config)

                # Setup opening book
                book_config = config.get("opening_book", {})
                if book_config.get("enabled", True):
                    self.opening_book = get_default_opening_book()
                    self.book_instant = book_config.get("strategy", "evaluated") == "instant"
                else:
                    self.opening_book = None
                    self.book_instant = False

                # Depth for move selection
                depth_config = config.get("engine", {}).get("depth", {})
                self.depth = depth_config.get("base", 9)
                self.deep = self.depth

                # Statistics
                self.book_hits = 0
                self.total_moves = 0

            def get_name(self) -> str:
                return self.name

            def get_move(self, game, moves, control=None):
                """Get next move using configuration-based strategy."""
                self.total_moves += 1

                if not moves:
                    return None

                # Get game history
                game_history = self._get_game_history(game)

                # Try opening book if enabled
                if self.opening_book:
                    book_moves = self.opening_book.get_book_moves(game_history)
                    if book_moves:
                        valid_book_moves = [m for m in book_moves if m in moves]
                        if valid_book_moves:
                            self.book_hits += 1
                            if self.book_instant:
                                # Get temperature from engine config
                                temperature = (
                                    self.bitboard_engine.config.temperature
                                    if hasattr(self.bitboard_engine, "config")
                                    else 0.0
                                )
                                return self.opening_book.get_best_opening_move(
                                    game_history,
                                    valid_book_moves,
                                    game.turn,
                                    show_details=False,
                                    temperature=temperature,
                                )

                # Engine search
                try:
                    bitboard_game = self._convert_to_bitboard(game)
                    move = self.bitboard_engine.get_best_move(
                        bitboard_game,
                        self.deep,
                        player_name=self.name,
                        opening_book=self.opening_book,
                        game_history=game_history,
                        observer=control,
                    )
                    if move and game.valid_move(move):
                        return move
                except Exception as e:
                    logger.error(f"Engine error for {self.name}: {e}")
                    # Fallback to first legal move
                    return moves[0] if moves else None

                return moves[0] if moves else None

            def _get_game_history(self, game):
                """Extract game history."""
                if hasattr(game, "history"):
                    return game.history
                return ""

            def _convert_to_bitboard(self, game):
                """Convert standard game to BitboardGame."""
                from Reversi.BitboardGame import BitboardGame

                bitboard = BitboardGame.create_empty()

                for y in range(1, 9):
                    for x in range(1, 9):
                        cell = game.matrix[y][x]
                        bit = (y - 1) * 8 + (x - 1)

                        if cell == "B":
                            bitboard.black |= 1 << bit
                        elif cell == "W":
                            bitboard.white |= 1 << bit

                bitboard.turn = game.turn
                bitboard.turn_cnt = game.turn_cnt
                bitboard.history = game.history if hasattr(game, "history") else ""
                bitboard.black_cnt = bitboard._count_bits(bitboard.black)
                bitboard.white_cnt = bitboard._count_bits(bitboard.white)
                bitboard._create_virtual_matrix()

                return bitboard

        return ConfiguredPlayer()
    
    def _create_rl_player(self, config: Dict[str, Any]) -> Any:
        """
        Create an RL player instance from configuration.
        
        Args:
            config: Full configuration dictionary
            
        Returns:
            PlayerRL instance
        """
        from Players.PlayerRL import PlayerRL
        
        metadata = config.get("metadata", {})
        rl_config = config.get("rl", {})
        
        # Get RL-specific parameters
        model_path = rl_config.get("model_path", "experimental/checkpoints/latest.pth")
        use_mcts = rl_config.get("use_mcts", True)
        mcts_simulations = rl_config.get("mcts_simulations", 400)
        temperature = rl_config.get("temperature", 0.1)
        name = metadata.get("name", "Neural Prime")
        
        # Create RL player
        player = PlayerRL(
            model_path=model_path,
            use_mcts=use_mcts,
            mcts_simulations=mcts_simulations,
            temperature=temperature,
            name=name
        )
        
        return player

    def _update_stats(self, config: Dict[str, Any], success: bool):
        """Update creation statistics."""
        if success:
            self._creation_stats["total_created"] += 1
        else:
            self._creation_stats["failed"] += 1

        # Track by category
        category = config.get("metadata", {}).get("category", "unknown")
        if category not in self._creation_stats["by_category"]:
            self._creation_stats["by_category"][category] = 0
        self._creation_stats["by_category"][category] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get creation statistics."""
        return self._creation_stats.copy()
