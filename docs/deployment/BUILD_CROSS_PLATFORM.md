# Build Cross-Platform per Reversi42

Questa guida spiega come creare build per Windows, Linux e macOS.

## 📦 Tipi di Build Disponibili

### 1. Python Package (Wheel + Source Distribution)
**Cross-platform** - Funziona su tutte le piattaforme con Python installato.

```bash
python -m build
```

Produce:
- `reversi42-X.Y.Z-py3-none-any.whl` (wheel package)
- `reversi42-X.Y.Z.tar.gz` (source distribution)

### 2. Eseguibili Standalone (PyInstaller)
**Platform-specific** - Eseguibili che non richiedono Python installato.

- **Windows**: `reversi42-windows-x86_64-X.Y.Z.exe`
- **macOS**: `reversi42-macos-x86_64-X.Y.Z`
- **Linux**: `reversi42-linux-x86_64-X.Y.Z`

## 🔨 Build Locali

### Prerequisiti

```bash
# Installa dipendenze di build
pip install -e ".[build]"
# oppure
pip install pyinstaller setuptools wheel
```

### Build Eseguibile Locale

Lo script `scripts/build_executables.sh` crea un eseguibile per la piattaforma corrente:

```bash
# Build per la piattaforma corrente
./scripts/build_executables.sh

# Oppure specifica la versione
./scripts/build_executables.sh 6.2.2
```

**Nota**: Per creare eseguibili per altre piattaforme, devi eseguire la build su quella piattaforma specifica (o usare GitHub Actions).

### Build Manuale con PyInstaller

```bash
# Build con configurazione personalizzata
pyinstaller reversi42.spec --clean --noconfirm

# L'eseguibile sarà in dist/reversi42 (o dist/reversi42.exe su Windows)
```

## 🚀 Build Automatiche con GitHub Actions

Il workflow `.github/workflows/release.yml` crea automaticamente build per tutte le piattaforme quando:

1. **Push di un tag di versione**:
   ```bash
   git tag v6.2.2
   git push origin v6.2.2
   ```

2. **Workflow dispatch manuale**:
   - Vai su GitHub → Actions → Release
   - Clicca "Run workflow"
   - Inserisci la versione (es. `6.2.2`)

### Cosa Viene Creato

Il workflow crea:

1. **Python Package** (wheel + sdist)
2. **Eseguibili** per Windows, macOS, Linux
3. **Docker Image**
4. **GitHub Release** con tutti gli artefatti

### Download degli Eseguibili

Dopo che il workflow completa:

1. Vai alla [pagina Releases](https://github.com/lookee/Reversi42/releases)
2. Trova la release corrispondente
3. Scarica l'eseguibile per la tua piattaforma:
   - Windows: `reversi42-windows-x86_64-X.Y.Z.exe.zip`
   - macOS: `reversi42-macos-x86_64-X.Y.Z.zip`
   - Linux: `reversi42-linux-x86_64-X.Y.Z.tar.gz`

## 📋 Configurazione PyInstaller

Il file `reversi42.spec` contiene la configurazione per PyInstaller:

- **Entry point**: `src/webgui/cli.py`
- **Data files**: Template HTML, CSS, JS, file di configurazione YAML
- **Hidden imports**: Tutti i moduli necessari per uvicorn, fastapi, websockets
- **Excludes**: Moduli di sviluppo non necessari (pytest, pylint, etc.)

### Personalizzazione

Per modificare la configurazione:

1. Modifica `reversi42.spec`
2. Aggiungi/rimuovi file in `datas`
3. Aggiungi/rimuovi moduli in `hiddenimports`
4. Ricostruisci: `pyinstaller reversi42.spec --clean`

## 🧪 Test degli Eseguibili

Dopo la build, testa l'eseguibile:

```bash
# Linux/macOS
./dist/reversi42 --help
./dist/reversi42 --port 8000

# Windows
dist\reversi42.exe --help
dist\reversi42.exe --port 8000
```

## 🎨 Aggiungere un'Icona

Le icone sono **opzionali** ma migliorano l'aspetto degli eseguibili.

### Formati Richiesti

- **Windows**: `icons/reversi42.ico`
- **macOS**: `icons/reversi42.icns`
- **Linux**: `icons/reversi42.png` (opzionale)

### Come Creare le Icone

Vedi [icons/README.md](../../icons/README.md) per istruzioni dettagliate.

**Quick start**:
1. Prendi un'immagine PNG (almeno 256x256 pixel)
2. Convertila online:
   - Windows: https://convertio.co/png-ico/
   - macOS: https://cloudconvert.com/png-to-icns
3. Salva i file nella directory `icons/`
4. Ricostruisci: `pyinstaller reversi42.spec --clean`

Il file `reversi42.spec` rileverà automaticamente le icone se presenti.

## 🔍 Troubleshooting

### Problema: Eseguibile non trova i file di configurazione

**Soluzione**: Verifica che `reversi42.spec` includa tutti i file necessari nella sezione `datas`.

### Problema: ImportError quando esegui l'eseguibile

**Soluzione**: Aggiungi il modulo mancante alla lista `hiddenimports` in `reversi42.spec`.

### Problema: Build fallisce su GitHub Actions

**Soluzione**: 
1. Controlla i log del workflow
2. Verifica che tutte le dipendenze siano installate
3. Assicurati che `reversi42.spec` sia presente nel repository

### Problema: Eseguibile troppo grande

**Soluzione**: 
1. Rimuovi moduli non necessari da `hiddenimports`
2. Aggiungi più moduli a `excludes` in `reversi42.spec`
3. Usa `upx=True` per comprimere (già abilitato)

## 📚 Risorse Aggiuntive

- [PyInstaller Documentation](https://pyinstaller.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Packaging Guide](https://packaging.python.org/)

## 🎯 Best Practices

1. **Testa sempre localmente** prima di creare una release
2. **Verifica gli eseguibili** su ogni piattaforma quando possibile
3. **Mantieni aggiornato** `reversi42.spec` quando aggiungi nuove dipendenze
4. **Documenta** eventuali requisiti specifici della piattaforma
5. **Firma gli eseguibili** (opzionale ma consigliato per distribuzione pubblica)

