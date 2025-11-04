#!/usr/bin/env python3
"""
Minimal setup.py for backward compatibility with older tools.

All project configuration is defined in pyproject.toml (PEP 518 standard).
This file exists only for compatibility with tools that don't yet support
pyproject.toml as the sole configuration source.

Modern installation commands (recommended):
    pip install .
    pip install -e .
    python -m build

For more information, see:
    https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html
"""

from setuptools import setup

# All configuration is in pyproject.toml
# This minimal setup.py delegates everything to pyproject.toml
setup()
