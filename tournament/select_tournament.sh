#!/bin/bash

#------------------------------------------------------------------------
#    Reversi42 - Interactive Tournament Selector
#    
#    Select and run pre-configured tournaments from the ring directory
#------------------------------------------------------------------------

# Colors for better UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RING_DIR="$SCRIPT_DIR/ring"

# Check if ring directory exists
if [ ! -d "$RING_DIR" ]; then
    echo -e "${RED}ERROR: Ring directory not found: $RING_DIR${NC}"
    exit 1
fi

# Function to display tournament info from JSON
get_tournament_info() {
    local config_file="$1"
    local field="$2"
    
    # Use Python to parse JSON (more reliable than jq)
    python3 -c "import json; f=open('$config_file'); d=json.load(f); print(d.get('$field', ''))" 2>/dev/null
}

# Function to count players in tournament
count_players() {
    local config_file="$1"
    python3 -c "import json; f=open('$config_file'); d=json.load(f); print(len(d.get('players', [])))" 2>/dev/null
}

# Function to get games per matchup
get_games_per_matchup() {
    local config_file="$1"
    python3 -c "import json; f=open('$config_file'); d=json.load(f); print(d.get('games_per_matchup', 0))" 2>/dev/null
}

# Display header
clear
echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                    REVERSI42 - TOURNAMENT SELECTOR                             ║"
echo "║                     Interactive Tournament Launcher                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Find all JSON files in ring directory
configs=($(ls -1 "$RING_DIR"/*.json 2>/dev/null | sort))

if [ ${#configs[@]} -eq 0 ]; then
    echo -e "${RED}No tournament configurations found in ring/${NC}"
    exit 1
fi

echo -e "${BOLD}Available Tournaments:${NC}"
echo ""

# Display tournaments with details
# Note: We'll use parallel arrays instead of associative array for bash 3.x compatibility
tournament_indices=()
tournament_files=()
index=1

for config in "${configs[@]}"; do
    tournament_indices+=($index)
    tournament_files+=("$config")
    config_name=$(basename "$config")
    name=$(get_tournament_info "$config" "name")
    description=$(get_tournament_info "$config" "description")
    players=$(count_players "$config")
    games=$(get_games_per_matchup "$config")
    
    # Calculate total games
    if [ -n "$players" ] && [ -n "$games" ]; then
        total_games=$((players * (players - 1) * games))
    else
        total_games="?"
    fi
    
    # Color based on tournament type
    if [[ "$config_name" == *"quick"* ]]; then
        color="${GREEN}"
        badge="⚡ QUICK"
    elif [[ "$config_name" == *"elite"* ]] || [[ "$config_name" == *"champion"* ]]; then
        color="${YELLOW}"
        badge="🏆 ELITE"
    elif [[ "$config_name" == *"grandmaster"* ]] || [[ "$config_name" == *"challenge"* ]]; then
        color="${MAGENTA}"
        badge="👑 ULTIMATE"
    elif [[ "$config_name" == *"beginner"* ]] || [[ "$config_name" == *"rapid"* ]]; then
        color="${CYAN}"
        badge="🎓 EASY"
    else
        color="${BLUE}"
        badge="📊 TEST"
    fi
    
    # Display tournament option
    echo -e "${color}${BOLD}[$index]${NC} ${badge} ${BOLD}${name}${NC}"
    echo -e "    ${description}"
    echo -e "    ${CYAN}Players:${NC} $players  ${CYAN}Games/Matchup:${NC} $games  ${CYAN}Total Games:${NC} $total_games"
    echo -e "    ${YELLOW}File:${NC} $config_name"
    echo ""
    
    ((index++))
done

echo -e "${BOLD}[0]${NC} ${RED}Exit${NC}"
echo ""

# Prompt for selection
echo -e -n "${BOLD}${GREEN}Select tournament [0-$((${#configs[@]}))]:${NC} "
read selection

# Validate input
if ! [[ "$selection" =~ ^[0-9]+$ ]]; then
    echo -e "${RED}Invalid input. Please enter a number.${NC}"
    exit 1
fi

# Check for exit
if [ "$selection" -eq 0 ]; then
    echo -e "${YELLOW}Exiting...${NC}"
    exit 0
fi

# Validate range
if [ "$selection" -lt 1 ] || [ "$selection" -gt ${#configs[@]} ]; then
    echo -e "${RED}Invalid selection. Please choose between 1 and ${#configs[@]}.${NC}"
    exit 1
fi

# Get selected configuration (using array index)
selected_config="${tournament_files[$((selection-1))]}"
config_name=$(basename "$selected_config")

# Display selection
echo ""
echo -e "${GREEN}${BOLD}Selected:${NC} $config_name"
echo ""

# Get tournament details for confirmation
name=$(get_tournament_info "$selected_config" "name")
description=$(get_tournament_info "$selected_config" "description")
players=$(count_players "$selected_config")
games=$(get_games_per_matchup "$selected_config")
total_games=$((players * (players - 1) * games))

# Estimate runtime
if [ "$players" -le 3 ]; then
    runtime="~1-3 minutes"
elif [ "$players" -le 5 ]; then
    if [ "$games" -le 2 ]; then
        runtime="~5-10 minutes"
    else
        runtime="~15-25 minutes"
    fi
elif [ "$players" -le 7 ]; then
    if [ "$games" -le 2 ]; then
        runtime="~10-15 minutes"
    else
        runtime="~30-45 minutes"
    fi
else
    if [ "$games" -le 2 ]; then
        runtime="~15-25 minutes"
    else
        runtime="~45-90 minutes"
    fi
fi

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC} ${BOLD}Tournament Details${NC}                                            ${CYAN}║${NC}"
echo -e "${CYAN}╠════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC} Name:           ${BOLD}${name}${NC}"
echo -e "${CYAN}║${NC} Description:    ${description}"
echo -e "${CYAN}║${NC}"
echo -e "${CYAN}║${NC} Players:        ${BOLD}${players}${NC}"
echo -e "${CYAN}║${NC} Games/Matchup:  ${BOLD}${games}${NC}"
echo -e "${CYAN}║${NC} Total Games:    ${BOLD}${total_games}${NC}"
echo -e "${CYAN}║${NC} Est. Runtime:   ${BOLD}${runtime}${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Ask for confirmation
echo -e -n "${YELLOW}${BOLD}Start this tournament? [Y/n]:${NC} "
read confirm

if [[ "$confirm" =~ ^[Nn] ]]; then
    echo -e "${YELLOW}Tournament cancelled.${NC}"
    exit 0
fi

# Run the tournament
echo ""
echo -e "${GREEN}${BOLD}Starting tournament...${NC}"
echo ""

cd "$SCRIPT_DIR"
python3 tournament.py --config "$selected_config"

exit_code=$?

# Display completion message
echo ""
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ Tournament completed successfully!${NC}"
    echo -e "${CYAN}Report saved in: ${SCRIPT_DIR}/reports/${NC}"
else
    echo -e "${RED}${BOLD}✗ Tournament failed with exit code: $exit_code${NC}"
fi

exit $exit_code

