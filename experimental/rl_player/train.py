"""
Main Training Script for RL Player

Implements the complete training loop:
1. Self-play to generate data
2. Training on replay buffer
3. Checkpoint saving
4. Configuration saving
"""

import os
import sys
import yaml
import json
import time
import torch
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path

# Add project root and src to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_dir = os.path.join(project_root, "src")
experimental_dir = os.path.join(project_root, "experimental")
sys.path.insert(0, project_root)  # Add project root for experimental imports
sys.path.insert(0, src_dir)  # Add src for Reversi imports

# Import from experimental module (relative to project root)
from experimental.rl_player.core.neural_network import NeuralNetwork
from experimental.rl_player.core.mcts import MCTS
from experimental.rl_player.core.self_play import SelfPlay
from experimental.rl_player.core.training import Trainer
from experimental.rl_player.data.replay_buffer import ReplayBuffer


class TrainingConfig:
    """Training configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Load configuration from file or use defaults."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
                print(f"✓ Loaded config from: {config_path}")
        else:
            # Default configuration
            self.config = {
                'training': {
                    'batch_size': 2048,
                    'learning_rate': 0.001,
                    'weight_decay': 1e-4,
                    'optimizer': 'AdamW',
                    'scheduler': 'CosineAnnealingLR',
                    'max_iterations': 1000000,
                },
                'mcts': {
                    'simulations': 800,
                    'c_puct': 1.0,
                    'dirichlet_alpha': 0.3,
                    'dirichlet_epsilon': 0.25,
                },
                'self_play': {
                    'games_per_iteration': 100,
                    'temperature': 1.0,
                    'temperature_decay': 0.99,
                },
                'replay_buffer': {
                    'capacity': 1000000,
                    'min_size': 10000,
                },
                'evaluation': {
                    'eval_frequency': 100,
                    'eval_games': 20,
                    'win_threshold': 0.55,
                },
                'checkpoint': {
                    'save_frequency': 1000,
                    'keep_last_n': 5,
                    'config_save_frequency': 1000,
                    'save_config_with_checkpoint': True,
                },
            }
    
    def get(self, key: str, default=None):
        """Get config value."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value


def save_configuration(
    config_dict: Dict,
    filepath: str,
    model: NeuralNetwork,
    training_state: Dict
):
    """
    Save complete configuration to YAML file.
    
    Args:
        config_dict: Configuration dictionary
        filepath: Path to save YAML file
        model: Neural network model
        training_state: Current training state
    """
    # Build complete configuration
    full_config = {
        'model_architecture': {
            'type': 'ResNet',
            'input_channels': model.model.input_channels,  # Should be 8 with opening book
            'num_residual_blocks': model.model.num_residual_blocks,
            'channels': model.model.channels,
        },
        'training_config': config_dict.get('training', {}),
        'mcts_config': config_dict.get('mcts', {}),
        'player_config': {
            'temperature': config_dict.get('self_play', {}).get('temperature', 0.1),
            'mcts_simulations': config_dict.get('mcts', {}).get('simulations', 800),
            'use_mcts_inference': True,
        },
        'checkpoint_path': training_state.get('checkpoint_path', ''),
        'model_version': '1.0.0',
        'training_iteration': training_state.get('iteration', 0),
        'timestamp': datetime.now().isoformat(),
    }
    
    # Save to YAML
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        yaml.dump(full_config, f, default_flow_style=False, sort_keys=False)


def main():
    """Main training loop."""
    print("=" * 70)
    print("RL Player Training")
    print("=" * 70)
    
    # Setup paths
    # Get project root (3 levels up: experimental/rl_player/train.py -> Reversi42/)
    project_root = Path(__file__).parent.parent.parent
    experimental_dir = project_root / "experimental"
    checkpoints_dir = experimental_dir / "checkpoints"
    checkpoints_dir.mkdir(exist_ok=True)
    
    config_path = experimental_dir / "config" / "rl_config.yaml"
    config = TrainingConfig(str(config_path))
    
    # Device
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"\nDevice: {device}")
    
    # Create or load model
    checkpoint_path = checkpoints_dir / "latest.pth"
    model = None
    
    if checkpoint_path.exists():
        print(f"\nAttempting to load checkpoint from {checkpoint_path}")
        try:
            model = NeuralNetwork.load(str(checkpoint_path), device=device)
            print(f"✓ Model loaded successfully. Parameters: {model.count_parameters():,}")
        except Exception as e:
            print(f"⚠ Warning: Failed to load checkpoint: {e}")
            print("  The checkpoint file may be corrupted or incomplete.")
            print("  Creating new model instead...")
            # Try to backup corrupted checkpoint
            corrupted_path = checkpoints_dir / "latest_corrupted.pth"
            try:
                import shutil
                if corrupted_path.exists():
                    corrupted_path.unlink()
                shutil.move(str(checkpoint_path), str(corrupted_path))
                print(f"  Moved corrupted checkpoint to: {corrupted_path}")
            except Exception as backup_error:
                print(f"  Could not backup corrupted checkpoint: {backup_error}")
    
    if model is None:
        print("\nCreating new model...")
        model = NeuralNetwork(
            input_channels=8,  # 8 channels=256,
            device=device
        )
        print(f"✓ Model created. Parameters: {model.count_parameters():,}")
    
    # Create MCTS
    mcts = MCTS(
        neural_network=model,
        c_puct=config.get('mcts.c_puct', 1.0),
        num_simulations=config.get('mcts.simulations', 800),
        dirichlet_alpha=config.get('mcts.dirichlet_alpha', 0.3),
        dirichlet_epsilon=config.get('mcts.dirichlet_epsilon', 0.25),
    )
    
    # Create self-play engine
    self_play = SelfPlay(
        neural_network=model,
        mcts=mcts,
        temperature=config.get('self_play.temperature', 1.0),
    )
    
    # Create trainer
    trainer = Trainer(
        neural_network=model,
        learning_rate=config.get('training.learning_rate', 0.001),
        weight_decay=config.get('training.weight_decay', 1e-4),
        optimizer_type=config.get('training.optimizer', 'AdamW'),
    )
    
    # Create replay buffer
    replay_buffer = ReplayBuffer(
        capacity=config.get('replay_buffer.capacity', 1000000)
    )
    
    # Training state
    training_state = {
        'iteration': 0,
        'games_played': 0,
        'best_win_rate': 0.0,
        'current_temperature': config.get('self_play.temperature', 1.0),
    }
    
    # Training loop parameters (define before using)
    max_iterations = config.get('training.max_iterations', 1000000)
    games_per_iteration = config.get('self_play.games_per_iteration', 100)
    save_frequency = config.get('checkpoint.save_frequency', 1000)
    config_save_frequency = config.get('checkpoint.config_save_frequency', 1000)
    
    # Load training state if exists
    state_path = checkpoints_dir / "training_state.json"
    if state_path.exists():
        with open(state_path, 'r') as f:
            saved_state = json.load(f)
            training_state.update(saved_state)
            training_state['iteration'] = saved_state.get('iteration', 0)
    
    # Save initial training state
    training_state['start_time'] = time.time() if 'start_time' not in training_state else training_state['start_time']
    training_state['max_iterations'] = max_iterations
    with open(state_path, 'w') as f:
        json.dump(training_state, f, indent=2)
    
    print(f"\nStarting from iteration {training_state['iteration']}")
    print(f"Temperature: {training_state['current_temperature']:.4f}")
    
    try:
        for iteration in range(training_state['iteration'], max_iterations):
            print(f"\n{'='*70}")
            print(f"Iteration {iteration + 1}/{max_iterations}")
            print(f"{'='*70}")
            
            # Self-play phase
            print(f"\nSelf-play: Generating {games_per_iteration} games...")
            print(f"This will take approximately {games_per_iteration * 5 / 60:.1f}-{games_per_iteration * 10 / 60:.1f} minutes")
            print(f"Each game uses {config.get('mcts.simulations', 800)} MCTS simulations per move\n")
            
            training_data = self_play.generate_games(
                num_games=games_per_iteration,
                verbose=True,  # Always verbose to show progress
                progress_bar=True
            )
            
            # Add to replay buffer
            for state, policy, value in training_data:
                replay_buffer.add(state, policy, value)
            
            training_state['games_played'] += games_per_iteration
            print(f"Replay buffer size: {len(replay_buffer)}")
            
            # Training phase
            if len(replay_buffer) >= config.get('replay_buffer.min_size', 10000):
                print(f"\nTraining on replay buffer...")
                avg_losses = trainer.train_epoch(
                    replay_buffer=replay_buffer,
                    batch_size=config.get('training.batch_size', 2048),
                    verbose=True
                )
                
                print(f"Policy Loss: {avg_losses['policy_loss']:.6f}")
                print(f"Value Loss: {avg_losses['value_loss']:.6f}")
                print(f"Total Loss: {avg_losses['total_loss']:.6f}")
            else:
                print(f"\nSkipping training: buffer size {len(replay_buffer)} < min_size")
            
            # Update iteration
            training_state['iteration'] = iteration + 1
            
            # Update temperature
            temp_decay = config.get('self_play.temperature_decay', 0.99)
            training_state['current_temperature'] *= temp_decay
            self_play.temperature = training_state['current_temperature']
            
            # Save checkpoint (periodic numbered checkpoints)
            if (iteration + 1) % save_frequency == 0:
                checkpoint_path = checkpoints_dir / f"checkpoint_{iteration + 1:06d}.pth"
                print(f"\nSaving checkpoint to {checkpoint_path}")
                model.save(str(checkpoint_path))
                
                # Save training state
                training_state['checkpoint_path'] = str(checkpoint_path)
                with open(state_path, 'w') as f:
                    json.dump(training_state, f, indent=2)
            
            # Always save latest.pth after each iteration (for recovery)
            latest_path = checkpoints_dir / "latest.pth"
            model.save(str(latest_path))
            
            # Save configuration
            if (iteration + 1) % config_save_frequency == 0:
                config_path_iter = checkpoints_dir / f"iteration_{iteration + 1:06d}_config.yaml"
                print(f"\nSaving configuration to {config_path_iter}")
                save_configuration(
                    config.config,
                    str(config_path_iter),
                    model,
                    training_state
                )
                
                # Update latest config
                latest_config_path = checkpoints_dir / "latest_config.yaml"
                save_configuration(
                    config.config,
                    str(latest_config_path),
                    model,
                    training_state
                )
    
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
        print("Saving checkpoint...")
        model.save(str(checkpoints_dir / "latest.pth"))
        with open(state_path, 'w') as f:
            json.dump(training_state, f, indent=2)
        print("Checkpoint saved.")
    
    print("\n" + "="*70)
    print("Training completed!")
    print("="*70)


if __name__ == "__main__":
    main()

