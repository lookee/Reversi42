#!/bin/bash
# Test build prerequisites

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo "Testing Build Setup"
echo "==================="
echo

echo "1. Python: $(python3 --version 2>&1 || echo 'NOT FOUND')"
echo "2. pip: $(pip3 --version 2>&1 | head -1 || echo 'NOT FOUND')"
echo "3. pygame: $(python3 -c 'import pygame; print(pygame.version.ver)' 2>/dev/null || echo 'NOT FOUND')"
echo "4. PyInstaller: $(pyinstaller --version 2>&1 || echo 'NOT FOUND - Install with: pip install pyinstaller')"
echo

if command -v pyinstaller &> /dev/null && python3 -c "import pygame" 2>/dev/null; then
    echo "✓ Ready to build!"
else
    echo "✗ Install missing dependencies:"
    echo "  pip install -r build/requirements-build.txt"
fi
