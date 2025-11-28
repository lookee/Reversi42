#!/usr/bin/env python3
"""
Standalone script to export RL model to ONNX format.
Can be run from anywhere in the project.
"""

import sys
import os
from pathlib import Path

# Get project root
# This script is in experimental/, so project root is parent
if '__file__' in globals() and Path(__file__).exists():
    script_path = Path(__file__).resolve()
    # experimental/export_to_onnx.py -> parent = experimental -> parent = Reversi42
    experimental_dir = script_path.parent
    project_root = experimental_dir.parent
else:
    # Fallback: find project root by looking for experimental/rl_player directory
    project_root = Path.cwd()
    current = Path.cwd()
    # If we're in experimental/, go up one level
    if (current / "rl_player").exists():
        project_root = current.parent
        experimental_dir = current
    else:
        # Search upwards
        while current != current.parent:
            if (current / "experimental" / "rl_player").exists():
                project_root = current
                break
            current = current.parent
        experimental_dir = project_root / "experimental"

# Verify we found the right project root
if not (project_root / "experimental" / "rl_player").exists():
    print(f"❌ Error: Cannot find experimental/rl_player directory")
    print(f"   Project root: {project_root}")
    print(f"   Experimental dir: {experimental_dir}")
    print(f"   Current dir: {Path.cwd()}")
    print(f"   Script file: {__file__ if '__file__' in globals() else 'unknown'}")
    sys.exit(1)

# Add paths (use absolute paths)
experimental_dir = project_root / "experimental"
src_dir = project_root / "src"

paths_to_add = [
    str(experimental_dir.resolve()),
    str(src_dir.resolve()),
    str(project_root.resolve())
]
for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

# Change to project root for relative paths
os.chdir(project_root)

# Now import and run export
try:
    from experimental.rl_player.utils.export_model import export_to_onnx
    
    model_path = "experimental/checkpoints/latest.pth"
    output_dir = "config/neuralnetwork"
    output_path = os.path.join(output_dir, "latest_onnx.onnx")
    
    print("=" * 70)
    print("Export RL Model to ONNX")
    print("=" * 70)
    print(f"Model: {model_path}")
    print(f"Output: {output_path}")
    print()
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"❌ Error: Model not found: {model_path}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Export
    print("Exporting...")
    export_to_onnx(model_path, output_path, input_channels=8)
    
    print()
    print("=" * 70)
    print("✅ Export completed!")
    print("=" * 70)
    print(f"ONNX model: {output_path}")
    print()
    print("You can now use the RL Player with ONNX Runtime (lightweight).")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print()
    print("Make sure you have:")
    print("  1. PyTorch installed: pip install torch>=2.0.0")
    print("  2. ONNX package installed: pip install onnx>=1.14.0")
    print("  3. NumPy compatible: pip install 'numpy>=1.24.0,<2.0.0'")
    print()
    print("Quick fix:")
    print("  pip install torch>=2.0.0 onnx>=1.14.0 'numpy>=1.24.0,<2.0.0'")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

