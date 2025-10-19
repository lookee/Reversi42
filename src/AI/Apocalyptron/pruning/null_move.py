"""
Null move pruning.

If giving the opponent a free move still doesn't help them,
we can safely prune this branch.

Extracted from GrandmasterEngine (lines 354-384).
"""

from AI.Apocalyptron.pruning.interfaces import PruningStrategy, PruningResult


class NullMovePruning(PruningStrategy):
    """
    Null move pruning strategy.
    
    Idea: If our position is so strong that even giving the opponent
    a free move (passing our turn) still results in a beta cutoff,
    then we can safely prune this branch.
    
    Conditions for attempting null move:
    - depth >= 3 (not too shallow)
    - Not in endgame (few pieces left)
    - Not forced to pass already
    - Not in critical position (alpha/beta not near infinity)
    - allow_null_move flag is True
    
    Reduction factor R = 2 (search at depth - R - 1)
    
    Provides 1.5-2.5x speedup in midgame.
    """
    
    REDUCTION_FACTOR = 2
    MIN_DEPTH = 3
    ENDGAME_THRESHOLD = 52  # Last 12 moves
    
    def __init__(self):
        """Initialize null move pruning"""
        self.attempts = 0
        self.cutoffs = 0
    
    def should_prune(self, context) -> PruningResult:
        """
        Check if null move pruning applies.
        
        This is a READ-ONLY check - actual null move search
        must be performed by the calling code.
        
        Args:
            context: SearchContext with search state
            
        Returns:
            PruningResult (should_prune=False, this is a SUGGESTION)
        """
        # Note: Null move pruning requires actually making a null move
        # and searching, so it can't be decided here without game state.
        # This is a placeholder - actual implementation needs to be in search.
        
        # Check preconditions
        if not context.allow_null_move:
            return PruningResult(False, reason="null_move_disabled")
        
        if context.depth < self.MIN_DEPTH:
            return PruningResult(False, reason="depth_too_shallow")
        
        # This is a READ-ONLY check - cannot actually perform null move here
        # Return False (caller must implement actual null move search)
        return PruningResult(False, reason="null_move_requires_search")
    
    def can_attempt_null_move(self, game, depth: int, alpha: int, beta: int,
                             allow_null_move: bool, move_list: list) -> bool:
        """
        Check if null move pruning can be attempted.
        
        This is the actual condition check extracted from GrandmasterEngine.
        
        Args:
            game: Current game state
            depth: Remaining depth
            alpha, beta: Alpha-beta window
            allow_null_move: Whether null move is allowed
            move_list: Available moves
            
        Returns:
            bool: True if null move should be attempted
        """
        INFINITY = 999999
        
        # Check all conditions
        if not allow_null_move:
            return False
        
        if depth < self.MIN_DEPTH:
            return False
        
        if len(move_list) == 0:  # Forced to pass
            return False
        
        if beta >= INFINITY - 1000:  # Critical situation
            return False
        
        if alpha <= -INFINITY + 1000:  # Critical situation
            return False
        
        # Check if in endgame
        piece_count = game.black_cnt + game.white_cnt
        if piece_count >= self.ENDGAME_THRESHOLD:
            return False
        
        return True
    
    def record_attempt(self):
        """Record that null move was attempted"""
        self.attempts += 1
    
    def record_cutoff(self):
        """Record that null move caused cutoff"""
        self.cutoffs += 1
    
    def get_statistics(self) -> dict:
        """Get null move statistics"""
        success_rate = (self.cutoffs / self.attempts * 100) if self.attempts > 0 else 0
        return {
            'attempts': self.attempts,
            'cutoffs': self.cutoffs,
            'success_rate': success_rate,
        }
    
    def reset_statistics(self):
        """Reset statistics"""
        self.attempts = 0
        self.cutoffs = 0

