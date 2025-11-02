#!/bin/bash
# Setup script for WebGUI test environment
# Usage: ./scripts/setup_webgui_tests.sh

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_message() {
    echo -e "${1}${2}${NC}"
}

print_header() {
    echo ""
    print_message "$BLUE" "========================================="
    print_message "$BLUE" "$1"
    print_message "$BLUE" "========================================="
    echo ""
}

# Change to project root
cd "$(dirname "$0")/.."

print_header "Reversi42 WebGUI Test Setup"

# Check Python
print_message "$BLUE" "Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_message "$RED" "Error: Python 3 is not installed"
    exit 1
fi
print_message "$GREEN" "✓ Python found: $(python3 --version)"

# Install Python dependencies
print_header "Installing Python Dependencies"
print_message "$BLUE" "Installing from requirements-dev.txt..."
pip install -r requirements-dev.txt
print_message "$GREEN" "✓ Python dependencies installed"

# Install Playwright browsers
print_header "Installing Playwright Browsers"
print_message "$BLUE" "This may take a few minutes..."
playwright install chromium firefox webkit
print_message "$GREEN" "✓ Playwright browsers installed"

# Check Node.js
print_header "Setting up JavaScript Tests"
if ! command -v node &> /dev/null; then
    print_message "$YELLOW" "Warning: Node.js not found"
    print_message "$YELLOW" "JavaScript tests will not be available"
    print_message "$YELLOW" "Install Node.js from: https://nodejs.org/"
else
    print_message "$GREEN" "✓ Node.js found: $(node --version)"
    
    # Install Node dependencies
    print_message "$BLUE" "Installing JavaScript dependencies..."
    cd tests/webgui
    npm install
    cd ../..
    print_message "$GREEN" "✓ JavaScript dependencies installed"
fi

# Verify setup
print_header "Verifying Setup"

# Check pytest
if python3 -m pytest --version &> /dev/null; then
    print_message "$GREEN" "✓ pytest is ready"
else
    print_message "$RED" "✗ pytest installation failed"
    exit 1
fi

# Check pytest-asyncio
if python3 -c "import pytest_asyncio" 2>/dev/null; then
    print_message "$GREEN" "✓ pytest-asyncio is ready"
else
    print_message "$YELLOW" "⚠ pytest-asyncio may not be installed"
fi

# Check playwright
if python3 -c "import playwright" 2>/dev/null; then
    print_message "$GREEN" "✓ Playwright is ready"
else
    print_message "$YELLOW" "⚠ Playwright may not be installed"
fi

# Check Jest (if Node.js is available)
if command -v node &> /dev/null; then
    if [ -d "tests/webgui/node_modules" ]; then
        print_message "$GREEN" "✓ Jest is ready"
    else
        print_message "$YELLOW" "⚠ Jest may not be installed"
    fi
fi

# Summary
print_header "Setup Complete!"

echo "You can now run tests with:"
echo ""
echo "  # All tests (except E2E)"
echo "  ./scripts/run_webgui_tests.sh"
echo ""
echo "  # With coverage"
echo "  ./scripts/run_webgui_tests.sh --coverage"
echo ""
echo "  # Backend only"
echo "  pytest tests/webgui/test_backend_server.py -v"
echo ""
echo "  # Frontend only"
echo "  cd tests/webgui && npm test"
echo ""
echo "  # E2E tests (start server first!)"
echo "  python src/webgui/backend_server.py --port 8000 &"
echo "  pytest tests/webgui/test_e2e.py -v"
echo ""

print_message "$GREEN" "✓ Setup completed successfully!"
print_message "$BLUE" "For more information, see: docs/WEBGUI_TESTING.md"
echo ""

