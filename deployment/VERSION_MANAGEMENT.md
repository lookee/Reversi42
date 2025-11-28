# Version Management - Reversi42

## Single Source of Truth

**Version number is stored ONLY in `pyproject.toml`**

```toml
[project]
name = "reversi42"
version = "3.2.0"  # ← EDIT HERE ONLY
```

## How It Works

All other files automatically read the version from `pyproject.toml`:

### 1. Python Code
```python
from __version__ import __version__

print(f"Reversi42 v{__version__}")
```

The `src/__version__.py` module automatically reads from `pyproject.toml`.

### 2. Setup.py
```python
setup(
    name="reversi42",
    version=get_version(),  # Reads from pyproject.toml
    ...
)
```

### 3. Web Backend
```python
from __version__ import __version__

app = FastAPI(
    title="Reversi42",
    version=__version__
)
```

## Updating Version

### Method 1: Using Script (Recommended)

```bash
# Show current version
python scripts/update_version.py --show

# Update to new version
python scripts/update_version.py 3.3.0
```

### Method 2: Manual Edit

1. Edit `pyproject.toml`
2. Find the line: `version = "3.2.0"`
3. Change to new version: `version = "3.3.0"`
4. Save file
5. Done! All code will automatically use the new version

## Version Format

Follow [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH[-PRERELEASE]

Examples:
  3.2.0         - Stable release
  3.2.1         - Patch release
  3.3.0         - Minor release
  4.0.0         - Major release
  4.0.0-beta.1  - Pre-release
```

## Files That Read Version Automatically

- ✅ `src/__version__.py` - Reads from pyproject.toml
- ✅ `setup.py` - Reads from pyproject.toml
- ✅ Any Python code importing from `__version__`
- ✅ Web backend (if it imports `__version__`)

## DO NOT Edit Version In:

- ❌ `setup.py` - Reads automatically
- ❌ `src/__version__.py` - Reads automatically  
- ❌ `README.md` - Update manually if shown
- ❌ Any other file - They should import from `__version__`

## Example Usage in Code

```python
# In any Python file
from __version__ import __version__, __author__, __license__

print(f"Reversi42 v{__version__}")
print(f"Author: {__author__}")
print(f"License: {__license__}")
```

## Verification

Check that all versions match:

```bash
# Show version from pyproject.toml
python scripts/update_version.py --show

# Verify in code
python -c "import sys; sys.path.insert(0, 'src'); from __version__ import __version__; print(__version__)"

# Both should print the same version!
```

## Release Checklist

When releasing a new version:

1. ✅ Update version in `pyproject.toml`
2. ✅ Update `CHANGELOG.md` with release notes
3. ✅ Update `README.md` if version is mentioned
4. ✅ Run tests: `pytest`
5. ✅ Verify version: `python scripts/update_version.py --show`
6. ✅ Commit: `git commit -m "Release v3.2.0"`
7. ✅ Tag: `git tag v3.2.0`
8. ✅ Push: `git push && git push --tags`

## Benefits

- ✅ **Single Source of Truth** - Edit version in ONE place only
- ✅ **No Duplication** - No version mismatches
- ✅ **Automatic** - All code reads from pyproject.toml
- ✅ **Standard** - Follows Python packaging best practices
- ✅ **Simple** - Easy to update and verify

## Troubleshooting

### Version mismatch detected

If you see different versions:

```bash
# Reset to pyproject.toml version
python scripts/update_version.py --show

# The script will show any mismatches
```

### ImportError: No module named '__version__'

Make sure `src/__version__.py` exists and `src` is in your Python path:

```python
import sys
sys.path.insert(0, 'src')
from __version__ import __version__
```

---

**Remember**: Always edit version in `pyproject.toml` only! 🎯

