"""
Reward Shaping Module

Calculates intermediate rewards during self-play:
- Corner capture: +0.1 per corner
- Bad squares penalty: -0.05 for dangerous squares (X-squares, C-squares)
- Mobility bonus: Based on relative mobility
- Stability bonus: For stable pieces
"""

import numpy as np
from typing import Tuple, Dict, List, Optional
from Reversi.BitboardGame import BitboardGame

# Corner positions: A1, H1, A8, H8
CORNER_POSITIONS = [0, 7, 56, 63]  # Bit positions

# X-squares: Adjacent to corners (dangerous!)
# A1 corner -> B2, A2, B1
# H1 corner -> G2, H2, G1
# A8 corner -> B7, A7, B8
# H8 corner -> G7, H7, G8
X_SQUARES = [
    9,   # B2 (near A1)
    1,   # A2 (near A1)
    8,   # B1 (near A1)
    54,  # G2 (near H1)
    62,  # H2 (near H1)
    55,  # G1 (near H1)
    49,  # B7 (near A8)
    57,  # A7 (near A8)
    48,  # B8 (near A8)
    46,  # G7 (near H8)
    63,  # H7 (near H8) - wait, H7 is 63? No, H8 is 63
    47,  # G8 (near H8)
]

# C-squares: Adjacent to corners on edges (also dangerous)
# A1 corner -> A3, C1
# H1 corner -> H3, F1
# A8 corner -> A6, C8
# H8 corner -> H6, F8
C_SQUARES = [
    2,   # A3 (near A1)
    16,  # C1 (near A1)
    58,  # H3 (near H1)
    45,  # F1 (near H1)
    40,  # A6 (near A8)
    19,  # C8 (near A8)
    59,  # H6 (near H8)
    46,  # F8 (near H8) - wait, F8 is 46, but G7 is also 46? Let me recalculate
]

# Recalculate C-squares properly
# A1 (0) -> A3 (2), C1 (16)
# H1 (7) -> H3 (5), F1 (45)
# A8 (56) -> A6 (40), C8 (19)
# H8 (63) -> H6 (59), F8 (46)
C_SQUARES = [2, 16, 5, 45, 40, 19, 59, 46]

# Remove duplicates and ensure they're not corners
BAD_SQUARES = list(set(X_SQUARES + C_SQUARES))
BAD_SQUARES = [pos for pos in BAD_SQUARES if pos not in CORNER_POSITIONS]


def get_corner_positions() -> List[int]:
    """Get list of corner positions."""
    return CORNER_POSITIONS.copy()


def get_bad_squares() -> List[int]:
    """Get list of bad square positions (X-squares and C-squares)."""
    return BAD_SQUARES.copy()


def count_corners(bitboard: int) -> int:
    """
    Count how many corners are occupied in a bitboard.
    
    Args:
        bitboard: 64-bit integer representing board
        
    Returns:
        Number of corners occupied (0-4)
    """
    count = 0
    for corner_pos in CORNER_POSITIONS:
        if bitboard & (1 << corner_pos):
            count += 1
    return count


def count_bad_squares(bitboard: int) -> int:
    """
    Count how many bad squares (X/C-squares) are occupied.
    
    Args:
        bitboard: 64-bit integer representing board
        
    Returns:
        Number of bad squares occupied
    """
    count = 0
    for bad_pos in BAD_SQUARES:
        if bitboard & (1 << bad_pos):
            count += 1
    return count


def calculate_mobility(game: BitboardGame, player_color: str) -> int:
    """
    Calculate mobility (number of legal moves) for a player.
    
    Args:
        game: Current game state
        player_color: "B" or "W"
        
    Returns:
        Number of legal moves
    """
    # Temporarily set turn to this player
    original_turn = game.turn
    game.turn = player_color
    
    legal_moves = game.get_move_list()
    mobility = len(legal_moves)
    
    # Restore original turn
    game.turn = original_turn
    
    return mobility


def calculate_stability(game: BitboardGame, player_color: str) -> int:
    """
    Calculate stability score (pieces that cannot be flipped).
    
    This is a simplified version - fully stable pieces are those
    that are in corners or completely surrounded.
    
    Args:
        game: Current game state
        player_color: "B" or "W"
        
    Returns:
        Stability score (0-64, approximate)
    """
    if player_color == "B":
        player_board = game.black
    else:
        player_board = game.white
    
    # Count corner pieces (always stable)
    stable_count = count_corners(player_board)
    
    # Count pieces that are surrounded on all sides (simplified heuristic)
    # A piece is "stable" if it's adjacent to stable pieces or corners
    # This is a simplified version - full stability calculation is complex
    
    # For now, we'll use a simple heuristic: pieces adjacent to corners
    # are more stable
    stable_mask = 0
    for corner_pos in CORNER_POSITIONS:
        if player_board & (1 << corner_pos):
            # Mark adjacent positions as potentially stable
            row = corner_pos // 8
            col = corner_pos % 8
            
            # Check all 8 directions
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row = row + dr
                    new_col = col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        pos = new_row * 8 + new_col
                        if player_board & (1 << pos):
                            stable_mask |= (1 << pos)
    
    # Count stable pieces (corners + adjacent to corners)
    stable_count = bin(player_board & (stable_mask | sum(1 << cp for cp in CORNER_POSITIONS))).count('1')
    
    return stable_count


def calculate_intermediate_reward(
    game: BitboardGame,
    player_color: str,
    previous_game_state: Optional[BitboardGame] = None,
    previous_player_color: Optional[str] = None
) -> float:
    """
    Calculate intermediate reward for a move.
    
    Rewards:
    - Corner capture: +0.1 per corner
    - Bad squares penalty: -0.05 per bad square
    - Mobility bonus: +0.01 per mobility advantage (relative)
    - Stability bonus: +0.005 per stable piece
    
    Args:
        game: Current game state (after move)
        player_color: "B" or "W" - player who just moved
        previous_game_state: Previous game state (before move) - optional
        previous_player_color: Previous player color - optional
        
    Returns:
        Intermediate reward value
    """
    reward = 0.0
    
    # Get player's bitboard
    if player_color == "B":
        player_board = game.black
        opponent_board = game.white
        opponent_color = "W"
    else:
        player_board = game.white
        opponent_board = game.black
        opponent_color = "B"
    
    # 1. Corner capture reward: +0.1 per corner
    player_corners = count_corners(player_board)
    opponent_corners = count_corners(opponent_board)
    
    # If we have previous state, calculate corner gain
    if previous_game_state is not None:
        if previous_player_color == player_color:
            # Previous state was also this player's turn (they just moved)
            if previous_player_color == "B":
                prev_player_board = previous_game_state.black
            else:
                prev_player_board = previous_game_state.white
            
            prev_corners = count_corners(prev_player_board)
            corner_gain = player_corners - prev_corners
            reward += corner_gain * 0.1
    else:
        # No previous state - use absolute corner count (scaled down)
        reward += player_corners * 0.01  # Smaller reward for absolute count
    
    # 2. Bad squares penalty: -0.05 per bad square
    player_bad_squares = count_bad_squares(player_board)
    opponent_bad_squares = count_bad_squares(opponent_board)
    
    # Penalty for having bad squares
    reward -= player_bad_squares * 0.05
    # Bonus if opponent has more bad squares
    reward += (opponent_bad_squares - player_bad_squares) * 0.02
    
    # 3. Mobility bonus: +0.01 per mobility advantage
    player_mobility = calculate_mobility(game, player_color)
    opponent_mobility = calculate_mobility(game, opponent_color)
    
    if player_mobility + opponent_mobility > 0:
        mobility_advantage = (player_mobility - opponent_mobility) / max(player_mobility + opponent_mobility, 1)
        reward += mobility_advantage * 0.01
    
    # 4. Stability bonus: +0.005 per stable piece
    player_stability = calculate_stability(game, player_color)
    opponent_stability = calculate_stability(game, opponent_color)
    
    stability_advantage = player_stability - opponent_stability
    reward += stability_advantage * 0.005
    
    return reward


def calculate_position_value(
    game: BitboardGame,
    player_color: str,
    final_outcome: float,
    intermediate_rewards: List[float],
    move_index: int
) -> float:
    """
    Calculate total value for a position combining final outcome and intermediate rewards.
    
    Args:
        game: Current game state
        player_color: "B" or "W"
        final_outcome: Final game outcome (+1 win, -1 loss, 0 draw)
        intermediate_rewards: List of intermediate rewards from this move onwards
        move_index: Index of this position in the game
        
    Returns:
        Total value (final outcome + discounted intermediate rewards)
    """
    # Start with final outcome
    value = final_outcome
    
    # Add discounted intermediate rewards from this position to the end
    # Use discount factor of 0.99 (slightly discount future intermediate rewards)
    discount = 0.99
    
    for i, intermediate_reward in enumerate(intermediate_rewards[move_index:], start=0):
        value += intermediate_reward * (discount ** i)
    
    return value

