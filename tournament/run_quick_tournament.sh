#!/bin/bash

#------------------------------------------------------------------------
#    Reversi42 - Quick Tournament Runner
#    
#    Runs the quick tournament using configuration from ring/
#------------------------------------------------------------------------

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configuration file
CONFIG_FILE="$SCRIPT_DIR/ring/quick_tournament.json"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                    REVERSI42 - QUICK TOURNAMENT RUNNER                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Configuration: ring/quick_tournament.json"
echo ""

# Run tournament with configuration
cd "$SCRIPT_DIR"
python3 tournament.py --config "$CONFIG_FILE"

exit $?

