# Guida alla Configurazione dei Secrets GitHub

## Problema
Le versioni 7.0.4 e 7.0.5 non vengono pubblicate automaticamente su PyPI perché il secret `PYPI_API_TOKEN` potrebbe non essere configurato correttamente.

## Soluzione: Configurare il Secret PyPI

### Passo 1: Ottieni il Token PyPI

1. Vai su: https://pypi.org/manage/account/token/
2. Accedi con il tuo account PyPI
3. Clicca su "Add API token"
4. Scegli:
   - **Scope**: "Entire account" (per pubblicare tutti i progetti)
   - **Description**: "GitHub Actions - Reversi42"
5. Clicca su "Add token"
6. **COPIA IL TOKEN** (lo vedrai solo una volta!)

### Passo 2: Configura il Secret su GitHub

1. Vai su: https://github.com/lookee/Reversi42/settings/secrets/actions
2. Clicca su "New repository secret"
3. Compila:
   - **Name**: `PYPI_API_TOKEN`
   - **Secret**: Incolla il token copiato da PyPI
4. Clicca su "Add secret"

### Passo 3: Configura l'Environment (Opzionale ma Consigliato)

Il workflow usa un environment chiamato "pypi". Verifica che esista:

1. Vai su: https://github.com/lookee/Reversi42/settings/environments
2. Se non esiste, crea un nuovo environment chiamato `pypi`
3. Aggiungi il secret `PYPI_API_TOKEN` all'environment
4. (Opzionale) Aggiungi protection rules se necessario

### Passo 4: Verifica il Workflow

1. Vai su: https://github.com/lookee/Reversi42/actions/workflows/release.yml
2. Controlla se ci sono workflow falliti per v7.0.4 o v7.0.5
3. Se ci sono errori, controlla i log per vedere se il problema è il token

### Passo 5: Riavvia il Workflow (se necessario)

Se il workflow non si è attivato automaticamente:

1. Vai su: https://github.com/lookee/Reversi42/actions/workflows/release.yml
2. Clicca su "Run workflow"
3. Seleziona:
   - **Use workflow from**: Branch: master
   - **Version**: Lascia vuoto (per usare il tag più recente)
4. Clicca su "Run workflow"

Oppure, per pubblicare una versione specifica:

1. Vai su: https://github.com/lookee/Reversi42/actions/workflows/release.yml
2. Clicca su "Run workflow"
3. Seleziona:
   - **Use workflow from**: Branch: master
   - **Version**: `7.0.5` (senza il prefisso "v")
4. Clicca su "Run workflow"

## Verifica della Pubblicazione

Dopo che il workflow è completato, verifica:

```bash
# Controlla la versione su PyPI
curl -s https://pypi.org/pypi/reversi42/json | python3 -c "import sys, json; print('Versione su PyPI:', json.load(sys.stdin)['info']['version'])"

# Dovrebbe mostrare: Versione su PyPI: 7.0.5
```

## Pubblicazione Manuale (Alternativa)

Se il workflow continua a fallire, puoi pubblicare manualmente:

```bash
# 1. Assicurati di avere il token
export PYPI_API_TOKEN=pypi-tuo-token

# 2. Pubblica la versione
cd /Users/lucaamore/Documents/devel/Reversi42
PUBLISH_VERSION=7.0.5 python scripts/publish_pypi.py

# Oppure usa twine direttamente
twine upload dist/reversi42-7.0.5* \
  --repository pypi \
  --username __token__ \
  --password $PYPI_API_TOKEN
```

## Troubleshooting

### Il workflow non si attiva
- Verifica che il tag sia stato pushato: `git ls-remote --tags origin | grep v7.0.5`
- Controlla che il pattern del workflow corrisponda: `v[0-9]+.[0-9]+.[0-9]+`

### Il workflow fallisce con "Authentication failed"
- Verifica che il secret `PYPI_API_TOKEN` sia configurato correttamente
- Assicurati che il token non sia scaduto
- Controlla che il token abbia i permessi corretti su PyPI

### Il workflow fallisce con "Package already exists"
- Questo è normale se la versione è già stata pubblicata
- Il workflow usa `skip_existing: true` quindi dovrebbe essere gestito automaticamente

### I badge non si aggiornano
- I badge si aggiornano automaticamente dopo la pubblicazione su PyPI
- Potrebbe richiedere alcuni minuti per la propagazione
- Verifica che il package sia effettivamente su PyPI

## Note Importanti

- **Non condividere mai il token PyPI** pubblicamente
- **Il token è visibile solo una volta** quando viene creato
- **Se perdi il token**, devi crearne uno nuovo
- **Il token può essere revocato** da PyPI se necessario

