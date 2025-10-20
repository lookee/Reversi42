#!/usr/bin/env python3
"""
Setup script for Reversi42.

This file provides backward compatibility for older tools.
Modern configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="reversi42",
    version="4.1.12",
    author="Luca Amore",
    author_email="luca.amore@gmail.com",
    description="Ultra-Fast Reversi (Othello) with Bitboard AI and Opening Book Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucaamore/reversi42",
    project_urls={
        "Bug Tracker": "https://github.com/lucaamore/reversi42/issues",
        "Documentation": "https://github.com/lucaamore/reversi42/tree/main/docs",
        "Source Code": "https://github.com/lucaamore/reversi42",
        "Changelog": "https://github.com/lucaamore/reversi42/blob/main/CHANGELOG.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": [
            "Images/*.png",
            "domain/knowledge/data/*.txt",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "mypy>=1.5.0",
            "pylint>=2.17.0",
            "black>=23.7.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "reversi42=reversi42:main",
        ],
    },
    zip_safe=False,
)

