"""
ViewFactory - Factory for Creating Board Views

Simplifies view creation with sensible defaults.

Version: 3.1.0
"""

# All views use lazy imports to avoid circular dependencies


class ViewFactory:
    """
    Factory for creating different view types.
    
    Makes it easy to switch between view implementations.
    Uses lazy imports to avoid circular dependencies.
    """
    
    @staticmethod
    def _get_view_class(view_type):
        """Get view class with lazy import"""
        if view_type in ('pygame', 'gui'):
            from ui.implementations.pygame.view import PygameBoardView
            return PygameBoardView
        elif view_type in ('terminal', 'console'):
            from ui.implementations.terminal import TerminalBoardView
            return TerminalBoardView
        elif view_type in ('headless', 'none'):
            from ui.implementations.headless import HeadlessBoardView
            return HeadlessBoardView
        else:
            return None
    
    # Legacy registry (deprecated - use _get_view_class)
    VIEW_TYPES = None  # Disabled to force lazy loading
    
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
        
        view_class = cls._get_view_class(view_type)
        if view_class is None:
            raise ValueError(f"Unsupported view type: {view_type}. "
                           f"Available: pygame, terminal, headless")
        
        return view_class(sizex, sizey, width, height, **kwargs)
    
    @classmethod
    def get_available_views(cls):
        """
        Get list of available view types.
        
        Returns:
            list: List of view type names
        """
        return ['pygame', 'terminal', 'headless', 'gui', 'console', 'none']
    
    # Note: register_view removed - use direct imports for custom views


# Convenience functions

def create_pygame_view(sizex=8, sizey=8):
    """Create default Pygame graphical view"""
    from ui.implementations.pygame.view import PygameBoardView
    return PygameBoardView(sizex, sizey)

def create_terminal_view(sizex=8, sizey=8):
    """Create ASCII art terminal view"""
    from ui.implementations.terminal import TerminalBoardView
    return TerminalBoardView(sizex, sizey)

def create_headless_view(sizex=8, sizey=8):
    """Create headless view (no rendering)"""
    from ui.implementations.headless import HeadlessBoardView
    return HeadlessBoardView(sizex, sizey)

