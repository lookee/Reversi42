# Experimental RL Player

Deep reinforcement learning player for Reversi using AlphaZero-style approach.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r experimental/requirements-rl.txt
```

### 2. Start Training

```bash
cd experimental/rl_player
python train.py
```

The training script will:
- Create a new model or load from checkpoint
- Generate self-play games
- Train on the replay buffer
- Save checkpoints every 1000 iterations
- Save configurations every 1000 iterations

## Configuration

Edit `experimental/config/rl_config.yaml` to customize:
- Training hyperparameters
- MCTS parameters
- Self-play settings
- Checkpoint frequency

## Checkpoints

Checkpoints are saved in `experimental/checkpoints/`:
- `latest.pth` - Latest model checkpoint
- `latest_config.yaml` - Latest configuration
- `iteration_XXXXXX.pth` - Periodic checkpoints
- `iteration_XXXXXX_config.yaml` - Configuration snapshots

## Resume Training

Training automatically resumes from the latest checkpoint if it exists. The training state is saved in `checkpoints/training_state.json`.

## Usage Example

```python
from experimental.rl_player.core.neural_network import NeuralNetwork
from experimental.rl_player.utils.state_encoder import encode_state
from Reversi.BitboardGame import BitboardGame

# Load trained model
model = NeuralNetwork.load("experimental/checkpoints/best.pth")

# Use model for inference
game = BitboardGame()
state = encode_state(game, "B", use_advanced_features=True)
policy, value = model.forward(state.unsqueeze(0))
```

## Architecture

- **State Encoder**: 7-channel input (pieces, legal moves, mobility, corners, edges, turn)
- **ResNet**: 19 residual blocks, 256 channels
- **Policy Head**: 65 outputs (64 positions + pass)
- **Value Head**: Position evaluation [-1, 1]
- **MCTS**: 800 simulations per move during training

## Training Progress

Monitor training progress:
- Checkpoints are saved periodically
- Training metrics are logged
- Configuration files track model state

## Notes

- Training is optimized for Apple Silicon M1 (MPS backend)
- Self-play generates training data automatically
- Model improves through iterative self-play and training

