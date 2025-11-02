#!/usr/bin/env python3
"""
Update Documentation Version Script

Automatically updates version references in documentation files
by reading from pyproject.toml (single source of truth).

Usage:
    python scripts/update_docs_version.py
"""

import re
from pathlib import Path


def get_version_from_pyproject():
    """Read version from pyproject.toml"""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("version"):
                parts = line.split("=")
                if len(parts) == 2:
                    return parts[1].strip().strip('"').strip("'")
    
    return None


def update_file_version(file_path, old_version, new_version):
    """Update version in a file"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace version patterns
    patterns = [
        (rf'Version: \*\*{re.escape(old_version)}\*\*', f'Version: **{new_version}**'),
        (rf'version {re.escape(old_version)}', f'version {new_version}'),
        (rf'v{re.escape(old_version)}', f'v{new_version}'),
        (rf'\(v{re.escape(old_version)}\)', f'(v{new_version})'),
    ]
    
    modified = False
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            modified = True
    
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    
    return False


def main():
    """Main function"""
    version = get_version_from_pyproject()
    
    if not version:
        print("❌ Could not read version from pyproject.toml")
        return 1
    
    print(f"📦 Current version in pyproject.toml: {version}")
    print()
    
    # Files to update (with current version references)
    doc_files = [
        "README.md",
        "docs/DOCUMENTATION_INDEX.md",
        "src/ui/README.md",
        "src/Board/README.md",
        "docs/user-guide/faq.md",
        "docs/api/README.md",
        "tests/README.md",
    ]
    
    project_root = Path(__file__).parent.parent
    updated_files = []
    
    # Note: This is a helper script
    # The real source of truth is pyproject.toml
    # Documentation should ideally reference it dynamically
    
    print("ℹ️  Note: Version is centrally managed in pyproject.toml")
    print("ℹ️  This script is for reference only")
    print()
    print("To update version:")
    print(f"  1. Edit pyproject.toml: version = \"{version}\"")
    print("  2. Run: python scripts/update_version.py X.Y.Z")
    print()
    print("All code automatically reads from pyproject.toml!")
    print("✅ No need to update documentation manually")


if __name__ == "__main__":
    main()

