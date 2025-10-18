#!/bin/bash

#------------------------------------------------------------------------
#    Reversi42 - Tournament Configuration Runner
#    
#    Runs a tournament using a specified configuration file from ring/
#------------------------------------------------------------------------

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if configuration file is provided
if [ $# -eq 0 ]; then
    echo "╔════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                    REVERSI42 - TOURNAMENT RUNNER                               ║"
    echo "╚════════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Usage: $0 <config_name>"
    echo ""
    echo "Available configurations in ring/:"
    echo ""
    
    # List available configurations
    if [ -d "$SCRIPT_DIR/ring" ]; then
        for config in "$SCRIPT_DIR/ring"/*.json; do
            if [ -f "$config" ]; then
                basename "$config"
            fi
        done
    else
        echo "  (No configurations found)"
    fi
    echo ""
    echo "Examples:"
    echo "  $0 quick_tournament.json"
    echo "  $0 evaluator_comparison.json"
    echo "  $0 ring/custom_config.json  (with path)"
    echo ""
    exit 1
fi

CONFIG_NAME="$1"

# Determine full path to config file
if [[ "$CONFIG_NAME" == */* ]]; then
    # Path provided (contains /)
    CONFIG_FILE="$CONFIG_NAME"
else
    # Just filename, look in ring/
    CONFIG_FILE="$SCRIPT_DIR/ring/$CONFIG_NAME"
fi

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Configuration file not found: $CONFIG_FILE"
    echo ""
    echo "Available configurations:"
    ls -1 "$SCRIPT_DIR/ring"/*.json 2>/dev/null | xargs -n 1 basename
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                    REVERSI42 - TOURNAMENT RUNNER                               ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Configuration: $CONFIG_FILE"
echo ""

# Run tournament with configuration
cd "$SCRIPT_DIR"
python3 tournament.py --config "$CONFIG_FILE"

exit $?

