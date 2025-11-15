"""
Configuration Validator

Validates player configuration files for correctness and completeness.
Implements comprehensive validation rules following the Single Responsibility Principle.

Architecture:
- Schema validation
- Type checking
- Range validation
- Cross-field validation
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ConfigValidator:
    """
    Validates player configuration dictionaries.

    Follows the Single Responsibility Principle: focuses solely on validation.
    Uses composition over inheritance for validation rules.
    """

    # Required top-level sections
    REQUIRED_SECTIONS = [
        "metadata",
        "engine",
        "evaluation",
        "move_ordering",
        "pruning",
        "opening_book",
        "behavior",
    ]

    # Required metadata fields
    REQUIRED_METADATA = ["name"]

    # Required engine fields
    REQUIRED_ENGINE = ["depth", "parallel", "transposition_table"]

    # Valid values for enum fields
    VALID_DEPTH_STRATEGIES = ["fixed", "iterative", "adaptive"]
    VALID_BOOK_STRATEGIES = ["instant", "evaluated", "disabled"]
    VALID_LOG_LEVELS = ["quiet", "normal", "verbose", "debug"]
    VALID_CATEGORIES = ["beginner", "intermediate", "advanced", "champion", "premium"]

    def __init__(self, strict: bool = False):
        """
        Initialize validator.

        Args:
            strict: If True, warnings are treated as errors
        """
        self.strict = strict
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, config: Dict[str, Any], config_path: Optional[Path] = None) -> bool:
        """
        Validate a configuration dictionary.

        Args:
            config: Configuration dictionary to validate
            config_path: Path to config file (for error messages)

        Returns:
            True if valid, False otherwise

        Note:
            Errors and warnings are accumulated in self.errors and self.warnings
        """
        self.errors = []
        self.warnings = []

        context = str(config_path) if config_path else "config"

        # Validate structure
        self._validate_structure(config, context)

        if not self.errors:  # Only validate details if structure is valid
            self._validate_metadata(config.get("metadata", {}), context)
            self._validate_engine(config.get("engine", {}), context)
            self._validate_evaluation(config.get("evaluation", {}), context)
            self._validate_move_ordering(config.get("move_ordering", {}), context)
            self._validate_pruning(config.get("pruning", {}), context)
            self._validate_opening_book(config.get("opening_book", {}), context)
            self._validate_behavior(config.get("behavior", {}), context)

        # Log results
        if self.errors:
            for error in self.errors:
                logger.error(f"  ❌ {error}")

        if self.warnings:
            for warning in self.warnings:
                logger.warning(f"  ⚠️  {warning}")

        # In strict mode, warnings count as errors
        is_valid = len(self.errors) == 0 and (not self.strict or len(self.warnings) == 0)

        return is_valid

    def _validate_structure(self, config: Dict[str, Any], context: str):
        """Validate top-level structure."""
        for section in self.REQUIRED_SECTIONS:
            if section not in config:
                self.errors.append(f"Missing required section '{section}' in {context}")

    def _validate_metadata(self, metadata: Dict[str, Any], context: str):
        """Validate metadata section."""
        if not metadata:
            return

        # Required fields
        for field in self.REQUIRED_METADATA:
            if field not in metadata:
                self.errors.append(f"Missing required metadata field '{field}'")

        # Validate name
        if "name" in metadata:
            name = metadata["name"]
            if not isinstance(name, str) or not name.strip():
                self.errors.append(f"metadata.name must be a non-empty string")

        # Validate ELO if present
        if "estimated_elo" in metadata:
            elo = metadata["estimated_elo"]
            if not isinstance(elo, int) or elo < 1000 or elo > 3000:
                self.warnings.append(
                    f"metadata.estimated_elo should be between 1000-3000, got {elo}"
                )

        # Validate category if present
        if "category" in metadata:
            category = metadata["category"]
            if category not in self.VALID_CATEGORIES:
                self.warnings.append(
                    f"metadata.category '{category}' not in standard categories: {self.VALID_CATEGORIES}"
                )

    def _validate_engine(self, engine: Dict[str, Any], context: str):
        """Validate engine section."""
        if not engine:
            return

        # Validate depth
        if "depth" in engine:
            depth_config = engine["depth"]
            if not isinstance(depth_config, dict):
                self.errors.append("engine.depth must be a dictionary")
                return

            if "base" not in depth_config:
                self.errors.append("engine.depth.base is required")
            else:
                base = depth_config["base"]
                if not isinstance(base, int) or base < 1 or base > 20:
                    self.errors.append(f"engine.depth.base must be 1-20, got {base}")

            if "strategy" not in depth_config:
                self.errors.append("engine.depth.strategy is required")
            else:
                strategy = depth_config["strategy"]
                if strategy not in self.VALID_DEPTH_STRATEGIES:
                    self.errors.append(
                        f"engine.depth.strategy must be one of {self.VALID_DEPTH_STRATEGIES}, got '{strategy}'"
                    )

                # Validate strategy-specific fields
                if strategy == "adaptive" and "adaptive" not in depth_config:
                    self.errors.append(
                        "engine.depth.adaptive configuration required for adaptive strategy"
                    )

        # Validate parallel
        if "parallel" in engine:
            parallel = engine["parallel"]
            if not isinstance(parallel, dict):
                self.errors.append("engine.parallel must be a dictionary")
            elif "enabled" not in parallel:
                self.errors.append("engine.parallel.enabled is required")

    def _validate_evaluation(self, evaluation: Dict[str, Any], context: str):
        """Validate evaluation section."""
        if not evaluation:
            return

        # Either preset or evaluators must be present
        has_preset = evaluation.get("preset") is not None
        has_evaluators = "evaluators" in evaluation and evaluation["evaluators"]

        if not has_preset and not has_evaluators:
            self.warnings.append("evaluation should have either 'preset' or 'evaluators' defined")

        # Validate evaluators if present
        if "evaluators" in evaluation:
            evaluators = evaluation["evaluators"]
            if not isinstance(evaluators, list):
                self.errors.append("evaluation.evaluators must be a list")
            else:
                for i, evaluator in enumerate(evaluators):
                    if not isinstance(evaluator, dict):
                        self.errors.append(f"evaluation.evaluators[{i}] must be a dictionary")
                        continue

                    if "name" not in evaluator:
                        self.errors.append(f"evaluation.evaluators[{i}].name is required")

                    if "enabled" not in evaluator:
                        self.warnings.append(f"evaluation.evaluators[{i}].enabled not specified")

                    if "weight" in evaluator:
                        weight = evaluator["weight"]
                        if not isinstance(weight, (int, float)) or weight < 0:
                            self.errors.append(
                                f"evaluation.evaluators[{i}].weight must be non-negative number"
                            )

    def _validate_move_ordering(self, move_ordering: Dict[str, Any], context: str):
        """Validate move_ordering section."""
        if not move_ordering:
            return

        if "strategies" in move_ordering:
            strategies = move_ordering["strategies"]
            if not isinstance(strategies, list):
                self.errors.append("move_ordering.strategies must be a list")

    def _validate_pruning(self, pruning: Dict[str, Any], context: str):
        """Validate pruning section."""
        # All pruning sections are optional, just validate structure if present
        for pruning_type in ["null_move", "futility", "late_move_reduction", "multi_cut"]:
            if pruning_type in pruning:
                config = pruning[pruning_type]
                if not isinstance(config, dict):
                    self.errors.append(f"pruning.{pruning_type} must be a dictionary")
                elif "enabled" not in config:
                    self.warnings.append(f"pruning.{pruning_type}.enabled not specified")

    def _validate_opening_book(self, opening_book: Dict[str, Any], context: str):
        """Validate opening_book section."""
        if not opening_book:
            return

        if "enabled" not in opening_book:
            self.warnings.append("opening_book.enabled not specified")

        if "strategy" in opening_book:
            strategy = opening_book["strategy"]
            if strategy not in self.VALID_BOOK_STRATEGIES:
                self.errors.append(
                    f"opening_book.strategy must be one of {self.VALID_BOOK_STRATEGIES}, got '{strategy}'"
                )

    def _validate_behavior(self, behavior: Dict[str, Any], context: str):
        """Validate behavior section."""
        if not behavior:
            return

        # Validate logging level if present
        if "logging" in behavior and isinstance(behavior["logging"], dict):
            logging_config = behavior["logging"]
            if "level" in logging_config:
                level = logging_config["level"]
                if level not in self.VALID_LOG_LEVELS:
                    self.errors.append(
                        f"behavior.logging.level must be one of {self.VALID_LOG_LEVELS}, got '{level}'"
                    )

        # Validate time settings if present
        if "time" in behavior and isinstance(behavior["time"], dict):
            time_config = behavior["time"]

            if "think_time_ms" in time_config:
                think_time = time_config["think_time_ms"]
                if not isinstance(think_time, int) or think_time < 0:
                    self.errors.append("behavior.time.think_time_ms must be non-negative integer")

            if "max_time_ms" in time_config and time_config["max_time_ms"] is not None:
                max_time = time_config["max_time_ms"]
                if not isinstance(max_time, int) or max_time <= 0:
                    self.errors.append("behavior.time.max_time_ms must be positive integer or null")

        # Validate randomization if present
        if "randomization" in behavior and isinstance(behavior["randomization"], dict):
            rand_config = behavior["randomization"]

            if "temperature" in rand_config:
                temp = rand_config["temperature"]
                if not isinstance(temp, (int, float)) or temp < 0 or temp > 1:
                    self.errors.append(
                        "behavior.randomization.temperature must be between 0.0 and 1.0"
                    )

    def get_validation_summary(self) -> str:
        """
        Get a formatted summary of validation results.

        Returns:
            Formatted string with errors and warnings
        """
        lines = []

        if self.errors:
            lines.append(f"❌ {len(self.errors)} Error(s):")
            for error in self.errors:
                lines.append(f"  • {error}")

        if self.warnings:
            lines.append(f"⚠️  {len(self.warnings)} Warning(s):")
            for warning in self.warnings:
                lines.append(f"  • {warning}")

        if not self.errors and not self.warnings:
            lines.append("✅ Configuration is valid")

        return "\n".join(lines)
