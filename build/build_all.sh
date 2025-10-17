#!/bin/bash
# Master build script - auto-detects platform

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

PLATFORM=$(uname -s)
echo "Building for: $PLATFORM"

case "$PLATFORM" in
    Linux*) ./build/build_linux_deb.sh ;;
    Darwin*) ./build/build_macos.sh ;;
    MINGW*|MSYS*|CYGWIN*) ./build/build_windows.sh ;;
    *) echo "Unknown platform"; exit 1 ;;
esac
