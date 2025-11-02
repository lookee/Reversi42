#!/bin/bash
# Start WebSocket server for Reversi42 game bridge

# Use system Python instead of Anaconda
PYTHON_BIN="/Library/Developer/CommandLineTools/usr/bin/python3"

# Set PYTHONPATH to include project root
export PYTHONPATH="/Users/lucaamore/Documents/devel/Reversi42:$PYTHONPATH"

# Start the server
$PYTHON_BIN -m src.webgui.backend_server --port 8000 --player DIVZERO.EXE
