# Troubleshooting Guide

## Problema: NumPy 2.x Incompatibilità

### Sintomi
```
A module that was compiled using NumPy 1.x cannot be run in NumPy 2.3.5
```

### Soluzione
```bash
conda activate reversi42_rl
pip install "numpy<2.0"
```

### Verifica
```bash
python -c "import numpy; print(numpy.__version__)"
# Dovrebbe mostrare: 1.26.x (non 2.x)
```

## Problema: Percorso Directory

### Sintomi
```
cd: experimental/rl_player: No such file or directory
```

### Soluzione
Lo script `start_training.sh` gestisce automaticamente i percorsi. Se il problema persiste:

```bash
# Vai direttamente nella directory
cd experimental/rl_player
python train.py
```

## Problema: Moduli Non Trovati

### Sintomi
```
ModuleNotFoundError: No module named 'experimental.rl_player'
```

### Soluzione
Assicurati di essere nella directory corretta:

```bash
# Dalla root del progetto
cd /Users/lucaamore/Documents/devel/Reversi42
conda activate reversi42_rl
cd experimental/rl_player
python train.py
```

## Verifica Setup Completo

```bash
# 1. Attiva ambiente
conda activate reversi42_rl

# 2. Verifica Python
python --version  # Dovrebbe essere 3.11.x

# 3. Verifica dipendenze
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import torch; print('MPS:', torch.backends.mps.is_available())"

# 4. Verifica struttura
ls experimental/rl_player/train.py  # Dovrebbe esistere
```

## Reset Completo Ambiente

Se tutto fallisce:

```bash
# Rimuovi ambiente
conda env remove -n reversi42_rl

# Ricrea
conda create -n reversi42_rl python=3.11 -y
conda activate reversi42_rl

# Installa dipendenze (con NumPy < 2.0)
pip install -r experimental/requirements-rl.txt
```

