"""
Adaptive Depth Search Strategy.

Adjusts search depth based on game phase (opening/midgame/endgame).
Optimizes resource allocation across game phases.
"""

from typing import Dict, List, Optional

from AI.Apocalyptron.observers.interfaces import SearchObserver
from AI.Apocalyptron.search.alphabeta_complete import AlphaBetaSearchComplete
from AI.Apocalyptron.search.iterative_deepening_strategy import IterativeDeepeningStrategy
from AI.Apocalyptron.search.strategy_interface import SearchStrategy


class AdaptiveDepthStrategy(SearchStrategy):
    """
    Adaptive depth search - varies depth by game phase.

    Adjusts search depth based on game phase:
    - Opening (0-19 pieces): Shallow search (position less critical)
    - Midgame (20-49 pieces): Standard depth (complex tactics)
    - Endgame (50-64 pieces): Deep search (exact calculation critical)

    Advantages:
    - Faster in opening (where deep search less valuable)
    - Deeper in endgame (where exactness matters most)
    - Better resource allocation

    Example:
        adaptive_config = {
            'opening': 7,   # Fast opening
            'midgame': 9,   # Standard midgame
            'endgame': 13   # Deep endgame
        }
    """

    def __init__(
        self,
        alphabeta: AlphaBetaSearchComplete,
        depth_config: Dict[str, int],
        observers: Optional[List[SearchObserver]] = None,
    ):
        """
        Initialize adaptive depth strategy.

        Args:
            alphabeta: AlphaBetaSearchComplete instance
            depth_config: Dict mapping phase → depth
                         {'opening': 7, 'midgame': 9, 'endgame': 13}
            observers: List of SearchObserver instances
        """
        self.alphabeta = alphabeta
        self.depth_config = depth_config
        self.observers = observers or []

        # Use IterativeDeepeningStrategy internally for better observer notifications
        # This gives us all the intermediate logs and iterations
        self.iterative_search = IterativeDeepeningStrategy(
            alphabeta, use_aspiration=True, observers=observers
        )

        # Validate depth config
        required_phases = {"opening", "midgame", "endgame"}
        if not required_phases.issubset(depth_config.keys()):
            raise ValueError(f"depth_config must include: {required_phases}")

    def get_best_move(
        self, game, depth: int, player_name: Optional[str] = None, opening_book=None, game_history: Optional[str] = None
    ):
        """
        Get best move using adaptive depth.

        Detects game phase and adjusts depth accordingly.

        Args:
            game: BitboardGame instance
            depth: Base/default depth (overridden by phase detection)
            player_name: Player name for display
            opening_book: Opening book instance
            game_history: Game history string

        Returns:
            Best move found
        """
        # Detect game phase
        phase = self._detect_phase(game)

        # Get depth for this phase
        actual_depth = self.depth_config.get(phase, depth)

        # Search at adjusted depth using iterative deepening
        return self.iterative_search.get_best_move(
            game, actual_depth, player_name, opening_book, game_history
        )

    def reset(self):
        """Reset search state"""
        self.iterative_search.reset()

    def add_observer(self, observer: SearchObserver):
        """Add an observer dynamically"""
        if observer and observer not in self.observers:
            self.observers.append(observer)
            # Propagate to internal search strategy
            self.iterative_search.add_observer(observer)

    def remove_observer(self, observer: SearchObserver):
        """Remove an observer"""
        if observer and observer in self.observers:
            self.observers.remove(observer)
            # Propagate to internal search strategy
            self.iterative_search.remove_observer(observer)

    def _detect_phase(self, game) -> str:
        """
        Detect game phase based on piece count.

        Args:
            game: BitboardGame instance

        Returns:
            Phase name: 'opening', 'midgame', or 'endgame'
        """
        total_pieces = game.black_cnt + game.white_cnt

        if total_pieces < 20:
            return "opening"
        elif total_pieces < 50:
            return "midgame"
        else:
            return "endgame"

    def get_current_phase(self, game) -> str:
        """
        Get current game phase (public method for testing).

        Args:
            game: BitboardGame instance

        Returns:
            Phase name: 'opening', 'midgame', or 'endgame'
        """
        return self._detect_phase(game)

    def get_depth_for_phase(self, phase: str) -> int:
        """
        Get configured depth for a specific phase.

        Args:
            phase: Phase name ('opening', 'midgame', 'endgame')

        Returns:
            Configured depth for that phase
        """
        return self.depth_config.get(phase, 9)  # Default 9 if not found
