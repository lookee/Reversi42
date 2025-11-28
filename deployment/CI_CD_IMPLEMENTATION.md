# CI/CD Implementation Guide

Complete guide to the Continuous Integration and Continuous Deployment implementation for Reversi42.

**Status**: ✅ Implemented  
**Platform**: GitHub Actions  
**Cost**: $0 (free for public repos)

---

## 🎯 Overview

Reversi42 now has a complete enterprise-grade CI/CD pipeline that:

✅ **Automatically tests** every PR and commit  
✅ **Enforces code quality** standards  
✅ **Builds multi-platform** executables  
✅ **Publishes releases** to GitHub and PyPI  
✅ **Deploys documentation** to GitHub Pages  
✅ **Monitors performance** and security  
✅ **Updates dependencies** automatically  

---

## 📁 Files Created

### GitHub Actions Workflows (5 workflows)

| File | Purpose | Triggers | Duration |
|------|---------|----------|----------|
| **ci.yml** | Main CI pipeline | PR, Push | ~10 min |
| **release.yml** | Release automation | Tags (v*) | ~30 min |
| **docs.yml** | Documentation deploy | Push to main/doc | ~5 min |
| **benchmarks.yml** | Performance tracking | Nightly, PR | ~10 min |
| **security.yml** | Security scanning | Weekly, Push | ~5 min |

### Configuration Files (7 files)

| File | Purpose |
|------|---------|
| **.github/dependabot.yml** | Auto dependency updates |
| **.github/release-drafter.yml** | Auto release notes |
| **Dockerfile** | Container image |
| **docker-compose.yml** | Local development |
| **.dockerignore** | Docker build optimization |
| **.coveragerc** | Coverage configuration |
| **setup.py** | Package setup (PyPI) |
| **MANIFEST.in** | Package manifest |

### Helper Scripts (5 scripts)

| Script | Purpose |
|--------|---------|
| **scripts/run_tests.sh** | Run test suite |
| **scripts/check_quality.sh** | Code quality checks |
| **scripts/benchmark.sh** | Performance benchmarks |
| **scripts/release.sh** | Create releases |
| **scripts/setup_dev.sh** | Setup dev environment |

**Total**: 17 new files for CI/CD

---

## 🔄 CI/CD Workflows

### Workflow 1: Continuous Integration (ci.yml)

**Purpose**: Validate every code change

**Pipeline**:

```
┌─────────────────────┐
│  Code Push/PR       │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐   ┌─────────┐
│Quality │   │  Tests  │
│Checks  │   │ (16x)   │
└────┬───┘   └────┬────┘
     │            │
     └──────┬─────┘
            │
     ┌──────┴──────┐
     │             │
     ▼             ▼
┌──────────┐  ┌─────────┐
│Integration│  │  Build  │
│  Tests    │  │  Check  │
└──────┬────┘  └────┬────┘
       │            │
       └─────┬──────┘
             ▼
      ┌────────────┐
      │ CI Status  │
      │ ✅ or ❌   │
      └────────────┘
```

**Jobs**:

1. **code-quality** (Ubuntu, ~3 min)
   - Black formatting check
   - isort import sorting
   - Pylint (score >= 7.0)
   - mypy type checking
   - Bandit security scan

2. **test** (Multi-platform matrix, ~7 min)
   - OS: Ubuntu, macOS, Windows
   - Python: 3.9, 3.10, 3.11, 3.12
   - Total combinations: 12 (3 OS × 4 Python)
   - Coverage upload to Codecov

3. **integration-tests** (Ubuntu, ~15 min)
   - Integration test suite
   - AI vs AI test games
   - Headless mode tests

4. **build-check** (Ubuntu, ~2 min)
   - Build Python package
   - Validate with twine
   - Upload artifacts

**Quality Gates**:
- ✅ All tests must pass
- ✅ Coverage >= 80%
- ✅ Pylint >= 7.0
- ✅ No formatting issues
- ✅ Build succeeds

### Workflow 2: Release Automation (release.yml)

**Purpose**: Automate release process

**Trigger**: Git tag `v*.*.*` (e.g., `v3.2.0`)

**Pipeline**:

```
┌─────────────────────┐
│  Git Tag (v3.2.0)   │
└──────────┬──────────┘
           │
    ┌──────┴────────────┬───────────┐
    │                   │           │
    ▼                   ▼           ▼
┌─────────┐      ┌──────────┐  ┌──────────┐
│ Package │      │ Executables │  Docker   │
│  Build  │      │   (3 OS)   │  Image    │
└────┬────┘      └──────┬─────┘  └────┬────┘
     │                   │            │
     └─────────┬─────────┴────────────┘
               │
               ▼
      ┌────────────────┐
      │ GitHub Release │
      │   + Artifacts  │
      └───────┬────────┘
              │
        ┌─────┴─────┐
        │           │
        ▼           ▼
   ┌────────┐  ┌──────────┐
   │  PyPI  │  │Docker Hub│
   └────────┘  └──────────┘
```

**Jobs**:

1. **build-python-package** (~3 min)
   - Build wheel and sdist
   - Validate with twine
   - Upload artifacts

2. **build-executables** (Matrix: 3 OS, ~20 min each)
   - macOS: DMG installer
   - Windows: EXE installer
   - Linux: AppImage
   - Upload artifacts

3. **create-release** (~2 min)
   - Download all artifacts
   - Extract release notes from CHANGELOG
   - Create GitHub Release
   - Upload all binaries

4. **publish-pypi** (~2 min)
   - Publish package to PyPI
   - Only on tagged releases

**Artifacts**:
- `reversi42-3.1.0-py3-none-any.whl`
- `reversi42-3.1.0.tar.gz`
- `reversi42-3.1.0-macos.dmg`
- `reversi42-3.1.0-windows.exe`
- `reversi42-3.1.0-linux.AppImage`

### Workflow 3: Documentation (docs.yml)

**Purpose**: Deploy documentation to GitHub Pages

**Triggers**:
- Push to `main` or `doc` branches
- Changes in `docs/` directory
- Manual dispatch

**Pipeline**:

```
┌─────────────────────┐
│  Push to main/doc   │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ Build Docs   │
    │ (Markdown)   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Check Links  │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │Deploy to     │
    │GitHub Pages  │
    └──────────────┘
```

**Output**: https://lookee.github.io/Reversi42/

### Workflow 4: Performance Benchmarks (benchmarks.yml)

**Purpose**: Track performance over time

**Triggers**:
- Nightly (2 AM UTC)
- Push to main
- Pull requests (optional)

**Benchmarks**:

1. **Bitboard Operations**
   - Move generation: Target <100ns
   - Make move: Target <50ns
   - Get score: Target <20ns

2. **AI Performance**
   - Depth 6: Target <0.5s
   - Depth 9: Target <2.0s

3. **Memory Usage**
   - Game state: Target <1KB
   - Total runtime: Target <200MB

4. **Full Game**
   - AI vs AI completion: Target <60s

**Regression Detection**: Fails if >10% slower than baseline

### Workflow 5: Security Scanning (security.yml)

**Purpose**: Detect security vulnerabilities

**Triggers**:
- Weekly (Sundays 3 AM UTC)
- Push to main
- Pull requests

**Scans**:

1. **Dependency Check**
   - Safety (known vulnerabilities)
   - pip-audit (CVE database)

2. **Code Analysis**
   - Bandit (SAST)
   - CodeQL (semantic analysis)

3. **Secret Detection**
   - GitHub secret scanning
   - No hardcoded credentials

---

## 🤖 Dependabot Configuration

**Purpose**: Automated dependency updates

**Schedule**: Weekly (Mondays 9 AM)

**Features**:
- Groups minor/patch updates
- Separates dev vs prod dependencies
- Auto-labels PRs
- Conventional commit messages

**Updates**:
- Python packages (weekly)
- GitHub Actions (weekly)
- Security patches (immediate)

---

## 📋 Quality Gates

### Pull Request Requirements

**Before merge, ALL must pass**:

```
✅ Code Quality
   ├─ Black formatting
   ├─ isort import sorting
   ├─ Pylint >= 7.0
   └─ mypy type checking

✅ Testing
   ├─ Unit tests pass (all platforms)
   ├─ Integration tests pass
   ├─ Coverage >= 80%
   └─ No flaky tests

✅ Security
   ├─ Bandit scan clean
   ├─ Safety check passed
   └─ CodeQL analysis clear

✅ Build
   └─ Package builds successfully

✅ Review
   ├─ At least 1 approval
   └─ All comments resolved
```

### Release Requirements

```
✅ Pre-Release
   ├─ All CI checks pass
   ├─ Version bumped
   ├─ CHANGELOG updated
   └─ Documentation updated

✅ Build
   ├─ Python package builds
   ├─ Executables build (3 platforms)
   ├─ Docker image builds
   └─ All artifacts signed

✅ Publish
   ├─ GitHub Release created
   ├─ PyPI package published
   ├─ Docker image pushed
   └─ Docs deployed
```

---

## 🚀 Release Process

### Automated (Recommended)

1. **Update version** in `pyproject.toml` and `setup.py`
2. **Update CHANGELOG.md** with release notes
3. **Commit changes**: `git commit -m "chore: bump version to 3.2.0"`
4. **Run release script**: `./scripts/release.sh 3.2.0`
5. **GitHub Actions** handles the rest automatically!

### Manual Steps (If Needed)

```bash
# 1. Ensure everything is committed
git status

# 2. Update version files
# Edit pyproject.toml and setup.py

# 3. Update CHANGELOG.md
# Add new version section

# 4. Commit version bump
git add pyproject.toml setup.py CHANGELOG.md
git commit -m "chore: bump version to 3.2.0"
git push origin main

# 5. Create and push tag
git tag -a v3.2.0 -m "Release 3.2.0"
git push origin v3.2.0

# 6. Monitor GitHub Actions
# https://github.com/lookee/Reversi42/actions
```

**Release Timeline**:
- **T+0**: Tag pushed
- **T+5min**: Builds start
- **T+30min**: GitHub Release created
- **T+35min**: PyPI published
- **T+40min**: Docker pushed
- **T+45min**: Docs updated

---

## 🐳 Docker Usage

### Build Locally

```bash
# Build image
docker build -t reversi42:latest .

# Run container
docker run --rm reversi42:latest --view headless

# Run with volume mounts
docker run --rm \
  -v $(pwd)/saves:/app/saves \
  -v $(pwd)/tournament/reports:/app/tournament/reports \
  reversi42:latest
```

### Docker Compose

```bash
# Start services
docker-compose up reversi42

# Development environment
docker-compose run reversi42-dev bash

# Run tournament
docker-compose run tournament
```

### Pull from Docker Hub (When Published)

```bash
docker pull lookee/reversi42:latest
docker run --rm lookee/reversi42:latest
```

---

## 📊 Monitoring & Badges

### GitHub Status Badges

Add to README.md:

```markdown
[![CI](https://github.com/lookee/Reversi42/workflows/CI/badge.svg)](https://github.com/lookee/Reversi42/actions/workflows/ci.yml)
[![Release](https://github.com/lookee/Reversi42/workflows/Release/badge.svg)](https://github.com/lookee/Reversi42/actions/workflows/release.yml)
[![codecov](https://codecov.io/gh/lookee/Reversi42/branch/main/graph/badge.svg)](https://codecov.io/gh/lookee/Reversi42)
[![Security](https://github.com/lookee/Reversi42/workflows/Security/badge.svg)](https://github.com/lookee/Reversi42/actions/workflows/security.yml)
```

### External Services (Free for Open Source)

1. **Codecov** - Coverage tracking
   - Sign up at https://codecov.io
   - Connect GitHub repository
   - Automatic coverage reports on PRs

2. **Shields.io** - Additional badges
   - PyPI version
   - License
   - Python versions
   - Downloads

3. **GitHub Insights** - Built-in analytics
   - Dependency graph
   - Security alerts
   - Traffic statistics

---

## 🛠️ Local Development Scripts

### Setup Development Environment

```bash
# First time setup
./scripts/setup_dev.sh

# Activates venv, installs deps, runs verification
```

### Run Tests

```bash
# Fast tests only
./scripts/run_tests.sh --fast

# With coverage
./scripts/run_tests.sh --coverage

# Complete suite
./scripts/run_tests.sh --all
```

### Check Code Quality

```bash
# Run all quality checks
./scripts/check_quality.sh

# Individual checks:
black --check src/ tests/
isort --check src/ tests/
pylint src/
mypy src/
```

### Run Benchmarks

```bash
# Performance benchmarks
./scripts/benchmark.sh

# Output shows timing for:
# - Bitboard operations
# - AI moves at various depths
# - Memory usage
# - Full game completion
```

### Create Release

```bash
# Interactive release process
./scripts/release.sh 3.2.0

# Runs all checks and creates tag
```

---

## 🔐 Secrets Configuration

For CI/CD to work completely, configure these GitHub Secrets:

| Secret | Purpose | Required For |
|--------|---------|--------------|
| **PYPI_API_TOKEN** | PyPI publishing | Release to PyPI |
| **DOCKERHUB_USERNAME** | Docker Hub login | Docker publish |
| **DOCKERHUB_TOKEN** | Docker Hub token | Docker publish |
| **CODECOV_TOKEN** | Coverage uploads | Coverage tracking |

### How to Add Secrets

1. Go to GitHub repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its value

### Getting Tokens

**PyPI Token**:
1. Create account at https://pypi.org
2. Go to Account Settings → API Tokens
3. Create token with scope: "Entire account"

**Docker Hub Token**:
1. Create account at https://hub.docker.com
2. Go to Account Settings → Security
3. Create Access Token

**Codecov Token**:
1. Sign up at https://codecov.io with GitHub
2. Add repository
3. Copy token from repository settings

---

## ⚙️ Configuration Options

### Customizing Workflows

Edit workflow files in `.github/workflows/`:

**Common Customizations**:

```yaml
# Change Python version
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'  # Update here

# Adjust test matrix
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]  # Remove windows if needed
    python-version: ['3.11', '3.12']   # Focus on newer versions

# Change coverage threshold
pytest --cov=src --cov-fail-under=85  # Increase to 85%

# Adjust pylint threshold
pylint src/ --fail-under=8.0  # Increase to 8.0
```

### Customizing Dependabot

Edit `.github/dependabot.yml`:

```yaml
# Change update frequency
schedule:
  interval: "daily"  # Options: daily, weekly, monthly

# Adjust PR limit
open-pull-requests-limit: 5

# Auto-merge minor updates (optional, requires GitHub App)
```

---

## 📈 Performance Tracking

### Benchmark Results

Benchmarks run nightly and on PRs. Results show:

- **Historical trends** (performance over time)
- **Regression detection** (>10% slower = warning)
- **Comparison charts** (current vs baseline)

### Viewing Results

1. Go to Actions → Benchmarks workflow
2. Click latest run
3. Download artifacts
4. Or view in PR comments (for PR-triggered benchmarks)

---

## 🔒 Security Features

### Automated Security

1. **Dependency Scanning**
   - Weekly checks with Safety and pip-audit
   - Immediate alerts for high-severity issues
   - Auto-PRs for security updates (Dependabot)

2. **Code Analysis**
   - Bandit SAST on every PR
   - CodeQL semantic analysis weekly
   - GitHub secret scanning always on

3. **Docker Security**
   - Multi-stage builds (minimal attack surface)
   - Non-root user
   - No secrets in images
   - Regular base image updates

### Security Workflow

```
Vulnerability Detected
         │
         ▼
  Dependabot creates PR
         │
         ▼
    CI runs tests
         │
         ▼
   Auto-merge (if safe)
         │
         ▼
    Vulnerability fixed
```

---

## 🎯 CI/CD Metrics

### Expected Performance

| Workflow | Frequency | Duration | Cost |
|----------|-----------|----------|------|
| CI | Per PR/Push | ~10 min | $0 |
| Release | On tags | ~30 min | $0 |
| Docs | Per push (doc) | ~5 min | $0 |
| Benchmarks | Nightly | ~10 min | $0 |
| Security | Weekly | ~5 min | $0 |

**Monthly Minutes**: ~15,000 min  
**Monthly Cost**: $0 (unlimited for public repos)

### Success Metrics

- **CI Success Rate**: Target >95%
- **Build Time**: Target <15 min
- **Test Coverage**: Target >80%
- **Security Issues**: Target 0 high-severity
- **Dependency Updates**: Weekly
- **Release Frequency**: ~Monthly

---

## 🐛 Troubleshooting

### CI Failures

**Black/isort failures**:
```bash
# Auto-fix locally
black src/ tests/
isort src/ tests/
git commit -am "style: format code"
```

**Test failures**:
```bash
# Run locally to debug
./scripts/run_tests.sh --all
# Fix failing tests
pytest tests/path/to/test.py -v
```

**Build failures**:
```bash
# Test build locally
python -m build
twine check dist/*
```

### Release Issues

**Tag already exists**:
```bash
# Delete local and remote tag
git tag -d v3.1.0
git push origin :refs/tags/v3.1.0
# Create new tag
git tag -a v3.2.0 -m "Release 3.2.0"
git push origin v3.2.0
```

**PyPI upload failed**:
- Check PYPI_API_TOKEN is set correctly
- Verify package version doesn't already exist
- Check package metadata is valid

### Docker Issues

**Build fails**:
```bash
# Test locally
docker build -t reversi42:test .

# Check logs
docker build --progress=plain -t reversi42:test .
```

**Container won't start**:
```bash
# Check logs
docker logs reversi42

# Run interactively
docker run -it reversi42:latest /bin/bash
```

---

## 📚 Best Practices

### 1. Branch Strategy

```
main (protected)
  ├─ develop (integration)
  │   ├─ feature/new-ai
  │   ├─ feature/ui-improvements
  │   └─ fix/bug-123
  ├─ doc (documentation)
  └─ release/3.2.0
```

### 2. Commit Messages

Follow Conventional Commits:

```
feat: add new evaluation function
fix: correct bitboard edge wrapping
docs: update API documentation
style: format code with black
refactor: extract move ordering logic
perf: optimize transposition table
test: add tests for parallel search
chore: update dependencies
ci: improve GitHub Actions caching
```

### 3. Pull Request Workflow

1. Create feature branch
2. Make changes
3. Run tests locally: `./scripts/run_tests.sh`
4. Check quality: `./scripts/check_quality.sh`
5. Commit with conventional message
6. Push and create PR
7. Wait for CI to pass
8. Request review
9. Address feedback
10. Merge when approved

### 4. Release Workflow

1. Update version in `pyproject.toml` and `setup.py`
2. Add release notes to `CHANGELOG.md`
3. Commit: `git commit -m "chore: bump version to 3.2.0"`
4. Run: `./scripts/release.sh 3.2.0`
5. Monitor GitHub Actions
6. Verify release on GitHub
7. Test PyPI package
8. Announce release

---

## 🎓 Advanced Topics

### Caching Strategy

GitHub Actions uses caching to speed up builds:

```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'  # Cache pip dependencies

- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

**Cache Hit**: 2-3x faster dependency installation

### Parallel Testing

```yaml
# Run tests in parallel
pytest tests/ -n auto  # Use all CPU cores

# Or specify core count
pytest tests/ -n 4  # Use 4 cores
```

**Speedup**: 2-4x on multi-core runners

### Conditional Workflows

```yaml
# Only run on specific paths
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'

# Skip CI with commit message
if: "!contains(github.event.head_commit.message, '[skip ci]')"
```

---

## 📞 Support

### CI/CD Issues

- Check [GitHub Actions docs](https://docs.github.com/en/actions)
- Review [workflow runs](https://github.com/lookee/Reversi42/actions)
- Open [issue](https://github.com/lookee/Reversi42/issues)

### Questions

- [GitHub Discussions](https://github.com/lookee/Reversi42/discussions)
- Email: luca.amore@gmail.com

---

## 🎉 Summary

Reversi42 now has **enterprise-grade CI/CD** with:

✅ **5 GitHub Actions workflows**  
✅ **Complete quality gates**  
✅ **Automated releases**  
✅ **Multi-platform builds**  
✅ **Security scanning**  
✅ **Performance monitoring**  
✅ **Documentation deployment**  
✅ **Developer-friendly scripts**  

**Cost**: $0/month (free for open source)  
**Maintenance**: Minimal (automated)  
**Reliability**: High (tested on every commit)

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-20  
**Implementation Status**: ✅ Complete

*For questions about CI/CD, see [Deployment Guide](README.md) or [GitHub Actions Documentation](https://docs.github.com/en/actions).*

