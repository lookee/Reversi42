"""
Temperature-based move selection for variety.

Implements probabilistic move selection using temperature to add variety
to AI play while maintaining quality.
"""

import math
import random
from typing import List, Tuple, TypeVar, Union

Move = TypeVar("Move")


def apply_temperature_selection(
    moves_with_values: List[Tuple[Move, Union[int, float]]], temperature: float
) -> Move:
    """
    Select a move probabilistically based on temperature.

    When temperature is 0.0, always selects the best move (deterministic).
    When temperature > 0.0, uses softmax to select probabilistically,
    giving higher probability to better moves but allowing variety.

    Args:
        moves_with_values: List of (move, value) tuples, sorted by value descending
        temperature: Temperature parameter (0.0 = deterministic, 1.0 = maximum variety)

    Returns:
        Selected move

    Examples:
        temperature=0.0: Always picks best move
        temperature=0.1: Mostly picks best, occasionally picks second-best
        temperature=0.5: Significant variety, but still favors better moves
        temperature=1.0: Maximum variety, all moves have similar probability
    """
    if not moves_with_values:
        raise ValueError("moves_with_values cannot be empty")

    if temperature <= 0.0:
        # Deterministic: always pick best move
        return moves_with_values[0][0]

    if len(moves_with_values) == 1:
        # Only one move available
        return moves_with_values[0][0]

    # Extract moves and values
    moves = [m for m, _ in moves_with_values]
    # Convert values to float for softmax calculation
    values = [float(v) for _, v in moves_with_values]

    # Normalize values to avoid overflow in softmax
    # Shift values so max is 0 (prevents exp overflow)
    max_value = max(values)
    normalized_values = [v - max_value for v in values]

    # Apply temperature: divide by temperature (higher temp = more uniform)
    # Add small epsilon to avoid division by zero
    temp_adjusted = [v / (temperature + 1e-10) for v in normalized_values]

    # Compute softmax probabilities
    exp_values = [math.exp(v) for v in temp_adjusted]
    sum_exp = sum(exp_values)
    probabilities = [exp / sum_exp for exp in exp_values]

    # Select move based on probabilities
    selected = random.choices(moves, weights=probabilities, k=1)[0]

    return selected


def get_top_moves_with_similar_values(
    moves_with_values: List[Tuple[Move, Union[int, float]]], threshold: float = 0.05
) -> List[Tuple[Move, Union[int, float]]]:
    """
    Get moves with values within threshold of the best move.

    Useful for temperature selection: only consider moves that are
    "close enough" to the best move.

    Args:
        moves_with_values: List of (move, value) tuples, sorted by value descending
        threshold: Relative threshold (e.g., 0.05 = within 5% of best value)

    Returns:
        List of moves within threshold
    """
    if not moves_with_values:
        return []

    best_value = moves_with_values[0][1]

    # Calculate absolute threshold
    if abs(best_value) > 1e-6:
        abs_threshold = abs(best_value) * threshold
    else:
        # If best value is near zero, use small absolute threshold
        abs_threshold = 50.0  # Reasonable default for Reversi evaluations

    # Find all moves within threshold
    similar_moves = []
    for move, value in moves_with_values:
        if abs(value - best_value) <= abs_threshold:
            similar_moves.append((move, value))
        else:
            # Values are sorted descending, so we can stop
            break

    return similar_moves
