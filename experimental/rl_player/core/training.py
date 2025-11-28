"""
Training Module

Handles the training loop with loss computation and optimization.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, Optional
from tqdm import tqdm

from ..core.neural_network import NeuralNetwork
from ..data.replay_buffer import ReplayBuffer
from ..utils.state_encoder import encode_batch


class Trainer:
    """
    Trainer for RL model.
    """
    
    def __init__(
        self,
        neural_network: NeuralNetwork,
        learning_rate: float = 0.001,
        weight_decay: float = 1e-4,
        optimizer_type: str = "AdamW",
    ):
        """
        Initialize trainer.
        
        Args:
            neural_network: NeuralNetwork instance to train
            learning_rate: Learning rate
            weight_decay: Weight decay for regularization
            optimizer_type: Optimizer type ("AdamW", "Adam", "SGD")
        """
        self.neural_network = neural_network
        self.neural_network.train_mode()
        
        # Setup optimizer
        # Ensure weight_decay is valid (>= 0)
        weight_decay = max(0.0, float(weight_decay)) if weight_decay is not None else 0.0
        
        if optimizer_type == "AdamW":
            self.optimizer = optim.AdamW(
                self.neural_network.model.parameters(),
                lr=learning_rate,
                weight_decay=weight_decay
            )
        elif optimizer_type == "Adam":
            self.optimizer = optim.Adam(
                self.neural_network.model.parameters(),
                lr=learning_rate,
                weight_decay=weight_decay
            )
        else:
            self.optimizer = optim.SGD(
                self.neural_network.model.parameters(),
                lr=learning_rate,
                weight_decay=weight_decay,
                momentum=0.9
            )
        
        # Loss functions
        self.policy_loss_fn = nn.CrossEntropyLoss()
        self.value_loss_fn = nn.MSELoss()
        
        # Metrics
        self.metrics = {
            'policy_loss': [],
            'value_loss': [],
            'total_loss': [],
        }
    
    def train_step(self, states, policies, values):
        """
        Perform a single training step.
        
        Args:
            states: Batch of game states [batch, channels, 8, 8]
            policies: Batch of target policies [batch, 65]
            values: Batch of target values [batch]
            
        Returns:
            Dictionary with loss values
        """
        # Convert to tensors if needed
        if isinstance(states, list):
            states = torch.stack(states).to(self.neural_network.device)
        else:
            states = states.to(self.neural_network.device)
        
        if isinstance(policies, list):
            policies = torch.stack(policies).to(self.neural_network.device)
        else:
            policies = policies.to(self.neural_network.device)
        
        if isinstance(values, list):
            values = torch.tensor(values, dtype=torch.float32).to(self.neural_network.device)
        else:
            values = values.to(self.neural_network.device)
        
        # Forward pass
        policy_logits, value_pred = self.neural_network.forward(states)
        
        # Compute losses
        # Policy loss: CrossEntropy between predicted and target policy
        policy_loss = self.policy_loss_fn(policy_logits, policies)
        
        # Value loss: MSE between predicted and target value
        value_loss = self.value_loss_fn(value_pred.squeeze(), values)
        
        # Total loss
        total_loss = policy_loss + value_loss
        
        # Backward pass
        self.optimizer.zero_grad()
        total_loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(self.neural_network.model.parameters(), max_norm=1.0)
        
        self.optimizer.step()
        
        # Store metrics
        loss_dict = {
            'policy_loss': policy_loss.item(),
            'value_loss': value_loss.item(),
            'total_loss': total_loss.item(),
        }
        
        self.metrics['policy_loss'].append(loss_dict['policy_loss'])
        self.metrics['value_loss'].append(loss_dict['value_loss'])
        self.metrics['total_loss'].append(loss_dict['total_loss'])
        
        return loss_dict
    
    def train_epoch(
        self,
        replay_buffer: ReplayBuffer,
        batch_size: int = 2048,
        num_batches: Optional[int] = None,
        verbose: bool = True
    ) -> Dict:
        """
        Train for one epoch.
        
        Args:
            replay_buffer: Replay buffer with training data
            batch_size: Batch size
            num_batches: Number of batches to train (None = use all data)
            verbose: Whether to show progress
            
        Returns:
            Dictionary with average losses
        """
        if len(replay_buffer) < batch_size:
            return {
                'policy_loss': 0.0,
                'value_loss': 0.0,
                'total_loss': 0.0,
            }
        
        # Determine number of batches
        if num_batches is None:
            num_batches = len(replay_buffer) // batch_size
        
        total_policy_loss = 0.0
        total_value_loss = 0.0
        total_loss = 0.0
        
        iterator = range(num_batches)
        if verbose:
            iterator = tqdm(iterator, desc="Training batches")
        
        for _ in iterator:
            # Sample batch
            states, policies, values = replay_buffer.sample(batch_size)
            
            # Convert policies from dict/array to tensor format
            # Policies should be [batch, 65] tensors
            policy_tensors = []
            for policy in policies:
                if isinstance(policy, dict):
                    # Convert dict to tensor
                    policy_tensor = torch.zeros(65)
                    for move, prob in policy.items():
                        row = move.get_y() - 1
                        col = move.get_x() - 1
                        idx = row * 8 + col
                        policy_tensor[idx] = prob
                    policy_tensors.append(policy_tensor)
                else:
                    policy_tensors.append(policy)
            
            policies = torch.stack(policy_tensors)
            
            # Training step
            loss_dict = self.train_step(states, policies, values)
            
            total_policy_loss += loss_dict['policy_loss']
            total_value_loss += loss_dict['value_loss']
            total_loss += loss_dict['total_loss']
        
        # Return averages
        return {
            'policy_loss': total_policy_loss / num_batches,
            'value_loss': total_value_loss / num_batches,
            'total_loss': total_loss / num_batches,
        }
    
    def get_metrics(self) -> Dict:
        """Get training metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self):
        """Reset metrics."""
        self.metrics = {
            'policy_loss': [],
            'value_loss': [],
            'total_loss': [],
        }

