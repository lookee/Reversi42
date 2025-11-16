#!/bin/bash
# Build executables for Windows, Linux, and macOS using PyInstaller
# Usage: ./scripts/build_executables.sh [version]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get version from pyproject.toml if not provided
if [ -z "$1" ]; then
    VERSION=$(grep -E '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/' | tr -d ' ')
    if [ -z "$VERSION" ]; then
        echo -e "${RED}Error: Could not determine version${NC}"
        echo "Usage: $0 [version]"
        exit 1
    fi
    echo -e "${BLUE}Using version from pyproject.toml: ${VERSION}${NC}"
else
    VERSION=$1
fi

# Detect OS
OS=$(uname -s)
ARCH=$(uname -m)

echo -e "${BLUE}🔨 Building Reversi42 Executables${NC}"
echo "======================================"
echo "Version: ${VERSION}"
echo "OS: ${OS}"
echo "Architecture: ${ARCH}"
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${YELLOW}⚠️  PyInstaller not found. Installing...${NC}"
    pip install pyinstaller
fi

# Install build dependencies
echo -e "\n${BLUE}→ Installing build dependencies...${NC}"
pip install -q -e ".[build]" || pip install -q pyinstaller setuptools wheel

# Clean previous builds
echo -e "\n${BLUE}→ Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.spec.bak

# Build executable
echo -e "\n${BLUE}→ Building executable...${NC}"
pyinstaller reversi42.spec --clean --noconfirm

# Check if build succeeded
if [ ! -f "dist/reversi42" ] && [ ! -f "dist/reversi42.exe" ]; then
    echo -e "${RED}❌ Build failed - executable not found${NC}"
    exit 1
fi

# Determine executable name and extension
if [ "$OS" = "Darwin" ]; then
    EXE_NAME="reversi42-macos-${ARCH}"
    EXE_EXT=""
    PLATFORM="macOS"
elif [ "$OS" = "Linux" ]; then
    EXE_NAME="reversi42-linux-${ARCH}"
    EXE_EXT=""
    PLATFORM="Linux"
elif [[ "$OS" == MINGW* ]] || [[ "$OS" == MSYS* ]] || [[ "$OS" == CYGWIN* ]]; then
    EXE_NAME="reversi42-windows-${ARCH}"
    EXE_EXT=".exe"
    PLATFORM="Windows"
else
    EXE_NAME="reversi42-${OS}-${ARCH}"
    EXE_EXT=""
    PLATFORM="${OS}"
fi

# Rename executable with version
FINAL_NAME="${EXE_NAME}-${VERSION}${EXE_EXT}"
if [ -f "dist/reversi42${EXE_EXT}" ]; then
    mv "dist/reversi42${EXE_EXT}" "dist/${FINAL_NAME}"
    echo -e "${GREEN}✅ Build successful!${NC}"
    echo ""
    echo "Executable: dist/${FINAL_NAME}"
    ls -lh "dist/${FINAL_NAME}"
    
    # Create archive
    echo -e "\n${BLUE}→ Creating archive...${NC}"
    cd dist
    if [ "$OS" = "Darwin" ]; then
        zip -q "${FINAL_NAME}.zip" "${FINAL_NAME}"
        echo "Archive: dist/${FINAL_NAME}.zip"
    elif [ "$OS" = "Linux" ]; then
        tar -czf "${FINAL_NAME}.tar.gz" "${FINAL_NAME}"
        echo "Archive: dist/${FINAL_NAME}.tar.gz"
    else
        zip -q "${FINAL_NAME}.zip" "${FINAL_NAME}"
        echo "Archive: dist/${FINAL_NAME}.zip"
    fi
    cd ..
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Build complete!${NC}"
echo ""
echo "To test the executable:"
echo "  ./dist/${FINAL_NAME} --help"

