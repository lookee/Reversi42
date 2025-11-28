"""
Replay Buffer for storing training data.

Stores (state, policy, value) tuples from self-play games.
"""

import numpy as np
from typing import List, Tuple, Optional
from collections import deque
import random


class ReplayBuffer:
    """
    Replay buffer for storing self-play data.
    """
    
    def __init__(self, capacity: int = 1_000_000):
        """
        Initialize replay buffer.
        
        Args:
            capacity: Maximum number of samples to store
        """
        self.capacity = capacity
        self.buffer: List[Tuple] = []
        self.position = 0
    
    def add(self, state, policy, value: float):
        """
        Add a sample to the buffer.
        
        Args:
            state: Game state (tensor or numpy array)
            policy: Policy distribution (dict mapping Move to prob, or array)
            value: Position value (float)
        """
        if len(self.buffer) < self.capacity:
            self.buffer.append((state, policy, value))
        else:
            self.buffer[self.position] = (state, policy, value)
            self.position = (self.position + 1) % self.capacity
    
    def add_batch(self, states, policies, values):
        """
        Add multiple samples at once.
        
        Args:
            states: List of game states
            policies: List of policy distributions
            values: List of position values
        """
        for state, policy, value in zip(states, policies, values):
            self.add(state, policy, value)
    
    def sample(self, batch_size: int) -> Tuple:
        """
        Sample a batch from the buffer.
        
        Args:
            batch_size: Number of samples to return
            
        Returns:
            Tuple of (states, policies, values)
        """
        if len(self.buffer) < batch_size:
            batch_size = len(self.buffer)
        
        samples = random.sample(self.buffer, batch_size)
        states, policies, values = zip(*samples)
        
        return list(states), list(policies), list(values)
    
    def __len__(self) -> int:
        """Get current buffer size."""
        return len(self.buffer)
    
    def clear(self):
        """Clear the buffer."""
        self.buffer.clear()
        self.position = 0

