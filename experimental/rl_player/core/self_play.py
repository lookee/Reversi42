"""
Self-Play Module

Plays games against itself to generate training data.
"""

import torch
import numpy as np
import copy
import time
from typing import List, Tuple, Optional
from tqdm import tqdm

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move
from ..core.mcts import MCTS
from ..core.neural_network import NeuralNetwork
from ..utils.state_encoder import encode_state
from ..data.replay_buffer import ReplayBuffer


class SelfPlay:
    """
    Self-play engine that generates training data.
    """
    
    def __init__(
        self,
        neural_network: NeuralNetwork,
        mcts: MCTS,
        temperature: float = 1.0,
        use_symmetries: bool = True,
        opening_book: Optional[object] = None,
        max_moves: int = 100
    ):
        """
        Initialize self-play engine.
        
        Args:
            neural_network: Neural network to use for play
            mcts: MCTS instance
            temperature: Temperature for move selection during self-play
            use_symmetries: Whether to use data augmentation (D8 symmetries)
            opening_book: Optional opening book instance
            max_moves: Maximum moves per game (safety limit)
        """
        self.neural_network = neural_network
        self.mcts = mcts
        self.temperature = temperature
        self.temperature = temperature
        self.use_symmetries = use_symmetries
        self.opening_book = opening_book
        self.max_moves = max_moves

    def generate_symmetries(self, state: torch.Tensor, policy: torch.Tensor, value: float) -> List[Tuple]:
        """
        Generate D8 symmetries (rotations + flips) for a training sample.
        
        Args:
            state: Tensor [channels, 8, 8]
            policy: Tensor [65] (64 positions + pass)
            value: Float value
            
        Returns:
            List of (state, policy, value) tuples
        """
        symmetries = []
        
        # Reshape policy (exclude pass move at index 64)
        policy_board = policy[:64].view(8, 8)
        policy_pass = policy[64]
        
        # 1. Original
        symmetries.append((state, policy, value))
        
        # 2. Rotations (90, 180, 270)
        for k in [1, 2, 3]:
            rot_state = torch.rot90(state, k, [1, 2])
            rot_policy_board = torch.rot90(policy_board, k, [0, 1])
            
            # Flatten and append pass
            rot_policy = torch.cat([rot_policy_board.flatten(), policy_pass.unsqueeze(0)])
            symmetries.append((rot_state, rot_policy, value))
            
        # 3. Horizontal Flip
        flip_state = torch.flip(state, [2])
        flip_policy_board = torch.flip(policy_board, [1])
        flip_policy = torch.cat([flip_policy_board.flatten(), policy_pass.unsqueeze(0)])
        symmetries.append((flip_state, flip_policy, value))
        
        # 4. Flip + Rotations
        for k in [1, 2, 3]:
            rot_flip_state = torch.rot90(flip_state, k, [1, 2])
            rot_flip_policy_board = torch.rot90(flip_policy_board, k, [0, 1])
            
            rot_flip_policy = torch.cat([rot_flip_policy_board.flatten(), policy_pass.unsqueeze(0)])
            symmetries.append((rot_flip_state, rot_flip_policy, value))
            
        return symmetries

    def play_game(self, verbose: bool = False, progress_callback: Optional[callable] = None) -> List[Tuple]:
        """
        Play a single game and return training data.
        
        Args:
            verbose: Whether to print game progress
            progress_callback: Optional callback(move_count) called during game
            
        Returns:
            List of (state, policy, value) tuples for training
        """
        game = BitboardGame()
        training_data = []
        move_history = []
        
        current_player = "B"
        move_count = 0
        
        max_moves = self.max_moves  # Use configured limit
        start_time = time.time()
        
        while move_count < max_moves and not game.is_finish():
            # Progress callback (every move for better feedback)
            if progress_callback:
                progress_callback(move_count)

            legal_moves = game.get_move_list()
            
            if len(legal_moves) == 0:
                # No legal moves - pass turn
                if verbose:
                    print(f"Move {move_count}: {current_player} passes")
                game.pass_turn()
                current_player = game.turn
                move_count += 1
                continue
            
            # Perform MCTS search (this can take time - 800 simulations per move)
            move_start_time = time.time()
            if verbose:
                print(f"\nMove {move_count + 1}: {current_player} thinking... (MCTS: {self.mcts.num_simulations} simulations)")
            
            root = self.mcts.search(game, current_player, add_noise=True, verbose=verbose)
            
            move_time = time.time() - move_start_time
            if verbose:
                print(f"  ✓ Move {move_count + 1} completed in {move_time:.1f}s")
            
            # Get visit distribution
            visit_dist = root.get_visit_distribution(temperature=self.temperature)
            
            # Select move
            if visit_dist:
                moves = list(visit_dist.keys())
                probs = list(visit_dist.values())
                selected_move = moves[np.random.choice(len(moves), p=probs)]
            else:
                # Fallback to random move
                selected_move = legal_moves[0]
            
            # Encode state from current player's perspective
            state = encode_state(
                game,
                current_player,
                use_advanced_features=True,
                use_opening_book=True,
                device=self.neural_network.device
            )
            
            # Convert visit distribution to policy array (65 elements: 64 positions + pass)
            policy_array = torch.zeros(65)
            for move, prob in visit_dist.items():
                row = move.get_y() - 1
                col = move.get_x() - 1
                idx = row * 8 + col
                policy_array[idx] = prob
            
            # Store training data (value will be set at end of game)
            # IMPORTANT: Clone state to avoid issues if game mutates (though encode_state returns new tensor)
            # Move to CPU to save GPU memory during game
            training_data.append((state.cpu(), policy_array.cpu(), None))
            move_history.append((current_player, selected_move))
            
            # Make move
            game.move(selected_move)
            current_player = game.turn
            move_count += 1
            
            # Show board state every 10 moves
            if verbose and move_count % 10 == 0:
                black_count = bin(game.black).count('1')
                white_count = bin(game.white).count('1')
                print(f"  Board state: Black={black_count}, White={white_count}, Moves={move_count}")
        
        # Assign final values based on game outcome
        black_count = bin(game.black).count('1')
        white_count = bin(game.white).count('1')
        total_time = time.time() - start_time
        
        if black_count > white_count:
            final_value_black = 1.0
            final_value_white = -1.0
            winner = "Black"
        elif white_count > black_count:
            final_value_black = -1.0
            final_value_white = 1.0
            winner = "White"
        else:
            final_value_black = 0.0
            final_value_white = 0.0
            winner = "Draw"
        
        if verbose:
            print(f"\n🏁 Game finished!")
            print(f"  Winner: {winner} (Black: {black_count}, White: {white_count})")
            print(f"  Total moves: {move_count}")
            print(f"  Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
            print(f"  Training positions: {len(training_data)}")
        
        # Assign values and apply symmetries
        result_data = []
        for i, (state, policy, _) in enumerate(training_data):
            player_color = move_history[i][0]
            value = final_value_black if player_color == "B" else final_value_white
            
            if self.use_symmetries:
                # Generate 8 symmetries
                sym_samples = self.generate_symmetries(state, policy, value)
                result_data.extend(sym_samples)
            else:
                result_data.append((state, policy, value))
        
        if verbose and self.use_symmetries:
             print(f"  Augmented positions: {len(result_data)} (x8 symmetries)")

        return result_data
    
    def generate_games(
        self,
        num_games: int,
        verbose: bool = False,
        progress_bar: bool = True
    ) -> List[Tuple]:
        """
        Generate multiple games.
        
        Args:
            num_games: Number of games to play
            verbose: Whether to print game details
            progress_bar: Whether to show progress bar
            
        Returns:
            List of all training samples from all games
        """
        all_training_data = []
        
        iterator = range(num_games)
        if progress_bar:
            iterator = tqdm(iterator, desc="Self-play games", unit="game")
        
        for game_idx in iterator:
            game_start_time = time.time()
            
            if game_idx == 0:
                print(f"\n{'='*70}")
                print(f"🎮 Starting game {game_idx + 1}/{num_games}")
                print(f"{'='*70}")
                print(f"MCTS simulations per move: {self.mcts.num_simulations}")
                print(f"Estimated time per game: ~5-10 minutes")
                print(f"{'='*70}\n")
            else:
                print(f"\n🎮 Starting game {game_idx + 1}/{num_games}...")
            
            game_data = self.play_game(verbose=True)  # Always verbose for progress
            all_training_data.extend(game_data)
            
            game_time = time.time() - game_start_time
            print(f"\n✓ Game {game_idx + 1} completed in {game_time/60:.1f} minutes")
            print(f"  Positions collected: {len(game_data)}")
            print(f"  Total positions so far: {len(all_training_data)}")
            
            # Update progress bar if available
            if progress_bar and hasattr(iterator, 'set_description'):
                iterator.set_description(f"Games: {game_idx + 1}/{num_games}, Positions: {len(all_training_data)}")
        
        return all_training_data

