"""
Zobrist hashing for position caching.

Provides fast, collision-resistant hashing of board positions
for transposition table lookups.
"""

import random


class ZobristHasher:
    """
    Zobrist hashing implementation for Reversi positions.

    Uses random 64-bit numbers to create unique position hashes.
    Hash updates are incremental (XOR operations) for speed.
    """

    def __init__(self, seed=42):
        """
        Initialize Zobrist hash tables.

        Args:
            seed: Random seed for reproducibility
        """
        random.seed(seed)

        # Hash values for each (square, color) combination
        # 64 squares x 2 colors = 128 values
        self.piece_hashes = {}

        for square in range(64):
            self.piece_hashes[(square, "B")] = random.getrandbits(64)
            self.piece_hashes[(square, "W")] = random.getrandbits(64)

        # Hash value for side to move
        self.side_hash = random.getrandbits(64)

    def hash_position(self, game) -> int:
        """
        Compute Zobrist hash for a position.

        Args:
            game: BitboardGame instance

        Returns:
            int: 64-bit hash value
        """
        h = 0

        # Hash black pieces
        black = game.black
        for square in range(64):
            if black & (1 << square):
                h ^= self.piece_hashes[(square, "B")]

        # Hash white pieces
        white = game.white
        for square in range(64):
            if white & (1 << square):
                h ^= self.piece_hashes[(square, "W")]

        # Hash side to move
        if game.turn == "W":
            h ^= self.side_hash

        return h

    def update_hash(self, current_hash: int, move, flipped_positions: list, color: str) -> int:
        """
        Update hash incrementally after a move.

        This is much faster than recomputing from scratch.

        Args:
            current_hash: Current position hash
            move: Move that was made
            flipped_positions: List of positions that were flipped
            color: Color that made the move ('B' or 'W')

        Returns:
            int: Updated hash value
        """
        h = current_hash

        # XOR out old side to move, XOR in new side
        h ^= self.side_hash

        # Add piece at move position
        move_square = (move.y - 1) * 8 + (move.x - 1)
        h ^= self.piece_hashes[(move_square, color)]

        # Flip pieces
        opponent = "W" if color == "B" else "B"
        for pos in flipped_positions:
            # XOR out opponent piece
            h ^= self.piece_hashes[(pos, opponent)]
            # XOR in our piece
            h ^= self.piece_hashes[(pos, color)]

        return h
