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
from ..utils.reward_shaping import calculate_intermediate_reward, calculate_position_value
from ..utils.game_transform import apply_symmetry_transform, get_symmetry_transforms
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
        use_reward_shaping: bool = True,
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
            use_reward_shaping: Whether to use intermediate rewards (corners, bad squares, mobility, stability)
            opening_book: Optional opening book instance
            max_moves: Maximum moves per game (safety limit)
        """
        self.neural_network = neural_network
        self.mcts = mcts
        self.temperature = temperature
        self.temperature = temperature
        self.use_symmetries = use_symmetries
        self.use_reward_shaping = use_reward_shaping
        self.opening_book = opening_book
        self.max_moves = max_moves

    def generate_symmetries(
        self, 
        state: torch.Tensor, 
        policy: torch.Tensor, 
        value: float,
        game_state_before: Optional[BitboardGame] = None,
        game_state_after: Optional[BitboardGame] = None,
        player_color: Optional[str] = None,
        final_outcome: Optional[float] = None,
        intermediate_rewards: Optional[List[float]] = None,
        move_index: Optional[int] = None
    ) -> List[Tuple]:
        """
        Generate D8 symmetries (rotations + flips) for a training sample.
        
        If reward shaping is enabled and game_state is provided, recalculates rewards
        for each symmetry to ensure correct learning.
        
        Args:
            state: Tensor [channels, 8, 8]
            policy: Tensor [65] (64 positions + pass)
            value: Float value (original, will be recalculated for symmetries if game_state provided)
            game_state: Optional BitboardGame state (for reward recalculation)
            player_color: Optional player color "B" or "W"
            final_outcome: Optional final game outcome
            intermediate_rewards: Optional list of intermediate rewards
            move_index: Optional move index for reward calculation
            
        Returns:
            List of (state, policy, value) tuples
        """
        symmetries = []
        
        # Reshape policy (exclude pass move at index 64)
        policy_board = policy[:64].view(8, 8)
        policy_pass = policy[64]
        
        # Define symmetry transformations (matching the order in generate_symmetries)
        transforms = [
            'identity',      # 0: Original
            'rot90',         # 1: Rotate 90
            'rot180',        # 2: Rotate 180
            'rot270',        # 3: Rotate 270
            'flip_h',        # 4: Horizontal flip
            'flip_h_rot90',  # 5: Flip then rotate 90
            'flip_h_rot180', # 6: Flip then rotate 180
            'flip_h_rot270', # 7: Flip then rotate 270
        ]
        
        # Apply each transformation
        for transform_type in transforms:
            if transform_type == 'identity':
                transformed_state = state
                transformed_policy_board = policy_board
            elif transform_type == 'rot90':
                transformed_state = torch.rot90(state, 1, [1, 2])
                transformed_policy_board = torch.rot90(policy_board, 1, [0, 1])
            elif transform_type == 'rot180':
                transformed_state = torch.rot90(state, 2, [1, 2])
                transformed_policy_board = torch.rot90(policy_board, 2, [0, 1])
            elif transform_type == 'rot270':
                transformed_state = torch.rot90(state, 3, [1, 2])
                transformed_policy_board = torch.rot90(policy_board, 3, [0, 1])
            elif transform_type == 'flip_h':
                transformed_state = torch.flip(state, [2])
                transformed_policy_board = torch.flip(policy_board, [1])
            elif transform_type == 'flip_h_rot90':
                flip_state = torch.flip(state, [2])
                flip_policy_board = torch.flip(policy_board, [1])
                transformed_state = torch.rot90(flip_state, 1, [1, 2])
                transformed_policy_board = torch.rot90(flip_policy_board, 1, [0, 1])
            elif transform_type == 'flip_h_rot180':
                flip_state = torch.flip(state, [2])
                flip_policy_board = torch.flip(policy_board, [1])
                transformed_state = torch.rot90(flip_state, 2, [1, 2])
                transformed_policy_board = torch.rot90(flip_policy_board, 2, [0, 1])
            elif transform_type == 'flip_h_rot270':
                flip_state = torch.flip(state, [2])
                flip_policy_board = torch.flip(policy_board, [1])
                transformed_state = torch.rot90(flip_state, 3, [1, 2])
                transformed_policy_board = torch.rot90(flip_policy_board, 3, [0, 1])
            
            # Flatten policy and append pass
            transformed_policy = torch.cat([transformed_policy_board.flatten(), policy_pass.unsqueeze(0)])
            
            # Calculate value for this symmetry
            if (self.use_reward_shaping and game_state_before is not None and 
                game_state_after is not None and player_color is not None and 
                final_outcome is not None and intermediate_rewards is not None and 
                move_index is not None):
                # Transform game states
                transformed_game_before = apply_symmetry_transform(game_state_before, transform_type)
                transformed_game_after = apply_symmetry_transform(game_state_after, transform_type)
                
                # Recalculate intermediate reward for transformed state
                transformed_reward = calculate_intermediate_reward(
                    transformed_game_after,
                    player_color,
                    transformed_game_before,
                    player_color
                )
                
                # For future rewards, we approximate by using original rewards
                # (full recalculation would require transforming entire game history)
                # This is a reasonable approximation since the relative value of positions
                # should be similar after transformation
                transformed_intermediate_rewards = [transformed_reward]
                if move_index + 1 < len(intermediate_rewards):
                    # Use original rewards for future moves (approximation)
                    transformed_intermediate_rewards.extend(intermediate_rewards[move_index + 1:])
                
                # Calculate value with transformed rewards
                transformed_value = calculate_position_value(
                    transformed_game_after,
                    player_color,
                    final_outcome,
                    transformed_intermediate_rewards,
                    0  # Start from beginning of transformed rewards
                )
            else:
                # No reward shaping or missing data - use original value
                transformed_value = value
            
            symmetries.append((transformed_state, transformed_policy, transformed_value))
        
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
        game_states_before = []  # Store game state BEFORE each move (for reward recalculation on symmetries)
        game_states_after = []  # Store game state AFTER each move (for reward recalculation on symmetries)
        intermediate_rewards = []  # Track intermediate rewards for reward shaping
        previous_game_state = None  # Track previous state for reward calculation
        previous_player_color = None
        
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
            
            # Store game state BEFORE move (for reward recalculation on symmetries)
            if self.use_reward_shaping:
                game_states_before.append(copy.deepcopy(game))
            
            # Store previous state BEFORE making the move (for reward calculation)
            previous_game_state = copy.deepcopy(game) if self.use_reward_shaping else None
            previous_player_color = current_player if self.use_reward_shaping else None
            
            # Make move
            game.move(selected_move)
            
            # Store game state AFTER move (for reward recalculation on symmetries)
            if self.use_reward_shaping:
                game_states_after.append(copy.deepcopy(game))
            
            # Calculate intermediate reward AFTER the move
            if self.use_reward_shaping and previous_game_state is not None:
                intermediate_reward = calculate_intermediate_reward(
                    game,  # Current state after move
                    current_player,  # Player who just moved
                    previous_game_state,  # State before move
                    previous_player_color  # Player who moved
                )
                intermediate_rewards.append(intermediate_reward)
                
                if verbose and abs(intermediate_reward) > 0.01:
                    print(f"  Intermediate reward: {intermediate_reward:.4f}")
            else:
                intermediate_rewards.append(0.0)
            
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
            final_value = final_value_black if player_color == "B" else final_value_white
            
            # Combine final outcome with intermediate rewards if reward shaping is enabled
            if self.use_reward_shaping:
                value = calculate_position_value(
                    game,  # Final game state
                    player_color,
                    final_value,
                    intermediate_rewards,
                    i
                )
            else:
                value = final_value
            
            if self.use_symmetries:
                # Generate 8 symmetries with reward recalculation if reward shaping is enabled
                if self.use_reward_shaping and i < len(game_states_before) and i < len(game_states_after):
                    # Get game states for this position (before and after move)
                    game_state_before = game_states_before[i]
                    game_state_after = game_states_after[i]
                    sym_samples = self.generate_symmetries(
                        state, 
                        policy, 
                        value,
                        game_state_before=game_state_before,
                        game_state_after=game_state_after,
                        player_color=player_color,
                        final_outcome=final_value,
                        intermediate_rewards=intermediate_rewards,
                        move_index=i
                    )
                else:
                    # No reward shaping or missing game state - use original value for all symmetries
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

