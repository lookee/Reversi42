#!/bin/bash
# Backend Server Startup Script with Monitor

# Configuration
PORT=${1:-8000}
PLAYER=${2:-"DIVZERO.EXE"}
MAX_RESTARTS=${3:-10}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Reversi42 Backend Server with Monitor${NC}"
echo -e "${BLUE}   Port: ${PORT}${NC}"
echo -e "${BLUE}   Player: ${PLAYER}${NC}"
echo -e "${BLUE}   Max Restarts: ${MAX_RESTARTS}${NC}"
echo ""

# Kill any existing processes
echo -e "${YELLOW}🔄 Cleaning up existing processes...${NC}"
pkill -f "backend_server" 2>/dev/null || true
pkill -f "backend_monitor" 2>/dev/null || true
sleep 2

# Check if Python is available
PYTHON_PATH="/Library/Developer/CommandLineTools/usr/bin/python3"
if [ ! -f "$PYTHON_PATH" ]; then
    echo -e "${RED}❌ Python not found at $PYTHON_PATH${NC}"
    echo -e "${RED}   Please install Xcode Command Line Tools${NC}"
    exit 1
fi

# Check if required modules are available
echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
if ! $PYTHON_PATH -c "import fastapi, uvicorn" 2>/dev/null; then
    echo -e "${RED}❌ FastAPI not installed${NC}"
    echo -e "${RED}   Please install: pip install fastapi uvicorn${NC}"
    exit 1
fi

# Set environment
export PYTHONPATH="/Users/lucaamore/Documents/devel/Reversi42:$PYTHONPATH"

# Start the monitor
echo -e "${GREEN}🎯 Starting backend monitor...${NC}"
cd /Users/lucaamore/Documents/devel/Reversi42

$PYTHON_PATH -m src.webgui.backend_monitor \
    --port $PORT \
    --player "$PLAYER" \
    --max-restarts $MAX_RESTARTS &

MONITOR_PID=$!

echo -e "${GREEN}✅ Monitor started with PID $MONITOR_PID${NC}"
echo -e "${BLUE}📊 Monitor logs: tail -f /tmp/backend_monitor.log${NC}"
echo -e "${BLUE}📊 Backend logs: tail -f /tmp/backend.log${NC}"
echo -e "${BLUE}📊 Detailed logs: tail -f /tmp/backend_detailed.log${NC}"
echo ""
echo -e "${GREEN}🌐 Server should be available at: http://localhost:$PORT${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the monitor${NC}"

# Wait for monitor
wait $MONITOR_PID

echo -e "${RED}🛑 Monitor stopped${NC}"
