"""
Players Package

All player implementations for Reversi42.

Version: 3.1.0
"""

# Lazy import to avoid circular dependencies
# TerminalHumanPlayer is imported on-demand where needed

__all__ = []

def __getattr__(name):
    """Lazy import to avoid circular dependencies"""
    if name == 'TerminalHumanPlayer':
        from ui.implementations.terminal import TerminalHumanPlayer
        return TerminalHumanPlayer
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

