# Quick Version Guide 🚀

## TL;DR

**Edit version ONLY in `pyproject.toml`:**

```toml
[project]
version = "3.2.0"  # ← EDIT HERE ONLY
```

Everything else updates automatically!

## Commands

```bash
# Show current version
python scripts/update_version.py --show

# Update version
python scripts/update_version.py 3.3.0

# Use in Python code
python -c "from __version__ import __version__; print(__version__)"
```

## Usage in Code

```python
from __version__ import __version__
print(f"Reversi42 v{__version__}")
```

## API Endpoints

```bash
curl http://localhost:8000/version
curl http://localhost:8000/stats
```

That's it! 🎉

See `VERSION_MANAGEMENT.md` for details.
