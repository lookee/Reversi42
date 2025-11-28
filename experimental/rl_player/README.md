# RL Player Module

Deep reinforcement learning player for Reversi using AlphaZero-style approach.

## Structure

```
rl_player/
├── __init__.py
├── core/                    # Core components
│   └── neural_network.py   # Neural network wrapper
├── models/                  # Neural network architectures
│   └── resnet.py           # ResNet architecture
├── utils/                   # Utilities
│   └── state_encoder.py    # State encoding with advanced features
└── README.md
```

## Features

- **Advanced State Encoding**: 8-channel input with:
  - Black/White pieces
  - Legal moves mask
  - Mobility count
  - Corner positions
  - Edge positions
  - Turn indicator
  - Opening book moves (NEW)

- **ResNet Architecture**: Deep residual network with:
  - 19 residual blocks (configurable)
  - Policy head (65 outputs: 64 positions + pass)
  - Value head (position evaluation)

- **M1 Optimization**: Automatic device detection (MPS/CUDA/CPU)

## Quick Start

```python
from experimental.rl_player.core.neural_network import NeuralNetwork
from experimental.rl_player.utils.state_encoder import encode_state
from Reversi.BitboardGame import BitboardGame

# Create model
model = NeuralNetwork(input_channels=7, num_residual_blocks=19)

# Encode game state
game = BitboardGame()
state = encode_state(game, player_color="B", use_advanced_features=True)

# Get policy and value
policy_logits, value = model.forward(state.unsqueeze(0))
```

## Model Architecture

- **Input**: [batch, 7, 8, 8] tensor
- **ResNet**: 19 residual blocks with 256 channels
- **Policy Head**: Convolution → Linear → 65 outputs
- **Value Head**: Convolution → Linear → Linear → 1 output (tanh)

Total parameters: ~4-5 million

