"""
Basic tests for RL Player components

Tests state encoding and neural network initialization.
"""

import pytest
import torch
import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from Reversi.BitboardGame import BitboardGame
from experimental.rl_player.utils.state_encoder import encode_state, encode_batch
from experimental.rl_player.core.neural_network import NeuralNetwork
from experimental.rl_player.models.resnet import ResNetReversi


def test_state_encoder_basic():
    """Test basic state encoding (2 channels)."""
    game = BitboardGame()
    state = encode_state(game, player_color="B", use_advanced_features=False)
    
    assert state.shape == (2, 8, 8), f"Expected shape (2, 8, 8), got {state.shape}"
    assert isinstance(state, torch.Tensor)


def test_state_encoder_advanced():
    """Test advanced state encoding (7 channels)."""
    game = BitboardGame()
    state = encode_state(game, player_color="B", use_advanced_features=True)
    
    assert state.shape == (7, 8, 8), f"Expected shape (7, 8, 8), got {state.shape}"
    assert isinstance(state, torch.Tensor)
    
    # Check channel values are in [0, 1]
    assert state.min() >= 0.0, "State values should be >= 0"
    assert state.max() <= 1.0, "State values should be <= 1"


def test_state_encoder_batch():
    """Test batch encoding."""
    games = [BitboardGame() for _ in range(4)]
    player_colors = ["B", "W", "B", "W"]
    
    batch = encode_batch(games, player_colors, use_advanced_features=True)
    
    assert batch.shape == (4, 7, 8, 8), f"Expected shape (4, 7, 8, 8), got {batch.shape}"


def test_resnet_model_creation():
    """Test ResNet model creation."""
    model = ResNetReversi(
        input_channels=7,
        num_residual_blocks=19,
        channels=256
    )
    
    assert model is not None
    param_count = model.count_parameters()
    assert param_count > 0, "Model should have parameters"
    assert 3_000_000 < param_count < 6_000_000, f"Expected ~4-5M parameters, got {param_count}"


def test_resnet_forward():
    """Test ResNet forward pass."""
    model = ResNetReversi(input_channels=7, num_residual_blocks=19, channels=256)
    model.eval()
    
    # Create dummy input
    x = torch.randn(2, 7, 8, 8)
    
    policy_logits, value = model(x)
    
    assert policy_logits.shape == (2, 65), f"Expected policy shape (2, 65), got {policy_logits.shape}"
    assert value.shape == (2, 1), f"Expected value shape (2, 1), got {value.shape}"
    assert value.min() >= -1.0 and value.max() <= 1.0, "Value should be in [-1, 1]"


def test_neural_network_wrapper():
    """Test NeuralNetwork wrapper."""
    nn_wrapper = NeuralNetwork(input_channels=7, num_residual_blocks=19, channels=256)
    
    assert nn_wrapper.device is not None
    assert nn_wrapper.model is not None
    
    # Test forward pass
    game = BitboardGame()
    state = encode_state(game, player_color="B", use_advanced_features=True)
    state_batch = state.unsqueeze(0)  # Add batch dimension
    
    policy_logits, value = nn_wrapper.forward(state_batch)
    
    assert policy_logits.shape == (1, 65)
    assert value.shape == (1, 1)


def test_neural_network_policy():
    """Test policy extraction with temperature."""
    nn_wrapper = NeuralNetwork(input_channels=7, num_residual_blocks=19, channels=256)
    
    game = BitboardGame()
    state = encode_state(game, player_color="B", use_advanced_features=True)
    state_batch = state.unsqueeze(0)
    
    policy = nn_wrapper.get_policy(state_batch, temperature=1.0)
    
    assert policy.shape == (1, 65)
    assert abs(policy.sum().item() - 1.0) < 1e-5, "Policy should sum to 1"
    assert (policy >= 0).all(), "Policy should be non-negative"


def test_neural_network_value():
    """Test value extraction."""
    nn_wrapper = NeuralNetwork(input_channels=7, num_residual_blocks=19, channels=256)
    
    game = BitboardGame()
    state = encode_state(game, player_color="B", use_advanced_features=True)
    state_batch = state.unsqueeze(0)
    
    value = nn_wrapper.get_value(state_batch)
    
    assert value.shape == (1, 1)
    assert value.min() >= -1.0 and value.max() <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

