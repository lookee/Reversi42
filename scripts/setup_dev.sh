#!/bin/bash
# Setup development environment for Reversi42
# Usage: ./scripts/setup_dev.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🛠️  Setting up Reversi42 Development Environment${NC}"
echo "======================================"

# Check Python version
echo -e "\n${BLUE}→ Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo -e "${RED}❌ Python 3.9+ required (found: ${PYTHON_VERSION})${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python ${PYTHON_VERSION}${NC}"

# Create virtual environment
echo -e "\n${BLUE}→ Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
    read -p "Recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi
echo -e "${GREEN}✅ Virtual environment ready${NC}"

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "\n${BLUE}→ Upgrading pip...${NC}"
pip install --upgrade pip wheel setuptools
echo -e "${GREEN}✅ pip upgraded${NC}"

# Install production dependencies
echo -e "\n${BLUE}→ Installing production dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✅ Production dependencies installed${NC}"

# Install development dependencies
echo -e "\n${BLUE}→ Installing development dependencies...${NC}"
pip install -r requirements-dev.txt
echo -e "${GREEN}✅ Development dependencies installed${NC}"

# Install package in editable mode
echo -e "\n${BLUE}→ Installing package in editable mode...${NC}"
pip install -e .
echo -e "${GREEN}✅ Package installed${NC}"

# Setup pre-commit hooks (optional)
echo -e "\n${BLUE}→ Setting up pre-commit hooks (optional)...${NC}"
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo -e "${GREEN}✅ Pre-commit hooks installed${NC}"
else
    echo -e "${YELLOW}⚠️  pre-commit not installed (optional)${NC}"
    echo "Install with: pip install pre-commit"
fi

# Make scripts executable
echo -e "\n${BLUE}→ Making scripts executable...${NC}"
chmod +x scripts/*.sh
chmod +x reversi42
echo -e "${GREEN}✅ Scripts executable${NC}"

# Verify installation
echo -e "\n${BLUE}→ Verifying installation...${NC}"
python -c "from src.Reversi.BitboardGame import BitboardGame; print('  BitboardGame import: OK')"
python -c "from src.Players.PlayerApocalyptron import PlayerApocalyptron; print('  PlayerApocalyptron import: OK')"
echo -e "${GREEN}✅ Installation verified${NC}"

# Run quick test
echo -e "\n${BLUE}→ Running quick test...${NC}"
pytest tests/ -v --tb=short -x -k "test_initial" 2>&1 | head -n 20
echo -e "${GREEN}✅ Tests working${NC}"

# Summary
echo -e "\n======================================"
echo -e "${GREEN}✅ Development environment ready!${NC}"
echo ""
echo "Next steps:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run tests: ./scripts/run_tests.sh"
echo "  3. Check code quality: ./scripts/check_quality.sh"
echo "  4. Run game: ./reversi42"
echo ""
echo "Documentation:"
echo "  - Development Guide: docs/development/README.md"
echo "  - Contributing: CONTRIBUTING.md"
echo "  - API Reference: docs/api/README.md"
echo ""
echo -e "${BLUE}Happy coding! 🚀${NC}"

