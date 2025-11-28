#!/bin/bash
# Script per configurare RL Player con ONNX (leggero, senza PyTorch)
# Usage: ./setup_rl_lightweight.sh

set -e

echo "=========================================="
echo "Setup RL Player Lightweight (ONNX)"
echo "=========================================="
echo ""

MODEL_PATH="experimental/checkpoints/latest.pth"
ONNX_OUTPUT="config/neuralnetwork/latest_onnx.onnx"

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Errore: Modello non trovato: $MODEL_PATH"
    exit 1
fi

echo "✓ Modello trovato: $MODEL_PATH"
echo ""

# Check if PyTorch is installed
if python3 -c "import torch" 2>/dev/null; then
    echo "✓ PyTorch installato"
    HAS_TORCH=true
else
    echo "⚠️  PyTorch non installato"
    echo ""
    echo "Installazione PyTorch (necessario solo per esportare)..."
    pip install torch>=2.0.0
    HAS_TORCH=true
fi

# Create output directory
mkdir -p config/neuralnetwork

# Export to ONNX
echo ""
echo "📦 Esportazione modello in formato ONNX..."
python experimental/rl_player/utils/export_model.py \
    "$MODEL_PATH" \
    --format onnx \
    --output-dir config/neuralnetwork

if [ ! -f "$ONNX_OUTPUT" ]; then
    echo "❌ Errore: Esportazione fallita"
    exit 1
fi

echo ""
echo "✓ Modello ONNX esportato: $ONNX_OUTPUT"
echo ""

# Install onnxruntime
echo "📦 Installazione ONNX Runtime..."
pip install onnxruntime

echo ""
echo "=========================================="
echo "✅ Setup completato!"
echo "=========================================="
echo ""
echo "Prossimi passi:"
echo ""
echo "1. Aggiorna config/players/enabled/neural/rl_player.yaml:"
echo "   rl:"
echo "     model_path: \"config/neuralnetwork/latest_onnx.onnx\""
echo "     use_mcts: false  # MCTS non disponibile con ONNX"
echo ""
echo "2. (Opzionale) Se non ti serve PyTorch, puoi disinstallarlo:"
echo "   pip uninstall torch torchvision torchaudio -y"
echo ""
echo "3. Riavvia il server e prova il giocatore RL!"
echo ""

