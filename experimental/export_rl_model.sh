#!/bin/bash
# Script per esportare il modello RL in formato leggero (ONNX)
# Usage: ./export_rl_model.sh [model_path]

set -e

MODEL_PATH="${1:-experimental/checkpoints/latest.pth}"
OUTPUT_DIR="config/neuralnetwork"

echo "=========================================="
echo "Export RL Model to Lightweight Format"
echo "=========================================="
echo ""
echo "Model: $MODEL_PATH"
echo "Output: $OUTPUT_DIR"
echo ""

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Error: Model not found: $MODEL_PATH"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Export to ONNX (lightweight - only needs onnxruntime)
echo "📦 Exporting to ONNX format..."
python experimental/rl_player/utils/export_model.py \
    "$MODEL_PATH" \
    --format onnx \
    --output-dir "$OUTPUT_DIR" \
    --input-channels 8

echo ""
echo "✅ Export completed!"
echo ""
echo "To use the lightweight model:"
echo "  1. Install onnxruntime: pip install onnxruntime"
echo "  2. Update config to use: config/neuralnetwork/latest_onnx.onnx"
echo ""
echo "ONNX Runtime is much lighter than PyTorch (~50MB vs ~2GB)!"

