#!/usr/bin/env python3
"""
Ensure ONNX model exists for RL Player.

This script checks if an ONNX model exists, and if not, tries to export it
from the PyTorch model. If PyTorch is not available, it provides instructions.
"""

import sys
import os
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "experimental"))

def main():
    """Ensure ONNX model exists."""
    pth_model = project_root / "experimental" / "checkpoints" / "latest.pth"
    onnx_model = project_root / "experimental" / "checkpoints" / "exported" / "latest_onnx.onnx"
    
    # Create exported directory
    onnx_model.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("RL Player - ONNX Model Check")
    print("=" * 70)
    print()
    
    # Check if ONNX model exists
    if onnx_model.exists():
        size_mb = onnx_model.stat().st_size / (1024 * 1024)
        print(f"✓ ONNX model found: {onnx_model}")
        print(f"  Size: {size_mb:.1f} MB")
        print()
        print("✅ ONNX model ready! RL Player can use lightweight inference.")
        return 0
    
    print(f"⚠️  ONNX model not found: {onnx_model}")
    print()
    
    # Check if PyTorch model exists
    if not pth_model.exists():
        print(f"❌ PyTorch model not found: {pth_model}")
        print()
        print("Please train a model first or provide a model checkpoint.")
        return 1
    
    print(f"✓ PyTorch model found: {pth_model}")
    print()
    print("Attempting to export to ONNX...")
    print()
    
    # Try to import PyTorch
    try:
        import torch
        print(f"✓ PyTorch available: {torch.__version__}")
    except ImportError:
        print("❌ PyTorch not installed")
        print()
        print("To export the model to ONNX, install PyTorch:")
        print("  pip install torch>=2.0.0")
        print()
        print("Then run:")
        print(f"  python experimental/rl_player/utils/export_model.py \\")
        print(f"    {pth_model} \\")
        print(f"    --format onnx \\")
        print(f"    --output-dir {onnx_model.parent}")
        print()
        print("Or use the automatic script:")
        print("  ./experimental/setup_rl_lightweight.sh")
        return 1
    
    # Try to export
    try:
        from experimental.rl_player.utils.export_model import export_to_onnx
        
        print("Exporting model to ONNX format...")
        export_to_onnx(
            str(pth_model),
            str(onnx_model),
            input_channels=8
        )
        
        if onnx_model.exists():
            size_mb = onnx_model.stat().st_size / (1024 * 1024)
            print()
            print("=" * 70)
            print("✅ Success!")
            print("=" * 70)
            print(f"ONNX model exported: {onnx_model}")
            print(f"Size: {size_mb:.1f} MB")
            print()
            print("RL Player is now ready to use lightweight ONNX inference!")
            return 0
        else:
            print("❌ Export failed - model file not created")
            return 1
            
    except Exception as e:
        print(f"❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

