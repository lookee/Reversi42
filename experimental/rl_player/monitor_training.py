#!/usr/bin/env python3
"""
Script per monitorare l'andamento del training RL.

Usage:
    python experimental/rl_player/monitor_training.py [--checkpoint-dir DIR] [--watch]
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


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
    
    # Trova latest.pth
    latest_path = checkpoint_dir / "latest.pth"
    if latest_path.exists():
        stat = latest_path.stat()
        info['latest'] = {
            'path': str(latest_path),
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': datetime.fromtimestamp(stat.st_mtime)
        }
    
    # Trova best.pth
    best_path = checkpoint_dir / "best.pth"
    if best_path.exists():
        stat = best_path.stat()
        info['best'] = {
            'path': str(best_path),
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': datetime.fromtimestamp(stat.st_mtime)
        }
    
    # Trova tutti i checkpoint numerati
    for checkpoint_file in checkpoint_dir.glob("checkpoint_*.pth"):
        stat = checkpoint_file.stat()
        # Estrai numero iterazione dal nome
        try:
            iter_num = int(checkpoint_file.stem.split('_')[1])
            info['all_checkpoints'].append({
                'iteration': iter_num,
                'path': str(checkpoint_file),
                'size_mb': stat.st_size / (1024 * 1024),
                'modified': datetime.fromtimestamp(stat.st_mtime)
            })
        except (ValueError, IndexError):
            pass
    
    info['all_checkpoints'].sort(key=lambda x: x['iteration'])
    return info


def format_duration(seconds: float) -> str:
    """Formatta durata in formato leggibile."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_size(size_mb: float) -> str:
    """Formatta dimensione."""
    if size_mb < 1024:
        return f"{size_mb:.1f} MB"
    else:
        return f"{size_mb/1024:.2f} GB"


def display_training_status(checkpoint_dir: Path, watch: bool = False):
    """Mostra stato del training."""
    
    while True:
        # Clear screen (se watch mode)
        if watch:
            os.system('clear' if os.name != 'nt' else 'cls')
        
        print("=" * 80)
        print("RL Training Monitor")
        print("=" * 80)
        print(f"Checkpoint directory: {checkpoint_dir}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Training state
        state = load_training_state(checkpoint_dir)
        if state:
            print("📊 Training State")
            print("-" * 80)
            print(f"  Iteration: {state.get('iteration', 0):,}")
            print(f"  Games played: {state.get('games_played', 0):,}")
            print(f"  Current temperature: {state.get('current_temperature', 1.0):.4f}")
            
            # Calcola tempo stimato
            if 'start_time' in state:
                start_time = datetime.fromtimestamp(state['start_time'])
                elapsed = datetime.now() - start_time
                print(f"  Training started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Elapsed time: {format_duration(elapsed.total_seconds())}")
                
                # Stima tempo rimanente (se abbiamo iterazioni)
                if state.get('iteration', 0) > 0:
                    avg_time_per_iter = elapsed.total_seconds() / state['iteration']
                    max_iterations = state.get('max_iterations', 1000000)
                    remaining_iters = max_iterations - state['iteration']
                    remaining_time = avg_time_per_iter * remaining_iters
                    print(f"  Estimated time remaining: {format_duration(remaining_time)}")
            
            print()
        else:
            print("⚠ No training state found")
            print()
        
        # Checkpoint info
        checkpoint_info = get_checkpoint_info(checkpoint_dir)
        
        print("💾 Checkpoints")
        print("-" * 80)
        
        if checkpoint_info['latest']:
            latest = checkpoint_info['latest']
            age = datetime.now() - latest['modified']
            print(f"  Latest: {Path(latest['path']).name}")
            print(f"    Size: {format_size(latest['size_mb'])}")
            print(f"    Modified: {latest['modified'].strftime('%Y-%m-%d %H:%M:%S')} ({format_duration(age.total_seconds())} ago)")
        else:
            print("  Latest: Not found")
        
        if checkpoint_info['best']:
            best = checkpoint_info['best']
            age = datetime.now() - best['modified']
            print(f"  Best: {Path(best['path']).name}")
            print(f"    Size: {format_size(best['size_mb'])}")
            print(f"    Modified: {best['modified'].strftime('%Y-%m-%d %H:%M:%S')} ({format_duration(age.total_seconds())} ago)")
        else:
            print("  Best: Not found")
        
        if checkpoint_info['all_checkpoints']:
            print(f"\n  Numbered checkpoints: {len(checkpoint_info['all_checkpoints'])}")
            print("  Recent checkpoints:")
            for cp in checkpoint_info['all_checkpoints'][-5:]:
                age = datetime.now() - cp['modified']
                print(f"    Iteration {cp['iteration']:,}: {format_duration(age.total_seconds())} ago")
        
        print()
        
        # Replay buffer info (se disponibile)
        replay_buffer_path = checkpoint_dir.parent / "training_data" / "replay_buffer.h5"
        if replay_buffer_path.exists():
            stat = replay_buffer_path.stat()
            print("📦 Replay Buffer")
            print("-" * 80)
            print(f"  Size: {format_size(stat.st_size / (1024 * 1024))}")
            print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        
        # Log files (se disponibili)
        log_dir = checkpoint_dir.parent / "logs"
        if log_dir.exists():
            log_files = list(log_dir.glob("*.log"))
            if log_files:
                latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
                stat = latest_log.stat()
                print("📝 Logs")
                print("-" * 80)
                print(f"  Latest log: {latest_log.name}")
                print(f"  Size: {format_size(stat.st_size / (1024 * 1024))}")
                print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Mostra ultime righe del log
                try:
                    with open(latest_log, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            print(f"\n  Last log entries:")
                            for line in lines[-5:]:
                                print(f"    {line.rstrip()}")
                except:
                    pass
                print()
        
        # TensorBoard logs (se disponibili)
        tb_log_dir = checkpoint_dir.parent / "logs" / "tensorboard"
        if tb_log_dir.exists():
            print("📈 TensorBoard")
            print("-" * 80)
            print(f"  Log directory: {tb_log_dir}")
            print(f"  View with: tensorboard --logdir {tb_log_dir}")
            print()
        
        # Progress bar (se abbiamo info)
        if state:
            max_iterations = state.get('max_iterations', 1000000)
            current_iter = state.get('iteration', 0)
            if max_iterations > 0:
                progress = (current_iter / max_iterations) * 100
                bar_length = 50
                filled = int(bar_length * current_iter / max_iterations)
                bar = '█' * filled + '░' * (bar_length - filled)
                print("📊 Progress")
                print("-" * 80)
                print(f"  [{bar}] {progress:.2f}%")
                print(f"  {current_iter:,} / {max_iterations:,} iterations")
                print()
        
        # Se non in watch mode, esci
        if not watch:
            break
        
        # Attendi prima di aggiornare
        print("Press Ctrl+C to stop monitoring...")
        time.sleep(5)


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor RL training progress")
    parser.add_argument(
        '--checkpoint-dir',
        type=str,
        default='experimental/checkpoints',
        help='Path to checkpoint directory'
    )
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch mode: continuously update display'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Update interval in seconds (watch mode)'
    )
    
    args = parser.parse_args()
    
    # Resolve checkpoint directory
    checkpoint_dir = Path(args.checkpoint_dir)
    if not checkpoint_dir.is_absolute():
        checkpoint_dir = project_root / checkpoint_dir
    
    if not checkpoint_dir.exists():
        print(f"Error: Checkpoint directory not found: {checkpoint_dir}")
        sys.exit(1)
    
    try:
        display_training_status(checkpoint_dir, watch=args.watch)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


if __name__ == "__main__":
    main()

