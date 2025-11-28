"""
Script di setup per Google Colab/Kaggle.

Usage in Colab:
  1. Upload questo file
  2. Esegui: !python setup_colab.py
"""

import subprocess
import sys
import os

def install_dependencies():
    """Installa dipendenze per training cloud."""
    print("=" * 70)
    print("Setting up Cloud Training Environment")
    print("=" * 70)
    print()
    
    # Installa PyTorch con CUDA
    print("Installing PyTorch with CUDA support...")
    subprocess.run([
        sys.executable, '-m', 'pip', 'install',
        'torch', 'torchvision', 'torchaudio',
        '--index-url', 'https://download.pytorch.org/whl/cu118'
    ], check=True)
    print("✓ PyTorch installed")
    print()
    
    # Installa altre dipendenze
    print("Installing other dependencies...")
    dependencies = [
        'numpy<2.0.0',  # Compatibilità PyTorch
        'tqdm',
        'tensorboard',
        'wandb',
        'h5py',
        'pyyaml'
    ]
    
    for dep in dependencies:
        subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)
    
    print("✓ Dependencies installed")
    print()
    
    # Verifica GPU
    print("Checking GPU availability...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
            print(f"✓ CUDA version: {torch.version.cuda}")
            print(f"✓ GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        else:
            print("⚠ No GPU available, will use CPU")
            print("  Note: Training will be much slower on CPU")
    except Exception as e:
        print(f"⚠ Error checking GPU: {e}")
    
    print()
    print("=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Upload your Reversi42 project")
    print("  2. Modify neural_network.py to use CUDA")
    print("  3. Run training script")
    print()


if __name__ == "__main__":
    install_dependencies()

