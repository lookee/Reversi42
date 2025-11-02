#!/bin/bash
# Start WebSocket server for Reversi42 game bridge

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEBGUI_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
PROJECT_ROOT="$( cd "$WEBGUI_DIR/../.." && pwd )"

# Use system Python instead of Anaconda
PYTHON_BIN="/Library/Developer/CommandLineTools/usr/bin/python3"

# Set PYTHONPATH to include project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Start the server
echo "🚀 Starting Reversi42 Backend Server..."
echo "   Project Root: $PROJECT_ROOT"
echo "   Port: 8000"
echo "   AI Player: DIVZERO.EXE"
echo ""

$PYTHON_BIN -m src.webgui.server.reversi42_server --port 8000 --player DIVZERO.EXE
