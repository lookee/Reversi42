#!/bin/bash

#------------------------------------------------------------------------
# Build Reversi42 for Windows
# Creates standalone .exe file
#------------------------------------------------------------------------

echo "========================================"
echo "Building Reversi42 for Windows"
echo "========================================"
echo

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Change to project root
cd "$PROJECT_ROOT"
echo "Working directory: $PROJECT_ROOT"
echo

# Check if pyinstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Error: PyInstaller not found"
    echo "Install with: pip install pyinstaller"
    exit 1
fi

# Set version
VERSION="0.2.0"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist *.spec
rm -rf pyinstaller_build

# Build executable
echo "Building Windows executable..."
pyinstaller --onefile \
    --windowed \
    --name=Reversi42 \
    --add-data="src:src" \
    --hidden-import=pygame.gfxdraw \
    --hidden-import=pygame.locals \
    --distpath=dist \
    --workpath=pyinstaller_build \
    --specpath=. \
    reversi42

if [ $? -eq 0 ]; then
    echo
    echo "✓ Build successful!"
    echo "  Executable: dist/Reversi42.exe"
    echo "  Size: $(du -h dist/Reversi42.exe | cut -f1)"
    echo
    echo "To test:"
    echo "  wine dist/Reversi42.exe  (on Linux/macOS)"
    echo "  dist\\Reversi42.exe      (on Windows)"
else
    echo
    echo "✗ Build failed!"
    exit 1
fi

# Optional: Create ZIP for distribution
echo "Creating distribution ZIP..."
cd dist
zip -r Reversi42-Windows-${VERSION}.zip Reversi42.exe
cd ..

echo
echo "✓ Distribution package created:"
echo "  dist/Reversi42-Windows-${VERSION}.zip"
echo

