# Setup RL Player - Guida Installazione Dipendenze

## 📦 Dipendenze Necessarie

Il giocatore RL può funzionare in **due modi**:

### 🪶 Opzione Leggera (Consigliata)
- **ONNX Runtime** (~50MB) - Molto più leggero di PyTorch
- Nessun PyTorch necessario per l'inferenza
- **Installazione**: `pip install onnxruntime`

### 🔥 Opzione Completa
- **PyTorch** (~2GB) - Necessario solo per addestramento o MCTS
- **NumPy** - Compatibile con PyTorch
- **Installazione**: `pip install torch>=2.0.0 "numpy>=1.24.0,<2.0.0"`

Le dipendenze sono **opzionali** - il giocatore RL non sarà disponibile se non installate.

## 🚀 Installazione Rapida

### ⭐ Opzione 1: Leggera (ONNX) - CONSIGLIATA

Se vuoi solo **giocare contro** il giocatore RL senza PyTorch:

```bash
# 1. Esporta il modello in formato ONNX (serve PyTorch solo una volta)
python experimental/rl_player/utils/export_model.py \
    experimental/checkpoints/latest.pth \
    --format onnx \
    --output-dir experimental/checkpoints/exported

# 2. Installa solo ONNX Runtime (leggero ~50MB)
pip install onnxruntime

# 3. Usa il modello ONNX nel config YAML
# Modifica config/players/enabled/gladiators/rl_player.yaml:
#   rl:
#     model_path: "experimental/checkpoints/exported/latest_onnx.onnx"
```

**Vantaggi**: 
- ✅ Molto più leggero (~50MB vs ~2GB)
- ✅ Nessun PyTorch necessario
- ✅ Più veloce al caricamento
- ⚠️ MCTS non disponibile (solo policy diretta)

### Opzione 2: Completa (PyTorch)

Se vuoi usare **MCTS** o addestrare:

```bash
# Installa PyTorch (con supporto MPS per M1/M2 Mac)
pip install torch>=2.0.0

# Installa NumPy compatibile
pip install "numpy>=1.24.0,<2.0.0"
```

**Nota per Mac M1/M2**: PyTorch installerà automaticamente il supporto MPS (Metal Performance Shaders) per accelerazione GPU.

### Opzione 2: Per Addestramento Completo

Se vuoi anche **addestrare** il giocatore RL:

```bash
# Installa tutte le dipendenze RL
pip install -r experimental/requirements-rl.txt
```

Questo installerà:
- PyTorch + TorchVision + TorchAudio
- NumPy (versione compatibile)
- TensorBoard (visualizzazione training)
- Weights & Biases (opzionale, tracking esperimenti)
- Altre dipendenze per training

## ✅ Verifica Installazione

Dopo l'installazione, verifica che tutto funzioni:

```bash
python -c "import torch; print(f'✓ PyTorch {torch.__version__}'); print(f'✓ MPS disponibile: {torch.backends.mps.is_available()}')"
```

Dovresti vedere:
```
✓ PyTorch 2.x.x
✓ MPS disponibile: True  # Su Mac M1/M2
```

## 🎮 Test Giocatore RL

Testa che il giocatore RL funzioni:

```bash
python experimental/test_rl_player.py
```

## ⚠️ Problemi Comuni

### "ModuleNotFoundError: No module named 'torch'"

**Soluzione**: Installa PyTorch:
```bash
pip install torch>=2.0.0
```

### "NumPy 1.x cannot be run in NumPy 2.3.5"

**Soluzione**: Installa NumPy compatibile:
```bash
pip install "numpy>=1.24.0,<2.0.0"
```

### "Model not found"

**Soluzione**: Assicurati che il modello esista:
```bash
ls experimental/checkpoints/latest.pth
```

Se non esiste, devi prima addestrare il modello:
```bash
python experimental/rl_player/train.py
```

## 📋 Dipendenze Minime per RL Player

Le dipendenze **minime** necessarie per usare il giocatore RL sono:

```
torch>=2.0.0
numpy>=1.24.0,<2.0.0
```

Tutte le altre dipendenze (TensorBoard, WandB, etc.) sono solo per l'addestramento.

## 🔧 Installazione Conda (Consigliata)

Se usi Conda, puoi installare PyTorch così:

```bash
# Crea ambiente (se non esiste)
conda create -n reversi42_rl python=3.11
conda activate reversi42_rl

# Installa PyTorch con MPS (Mac M1/M2)
conda install pytorch torchvision torchaudio -c pytorch

# Installa NumPy compatibile
conda install "numpy<2.0.0"

# Installa altre dipendenze Reversi42
pip install -r requirements.txt
```

## 📝 Note

- **PyTorch è grande** (~2GB): considera se ne hai bisogno prima di installarlo
- **RL Player è opzionale**: Reversi42 funziona perfettamente senza di esso
- **MPS su Mac**: PyTorch usa automaticamente la GPU M1/M2 se disponibile
- **CUDA su Linux/Windows**: PyTorch userà automaticamente CUDA se disponibile

## 🎯 Quick Start

```bash
# 1. Installa dipendenze minime
pip install torch>=2.0.0 "numpy>=1.24.0,<2.0.0"

# 2. Verifica installazione
python -c "import torch; print('✓ PyTorch OK')"

# 3. Test giocatore RL
python experimental/test_rl_player.py

# 4. Avvia web GUI e seleziona "RL Player"
python -m src.ui.web
```

---

**Domande?** Controlla `experimental/requirements-rl.txt` per la lista completa delle dipendenze.

