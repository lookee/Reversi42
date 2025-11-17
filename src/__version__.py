"""
Reversi42 Version Information

This module provides version information for Reversi42.
The version is read from pyproject.toml to maintain a single source of truth.
"""

import os
from pathlib import Path

__version__ = "6.3.5"  # Fallback version (must match pyproject.toml)


def get_version():
    """
    Get version from pyproject.toml.

    Priority:
    1. Parse pyproject.toml directly (most reliable for development)
    2. Use importlib.metadata (for installed package)
    3. Fallback to hardcoded version

    Returns:
        str: Version string (e.g., "5.0.0")
    """
    # PRIORITY 1: Parse pyproject.toml directly (no dependencies)
    try:
        current_file = Path(__file__)
        project_root = current_file.parent.parent
        pyproject_path = project_root / "pyproject.toml"

        if pyproject_path.exists():
            with open(pyproject_path, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    # Look for: version = "X.Y.Z"
                    if stripped.startswith("version") and "=" in line:
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            version_str = parts[1].strip().strip('"').strip("'")
                            # Validate it looks like a version
                            if version_str and version_str[0].isdigit():
                                return version_str
    except Exception:
        pass

    # PRIORITY 2: Try importlib.metadata (for installed package)
    try:
        from importlib.metadata import version

        return version("reversi42")
    except Exception:
        pass

    # PRIORITY 3: Try tomli if available
    try:
        import tomli

        current_file = Path(__file__)
        project_root = current_file.parent.parent
        pyproject_path = project_root / "pyproject.toml"

        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomli.load(f)
                return data.get("project", {}).get("version", __version__)
    except Exception:
        pass

    # FINAL FALLBACK
    return __version__


# Set module version
__version__ = get_version()

# Metadata
__author__ = "Luca Amore"
__email__ = "luca.amore@gmail.com"
__license__ = "GPL-3.0-or-later"
__url__ = "https://github.com/lucaamore/reversi42"


if __name__ == "__main__":
    print(f"Reversi42 version {__version__}")
