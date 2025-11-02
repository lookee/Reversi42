#!/bin/bash
# Script to run all WebGUI tests
# Usage: ./scripts/run_webgui_tests.sh [options]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Print header
print_header() {
    echo ""
    print_message "$BLUE" "========================================="
    print_message "$BLUE" "$1"
    print_message "$BLUE" "========================================="
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main script
main() {
    print_header "Reversi42 WebGUI Test Suite"
    
    # Change to project root
    cd "$(dirname "$0")/.."
    
    # Parse arguments
    RUN_BACKEND=true
    RUN_OBSERVER=true
    RUN_FRONTEND=true
    RUN_E2E=false
    VERBOSE=false
    COVERAGE=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backend-only)
                RUN_OBSERVER=false
                RUN_FRONTEND=false
                RUN_E2E=false
                shift
                ;;
            --observer-only)
                RUN_BACKEND=false
                RUN_FRONTEND=false
                RUN_E2E=false
                shift
                ;;
            --frontend-only)
                RUN_BACKEND=false
                RUN_OBSERVER=false
                RUN_E2E=false
                shift
                ;;
            --e2e)
                RUN_E2E=true
                shift
                ;;
            --all)
                RUN_BACKEND=true
                RUN_OBSERVER=true
                RUN_FRONTEND=true
                RUN_E2E=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -c|--coverage)
                COVERAGE=true
                shift
                ;;
            -h|--help)
                print_message "$GREEN" "Usage: $0 [options]"
                echo ""
                echo "Options:"
                echo "  --backend-only      Run only backend tests"
                echo "  --observer-only     Run only observer tests"
                echo "  --frontend-only     Run only frontend tests"
                echo "  --e2e              Include E2E tests (requires server)"
                echo "  --all              Run all tests including E2E"
                echo "  -v, --verbose      Verbose output"
                echo "  -c, --coverage     Generate coverage report"
                echo "  -h, --help         Show this help"
                echo ""
                exit 0
                ;;
            *)
                print_message "$RED" "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Check Python
    if ! command_exists python3; then
        print_message "$RED" "Error: Python 3 is not installed"
        exit 1
    fi
    
    print_message "$GREEN" "✓ Python 3 found: $(python3 --version)"
    
    # Check pytest
    if ! python3 -m pytest --version >/dev/null 2>&1; then
        print_message "$RED" "Error: pytest is not installed"
        print_message "$YELLOW" "Install with: pip install pytest pytest-asyncio"
        exit 1
    fi
    
    print_message "$GREEN" "✓ pytest found"
    
    # Build pytest command
    PYTEST_CMD="python3 -m pytest"
    
    if [ "$VERBOSE" = true ]; then
        PYTEST_CMD="$PYTEST_CMD -v -s"
    else
        PYTEST_CMD="$PYTEST_CMD -v"
    fi
    
    if [ "$COVERAGE" = true ]; then
        PYTEST_CMD="$PYTEST_CMD --cov=src/webgui --cov-report=html --cov-report=term"
    fi
    
    # Run backend tests
    if [ "$RUN_BACKEND" = true ]; then
        print_header "Running Backend Tests"
        $PYTEST_CMD tests/webgui/test_backend_server.py
        if [ $? -eq 0 ]; then
            print_message "$GREEN" "✓ Backend tests passed"
        else
            print_message "$RED" "✗ Backend tests failed"
            exit 1
        fi
    fi
    
    # Run observer tests
    if [ "$RUN_OBSERVER" = true ]; then
        print_header "Running Observer Tests"
        $PYTEST_CMD tests/webgui/test_websocket_observer.py
        if [ $? -eq 0 ]; then
            print_message "$GREEN" "✓ Observer tests passed"
        else
            print_message "$RED" "✗ Observer tests failed"
            exit 1
        fi
    fi
    
    # Run frontend tests
    if [ "$RUN_FRONTEND" = true ]; then
        print_header "Running Frontend Tests"
        
        if ! command_exists npm; then
            print_message "$YELLOW" "Warning: npm not found, skipping frontend tests"
            print_message "$YELLOW" "Install Node.js to run frontend tests"
        else
            cd tests/webgui
            
            # Install dependencies if needed
            if [ ! -d "node_modules" ]; then
                print_message "$YELLOW" "Installing Node.js dependencies..."
                npm install
            fi
            
            npm test
            if [ $? -eq 0 ]; then
                print_message "$GREEN" "✓ Frontend tests passed"
            else
                print_message "$RED" "✗ Frontend tests failed"
                cd ../..
                exit 1
            fi
            
            cd ../..
        fi
    fi
    
    # Run E2E tests
    if [ "$RUN_E2E" = true ]; then
        print_header "Running E2E Tests"
        
        # Check if Playwright is installed
        if ! python3 -c "import playwright" >/dev/null 2>&1; then
            print_message "$YELLOW" "Warning: Playwright not installed"
            print_message "$YELLOW" "Install with: pip install pytest-playwright && playwright install"
            print_message "$YELLOW" "Skipping E2E tests"
        else
            # Check if server is running
            if curl -s http://localhost:8000 >/dev/null 2>&1; then
                print_message "$GREEN" "✓ Server is running"
                $PYTEST_CMD tests/webgui/test_e2e.py
                if [ $? -eq 0 ]; then
                    print_message "$GREEN" "✓ E2E tests passed"
                else
                    print_message "$RED" "✗ E2E tests failed"
                    exit 1
                fi
            else
                print_message "$YELLOW" "Warning: Server not running at http://localhost:8000"
                print_message "$YELLOW" "Start server with: python src/webgui/backend_server.py --port 8000"
                print_message "$YELLOW" "Skipping E2E tests"
            fi
        fi
    fi
    
    # Summary
    print_header "Test Summary"
    
    if [ "$COVERAGE" = true ]; then
        print_message "$GREEN" "Coverage report generated at: htmlcov/index.html"
        
        # Try to open coverage report
        if command_exists open; then
            print_message "$BLUE" "Opening coverage report..."
            open htmlcov/index.html
        elif command_exists xdg-open; then
            xdg-open htmlcov/index.html
        fi
    fi
    
    print_message "$GREEN" "✓ All selected tests passed!"
    echo ""
}

# Run main
main "$@"

