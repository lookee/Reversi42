# Guida ai Test WebGUI - Reversi42

Guida completa per eseguire e comprendere i test automatici della componente web di Reversi42.

## 📋 Indice

- [Panoramica](#panoramica)
- [Installazione Rapida](#installazione-rapida)
- [Esecuzione Test](#esecuzione-test)
- [Tipi di Test](#tipi-di-test)
- [Copertura dei Test](#copertura-dei-test)
- [Risoluzione Problemi](#risoluzione-problemi)
- [Best Practices](#best-practices)

## 🎯 Panoramica

La suite di test WebGUI copre tutti gli aspetti della componente web:

- **Backend**: Server WebSocket, gestione sessioni, AI
- **Frontend**: JavaScript, rendering, UI
- **Integrazione**: Test end-to-end completi
- **Performance**: Benchmark e ottimizzazione

### Statistiche

- **Test Totali**: 150+
- **Copertura**: > 80%
- **Tempo Esecuzione**: < 2 minuti
- **Linguaggi**: Python, JavaScript

## 🚀 Installazione Rapida

### Prerequisiti

```bash
# Python 3.8+
python3 --version

# Node.js 16+ (per test frontend)
node --version
npm --version
```

### Setup Completo

```bash
# 1. Installa dipendenze Python
pip install -r requirements-dev.txt

# 2. Installa browser per E2E
playwright install

# 3. Installa dipendenze JavaScript
cd tests/webgui
npm install
cd ../..
```

### Verifica Installazione

```bash
# Verifica pytest
python3 -m pytest --version

# Verifica Playwright
python3 -c "import playwright; print('Playwright OK')"

# Verifica Jest
cd tests/webgui && npm test -- --version && cd ../..
```

## 🧪 Esecuzione Test

### Modo Più Semplice

```bash
# Esegui tutti i test (escluso E2E)
./scripts/run_webgui_tests.sh

# Esegui tutti i test (incluso E2E)
./scripts/run_webgui_tests.sh --all

# Con coverage
./scripts/run_webgui_tests.sh --coverage
```

### Test Backend

```bash
# Tutti i test backend
pytest tests/webgui/test_backend_server.py -v

# Test specifico
pytest tests/webgui/test_backend_server.py::TestGameSession::test_game_session_creation -v

# Con output dettagliato
pytest tests/webgui/test_backend_server.py -v -s

# In parallelo
pytest tests/webgui/test_backend_server.py -v -n auto
```

### Test Observer

```bash
# Tutti i test observer
pytest tests/webgui/test_websocket_observer.py -v

# Solo test di notifiche
pytest tests/webgui/test_websocket_observer.py::TestObserverNotifications -v
```

### Test Frontend

```bash
cd tests/webgui

# Tutti i test
npm test

# Con coverage
npm run test:coverage

# In watch mode (ricarica automatica)
npm run test:watch

# Test specifico
npm test -- --testNamePattern="coordToIdx"
```

### Test E2E

```bash
# IMPORTANTE: Avvia prima il server!
# Terminal 1:
python src/webgui/backend_server.py --port 8000

# Terminal 2:
pytest tests/webgui/test_e2e.py -v

# Con browser visibile (headful)
pytest tests/webgui/test_e2e.py -v --headed

# Solo Chrome
pytest tests/webgui/test_e2e.py -v --browser chromium

# Solo Firefox
pytest tests/webgui/test_e2e.py -v --browser firefox
```

## 📊 Tipi di Test

### 1. Test Backend (`test_backend_server.py`)

**Cosa viene testato:**
- ✅ Creazione e gestione sessioni
- ✅ Messaggi WebSocket (init, move, reset, undo/redo)
- ✅ Validazione mosse
- ✅ Integrazione AI
- ✅ Gestione errori
- ✅ Sessioni concorrenti
- ✅ Opening book

**Esempi:**

```python
# Test creazione sessione
def test_game_session_creation():
    session = GameSession("test", "DIVZERO.EXE")
    assert session.ai_white is not None

# Test mossa valida
def test_make_valid_move():
    session = GameSession("test")
    success, error = session.make_move("C4")
    assert success is True

# Test gestione errori
def test_error_handling():
    session = GameSession("test")
    for i in range(5):
        session.handle_error(Exception(f"Error {i}"))
    assert session.error_count == 0  # Reset dopo max
```

### 2. Test Observer (`test_websocket_observer.py`)

**Cosa viene testato:**
- ✅ Lifecycle search (start/complete)
- ✅ Notifiche real-time
- ✅ Tracking statistiche
- ✅ Formatting messaggi
- ✅ Aspiration windows
- ✅ Ricerca parallela

**Esempi:**

```python
# Test search start
async def test_on_search_start():
    observer.on_search_start(depth=8, player_name="AI")
    assert observer.player_name == "AI"

# Test statistiche
def test_calculate_aspiration_rate():
    observer.aspiration_hits = 8
    observer.aspiration_fails = 2
    rate = observer._calculate_aspiration_rate()
    assert rate == 80.0
```

### 3. Test Frontend (`test_frontend.js`)

**Cosa viene testato:**
- ✅ Funzioni utility (coordToIdx, normalize64, countBW)
- ✅ Parsing JSON
- ✅ Rendering scacchiera
- ✅ Validazione mosse
- ✅ Gestione storia
- ✅ Edge cases
- ✅ Performance

**Esempi:**

```javascript
// Test coordinata a indice
test('coordToIdx converts A1 to index 0', () => {
    expect(utils.coordToIdx('A1')).toBe(0);
});

// Test conteggio dischi
test('countBW counts discs correctly', () => {
    const arr = ['B', 'B', 'W', '.', 'W', 'B'];
    const result = utils.countBW(arr);
    expect(result.b).toBe(3);
    expect(result.w).toBe(2);
});

// Test performance
test('coordToIdx is fast', () => {
    const start = Date.now();
    for (let i = 0; i < 10000; i++) {
        utils.coordToIdx('D4');
    }
    expect(Date.now() - start).toBeLessThan(100);
});
```

### 4. Test E2E (`test_e2e.py`)

**Cosa viene testato:**
- ✅ Caricamento pagina
- ✅ Rendering completo
- ✅ Interazioni utente
- ✅ Comunicazione WebSocket
- ✅ Responsive design
- ✅ Compatibilità browser
- ✅ Performance
- ✅ Accessibilità

**Esempi:**

```python
# Test caricamento pagina
async def test_page_loads(page):
    response = await page.goto("http://localhost:8000")
    assert response.status == 200

# Test click mossa
async def test_click_valid_move(page):
    await page.goto("http://localhost:8000")
    valid_move = await page.query_selector('.valid')
    await valid_move.click()
    # Verifica aggiornamento

# Test responsive
async def test_mobile_viewport(browser_context):
    page = await browser_context.new_page()
    await page.set_viewport_size({'width': 375, 'height': 667})
    # Verifica funzionalità
```

## 📈 Copertura dei Test

### Generare Report Coverage

```bash
# Python coverage
pytest tests/webgui/ --cov=src/webgui --cov-report=html
open htmlcov/index.html

# JavaScript coverage
cd tests/webgui
npm run test:coverage
open coverage/index.html
```

### Obiettivi di Copertura

- **Backend**: > 80%
- **Frontend**: > 70%
- **E2E**: Percorsi critici 100%

### Verificare Coverage

```bash
# Verifica coverage minima
pytest tests/webgui/ --cov=src/webgui --cov-fail-under=80
```

## 🔧 Risoluzione Problemi

### Problema: Test Falliscono

**Soluzione 1**: Verifica dipendenze
```bash
pip install -r requirements-dev.txt
cd tests/webgui && npm install
```

**Soluzione 2**: Verifica PATH
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest tests/webgui/ -v
```

**Soluzione 3**: Pulisci cache
```bash
# Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Jest cache
cd tests/webgui && npm test -- --clearCache
```

### Problema: E2E Timeout

**Causa**: Server non in esecuzione

**Soluzione**:
```bash
# Terminal 1: Avvia server
python src/webgui/backend_server.py --port 8000

# Terminal 2: Esegui test
export TEST_SERVER_URL=http://localhost:8000
pytest tests/webgui/test_e2e.py -v
```

### Problema: Playwright Non Trovato

**Soluzione**:
```bash
pip install pytest-playwright
playwright install
```

### Problema: Jest Non Trovato

**Soluzione**:
```bash
cd tests/webgui
npm install
npm test
```

### Problema: Import Error

**Causa**: Esecuzione da directory sbagliata

**Soluzione**:
```bash
# Esegui SEMPRE dalla root del progetto
cd /path/to/Reversi42
pytest tests/webgui/ -v
```

## 🎓 Best Practices

### 1. Esegui Test Prima di Commit

```bash
# Pre-commit hook
./scripts/run_webgui_tests.sh
git commit -m "Your message"
```

### 2. Test Driven Development

```python
# 1. Scrivi test che fallisce
def test_new_feature():
    result = new_feature()
    assert result == expected

# 2. Implementa feature
def new_feature():
    return expected

# 3. Verifica test passa
pytest tests/webgui/test_backend_server.py::test_new_feature -v
```

### 3. Usa Markers per Organizzare

```python
@pytest.mark.slow
def test_performance():
    # Test pesante
    pass

@pytest.mark.e2e
def test_integration():
    # Test integrazione
    pass

# Esegui solo test veloci
pytest tests/webgui/ -v -m "not slow"
```

### 4. Debug Test Falliti

```bash
# Con debugger
pytest tests/webgui/test_backend_server.py --pdb

# Con output dettagliato
pytest tests/webgui/test_backend_server.py -v -s

# Solo test fallito
pytest tests/webgui/test_backend_server.py::test_specific -v
```

### 5. Continuous Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run tests
        run: ./scripts/run_webgui_tests.sh --coverage
```

## 📝 Scenari di Test Importanti

### Scenario 1: Nuova Feature

```bash
# 1. Crea test
vim tests/webgui/test_backend_server.py

# 2. Esegui test (deve fallire)
pytest tests/webgui/test_backend_server.py::test_new_feature -v

# 3. Implementa feature
vim src/webgui/backend_server.py

# 4. Esegui test (deve passare)
pytest tests/webgui/test_backend_server.py::test_new_feature -v

# 5. Verifica tutti i test
./scripts/run_webgui_tests.sh
```

### Scenario 2: Bug Fix

```bash
# 1. Crea test che riproduce bug
def test_bug_reproduction():
    # Riproduci bug
    assert buggy_function() == expected  # Fallisce

# 2. Fix bug
# ... implementa fix ...

# 3. Verifica test passa
pytest tests/webgui/test_backend_server.py::test_bug_reproduction -v
```

### Scenario 3: Refactoring

```bash
# 1. Verifica tutti i test passano
pytest tests/webgui/ -v

# 2. Fai refactoring
# ... modifica codice ...

# 3. Esegui test continuamente
pytest tests/webgui/ -v --looponfail

# 4. Verifica coverage non diminuisce
pytest tests/webgui/ --cov=src/webgui --cov-report=term
```

## 📚 Risorse Aggiuntive

### Documentazione

- [Pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [Playwright Documentation](https://playwright.dev/)

### Tools Utili

```bash
# Profiling test lenti
pytest tests/webgui/ --durations=10

# Test in ordine casuale
pytest tests/webgui/ --random-order

# Ferma al primo fallimento
pytest tests/webgui/ -x

# Esegui solo test modificati di recente
pytest tests/webgui/ --lf  # last failed
pytest tests/webgui/ --ff  # failed first
```

## 🆘 Supporto

### Problemi Comuni

1. **Test lenti**: Usa `-n auto` per parallelizzare
2. **Import errors**: Verifica PYTHONPATH
3. **Timeout E2E**: Aumenta timeout o avvia server
4. **Coverage bassa**: Aggiungi test per codice non coperto

### Ottenere Aiuto

1. Controlla questa guida
2. Leggi i log di test
3. Verifica documentazione
4. Apri issue su GitHub

## 📊 Metriche di Qualità

### Target di Qualità

- ✅ Tutti i test passano
- ✅ Coverage > 80%
- ✅ Nessun flaky test
- ✅ Tempo esecuzione < 2 min
- ✅ Nessun warning

### Verifica Qualità

```bash
# Verifica completa
./scripts/run_webgui_tests.sh --coverage

# Verifica warnings
pytest tests/webgui/ -v -W error

# Verifica stile
pylint src/webgui/
black --check src/webgui/

# Verifica typing
mypy src/webgui/
```

## 🎉 Conclusione

I test automatici sono essenziali per:

- ✅ Prevenire regressioni
- ✅ Documentare comportamento
- ✅ Facilitare refactoring
- ✅ Aumentare confidenza
- ✅ Migliorare qualità

**Esegui sempre i test prima di fare commit!**

```bash
./scripts/run_webgui_tests.sh && git commit -m "Your message"
```

---

**Autore**: Luca Amore  
**Licenza**: GPL-3.0-or-later  
**Versione**: 1.0.0

