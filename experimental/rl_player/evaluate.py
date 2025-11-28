"""
Script per valutare il modello addestrato.

Usage:
    python experimental/rl_player/evaluate.py [checkpoint_path]
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

import torch
from experimental.rl_player.core.neural_network import NeuralNetwork
from experimental.rl_player.core.mcts import MCTS
from Reversi.BitboardGame import BitboardGame


def evaluate_model(checkpoint_path: str, num_simulations: int = 800):
    """Valuta il modello su posizione iniziale."""
    
    print("=" * 70)
    print("RL Player Model Evaluation")
    print("=" * 70)
    print()
    
    # Setup device
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
    print(f"Device: {device}")
    print()
    
    # Load model
    print(f"Loading model from: {checkpoint_path}")
    try:
        model = NeuralNetwork.load(checkpoint_path, device=device)
        print(f"✓ Model loaded successfully")
        print(f"  Parameters: {model.count_parameters():,}")
        print()
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return
    
    # Create MCTS
    mcts = MCTS(model, num_simulations=num_simulations)
    print(f"MCTS configured with {num_simulations} simulations")
    print()
    
    # Test on initial position
    print("Testing on initial position...")
    game = BitboardGame()
    
    print(f"Initial position:")
    print(f"  Black pieces: {bin(game.black).count('1')}")
    print(f"  White pieces: {bin(game.white).count('1')}")
    print(f"  Legal moves: {len(game.get_move_list())}")
    print()
    
    # Perform MCTS search
    print("Performing MCTS search...")
    root = mcts.search(game, 'B', add_noise=False)
    
    print(f"\nResults:")
    print(f"  Root value estimate: {root.value_estimate:.4f}")
    print(f"  Total visits: {root.visit_count}")
    print(f"  Average value: {root.get_value():.4f}")
    print()
    
    # Show top moves
    if root.children:
        print("Top 5 moves:")
        sorted_children = sorted(
            root.children.items(),
            key=lambda x: x[1].visit_count,
            reverse=True
        )[:5]
        
        for i, (move, child) in enumerate(sorted_children, 1):
            visit_pct = (child.visit_count / root.visit_count) * 100
            print(f"  {i}. {move} ({move.get_x()},{move.get_y()}):")
            print(f"     Visits: {child.visit_count} ({visit_pct:.1f}%)")
            print(f"     Value: {child.get_value():.4f}")
            print(f"     Prior: {root.prior_probs.get(move, 0.0):.4f}")
    
    print()
    print("=" * 70)
    print("Evaluation complete!")
    print("=" * 70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate RL model")
    parser.add_argument(
        "checkpoint",
        nargs="?",
        default="experimental/checkpoints/latest.pth",
        help="Path to checkpoint file"
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=800,
        help="Number of MCTS simulations"
    )
    
    args = parser.parse_args()
    
    # Resolve path
    checkpoint_path = Path(args.checkpoint)
    if not checkpoint_path.is_absolute():
        checkpoint_path = project_root / checkpoint_path
    
    if not checkpoint_path.exists():
        print(f"Error: Checkpoint not found: {checkpoint_path}")
        sys.exit(1)
    
    evaluate_model(str(checkpoint_path), args.simulations)

