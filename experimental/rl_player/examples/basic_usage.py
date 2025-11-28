"""
Basic usage example for RL Player

This example shows how to:
1. Create a neural network model
2. Encode game state
3. Get policy and value predictions
"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from Reversi.BitboardGame import BitboardGame
from experimental.rl_player.core.neural_network import NeuralNetwork
from experimental.rl_player.utils.state_encoder import encode_state


def main():
    """Basic usage example."""
    print("=" * 60)
    print("RL Player - Basic Usage Example")
    print("=" * 60)
    
    # 1. Create a game
    print("\n1. Creating game...")
    game = BitboardGame()
    print(f"   Game created. Turn: {game.turn}")
    
    # 2. Create neural network model
    print("\n2. Creating neural network model...")
    model = NeuralNetwork(
        input_channels=8,  # Use advanced features + opening book (8 channels)
        num_residual_blocks=19,
        channels=256
    )
    print(f"   Model created on device: {model.device}")
    print(f"   Total parameters: {model.count_parameters():,}")
    
    # 3. Encode game state
    print("\n3. Encoding game state...")
    state = encode_state(
        game,
        player_color="B",
        use_advanced_features=True,
        use_opening_book=True,
        device=model.device
    )
    print(f"   State shape: {state.shape} (channels, height, width)")
    print(f"   Using advanced features: 8 channels (including opening book)")
    
    # 4. Get predictions
    print("\n4. Getting model predictions...")
    state_batch = state.unsqueeze(0)  # Add batch dimension: [1, 7, 8, 8]
    
    # Forward pass
    policy_logits, value = model.forward(state_batch)
    print(f"   Policy logits shape: {policy_logits.shape}")
    print(f"   Value shape: {value.shape}")
    print(f"   Position value: {value.item():.4f}")
    
    # Get policy probabilities
    policy = model.get_policy(state_batch, temperature=1.0)
    print(f"   Policy probabilities shape: {policy.shape}")
    
    # Find best move (excluding pass)
    move_probs = policy[0, :64]  # First 64 positions (exclude pass)
    best_move_idx = move_probs.argmax().item()
    best_move_prob = move_probs[best_move_idx].item()
    
    row = best_move_idx // 8
    col = best_move_idx % 8
    move_name = f"{chr(ord('A') + col)}{row + 1}"
    
    print(f"\n   Best move prediction:")
    print(f"   - Position: {move_name} (index {best_move_idx})")
    print(f"   - Probability: {best_move_prob:.4f}")
    
    # 5. Test with different player
    print("\n5. Testing with white player perspective...")
    state_white = encode_state(
        game,
        player_color="W",
        use_advanced_features=True,
        use_opening_book=True,
        device=model.device
    )
    value_white = model.get_value(state_white.unsqueeze(0))
    print(f"   Value from white perspective: {value_white.item():.4f}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r experimental/requirements-rl.txt")
        sys.exit(1)

