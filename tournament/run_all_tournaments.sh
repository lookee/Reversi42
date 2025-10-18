#!/bin/bash

#------------------------------------------------------------------------
#    Reversi42 - Run All Tournaments
#    
#    Executes all tournament configurations in the ring directory
#    and generates comprehensive summary report
#------------------------------------------------------------------------

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RING_DIR="$SCRIPT_DIR/ring"
REPORTS_DIR="$SCRIPT_DIR/reports"

# Check ring directory exists
if [ ! -d "$RING_DIR" ]; then
    echo -e "${RED}ERROR: Ring directory not found: $RING_DIR${NC}"
    exit 1
fi

# Create reports directory if it doesn't exist
mkdir -p "$REPORTS_DIR"

# Find all tournament configurations
configs=($(ls -1 "$RING_DIR"/*.json 2>/dev/null | sort))

if [ ${#configs[@]} -eq 0 ]; then
    echo -e "${RED}ERROR: No tournament configurations found in ring/${NC}"
    exit 1
fi

# Display header
clear
echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                   REVERSI42 - RUN ALL TOURNAMENTS                              ║"
echo "║                   Automated Tournament Batch Execution                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Display tournaments to be run
echo -e "${BOLD}${GREEN}Found ${#configs[@]} tournaments to run:${NC}"
echo ""

total_games=0
total_estimated_time=0

for config in "${configs[@]}"; do
    config_name=$(basename "$config")
    name=$(python3 -c "import json; print(json.load(open('$config')).get('name', 'Unknown'))" 2>/dev/null)
    players=$(python3 -c "import json; print(len(json.load(open('$config')).get('players', [])))" 2>/dev/null)
    games_per=$(python3 -c "import json; print(json.load(open('$config')).get('games_per_matchup', 0))" 2>/dev/null)
    
    if [ -n "$players" ] && [ -n "$games_per" ]; then
        games=$((players * (players - 1) * games_per))
        total_games=$((total_games + games))
        
        # Rough time estimate (depends on tournament type)
        if [ "$players" -le 3 ]; then
            est_time=2
        elif [ "$players" -le 5 ]; then
            if [ "$games_per" -le 2 ]; then
                est_time=10
            else
                est_time=20
            fi
        elif [ "$players" -le 7 ]; then
            if [ "$games_per" -le 2 ]; then
                est_time=15
            else
                est_time=40
            fi
        else
            if [ "$games_per" -le 2 ]; then
                est_time=20
            else
                est_time=60
            fi
        fi
        
        total_estimated_time=$((total_estimated_time + est_time))
    else
        games="?"
        est_time="?"
    fi
    
    echo -e "  ${CYAN}•${NC} ${BOLD}$name${NC}"
    echo -e "    ${YELLOW}File:${NC} $config_name | ${CYAN}Players:${NC} $players | ${CYAN}Games:${NC} $games | ${CYAN}Est:${NC} ~${est_time}min"
done

echo ""
echo -e "${BOLD}${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}Total Statistics:${NC}"
echo -e "  ${CYAN}Tournaments:${NC} ${BOLD}${#configs[@]}${NC}"
echo -e "  ${CYAN}Total Games:${NC} ${BOLD}${total_games}${NC}"
echo -e "  ${CYAN}Estimated Time:${NC} ${BOLD}~${total_estimated_time} minutes (${BOLD}~$((total_estimated_time / 60))h $((total_estimated_time % 60))m${NC})"
echo -e "${BOLD}${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Warning for long execution
if [ $total_estimated_time -gt 60 ]; then
    echo -e "${YELLOW}${BOLD}⚠️  WARNING: This will take significant time (~$((total_estimated_time / 60)) hours)${NC}"
    echo -e "${YELLOW}   Consider running in background or using screen/tmux${NC}"
    echo ""
fi

# Ask for confirmation
echo -e -n "${BOLD}${GREEN}Run all tournaments? [y/N]:${NC} "
read confirm

if [[ ! "$confirm" =~ ^[Yy] ]]; then
    echo -e "${YELLOW}Cancelled by user.${NC}"
    exit 0
fi

# Create summary log
timestamp=$(date +"%Y%m%d_%H%M%S")
summary_log="$REPORTS_DIR/all_tournaments_summary_${timestamp}.txt"
batch_start=$(date +%s)

echo ""
echo -e "${GREEN}${BOLD}Starting batch execution...${NC}"
echo -e "${CYAN}Summary will be saved to: ${summary_log}${NC}"
echo ""

# Initialize summary
{
    echo "╔════════════════════════════════════════════════════════════════════════════════╗"
    echo "║              REVERSI42 - ALL TOURNAMENTS BATCH EXECUTION SUMMARY               ║"
    echo "╚════════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Execution Start: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Total Tournaments: ${#configs[@]}"
    echo "Total Games: ${total_games}"
    echo ""
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo ""
} > "$summary_log"

# Execute each tournament
success_count=0
failed_count=0
completed_tournaments=()
failed_tournaments=()

for i in "${!configs[@]}"; do
    config="${configs[$i]}"
    config_name=$(basename "$config")
    tournament_num=$((i + 1))
    
    echo -e "${BOLD}${CYAN}[$tournament_num/${#configs[@]}]${NC} ${BOLD}Running: $config_name${NC}"
    
    tournament_start=$(date +%s)
    
    # Run tournament (non-interactive)
    cd "$SCRIPT_DIR"
    if python3 tournament.py --config "$config" > /dev/null 2>&1; then
        tournament_end=$(date +%s)
        duration=$((tournament_end - tournament_start))
        
        echo -e "  ${GREEN}✓ Completed in ${duration}s ($(($duration / 60))m $(($duration % 60))s)${NC}"
        
        # Log to summary
        {
            echo "[$tournament_num] $config_name"
            echo "  Status: SUCCESS"
            echo "  Duration: ${duration}s ($(($duration / 60))m $(($duration % 60))s)"
            echo ""
        } >> "$summary_log"
        
        success_count=$((success_count + 1))
        completed_tournaments+=("$config_name")
    else
        tournament_end=$(date +%s)
        duration=$((tournament_end - tournament_start))
        
        echo -e "  ${RED}✗ Failed after ${duration}s${NC}"
        
        # Log to summary
        {
            echo "[$tournament_num] $config_name"
            echo "  Status: FAILED"
            echo "  Duration: ${duration}s"
            echo ""
        } >> "$summary_log"
        
        failed_count=$((failed_count + 1))
        failed_tournaments+=("$config_name")
    fi
    
    echo ""
done

batch_end=$(date +%s)
total_duration=$((batch_end - batch_start))

# Finalize summary
{
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "BATCH EXECUTION COMPLETED"
    echo ""
    echo "Execution End: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Total Duration: ${total_duration}s ($(($total_duration / 60))m $(($total_duration % 60))s)"
    echo ""
    echo "Results:"
    echo "  Successful: $success_count / ${#configs[@]}"
    echo "  Failed: $failed_count / ${#configs[@]}"
    echo ""
    
    if [ $success_count -gt 0 ]; then
        echo "Completed Tournaments:"
        for tournament in "${completed_tournaments[@]}"; do
            echo "  ✓ $tournament"
        done
        echo ""
    fi
    
    if [ $failed_count -gt 0 ]; then
        echo "Failed Tournaments:"
        for tournament in "${failed_tournaments[@]}"; do
            echo "  ✗ $tournament"
        done
        echo ""
    fi
    
    echo "Individual reports saved in: $REPORTS_DIR"
    echo ""
    echo "════════════════════════════════════════════════════════════════════════════════"
} >> "$summary_log"

# Display final summary
echo ""
echo -e "${BOLD}${GREEN}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}║                        BATCH EXECUTION COMPLETED                               ║${NC}"
echo -e "${BOLD}${GREEN}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}Summary:${NC}"
echo -e "  ${CYAN}Total Tournaments:${NC} ${#configs[@]}"
echo -e "  ${GREEN}Successful:${NC} $success_count"
echo -e "  ${RED}Failed:${NC} $failed_count"
echo -e "  ${CYAN}Total Duration:${NC} $(($total_duration / 60))m $(($total_duration % 60))s"
echo ""
echo -e "${BOLD}Reports:${NC}"
echo -e "  ${CYAN}Individual reports:${NC} $REPORTS_DIR/tournament_report_*.txt"
echo -e "  ${CYAN}Batch summary:${NC} $summary_log"
echo ""

if [ $failed_count -gt 0 ]; then
    echo -e "${YELLOW}${BOLD}⚠️  Some tournaments failed:${NC}"
    for tournament in "${failed_tournaments[@]}"; do
        echo -e "  ${RED}✗${NC} $tournament"
    done
    echo ""
fi

if [ $success_count -eq ${#configs[@]} ]; then
    echo -e "${GREEN}${BOLD}✓ All tournaments completed successfully!${NC}"
    exit 0
else
    echo -e "${YELLOW}${BOLD}⚠️  Batch completed with errors${NC}"
    exit 1
fi

