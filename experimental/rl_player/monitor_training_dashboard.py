#!/usr/bin/env python3
"""
Dashboard interattiva per monitorare il training con grafici.

Usage:
    python experimental/rl_player/monitor_training_dashboard.py
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠ matplotlib not installed. Install with: pip install matplotlib")


def load_training_history(checkpoint_dir: Path) -> List[Dict]:
    """Carica storico training da file di log o checkpoint."""
    history = []
    
    # Cerca file di log
    log_dir = checkpoint_dir.parent / "logs"
    if log_dir.exists():
        for log_file in log_dir.glob("training_*.json"):
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        history.extend(data)
                    else:
                        history.append(data)
            except:
                pass
    
    # Ordina per iterazione
    history.sort(key=lambda x: x.get('iteration', 0))
    return history


def plot_training_progress(checkpoint_dir: Path):
    """Crea grafici del progresso training."""
    if not HAS_MATPLOTLIB:
        print("Cannot create plots: matplotlib not installed")
        return
    
    state = load_training_state(checkpoint_dir)
    history = load_training_history(checkpoint_dir)
    
    if not state and not history:
        print("No training data found to plot")
        return
    
    # Crea figura con subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('RL Training Progress', fontsize=16)
    
    # Plot 1: Loss over iterations
    ax1 = axes[0, 0]
    if history:
        iterations = [h.get('iteration', 0) for h in history]
        policy_losses = [h.get('policy_loss', 0) for h in history]
        value_losses = [h.get('value_loss', 0) for h in history]
        total_losses = [h.get('total_loss', 0) for h in history]
        
        ax1.plot(iterations, policy_losses, label='Policy Loss', alpha=0.7)
        ax1.plot(iterations, value_losses, label='Value Loss', alpha=0.7)
        ax1.plot(iterations, total_losses, label='Total Loss', alpha=0.7)
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Loss')
        ax1.set_title('Training Loss')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    else:
        ax1.text(0.5, 0.5, 'No loss data available', 
                ha='center', va='center', transform=ax1.transAxes)
    
    # Plot 2: Games played
    ax2 = axes[0, 1]
    if state:
        games_played = state.get('games_played', 0)
        iterations = state.get('iteration', 0)
        
        ax2.bar(['Games Played', 'Iterations'], [games_played, iterations])
        ax2.set_ylabel('Count')
        ax2.set_title('Training Progress')
        ax2.grid(True, alpha=0.3, axis='y')
    else:
        ax2.text(0.5, 0.5, 'No progress data available',
                ha='center', va='center', transform=ax2.transAxes)
    
    # Plot 3: Checkpoint timeline
    ax3 = axes[1, 0]
    checkpoint_info = get_checkpoint_info(checkpoint_dir)
    if checkpoint_info['all_checkpoints']:
        checkpoints = checkpoint_info['all_checkpoints']
        iterations = [cp['iteration'] for cp in checkpoints]
        timestamps = [cp['modified'] for cp in checkpoints]
        
        ax3.scatter(timestamps, iterations, alpha=0.6)
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Iteration')
        ax3.set_title('Checkpoint Timeline')
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax3.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        ax3.grid(True, alpha=0.3)
    else:
        ax3.text(0.5, 0.5, 'No checkpoint data available',
                ha='center', va='center', transform=ax3.transAxes)
    
    # Plot 4: Training speed
    ax4 = axes[1, 1]
    if state and 'start_time' in state:
        start_time = datetime.fromtimestamp(state['start_time'])
        elapsed = (datetime.now() - start_time).total_seconds()
        iterations = state.get('iteration', 1)
        
        if iterations > 0:
            iter_per_hour = (iterations / elapsed) * 3600
            games_per_hour = (state.get('games_played', 0) / elapsed) * 3600
            
            ax4.bar(['Iterations/hour', 'Games/hour'], 
                   [iter_per_hour, games_per_hour])
            ax4.set_ylabel('Rate')
            ax4.set_title('Training Speed')
            ax4.grid(True, alpha=0.3, axis='y')
    else:
        ax4.text(0.5, 0.5, 'No speed data available',
                ha='center', va='center', transform=ax4.transAxes)
    
    plt.tight_layout()
    
    # Salva grafico
    output_path = checkpoint_dir.parent / "training_progress.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved to: {output_path}")
    
    # Mostra grafico
    try:
        plt.show()
    except:
        print("(Cannot display plot in this environment)")


def load_training_state(checkpoint_dir: Path) -> Optional[Dict]:
    """Carica training state."""
    state_path = checkpoint_dir / "training_state.json"
    if state_path.exists():
        with open(state_path, 'r') as f:
            return json.load(f)
    return None


def get_checkpoint_info(checkpoint_dir: Path) -> Dict:
    """Ottieni info sui checkpoint."""
    info = {
        'latest': None,
        'best': None,
        'all_checkpoints': []
    }
    
    if not checkpoint_dir.exists():
        return info
    
    for checkpoint_file in checkpoint_dir.glob("checkpoint_*.pth"):
        stat = checkpoint_file.stat()
        try:
            iter_num = int(checkpoint_file.stem.split('_')[1])
            info['all_checkpoints'].append({
                'iteration': iter_num,
                'modified': datetime.fromtimestamp(stat.st_mtime)
            })
        except:
            pass
    
    info['all_checkpoints'].sort(key=lambda x: x['iteration'])
    return info


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Training progress dashboard")
    parser.add_argument(
        '--checkpoint-dir',
        type=str,
        default='experimental/checkpoints',
        help='Path to checkpoint directory'
    )
    parser.add_argument(
        '--save-only',
        action='store_true',
        help='Save plot without displaying'
    )
    
    args = parser.parse_args()
    
    checkpoint_dir = Path(args.checkpoint_dir)
    if not checkpoint_dir.is_absolute():
        checkpoint_dir = project_root / checkpoint_dir
    
    if not checkpoint_dir.exists():
        print(f"Error: Checkpoint directory not found: {checkpoint_dir}")
        sys.exit(1)
    
    plot_training_progress(checkpoint_dir)


if __name__ == "__main__":
    main()

