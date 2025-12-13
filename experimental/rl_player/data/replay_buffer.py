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

    def save(self, filepath: str):
        """
        Save replay buffer to disk.
        
        Args:
            filepath: Path to save pickle file
        """
        import pickle
        import os
        
        # Save as temporary file first to avoid corruption
        temp_path = filepath + ".tmp"
        
        try:
            with open(temp_path, 'wb') as f:
                pickle.dump({
                    'buffer': self.buffer,
                    'position': self.position,
                    'capacity': self.capacity
                }, f)
            
            # Atomic rename
            os.replace(temp_path, filepath)
            print(f"✓ Replay buffer saved to {filepath} ({len(self)} samples)")
            
        except Exception as e:
            print(f"⚠ Failed to save replay buffer: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def load(self, filepath: str):
        """
        Load replay buffer from disk.
        
        Args:
            filepath: Path to load pickle file from
        """
        import pickle
        import os
        
        if not os.path.exists(filepath):
            print(f"ℹ No replay buffer found at {filepath}")
            return
            
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                
            self.buffer = data.get('buffer', [])
            self.position = data.get('position', 0)
            self.capacity = data.get('capacity', self.capacity)
            
            print(f"✓ Replay buffer loaded from {filepath} ({len(self)} samples)")
            
        except Exception as e:
            print(f"⚠ Failed to load replay buffer: {e}")


