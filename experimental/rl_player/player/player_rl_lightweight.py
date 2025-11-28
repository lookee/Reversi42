"""
Lightweight RL Player - Minimal Dependencies

This player can be used with minimal dependencies by using exported models:
- TorchScript: Only needs torch (no training dependencies)
- ONNX: Only needs onnxruntime (very lightweight)
- CoreML: Zero Python dependencies (Mac only)

Design: Lazy loading - only imports what's needed when model is loaded.
"""

import os
import sys
from typing import List, Optional
from pathlib import Path

# Add src to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from Players.Player import Player
from Reversi.Game import Move
from Reversi.BitboardGame import BitboardGame


class PlayerRLLightweight(Player):
    """
    Lightweight RL Player with minimal dependencies.
    
    Supports multiple model formats:
    - PyTorch (.pth) - Full PyTorch required
    - TorchScript (.pt) - Only torch required (no training)
    - ONNX (.onnx) - Only onnxruntime required
    - CoreML (.mlmodel) - Zero Python dependencies (Mac)
    
    Design Pattern: Lazy Loading + Strategy
    - Only loads inference library when needed
    - Supports multiple inference backends
    """
    
    PLAYER_METADATA = {
        "display_name": "RL Player (Lightweight)",
        "description": "Deep RL player - Lightweight inference",
        "enabled": True,
        "parameters": {
            "model_path": {
                "type": str,
                "default": "experimental/checkpoints/best.pth",
                "description": "Path to model (supports .pth, .pt, .onnx, .mlmodel)"
            },
            "temperature": {
                "type": float,
                "default": 0.1,
                "min": 0.0,
                "max": 1.0,
                "description": "Sampling temperature (0=deterministic)"
            },
            "use_mcts": {
                "type": bool,
                "default": False,
                "description": "Use MCTS for move selection (requires full RL dependencies)"
            },
            "mcts_simulations": {
                "type": int,
                "default": 800,
                "min": 100,
                "max": 2000,
                "description": "MCTS simulations (only if use_mcts=True)"
            }
        }
    }
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        temperature: float = 0.1,
        use_mcts: bool = False,
        mcts_simulations: int = 800
    ):
        """
        Initialize lightweight RL player.
        
        Args:
            model_path: Path to model file (auto-detects format)
            temperature: Sampling temperature
            use_mcts: Whether to use MCTS (requires full dependencies)
            mcts_simulations: MCTS simulations if enabled
        """
        super().__init__()
        self.name = "RL Player (Lightweight)"
        
        if model_path is None:
            # Try to find best model
            checkpoints_dir = Path(__file__).parent.parent.parent / "checkpoints"
            model_path = checkpoints_dir / "best.pth"
            if not model_path.exists():
                model_path = checkpoints_dir / "latest.pth"
        
        self.model_path = str(model_path)
        self.temperature = temperature
        self.use_mcts = use_mcts
        self.mcts_simulations = mcts_simulations
        
        # Lazy loading - will be initialized on first use
        self._model = None
        self._model_type = None
        self._inference_fn = None
        
        # Detect model format
        self._detect_model_format()
    
    def _detect_model_format(self):
        """Detect model format from file extension."""
        path = Path(self.model_path)
        ext = path.suffix.lower()
        
        if ext == ".pth":
            self._model_type = "pytorch"
        elif ext == ".pt":
            self._model_type = "torchscript"
        elif ext == ".onnx":
            self._model_type = "onnx"
        elif ext == ".mlmodel":
            self._model_type = "coreml"
        else:
            raise ValueError(f"Unsupported model format: {ext}. Supported: .pth, .pt, .onnx, .mlmodel")
    
    def _load_model(self):
        """Lazy load model based on format."""
        if self._model is not None:
            return
        
        if self._model_type == "pytorch":
            self._load_pytorch_model()
        elif self._model_type == "torchscript":
            self._load_torchscript_model()
        elif self._model_type == "onnx":
            self._load_onnx_model()
        elif self._model_type == "coreml":
            self._load_coreml_model()
    
    def _load_pytorch_model(self):
        """Load PyTorch model (full dependencies)."""
        try:
            import torch
            from experimental.rl_player.core.neural_network import NeuralNetwork
            
            device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
            self._model = NeuralNetwork.load(self.model_path, device=device)
            self._model.eval_mode()
            self._inference_fn = self._pytorch_inference
        except ImportError:
            raise ImportError("PyTorch model requires torch. Install with: pip install torch")
    
    def _load_torchscript_model(self):
        """Load TorchScript model (only torch, no training)."""
        try:
            import torch
            
            device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
            self._model = torch.jit.load(self.model_path, map_location=device)
            self._model.eval()
            self._inference_fn = self._torchscript_inference
        except ImportError:
            raise ImportError("TorchScript model requires torch. Install with: pip install torch")
    
    def _load_onnx_model(self):
        """Load ONNX model (only onnxruntime)."""
        try:
            import onnxruntime as ort
            
            # Create inference session
            providers = ['CPUExecutionProvider']
            if ort.get_device() == 'GPU':
                providers.insert(0, 'CUDAExecutionProvider')
            
            self._model = ort.InferenceSession(self.model_path, providers=providers)
            self._inference_fn = self._onnx_inference
        except ImportError:
            raise ImportError("ONNX model requires onnxruntime. Install with: pip install onnxruntime")
    
    def _load_coreml_model(self):
        """Load CoreML model (zero Python dependencies)."""
        try:
            import coremltools as ct
            
            self._model = ct.models.MLModel(self.model_path)
            self._inference_fn = self._coreml_inference
        except ImportError:
            raise ImportError("CoreML model requires coremltools. Install with: pip install coremltools")
    
    def _encode_state(self, game: BitboardGame, player_color: str):
        """Encode game state to tensor."""
        from experimental.rl_player.utils.state_encoder import encode_state
        
        return encode_state(
            game,
            player_color,
            use_advanced_features=True,
            use_opening_book=True
        )
    
    def _pytorch_inference(self, state):
        """PyTorch inference."""
        import torch
        
        state_batch = state.unsqueeze(0).to(self._model.device)
        policy_logits, value = self._model.forward(state_batch)
        return policy_logits[0].cpu().numpy(), value[0].item()
    
    def _torchscript_inference(self, state):
        """TorchScript inference."""
        import torch
        
        device = next(self._model.parameters()).device if hasattr(self._model, 'parameters') else torch.device("cpu")
        state_batch = state.unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = self._model(state_batch)
            if isinstance(outputs, tuple):
                policy_logits, value = outputs
            else:
                policy_logits = outputs[0]
                value = outputs[1]
        
        return policy_logits[0].cpu().numpy(), value[0].item()
    
    def _onnx_inference(self, state):
        """ONNX inference."""
        import numpy as np
        
        # Convert to numpy
        state_np = state.numpy() if hasattr(state, 'numpy') else state
        state_batch = np.expand_dims(state_np, axis=0).astype(np.float32)
        
        # Run inference
        outputs = self._model.run(None, {'board_state': state_batch})
        policy_logits = outputs[0][0]
        value = outputs[1][0][0]
        
        return policy_logits, value
    
    def _coreml_inference(self, state):
        """CoreML inference."""
        import numpy as np
        
        # Convert to numpy
        state_np = state.numpy() if hasattr(state, 'numpy') else state
        state_batch = np.expand_dims(state_np, axis=0).astype(np.float32)
        
        # Run inference
        prediction = self._model.predict({'board_state': state_batch})
        policy_logits = prediction['policy_logits']
        value = prediction['value'][0]
        
        return policy_logits, value
    
    def get_move(self, game: BitboardGame, legal_moves: List[Move]) -> Optional[Move]:
        """
        Get move using RL model.
        
        Args:
            game: Current game state
            legal_moves: List of legal moves
            
        Returns:
            Selected move or None
        """
        if not legal_moves:
            return None
        
        # Lazy load model
        if self._model is None:
            self._load_model()
        
        # Get current player color
        player_color = game.turn
        
        # Encode state
        state = self._encode_state(game, player_color)
        
        # Get policy and value
        policy_logits, value = self._inference_fn(state)
        
        # Convert policy to probabilities
        import numpy as np
        policy_probs = np.exp(policy_logits) / np.sum(np.exp(policy_logits))
        
        # Filter to legal moves only
        legal_probs = {}
        for move in legal_moves:
            row = move.get_y() - 1
            col = move.get_x() - 1
            idx = row * 8 + col
            legal_probs[move] = policy_probs[idx]
        
        # Normalize
        total_prob = sum(legal_probs.values())
        if total_prob > 0:
            legal_probs = {move: prob / total_prob for move, prob in legal_probs.items()}
        else:
            # Fallback to uniform
            legal_probs = {move: 1.0 / len(legal_moves) for move in legal_moves}
        
        # Sample move
        moves = list(legal_probs.keys())
        probs = list(legal_probs.values())
        
        if self.temperature == 0.0:
            # Deterministic: choose best move
            best_move = max(legal_probs.items(), key=lambda x: x[1])[0]
            return best_move
        else:
            # Sample with temperature
            probs = np.array(probs) ** (1.0 / self.temperature)
            probs = probs / probs.sum()
            selected_move = np.random.choice(len(moves), p=probs)
            return moves[selected_move]

