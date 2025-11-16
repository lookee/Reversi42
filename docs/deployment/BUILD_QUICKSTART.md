# Quick Start: Build Cross-Platform

## 🚀 Build Rapida

### Build Locale (Piattaforma Corrente)

```bash
# Installa dipendenze
pip install -e ".[build]"

# Build eseguibile
./scripts/build_executables.sh

# L'eseguibile sarà in dist/
```

### Build Automatica (Tutte le Piattaforme)

1. **Crea un tag di versione**:
   ```bash
   git tag v6.2.2
   git push origin v6.2.2
   ```

2. **GitHub Actions creerà automaticamente**:
   - ✅ Eseguibile Windows
   - ✅ Eseguibile macOS  
   - ✅ Eseguibile Linux
   - ✅ Python wheel package
   - ✅ Docker image

3. **Scarica dalla [pagina Releases](https://github.com/lucaamore/reversi42/releases)**

## 📋 Requisiti

- Python 3.9+
- PyInstaller (`pip install pyinstaller`)
- Tutte le dipendenze del progetto

## 🔍 Verifica Build

```bash
# Test eseguibile
./dist/reversi42 --help
./dist/reversi42 --version
```

## 📚 Documentazione Completa

Vedi [BUILD_CROSS_PLATFORM.md](./BUILD_CROSS_PLATFORM.md) per dettagli completi.

