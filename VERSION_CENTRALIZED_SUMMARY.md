# ✅ Version Management Centralized - Summary

## Sistema Completato 🎉

Il numero di versione è ora **centralizzato** in un unico punto: `pyproject.toml`

## Single Source of Truth

```toml
# pyproject.toml
[project]
name = "reversi42"
version = "3.2.0"  # ← EDIT ONLY HERE!
```

## Come Funziona

### 1. File Creati/Modificati

#### ✅ Creati:
- **`src/__version__.py`** - Modulo che legge automaticamente da pyproject.toml
- **`scripts/update_version.py`** - Script per gestire le versioni
- **`VERSION_MANAGEMENT.md`** - Documentazione completa

#### ✅ Modificati:
- **`pyproject.toml`** - Versione impostata a 3.2.0
- **`setup.py`** - Legge versione da pyproject.toml
- **`src/webgui/backend_server.py`** - Usa `__version__` module

### 2. Utilizzo nel Codice

```python
# In qualsiasi file Python
from __version__ import __version__, __author__, __license__

print(f"Reversi42 v{__version__}")
# Output: Reversi42 v3.2.0
```

### 3. Gestione Versione

```bash
# Mostra versione corrente
python scripts/update_version.py --show

# Aggiorna versione
python scripts/update_version.py 3.3.0
```

### 4. Backend Web

Il backend FastAPI ora include la versione:

```python
app = FastAPI(
    title="Reversi42 WebSocket Backend",
    version=__version__,  # Legge da pyproject.toml
    ...
)
```

Endpoints disponibili:
- `GET /version` - Restituisce info versione
- `GET /stats` - Include versione nelle statistiche
- `GET /docs` - Swagger UI con versione

## Test di Verifica

```bash
# Test 1: Verifica versione in pyproject.toml
grep "version" pyproject.toml

# Test 2: Verifica import Python
python -c "import sys; sys.path.insert(0, 'src'); from __version__ import __version__; print(__version__)"

# Test 3: Verifica setup.py
python setup.py --version

# Test 4: Usa script di gestione
python scripts/update_version.py --show
```

## Risultati

### ✅ Prima (Problemi):
- Versione in pyproject.toml: **5.0.0**
- Versione in setup.py: **4.1.16**
- Versione in README.md: **3.2.0**
- Versione in altri file: **vari**
- **PROBLEMA**: Nessuna single source of truth!

### ✅ Dopo (Soluzione):
- **Single source**: `pyproject.toml` → **3.2.0**
- `setup.py` → **legge automaticamente**
- `src/__version__.py` → **legge automaticamente**
- `backend_server.py` → **importa da __version__**
- **SOLUZIONE**: Una sola versione da modificare!

## File che Leggono Automaticamente

1. **`src/__version__.py`**
   ```python
   # Legge da pyproject.toml con 3 metodi di fallback
   __version__ = get_version()  # → "3.2.0"
   ```

2. **`setup.py`**
   ```python
   version=get_version()  # Legge da pyproject.toml
   ```

3. **`src/webgui/backend_server.py`**
   ```python
   from __version__ import __version__
   app = FastAPI(version=__version__)
   ```

4. **Qualsiasi altro file**
   ```python
   from __version__ import __version__
   ```

## Come Aggiornare la Versione

### Metodo 1: Script (Consigliato)

```bash
python scripts/update_version.py 3.3.0
```

### Metodo 2: Manuale

1. Apri `pyproject.toml`
2. Trova: `version = "3.2.0"`
3. Cambia in: `version = "3.3.0"`
4. Salva
5. ✅ Fatto! Tutti i file leggeranno automaticamente la nuova versione

## API Versioning

Con il server avviato, puoi interrogare la versione via HTTP:

```bash
# Get version
curl http://localhost:8000/version

# Response:
{
  "version": "3.2.0",
  "name": "Reversi42",
  "description": "Ultra-Fast Reversi (Othello) with Bitboard AI"
}

# Get stats (include version)
curl http://localhost:8000/stats

# Response:
{
  "version": "3.2.0",
  "active_sessions": 0,
  "active_connections": 0,
  "uptime": "N/A"
}
```

## Swagger/OpenAPI

Vai su `http://localhost:8000/docs` per vedere:
- Documentazione API con versione
- Tutti gli endpoints
- License info
- Contact info

## Benefits

### ✅ Single Source of Truth
- Modifica versione in **UN SOLO POSTO**
- Nessuna duplicazione
- Nessun rischio di disallineamento

### ✅ Automatic Propagation
- Tutti i file leggono automaticamente
- No bisogno di aggiornare manualmente
- Sempre sincronizzati

### ✅ Easy to Update
- Un comando: `python scripts/update_version.py X.Y.Z`
- O edit manuale di una sola riga
- Verifica immediata con `--show`

### ✅ Standard Compliant
- Segue PEP 621 (pyproject.toml)
- Compatibile con build tools moderni
- Usa importlib.metadata quando installato

## Files Structure

```
Reversi42/
├── pyproject.toml                 # ← VERSION SOURCE OF TRUTH
├── setup.py                       # Reads from pyproject.toml
├── VERSION_MANAGEMENT.md          # Documentation
├── VERSION_CENTRALIZED_SUMMARY.md # This file
│
├── src/
│   ├── __version__.py             # Module that reads version
│   └── webgui/
│       └── backend_server.py      # Uses __version__
│
└── scripts/
    └── update_version.py          # Version management script
```

## Changelog Format

Quando aggiorni la versione, aggiorna anche `CHANGELOG.md`:

```markdown
## [3.3.0] - 2025-11-03

### Added
- New feature X

### Changed
- Modified feature Y

### Fixed
- Bug Z
```

## Release Workflow

```bash
# 1. Update version
python scripts/update_version.py 3.3.0

# 2. Update CHANGELOG.md
# (manually)

# 3. Run tests
pytest

# 4. Commit
git add pyproject.toml CHANGELOG.md
git commit -m "Release v3.3.0"

# 5. Tag
git tag v3.3.0

# 6. Push
git push && git push --tags
```

---

**🎯 Remember**: Only edit version in `pyproject.toml`!

Everything else updates automatically! ✨

