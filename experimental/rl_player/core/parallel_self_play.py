"""
Parallel Self-Play Module

Implements parallel game generation using multiprocessing.
Optimized for macOS/Apple Silicon (M1/M2/M3) using 'spawn' start method.
"""

import os
import torch
import torch.multiprocessing as mp
import time
import queue
from typing import List, Tuple, Optional, Dict
import logging

from Reversi.BitboardGame import BitboardGame
from ..core.mcts import MCTS
from ..core.neural_network import NeuralNetwork
from ..core.self_play import SelfPlay

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def worker_play_game(
    rank: int, 
    model_config: Dict, 
    model_state_dict: Dict, 
    mcts_config: Dict, 
    temperature: float,
    use_symmetries: bool,
    device_str: str,
    result_queue: mp.Queue,
    num_games: int,
    max_moves: int,
    opening_book: Optional[object]
):
    """
    Worker process function to play games.
    
    Args:
        rank: Worker ID
        model_config: Config to create model
        model_state_dict: Weights to load
        mcts_config: Config for MCTS
        temperature: Exploration temperature
        use_symmetries: Whether to use data augmentation
        device_str: Device to use ('cpu' or 'mps')
        result_queue: Queue to send results back
        num_games: Number of games this worker should play
        max_moves: Maximum moves per game (safety limit)
        opening_book: Pre-loaded opening book
    """
    # Set random seed for this worker to ensure diversity
    torch.manual_seed(rank + int(time.time()))
    import numpy as np
    np.random.seed(rank + int(time.time()))
    
    try:
        # Create model instance for this worker
        # On MPS, each process needs its own context or use CPU
        device = torch.device(device_str)
        
        # Create model wrapper
        from ..models.resnet import create_resnet_model
        model = create_resnet_model(**model_config)
        model.load_state_dict(model_state_dict)
        model.to(device)
        model.eval()
        
        nn_wrapper = NeuralNetwork(model=model, device=device)
        
        # Create MCTS
        mcts = MCTS(
            neural_network=nn_wrapper,
            c_puct=mcts_config.get('c_puct', 1.0),
            num_simulations=mcts_config.get('simulations', 800),
            dirichlet_alpha=mcts_config.get('dirichlet_alpha', 0.3),
            dirichlet_epsilon=mcts_config.get('dirichlet_epsilon', 0.25),
            opening_book=opening_book
        )
        
        # Create SelfPlay
        self_play = SelfPlay(
            neural_network=nn_wrapper,
            mcts=mcts,
            temperature=temperature,
            use_symmetries=use_symmetries,
            opening_book=opening_book,
            max_moves=max_moves
        )
        
        # Play assigned games
        for i in range(num_games):
            # Define progress callback
            def progress_callback(moves):
                # Send progress update (non-blocking best effort)
                try:
                    result_queue.put_nowait(('progress', 1))
                except:
                    pass

            # Play game
            game_data = self_play.play_game(
                verbose=False,
                progress_callback=progress_callback
            )
            
            # Send result
            result_queue.put(('data', game_data))
            
        result_queue.put(('done', None))
            
    except Exception as e:
        print(f"Worker {rank} failed: {e}")
        import traceback
        traceback.print_exc()
        # Send error
        result_queue.put(('error', str(e)))


class ParallelSelfPlay:
    """
    Parallel implementation of SelfPlay using multiprocessing.
    """
    
    def __init__(
        self,
        neural_network: NeuralNetwork,
        mcts_config: Dict,
        temperature: float = 1.0,
        num_workers: Optional[int] = None,
        use_mps_workers: bool = False,
        use_symmetries: bool = True,
        max_moves: int = 100
    ):
        """
        Initialize ParallelSelfPlay.
        
        Args:
            neural_network: Master neural network (weights will be copied)
            mcts_config: Configuration for MCTS
            temperature: Temperature for self-play
            num_workers: Number of worker processes (None = auto-detect CPU cores)
            use_mps_workers: Whether to use MPS (GPU) in workers.
            use_symmetries: Whether to use data augmentation (D8 symmetries)
            max_moves: Maximum moves per game
        """
        self.master_network = neural_network
        self.mcts_config = mcts_config
        self.temperature = temperature
        self.use_symmetries = use_symmetries
        self.max_moves = max_moves
        
        # Load opening book ONCE in master process
        from ..utils.state_encoder import get_opening_book
        print("Master: Loading opening book...")
        self.opening_book = get_opening_book()
        print("Master: Opening book loaded.")
        
        # Auto-detect workers
        if num_workers is None:
            # Leave one core free for OS/main process
            self.num_workers = max(1, os.cpu_count() - 1)
        else:
            self.num_workers = num_workers
            
        self.use_mps_workers = use_mps_workers
        
        logger.info(f"Initialized ParallelSelfPlay with {self.num_workers} workers")
        
    def generate_games(
        self,
        num_games: int,
        verbose: bool = True,
        progress_bar: bool = True
    ) -> List[Tuple]:
        """
        Generate games in parallel.
        
        Args:
            num_games: Total number of games to generate
            verbose: Whether to print progress
            progress_bar: Whether to use tqdm
            
        Returns:
            List of training data tuples
        """
        start_time = time.time()
        
        # Prepare model data for workers
        # We pass config and state_dict to avoid pickling complex objects
        model_config = {
            'input_channels': self.master_network.model.input_channels,
            'num_residual_blocks': self.master_network.model.num_residual_blocks,
            'channels': self.master_network.model.channels
        }
        
        model_state_dict = self.master_network.model.state_dict()
        # Ensure state dict is on CPU for pickling
        model_state_dict = {k: v.cpu() for k, v in model_state_dict.items()}
        
        # Determine device for workers
        # On macOS M1, it's often faster/stabler to run parallel inference on CPU 
        # unless we use a specialized batched inference engine.
        worker_device = "mps" if self.use_mps_workers and torch.backends.mps.is_available() else "cpu"
        
        # Distribute games among workers
        games_per_worker = [num_games // self.num_workers] * self.num_workers
        # Distribute remainder
        for i in range(num_games % self.num_workers):
            games_per_worker[i] += 1
            
        # Remove workers with 0 games
        active_workers = [(i, count) for i, count in enumerate(games_per_worker) if count > 0]
        
        if verbose:
            print(f"Starting {len(active_workers)} workers for {num_games} games...")
            print(f"Worker device: {worker_device}")
            print(f"Symmetries enabled: {self.use_symmetries}")
        
        # Queue for results
        ctx = mp.get_context('spawn')
        result_queue = ctx.Queue()
        
        # Start processes
        processes = []
        for rank, count in active_workers:
            p = ctx.Process(
                target=worker_play_game,
                args=(
                    rank,
                    model_config,
                    model_state_dict,
                    self.mcts_config,
                    self.temperature,
                    self.use_symmetries,
                    worker_device,
                    result_queue,
                    count,
                    self.max_moves,  # Max moves
                    self.opening_book  # Pass the loaded book
                )
            )
            p.start()
            processes.append(p)
            
        # Collect results
        all_training_data = []
        completed_games = 0
        
        # Setup progress bar
        pbar = None
        move_pbar = None
        if progress_bar:
            from tqdm import tqdm
            pbar = tqdm(total=num_games, desc="Parallel Games", unit="game", position=0)
            # Add a secondary progress bar for total moves (rough estimate: 60 moves * num_games)
            move_pbar = tqdm(total=num_games * 60, desc="Total Moves", unit="move", position=1, leave=False)
        
        # Monitor Loop
        active_count = len(processes)
        while active_count > 0:
            # Drain queue aggressively to keep UI responsive
            try:
                # First check with timeout to wait for data (avoid busy loop)
                # But once we have data, keep reading until empty
                has_data = True
                first_msg = True
                
                while has_data:
                    try:
                        timeout = 1.0 if first_msg else 0.001
                        msg = result_queue.get(timeout=timeout)
                        first_msg = False
                        
                        # Unwrap message: (type, data)
                        if isinstance(msg, tuple) and len(msg) == 2:
                            m_type, data = msg
                            
                            if m_type == 'data':
                                # 'data' is a list of training samples from one game
                                all_training_data.extend(data)
                                completed_games += 1
                                if pbar:
                                    pbar.update(1)
                                    
                            elif m_type == 'progress':
                                if move_pbar:
                                    move_pbar.update(1) # Report every move
                                    
                            elif m_type == 'error':
                                logger.error(f"Worker error: {data}")
                                
                            elif m_type == 'done':
                                active_count -= 1
                    except queue.Empty:
                        has_data = False
                        
            except KeyboardInterrupt:
                # Handle interrupt in main loop
                break
            # Check if processes are still alive
            alive_count = sum(1 for p in processes if p.is_alive())
            if alive_count == 0 and result_queue.empty():
                break
                    
        # Join processes
        for p in processes:
            p.join()
            
        if pbar:
            pbar.close()
        if move_pbar:
            move_pbar.close()
            
        total_time = time.time() - start_time
        if verbose:
            print(f"Generated {completed_games} games in {total_time:.1f}s")
            print(f"Throughput: {completed_games / total_time * 60:.2f} games/min")
            
        return all_training_data
