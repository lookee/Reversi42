"""
Monte Carlo Tree Search (MCTS) for Reversi

Implements UCB1-based MCTS with neural network guidance.
Inspired by AlphaZero.
"""

import math
import numpy as np
import torch
import copy
from typing import List, Optional, Tuple, Dict
from collections import defaultdict

from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move
from ..utils.state_encoder import encode_state


class MCTSNode:
    """
    Node in MCTS tree.
    """
    
    def __init__(self, game: BitboardGame, parent: Optional['MCTSNode'] = None, move: Optional[Move] = None):
        """
        Initialize MCTS node.
        
        Args:
            game: Current game state
            parent: Parent node (None for root)
            move: Move that led to this node
        """
        self.game = game
        self.parent = parent
        self.move = move
        
        # MCTS statistics
        self.visit_count = 0
        self.value_sum = 0.0
        self.value_estimate = 0.0  # From neural network
        
        # Children
        self.children: Dict[Move, 'MCTSNode'] = {}
        self.legal_moves: List[Move] = game.get_move_list()
        self.is_expanded = False
        
        # Prior probabilities from neural network
        self.prior_probs: Dict[Move, float] = {}
    
    def is_terminal(self) -> bool:
        """Check if node is terminal (game over)."""
        return self.game.is_finish()
    
    def get_value(self) -> float:
        """Get average value of this node."""
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count
    
    def ucb_score(self, c_puct: float = 1.0) -> float:
        """
        Calculate UCB1 score for selection.
        
        Args:
            c_puct: Exploration constant
            
        Returns:
            UCB score
        """
        if self.visit_count == 0:
            return float('inf')
        
        exploitation = self.get_value()
        exploration = c_puct * math.sqrt(
            math.log(self.parent.visit_count + 1) / (self.visit_count + 1)
        )
        
        return exploitation + exploration
    
    def select_child(self, c_puct: float = 1.0) -> 'MCTSNode':
        """
        Select child with highest UCB score.
        
        Args:
            c_puct: Exploration constant
            
        Returns:
            Selected child node
        """
        if not self.children:
            return None
        
        best_score = float('-inf')
        best_child = None
        
        for move, child in self.children.items():
            # UCB1 formula with prior
            if child.visit_count == 0:
                # Use prior probability for unvisited nodes
                prior = self.prior_probs.get(move, 0.0)
                score = c_puct * prior * math.sqrt(self.visit_count + 1) / (child.visit_count + 1)
            else:
                # Standard UCB1
                exploitation = child.get_value()
                exploration = c_puct * self.prior_probs.get(move, 0.0) * math.sqrt(
                    self.visit_count + 1
                ) / (child.visit_count + 1)
                score = exploitation + exploration
            
            if score > best_score:
                best_score = score
                best_child = child
        
        return best_child
    
    def expand(self, prior_probs: Dict[Move, float]):
        """
        Expand node by creating children.
        
        Args:
            prior_probs: Prior probabilities for each legal move
        """
        if self.is_expanded:
            return
        
        self.is_expanded = True
        self.prior_probs = prior_probs
        
        # Create children for each legal move
        for move in self.legal_moves:
            # Create new game state by copying
            new_game = copy.deepcopy(self.game)
            if new_game.valid_move(move):
                new_game.move(move)
                child = MCTSNode(new_game, parent=self, move=move)
                self.children[move] = child
    
    def backup(self, value: float):
        """
        Backpropagate value up the tree.
        
        Args:
            value: Value to backpropagate (from perspective of node's player)
        """
        self.visit_count += 1
        self.value_sum += value
        
        # Backpropagate to parent (with sign flip for opponent)
        if self.parent is not None:
            self.parent.backup(-value)  # Flip sign for opponent perspective
    
    def get_visit_distribution(self, temperature: float = 1.0) -> Dict[Move, float]:
        """
        Get visit count distribution as probabilities.
        
        Args:
            temperature: Temperature for softmax (1.0 = normal, 0.0 = deterministic)
            
        Returns:
            Dictionary mapping moves to probabilities
        """
        if not self.children:
            return {}
        
        visit_counts = {move: child.visit_count for move, child in self.children.items()}
        total_visits = sum(visit_counts.values())
        
        if total_visits == 0:
            # Uniform distribution if no visits
            return {move: 1.0 / len(self.children) for move in self.children.keys()}
        
        # Apply temperature
        if temperature == 0.0:
            # Deterministic: return move with most visits
            best_move = max(visit_counts.items(), key=lambda x: x[1])[0]
            return {move: 1.0 if move == best_move else 0.0 for move in visit_counts.keys()}
        
        # Softmax with temperature
        visit_probs = {}
        for move, count in visit_counts.items():
            visit_probs[move] = (count / total_visits) ** (1.0 / temperature)
        
        # Normalize
        total_prob = sum(visit_probs.values())
        return {move: prob / total_prob for move, prob in visit_probs.items()}


class MCTS:
    """
    Monte Carlo Tree Search with neural network guidance.
    """
    
    def __init__(
        self,
        neural_network,
        c_puct: float = 1.0,
        num_simulations: int = 800,
        dirichlet_alpha: float = 0.3,
        dirichlet_epsilon: float = 0.25,
    ):
        """
        Initialize MCTS.
        
        Args:
            neural_network: NeuralNetwork instance
            c_puct: Exploration constant for UCB1
            num_simulations: Number of MCTS simulations per move
            dirichlet_alpha: Dirichlet noise parameter
            dirichlet_epsilon: Weight of Dirichlet noise
        """
        self.neural_network = neural_network
        self.c_puct = c_puct
        self.num_simulations = num_simulations
        self.dirichlet_alpha = dirichlet_alpha
        self.dirichlet_epsilon = dirichlet_epsilon
    
    def search(self, game: BitboardGame, player_color: str, add_noise: bool = True) -> MCTSNode:
        """
        Perform MCTS search from given game state.
        
        Args:
            game: Current game state
            player_color: "B" or "W" - current player
            add_noise: Whether to add Dirichlet noise to root (for training)
            
        Returns:
            Root node with search results
        """
        # Ensure model is in eval mode (no gradients needed for inference)
        self.neural_network.eval_mode()
        
        root = MCTSNode(game)
        
        # Get initial policy and value from neural network
        state = encode_state(game, player_color, use_advanced_features=True, use_opening_book=True, device=self.neural_network.device)
        state_batch = state.unsqueeze(0)
        
        policy_logits, value = self.neural_network.forward(state_batch)
        policy_probs = torch.softmax(policy_logits[0], dim=0).detach().cpu().numpy()
        
        # Map policy to moves
        prior_probs = {}
        legal_moves = game.get_move_list()
        
        if len(legal_moves) == 0:
            # No legal moves - pass
            root.value_estimate = value.item()
            return root
        
        # Create move to index mapping
        move_to_idx = {}
        for i, move in enumerate(legal_moves):
            # Convert move to index (0-63)
            row = move.get_y() - 1  # Move uses 1-based indexing
            col = move.get_x() - 1
            idx = row * 8 + col
            move_to_idx[move] = idx
        
        # Extract prior probabilities for legal moves
        for move in legal_moves:
            idx = move_to_idx[move]
            prior_probs[move] = policy_probs[idx]
        
        # Add Dirichlet noise for exploration (only at root, only during training)
        if add_noise and len(legal_moves) > 1:
            noise = np.random.dirichlet([self.dirichlet_alpha] * len(legal_moves))
            for i, move in enumerate(legal_moves):
                prior_probs[move] = (
                    (1 - self.dirichlet_epsilon) * prior_probs[move] +
                    self.dirichlet_epsilon * noise[i]
                )
        
        # Normalize
        total_prob = sum(prior_probs.values())
        prior_probs = {move: prob / total_prob for move, prob in prior_probs.items()}
        
        root.value_estimate = value.item()
        root.expand(prior_probs)
        
        # Perform simulations
        # Log progress every 10% of simulations
        log_interval = max(1, self.num_simulations // 10)
        for sim_idx in range(self.num_simulations):
            node = root
            
            # Selection: traverse to leaf
            while node.is_expanded and node.children:
                node = node.select_child(self.c_puct)
                if node is None:
                    break
            
            # Expansion and evaluation
            if not node.is_terminal():
                # Get neural network prediction
                current_player = node.game.turn
                state = encode_state(
                    node.game,
                    current_player,
                    use_advanced_features=True,
                    use_opening_book=True,
                    device=self.neural_network.device
                )
                state_batch = state.unsqueeze(0)
                
                # Use torch.no_grad() to disable gradient computation
                with torch.no_grad():
                    policy_logits, value = self.neural_network.forward(state_batch)
                    policy_probs = torch.softmax(policy_logits[0], dim=0).cpu().numpy()
                
                # Expand node
                legal_moves = node.game.get_move_list()
                if len(legal_moves) > 0:
                    prior_probs = {}
                    for move in legal_moves:
                        row = move.get_y() - 1
                        col = move.get_x() - 1
                        idx = row * 8 + col
                        prior_probs[move] = policy_probs[idx]
                    
                    # Normalize
                    total_prob = sum(prior_probs.values())
                    prior_probs = {move: prob / total_prob for move, prob in prior_probs.items()}
                    
                    node.expand(prior_probs)
                    node.value_estimate = value.item()
                else:
                    # No legal moves - game might be over
                    node.value_estimate = 0.0
            else:
                # Terminal node - get game result
                black_count = bin(node.game.black).count('1')
                white_count = bin(node.game.white).count('1')
                
                if black_count > white_count:
                    node.value_estimate = 1.0 if node.game.turn == "B" else -1.0
                elif white_count > black_count:
                    node.value_estimate = 1.0 if node.game.turn == "W" else -1.0
                else:
                    node.value_estimate = 0.0
            
            # Backpropagation
            node.backup(node.value_estimate)
            
            # Log progress
            if (sim_idx + 1) % log_interval == 0:
                progress = (sim_idx + 1) / self.num_simulations * 100
                print(f"  MCTS progress: {sim_idx + 1}/{self.num_simulations} simulations ({progress:.0f}%)", end='\r')
        
        # Clear progress line
        print(" " * 60, end='\r')
        
        return root
    
    def get_best_move(self, game: BitboardGame, player_color: str, temperature: float = 0.0) -> Optional[Move]:
        """
        Get best move using MCTS.
        
        Args:
            game: Current game state
            player_color: Current player color
            temperature: Temperature for move selection (0.0 = deterministic)
            
        Returns:
            Best move or None if no legal moves
        """
        root = self.search(game, player_color, add_noise=False)
        
        if not root.children:
            return None
        
        # Get visit distribution
        visit_dist = root.get_visit_distribution(temperature)
        
        if not visit_dist:
            return None
        
        # Sample move according to distribution
        moves = list(visit_dist.keys())
        probs = list(visit_dist.values())
        selected_move = np.random.choice(moves, p=probs)
        
        return selected_move

