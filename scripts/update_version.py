#!/usr/bin/env python3
"""
Update Version Script

Updates the version number in pyproject.toml (single source of truth).
All other files read the version from pyproject.toml automatically.

Usage:
    python scripts/update_version.py 3.3.0
    python scripts/update_version.py --show
"""

import argparse
import re
import sys
from pathlib import Path


def get_project_root():
    """Get project root directory"""
    return Path(__file__).parent.parent


def read_current_version():
    """Read current version from pyproject.toml"""
    pyproject_path = get_project_root() / "pyproject.toml"

    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        sys.exit(1)

    with open(pyproject_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("version"):
                parts = line.split("=")
                if len(parts) == 2:
                    version = parts[1].strip().strip('"').strip("'")
                    return version

    return None


def update_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = get_project_root() / "pyproject.toml"

    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        sys.exit(1)

    # Validate version format (semantic versioning)
    if not re.match(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$", new_version):
        print(f"Error: Invalid version format '{new_version}'")
        print("Expected format: MAJOR.MINOR.PATCH (e.g., 3.2.0)")
        sys.exit(1)

    # Read and update pyproject.toml
    content = pyproject_path.read_text(encoding="utf-8")

    # Replace version line
    new_content = re.sub(r'version\s*=\s*["\'][^"\']+["\']', f'version = "{new_version}"', content)

    # Write back
    pyproject_path.write_text(new_content, encoding="utf-8")

    print(f"✅ Version updated to {new_version} in pyproject.toml")
    print("\nAll other files will automatically read this version:")
    print("  - src/__version__.py")
    print("  - setup.py")
    print("  - Any code importing from __version__")


def show_version():
    """Show current version"""
    version = read_current_version()

    if version:
        print(f"Current version: {version}")
        print(f"\nSource: pyproject.toml (line with 'version = \"{version}\"')")

        # Try to import and verify
        try:
            sys.path.insert(0, str(get_project_root() / "src"))
            from __version__ import __version__ as code_version

            if code_version == version:
                print(f"✅ Code version matches: {code_version}")
            else:
                print(f"⚠️  Code version differs: {code_version}")
        except ImportError:
            print("ℹ️  Could not import __version__.py (this is OK)")
    else:
        print("Error: Could not read version from pyproject.toml")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Update version number (single source of truth in pyproject.toml)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Show current version:
    python scripts/update_version.py --show
  
  Update to new version:
    python scripts/update_version.py 3.3.0
    python scripts/update_version.py 4.0.0-beta.1
        """,
    )

    parser.add_argument("version", nargs="?", help="New version number (e.g., 3.2.0)")

    parser.add_argument("--show", action="store_true", help="Show current version")

    args = parser.parse_args()

    if args.show:
        show_version()
    elif args.version:
        current = read_current_version()
        print(f"Current version: {current}")
        print(f"New version: {args.version}")

        response = input("\nUpdate version? [y/N] ")
        if response.lower() == "y":
            update_version(args.version)
        else:
            print("Cancelled")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
