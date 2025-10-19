"""
Test positions for characterization testing.

Standard positions used throughout Reversi testing.
"""

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


class TestPositions:
    """Collection of standard test positions"""
    
    @staticmethod
    def initial_position():
        """Standard opening position"""
        game = BitboardGame()
        return game
    
    @staticmethod
    def after_first_move():
        """Position after F5"""
        game = BitboardGame()
        game.move(Move(6, 5))  # F5
        return game
    
    @staticmethod
    def early_midgame():
        """Early midgame position - move 10"""
        game = BitboardGame()
        # Play a standard opening sequence
        moves = [
            Move(6, 5),  # F5
            Move(6, 6),  # f6
            Move(5, 5),  # E5
            Move(6, 4),  # f4
            Move(5, 3),  # E3
            Move(4, 6),  # d6
            Move(3, 5),  # C5
            Move(4, 3),  # d3
            Move(5, 6),  # e6
            Move(3, 6),  # c6
        ]
        for move in moves:
            if game.valid_move(move):
                game.move(move)
        return game
    
    @staticmethod
    def midgame_tactical():
        """Midgame with tactical opportunities"""
        game = BitboardGame()
        # Sequence that creates tactical position
        moves = [
            Move(6, 5),  # F5
            Move(4, 6),  # d6
            Move(3, 5),  # C5
            Move(5, 6),  # e6
            Move(6, 6),  # F6
            Move(6, 4),  # f4
            Move(5, 7),  # E7
            Move(6, 3),  # f3
            Move(7, 5),  # G5
            Move(3, 6),  # c6
            Move(3, 7),  # C7
            Move(4, 7),  # d7
            Move(4, 3),  # D3
            Move(5, 3),  # e3
        ]
        for move in moves:
            if game.valid_move(move):
                game.move(move)
        return game
    
    @staticmethod
    def late_midgame():
        """Late midgame - ~40 pieces on board"""
        game = BitboardGame()
        # Extended sequence
        moves = [
            Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6),
            Move(6, 6), Move(6, 4), Move(5, 7), Move(6, 3),
            Move(7, 5), Move(3, 6), Move(3, 7), Move(4, 7),
            Move(4, 3), Move(5, 3), Move(6, 7), Move(7, 6),
            Move(3, 4), Move(4, 5), Move(3, 3), Move(2, 4),
            Move(5, 4), Move(2, 5), Move(2, 6), Move(2, 3),
            Move(4, 2), Move(5, 2), Move(6, 2), Move(7, 3),
        ]
        for move in moves:
            if game.valid_move(move):
                game.move(move)
        return game
    
    @staticmethod
    def endgame():
        """Endgame position - few empty squares"""
        game = BitboardGame()
        # Long sequence to reach endgame
        moves = [
            Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6),
            Move(6, 6), Move(6, 4), Move(5, 7), Move(6, 3),
            Move(7, 5), Move(3, 6), Move(3, 7), Move(4, 7),
            Move(4, 3), Move(5, 3), Move(6, 7), Move(7, 6),
            Move(3, 4), Move(4, 5), Move(3, 3), Move(2, 4),
            Move(5, 4), Move(2, 5), Move(2, 6), Move(2, 3),
            Move(4, 2), Move(5, 2), Move(6, 2), Move(7, 3),
            Move(7, 4), Move(8, 5), Move(7, 2), Move(8, 3),
            Move(3, 2), Move(2, 2), Move(1, 3), Move(1, 4),
            Move(8, 4), Move(8, 6), Move(1, 5), Move(1, 6),
        ]
        for move in moves:
            if game.valid_move(move):
                game.move(move)
        return game
    
    @staticmethod
    def corner_capture():
        """Position where corner can be captured"""
        game = BitboardGame()
        # Sequence leading to corner opportunity
        moves = [
            Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6),
            Move(6, 6), Move(6, 4), Move(7, 5), Move(7, 6),
            Move(8, 6), Move(8, 5), Move(7, 4), Move(6, 3),
        ]
        for move in moves:
            if game.valid_move(move):
                game.move(move)
        return game
    
    @staticmethod
    def all_positions():
        """Get all test positions"""
        return {
            'initial': TestPositions.initial_position(),
            'after_first': TestPositions.after_first_move(),
            'early_midgame': TestPositions.early_midgame(),
            'midgame_tactical': TestPositions.midgame_tactical(),
            'late_midgame': TestPositions.late_midgame(),
            'endgame': TestPositions.endgame(),
            'corner_capture': TestPositions.corner_capture(),
        }

