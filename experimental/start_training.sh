#!/bin/bash

# Script per avviare il training del giocatore RL
# Usage: ./start_training.sh

set -e

echo "=========================================="
echo "RL Player Training - Startup Script"
echo "=========================================="
echo ""

# Check if we're in the right directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Check if PyTorch is installed
echo "Checking PyTorch installation..."
if python3 -c "import torch; print(f'PyTorch {torch.__version__}')" 2>/dev/null; then
    echo "✓ PyTorch is installed"
    # Check MPS support
    if python3 -c "import torch; print('MPS available:', torch.backends.mps.is_available())" 2>/dev/null; then
        python3 -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
    fi
else
    echo "✗ PyTorch is NOT installed"
    echo ""
    echo "Please install dependencies first:"
    echo "  pip install -r experimental/requirements-rl.txt"
    exit 1
fi
echo ""

# Check if required packages are installed
echo "Checking required packages..."
missing_packages=()
for package in numpy tqdm yaml; do
    if ! python3 -c "import $package" 2>/dev/null; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "✗ Missing packages: ${missing_packages[*]}"
    echo ""
    echo "Please install dependencies:"
    echo "  pip install -r experimental/requirements-rl.txt"
    exit 1
else
    echo "✓ All required packages are installed"
fi
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p experimental/checkpoints
mkdir -p experimental/config
mkdir -p experimental/training_data
echo "✓ Directories created"
echo ""

# Check if config file exists
if [ ! -f "experimental/config/rl_config.yaml" ]; then
    echo "⚠ Config file not found, using defaults"
else
    echo "✓ Config file found"
fi
echo ""

# Start training
echo "=========================================="
echo "Starting RL Player Training"
echo "=========================================="
echo ""
echo "Training will:"
echo "  - Create/load model from checkpoints/"
echo "  - Generate self-play games"
echo "  - Train on replay buffer"
echo "  - Save checkpoints every 1000 iterations"
echo "  - Save configurations every 1000 iterations"
echo ""
echo "Press Ctrl+C to stop training (checkpoint will be saved)"
echo ""
echo "=========================================="
echo ""

# Navigate to rl_player directory and run training script
if [ -d "rl_player" ]; then
    cd rl_player
    # Use the run_training.sh script which handles paths correctly
    if [ -f "run_training.sh" ]; then
        bash run_training.sh
    else
        # Fallback: set PYTHONPATH and run directly
        export PYTHONPATH="$(pwd)/../..:$(pwd)/../../src:$PYTHONPATH"
        python train.py
    fi
else
    echo "❌ Error: Cannot find rl_player directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

