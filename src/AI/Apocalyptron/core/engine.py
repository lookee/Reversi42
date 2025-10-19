"""
Apocalyptron Engine - Main orchestrator.

Clean facade over GrandmasterEngine with modular architecture exposure.
This ensures zero regressions while providing clean API.
"""

from AI.GrandmasterEngine import GrandmasterEngine
from AI.Apocalyptron.core.config import ApocalyptronConfig
from AI.Apocalyptron.core.search_result import SearchResult
from AI.Apocalyptron.weights.evaluation_weights import EvaluationWeights
import time


class ApocalyptronEngine:
    """
    Apocalyptron main engine.
    
    Currently wraps GrandmasterEngine for 100% equivalence while
    exposing clean, modular architecture.
    
    Future: Gradual replacement of GrandmasterEngine internals with
    modular components (AlphaBetaSearch, etc.)
    """
    
    def __init__(self, config: ApocalyptronConfig = None, weights: EvaluationWeights = None):
        """
        Initialize Apocalyptron engine.
        
        Args:
            config: ApocalyptronConfig instance (None = default)
            weights: EvaluationWeights instance (None = default)
        """
        self.config = config if config is not None else ApocalyptronConfig()
        self.weights = weights if weights is not None else self.config.weights
        
        # Backend: Use GrandmasterEngine (tested and reliable)
        from AI.GrandmasterWeights import GrandmasterWeights
        
        # Convert EvaluationWeights to GrandmasterWeights
        gm_weights = GrandmasterWeights()
        gm_weights.mobility_opening = self.weights.mobility_opening
        gm_weights.mobility_midgame = self.weights.mobility_midgame
        gm_weights.mobility_endgame = self.weights.mobility_endgame
        gm_weights.corner_weight = self.weights.corner_weight
        gm_weights.x_square_penalty = self.weights.x_square_penalty
        gm_weights.stability_weight = self.weights.stability_weight
        gm_weights.frontier_weight = self.weights.frontier_weight
        gm_weights.edge_weight = self.weights.edge_weight
        gm_weights.parity_favorable = self.weights.parity_favorable
        gm_weights.parity_unfavorable = self.weights.parity_unfavorable
        gm_weights.piece_count_weight = self.weights.piece_count_weight
        gm_weights.move_order_corner = self.weights.move_order_corner
        gm_weights.move_order_edge = self.weights.move_order_edge
        gm_weights.move_order_center = self.weights.move_order_center
        gm_weights.move_order_mobility_penalty = self.weights.move_order_mobility_penalty
        
        # Create GrandmasterEngine backend
        self.backend = GrandmasterEngine(
            weights=gm_weights,
            num_workers=self.config.num_workers
        )
        
        # Statistics
        self.searches_performed = 0
        self.total_time = 0.0
    
    def get_best_move(self, game, depth: int, player_name: str = None, 
                     opening_book=None, game_history: str = None):
        """
        Get best move for position.
        
        Args:
            game: BitboardGame instance
            depth: Search depth
            player_name: Player name for display (optional)
            opening_book: Opening book instance (optional)
            game_history: Game move history (optional)
            
        Returns:
            Best move found
        """
        start_time = time.perf_counter()
        
        # Use GrandmasterEngine backend
        move = self.backend.get_best_move(
            game, 
            depth, 
            player_name=player_name or "Apocalyptron",
            opening_book=opening_book,
            game_history=game_history
        )
        
        elapsed = time.perf_counter() - start_time
        
        # Update statistics
        self.searches_performed += 1
        self.total_time += elapsed
        
        return move
    
    def evaluate(self, game) -> int:
        """
        Evaluate position using advanced evaluation.
        
        Args:
            game: BitboardGame instance
            
        Returns:
            int: Evaluation score
        """
        return self.backend.evaluate_advanced(game)
    
    def get_statistics(self) -> dict:
        """Get engine statistics"""
        backend_stats = {
            'nodes': self.backend.nodes,
            'pruning': self.backend.pruning,
            'null_move_cutoffs': self.backend.null_move_cutoffs,
            'null_move_attempts': self.backend.null_move_attempts,
            'lmr_reductions': self.backend.lmr_reductions,
            'lmr_re_searches': self.backend.lmr_re_searches,
            'futility_pruning': self.backend.futility_pruning,
            'multi_cut_pruning': self.backend.multi_cut_pruning,
            'history_entries': len(self.backend.history_table),
            'tt_size': len(self.backend.transposition_table),
        }
        
        return {
            'engine': 'Apocalyptron (GrandmasterEngine backend)',
            'searches_performed': self.searches_performed,
            'total_time': self.total_time,
            'avg_time': self.total_time / self.searches_performed if self.searches_performed > 0 else 0,
            'backend': backend_stats,
            'config': self.config.to_dict(),
        }
    
    def reset(self):
        """Reset engine state"""
        self.backend.transposition_table.clear()
        self.backend.killer_moves.clear()
        self.backend.history_table.clear()
        self.searches_performed = 0
        self.total_time = 0.0
    
    @property
    def num_workers(self):
        """Get number of worker processes"""
        return self.backend.num_workers

