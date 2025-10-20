"""
Test positions for characterization testing.

Standard positions used throughout Reversi testing.
"""

from src.Reversi.BitboardGame import BitboardGame


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
        game = game.make_move(37)  # F5 (position 37)
        return game
    
    @staticmethod
    def early_midgame():
        """Early midgame position - move 10"""
        game = BitboardGame()
        # Play a standard opening sequence
        moves = [37, 38, 29, 36, 21, 26, 19, 20, 30, 22]  # F5, f6, E5, f4, E3, d6, C5, d3, e6, c6
        for move in moves:
            if move in game.get_valid_moves(game.current_player):
                game = game.make_move(move)
        return game
    
    @staticmethod
    def midgame_tactical():
        """Midgame with tactical opportunities"""
        game = BitboardGame()
        # Sequence that creates tactical position
        moves = [37, 26, 19, 30, 38, 36, 31, 35, 39, 22, 23, 24, 20, 21]  # F5, d6, C5, e6, F6, f4, E7, f3, G5, c6, C7, d7, D3, e3
        for move in moves:
            if move in game.get_valid_moves(game.current_player):
                game = game.make_move(move)
        return game
    
    @staticmethod
    def late_midgame():
        """Late midgame - ~40 pieces on board"""
        game = BitboardGame()
        # Extended sequence
        moves = [37, 26, 19, 30, 38, 36, 31, 35, 39, 22, 23, 24, 20, 21, 40, 41, 18, 25, 17, 10, 28, 11, 12, 9, 8, 13, 14, 43]
        for move in moves:
            if move in game.get_valid_moves(game.current_player):
                game = game.make_move(move)
        return game
    
    @staticmethod
    def endgame():
        """Endgame position - few empty squares"""
        game = BitboardGame()
        # Long sequence to reach endgame
        moves = [37, 26, 19, 30, 38, 36, 31, 35, 39, 22, 23, 24, 20, 21, 40, 41, 18, 25, 17, 10, 28, 11, 12, 9, 8, 13, 14, 43, 44, 45, 42, 46, 15, 6, 1, 2, 47, 48, 3, 4]
        for move in moves:
            if move in game.get_valid_moves(game.current_player):
                game = game.make_move(move)
        return game
    
    @staticmethod
    def corner_capture():
        """Position where corner can be captured"""
        game = BitboardGame()
        # Sequence leading to corner opportunity
        moves = [37, 26, 19, 30, 38, 36, 39, 40, 48, 47, 44, 35]
        for move in moves:
            if move in game.get_valid_moves(game.current_player):
                game = game.make_move(move)
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

