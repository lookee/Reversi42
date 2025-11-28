# Guida Esportazione Modello ONNX

## ⚠️ Problema NumPy/PyTorch

Se vedi errori come:
- `A module that was compiled using NumPy 1.x cannot be run in NumPy 2.3.5`
- `Failed to initialize NumPy: _ARRAY_API not found`

**Soluzione**: Usa l'ambiente conda corretto con NumPy compatibile.

## 🚀 Soluzione Rapida

### Passo 1: Attiva Ambiente con PyTorch

```bash
# Attiva ambiente che ha PyTorch (es. reversi42_rl)
conda activate reversi42_rl

# Verifica PyTorch
python -c "import torch; print(f'PyTorch: {torch.__version__}')"

# Verifica NumPy compatibile
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
# Dovrebbe essere < 2.0 (es. 1.26.4)
```

### Passo 2: Installa NumPy Compatibile (se necessario)

```bash
# Se NumPy è >= 2.0, downgrade
pip install "numpy>=1.24.0,<2.0.0"
```

### Passo 3: Esporta Modello

```bash
# Dalla root del progetto
cd /Users/lucaamore/Documents/devel/Reversi42

# Usa lo script standalone (più semplice)
python experimental/export_to_onnx.py

# Oppure lo script originale
python experimental/rl_player/utils/export_model.py \
    experimental/checkpoints/latest.pth \
    --format onnx \
    --output-dir config/neuralnetwork
```

## 📋 Setup Completo Ambiente

Se non hai un ambiente con PyTorch:

```bash
# Crea nuovo ambiente
conda create -n reversi42_export python=3.11 -y
conda activate reversi42_export

# Installa PyTorch
conda install pytorch -c pytorch -y

# Installa NumPy compatibile
conda install "numpy<2.0.0" -y

# Esporta modello
cd /Users/lucaamore/Documents/devel/Reversi42
python experimental/export_to_onnx.py

# Dopo l'esportazione, puoi disinstallare PyTorch se vuoi
conda deactivate
```

## ✅ Verifica Esportazione

```bash
# Verifica che il modello ONNX esista
ls -lh config/neuralnetwork/latest_onnx.onnx

# Dovrebbe essere ~20-40MB (più piccolo del .pth)
```

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'torch'"

**Soluzione**: Attiva ambiente con PyTorch o installalo:
```bash
conda activate reversi42_rl
# oppure
pip install torch>=2.0.0
```

### "NumPy 2.x incompatibile"

**Soluzione**: Downgrade NumPy:
```bash
pip install "numpy>=1.24.0,<2.0.0"
```

### "ImportError: attempted relative import"

**Soluzione**: Usa lo script standalone:
```bash
python experimental/export_to_onnx.py
```

## 📝 Note

- L'esportazione richiede PyTorch solo **una volta**
- Dopo l'esportazione, puoi usare solo ONNX Runtime (leggero)
- Il modello ONNX è più piccolo del .pth originale
- ONNX non supporta MCTS (solo policy diretta)

