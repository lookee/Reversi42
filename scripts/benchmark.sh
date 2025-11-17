#!/bin/bash
# Run performance benchmarks for Reversi42
# Usage: ./scripts/benchmark.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set headless mode for benchmarks
export REVERSI42_VIEW=headless

# Run Python benchmark script
python3 "$(dirname "$0")/benchmark.py"

