# Troubleshooting Guide - Risoluzione Problemi

## Problemi Identificati

### 1. CI Falling ❌
**Causa**: Il file `src/webgui/server/reversi42_server.py` non era formattato correttamente con Black.

**Soluzione**: ✅ **RISOLTO**
- File formattato con `black src/webgui/server/reversi42_server.py`
- Commit pushato: `feab0a1`

**Verifica**:
```bash
black --check src/ tests/
```

---

### 2. Release Falling ❌
**Causa**: Il workflow di release potrebbe fallire per diversi motivi:
- Secret `PYPI_API_TOKEN` non configurato
- Workflow non si attiva correttamente con i tag
- Errori durante il build o la pubblicazione

**Soluzione**:
1. **Verifica che il secret PYPI_API_TOKEN sia configurato**:
   - Vai su: https://github.com/lookee/Reversi42/settings/secrets/actions
   - Assicurati che `PYPI_API_TOKEN` esista e sia valido
   - Ottieni il token su: https://pypi.org/manage/account/token/

2. **Verifica che il workflow si attivi**:
   - Vai su: https://github.com/lookee/Reversi42/actions/workflows/release.yml
   - Controlla se i workflow per v7.0.4 e v7.0.5 sono stati eseguiti
   - Se non si sono attivati, potrebbe essere un problema con il pattern dei tag

3. **Riavvia manualmente il workflow**:
   - Vai su: https://github.com/lookee/Reversi42/actions/workflows/release.yml
   - Clicca su "Run workflow"
   - Seleziona il tag v7.0.5

---

### 3. PyPI Package or Version Not Found ❌
**Causa**: Le versioni 7.0.4 e 7.0.5 non sono state pubblicate su PyPI.

**Stato attuale**:
- Su PyPI: versione 7.0.3 ✅
- Tag creati: v7.0.4, v7.0.5 ✅
- Pubblicazione: ❌ Mancante

**Soluzione**:

#### Opzione A: Pubblicazione Automatica (Consigliata)
Il workflow GitHub Actions dovrebbe pubblicare automaticamente quando:
1. Il tag viene pushato
2. Il secret `PYPI_API_TOKEN` è configurato
3. Il workflow completa con successo

**Verifica**:
```bash
# Controlla se il package è stato pubblicato
curl https://pypi.org/pypi/reversi42/json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['version'])"
```

#### Opzione B: Pubblicazione Manuale
Se il workflow non funziona, puoi pubblicare manualmente:

```bash
# 1. Assicurati di avere il token PyPI
export PYPI_API_TOKEN=pypi-tuo-token

# 2. Pubblica la versione specifica
cd /Users/lucaamore/Documents/devel/Reversi42
PUBLISH_VERSION=7.0.5 python scripts/publish_pypi.py

# Oppure usa twine direttamente
twine upload dist/reversi42-7.0.5* --repository pypi --username __token__ --password $PYPI_API_TOKEN
```

---

### 4. Python Package or Version Not Found ❌
**Causa**: Stesso problema del punto 3 - le versioni non sono su PyPI.

**Soluzione**: Vedi punto 3.

**Verifica badge nel README**:
I badge nel README puntano a PyPI:
- `https://img.shields.io/pypi/v/reversi42.svg` - Mostra l'ultima versione su PyPI
- `https://img.shields.io/pypi/pyversions/reversi42.svg` - Mostra le versioni Python supportate
- `https://img.shields.io/pypi/dm/reversi42.svg` - Mostra i download mensili

Questi badge funzioneranno automaticamente una volta che il package è pubblicato su PyPI.

---

### 5. Download Package Not Found ❌
**Causa**: Stesso problema - il package non è disponibile per il download perché non è stato pubblicato.

**Soluzione**: Vedi punto 3.

---

## Checklist di Risoluzione

### ✅ Passi Immediati

1. **Verifica CI**:
   ```bash
   black --check src/ tests/
   isort --check-only src/ tests/
   pytest tests/ -v
   ```

2. **Verifica Secret PyPI**:
   - Vai su: https://github.com/lookee/Reversi42/settings/secrets/actions
   - Verifica che `PYPI_API_TOKEN` esista

3. **Verifica Workflow Release**:
   - Vai su: https://github.com/lookee/Reversi42/actions/workflows/release.yml
   - Controlla gli ultimi workflow eseguiti
   - Verifica eventuali errori

4. **Pubblica Manualmente (se necessario)**:
   ```bash
   export PYPI_API_TOKEN=pypi-tuo-token
   PUBLISH_VERSION=7.0.5 python scripts/publish_pypi.py
   ```

### 🔍 Debug Workflow

Se il workflow fallisce, controlla:

1. **Log del workflow**:
   - Vai su: https://github.com/lookee/Reversi42/actions
   - Clicca sul workflow fallito
   - Controlla i log di ogni step

2. **Problemi comuni**:
   - Secret non configurato → Aggiungi `PYPI_API_TOKEN` nei secrets
   - Build fallito → Controlla errori di compilazione
   - Test falliti → Risolvi i test che falliscono
   - Formattazione → Esegui `black` e `isort`

### 📝 Note Importanti

- **I badge nel README si aggiornano automaticamente** una volta che il package è su PyPI
- **Il workflow di release si attiva automaticamente** quando un tag viene pushato
- **Le versioni devono essere pubblicate su PyPI** per essere visibili nei badge

---

## Comandi Utili

```bash
# Verifica versione locale
python -c "from src import __version__; print(__version__.__version__)"

# Verifica versione su PyPI
curl -s https://pypi.org/pypi/reversi42/json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['version'])"

# Lista tag locali
git tag -l | grep "7.0" | sort -V

# Lista tag remoti
git ls-remote --tags origin | grep "v7.0"

# Build locale
python -m build

# Verifica package
twine check dist/*

# Pubblica manualmente
twine upload dist/reversi42-7.0.5* --repository pypi --username __token__ --password $PYPI_API_TOKEN
```

---

## Stato Attuale

- ✅ Versione locale: 7.0.5
- ✅ Tag git: v7.0.5 creato e pushato
- ✅ Package buildato: reversi42-7.0.5 disponibile in dist/
- ❌ Pubblicazione PyPI: Mancante (versione 7.0.3 è l'ultima su PyPI)
- ❌ Badge README: Mostreranno 7.0.3 finché 7.0.5 non è pubblicato

---

## Prossimi Passi

1. Verifica che il secret `PYPI_API_TOKEN` sia configurato su GitHub
2. Controlla i log del workflow di release per v7.0.5
3. Se il workflow non si è attivato, riavvialo manualmente
4. Se continua a fallire, pubblica manualmente usando il token PyPI
5. Una volta pubblicato, i badge si aggiorneranno automaticamente

