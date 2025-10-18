"""
Board Model - Pure Domain Logic

Represents the board state without any UI dependencies.
Framework-agnostic, easily testable.

Architecture: Model in MVC pattern
Version: 3.1.0
"""

from typing import List


class BoardModel:
    """
    Board model - pure domain logic.
    
    Responsibilities:
    - Store board state
    - Provide state access
    - NO rendering
    - NO input handling
    - NO UI logic
    
    State representation:
    - 'B' or 'X' = Black piece
    - 'W' or 'O' = White piece
    - 0 or ' ' = Empty
    - 'b' = Valid move for black
    - 'w' = Valid move for white
    """
    
    def __init__(self, sizex: int, sizey: int):
        """
        Initialize board model.
        
        Args:
            sizex: Board width
            sizey: Board height
        """
        self.sizex = sizex
        self.sizey = sizey
        self.matrix = [[0 for row in range(self.sizey)] for col in range(self.sizex)]
    
    def setPoint(self, x: int, y: int, value):
        """
        Set cell value.
        
        Args:
            x: Column (0-indexed)
            y: Row (0-indexed)
            value: Cell value ('B', 'W', 0, 'b', 'w', etc.)
        """
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            self.matrix[x][y] = value
    
    def unsetPoint(self, x: int, y: int):
        """Clear cell"""
        self.setPoint(x, y, 0)
    
    def getPoint(self, x: int, y: int):
        """
        Get cell value.
        
        Args:
            x: Column (0-indexed)
            y: Row (0-indexed)
            
        Returns:
            Cell value
        """
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            return self.matrix[x][y]
        return None
    
    def to_2d_array(self) -> List[List[str]]:
        """
        Convert model to 2D array for rendering.
        
        Returns:
            2D list of cell values
        """
        return [[self.matrix[x][y] for x in range(self.sizex)] 
                for y in range(self.sizey)]
    
    def clear(self):
        """Clear entire board"""
        self.matrix = [[0 for row in range(self.sizey)] for col in range(self.sizex)]

