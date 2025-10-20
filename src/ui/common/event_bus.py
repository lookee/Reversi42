"""
EventBus - Decoupled Event System

Implements Observer Pattern for decoupled component communication.
Components can emit and listen to events without knowing each other.

Design Pattern: Observer + Mediator
"""

from typing import Callable, Dict, List, Any, Optional
from collections import defaultdict


class EventBus:
    """
    Event bus for decoupled component communication.
    
    Implements Observer Pattern - components subscribe to events
    without knowing who publishes them.
    
    Usage:
        bus = EventBus()
        
        # Subscribe
        bus.on('piece_placed', update_score)
        bus.on('piece_placed', play_sound)
        
        # Publish
        bus.emit('piece_placed', {'x': 3, 'y': 3, 'color': 'B'})
        
        # Both callbacks are called!
    """
    
    def __init__(self):
        """Initialize event bus."""
        self.listeners: Dict[str, List[Callable]] = defaultdict(list)
    
    def on(self, event_name: str, callback: Callable):
        """
        Subscribe to an event.
        
        Args:
            event_name: Name of the event
            callback: Function to call when event is emitted
        """
        if callback not in self.listeners[event_name]:
            self.listeners[event_name].append(callback)
    
    def off(self, event_name: str, callback: Callable):
        """
        Unsubscribe from an event.
        
        Args:
            event_name: Name of the event
            callback: Callback to remove
        """
        if callback in self.listeners[event_name]:
            self.listeners[event_name].remove(callback)
    
    def emit(self, event_name: str, data: Any = None):
        """
        Emit an event to all subscribers.
        
        Args:
            event_name: Name of the event
            data: Event data (optional)
        """
        for callback in self.listeners[event_name]:
            try:
                if data is not None:
                    callback(data)
                else:
                    callback()
            except Exception as e:
                print(f"⚠️  Error in event handler for '{event_name}': {e}")
    
    def clear(self, event_name: Optional[str] = None):
        """
        Clear listeners.
        
        Args:
            event_name: Event to clear (None = clear all)
        """
        if event_name:
            self.listeners[event_name].clear()
        else:
            self.listeners.clear()
    
    def has_listeners(self, event_name: str) -> bool:
        """
        Check if event has any listeners.
        
        Args:
            event_name: Event name
            
        Returns:
            True if event has listeners
        """
        return len(self.listeners[event_name]) > 0


# Global event bus instance (singleton)
_global_event_bus = None


def get_global_event_bus() -> EventBus:
    """
    Get global event bus instance (Singleton).
    
    Returns:
        Global EventBus instance
    """
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus

