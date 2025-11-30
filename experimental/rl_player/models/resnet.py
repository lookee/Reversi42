"""
ResNet Architecture for Reversi

ResNet-based neural network with Policy and Value heads.
Inspired by AlphaZero and Leela Chess Zero.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple


class ResidualBlock(nn.Module):
    """
    Residual block with two convolutional layers and skip connection.
    """
    
    def __init__(self, channels: int):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual  # Skip connection
        out = F.relu(out)
        return out


class ResNetReversi(nn.Module):
    """
    ResNet architecture for Reversi with Policy and Value heads.
    
    Architecture:
    - Input: [batch, channels, 8, 8] (channels = 2, 7, or 8)
    - Convolutional block
    - N residual blocks
    - Policy head: outputs move probabilities [batch, 65] (64 positions + pass)
    - Value head: outputs position value [batch, 1] in [-1, 1]
    """
    
    def __init__(
        self,
        input_channels: int = 8,  # 2 (basic), 7 (advanced), or 8 (advanced + opening book)
        num_residual_blocks: int = 19,
        channels: int = 256,
        policy_head_channels: int = 2,
        value_head_hidden: int = 256,
    ):
        """
        Initialize ResNet for Reversi.
        
        Args:
            input_channels: Number of input channels (2, 7, or 8)
            num_residual_blocks: Number of residual blocks
            channels: Number of channels in residual blocks
            policy_head_channels: Channels in policy head convolution
            value_head_hidden: Hidden units in value head
        """
        super().__init__()
        
        self.input_channels = input_channels
        self.num_residual_blocks = num_residual_blocks
        self.channels = channels
        
        # Initial convolutional block
        self.conv_block = nn.Sequential(
            nn.Conv2d(input_channels, channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True)
        )
        
        # Residual blocks
        self.residual_blocks = nn.ModuleList([
            ResidualBlock(channels) for _ in range(num_residual_blocks)
        ])
        
        # Policy head
        self.policy_conv = nn.Conv2d(channels, policy_head_channels, kernel_size=1, bias=False)
        self.policy_bn = nn.BatchNorm2d(policy_head_channels)
        self.policy_fc = nn.Linear(policy_head_channels * 8 * 8, 65)  # 64 positions + pass
        
        # Value head
        self.value_conv = nn.Conv2d(channels, 1, kernel_size=1, bias=False)
        self.value_bn = nn.BatchNorm2d(1)
        self.value_fc1 = nn.Linear(8 * 8, value_head_hidden)
        self.value_fc2 = nn.Linear(value_head_hidden, 1)
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass.
        
        Args:
            x: Input tensor [batch, channels, 8, 8]
            
        Returns:
            Tuple of (policy_logits, value)
            - policy_logits: [batch, 65] (logits before softmax)
            - value: [batch, 1] (tanh output in [-1, 1])
        """
        # Initial convolution
        x = self.conv_block(x)
        
        # Residual blocks
        for block in self.residual_blocks:
            x = block(x)
        
        # Policy head
        policy = self.policy_conv(x)
        policy = F.relu(self.policy_bn(policy))
        policy = policy.view(policy.size(0), -1)  # Flatten
        policy_logits = self.policy_fc(policy)
        
        # Value head
        value = self.value_conv(x)
        value = F.relu(self.value_bn(value))
        value = value.view(value.size(0), -1)  # Flatten
        value = F.relu(self.value_fc1(value))
        value = torch.tanh(self.value_fc2(value))
        
        return policy_logits, value
    
    def get_policy(self, x: torch.Tensor, temperature: float = 1.0) -> torch.Tensor:
        """
        Get policy probabilities with temperature.
        
        Args:
            x: Input tensor [batch, channels, 8, 8]
            temperature: Temperature for softmax (1.0 = normal, <1.0 = sharper)
            
        Returns:
            Policy probabilities [batch, 65]
        """
        policy_logits, _ = self.forward(x)
        policy_logits = policy_logits / temperature
        return F.softmax(policy_logits, dim=1)
    
    def get_value(self, x: torch.Tensor) -> torch.Tensor:
        """
        Get position value only.
        
        Args:
            x: Input tensor [batch, channels, 8, 8]
            
        Returns:
            Position value [batch, 1]
        """
        _, value = self.forward(x)
        return value
    
    def count_parameters(self) -> int:
        """Count total number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def create_resnet_model(
    input_channels: int = 7,
    num_residual_blocks: int = 19,
    channels: int = 256,
    **kwargs
) -> ResNetReversi:
    """
    Factory function to create ResNet model.
    
    Args:
        input_channels: Number of input channels
        num_residual_blocks: Number of residual blocks
        channels: Number of channels
        **kwargs: Additional arguments passed to ResNetReversi
        
    Returns:
        ResNetReversi model
    """
    return ResNetReversi(
        input_channels=input_channels,
        num_residual_blocks=num_residual_blocks,
        channels=channels,
        **kwargs
    )
