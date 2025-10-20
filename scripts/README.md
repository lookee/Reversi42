# Development Scripts

Helper scripts for Reversi42 development and CI/CD.

## 📋 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| **setup_dev.sh** | Setup development environment | `./scripts/setup_dev.sh` |
| **run_tests.sh** | Run test suite | `./scripts/run_tests.sh [--fast\|--coverage\|--all]` |
| **check_quality.sh** | Code quality checks | `./scripts/check_quality.sh` |
| **benchmark.sh** | Performance benchmarks | `./scripts/benchmark.sh` |
| **release.sh** | Create new release | `./scripts/release.sh <version>` |

---

## 🛠️ setup_dev.sh

**Purpose**: One-command development environment setup

**What it does**:
1. Checks Python version (3.9+ required)
2. Creates virtual environment
3. Installs all dependencies
4. Installs package in editable mode
5. Sets up pre-commit hooks (optional)
6. Makes scripts executable
7. Runs verification tests

**Usage**:
```bash
./scripts/setup_dev.sh
```

**First-time contributors**: Run this first!

---

## 🧪 run_tests.sh

**Purpose**: Run tests with various options

**Modes**:

### Fast Mode
```bash
./scripts/run_tests.sh --fast
```
- Runs only quick tests
- Skips slow integration tests
- Best for: Rapid development iterations
- Duration: ~30 seconds

### Coverage Mode
```bash
./scripts/run_tests.sh --coverage
```
- Runs all tests with coverage
- Generates HTML coverage report
- Opens `htmlcov/index.html`
- Duration: ~2 minutes

### All Mode (Default)
```bash
./scripts/run_tests.sh --all
./scripts/run_tests.sh  # Same as --all
```
- Runs complete test suite
- Unit, integration, characterization tests
- Comprehensive verification
- Duration: ~5 minutes

**Output**:
- ✅ Green checkmarks for passed tests
- ❌ Red X for failed tests
- Coverage percentage
- Detailed error messages

---

## 🔍 check_quality.sh

**Purpose**: Enforce code quality standards

**Checks**:

1. **Black** - Code formatting
   - Ensures consistent style
   - Auto-fixable: `black src/ tests/`

2. **isort** - Import sorting
   - Alphabetical, grouped imports
   - Auto-fixable: `isort src/ tests/`

3. **Pylint** - Code linting
   - Score must be >= 7.0
   - Checks style, bugs, complexity

4. **mypy** - Type checking
   - Static type analysis
   - Warning only (not enforced)

5. **Bandit** - Security linting
   - Detects security issues
   - Warning only

**Usage**:
```bash
./scripts/check_quality.sh
```

**Exit Codes**:
- `0` - All critical checks passed
- `1` - Some checks failed (must fix)

**Before every commit**: Run this script!

---

## ⚡ benchmark.sh

**Purpose**: Measure performance and detect regressions

**Benchmarks**:

### 1. Bitboard Operations
- Move generation speed (ns/op)
- Make move speed (ns/op)
- Score calculation (ns/op)

**Targets**:
- Move generation: <100ns
- Make move: <50ns
- Get score: <20ns

### 2. AI Performance
- Depth 6 search time
- Depth 9 search time

**Targets**:
- Depth 6: <0.5 seconds
- Depth 9: <2.0 seconds

### 3. Memory Usage
- BitboardGame size
- PlayerApocalyptron size

**Targets**:
- Game state: <1KB
- Player: Reasonable overhead

### 4. Full Game
- Complete AI vs AI game
- Time per move average

**Targets**:
- Full game: <60 seconds
- Per move: <1 second (depth 6)

**Usage**:
```bash
./scripts/benchmark.sh
```

**Output**: Performance report with ✅/⚠️ indicators

**Use cases**:
- Before submitting performance-related PRs
- After optimization changes
- Regular performance tracking

---

## 🚀 release.sh

**Purpose**: Automated release process

**What it does**:

1. **Pre-flight Checks**
   - Verifies working directory is clean
   - Checks current branch (prefer main)
   - Pulls latest changes

2. **Version Validation**
   - Checks `pyproject.toml` has correct version
   - Updates `setup.py` if needed
   - Verifies CHANGELOG.md has release notes

3. **Quality Assurance**
   - Runs complete test suite
   - Runs code quality checks
   - Builds and validates package

4. **Release Creation**
   - Creates git tag
   - Pushes tag to origin
   - Triggers GitHub Actions release workflow

**Usage**:
```bash
./scripts/release.sh 3.2.0
```

**Interactive**: Prompts for confirmation at critical steps

**Prerequisites**:
- Clean working directory
- Version updated in `pyproject.toml`
- CHANGELOG.md updated with release notes
- All tests passing

**Output**: Git tag created, GitHub Actions triggered

---

## 🎯 Typical Workflows

### Daily Development

```bash
# 1. Start your day
git pull origin main
source venv/bin/activate

# 2. Make changes
# ... edit code ...

# 3. Test frequently
./scripts/run_tests.sh --fast

# 4. Before commit
./scripts/check_quality.sh

# 5. Commit
git commit -m "feat: add new feature"

# 6. Before pushing
./scripts/run_tests.sh --all

# 7. Push
git push origin feature/my-feature
```

### Preparing a PR

```bash
# 1. Ensure all tests pass
./scripts/run_tests.sh --all

# 2. Check code quality
./scripts/check_quality.sh

# 3. Check coverage
./scripts/run_tests.sh --coverage
# Ensure >= 80%

# 4. Run benchmarks (if performance-related)
./scripts/benchmark.sh

# 5. Create PR on GitHub
```

### Creating a Release

```bash
# 1. Update version
# Edit pyproject.toml: version = "3.2.0"
# Edit setup.py: version = "3.2.0"

# 2. Update CHANGELOG
# Add release notes under [3.2.0] section

# 3. Commit version bump
git add pyproject.toml setup.py CHANGELOG.md
git commit -m "chore: bump version to 3.2.0"
git push origin main

# 4. Run release script
./scripts/release.sh 3.2.0

# 5. Monitor GitHub Actions
# https://github.com/lucaamore/reversi42/actions
```

---

## 🔧 Script Internals

### Environment Detection

Scripts automatically:
- Detect and activate virtual environment
- Check Python version
- Validate dependencies installed
- Set appropriate environment variables

### Error Handling

All scripts use `set -e`:
- Exit immediately on error
- Prevents partial execution
- Clear error messages
- Suggests fixes where possible

### Output Formatting

Color-coded output:
- 🔵 **Blue**: Information
- 🟢 **Green**: Success
- 🟡 **Yellow**: Warning
- 🔴 **Red**: Error

---

## 📝 Adding New Scripts

### Template

```bash
#!/bin/bash
# Description of what this script does
# Usage: ./scripts/my_script.sh [args]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Script Name${NC}"
echo "======================================"

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Your script logic here

echo -e "${GREEN}✅ Script completed${NC}"
```

### Make Executable

```bash
chmod +x scripts/my_script.sh
```

### Add to Documentation

Update this README.md with:
- Script name and purpose
- Usage instructions
- Expected output

---

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code style guidelines
- Testing requirements
- Pull request process

---

**Last Updated**: 2025-10-20  
**Maintained by**: Development Team

*These scripts are designed to make development easier and ensure quality. Suggestions welcome!*

