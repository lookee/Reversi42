# CI/CD Reference

Central reference for Continuous Integration and Continuous Deployment of Reversi42.

## Overview

- Platform: GitHub Actions (public repo – unlimited minutes)
- Scope: CI (quality + tests), Releases, Docs deploy, Benchmarks, Security
- Cost: $0/month

## Workflows

Workflows are under .github/workflows/:

- CI Pipeline: .github/workflows/ci.yml
- Release Automation: .github/workflows/release.yml
- Docs Deploy: .github/workflows/docs.yml
- Benchmarks: .github/workflows/benchmarks.yml
- Security Scanning: .github/workflows/security.yml

## Badges (add to README)

[![CI](https://github.com/lucaamore/reversi42/actions/workflows/ci.yml/badge.svg)](https://github.com/lucaamore/reversi42/actions/workflows/ci.yml)
[![Release](https://github.com/lucaamore/reversi42/actions/workflows/release.yml/badge.svg)](https://github.com/lucaamore/reversi42/actions/workflows/release.yml)
[![Security](https://github.com/lucaamore/reversi42/actions/workflows/security.yml/badge.svg)](https://github.com/lucaamore/reversi42/actions/workflows/security.yml)

(Optional)
[![codecov](https://codecov.io/gh/lucaamore/reversi42/branch/main/graph/badge.svg)](https://codecov.io/gh/lucaamore/reversi42)

## GitHub Secrets (required)

- PYPI_API_TOKEN: for PyPI publishing
- DOCKERHUB_USERNAME / DOCKERHUB_TOKEN: for Docker publish (optional)
- CODECOV_TOKEN: for coverage uploads (optional)

Add via GitHub → Settings → Secrets and variables → Actions.

## Local Commands

- Setup dev env: ./scripts/setup_dev.sh
- Run tests: ./scripts/run_tests.sh --all
- Quality checks: ./scripts/check_quality.sh
- Benchmarks: ./scripts/benchmark.sh
- Create release: ./scripts/release.sh <version>

## Release Flow (tag-driven)

1) Update version (pyproject.toml, setup.py), update CHANGELOG
2) Tag: git tag -a vX.Y.Z -m "Release X.Y.Z" && git push origin vX.Y.Z
3) Actions build: PyPI, binaries, Docker; GitHub Release created

## Documentation Deploy

- Trigger: push to main/doc or manual
- Output: GitHub Pages (gh-pages branch)

## Support

- Actions runs: https://github.com/lucaamore/reversi42/actions
- Issues: https://github.com/lucaamore/reversi42/issues
- Discussions: https://github.com/lucaamore/reversi42/discussions
