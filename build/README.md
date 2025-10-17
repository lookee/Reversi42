# Build Scripts

Automated build scripts for creating distributable packages.

## Quick Start

```bash
# Install dependencies
pip install -r requirements-build.txt

# Test setup
./test_build_setup.sh

# Build for your platform
cd /path/to/Reversi42
./build/build_all.sh
```

## Scripts

- `build_all.sh` - Auto-detect platform
- `build_macos.sh` - macOS (.app/.dmg)
- `build_linux_deb.sh` - Linux (.deb)  
- `build_windows.sh` - Windows (.exe)
- `test_build_setup.sh` - Verify prerequisites

See BUILD.md in project root for complete documentation.
