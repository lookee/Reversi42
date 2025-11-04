#!/bin/bash
# Reversi42 - Development Mode Runner
# Quick launch script for development environment
# Usage: ./dev.sh [options]
#
# Examples:
#   ./dev.sh                           # Start with defaults
#   ./dev.sh --port 3000               # Custom port
#   ./dev.sh --reload                  # Auto-reload on changes
#   ./dev.sh --list-players            # List all AI players
#   ./dev.sh --help                    # Show help

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory (project root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$PROJECT_ROOT/src"

# Check if src directory exists
if [ ! -d "$SRC_DIR" ]; then
    echo -e "${RED}❌ Error: src/ directory not found${NC}"
    echo "   Make sure you're in the project root directory"
    exit 1
fi

# Activate virtual environment if exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
    source "$PROJECT_ROOT/venv/bin/activate"
elif [ -d "$PROJECT_ROOT/.venv" ]; then
    echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
    source "$PROJECT_ROOT/.venv/bin/activate"
else
    echo -e "${YELLOW}⚠️  No virtual environment found${NC}"
    echo "   Consider running: ./scripts/setup_dev.sh"
    echo ""
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${BLUE}🐍 Python version: $python_version${NC}"

# Set PYTHONPATH to include src directory
export PYTHONPATH="$SRC_DIR:$PYTHONPATH"

# Print info
echo -e "${GREEN}🎮 Starting Reversi42 in development mode...${NC}"
echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"
echo -e "${BLUE}📦 Source directory: $SRC_DIR${NC}"
echo ""

# Run the application
cd "$PROJECT_ROOT"
python3 -m webgui.cli "$@"

