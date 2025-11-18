#!/usr/bin/env python3
"""
Script per pubblicare il package su PyPI.

Uso:
    python scripts/publish_pypi.py
    
    Oppure con token esplicito:
    PYPI_API_TOKEN=pypi-tuo-token python scripts/publish_pypi.py
"""

import os
import sys
import subprocess
from pathlib import Path

def publish_to_pypi():
    """Pubblica il package su PyPI."""
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "dist"
    
    if not dist_dir.exists():
        print("❌ Directory dist/ non trovata. Esegui prima: python -m build")
        return False
    
    # Trova i file da pubblicare (solo versione specifica o ultima)
    import re
    
    # Prova a rilevare la versione corrente dal codice
    try:
        sys.path.insert(0, str(project_root / "src"))
        from __version__ import __version__ as current_version
        version = os.getenv('PUBLISH_VERSION', current_version)
    except ImportError:
        # Fallback: leggi da pyproject.toml
        try:
            pyproject_path = project_root / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip().startswith("version"):
                            version = line.split("=")[1].strip().strip('"').strip("'")
                            break
            else:
                version = os.getenv('PUBLISH_VERSION', '7.0.5')
        except Exception:
            version = os.getenv('PUBLISH_VERSION', '7.0.5')
    
    wheel_files = [f for f in dist_dir.glob("*.whl") if version in f.name]
    sdist_files = [f for f in dist_dir.glob("*.tar.gz") if version in f.name]
    
    if not wheel_files and not sdist_files:
        print(f"❌ Nessun file per versione {version} trovato in dist/")
        return False
    
    files_to_upload = wheel_files + sdist_files
    print(f"📦 File da pubblicare: {len(files_to_upload)}")
    for f in files_to_upload:
        print(f"   - {f.name}")
    
    # Verifica token
    token = os.getenv('PYPI_API_TOKEN') or os.getenv('TWINE_PASSWORD')
    if not token:
        print("\n⚠️  Token PyPI non trovato!")
        print("\nOpzioni:")
        print("1. Imposta variabile d'ambiente:")
        print("   export PYPI_API_TOKEN=pypi-tuo-token")
        print("2. Oppure pubblica manualmente:")
        print("   twine upload dist/reversi42-7.0.0b1* --repository pypi")
        print("\n💡 Ottieni il token su: https://pypi.org/manage/account/token/")
        return False
    
    # Pubblica con twine
    print("\n🚀 Pubblicazione su PyPI...")
    try:
        # Usa twine se disponibile
        result = subprocess.run(
            [
                sys.executable, "-m", "twine", "upload",
                *[str(f) for f in files_to_upload],
                "--repository", "pypi",
                "--non-interactive",
                "--username", "__token__",
                "--password", token,
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Pubblicazione completata con successo!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore durante la pubblicazione:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("❌ twine non trovato. Installa con: pip install twine")
        return False

if __name__ == '__main__':
    success = publish_to_pypi()
    sys.exit(0 if success else 1)

