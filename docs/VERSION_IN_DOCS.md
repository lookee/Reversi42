# Version References in Documentation

## Current Version: 3.2.0

This document explains version references in the documentation.

## Single Source of Truth

The version is stored in `pyproject.toml`:

```toml
[project]
version = "3.2.0"
```

## Version References Guide

### ✅ Updated to 3.2.0 (Current Version)

These files reference the **current** version and have been updated:

- `README.md` - Main documentation
- `docs/DOCUMENTATION_INDEX.md` - Documentation index
- `src/ui/README.md` - UI module documentation
- `src/Board/README.md` - Board module documentation
- `docs/user-guide/faq.md` - FAQ
- `docs/api/README.md` - API documentation
- `tests/README.md` - Test documentation

### 📚 Historical Version References (Keep As-Is)

These files reference **specific historical versions** when features were introduced.
**These should NOT be changed** as they document when features were added:

#### v4.2.0 References (Epic Gladiators Release)
- `README.md` - "Complete Player Roster (v4.2.0)"
- `docs/architecture/apocalyptron-engine.md` - "NEW in v4.2.0"
- `docs/tutorials/CREATE_CUSTOM_PLAYER.md` - Engine version
- `tournament/ring/README.md` - Tournament system version

**Reason**: These mark when Epic Gladiators and SearchStrategy were introduced.

#### v3.0.0 References (Bitboard Release)
- `README.md` - "Core Technologies (v3.0.0)"
- `README.md` - "Bitboard Engine (NEW in 3.0.0)"

**Reason**: These mark when bitboard engine was introduced.

#### v3.1.0 References (Multiple Views Release)
- `docs/architecture/apocalyptron-engine.md` - "Engine Version"
- `tests/apocalyptron/TEST_STRATEGY.md` - Test suite version

**Reason**: These mark when multiple view support was added.

### 🔄 Auto-Generated Version References

These files are automatically generated or use dynamic versioning:

- `src/__version__.py` - Reads from pyproject.toml
- `src/webgui/backend_server.py` - Imports from __version__
- `VERSION_MANAGEMENT.md` - Version management guide
- `VERSION_CENTRALIZED_SUMMARY.md` - Centralization summary

### 📝 Release-Specific Documentation

#### CHANGELOG.md
Contains **all versions** with their release notes. Do NOT change historical entries!

Only add new entries at the top:
```markdown
## [3.2.0] - 2025-11-02
### Changed
- Removed pygame and terminal views
- Web interface is now primary
```

#### Git Tags
Version tags in git history should remain unchanged:
- `v3.0.0` - Bitboard engine
- `v3.1.0` - Multiple views
- `v3.2.0` - Web-first architecture
- `v4.2.0` - Epic Gladiators

## How to Update Documentation Version

### When Releasing a New Version

1. **Update pyproject.toml** (single source of truth):
   ```bash
   python scripts/update_version.py 3.3.0
   ```

2. **Update "current version" references** in these files:
   - README.md (top section)
   - docs/DOCUMENTATION_INDEX.md
   - src/ui/README.md
   - src/Board/README.md
   - docs/api/README.md
   - tests/README.md

3. **Add CHANGELOG entry** (don't modify old entries):
   ```markdown
   ## [3.3.0] - YYYY-MM-DD
   ### Added/Changed/Fixed
   ```

4. **Keep historical references** unchanged (v3.0.0, v3.1.0, v4.2.0, etc.)

## Quick Reference

| File | Type | Update? |
|------|------|---------|
| README.md (top) | Current | ✅ Yes |
| README.md (feature markers) | Historical | ❌ No |
| docs/DOCUMENTATION_INDEX.md | Current | ✅ Yes |
| src/ui/README.md | Current | ✅ Yes |
| src/Board/README.md | Current | ✅ Yes |
| docs/architecture/*.md (v4.2.0) | Historical | ❌ No |
| CHANGELOG.md | All versions | ➕ Add new only |
| pyproject.toml | Source of truth | ✅ Yes |

## Example Commit Message

```bash
git commit -m "docs: update documentation to v3.2.0

- Updated current version references in main docs
- Kept historical version markers unchanged
- Added v3.2.0 entry to CHANGELOG"
```

---

**Rule of Thumb**:
- If it says "current version" or "as of vX.X.X" → Update it
- If it says "NEW in vX.X.X" or "since vX.X.X" → Keep it (historical marker)

