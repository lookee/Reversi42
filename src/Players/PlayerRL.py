"""
Neural Prime - Deep Reinforcement Learning Player

Neural network player trained via Reinforcement Learning (AlphaZero-style).
Uses a deep neural network that learns by playing against itself.
Can use MCTS for stronger play or direct policy for faster play.

Design: Adapter pattern - wraps experimental RL player for main system.
"""

import os
import sys
from typing import List, Optional
from pathlib import Path

from Players.Player import Player
from Reversi.Game import Move
from Reversi.BitboardGame import BitboardGame


class PlayerRL(Player):
    """
    Neural Prime - Deep Reinforcement Learning Player.
    
    Neural network trained via self-play reinforcement learning.
    Uses latest.pth checkpoint by default.
    Can use MCTS for stronger play or direct policy for faster play.
    """
    
    PLAYER_METADATA = {
        "display_name": "Neural Prime",
        "description": "Deep Reinforcement Learning player - Neural network trained via self-play reinforcement learning",
        "enabled": True,
        "parameters": {
            "model_path": {
                "type": str,
                "default": "config/neuralnetwork/latest_onnx.onnx",
                "description": "Path to model (.onnx recommended - lightweight, no PyTorch needed, or .pth/.pt for PyTorch)"
            },
            "use_mcts": {
                "type": bool,
                "default": True,
                "description": "Use MCTS for move selection (stronger but slower)"
            },
            "mcts_simulations": {
                "type": int,
                "default": 400,
                "min": 100,
                "max": 2000,
                "description": "Number of MCTS simulations (only if use_mcts=True)"
            },
            "temperature": {
                "type": float,
                "default": 0.1,
                "min": 0.0,
                "max": 1.0,
                "description": "Sampling temperature (0=deterministic, higher=more random)"
            }
        }
    }
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        use_mcts: bool = True,
        mcts_simulations: int = 400,
        temperature: float = 0.1,
        name: str = "Neural Prime"
    ):
        """
        Initialize RL player.
        
        Args:
            model_path: Path to model checkpoint (default: latest.pth)
            use_mcts: Whether to use MCTS (True) or direct policy (False)
            mcts_simulations: Number of MCTS simulations if use_mcts=True
            temperature: Sampling temperature for move selection
            name: Player name
        """
        super().__init__()
        self.name = name
        self.use_mcts = use_mcts
        self.mcts_simulations = mcts_simulations
        self.temperature = temperature
        
        # Initialize opening book
        from domain.knowledge.opening_book import OpeningBook
        project_root = Path(__file__).parent.parent.parent
        book_dir = project_root / "src" / "domain" / "knowledge" / "data"
        
        # Load opening books (same as Apocalyptron)
        self.opening_book = OpeningBook()
        book_files = [
            book_dir / "00_opening_ffo.txt",
            book_dir / "01_opening_pointystone.txt"
        ]
        for book_file in book_files:
            if book_file.exists():
                self.opening_book.load_additional_book(str(book_file))
        
        # Find model path (prefer ONNX for lightweight inference)
        if model_path is None:
            project_root = Path(__file__).parent.parent.parent
            checkpoints_dir = project_root / "experimental" / "checkpoints"
            exported_dir = checkpoints_dir / "exported"
            
            # Try ONNX first (lightweight)
            onnx_path = exported_dir / "latest_onnx.onnx"
            if onnx_path.exists():
                model_path = onnx_path
            else:
                # Fallback to PyTorch
                model_path = checkpoints_dir / "latest.pth"
                if not model_path.exists():
                    # Try best.pth
                    model_path = checkpoints_dir / "best.pth"
        
        self.model_path = str(model_path)
        
        # Lazy load - only import when needed
        self._neural_network = None
        self._mcts = None
        self._model_loaded = False
        self._model_type = None  # "pytorch", "onnx", "torchscript"
        self._onnx_session = None
        self._torchscript_model = None
        self._model_type = None  # "pytorch", "onnx", "torchscript"
        self._onnx_session = None
        self._torchscript_model = None
    
    def _load_model(self):
        """Lazy load model and dependencies - supports lightweight formats."""
        if self._model_loaded:
            return
        
        # Add experimental to path
        project_root = Path(__file__).parent.parent.parent
        experimental_dir = project_root / "experimental"
        src_dir = project_root / "src"
        
        if str(experimental_dir) not in sys.path:
            sys.path.insert(0, str(experimental_dir))
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))
        
        # Resolve model path relative to project root
        model_path = Path(self.model_path)
        if not model_path.is_absolute():
            model_path = project_root / model_path
        model_path = model_path.resolve()
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path} (resolved to: {model_path})")
        
        # Detect model format from extension
        model_ext = model_path.suffix.lower()
        
        # Try lightweight formats first (ONNX, TorchScript)
        if model_ext == ".onnx":
            self._load_onnx_model()
            return
        elif model_ext == ".pt":
            self._load_torchscript_model()
            return
        
        # Fallback to PyTorch (.pth) - requires full PyTorch
        try:
            from experimental.rl_player.core.neural_network import NeuralNetwork
            import torch
            
            # Detect device
            if torch.backends.mps.is_available():
                device = torch.device('mps')
            elif torch.cuda.is_available():
                device = torch.device('cuda')
            else:
                device = torch.device('cpu')
            
            # Load PyTorch model
            self._neural_network = NeuralNetwork.load(self.model_path, device=device)
            self._model_loaded = True
            
            # Load MCTS if needed
            if self.use_mcts:
                from experimental.rl_player.core.mcts import MCTS
                self._mcts = MCTS(
                    neural_network=self._neural_network,
                    num_simulations=self.mcts_simulations,
                    c_puct=1.0,
                    dirichlet_alpha=0.3,
                    dirichlet_epsilon=0.25
                )
            
        except ImportError as e:
            raise ImportError(
                f"PyTorch not installed. For lightweight inference, export model to ONNX:\n"
                f"  python experimental/rl_player/utils/export_model.py --model-path {self.model_path} --format onnx\n"
                f"Or install PyTorch: pip install torch>=2.0.0"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Failed to load RL model from {self.model_path}: {e}") from e
    
    def _load_onnx_model(self):
        """Load ONNX model (lightweight - only needs onnxruntime)."""
        try:
            import onnxruntime as ort
            import numpy as np
            
            # Create inference session
            providers = ['CPUExecutionProvider']
            if ort.get_device() == 'GPU':
                providers.insert(0, 'CUDAExecutionProvider')
            
            self._onnx_session = ort.InferenceSession(str(self.model_path), providers=providers)
            self._model_loaded = True
            self._model_type = "onnx"
            
            print(f"✓ Loaded ONNX model (lightweight - no PyTorch required)")
            
        except ImportError:
            raise ImportError(
                "ONNX model requires onnxruntime (lightweight). Install with: "
                "pip install onnxruntime"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load ONNX model: {e}") from e
    
    def _load_torchscript_model(self):
        """Load TorchScript model (lighter than full PyTorch)."""
        try:
            import torch
            
            device = torch.device("cpu")  # TorchScript typically on CPU
            if torch.backends.mps.is_available():
                device = torch.device("mps")
            elif torch.cuda.is_available():
                device = torch.device("cuda")
            
            self._torchscript_model = torch.jit.load(str(self.model_path), map_location=device)
            self._torchscript_model.eval()
            self._model_loaded = True
            self._model_type = "torchscript"
            
            print(f"✓ Loaded TorchScript model (lighter than full PyTorch)")
            
        except ImportError:
            raise ImportError(
                "TorchScript model requires torch. Install with: pip install torch>=2.0.0"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load TorchScript model: {e}") from e
    
    def _get_game_history(self, game: BitboardGame) -> str:
        """
        Get game history as move string for opening book lookup.
        
        Args:
            game: Current game state
            
        Returns:
            String of moves (e.g., "F5d6C3")
        """
        # BitboardGame stores history as a string attribute
        if hasattr(game, 'history') and game.history:
            return game.history
        
        # Fallback: try to reconstruct from move_history if available
        if hasattr(game, 'move_history') and game.move_history:
            history = []
            for move in game.move_history:
                if hasattr(move, 'get_x') and hasattr(move, 'get_y'):
                    col = chr(ord('A') + move.get_x() - 1)
                    row = str(move.get_y())
                    # Black moves are uppercase, white moves are lowercase
                    move_str = col + row
                    # Determine if it's black or white based on turn count
                    # For now, alternate case (first move is black = uppercase)
                    if len(history) % 2 == 0:
                        history.append(move_str.upper())
                    else:
                        history.append(move_str.lower())
            return ''.join(history)
        
        return ""
    
    def get_move(self, game: BitboardGame, move_list: List[Move], control=None) -> Optional[Move]:
        """
        Get next move using RL model.
        
        Strategy priority:
        1. Opening book (if available)
        2. RL model (MCTS or direct policy)
        
        Args:
            game: Current game state
            move_list: List of legal moves
            control: (Optional) Control object (not used)
            
        Returns:
            Selected move or None if no legal moves
        """
        if not move_list:
            return None
        
        # Get current player (needed for opening book and later)
        current_player = game.turn
        
        # Get game history for opening book
        game_history = self._get_game_history(game)
        
        # Try opening book first (always check)
        book_moves = self.opening_book.get_book_moves(game_history)
        
        if book_moves:
            # Filter to valid moves only
            valid_book_moves = [m for m in book_moves if m in move_list]
            
            if valid_book_moves:
                # Use opening book move
                selected_move = valid_book_moves[0]
                
                # Send opening book move information if observer available
                observer = control
                has_observer = observer is not None and hasattr(observer, '_send_async')
                
                if has_observer:
                    # Get opening name and advantage if available
                    opening_name = self.opening_book.get_current_opening_name(game_history)
                    advantage = self.opening_book.get_opening_advantage(game_history)
                    
                    # Test history after this move
                    move_str = str(selected_move).upper()
                    test_history = game_history + move_str if current_player == "B" else game_history + move_str.lower()
                    next_opening = self.opening_book.get_current_opening_name(test_history)
                    
                    coord = f"{chr(64+selected_move.x)}{selected_move.y}"
                    
                    observer._send_async({
                        "type": "ai_move",
                        "data": {
                            "move": coord,
                            "evaluation": 0,  # Opening book moves don't have evaluation
                            "depth": "Opening Book",
                            "nodes_searched": 0,
                            "nodes_pruned": 0,
                            "opening_book": True,
                            "opening_name": opening_name or next_opening or "Book",
                            "opening_advantage": advantage or "=",
                            "method": "Opening Book",
                        },
                    })
                
                return selected_move
        
        # Load model if not already loaded
        self._load_model()
        
        # Check if we have an observer for sending statistics
        observer = control
        has_observer = observer is not None and hasattr(observer, '_send_async')
        
        # Debug: log observer status
        if observer is None:
            print("⚠️  PlayerRL: No observer provided (control is None)")
        elif not hasattr(observer, '_send_async'):
            print(f"⚠️  PlayerRL: Observer provided but missing _send_async method. Type: {type(observer)}")
        else:
            print(f"✓ PlayerRL: Observer available, will send statistics")
        
        try:
            if self.use_mcts and self._mcts:
                # Send initial thinking message
                if has_observer:
                    import time
                    search_start_time = time.time()
                    
                    observer._send_async({
                        "type": "ai_thinking",
                        "data": {
                            "status": f"MCTS search ({self.mcts_simulations} simulations)...",
                            "depth": f"MCTS",
                            "nodes_searched": 0,
                            "nodes_pruned": 0,
                        },
                    })
                
                # Use MCTS for stronger play
                root = self._mcts.search(game, current_player, add_noise=False)
                
                # Get best move from MCTS
                if root.children:
                    # Get visit distribution
                    visit_dist = root.get_visit_distribution(temperature=self.temperature)
                    if visit_dist:
                        # Select move based on visit distribution
                        moves = list(visit_dist.keys())
                        probs = list(visit_dist.values())
                        
                        import numpy as np
                        selected_move = moves[np.random.choice(len(moves), p=probs)]
                        
                        # Calculate statistics for display
                        if has_observer:
                            import time
                            search_time = time.time() - search_start_time
                            
                            # Get visit counts and value for selected move
                            selected_node = root.children.get(selected_move)
                            visit_count = selected_node.visit_count if selected_node else 0
                            
                            # Get average value from selected node (value_sum / visit_count)
                            if selected_node and selected_node.visit_count > 0:
                                value = selected_node.get_value()
                            else:
                                value = root.get_value() if root.visit_count > 0 else 0.0
                            
                            # Calculate total visits (sum of all children)
                            total_visits = sum(child.visit_count for child in root.children.values())
                            
                            # Get root value for position evaluation
                            root_value = root.get_value() if root.visit_count > 0 else 0.0
                            
                            # Calculate nodes per second
                            nps = int(total_visits / search_time) if search_time > 0 else 0
                            
                            # Send final move message with statistics
                            coord = f"{chr(64+selected_move.x)}{selected_move.y}"
                            observer._send_async({
                                "type": "ai_move",
                                "data": {
                                    "move": coord,
                                    "evaluation": int(root_value * 100),  # Root position value in centipawns
                                    "depth": f"MCTS ({self.mcts_simulations} sim)",
                                    "depth_reached": self.mcts_simulations,  # Use simulations as depth equivalent
                                    "nodes_searched": total_visits,
                                    "nodes_pruned": 0,
                                    "mcts_simulations": self.mcts_simulations,
                                    "mcts_visits": visit_count,
                                    "mcts_value": float(value),
                                    "mcts_root_value": float(root_value),
                                    "search_time_ms": int(search_time * 1000),
                                    "nodes_per_second": nps,
                                    "method": "MCTS",
                                },
                            })
                        
                        return selected_move
                
                # Fallback: use first legal move
                return move_list[0]
            
            else:
                # Use direct policy (faster but weaker)
                # Send initial thinking message
                if has_observer:
                    import time
                    search_start_time = time.time()
                    
                    observer._send_async({
                        "type": "ai_thinking",
                        "data": {
                            "status": "Policy inference...",
                            "depth": "Direct Policy",
                            "nodes_searched": 0,
                            "nodes_pruned": 0,
                        },
                    })
                
                from experimental.rl_player.utils.state_encoder import encode_state
                import torch
                
                state = encode_state(
                    game,
                    current_player,
                    use_advanced_features=True,
                    use_opening_book=True,
                    device=self._neural_network.device if self._neural_network else torch.device('cpu')
                )
                
                # Get policy and value
                if self._model_type == "onnx":
                    import numpy as np
                    import onnxruntime as ort
                    
                    # ONNX inference
                    input_name = self._onnx_session.get_inputs()[0].name
                    outputs = self._onnx_session.run(None, {input_name: state.numpy()})
                    policy_logits = outputs[0]
                    value = outputs[1][0][0] if len(outputs) > 1 else 0.0
                    policy_probs = torch.softmax(torch.tensor(policy_logits[0]), dim=0).numpy()
                elif self._model_type == "torchscript":
                    with torch.no_grad():
                        outputs = self._torchscript_model(state.unsqueeze(0))
                        if isinstance(outputs, tuple):
                            policy_logits, value_output = outputs
                            value = value_output[0][0].item() if len(value_output.shape) > 1 else value_output[0].item()
                        else:
                            policy_logits = outputs
                            value = 0.0
                        policy_probs = torch.softmax(policy_logits[0], dim=0).cpu().numpy()
                else:
                    # PyTorch model
                    with torch.no_grad():
                        policy_logits, value_output = self._neural_network.forward(state.unsqueeze(0))
                        value = value_output[0][0].item() if len(value_output.shape) > 1 else value_output[0].item()
                        policy_probs = torch.softmax(policy_logits[0], dim=0).cpu().numpy()
                
                # Select move based on policy
                move_scores = []
                for move in move_list:
                    row = move.get_y() - 1
                    col = move.get_x() - 1
                    idx = row * 8 + col
                    move_scores.append((move, policy_probs[idx]))
                
                # Sort by probability
                move_scores.sort(key=lambda x: x[1], reverse=True)
                
                # Apply temperature
                if self.temperature > 0:
                    import numpy as np
                    probs = np.array([score[1] for score in move_scores])
                    probs = probs ** (1.0 / self.temperature)
                    probs = probs / probs.sum()
                    selected_idx = np.random.choice(len(move_scores), p=probs)
                    selected_move = move_scores[selected_idx][0]
                    selected_prob = move_scores[selected_idx][1]
                else:
                    # Deterministic: return best move
                    selected_move = move_scores[0][0]
                    selected_prob = move_scores[0][1]
                
                # Send final move message with statistics
                if has_observer:
                    import time
                    search_time = time.time() - search_start_time
                    
                    # Calculate nodes (nodes) per second (1 forward pass = 1 node)
                    nps = int(1 / search_time) if search_time > 0 else 0
                    
                    coord = f"{chr(64+selected_move.x)}{selected_move.y}"
                    observer._send_async({
                        "type": "ai_move",
                        "data": {
                            "move": coord,
                            "evaluation": int(value * 100),  # Convert to centipawns
                            "depth": "Direct Policy",
                            "depth_reached": 1,  # Single forward pass
                            "nodes_searched": 1,  # Single forward pass
                            "nodes_pruned": 0,
                            "policy_probability": float(selected_prob),
                            "policy_value": float(value),
                            "search_time_ms": int(search_time * 1000),
                            "nodes_per_second": nps,
                            "method": "Policy",
                        },
                    })
                
                return selected_move
        
        except Exception as e:
            # Fallback on error
            print(f"Warning: RL player error: {e}")
            return move_list[0] if move_list else None

