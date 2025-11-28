"""
Model Export Utilities

Export trained RL model to formats suitable for inference with minimal dependencies:
- TorchScript (JIT) - PyTorch senza training dependencies
- ONNX - Formato standard, supportato da molte librerie
- CoreML (Mac) - Nativo Apple, zero dipendenze Python
"""

import os
import sys
from typing import Optional
from pathlib import Path

# Add paths for imports - must be done before importing torch
# Robust method to find project root by searching for experimental/rl_player

def find_project_root():
    """Find project root by looking for experimental/rl_player directory."""
    # Try from script location first
    if __file__:
        script_file = Path(__file__).resolve()
        # Try going up from script location
        current = script_file.parent
        for _ in range(5):  # Max 5 levels up
            if (current / "experimental" / "rl_player").exists():
                return current
            if current == current.parent:  # Reached filesystem root
                break
            current = current.parent
    
    # Fallback: search from current working directory
    current = Path.cwd()
    while current != current.parent:
        if (current / "experimental" / "rl_player").exists():
            return current
        current = current.parent
    
    # Last resort: assume we're in project root if experimental/rl_player exists here
    if (Path.cwd() / "experimental" / "rl_player").exists():
        return Path.cwd()
    
    raise RuntimeError(
        f"Cannot find project root (looking for experimental/rl_player). "
        f"Current dir: {Path.cwd()}, "
        f"Script file: {__file__ if '__file__' in globals() else 'unknown'}"
    )

project_root = find_project_root()
experimental_dir = project_root / "experimental"
src_dir = project_root / "src"

# Add to path if not already there (use absolute paths)
paths_to_add = [
    str(experimental_dir.resolve()),
    str(src_dir.resolve()),
    str(project_root.resolve())
]
for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

# Final verification
if not (experimental_dir / "rl_player").exists():
    raise RuntimeError(
        f"Cannot find experimental/rl_player directory. "
        f"Project root: {project_root}, Experimental: {experimental_dir}, "
        f"Python path: {sys.path[:3]}"
    )

# Now import torch and neural network
import torch
from experimental.rl_player.core.neural_network import NeuralNetwork


def export_to_torchscript(
    model_path: str,
    output_path: str,
    input_channels: int = 8,
    device: Optional[torch.device] = None
) -> str:
    """
    Export model to TorchScript (JIT) format.
    
    TorchScript allows inference without full PyTorch training dependencies.
    Smaller footprint, faster loading.
    
    Args:
        model_path: Path to trained model (.pth)
        output_path: Path to save TorchScript model (.pt)
        input_channels: Number of input channels
        device: Device to use (auto-detected if None)
        
    Returns:
        Path to exported model
    """
    if device is None:
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    
    # Load model
    model = NeuralNetwork.load(model_path, device=device)
    model.eval_mode()
    
    # Create dummy input
    dummy_input = torch.randn(1, input_channels, 8, 8).to(device)
    
    # Trace model
    traced_model = torch.jit.trace(model.model, dummy_input)
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    traced_model.save(output_path)
    
    print(f"✓ Model exported to TorchScript: {output_path}")
    return output_path


def export_to_onnx(
    model_path: str,
    output_path: str,
    input_channels: int = 8,
    device: Optional[torch.device] = None
) -> str:
    """
    Export model to ONNX format.
    
    ONNX is a standard format supported by many inference engines.
    Can be used with ONNX Runtime (lightweight) instead of PyTorch.
    
    Args:
        model_path: Path to trained model (.pth)
        output_path: Path to save ONNX model (.onnx)
        input_channels: Number of input channels
        device: Device to use (auto-detected if None)
        
    Returns:
        Path to exported model
    """
    try:
        import torch.onnx
    except ImportError:
        raise ImportError(
            "ONNX export requires torch.onnx. Install with: pip install torch"
        )
    
    # Check if onnx package is installed (required by torch.onnx.export)
    try:
        import onnx
    except ImportError:
        raise ImportError(
            "ONNX export requires 'onnx' package. Install with: pip install onnx>=1.14.0"
        )
    
    if device is None:
        device = torch.device("cpu")  # ONNX export typically on CPU
    
    # Load model
    model = NeuralNetwork.load(model_path, device=device)
    model.eval_mode()
    
    # Create dummy input
    dummy_input = torch.randn(1, input_channels, 8, 8).to(device)
    
    # Export to ONNX
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    torch.onnx.export(
        model.model,
        dummy_input,
        output_path,
        input_names=['board_state'],
        output_names=['policy_logits', 'value'],
        dynamic_axes={
            'board_state': {0: 'batch_size'},
            'policy_logits': {0: 'batch_size'},
            'value': {0: 'batch_size'}
        },
        opset_version=11
    )
    
    print(f"✓ Model exported to ONNX: {output_path}")
    return output_path


def export_to_coreml(
    model_path: str,
    output_path: str,
    input_channels: int = 8,
    device: Optional[torch.device] = None
) -> str:
    """
    Export model to CoreML format (Mac only).
    
    CoreML is Apple's native ML format. Zero Python dependencies for inference.
    Can be used directly in iOS/macOS apps.
    
    Args:
        model_path: Path to trained model (.pth)
        output_path: Path to save CoreML model (.mlmodel)
        input_channels: Number of input channels
        device: Device to use (auto-detected if None)
        
    Returns:
        Path to exported model
    """
    try:
        import coremltools as ct
    except ImportError:
        raise ImportError("CoreML export requires coremltools. Install with: pip install coremltools")
    
    if device is None:
        device = torch.device("cpu")
    
    # Load model
    model = NeuralNetwork.load(model_path, device=device)
    model.eval_mode()
    
    # Create dummy input
    dummy_input = torch.randn(1, input_channels, 8, 8).to(device)
    
    # Trace model first
    traced_model = torch.jit.trace(model.model, dummy_input)
    
    # Convert to CoreML
    mlmodel = ct.convert(
        traced_model,
        inputs=[ct.TensorType(name="board_state", shape=(1, input_channels, 8, 8))],
        outputs=[ct.TensorType(name="policy_logits"), ct.TensorType(name="value")],
        compute_units=ct.ComputeUnit.CPU_AND_NEURAL_ENGINE  # Use Neural Engine on M1
    )
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    mlmodel.save(output_path)
    
    print(f"✓ Model exported to CoreML: {output_path}")
    return output_path


def export_all_formats(
    model_path: str,
    output_dir: str,
    input_channels: int = 8
):
    """
    Export model to all available formats.
    
    Args:
        model_path: Path to trained model
        output_dir: Directory to save exported models
        input_channels: Number of input channels
    """
    model_name = Path(model_path).stem
    
    print(f"Exporting model: {model_path}")
    print(f"Output directory: {output_dir}")
    print()
    
    # TorchScript
    try:
        export_to_torchscript(
            model_path,
            os.path.join(output_dir, f"{model_name}_torchscript.pt"),
            input_channels
        )
    except Exception as e:
        print(f"✗ TorchScript export failed: {e}")
    
    # ONNX
    try:
        export_to_onnx(
            model_path,
            os.path.join(output_dir, f"{model_name}_onnx.onnx"),
            input_channels
        )
    except Exception as e:
        print(f"✗ ONNX export failed: {e}")
    
    # CoreML (Mac only)
    try:
        export_to_coreml(
            model_path,
            os.path.join(output_dir, f"{model_name}_coreml.mlmodel"),
            input_channels
        )
    except Exception as e:
        print(f"✗ CoreML export failed: {e}")


if __name__ == "__main__":
    import argparse
    
    # Ensure paths are set up correctly when run as script
    # Get project root (4 levels up: experimental/rl_player/utils/export_model.py)
    script_file = Path(__file__).resolve()
    project_root = script_file.parent.parent.parent.parent
    
    # Add paths if not already there
    experimental_dir = project_root / "experimental"
    src_dir = project_root / "src"
    paths_to_add = [str(experimental_dir), str(src_dir), str(project_root)]
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    # Change to project root for relative paths
    os.chdir(project_root)
    
    parser = argparse.ArgumentParser(description="Export RL model to inference formats")
    parser.add_argument("model_path", help="Path to trained model (.pth)")
    parser.add_argument("--output-dir", default="config/neuralnetwork", help="Output directory for exported models")
    parser.add_argument("--format", choices=["torchscript", "onnx", "coreml", "all"], default="all", help="Export format")
    parser.add_argument("--input-channels", type=int, default=8, help="Number of input channels")
    
    args = parser.parse_args()
    
    # Resolve paths relative to project root
    if not os.path.isabs(args.model_path):
        args.model_path = str(project_root / args.model_path)
    if not os.path.isabs(args.output_dir):
        args.output_dir = str(project_root / args.output_dir)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.format == "all":
        export_all_formats(args.model_path, args.output_dir, args.input_channels)
    elif args.format == "torchscript":
        export_to_torchscript(
            args.model_path,
            os.path.join(args.output_dir, f"{Path(args.model_path).stem}_torchscript.pt"),
            args.input_channels
        )
    elif args.format == "onnx":
        export_to_onnx(
            args.model_path,
            os.path.join(args.output_dir, f"{Path(args.model_path).stem}_onnx.onnx"),
            args.input_channels
        )
    elif args.format == "coreml":
        export_to_coreml(
            args.model_path,
            os.path.join(args.output_dir, f"{Path(args.model_path).stem}_coreml.mlmodel"),
            args.input_channels
        )

