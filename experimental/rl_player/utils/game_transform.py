"""
Game Transform Utilities

Functions to transform BitboardGame states according to symmetries.
Used for recalculating rewards on symmetries.
"""

import copy
from Reversi.BitboardGame import BitboardGame


def transform_bitboard(bitboard: int, transform_type: str) -> int:
    """
    Transform a bitboard according to a symmetry transformation.
    
    Args:
        bitboard: 64-bit integer representing board
        transform_type: One of 'rot90', 'rot180', 'rot270', 'flip_h', 'flip_v', 'flip_d1', 'flip_d2'
        
    Returns:
        Transformed bitboard
    """
    # Convert bitboard to 8x8 array
    board = [[0] * 8 for _ in range(8)]
    for i in range(64):
        if bitboard & (1 << i):
            row = i // 8
            col = i % 8
            board[row][col] = 1
    
    # Apply transformation
    if transform_type == 'rot90':
        board = [list(row) for row in zip(*board[::-1])]
    elif transform_type == 'rot180':
        board = [row[::-1] for row in board[::-1]]
    elif transform_type == 'rot270':
        board = [list(row) for row in zip(*board)][::-1]
    elif transform_type == 'flip_h':
        board = [row[::-1] for row in board]
    elif transform_type == 'flip_v':
        board = board[::-1]
    elif transform_type == 'flip_d1':  # Diagonal from top-left to bottom-right
        board = [list(row) for row in zip(*board)]
    elif transform_type == 'flip_d2':  # Diagonal from top-right to bottom-left
        board = [list(row) for row in zip(*[row[::-1] for row in board])][::-1]
    else:
        raise ValueError(f"Unknown transform_type: {transform_type}")
    
    # Convert back to bitboard
    result = 0
    for row in range(8):
        for col in range(8):
            if board[row][col]:
                pos = row * 8 + col
                result |= (1 << pos)
    
    return result


def transform_game(game: BitboardGame, transform_type: str) -> BitboardGame:
    """
    Transform a BitboardGame according to a symmetry transformation.
    
    Args:
        game: BitboardGame instance
        transform_type: One of 'rot90', 'rot180', 'rot270', 'flip_h', 'flip_v', 'flip_d1', 'flip_d2'
        
    Returns:
        New transformed BitboardGame instance
    """
    # Create a copy
    transformed = copy.deepcopy(game)
    
    # Transform both bitboards
    transformed.black = transform_bitboard(game.black, transform_type)
    transformed.white = transform_bitboard(game.white, transform_type)
    
    # Note: Turn doesn't change with symmetry (it's about whose turn it is, not board position)
    
    return transformed


def get_symmetry_transforms() -> list:
    """
    Get list of all D8 symmetry transformations.
    
    Returns:
        List of transform_type strings
    """
    return [
        'identity',  # Original (no transform)
        'rot90',
        'rot180',
        'rot270',
        'flip_h',
        'flip_h_rot90',  # flip_h then rot90
        'flip_h_rot180',  # flip_h then rot180
        'flip_h_rot270',  # flip_h then rot270
    ]


def apply_symmetry_transform(game: BitboardGame, transform_type: str) -> BitboardGame:
    """
    Apply a symmetry transformation to a game.
    
    Args:
        game: BitboardGame instance
        transform_type: One of the symmetry transforms from get_symmetry_transforms()
        
    Returns:
        New transformed BitboardGame instance
    """
    if transform_type == 'identity':
        return copy.deepcopy(game)
    elif transform_type == 'rot90':
        return transform_game(game, 'rot90')
    elif transform_type == 'rot180':
        return transform_game(game, 'rot180')
    elif transform_type == 'rot270':
        return transform_game(game, 'rot270')
    elif transform_type == 'flip_h':
        return transform_game(game, 'flip_h')
    elif transform_type == 'flip_h_rot90':
        transformed = transform_game(game, 'flip_h')
        return transform_game(transformed, 'rot90')
    elif transform_type == 'flip_h_rot180':
        transformed = transform_game(game, 'flip_h')
        return transform_game(transformed, 'rot180')
    elif transform_type == 'flip_h_rot270':
        transformed = transform_game(game, 'flip_h')
        return transform_game(transformed, 'rot270')
    else:
        raise ValueError(f"Unknown transform_type: {transform_type}")

