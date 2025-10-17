# Building Reversi42 for Distribution

This guide explains how to create distributable packages for Windows, Linux (Ubuntu), and macOS.

## Prerequisites

### All Platforms
- Python 3.6+
- pip
- Virtual environment (recommended)

### Install PyInstaller
```bash
pip install pyinstaller
```

### Platform-Specific Tools

**Windows:**
- Windows 10/11 or Wine on Linux/macOS
- NSIS (Nullsoft Scriptable Install System) for installer

**Linux (Ubuntu):**
- `dpkg-deb` (usually pre-installed)
- `fakeroot` for package building

**macOS:**
- Xcode Command Line Tools
- `create-dmg` (optional, for DMG creation)

---

## Building for Windows

### Step 1: Build Executable with PyInstaller

```bash
# On Windows or using Wine
cd /path/to/Reversi42

# Create Windows executable
pyinstaller --onefile \
    --windowed \
    --name=Reversi42 \
    --icon=src/Images/icon.ico \
    --add-data="src:src" \
    reversi42

# Output: dist/Reversi42.exe
```

### Step 2: Create Installer with NSIS (Optional)

Create `installer.nsi`:
```nsis
!include "MUI2.nsh"

Name "Reversi42"
OutFile "Reversi42-Setup.exe"
InstallDir "$PROGRAMFILES\Reversi42"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File "dist\Reversi42.exe"
    File /r "src"
    CreateShortcut "$DESKTOP\Reversi42.lnk" "$INSTDIR\Reversi42.exe"
SectionEnd
```

Build installer:
```bash
makensis installer.nsi
```

### Alternative: Use build script
```bash
./build/build_windows.sh
```

---

## Building for Linux (Ubuntu/Debian)

### Step 1: Build Executable

```bash
# On Linux
cd /path/to/Reversi42

# Create Linux executable
pyinstaller --onefile \
    --name=reversi42 \
    --add-data="src:src" \
    reversi42

# Output: dist/reversi42
```

### Step 2: Create .deb Package

```bash
# Use provided script
./build/build_linux_deb.sh

# Or manually:
./build/create_deb_package.sh
```

Package structure:
```
reversi42_0.2.0_amd64/
├── DEBIAN/
│   └── control
└── usr/
    ├── bin/
    │   └── reversi42
    ├── share/
    │   ├── applications/
    │   │   └── reversi42.desktop
    │   ├── icons/
    │   │   └── reversi42.png
    │   └── reversi42/
    │       └── src/
```

Build:
```bash
dpkg-deb --build reversi42_0.2.0_amd64
```

Install:
```bash
sudo dpkg -i reversi42_0.2.0_amd64.deb
```

---

## Building for macOS

### Step 1: Build App Bundle

```bash
# On macOS
cd /path/to/Reversi42

# Create macOS app bundle
pyinstaller --onefile \
    --windowed \
    --name=Reversi42 \
    --icon=src/Images/icon.icns \
    --add-data="src:src" \
    --osx-bundle-identifier=com.lucaamore.reversi42 \
    reversi42

# Output: dist/Reversi42.app
```

### Step 2: Create DMG (Optional)

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
    --volname "Reversi42" \
    --window-pos 200 120 \
    --window-size 800 400 \
    --icon-size 100 \
    --icon "Reversi42.app" 200 190 \
    --hide-extension "Reversi42.app" \
    --app-drop-link 600 185 \
    "Reversi42.dmg" \
    "dist/Reversi42.app"
```

### Alternative: Use build script
```bash
./build/build_macos.sh
```

---

## Automated Build Scripts

We provide automated build scripts for all platforms:

### Quick Build All Platforms

```bash
# Build everything (requires platform-specific tools)
./build/build_all.sh
```

### Individual Platform Builds

```bash
# Windows
./build/build_windows.sh

# Linux (Ubuntu/Debian)
./build/build_linux_deb.sh

# macOS
./build/build_macos.sh
```

---

## Testing Builds

### Windows
```cmd
dist\Reversi42.exe
```

### Linux
```bash
./dist/reversi42
# Or after installing .deb:
reversi42
```

### macOS
```bash
open dist/Reversi42.app
```

---

## Distribution

### File Sizes (Approximate)
- Windows EXE: ~15-20 MB
- Linux binary: ~15-20 MB
- macOS .app: ~20-25 MB
- With DMG/installer: +5-10 MB

### Checksums

Generate checksums for distribution:
```bash
# SHA256
sha256sum dist/Reversi42.exe > Reversi42-windows.sha256
sha256sum reversi42_0.2.0_amd64.deb > Reversi42-linux.sha256
sha256sum Reversi42.dmg > Reversi42-macos.sha256
```

---

## Troubleshooting

### PyInstaller Issues

**Missing modules:**
```bash
pyinstaller --hidden-import=pygame.gfxdraw reversi42
```

**Large file size:**
```bash
# Use --onefile and exclude unnecessary modules
pyinstaller --onefile --exclude-module matplotlib reversi42
```

### Platform-Specific Issues

**Windows:**
- Antivirus may flag PyInstaller executables
- Sign the executable to avoid warnings

**Linux:**
- Ensure all dependencies in .deb control file
- Test on clean Ubuntu installation

**macOS:**
- Code signing required for distribution
- Notarization needed for macOS 10.15+

---

## Advanced: Code Signing

### macOS
```bash
codesign --deep --force --verify --verbose \
    --sign "Developer ID Application: Your Name" \
    dist/Reversi42.app
```

### Windows
Requires a code signing certificate:
```bash
signtool sign /f certificate.pfx /p password \
    /t http://timestamp.digicert.com \
    dist/Reversi42.exe
```

---

## Release Checklist

- [ ] Update version number in all files
- [ ] Test on target platform
- [ ] Build executable
- [ ] Test executable on clean system
- [ ] Generate checksums
- [ ] Create release notes
- [ ] Tag git release
- [ ] Upload to distribution platform

---

See individual build scripts in `build/` directory for detailed implementation.

