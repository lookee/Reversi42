# Perché Non Vedi Altri File?

## 🔍 Situazione Attuale

Nella directory `checkpoints/` vedi solo:
- `latest_corrupted.pth` (27 MB)

**Mancano**:
- ❌ `latest.pth` (checkpoint corrente)
- ❌ `training_state.json` (stato training)
- ❌ `checkpoint_*.pth` (checkpoint numerati)

## 📋 Perché Non Ci Sono Altri File?

### 1. Checkpoint Salvati Ogni 1000 Iterazioni

Dalla configurazione (`rl_config.yaml`):
```yaml
checkpoint:
  save_frequency: 1000  # Salva ogni 1000 iterazioni
```

**Significa**:
- ✅ Checkpoint vengono salvati solo ogni **1000 iterazioni**
- ✅ Se il training è a iterazione < 1000, **nessun checkpoint ancora salvato**
- ✅ `latest.pth` viene creato solo quando salvi un checkpoint

### 2. Training State Non Salvato

`training_state.json` viene salvato:
- ✅ All'inizio del training
- ✅ Dopo ogni iterazione
- ❌ Se il training non è mai partito o è crashato subito, non esiste

### 3. Il Training Potrebbe Non Essere Partito

Possibili scenari:
1. **Training non avviato**: Non hai ancora avviato il training
2. **Training interrotto subito**: Si è fermato prima del primo salvataggio
3. **Training in corso**: Sta ancora facendo la prima iterazione (può richiedere ore!)

## 🔍 Verifica Stato Training

### Controlla se il Training è in Corso

```bash
# Verifica processi Python
ps aux | grep train.py

# Verifica se c'è un processo di training attivo
```

### Controlla Log

```bash
# Cerca file di log
find experimental -name "*.log" -o -name "training_*.txt"
```

### Verifica Directory

```bash
cd experimental
ls -lah

# Dovresti vedere:
# - checkpoints/
# - config/
# - rl_player/
# - training_data/ (se training è partito)
# - logs/ (se configurato)
```

## 🎯 Cosa Significa

### Scenario 1: Training Non Ancora Avviato

Se non hai ancora avviato il training:
- ✅ Normale non vedere checkpoint
- ✅ Avvia il training: `python experimental/rl_player/train.py`
- ✅ I checkpoint verranno creati dopo 1000 iterazioni

### Scenario 2: Training Interrotto Prima del Primo Salvataggio

Se il training si è fermato prima di 1000 iterazioni:
- ✅ Normale non vedere `latest.pth`
- ✅ Il training riprenderà da iterazione 0
- ✅ I checkpoint verranno creati quando raggiungi 1000 iterazioni

### Scenario 3: Training in Corso

Se il training sta ancora girando:
- ✅ Sta ancora facendo self-play (può richiedere 10+ ore per 100 giochi)
- ✅ Nessun checkpoint ancora perché < 1000 iterazioni
- ✅ Usa `monitor_training.py` per vedere progresso

## 📊 Quando Vedrai i Checkpoint?

### Timeline Attesa

```
Iterazione 0: Training inizia
  ↓
Iterazione 1-999: Self-play e training (nessun checkpoint salvato)
  ↓
Iterazione 1000: ✅ PRIMO CHECKPOINT SALVATO
  - latest.pth creato
  - checkpoint_1000.pth creato
  - training_state.json aggiornato
  ↓
Iterazione 2000: ✅ SECONDO CHECKPOINT
  - checkpoint_2000.pth creato
  ↓
...
```

### Tempo per Primo Checkpoint

Con configurazione standard:
- **100 giochi per iterazione**: ~10 ore
- **1000 iterazioni**: ~10,000 ore = **~417 giorni** ❌

**Questo è troppo!** Probabilmente vuoi modificare la configurazione.

## 🔧 Soluzione: Modifica Frequenza Salvataggio

### Opzione 1: Salva Più Spesso (Raccomandato)

Modifica `experimental/config/rl_config.yaml`:

```yaml
checkpoint:
  save_frequency: 10  # Salva ogni 10 iterazioni invece di 1000
  config_save_frequency: 10
```

**Risultato**:
- ✅ Checkpoint ogni ~100 ore (10 iterazioni × 10 ore)
- ✅ Più frequente, più sicuro
- ✅ Puoi monitorare progresso meglio

### Opzione 2: Salva Sempre Latest

Modifica `train.py` per salvare `latest.pth` sempre:

```python
# Salva latest.pth dopo ogni iterazione (non solo ogni 1000)
latest_path = checkpoints_dir / "latest.pth"
model.save(str(latest_path))
```

**Risultato**:
- ✅ `latest.pth` sempre aggiornato
- ✅ Puoi riprendere training sempre
- ✅ Checkpoint numerati ogni 1000 iterazioni

## ✅ Verifica Cosa Sta Succedendo

### Step 1: Controlla se Training è Attivo

```bash
# Verifica processi
ps aux | grep python | grep train
```

### Step 2: Verifica Training State

```bash
cd experimental/checkpoints
cat training_state.json 2>/dev/null || echo "No training state"
```

### Step 3: Avvia Monitor

```bash
python experimental/rl_player/monitor_training.py
```

Questo ti dirà:
- Se il training è attivo
- A che iterazione sei
- Quando verrà salvato il prossimo checkpoint

## 🎯 Raccomandazione

### Per Test e Sviluppo

Modifica configurazione per salvare più spesso:

```yaml
checkpoint:
  save_frequency: 10  # Ogni 10 iterazioni
```

### Per Training Serio

```yaml
checkpoint:
  save_frequency: 100  # Ogni 100 iterazioni (~1000 ore)
```

### Per Training Veloce

```yaml
checkpoint:
  save_frequency: 1  # Ogni iterazione (per test)
```

## 💡 Conclusione

**Non vedi altri file perché**:
1. ✅ Checkpoint salvati solo ogni 1000 iterazioni
2. ✅ Training probabilmente non ha ancora raggiunto 1000 iterazioni
3. ✅ `latest.pth` creato solo quando salvi checkpoint

**Cosa fare**:
1. ✅ Verifica se training è attivo
2. ✅ Modifica `save_frequency` per salvare più spesso
3. ✅ Usa `monitor_training.py` per vedere progresso

**Vuoi che modifichi la configurazione per salvare più spesso?** 🚀

