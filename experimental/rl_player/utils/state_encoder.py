"""
State Encoder for Reversi

Converts BitboardGame state to PyTorch tensor with advanced feature channels.

Channels:
- 0: Black pieces
- 1: White pieces
- 2: Legal moves mask
- 3: Mobility count (for each position)
- 4: Corner positions
- 5: Edge positions
- 6: Turn indicator
- 7: Opening book moves (NEW)
"""

import numpy as np
import torch
from typing import Optional

# Import BitboardGame from main codebase (minimal dependency)
import sys
import os

# Add src to path to import BitboardGame
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move

# Lazy import opening book (only when needed)
_opening_book = None


def get_opening_book():
    """Get or create opening book instance (lazy loading)."""
    global _opening_book
    if _opening_book is None:
        try:
            from domain.knowledge import get_default_opening_book
            _opening_book = get_default_opening_book()
        except ImportError:
            # Opening book not available, return None
            _opening_book = None
    return _opening_book


# Corner positions: A1, H1, A8, H8
CORNER_POSITIONS = [0, 7, 56, 63]  # Bit positions for corners

# Edge positions (excluding corners)
EDGE_MASK = 0x8181818181818181  # Left and right edges
EDGE_MASK |= 0x00000000000000FF  # Top edge
EDGE_MASK |= 0xFF00000000000000  # Bottom edge
# Remove corners
EDGE_MASK &= ~(1 << 0) & ~(1 << 7) & ~(1 << 56) & ~(1 << 63)
EDGE_MASK &= 0xFFFFFFFFFFFFFFFF


def bitboard_to_array(bitboard: int, size: int = 8) -> np.ndarray:
    """
    Convert bitboard (64-bit integer) to numpy array.
    
    Args:
        bitboard: 64-bit integer representing board
        size: Board size (default 8)
        
    Returns:
        8x8 numpy array with 1.0 where bit is set, 0.0 otherwise
    """
    array = np.zeros((size, size), dtype=np.float32)
    for i in range(size * size):
        if bitboard & (1 << i):
            row = i // size
            col = i % size
            array[row, col] = 1.0
    return array


def count_mobility_at_position(game: BitboardGame, position: int, player_color: str) -> int:
    """
    Count mobility (number of pieces that would be flipped) if a piece is placed at position.
    
    This counts how many opponent pieces would be flipped, which correlates with mobility.
    
    Args:
        game: Current game state
        position: Position to check (0-63)
        player_color: "B" or "W"
        
    Returns:
        Mobility count (0-64) - normalized count of flippable pieces
    """
    # Get current player's bitboard
    if player_color == "B":
        player_board = game.black
        opponent_board = game.white
    else:
        player_board = game.white
        opponent_board = game.black
    
    # Check if position is empty
    if (player_board | opponent_board) & (1 << position):
        return 0  # Position is not empty
    
    # Count flips in all directions
    mobility = 0
    position_bit = 1 << position
    
    for shift_amount, edge_mask in BitboardGame.DIRECTIONS:
        # Check if we can flip pieces in this direction
        if shift_amount > 0:
            check_pos = (position_bit & edge_mask) << shift_amount
        else:
            check_pos = (position_bit & edge_mask) >> -shift_amount
        
        # Count consecutive opponent pieces
        count = 0
        temp_pos = check_pos
        
        while temp_pos & opponent_board & edge_mask:
            count += 1
            if shift_amount > 0:
                temp_pos = (temp_pos & edge_mask) << shift_amount
            else:
                temp_pos = (temp_pos & edge_mask) >> -shift_amount
        
        # If we hit our own piece, add to mobility
        if temp_pos & player_board & edge_mask:
            mobility += count
    
    return min(mobility, 64)  # Cap at 64


def encode_state(
    game: BitboardGame,
    player_color: str,
    use_advanced_features: bool = True,
    use_opening_book: bool = True,
    device: Optional[torch.device] = None
) -> torch.Tensor:
    """
    Encode BitboardGame state to PyTorch tensor.
    
    Args:
        game: BitboardGame instance
        player_color: "B" (black) or "W" (white) - current player's perspective
        use_advanced_features: If True, includes advanced feature channels
        use_opening_book: If True, includes opening book channel (requires advanced features)
        device: PyTorch device (if None, uses CPU)
        
    Returns:
        Tensor of shape [channels, 8, 8]
        - Channels: 2 (basic), 7 (advanced), or 8 (advanced + opening book)
    """
    if device is None:
        device = torch.device("cpu")
    
    # Channel 0: Black pieces
    black_array = bitboard_to_array(game.black)
    
    # Channel 1: White pieces
    white_array = bitboard_to_array(game.white)
    
    channels = [black_array, white_array]
    
    if use_advanced_features:
        # Channel 2: Legal moves mask
        legal_moves_bitboard = game.get_valid_moves()
        legal_moves_array = bitboard_to_array(legal_moves_bitboard)
        channels.append(legal_moves_array)
        
        # Channel 3: Mobility count (for each position)
        mobility_array = np.zeros((8, 8), dtype=np.float32)
        for i in range(64):
            row = i // 8
            col = i % 8
            # Only calculate mobility for empty squares
            if not (game.black & (1 << i)) and not (game.white & (1 << i)):
                mobility = count_mobility_at_position(game, i, player_color)
                # Normalize to [0, 1]
                mobility_array[row, col] = mobility / 64.0
        channels.append(mobility_array)
        
        # Channel 4: Corner positions
        corner_array = np.zeros((8, 8), dtype=np.float32)
        for pos in CORNER_POSITIONS:
            row = pos // 8
            col = pos % 8
            corner_array[row, col] = 1.0
        channels.append(corner_array)
        
        # Channel 5: Edge positions (excluding corners)
        edge_array = np.zeros((8, 8), dtype=np.float32)
        for i in range(64):
            if EDGE_MASK & (1 << i):
                row = i // 8
                col = i % 8
                edge_array[row, col] = 1.0
        channels.append(edge_array)
        
        # Channel 6: Turn indicator
        turn_array = np.ones((8, 8), dtype=np.float32) if game.turn == player_color else np.zeros((8, 8), dtype=np.float32)
        channels.append(turn_array)
        
        # Channel 7: Opening book moves
        if use_opening_book:
            book_array = np.zeros((8, 8), dtype=np.float32)
            opening_book = get_opening_book()
            
            if opening_book is not None:
                # Get game history from BitboardGame
                game_history = game.history if hasattr(game, 'history') else ""
                
                # Check if current position is in book
                if opening_book.is_in_book(game_history):
                    # Get book moves for current position
                    book_moves = opening_book.get_book_moves(game_history)
                    
                    # Mark book moves on the board
                    for move in book_moves:
                        # Move object has x, y coordinates (1-based)
                        # Convert to 0-based indices
                        row = move.get_y() - 1
                        col = move.get_x() - 1
                        
                        if 0 <= row < 8 and 0 <= col < 8:
                            book_array[row, col] = 1.0
            
            channels.append(book_array)
    
    # Stack channels: [channels, 8, 8]
    state = np.stack(channels, axis=0)
    
    # Convert to tensor
    tensor = torch.from_numpy(state).float().to(device)
    
    return tensor


def encode_batch(
    games: list,
    player_colors: list,
    use_advanced_features: bool = True,
    use_opening_book: bool = True,
    device: Optional[torch.device] = None
) -> torch.Tensor:
    """
    Encode a batch of game states.
    
    Args:
        games: List of BitboardGame instances
        player_colors: List of player colors ("B" or "W")
        use_advanced_features: If True, includes advanced features
        use_opening_book: If True, includes opening book channel
        device: PyTorch device
        
    Returns:
        Tensor of shape [batch_size, channels, 8, 8]
    """
    encoded_states = []
    for game, player_color in zip(games, player_colors):
        state = encode_state(game, player_color, use_advanced_features, use_opening_book, device)
        encoded_states.append(state)
    
    return torch.stack(encoded_states, dim=0)

