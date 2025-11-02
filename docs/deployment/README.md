# Deployment Guide

Complete guide for deploying and distributing Reversi42.

## Quick Links

- [**Installation**](installation.md) - How to install Reversi42
- [**Platform-Specific Guides**](platforms/) - macOS, Windows, Linux
- [**Building Distributions**](building.md) - Create executables
- [**Package Management**](packaging.md) - PyPI, Homebrew, etc.
- [**Docker**](docker.md) - Containerized deployment
- [**Configuration**](configuration.md) - Post-install configuration

## Installation Methods

### Method 1: From Source (Recommended for Development)

```bash
# Clone repository
git clone https://github.com/lucaamore/reversi42.git
cd reversi42

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
./reversi42
# or
python3 src/reversi42.py
```

### Method 2: PyPI (When Available)

```bash
pip install reversi42
reversi42
```

### Method 3: Pre-built Binary

Download from [Releases](https://github.com/lucaamore/reversi42/releases):

- **macOS**: `reversi42-macos.dmg`
- **Windows**: `reversi42-windows.exe`
- **Linux**: `reversi42-linux.AppImage`

## Platform-Specific Installation

### macOS

```bash
# Using Homebrew (planned)
brew install reversi42

# Or from DMG
# Download reversi42-macos.dmg
# Drag to Applications folder
```

**Requirements**:
- macOS 10.14 or later
- Python 3.9+ (for source install)

### Windows

```bash
# Using installer
# Download reversi42-setup.exe
# Run installer

# Or using Scoop (planned)
scoop install reversi42
```

**Requirements**:
- Windows 10 or later
- Python 3.9+ (for source install)

### Linux

```bash
# Using AppImage
chmod +x reversi42-linux.AppImage
./reversi42-linux.AppImage

# Or Snap (planned)
snap install reversi42

# Or from source
git clone https://github.com/lucaamore/reversi42.git
cd reversi42
pip install -r requirements.txt
./reversi42
```

**Requirements**:
- Modern Linux distribution
- Python 3.9+
- SDL2 libraries (usually pre-installed)

## System Requirements

### Minimum Requirements

- **OS**: macOS 10.14+, Windows 10+, or Linux (any modern distro)
- **CPU**: 1 GHz processor
- **RAM**: 512 MB
- **Storage**: 50 MB
- **Display**: 800x600 resolution

### Recommended Requirements

- **OS**: macOS 13+, Windows 11+, or Linux
- **CPU**: Multi-core processor (2+ cores for AI)
- **RAM**: 2 GB
- **Storage**: 100 MB
- **Display**: 1920x1080 or higher

### For Tournament/AI Development

- **CPU**: 4+ cores (for parallel search)
- **RAM**: 4 GB
- **Storage**: 200 MB (for logs and game database)

## Building from Source

### Build Tools

```bash
# Install build dependencies
pip install -r requirements-build.txt

# Install platform tools
# macOS: Xcode Command Line Tools
xcode-select --install

# Windows: Visual Studio Build Tools
# Download from Microsoft

# Linux: build-essential
sudo apt-get install build-essential
```

### Building Executables

```bash
cd build

# Build for your platform
./build_all.sh

# Or platform-specific
./build_macos.sh
./build_windows.sh
./build_linux.sh
```

See [Building Guide](building.md) for details.

## Docker Deployment

### Running in Docker

```bash
# Pull image (when available)
docker pull lucaamore/reversi42:latest

# Or build locally
docker build -t reversi42 .

# Run headless (for tournaments)
docker run --rm reversi42 --view headless

# Run with X11 forwarding (Linux)
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix reversi42
```

See [Docker Guide](docker.md) for details.

## Configuration

### Configuration Files

```bash
# System config (do not edit)
/opt/reversi42/config.json

# User config
~/.reversi42/config.json

# Project config
./reversi42.config.json
```

### Environment Variables

```bash
# Set AI depth
export REVERSI42_AI_DEPTH=10

# Set view type
export REVERSI42_VIEW=terminal

# Set log level
export REVERSI42_LOG_LEVEL=DEBUG
```

See [Configuration Guide](configuration.md) for all options.

## Post-Installation

### Verify Installation

```bash
# Check version
reversi42 --version

# List available views
reversi42 --list-views

# Run quick test
reversi42 --view headless
```

### Initial Setup

1. **Run the game** to create config directory
2. **Configure preferences** (AI depth, view, etc.)
3. **Optional**: Import custom opening books
4. **Optional**: Set up tournament configurations

## Troubleshooting

### Common Issues

#### "FastAPI not found" or "uvicorn not found"

```bash
pip install -r requirements.txt
```

#### "Permission denied" (Linux/macOS)

```bash
chmod +x reversi42
```

#### "Python version" error

```bash
# Ensure Python 3.9+
python3 --version

# Use specific Python version
python3.11 -m venv venv
```

#### Display issues (Linux)

```bash
# Install SDL2
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

See [Troubleshooting Guide](troubleshooting.md) for more.

## Updating

### From Source

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### From Package Manager

```bash
# PyPI
pip install --upgrade reversi42

# Homebrew
brew upgrade reversi42

# Scoop
scoop update reversi42
```

### From Binary

Download latest version from [Releases](https://github.com/lucaamore/reversi42/releases).

## Uninstalling

### From Source

```bash
# Just delete the directory
rm -rf reversi42/
```

### From PyPI

```bash
pip uninstall reversi42
```

### From Package Manager

```bash
# Homebrew
brew uninstall reversi42

# Scoop
scoop uninstall reversi42
```

### Clean Up User Data

```bash
# Remove config and saved games
rm -rf ~/.reversi42/
```

## Deployment for Production

### Server Deployment

For running tournaments or analysis on servers:

```bash
# Install headless
pip install reversi42[headless]

# Run tournament
reversi42 --view headless --tournament config.json
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Run Reversi42 Tests
  run: |
    pip install reversi42
    reversi42 --version
    pytest tests/
```

See [CI/CD Guide](ci-cd.md) for more.

## Platform-Specific Guides

Detailed guides for each platform:

- [macOS Deployment](platforms/macos.md)
- [Windows Deployment](platforms/windows.md)
- [Linux Deployment](platforms/linux.md)
- [Raspberry Pi](platforms/raspberry-pi.md)

## Distribution

### Creating Releases

See [Release Process](release-process.md) for:
- Version numbering
- Building distributions
- Publishing to package managers
- Creating GitHub releases

### Package Repositories

- **PyPI**: [package/pypi.md](package/pypi.md)
- **Homebrew**: [package/homebrew.md](package/homebrew.md)
- **Snap**: [package/snap.md](package/snap.md)
- **AUR**: [package/aur.md](package/aur.md)

## Support

For deployment issues:
- Check [Troubleshooting](troubleshooting.md)
- Open an [Issue](https://github.com/lucaamore/reversi42/issues)
- Ask in [Discussions](https://github.com/lucaamore/reversi42/discussions)

---

**Next Steps**:
1. Choose your installation method
2. Follow platform-specific guide
3. Configure your preferences
4. Start playing!

