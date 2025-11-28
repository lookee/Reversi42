#!/bin/bash

# Script per avviare il training dalla directory rl_player
# Questo script gestisce correttamente i percorsi Python

set -e

# Get project root (3 levels up from this script)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

# Change to project root
cd "$PROJECT_ROOT"

# Activate conda environment if available
if command -v conda &> /dev/null; then
    # Try to activate reversi42_rl if it exists
    if conda env list | grep -q "^reversi42_rl "; then
        eval "$(conda shell.bash hook)"
        conda activate reversi42_rl
    fi
fi

# Set PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/src:$PYTHONPATH"

# Run training
echo "Project root: $PROJECT_ROOT"
echo "Python path: $PYTHONPATH"
echo ""
python "$SCRIPT_DIR/train.py"

