"""
ASCII Board Renderer - Common Board Rendering Utilities

Provides consistent ASCII art board rendering for terminal/console output.
Shared by Game.get_view() and TerminalBoardView for consistency.

Version: 3.1.0
Architecture: Shared utility in ui/utils/
"""


class ASCIIBoardRenderer:
    """
    Common ASCII art board renderer.
    
    Provides two styles:
    - COMPACT: Simple format without cell separators
    - DETAILED: Full format with cell separators and grid lines
    """
    
    # Piece symbols
    BLACK_PIECE = '●'
    WHITE_PIECE = '○'
    EMPTY = '·'
    
    # Box drawing characters
    BOX_H = '─'
    BOX_V = '│'
    BOX_TL = '┌'
    BOX_TR = '┐'
    BOX_BL = '└'
    BOX_BR = '┘'
    BOX_CROSS = '┼'
    BOX_T_DOWN = '┬'
    BOX_T_UP = '┴'
    BOX_T_RIGHT = '├'
    BOX_T_LEFT = '┤'
    
    @classmethod
    def render_header(cls, turn, black_count, white_count, move_count, style='compact'):
        """
        Render consistent header for board display.
        
        Args:
            turn: Current turn ('B' or 'W')
            black_count: Black pieces count
            white_count: White pieces count
            move_count: Current move number
            style: 'compact' or 'detailed'
            
        Returns:
            str: Formatted header
        """
        turn_symbol = cls.BLACK_PIECE if turn == 'B' else cls.WHITE_PIECE
        
        lines = []
        lines.append(cls.BOX_H * 40)
        lines.append(f"  Turn: {turn_symbol}  |   {cls.BLACK_PIECE}:{black_count:>2}  " +
                    f"{cls.WHITE_PIECE}:{white_count:>2}  |  Move:{move_count}")
        lines.append(cls.BOX_H * 40)
        
        return '\n'.join(lines)
    
    @classmethod
    def render_board_compact(cls, board_matrix, size=8):
        """
        Render board in compact format (no cell separators).
        
        Args:
            board_matrix: 2D array or string of board state
            size: Board size (default 8)
            
        Returns:
            str: Formatted board
        """
        lines = []
        
        # Column headers
        col_header = "   " + " ".join("ABCDEFGH"[:size])
        lines.append(col_header)
        
        # Top border
        lines.append("  " + cls.BOX_TL + cls.BOX_H * (size * 2 - 1) + cls.BOX_TR)
        
        # Board rows
        for y in range(size):
            row = f"{y + 1} {cls.BOX_V}"
            for x in range(size):
                # Get piece
                if isinstance(board_matrix, str):
                    idx = y * size + x
                    cell = board_matrix[idx] if idx < len(board_matrix) else '.'
                else:
                    cell = board_matrix[y][x] if y < len(board_matrix) and x < len(board_matrix[y]) else '.'
                
                # Convert to symbol
                if cell in ['B', 'b']:
                    piece = cls.BLACK_PIECE
                elif cell in ['W', 'w']:
                    piece = cls.WHITE_PIECE
                else:
                    piece = cls.EMPTY
                
                row += piece
                if x < size - 1:
                    row += ' '
            
            row += f"{cls.BOX_V} {y + 1}"
            lines.append(row)
        
        # Bottom border
        lines.append("  " + cls.BOX_BL + cls.BOX_H * (size * 2 - 1) + cls.BOX_BR)
        
        # Column headers bottom
        lines.append(col_header)
        
        return '\n'.join(lines)
    
    @classmethod
    def render_board_detailed(cls, board_matrix, size=8, valid_moves=None, last_move=None, cursor_pos=None):
        """
        Render board in detailed format (with cell separators and grid lines).
        
        Args:
            board_matrix: 2D array of board state
            size: Board size (default 8)
            valid_moves: List of (x, y) tuples for valid moves
            last_move: Tuple (x, y) for last move
            cursor_pos: Tuple (x, y) for cursor position
            
        Returns:
            str: Formatted board with grid
        """
        if valid_moves is None:
            valid_moves = []
        
        lines = []
        
        # Column headers
        col_header = "    " + "   ".join("ABCDEFGH"[:size])
        lines.append(col_header)
        
        # Top border
        top_line = "  " + cls.BOX_TL
        for x in range(size):
            top_line += cls.BOX_H * 3
            if x < size - 1:
                top_line += cls.BOX_T_DOWN
        top_line += cls.BOX_TR
        lines.append(top_line)
        
        # Board rows
        for y in range(size):
            row = f"{y + 1} {cls.BOX_V}"
            
            for x in range(size):
                # Get piece
                cell = board_matrix[y][x] if y < len(board_matrix) and x < len(board_matrix[y]) else ' '
                
                # Convert to symbol
                if cell in ['B', 'b']:
                    piece = cls.BLACK_PIECE
                elif cell in ['W', 'w']:
                    piece = cls.WHITE_PIECE
                elif (x, y) in valid_moves:
                    piece = '*'  # Valid move marker
                else:
                    piece = cls.EMPTY
                
                row += f" {piece} {cls.BOX_V}"
            
            lines.append(row)
            
            # Add separator between rows (except after last row)
            if y < size - 1:
                sep_line = "  " + cls.BOX_T_RIGHT
                for x in range(size):
                    sep_line += cls.BOX_H * 3
                    if x < size - 1:
                        sep_line += cls.BOX_CROSS
                sep_line += cls.BOX_T_LEFT
                lines.append(sep_line)
        
        # Bottom border
        bottom_line = "  " + cls.BOX_BL
        for x in range(size):
            bottom_line += cls.BOX_H * 3
            if x < size - 1:
                bottom_line += cls.BOX_T_UP
        bottom_line += cls.BOX_BR
        lines.append(bottom_line)
        
        return '\n'.join(lines)

