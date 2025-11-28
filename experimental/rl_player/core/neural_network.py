"""
Neural Network Wrapper

Wrapper around ResNet model with device management and utility methods.
"""

import torch
import torch.nn as nn
from typing import Optional, Tuple

from ..models.resnet import ResNetReversi, create_resnet_model


class NeuralNetwork:
    """
    Wrapper for neural network with device management and utilities.
    """
    
    def __init__(
        self,
        model: Optional[ResNetReversi] = None,
        input_channels: int = 8,  # Default to 8 (with opening book)
        num_residual_blocks: int = 19,
        channels: int = 256,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize neural network.
        
        Args:
            model: Pre-initialized ResNet model (if None, creates new)
            input_channels: Number of input channels (if creating new model)
            num_residual_blocks: Number of residual blocks (if creating new model)
            channels: Number of channels (if creating new model)
            device: PyTorch device (auto-detected if None)
        """
        # Auto-detect device
        if device is None:
            if torch.backends.mps.is_available():
                device = torch.device("mps")
            elif torch.cuda.is_available():
                device = torch.device("cuda")
            else:
                device = torch.device("cpu")
        
        self.device = device
        
        # Create or use provided model
        if model is None:
            self.model = create_resnet_model(
                input_channels=input_channels,
                num_residual_blocks=num_residual_blocks,
                channels=channels
            )
        else:
            self.model = model
        
        # Move model to device
        self.model = self.model.to(self.device)
        self.model.eval()  # Start in eval mode
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass.
        
        Args:
            x: Input tensor [batch, channels, 8, 8]
            
        Returns:
            Tuple of (policy_logits, value)
        """
        x = x.to(self.device)
        return self.model(x)
    
    def get_policy(self, x: torch.Tensor, temperature: float = 1.0) -> torch.Tensor:
        """
        Get policy probabilities.
        
        Args:
            x: Input tensor [batch, channels, 8, 8]
            temperature: Temperature for softmax
            
        Returns:
            Policy probabilities [batch, 65]
        """
        x = x.to(self.device)
        return self.model.get_policy(x, temperature)
    
    def get_value(self, x: torch.Tensor) -> torch.Tensor:
        """
        Get position value.
        
        Args:
            x: Input tensor [batch, channels, 8, 8]
            
        Returns:
            Position value [batch, 1]
        """
        x = x.to(self.device)
        return self.model.get_value(x)
    
    def train_mode(self):
        """Switch to training mode."""
        self.model.train()
    
    def eval_mode(self):
        """Switch to evaluation mode."""
        self.model.eval()
    
    def save(self, filepath: str):
        """
        Save model to file.
        
        Args:
            filepath: Path to save model
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_config': {
                'input_channels': self.model.input_channels,
                'num_residual_blocks': self.model.num_residual_blocks,
                'channels': self.model.channels,
            }
        }, filepath)
    
    @classmethod
    def load(cls, filepath: str, device: Optional[torch.device] = None) -> 'NeuralNetwork':
        """
        Load model from file.
        
        Args:
            filepath: Path to model file
            device: PyTorch device (auto-detected if None)
            
        Returns:
            NeuralNetwork instance
            
        Raises:
            FileNotFoundError: If file doesn't exist
            RuntimeError: If checkpoint is corrupted
        """
        import os
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Checkpoint file not found: {filepath}")
        
        try:
            checkpoint = torch.load(filepath, map_location=device)
        except Exception as e:
            raise RuntimeError(f"Failed to load checkpoint {filepath}: {e}. The file may be corrupted.")
        
        # Validate checkpoint structure
        if 'model_state_dict' not in checkpoint:
            raise RuntimeError(f"Invalid checkpoint format: missing 'model_state_dict' in {filepath}")
        
        model_config = checkpoint.get('model_config', {})
        
        # Use default config if not in checkpoint
        if not model_config:
            print("⚠ Warning: No model_config in checkpoint, using defaults")
            model_config = {
                'input_channels': 8,
                'num_residual_blocks': 19,
                'channels': 256
            }
        
        # Create model with saved config
        model = create_resnet_model(**model_config)
        
        try:
            model.load_state_dict(checkpoint['model_state_dict'])
        except Exception as e:
            raise RuntimeError(f"Failed to load model weights from checkpoint: {e}. Model architecture may have changed.")
        
        # Create wrapper
        nn_wrapper = cls(model=model, device=device)
        return nn_wrapper
    
    def count_parameters(self) -> int:
        """Count total parameters."""
        return self.model.count_parameters()

