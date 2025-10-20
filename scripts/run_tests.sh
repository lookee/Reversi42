#!/bin/bash
# Run complete test suite for Reversi42
# Usage: ./scripts/run_tests.sh [--fast|--coverage|--all]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Reversi42 Test Suite${NC}"
echo "======================================"

# Parse arguments
MODE=${1:-all}

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

case $MODE in
  --fast)
    echo -e "${BLUE}Running fast tests only...${NC}"
    pytest tests/ -v -m "not slow" --tb=short
    ;;
  
  --coverage)
    echo -e "${BLUE}Running tests with coverage...${NC}"
    pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
    echo -e "${GREEN}✅ Coverage report: htmlcov/index.html${NC}"
    ;;
  
  --all)
    echo -e "${BLUE}Running complete test suite...${NC}"
    
    # Unit tests
    echo -e "\n${BLUE}→ Unit Tests${NC}"
    pytest tests/apocalyptron/unit/ -v
    
    # Integration tests
    echo -e "\n${BLUE}→ Integration Tests${NC}"
    pytest tests/apocalyptron/integration/ -v
    
    # Characterization tests
    echo -e "\n${BLUE}→ Characterization Tests${NC}"
    pytest tests/apocalyptron/characterization/ -v
    
    echo -e "\n${GREEN}✅ All tests passed!${NC}"
    ;;
  
  *)
    echo -e "${RED}Unknown mode: $MODE${NC}"
    echo "Usage: $0 [--fast|--coverage|--all]"
    exit 1
    ;;
esac

exit 0

