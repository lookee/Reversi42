#------------------------------------------------------------------------
#    Copyright (C) 2025 Luca Amore <luca.amore at gmail.com>
#    Bitboard Implementation for Maximum Performance
#
#    This is a high-performance bitboard implementation of Reversi
#    Expected speedup: 50-100x faster than array-based implementation
#------------------------------------------------------------------------

from Reversi.Game import Move

class BitboardGame:
    """
    Ultra-fast bitboard implementation of Reversi.
    
    Uses 64-bit integers to represent board state:
    - Each bit represents a square (0-63)
    - Bit operations for move generation and validation
    - O(1) copy and undo operations
    """
    
    # Pre-computed masks and shift tables
    # Directions: N, NE, E, SE, S, SW, W, NW
    DIRECTIONS = [
        (-8, 0x00FFFFFFFFFFFFFF),  # North
        (-7, 0x007F7F7F7F7F7F7F),  # NE
        (1,  0x7F7F7F7F7F7F7F7F),  # East
        (9,  0x7F7F7F7F7F7F7F00),  # SE
        (8,  0xFFFFFFFFFFFFFF00),  # South
        (7,  0xFEFEFEFEFEFEFE00),  # SW
        (-1, 0xFEFEFEFEFEFEFEFE),  # West
        (-9, 0x00FEFEFEFEFEFEFE),  # NW
    ]
    
    @classmethod
    def create_empty(cls):
        """Create an empty BitboardGame without initializing to starting position"""
        instance = cls.__new__(cls)
        instance.size = 8
        instance.cells_cnt = 64
        instance.black = 0
        instance.white = 0
        instance.turn = 'B'
        instance.turn_cnt = 0
        instance.history = ""
        instance.move_stack = []
        instance.black_cnt = 0
        instance.white_cnt = 0
        instance.limit = 9
        instance.corner = ((1, 2), (8, 7))
        instance.matrix = [['.' for _ in range(10)] for _ in range(10)]
        return instance
    
    def __init__(self):
        """Initialize with standard starting position"""
        self.size = 8
        self.cells_cnt = 64
        
        # Bitboards for each player
        # Standard start: d4, e5 = white; d5, e4 = black
        # Position 27 (d4), 36 (e5) = white
        # Position 28 (d5), 35 (e4) = black
        self.black = 0x0000000810000000  # Bits 35, 28
        self.white = 0x0000001008000000  # Bits 36, 27
        
        # Game state
        self.turn = 'B'
        self.turn_cnt = 0
        self.history = ""
        
        # Move history for undo
        self.move_stack = []
        
        # Piece counts (calculated from bitboards)
        self.black_cnt = self._count_bits(self.black)
        self.white_cnt = self._count_bits(self.white)
        
        # Compatibility attributes for evaluators
        self.limit = self.size + 1
        self.corner = ((1, 2), (self.size, self.size - 1))
        
        # Create virtual matrix for evaluator compatibility
        self._create_virtual_matrix()
    
    def _create_virtual_matrix(self):
        """Create matrix representation from bitboards (for evaluator compatibility)"""
        # Create 10x10 matrix with borders (like original Game)
        self.matrix = [['.' for _ in range(10)] for _ in range(10)]
        
        # Fill borders with '.'
        # Fill actual board from bitboards
        for bit in range(64):
            row = bit // 8
            col = bit % 8
            mask = 1 << bit
            
            # Matrix uses 1-indexed with borders, so offset by 1
            if self.black & mask:
                self.matrix[row + 1][col + 1] = 'B'
            elif self.white & mask:
                self.matrix[row + 1][col + 1] = 'W'
            else:
                self.matrix[row + 1][col + 1] = '.'
    
    @staticmethod
    def _count_bits(n):
        """Count number of set bits (population count)"""
        count = 0
        while n:
            count += 1
            n &= n - 1  # Clear lowest bit
        return count
    
    @staticmethod
    def _coord_to_bit(x, y):
        """Convert (x,y) coordinates to bit position (0-63)"""
        # x,y are 1-indexed (1-8)
        col = x - 1  # 0-7
        row = y - 1  # 0-7
        return row * 8 + col
    
    @staticmethod
    def _bit_to_coord(bit):
        """Convert bit position to (x,y) coordinates"""
        row = bit // 8
        col = bit % 8
        return (col + 1, row + 1)  # 1-indexed
    
    def get_turn(self):
        """Get current player"""
        return self.turn
    
    def switch_player(self):
        """Switch turn"""
        self.turn = 'W' if self.turn == 'B' else 'B'
    
    def _get_player_boards(self):
        """Get (player, opponent) bitboards for current turn"""
        if self.turn == 'B':
            return self.black, self.white
        else:
            return self.white, self.black
    
    def _shift(self, board, direction, mask):
        """Shift bitboard in a direction with edge wrapping prevention"""
        shift_amount, edge_mask = direction
        if shift_amount > 0:
            return (board << shift_amount) & edge_mask
        else:
            return (board >> -shift_amount) & edge_mask
    
    def get_valid_moves(self):
        """
        Generate all valid moves using shift and mask algorithm.
        The mask must be applied to the source BEFORE shifting to prevent wrap-around.
        """
        player, opponent = self._get_player_boards()
        empty = ~(player | opponent) & 0xFFFFFFFFFFFFFFFF
        
        valid_moves = 0
        
        # For each of the 8 directions
        for shift_amount, edge_mask in self.DIRECTIONS:
            # Find opponent pieces next to our pieces in this direction
            # IMPORTANT: Apply mask BEFORE shift to prevent edge wrap
            if shift_amount > 0:
                flip_candidates = opponent & ((player & edge_mask) << shift_amount)
            else:
                flip_candidates = opponent & ((player & edge_mask) >> -shift_amount)
            
            # Propagate through consecutive opponent pieces
            for _ in range(5):  # Max 6 opponents in a row
                if shift_amount > 0:
                    flip_candidates |= opponent & ((flip_candidates & edge_mask) << shift_amount)
                else:
                    flip_candidates |= opponent & ((flip_candidates & edge_mask) >> -shift_amount)
            
            # Valid moves are empty squares one step beyond the flip line
            if shift_amount > 0:
                valid_moves |= empty & ((flip_candidates & edge_mask) << shift_amount)
            else:
                valid_moves |= empty & ((flip_candidates & edge_mask) >> -shift_amount)
        
        return valid_moves
    
    def get_move_list(self):
        """Convert bitboard of valid moves to Move objects"""
        valid_moves = self.get_valid_moves()
        moves = []
        
        bit = 0
        while valid_moves:
            if valid_moves & 1:
                x, y = self._bit_to_coord(bit)
                moves.append(Move(x, y))
            valid_moves >>= 1
            bit += 1
        
        return moves
    
    def valid_move(self, move):
        """Check if a move is valid"""
        bit = self._coord_to_bit(move.x, move.y)
        valid_moves = self.get_valid_moves()
        return (valid_moves >> bit) & 1 == 1
    
    def move(self, move):
        """Make a move on the bitboard"""
        bit = self._coord_to_bit(move.x, move.y)
        player, opponent = self._get_player_boards()
        
        # Save state for undo
        self.move_stack.append((self.black, self.white, self.turn, self.history))
        
        # Calculate flips
        flips = 0
        move_bit = 1 << bit
        
        for direction in self.DIRECTIONS:
            flip_line = 0
            test = self._shift(move_bit, direction, direction[1])
            
            # Scan through opponent pieces
            while test and (test & opponent):
                flip_line |= test
                test = self._shift(test, direction, direction[1])
            
            # Valid if ended on player piece
            if test & player:
                flips |= flip_line
        
        # Apply move and flips
        if self.turn == 'B':
            self.black |= move_bit | flips
            self.white &= ~flips
            self.history += str(move).upper()
        else:
            self.white |= move_bit | flips
            self.black &= ~flips
            self.history += str(move).lower()
        
        # Update counts
        self.black_cnt = self._count_bits(self.black)
        self.white_cnt = self._count_bits(self.white)
        
        self.turn_cnt += 1
        self.switch_player()
        
        # Update virtual matrix for evaluator compatibility
        self._create_virtual_matrix()
    
    def undo_move(self):
        """Undo last move - O(1) operation!"""
        if not self.move_stack:
            return
        
        self.black, self.white, self.turn, self.history = self.move_stack.pop()
        self.black_cnt = self._count_bits(self.black)
        self.white_cnt = self._count_bits(self.white)
        self.turn_cnt -= 1
        
        # Update virtual matrix
        self._create_virtual_matrix()
    
    def pass_turn(self):
        """Pass turn when no moves available"""
        self.move_stack.append((self.black, self.white, self.turn, self.history))
        self.switch_player()
        self.turn_cnt += 1
    
    def is_finish(self):
        """Check if game is over"""
        # Game over if board is full
        if self.black_cnt + self.white_cnt == 64:
            return True
        
        # Or if neither player has moves
        player, opponent = self._get_player_boards()
        if self.get_valid_moves() == 0:
            # Switch and check opponent
            self.switch_player()
            opp_moves = self.get_valid_moves()
            self.switch_player()
            return opp_moves == 0
        
        return False
    
    def check_win(self):
        """Check if current player has won"""
        if not self.is_finish():
            return False
        return (self.black_cnt > self.white_cnt and self.turn == 'B') or \
               (self.white_cnt > self.black_cnt and self.turn == 'W')
    
    def check_lost(self):
        """Check if current player has lost"""
        if not self.is_finish():
            return False
        return (self.black_cnt < self.white_cnt and self.turn == 'B') or \
               (self.white_cnt < self.black_cnt and self.turn == 'W')
    
    def export_str(self):
        """Export board state as string (for compatibility)"""
        result = []
        for row in range(8):
            line = []
            for col in range(8):
                bit = row * 8 + col
                mask = 1 << bit
                if self.black & mask:
                    line.append('B')
                elif self.white & mask:
                    line.append('W')
                else:
                    line.append('.')
            result.append(''.join(line))
        return '\n'.join(result)
    
    def view(self):
        """Print board to console with elegant compact layout"""
        print()
        
        # Compact header
        print("─" * 40)
        print("  Turn: %-2s   ●:%2d  ○:%2d   Move:%2d" % (
            self.turn, self.black_cnt, self.white_cnt, self.turn_cnt
        ))
        print("─" * 40)
        print()
        
        # Compact column headers
        print("    A B C D E F G H")
        
        # Top border
        print("  ┌" + "─" * 15 + "┐")
        
        # Board rows
        for row in range(8):
            print(f"{row + 1} │", end='')
            for col in range(8):
                bit = row * 8 + col
                mask = 1 << bit
                if self.black & mask:
                    print('●', end='')
                elif self.white & mask:
                    print('○', end='')
                else:
                    print('·', end='')
                
                # Space between cells except at the end
                if col < 7:
                    print(' ', end='')
            
            print(f"│ {row + 1}")
        
        # Bottom border
        print("  └" + "─" * 15 + "┘")
        
        # Column headers at bottom
        print("    A B C D E F G H")
        print()
    
    def get_zobrist_hash(self):
        """Get Zobrist hash for transposition table (to be implemented)"""
        # For now, use simple hash
        return hash((self.black, self.white, self.turn))
    
    def clone(self):
        """Create a copy of the game state - O(1) with bitboards!"""
        new_game = BitboardGame()
        new_game.black = self.black
        new_game.white = self.white
        new_game.turn = self.turn
        new_game.turn_cnt = self.turn_cnt
        new_game.black_cnt = self.black_cnt
        new_game.white_cnt = self.white_cnt
        new_game.history = self.history
        new_game.move_stack = self.move_stack.copy()
        return new_game
    
    def get_result(self):
        """Get game result as string (for compatibility)"""
        out = ""
        out += f"\nblack: {self.black_cnt} white: {self.white_cnt}\n"
        
        if self.black_cnt > self.white_cnt:
            out += f"the winner is black: +{self.black_cnt - self.white_cnt}"
        elif self.white_cnt > self.black_cnt:
            out += f"the winner is white: +{self.white_cnt - self.black_cnt}"
        else:
            out += "the game is drawn!"
        
        return out
    
    def result(self):
        """Print game result"""
        print(self.get_result())

