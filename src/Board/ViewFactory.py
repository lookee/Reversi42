"""
ViewFactory - Factory for Creating Board Views

Simplifies view creation with sensible defaults.

Version: 3.1.0
"""

from .PygameBoardView import PygameBoardView
from .TerminalBoardView import TerminalBoardView
from .HeadlessBoardView import HeadlessBoardView


class ViewFactory:
    """
    Factory for creating different view types.
    
    Makes it easy to switch between view implementations.
    """
    
    # Registry of available views
    VIEW_TYPES = {
        'pygame': PygameBoardView,
        'terminal': TerminalBoardView,
        'headless': HeadlessBoardView,
        'gui': PygameBoardView,  # Alias
        'console': TerminalBoardView,  # Alias
        'none': HeadlessBoardView,  # Alias
    }
    
    @classmethod
    def create_view(cls, view_type='pygame', sizex=8, sizey=8, width=800, height=600, **kwargs):
        """
        Create a view of the specified type.
        
        Args:
            view_type: Type of view ('pygame', 'terminal', 'headless')
            sizex: Board width
            sizey: Board height
            width: Display width
            height: Display height
            **kwargs: Additional view-specific arguments
            
        Returns:
            AbstractBoardView: Instance of requested view type
            
        Raises:
            ValueError: If view_type is not supported
        """
        view_type = view_type.lower()
        
        if view_type not in cls.VIEW_TYPES:
            raise ValueError(f"Unsupported view type: {view_type}. "
                           f"Available: {list(cls.VIEW_TYPES.keys())}")
        
        view_class = cls.VIEW_TYPES[view_type]
        return view_class(sizex, sizey, width, height, **kwargs)
    
    @classmethod
    def get_available_views(cls):
        """
        Get list of available view types.
        
        Returns:
            list: List of view type names
        """
        return list(cls.VIEW_TYPES.keys())
    
    @classmethod
    def register_view(cls, name, view_class):
        """
        Register a custom view type.
        
        Args:
            name: Name for the view type
            view_class: Class implementing AbstractBoardView
        """
        cls.VIEW_TYPES[name] = view_class


# Convenience functions

def create_pygame_view(sizex=8, sizey=8):
    """Create default Pygame graphical view"""
    return ViewFactory.create_view('pygame', sizex, sizey)

def create_terminal_view(sizex=8, sizey=8):
    """Create ASCII art terminal view"""
    return ViewFactory.create_view('terminal', sizex, sizey)

def create_headless_view(sizex=8, sizey=8):
    """Create headless view (no rendering)"""
    return ViewFactory.create_view('headless', sizex, sizey)

