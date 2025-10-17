#!/bin/bash

#------------------------------------------------------------------------
# Build Reversi42 for Linux (Ubuntu/Debian)
# Creates .deb package
#------------------------------------------------------------------------

echo "========================================"
echo "Building Reversi42 for Linux (DEB)"
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
ARCH="amd64"
PKG_NAME="reversi42_${VERSION}_${ARCH}"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist *.spec ${PKG_NAME} ${PKG_NAME}.deb
rm -rf pyinstaller_build

# Build executable
echo "Building Linux executable..."
pyinstaller --onefile \
    --name=reversi42 \
    --add-data="src:src" \
    --hidden-import=pygame.gfxdraw \
    --hidden-import=pygame.locals \
    --distpath=dist \
    --workpath=pyinstaller_build \
    --specpath=. \
    reversi42

if [ $? -ne 0 ]; then
    echo "✗ PyInstaller build failed!"
    exit 1
fi

echo "✓ Executable built successfully"

# Create DEB package structure
echo
echo "Creating DEB package structure..."

mkdir -p ${PKG_NAME}/DEBIAN
mkdir -p ${PKG_NAME}/usr/bin
mkdir -p ${PKG_NAME}/usr/share/applications
mkdir -p ${PKG_NAME}/usr/share/icons/hicolor/256x256/apps
mkdir -p ${PKG_NAME}/usr/share/doc/reversi42

# Copy executable
cp dist/reversi42 ${PKG_NAME}/usr/bin/
chmod +x ${PKG_NAME}/usr/bin/reversi42

# Create control file
cat > ${PKG_NAME}/DEBIAN/control << EOF
Package: reversi42
Version: ${VERSION}
Section: games
Priority: optional
Architecture: ${ARCH}
Depends: python3, python3-pygame
Maintainer: Luca Amore <luca.amore@gmail.com>
Description: Complete Reversi/Othello game with AI
 Reversi42 is a complete implementation of the classic Reversi (Othello)
 board game featuring:
 - Full GUI with Pygame
 - AI opponent with configurable difficulty
 - Multiple player types and strategies
 - Tournament system with statistics
 - Save/Load functionality
Homepage: https://www.lucaamore.com
EOF

# Create desktop entry
cat > ${PKG_NAME}/usr/share/applications/reversi42.desktop << EOF
[Desktop Entry]
Type=Application
Name=Reversi42
Comment=Classic Reversi/Othello game with AI
Exec=/usr/bin/reversi42
Icon=reversi42
Terminal=false
Categories=Game;BoardGame;
Keywords=reversi;othello;board;game;
EOF

# Copy documentation
cp README ${PKG_NAME}/usr/share/doc/reversi42/
cp COPYING ${PKG_NAME}/usr/share/doc/reversi42/

# Build DEB package
echo
echo "Building DEB package..."
dpkg-deb --build ${PKG_NAME}

if [ $? -eq 0 ]; then
    echo
    echo "✓ DEB package created successfully!"
    echo "  Package: ${PKG_NAME}.deb"
    echo "  Size: $(du -h ${PKG_NAME}.deb | cut -f1)"
    echo
    echo "To install:"
    echo "  sudo dpkg -i ${PKG_NAME}.deb"
    echo
    echo "To remove:"
    echo "  sudo dpkg -r reversi42"
else
    echo "✗ DEB package build failed!"
    exit 1
fi

# Cleanup build directory
echo "Cleaning up..."
rm -rf ${PKG_NAME}

echo
echo "✓ Build complete!"

