#!/bin/bash

#------------------------------------------------------------------------
# Build Reversi42 for macOS
# Creates .app bundle and optional .dmg
#------------------------------------------------------------------------

echo "========================================"
echo "Building Reversi42 for macOS"
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

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Warning: Not running on macOS"
    echo "Cross-compilation may not work correctly"
fi

# Set version
VERSION="0.2.0"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist *.spec Reversi42.dmg
# Clean PyInstaller temp build directory (different from our build/ scripts directory)
rm -rf pyinstaller_build

# Build app bundle
echo "Building macOS app bundle..."
pyinstaller --onefile \
    --windowed \
    --name=Reversi42 \
    --add-data="src:src" \
    --osx-bundle-identifier=com.lucaamore.reversi42 \
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

echo "✓ App bundle built successfully"

# Create Info.plist with proper metadata
echo
echo "Updating Info.plist..."
cat > dist/Reversi42.app/Contents/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>Reversi42</string>
    <key>CFBundleName</key>
    <string>Reversi42</string>
    <key>CFBundleIdentifier</key>
    <string>com.lucaamore.reversi42</string>
    <key>CFBundleVersion</key>
    <string>${VERSION}</string>
    <key>CFBundleShortVersionString</key>
    <string>${VERSION}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleExecutable</key>
    <string>Reversi42</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2011-2025 Luca Amore</string>
</dict>
</plist>
EOF

echo "✓ Info.plist updated"

# Optional: Create DMG
if command -v create-dmg &> /dev/null; then
    echo
    echo "Creating DMG installer..."
    
    create-dmg \
        --volname "Reversi42" \
        --volicon "src/Images/icon.icns" \
        --window-pos 200 120 \
        --window-size 800 400 \
        --icon-size 100 \
        --icon "Reversi42.app" 200 190 \
        --hide-extension "Reversi42.app" \
        --app-drop-link 600 185 \
        --no-internet-enable \
        "Reversi42-${VERSION}.dmg" \
        "dist/Reversi42.app"
    
    if [ $? -eq 0 ]; then
        echo "✓ DMG created successfully!"
        echo "  File: Reversi42-${VERSION}.dmg"
        echo "  Size: $(du -h Reversi42-${VERSION}.dmg | cut -f1)"
    fi
else
    echo
    echo "Note: create-dmg not found. Skipping DMG creation."
    echo "Install with: brew install create-dmg"
    echo "App bundle is still available: dist/Reversi42.app"
fi

echo
echo "✓ macOS build complete!"
echo
echo "Output files:"
echo "  - dist/Reversi42.app (Application bundle)"
if [ -f "Reversi42-${VERSION}.dmg" ]; then
    echo "  - Reversi42-${VERSION}.dmg (Installer)"
fi
echo
echo "To test:"
echo "  open dist/Reversi42.app"
echo

