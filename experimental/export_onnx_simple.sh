#!/bin/bash
# Script semplice per esportare modello ONNX
# Usage: ./export_onnx_simple.sh

set -e

echo "=========================================="
echo "Export RL Model to ONNX"
echo "=========================================="
echo ""

# Vai alla root del progetto
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

echo "Project root: $PROJECT_ROOT"
echo ""

# Verifica ambiente
if ! python3 -c "import torch" 2>/dev/null; then
    echo "❌ PyTorch non installato!"
    echo ""
    echo "Installa PyTorch:"
    echo "  pip install torch>=2.0.0"
    echo ""
    echo "Oppure attiva ambiente con PyTorch:"
    echo "  conda activate reversi42_rl"
    exit 1
fi

# Verifica onnx package (richiesto per export)
if ! python3 -c "import onnx" 2>/dev/null; then
    echo "⚠️  Pacchetto 'onnx' non installato (richiesto per esportazione)"
    echo "Installazione onnx..."
    pip install onnx>=1.14.0 --quiet
    echo "✓ onnx installato"
else
    echo "✓ onnx OK"
fi

# Verifica NumPy compatibile
NUMPY_VERSION=$(python3 -c "import numpy; print(numpy.__version__)" 2>/dev/null || echo "not installed")
if [ "$NUMPY_VERSION" != "not installed" ]; then
    MAJOR=$(echo $NUMPY_VERSION | cut -d. -f1)
    if [ "$MAJOR" -ge 2 ]; then
        echo "⚠️  NumPy $NUMPY_VERSION incompatibile (richiesto < 2.0)"
        echo "Downgrading NumPy..."
        pip install "numpy>=1.24.0,<2.0.0" --quiet
        echo "✓ NumPy aggiornato"
    else
        echo "✓ NumPy $NUMPY_VERSION OK"
    fi
fi

# Verifica modello
MODEL_PATH="$PROJECT_ROOT/experimental/checkpoints/latest.pth"
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Modello non trovato: $MODEL_PATH"
    exit 1
fi

echo "✓ Modello trovato: $MODEL_PATH"
echo ""

# Crea directory output
OUTPUT_DIR="$PROJECT_ROOT/config/neuralnetwork"
mkdir -p "$OUTPUT_DIR"

# Esporta usando Python con path corretto
echo "Esportazione in corso..."
cd "$PROJECT_ROOT"

python3 << PYTHON_SCRIPT
import sys
import os
from pathlib import Path

# Setup paths
project_root = Path("$PROJECT_ROOT")
experimental_dir = project_root / "experimental"
src_dir = project_root / "src"

for path in [str(experimental_dir), str(src_dir), str(project_root)]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import and export
from experimental.rl_player.utils.export_model import export_to_onnx

model_path = "$MODEL_PATH"
output_path = "$OUTPUT_DIR/latest_onnx.onnx"

print("Exporting to ONNX...")
export_to_onnx(model_path, output_path, input_channels=8)
print(f"✓ Export completed: {output_path}")
PYTHON_SCRIPT

echo ""
echo "=========================================="
echo "✅ Esportazione completata!"
echo "=========================================="
echo ""
echo "Modello ONNX: $OUTPUT_DIR/latest_onnx.onnx"
echo ""
echo "Ora puoi usare il giocatore RL con ONNX Runtime (leggero)."

